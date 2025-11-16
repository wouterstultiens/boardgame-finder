# src/boardgamefinder/pipeline/enrich_listing.py
from ..domain.models import Game, Listing
from ..services.extractor import NameExtractor
from ..services.matcher import NameMatcher
from ..adapters.ocr_client import OcrClient

class ListingEnricher:
    """
    Handles the full enrichment of a Listing object by coordinating OCR,
    LLM extraction, and BGG name matching.
    """
    def __init__(self, ocr_client: OcrClient, extractor: NameExtractor, matcher: NameMatcher):
        self.ocr_client = ocr_client
        self.extractor = extractor
        self.matcher = matcher
        print("ListingEnricher initialized.")

    def enrich(self, listing: Listing) -> Listing:
        """Orchestrates the enrichment process for a single listing."""
        print(f"Enriching listing: {listing.title}")
        
        # 1. Extract text from images via OCR
        listing.image_texts = self.ocr_client.extract_text_from_urls(listing.images)

        # 2. Extract game names using the LLM
        extracted_games_data = self.extractor.extract(
            title=listing.title,
            description=listing.description,
            image_texts=listing.image_texts
        )
        
        # This will overwrite any existing games on the listing
        listing.games = [Game(**item) for item in extracted_games_data]

        # 3. Match each extracted game with BGG data
        for game in listing.games:
            bgg_match = self.matcher.match(game.llm_name, game.llm_lang)
            if bgg_match:
                game.bgg_data = bgg_match

        print(f"Enrichment complete for: {listing.title}")
        return listing