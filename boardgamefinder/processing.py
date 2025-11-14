# boardgamefinder/processing.py
from .models import Listing, Game, BGGData
from .matchers import NameMatcher
from .extractors import NameExtractor
from .ocr import extract_text_from_image_urls

class ListingProcessor:
    """
    Handles the enrichment of a Listing object by extracting game names
    and matching them to BGG data.
    """
    def __init__(self, name_extractor: NameExtractor, bgg_matcher: NameMatcher):
        self.name_extractor = name_extractor
        self.bgg_matcher = bgg_matcher

    def enrich_listing(self, listing: Listing) -> Listing:
        """
        Orchestrates the extraction of game names and matching with BGG data.
        """
        # 1. Extract text from images
        listing.image_texts = extract_text_from_image_urls(listing.images)

        # 2. Extract game names (+ language) using title, description, and image texts
        extracted = self.name_extractor.extract(
            title=listing.title,
            description=listing.description
        )
        listing.games = [Game(llm_name=item["name"], llm_lang=item["lang"]) for item in extracted]

        # 3. Match each game with BGG data
        for game in listing.games:
            self._match_bgg_data(game)

        return listing

    def _match_bgg_data(self, game: Game) -> None:
        """Matches the LLM name to BGG data and adds it to the Game object."""
        row = self.bgg_matcher.match_name(game.llm_name)

        if row is not None:
            bgg_data = BGGData(
                link=f"https://boardgamegeek.com/boardgame/{str(row['BGGId'])}",
                name=row["Name"],
                year_published=int(row["YearPublished"]),
                weight=float(row["GameWeight"]),
                rating=float(row["AvgRating"]),
            )
            game.bgg_data.append(bgg_data)