# src/processing.py
from typing import List
import pandas as pd

from models import Listing, Game, BGGData
from llm import BaseLLM
from bgg import NameMatcher 

class ListingProcessor:
    """
    Handles the enrichment of a Listing object by extracting game names
    and matching them to BGG data.
    """
    def __init__(self, llm: BaseLLM, bgg_matcher: NameMatcher):
        self.llm = llm
        self.bgg_matcher = bgg_matcher

    def enrich_listing(self, listing: Listing) -> Listing:
        """
        Orchestrates the extraction of game names and matching with BGG data.
        """
        # 1. Extract game names
        game_names = self.llm.extract_names(
            title=listing.title,
            description=listing.description
        )
        listing.games = [Game(llm_name=name) for name in game_names]

        # 2. Match each game with BGG data
        for game in listing.games:
            self._match_bgg_data(game)
        
        return listing

    def _match_bgg_data(self, game: Game) -> None:
        """Matches the LLM name to BGG data and adds it to the Game object."""
        # row will be pd.Series or None
        row = self.bgg_matcher.match_name(game.llm_name) 

        if row is not None:
            # Logic previously in Game.apply_bgg_row()
            bgg_data = BGGData(
                id=str(row["BGGId"]),
                name=row["Name"],
                description=row["Description"],
                year_published=int(row["YearPublished"]),
                weight=float(row["GameWeight"]),
                rating=float(row["AvgRating"]),
            )
            # The field is now named bgg_data
            game.bgg_data.append(bgg_data)