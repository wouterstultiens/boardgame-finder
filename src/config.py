from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Marktplaats
    zip_code: str
    distance_km: int
    max_listings: int
    marktplaats_category_name: str

    # LLM
    together_api_key: str
    together_llm_model: str

    # BGG
    bgg_enabled: bool
    bgg_min_rating: float
    bgg_min_weight: float
    bgg_max_weight: float

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
