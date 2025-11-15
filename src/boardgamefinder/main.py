# src/boardgamefinder/main.py

from .adapters.firestore_repository import get_listing_repository
from .adapters.ocr_client import OcrClient
from .adapters.llm_client import get_llm_client
from .adapters.bgg_repository import get_bgg_repository
from .services.extractor import JsonNameExtractor
from .services.matcher import FuzzyNameMatcher
from .pipeline.enrich_listing import ListingEnricher
from .pipeline.run_pipeline import run_pipeline
from .web.generator import WebGenerator


def main():
    print("Initializing components for scheduled run...")
    listing_repo = get_listing_repository()
    ocr_client = OcrClient()
    llm_client = get_llm_client()
    bgg_repo = get_bgg_repository()

    extractor = JsonNameExtractor(client=llm_client)
    matcher = FuzzyNameMatcher(repository=bgg_repo)
    enricher = ListingEnricher(
        ocr_client=ocr_client,
        extractor=extractor,
        matcher=matcher,
    )

    # 1) Run the pipeline
    new_count = run_pipeline(enricher=enricher, repo=listing_repo)

    # 2) Only regenerate the website if we actually found new listings
    if new_count > 0:
        print(f"{new_count} new listings found – regenerating website...")
        generator = WebGenerator(listing_repo)
        generator.generate_site()
    else:
        print("No new listings – skipping website generation.")


if __name__ == "__main__":
    main()
