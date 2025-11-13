from abc import ABC, abstractmethod
from typing import Optional
import difflib

import pandas as pd

COLS = ["BGGId", "Name", "Description", "YearPublished", "GameWeight", "AvgRating"]


def load_bgg(path: str = "bgg_data/games.csv") -> pd.DataFrame:
    return pd.read_csv(path)[COLS]


class NameMatcher(ABC):
    """
    Abstract matcher: can be implemented with fuzzy, embeddings, etc.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    @abstractmethod
    def match_name(self, name: str) -> Optional[pd.Series]:
        """
        Return the best matching BGG row, or None.
        """
        ...


class FuzzyNameMatcher(NameMatcher):
    """
    Very simple fuzzy matcher using difflib.
    """

    def __init__(self, df: pd.DataFrame, cutoff: float = 0.6):
        super().__init__(df)
        self.cutoff = cutoff
        self._names = df["Name"].astype(str).tolist()

    def match_name(self, name: str) -> Optional[pd.Series]:
        best = difflib.get_close_matches(
            name,
            self._names,
            n=1,
            cutoff=self.cutoff,
        )
        if not best:
            return None
        best_name = best[0]
        idx = self._names.index(best_name)
        return self.df.iloc[idx]
