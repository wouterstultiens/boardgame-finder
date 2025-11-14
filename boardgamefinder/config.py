# src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional

class Settings(BaseSettings):
    # Marktplaats
    zip_code: str
    distance_km: int
    max_listings: int
    offset: int
    marktplaats_category_name: str

    # LLM provider
    llm_provider: Literal["azure", "together"]

    # Together LLM
    together_api_key: Optional[str]
    together_llm_model: Optional[str]

    # Azure LLM
    ssl_cert_file: Optional[str]
    azure_client_id: Optional[str]
    azure_tenant_id: Optional[str]
    azure_client_secret: Optional[str]

    # Extraction selection
    extraction_method: Literal["json"]

    # Matching selection
    matching_method: Literal["fuzzy", "echo"]

    # BGG
    bgg_repo: Literal["file", "dummy"]
    bgg_min_rating: float
    bgg_min_weight: float
    bgg_max_weight: float

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()