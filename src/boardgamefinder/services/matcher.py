# src/boardgamefinder/services/matcher.py
import difflib
import re
from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd

from ..adapters.bgg_repository import BGGRepository
from ..domain.models import BGGData

def _normalize_name(s: str) -> str:
    """Normalizes a game name for robust matching."""
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s) # Keep only letters, digits, and spaces
    s = re.sub(r"\s+", " ", s) # Collapse multiple spaces
    return s.strip()

class NameMatcher(ABC):
    """Abstract interface for matching a name to a BGG game entry."""
    def __init__(self, repository: BGGRepository):
        self.df = repository.get_all_games()
        # Pre-filter out entries without a name
        self.df = self.df[self.df["Name"].notna()].copy()

    @abstractmethod
    def match(self, name: str) -> Optional[BGGData]:
        ...

class FuzzyNameMatcher(NameMatcher):
    """Matches names using a fuzzy string matching algorithm."""
    def __init__(self, repository: BGGRepository, cutoff: float = 0.7):
        super().__init__(repository)
        self.cutoff = cutoff
        self._names = self.df["Name"].astype(str).tolist()
        self._norm_names = [_normalize_name(n) for n in self._names]
        print(f"FuzzyNameMatcher initialized with {len(self._names)} BGG entries.")

    def match(self, name: str) -> Optional[BGGData]:
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
            year_published=int(row["YearPublished"]) if pd.notna(row["YearPublished"]) else None,
            weight=float(row["GameWeight"]) if pd.notna(row["GameWeight"]) else None,
            rating=float(row["AvgRating"]) if pd.notna(row["AvgRating"]) else None,
            image_path=row["ImagePath"] if pd.notna(row["ImagePath"]) else None,
        )