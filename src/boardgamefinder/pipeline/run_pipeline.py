# src/boardgamefinder/pipeline/run_pipeline.py
from ..config import settings
from ..adapters.marktplaats_client import MarktplaatsClient
from ..adapters.firestore_repository import ListingRepository
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