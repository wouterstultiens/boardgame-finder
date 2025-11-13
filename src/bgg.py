from abc import ABC, abstractmethod
from typing import Optional
import difflib

import pandas as pd

COLS = ["BGGId", "Name", "Description", "YearPublished", "GameWeight", "AvgRating"]

# load_bgg function is removed

# --- Repository Abstraction (New) ---

class BGGRepository(ABC):
    """
    Abstract class for fetching BGG data, decoupling data access.
    """
    @abstractmethod
    def get_all_games(self) -> pd.DataFrame:
        ...

class BGGFileRepository(BGGRepository):
    """
    Concrete implementation that loads data from a local CSV file.
    """
    def __init__(self, path: str = "bgg_data/games.csv"):
        self._path = path
        self._df = None

    def get_all_games(self) -> pd.DataFrame:
        if self._df is None:
            self._df = pd.read_csv(self._path)[COLS]
        return self._df
        
# --- Matcher Classes (Modified) ---

class NameMatcher(ABC):
    """
    Abstract matcher: can be implemented with fuzzy, embeddings, etc.
    Now takes a BGGRepository dependency.
    """

    def __init__(self, repository: BGGRepository): # Changed dependency
        self.df = repository.get_all_games() # Load the data via the repo

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

    # Constructor now takes the repository
    def __init__(self, repository: BGGRepository, cutoff: float = 0.6): 
        super().__init__(repository) # Pass repo to parent
        self.cutoff = cutoff
        self._names = self.df["Name"].astype(str).tolist()

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