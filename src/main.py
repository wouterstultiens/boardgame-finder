from config import settings
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

    print(listings[0])

if __name__ == "__main__":
    main()