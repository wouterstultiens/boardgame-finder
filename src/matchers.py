import difflib
from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd

from bgg import BGGRepository


class NameMatcher(ABC):
    def __init__(self, repository: BGGRepository):
        self.df = repository.get_all_games()

    @abstractmethod
    def match_name(self, name: str) -> Optional[pd.Series]:
        """
        Return the best matching BGG row, or None.
        """
        ...


class FuzzyNameMatcher(NameMatcher):
    def __init__(self, repository: BGGRepository):
        super().__init__(repository)
        self._names = self.df["Name"].astype(str).tolist()

    def match_name(self, name: str) -> Optional[pd.Series]:
        best = difflib.get_close_matches(
            name,
            self._names,
            n=1,
            cutoff=0.6,
        )
        if not best:
            return None
        best_name = best[0]
        idx = self._names.index(best_name)
        return self.df.iloc[idx]


class EchoNameMatcher(NameMatcher):
    def match_name(self, name: str) -> Optional[pd.Series]:
        return None


def make_name_matcher(method: str, repository: BGGRepository) -> NameMatcher:
    if method == "fuzzy":
        return FuzzyNameMatcher(repository=repository)
    elif method == "echo":
        return EchoNameMatcher(repository=repository)
    else:
        raise ValueError("Wrong value for method NameMatcher")
