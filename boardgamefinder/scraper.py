from typing import List
import requests
import json
from bs4 import BeautifulSoup
from marktplaats import SearchQuery, SortBy, SortOrder, category_from_name
from .models import Listing


def _get_listing_details(url: str) -> tuple[list[str], str]:
    """
    Fetch images and description for a single listing in one HTTP request.
    """
    try:
        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0 Safari/537.36"
                )
            },
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # extract images from ld+json script
        images = []
        for data in soup.select('script[type="application/ld+json"]'):
            try:
                parsed = json.loads(data.text)
                if isinstance(parsed, dict) and parsed.get("@type") == "Product":
                    images.extend(f"https:{img}" for img in parsed.get("image", []))
                    break
            except json.JSONDecodeError:
                continue

        # extract description
        desc_div = soup.select_one("div.Description-description")
        if desc_div:
            inner = desc_div.decode_contents()
            inner = inner.replace("<br/>", "\n").replace("<br />", "\n").replace("<br>", "\n")
            description = BeautifulSoup(inner, "html.parser").get_text().strip()
        else:
            description = ""

        return images, description
    except Exception as e:
        print(f"\n\033[31mUNABLE TO GET DETAILS FOR {url}: {e}\033[0m\n")
        return [], ""


def _to_listing_data(listing) -> Listing:
    url = str(listing.link)
    images, full_description = _get_listing_details(url)

    return Listing(
        title=str(listing.title),
        description=full_description or listing.description,
        price=float(listing.price),
        price_type=str(listing.price_type),
        link=url,
        city=listing.location.city,
        distance_km=int(listing.location.distance / 1000),
        date=listing.date,
        images=images or [str(img) for img in listing.get_images()],
    )


def fetch_listings(
    zip_code: str,
    distance_km: int,
    category_name: str,
    limit: int,
) -> List[Listing]:
    """
    Fetch a list of listings and enrich each with images + full description.
    """
    search = SearchQuery(
        zip_code=zip_code,
        distance=distance_km * 1000,
        limit=limit,
        sort_by=SortBy.DATE,
        sort_order=SortOrder.DESC,
        category=category_from_name(category_name),
    )
    listings = search.get_listings()
    return [_to_listing_data(listing) for listing in listings]
