from config import settings
from llm import TogetherLLM
from scraper import fetch_listings

from bgg import BGGFileRepository, FuzzyNameMatcher
from processing import ListingProcessor 


def main():
    # --- 1. Data retrieval ---
    listings = fetch_listings(
        zip_code=settings.zip_code,
        distance_km=settings.distance_km,
        limit=settings.max_listings,
        category_name=settings.marktplaats_category_name
    )

    # --- 2. Services ---
    llm = TogetherLLM(
        api_key=settings.together_api_key,
        model=settings.together_llm_model
    )
    bgg_repo = BGGFileRepository() # Create the repository
    matcher = FuzzyNameMatcher(bgg_repo) # Pass repo dependency to matcher
    processor = ListingProcessor(llm=llm, bgg_matcher=matcher)

    # --- 3. Execution ---
    for listing in listings:
        enriched_listing = processor.enrich_listing(listing)
        
        print(enriched_listing) 


if __name__ == "__main__":
    main()