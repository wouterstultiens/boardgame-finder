# src/boardgamefinder/config.py
from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Marktplaats Configuration
    zip_code: str = "7412XM"
    distance_km: int = 10
    max_listings: int = 50
    marktplaats_category_name: str = "Gezelschapsspellen | Bordspellen"

    # LLM Provider Configuration
    llm_provider: Literal["azure", "together"] = "azure"

    # Together LLM Settings
    together_api_key: Optional[str] = None
    together_llm_model: Optional[str] = "Qwen/Qwen3-Next-80B-A3B-Instruct"

    # Azure LLM Settings
    ssl_cert_file: Optional[str] = None
    azure_client_id: Optional[str] = None
    azure_tenant_id: Optional[str] = None
    azure_client_secret: Optional[str] = None

    # Core Services Configuration
    extraction_method: Literal["json"] = "json"
    matching_method: Literal["fuzzy", "llm"] = "llm"

    # BGG Data Source Configuration
    bgg_repository_type: Literal["gcs", "file", "dummy"] = "gcs"
    bgg_gcs_bucket_name: Optional[str] = "your-bgg-data-bucket"
    bgg_gcs_file_path: Optional[str] = "games.csv"
    bgg_local_file_path: Optional[str] = "bgg_data/games.csv" # For local fallback

    # BGG Filtering Rules
    bgg_min_rating: float = 0.0
    bgg_min_weight: float = 0.0
    bgg_max_weight: float = 5.0

    # Google Cloud Project Configuration
    google_application_credentials: Optional[str] = None
    gcp_project_id: Optional[str] = None

    # Web output
    web_output_dir: str = "docs"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Instantiate a single settings object for the application
settings = Settings()