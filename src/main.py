# src/main.py
from config import settings
from scraper import fetch_listings

from bgg import BGGFileRepository, FuzzyNameMatcher
from processing import ListingProcessor

from extractors import NameExtractor
from llm_client import AzureOpenAILLM


def main():
    # --- 1. Data retrieval ---
    listings = fetch_listings(
        zip_code=settings.zip_code,
        distance_km=settings.distance_km,
        limit=settings.max_listings,
        category_name=settings.marktplaats_category_name
    )

    # --- 2. Services ---
    # llm_client = TogetherChatClient(
    #     api_key=settings.together_api_key,
    #     model=settings.together_llm_model
    # )
    llm_client = AzureOpenAILLM()
    name_extractor = NameExtractor(client=llm_client)

    bgg_repo = BGGFileRepository()
    matcher = FuzzyNameMatcher(repository=bgg_repo)

    processor = ListingProcessor(name_extractor=name_extractor, bgg_matcher=matcher)

    # --- 3. Execution ---
    for listing in listings:
        enriched_listing = processor.enrich_listing(listing)
        print(enriched_listing)


if __name__ == "__main__":
    main()
