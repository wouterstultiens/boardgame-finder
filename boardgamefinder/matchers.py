# boardgamefinder/matchers.py
import difflib
import re
from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd

from .bgg import BGGRepository


def _normalize_name(s: str) -> str:
    s = s.lower()
    # keep only letters, digits and spaces
    s = re.sub(r"[^a-z0-9]+", " ", s)
    # collapse multiple spaces
    s = re.sub(r"\s+", " ", s)
    return s.strip()


class NameMatcher(ABC):
    def __init__(self, repository: BGGRepository):
        self.df = repository.get_all_games()

    @abstractmethod
    def match_name(self, name: str) -> Optional[pd.Series]:
        ...


class FuzzyNameMatcher(NameMatcher):
    def __init__(self, repository: BGGRepository):
        super().__init__(repository)
        self._names = self.df["Name"].astype(str).tolist()
        self._norm_names = [_normalize_name(n) for n in self._names]

    def match_name(self, name: str) -> Optional[pd.Series]:
        norm_query = _normalize_name(name)

        best = difflib.get_close_matches(
            norm_query,
            self._norm_names,
            n=1,
            cutoff=0.6,   # you can tweak this if needed
        )
        if not best:
            return None

        best_norm = best[0]
        idx = self._norm_names.index(best_norm)
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
