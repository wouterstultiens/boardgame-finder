# src/boardgamefinder/pipeline/run_pipeline.py
from ..config import settings
from ..adapters.marktplaats_client import MarktplaatsClient
from ..adapters.firestore_repository import ListingRepository, get_listing_repository
from ..adapters.ocr_client import OcrClient
from ..adapters.llm_client import get_llm_client
from ..adapters.bgg_repository import get_bgg_repository
from ..services.extractor import JsonNameExtractor
from ..services.matcher import FuzzyNameMatcher
from .enrich_listing import ListingEnricher

def run_pipeline(enricher: ListingEnricher, repo: ListingRepository):
    """Executes the full end-to-end data processing pipeline."""
    print("--- Starting BoardGameFinder Pipeline ---")

    # 1. Scrape new listings from Marktplaats
    mp_client = MarktplaatsClient()
    scraped_listings = mp_client.fetch_listings(
        zip_code=settings.zip_code,
        distance_km=settings.distance_km,
        limit=settings.max_listings,
        category_name=settings.marktplaats_category_name
    )

    new_listings_count = 0
    # 2. Process each listing
    for listing in scraped_listings:
        # Check if the listing already exists and has been processed
        cached = repo.find_by_link(str(listing.link))
        if cached and cached.games:
            print(f"Skipping already processed listing: {listing.title}")
            continue

        new_listings_count += 1
        # Enrich the new listing with games and BGG data
        enriched_listing = enricher.enrich(listing)

        # Save the result to the database
        repo.save(enriched_listing)

    print(f"--- Pipeline Finished ---")
    print(f"Processed {new_listings_count} new listings out of {len(scraped_listings)} found.")
    return new_listings_count


if __name__ == "__main__":
    # 1. Initialize all necessary components from adapters and services
    print("Initializing components for pipeline run...")
    listing_repo = get_listing_repository()
    ocr_client = OcrClient()
    llm_client = get_llm_client()
    bgg_repo = get_bgg_repository()

    # 2. Set up the extractor and matcher services
    extractor = JsonNameExtractor(client=llm_client)
    matcher = FuzzyNameMatcher(repository=bgg_repo)

    # 3. Create the main enricher service
    enricher = ListingEnricher(
        ocr_client=ocr_client,
        extractor=extractor,
        matcher=matcher
    )

    # 4. Run the pipeline with the configured components
    run_pipeline(enricher=enricher, repo=listing_repo)