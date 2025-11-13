from typing import List
from marktplaats import SearchQuery, SortBy, SortOrder, category_from_name

from src.models import Listing, ListingImage

def _to_listing_data(listing) -> Listing:
    # Robust against missing fields in the lib
    images = []
    for img in listing.get_images():
        images.append(ListingImage(url=str(img)))

    city = None
    distance = None
    try:
        city = listing.location.city
        distance = int(getattr(listing.location, "distance", None) or 0)
    except Exception:
        pass

    seller_name = None
    try:
        seller_name = listing.seller.name
    except Exception:
        pass

    return Listing(
        title=str(getattr(listing, "title", "")),
        description=str(getattr(listing, "description", "")),
        price=float(getattr(listing, "price", 0.0) or 0.0),
        price_type=str(getattr(listing, "price_type", None)),
        link=str(getattr(listing, "link", "")),
        city=city,
        distance_m=distance,
        seller_name=seller_name,
        date=getattr(listing, "date", None),
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

