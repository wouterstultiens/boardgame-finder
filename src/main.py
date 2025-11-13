from config import settings
from llm import TogetherLLM
from scraper import fetch_listings

def main():
    listings = fetch_listings(
        zip_code=settings.zip_code,
        distance_km=settings.distance_km,
        limit=settings.max_listings,
        category_name=settings.marktplaats_category_name
    )

    llm = TogetherLLM(
        api_key=settings.together_api_key,
        model=settings.together_llm_model
    )

    for listing in listings:
        listing.extract_games(llm)
        print(listing)

if __name__ == "__main__":
    main()