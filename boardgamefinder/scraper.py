from typing import List
from marktplaats import SearchQuery, SortBy, SortOrder, category_from_name

from .models import Listing

def _to_listing_data(listing) -> Listing:
    images = [str(img) for img in listing.get_images()]

    return Listing(
        title=str(listing.title),
        description=str(listing.description),
        price=float(listing.price),
        price_type=str(listing.price_type),
        link=str(listing.link),
        city=listing.location.city,
        distance_km=int(listing.location.distance/1000),
        date=listing.date,
        images=images,
    )

def fetch_listings(
    zip_code: str,
    distance_km: int,
    category_name: str,
    limit: int
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
    out: List[Listing] = []
    for listing in listings:
        out.append(_to_listing_data(listing))
    return out

