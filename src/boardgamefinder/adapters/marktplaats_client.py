# src/boardgamefinder/adapters/marktplaats_client.py
import json
from typing import List, Tuple
import requests
from bs4 import BeautifulSoup
from marktplaats import SearchQuery, SortBy, SortOrder, category_from_name

from ..domain.models import Listing

class MarktplaatsClient:
    """A client to scrape listings from Marktplaats."""

    def __init__(self, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"):
        self.user_agent = user_agent
        print("MarktplaatsClient initialized.")

    def _get_listing_details(self, url: str) -> Tuple[List[str], str]:
        """Fetches images and the full description for a single listing."""
        try:
            response = requests.get(url, timeout=20, headers={"User-Agent": self.user_agent})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            images = []
            for data in soup.select('script[type="application/ld+json"]'):
                try:
                    parsed = json.loads(data.text)
                    if isinstance(parsed, dict) and parsed.get("@type") == "Product":
                        images.extend(f"https:{img}" for img in parsed.get("image", []))
                        break
                except json.JSONDecodeError:
                    continue

            desc_div = soup.select_one("div.Description-description")
            description = ""
            if desc_div:
                inner = desc_div.decode_contents().replace("<br/>", "\n").replace("<br />", "\n").replace("<br>", "\n")
                description = BeautifulSoup(inner, "html.parser").get_text().strip()

            return images, description
        except Exception as e:
            print(f"Warning: Unable to get details for {url}: {e}")
            return [], ""

    def _to_listing_model(self, mp_listing) -> Listing:
        """Converts a Marktplaats listing object to our internal Listing model."""
        url = str(mp_listing.link)
        images, full_description = self._get_listing_details(url)

        return Listing(
            title=str(mp_listing.title),
            description=full_description or mp_listing.description,
            price=float(mp_listing.price),
            price_type=str(mp_listing.price_type),
            link=url,
            city=mp_listing.location.city,
            distance_km=int(mp_listing.location.distance / 1000),
            date=mp_listing.date,
            images=images or [str(img) for img in mp_listing.get_images()],
        )

    def fetch_listings(self, zip_code: str, distance_km: int, category_name: str, limit: int) -> List[Listing]:
        """Fetches a list of listings and enriches them with details."""
        print(f"Fetching up to {limit} listings for category '{category_name}'...")
        search = SearchQuery(
            zip_code=zip_code,
            distance=distance_km * 1000,
            limit=limit,
            sort_by=SortBy.DATE,
            sort_order=SortOrder.DESC,
            category=category_from_name(category_name),
        )
        mp_listings = search.get_listings()
        print(f"Found {len(mp_listings)} raw listings. Converting to domain models...")
        return [self._to_listing_model(l) for l in mp_listings]