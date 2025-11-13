from config import settings
from llm import TogetherLLM
from scraper import fetch_listings

def main():
    zip_code = settings.zip_code
    distance_km = settings.distance_km
    max_listings = settings.max_listings
    marktplaats_category_name = settings.marktplaats_category_name
    together_api_key = settings.together_api_key
    together_llm_model = settings.together_llm_model

    listings = fetch_listings(
        zip_code=zip_code,
        distance_km=distance_km,
        limit=max_listings,
        category_name=marktplaats_category_name
    )

    for listing in listings:
        llm = TogetherLLM(api_key=together_api_key, model=together_llm_model)
        listing.games_llm = llm.extract_names(title=listing.title, description=listing.description)
        print(listing)

if __name__ == "__main__":
    main()