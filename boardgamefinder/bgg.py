# src/bgg.py
from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd

COLS = ["BGGId", "Name", "YearPublished", "GameWeight", "AvgRating", "ImagePath"]


# --- Repository Abstraction ---

class BGGRepository(ABC):
    @abstractmethod
    def get_all_games(self) -> pd.DataFrame:
        ...


class BGGFileRepository(BGGRepository):
    def __init__(self, path: str = "bgg_data/games.csv"):
        self._path = path
        self._df: Optional[pd.DataFrame] = None

    def get_all_games(self) -> pd.DataFrame:
        if self._df is None:
            self._df = pd.read_csv(self._path)[COLS]
        return self._df


class DummyRepository(BGGRepository):
    def get_all_games(self) -> pd.DataFrame:
        return pd.DataFrame()


def make_bgg_repository(kind: str) -> BGGRepository:
    if kind == "file":
        return BGGFileRepository()
    elif kind == "dummy":
        return DummyRepository()
    else:
        raise ValueError("Wrong value for kind of BGGRepository")