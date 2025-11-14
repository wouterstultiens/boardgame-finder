from typing import List

import requests
from bs4 import BeautifulSoup
from marktplaats import SearchQuery, SortBy, SortOrder, category_from_name

from .models import Listing


def _full_description(url: str) -> str:
    try:
        html = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0 Safari/537.36"
                )
            },
        ).text

        soup = BeautifulSoup(html, "html.parser")
        desc_div = soup.select_one("div.Description-description")
        inner = desc_div.decode_contents()
        inner = inner.replace("<br/>", "\n").replace("<br />", "\n").replace("<br>", "\n")
        return BeautifulSoup(inner, "html.parser").get_text()
    except:
        print("\n\n\033[31mUNABLE TO GET FULL DESCRIPTION\033[0m\n\n")
        return ""


def _to_listing_data(listing) -> Listing:
    images = [str(img) for img in listing.get_images()]
    url = str(listing.link)

    return Listing(
        title=str(listing.title),
        description=_full_description(url) or listing.description,
        price=float(listing.price),
        price_type=str(listing.price_type),
        link=url,
        city=listing.location.city,
        distance_km=int(listing.location.distance / 1000),
        date=listing.date,
        images=images,
    )


def fetch_listings(
    zip_code: str,
    distance_km: int,
    category_name: str,
    limit: int,
) -> List[Listing]:
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
