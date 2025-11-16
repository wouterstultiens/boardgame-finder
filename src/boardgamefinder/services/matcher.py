# src/boardgamefinder/services/matcher.py
import difflib
import re
from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd

from ..adapters.bgg_repository import BGGRepository
from ..adapters.llm_client import LLM, Message
from ..domain.models import BGGData
from ..prompts import MATCHER_SYSTEM_PROMPT


def _normalize_name(s: str) -> str:
    """Normalizes a game name for robust matching."""
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)  # Keep only letters, digits, and spaces
    s = re.sub(r"\s+", " ", s)  # Collapse multiple spaces
    return s.strip()


class NameMatcher(ABC):
    """Abstract interface for matching a name to a BGG game entry."""

    def __init__(self, repository: BGGRepository):
        self.df = repository.get_all_games()
        # Pre-filter out entries without a name
        self.df = self.df[self.df["Name"].notna()].copy()

    @abstractmethod
    def match(self, name: str, llm_lang: str) -> Optional[BGGData]:
        ...


class FuzzyNameMatcher(NameMatcher):
    """Matches names using a fuzzy string matching algorithm."""

    def __init__(self, repository: BGGRepository, cutoff: float = 0.7):
        super().__init__(repository)
        self.cutoff = cutoff
        self._names = self.df["Name"].astype(str).tolist()
        self._norm_names = [_normalize_name(n) for n in self._names]
        print(f"FuzzyNameMatcher initialized with {len(self._names)} BGG entries.")

    def match(self, name: str, llm_lang: str) -> Optional[BGGData]:
        if not name:
            return None

        norm_query = _normalize_name(name)
        best_matches = difflib.get_close_matches(
            norm_query, self._norm_names, n=1, cutoff=self.cutoff
        )

        if not best_matches:
            return None

        best_norm = best_matches[0]
        idx = self._norm_names.index(best_norm)
        row = self.df.iloc[idx]

        print(f"Matched '{name}' -> '{row['Name']}' (BGGId: {row['BGGId']})")

        return BGGData(
            id=int(row["BGGId"]),
            link=f"https://boardgamegeek.com/boardgame/{row['BGGId']}",
            name=row["Name"],
            year_published=(
                int(row["YearPublished"]) if pd.notna(row["YearPublished"]) else None
            ),
            weight=float(row["GameWeight"]) if pd.notna(row["GameWeight"]) else None,
            rating=float(row["AvgRating"]) if pd.notna(row["AvgRating"]) else None,
            image_path=row["ImagePath"] if pd.notna(row["ImagePath"]) else None,
        )


class LLMNameMatcher(NameMatcher):
    """
    Matches names using a two-step fuzzy search combined with an LLM call
    to select the best candidate.
    """

    def __init__(
        self, repository: BGGRepository, llm_client: LLM, num_candidates: int = 20
    ):
        super().__init__(repository)
        self.llm_client = llm_client
        self.num_candidates = num_candidates
        self._names = self.df["Name"].astype(str).tolist()
        self._norm_names = [_normalize_name(n) for n in self._names]
        print(f"LLMNameMatcher initialized with {len(self._names)} BGG entries.")

    def _get_fuzzy_candidates(self, normalized_query: str) -> pd.DataFrame:
        """Finds top N fuzzy matches and returns them as a DataFrame."""
        matches = difflib.get_close_matches(
            normalized_query, self._norm_names, n=self.num_candidates, cutoff=0.6
        )
        if not matches:
            return pd.DataFrame()

        indices = [self._norm_names.index(match) for match in matches]
        return self.df.iloc[indices].copy()

    def _format_candidates_for_prompt(self, candidates_df: pd.DataFrame) -> str:
        """Formats a DataFrame of candidates into a list string for the LLM prompt."""
        if candidates_df.empty:
            return "No candidates found."

        return "\n".join(
            [f"- ID: {row['BGGId']}, Name: {row['Name']}" for _, row in candidates_df.iterrows()]
        )

    def match(self, name: str, llm_lang: str) -> Optional[BGGData]:
        if not name:
            return None

        # Step 1: Perform fuzzy search on base name and full name
        base_name = name.split(":")[0].strip()
        candidates_base = self._get_fuzzy_candidates(_normalize_name(base_name))
        candidates_full = self._get_fuzzy_candidates(_normalize_name(name))

        # Combine and deduplicate candidates
        all_candidates = (
            pd.concat([candidates_full, candidates_base])
            .drop_duplicates(subset=["BGGId"])
            .reset_index(drop=True)
        )

        if all_candidates.empty:
            print(f"No fuzzy candidates found for '{name}'.")
            return None

        print(f"\n--- Debugging Candidates for '{name}' ---")
        print(f"Found {len(all_candidates)} unique candidates:")
        for _, row in all_candidates.iterrows():
            print(f"  - ID: {row['BGGId']}, Name: {row['Name']}")
        print("------------------------------------------")

        # Step 2: Call LLM to select the best candidate
        prompt_candidates = self._format_candidates_for_prompt(all_candidates)
        user_prompt = f'Original game name: "{name}"\nllm_lang: "{llm_lang}"\n\nCandidate games:\n{prompt_candidates}'
        messages = [
            Message("system", MATCHER_SYSTEM_PROMPT),
            Message("user", user_prompt),
        ]
        llm_response = self.llm_client.get_response(messages, temperature=0.0)

        # Step 3: Parse LLM response and return the BGGData object
        response_text = llm_response.strip()
        print(f"LLM decision for '{name}': '{response_text}'")

        if response_text.lower() == "none" or not response_text.isdigit():
            return None

        try:
            best_id = int(response_text)
            match_row = self.df[self.df["BGGId"] == best_id].iloc[0]

            print(f"Matched '{name}' -> '{match_row['Name']}' (BGGId: {match_row['BGGId']})")

            return BGGData(
                id=int(match_row["BGGId"]),
                link=f"https://boardgamegeek.com/boardgame/{match_row['BGGId']}",
                name=match_row["Name"],
                year_published=(
                    int(match_row["YearPublished"])
                    if pd.notna(match_row["YearPublished"])
                    else None
                ),
                weight=float(match_row["GameWeight"]) if pd.notna(match_row["GameWeight"]) else None,
                rating=float(match_row["AvgRating"]) if pd.notna(match_row["AvgRating"]) else None,
                image_path=match_row["ImagePath"] if pd.notna(match_row["ImagePath"]) else None,
            )
        except (ValueError, IndexError):
            print(f"Warning: LLM returned an invalid BGG ID '{response_text}'.")
            return None