# src/boardgamefinder/adapters/bgg_repository.py
from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd
from io import BytesIO
from google.cloud import storage

from ..config import settings

COLS = ["BGGId", "Name", "YearPublished", "GameWeight", "AvgRating", "ImagePath"]

class BGGRepository(ABC):
    """Abstract interface for a repository of BoardGameGeek game data."""
    @abstractmethod
    def get_all_games(self) -> pd.DataFrame:
        ...

class BGGFileRepository(BGGRepository):
    """Loads BGG data from a local CSV file."""
    def __init__(self, path: str):
        self._path = path
        self._df: Optional[pd.DataFrame] = None
        print(f"Initializing BGGFileRepository with path: {self._path}")

    def get_all_games(self) -> pd.DataFrame:
        if self._df is None:
            print(f"Loading BGG data from local file: {self._path}...")
            self._df = pd.read_csv(self._path)[COLS]
            
            # At least 200 people should own it
            print("BGG data loaded successfully.")
        return self._df

class BGGGCSRepository(BGGRepository):
    """Loads BGG data from a CSV file in a Google Cloud Storage bucket."""
    def __init__(self, bucket_name: str, file_path: str):
        self._bucket_name = bucket_name
        self._file_path = file_path
        self._df: Optional[pd.DataFrame] = None
        self._storage_client = storage.Client()
        print(f"Initializing BGGGCSRepository with gs://{bucket_name}/{file_path}")

    def get_all_games(self) -> pd.DataFrame:
        if self._df is None:
            print(f"Loading BGG data from GCS: gs://{self._bucket_name}/{self._file_path}...")
            bucket = self._storage_client.bucket(self._bucket_name)
            blob = bucket.blob(self._file_path)
            
            data = blob.download_as_bytes()
            self._df = pd.read_csv(BytesIO(data))[COLS]
            print("BGG data loaded successfully.")
        return self._df

class DummyRepository(BGGRepository):
    """A dummy repository that returns an empty DataFrame, for testing."""
    def __init__(self):
        print("Initializing Dummy BGG Repository.")

    def get_all_games(self) -> pd.DataFrame:
        return pd.DataFrame(columns=COLS)

def get_bgg_repository() -> BGGRepository:
    """Factory function to create a BGGRepository based on app settings."""
    repo_type = settings.bgg_repository_type
    if repo_type == "gcs":
        return BGGGCSRepository(
            bucket_name=settings.bgg_gcs_bucket_name,
            file_path=settings.bgg_gcs_file_path,
        )
    elif repo_type == "file":
        return BGGFileRepository(path=settings.bgg_local_file_path)
    elif repo_type == "dummy":
        return DummyRepository()
    else:
        raise ValueError(f"Unknown BGG repository type: {repo_type}")