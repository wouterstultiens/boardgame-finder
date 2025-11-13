from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # scrape
    zip_code: str
    distance_km: int
    max_listings: int
    marktplaats_category_name: str

    # bgg
    bgg_enabled: bool = False
    bgg_min_rating: float = 7.2
    bgg_min_weight: float = 1.0
    bgg_max_weight: float = 3.5

    # llm
    llm_enabled: bool = True
    together_api_key: str | None = None
    llm_model: str = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
