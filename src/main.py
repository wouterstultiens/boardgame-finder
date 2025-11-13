from config import settings
from llm import TogetherLLM
from scraper import fetch_listings

def main():
    zip_code = settings.zip_code
    distance_km = settings.distance_km
    max_listings = settings.max_listings
    marktplaats_category_name = settings.marktplaats_category_name

    listings = fetch_listings(
        zip_code=zip_code,
        distance_km=distance_km,
        limit=max_listings,
        category_name=marktplaats_category_name
    )

    for listing in listings:
        llm = TogetherLLM()
        listing.games_llm = llm.extract_names(title=listing.title, description=listing.description)
        print(listing)

if __name__ == "__main__":
    main()