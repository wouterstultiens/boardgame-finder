# src/main.py
from .config import settings
from .scraper import fetch_listings

from .bgg import make_bgg_repository
from .matchers import make_name_matcher
from .processing import ListingProcessor

from .extractors import make_name_extractor
from .llm_client import make_llm


def main():
    # --- 1. Data retrieval ---
    listings = fetch_listings(
        zip_code=settings.zip_code,
        distance_km=settings.distance_km,
        limit=settings.max_listings,
        offset=settings.offset,
        category_name=settings.marktplaats_category_name
    )

    # --- 2. Services (configured via .env) ---
    llm_client = make_llm(
        provider=settings.llm_provider,
        model=settings.together_llm_model,
        api_key=settings.together_api_key,
    )
    name_extractor = make_name_extractor(method=settings.extraction_method, client=llm_client)

    bgg_repo = make_bgg_repository(kind=settings.bgg_repo)
    matcher = make_name_matcher(
        method=settings.matching_method,
        repository=bgg_repo
    )

    processor = ListingProcessor(name_extractor=name_extractor, bgg_matcher=matcher)

    # --- 3. Execution ---
    for listing in listings:
        enriched_listing = processor.enrich_listing(listing)
        print(enriched_listing)


if __name__ == "__main__":
    main()