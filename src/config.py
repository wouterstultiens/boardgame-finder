from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Marktplaats
    zip_code: str
    distance_km: int
    max_listings: int
    marktplaats_category_name: str

    # LLM
    llm_enabled: bool = True
    together_api_key: str | None = None
    llm_model: str = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

    # BGG
    bgg_enabled: bool
    bgg_min_rating: float
    bgg_min_weight: float
    bgg_max_weight: float

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
