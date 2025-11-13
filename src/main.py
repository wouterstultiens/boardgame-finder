from config import settings
from llm import TogetherLLM
from scraper import fetch_listings

from bgg import load_bgg, FuzzyNameMatcher


def main():
    # 1. Fetch listings from Marktplaats
    listings = fetch_listings(
        zip_code=settings.zip_code,
        distance_km=settings.distance_km,
        limit=settings.max_listings,
        category_name=settings.marktplaats_category_name
    )

    # 2. Init LLM
    llm = TogetherLLM(
        api_key=settings.together_api_key,
        model=settings.together_llm_model
    )

    # 3. Load BGG data + matcher
    bgg_df = load_bgg()
    matcher = FuzzyNameMatcher(bgg_df)

    # 4. Process listings
    for listing in listings:
        # Extract game names via LLM
        listing.extract_games(llm)

        # Match each extracted name to BGG
        for game in listing.games:
            row = matcher.match_name(game.llm_name)
            if row is not None:
                game.apply_bgg_row(row)

        print(listing)


if __name__ == "__main__":
    main()
