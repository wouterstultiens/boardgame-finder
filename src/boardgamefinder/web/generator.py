# src/boardgamefinder/web/generator.py
import os
from typing import Dict, List, Any
from datetime import datetime, timezone, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape
import zoneinfo

from ..adapters.firestore_repository import ListingRepository
from ..config import settings

# Define the local timezone for accurate UTC conversion and display
LOCAL_TIMEZONE = zoneinfo.ZoneInfo("Europe/Amsterdam")

class WebGenerator:
    """Generates the static website from Firestore data."""

    def __init__(self, repo: ListingRepository):
        self.repo = repo
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self.env.globals["now"] = lambda: datetime.now(timezone.utc)
        print(f"WebGenerator initialized. Output directory: {settings.web_output_dir}")

    def _get_aware_utc_datetime(self, dt: datetime) -> datetime:
        """Converts a datetime object to an aware UTC datetime."""
        if dt.tzinfo is None:
            # Firestore stores naive datetimes as UTC. Assume UTC if naive.
            return dt.replace(tzinfo=timezone.utc)
        # If already aware, just convert to UTC for consistency
        return dt.astimezone(timezone.utc)

    def generate_site(self):
        """Fetches data, renders HTML, and saves it to the output directory."""
        print("Starting website generation...")
        all_listings = self.repo.get_all()
        one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)
        games_map: Dict[int, Dict[str, Any]] = {}

        for listing in all_listings:
            # USE created_at for all filtering and display logic
            listing_creation_date_utc = self._get_aware_utc_datetime(listing.created_at)
            
            if listing_creation_date_utc < one_month_ago:
                continue

            for game in listing.games:
                if game.bgg_data:
                    bgg_id = game.bgg_data.id
                    if not (settings.bgg_min_rating <= game.bgg_data.rating <= 10.0):
                        continue
                    if not (settings.bgg_min_weight <= game.bgg_data.weight <= settings.bgg_max_weight):
                        continue

                    if bgg_id not in games_map:
                        games_map[bgg_id] = {
                            "name": game.bgg_data.name,
                            "rating": game.bgg_data.rating,
                            "weight": game.bgg_data.weight,
                            "year": game.bgg_data.year_published,
                            "bgg_link": str(game.bgg_data.link),
                            "image": str(game.bgg_data.image_path) if game.bgg_data.image_path else "",
                            "listings": [],
                        }
                    
                    games_map[bgg_id]["listings"].append({
                        "link": str(listing.link),
                        "date": listing_creation_date_utc, # Use the created_at timestamp
                    })

        # Process games after aggregation: sort listings, find newest, and format dates
        for game_id, game_data in games_map.items():
            if game_data["listings"]:
                # Sort listings by date (newest first) for display
                game_data["listings"].sort(key=lambda l: l["date"], reverse=True)
                
                # The newest listing's date is used by the JS filter
                newest_listing_date = game_data["listings"][0]["date"]
                games_map[game_id]["newest_listing_date"] = newest_listing_date

                # Add a formatted string for display on each listing link
                for listing_item in game_data["listings"]:
                    listing_item["date_formatted"] = listing_item["date"].astimezone(LOCAL_TIMEZONE).strftime("%m-%d %H:%M")

        sorted_games = sorted(games_map.values(), key=lambda g: g["rating"], reverse=True)
        print(f"Found {len(sorted_games)} unique, filtered games to display.")

        template = self.env.get_template("index.html.j2")
        html_content = template.render(games=sorted_games, zip_code=settings.zip_code)

        os.makedirs(settings.web_output_dir, exist_ok=True)
        output_path = os.path.join(settings.web_output_dir, "index.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ Website successfully generated at: {output_path}")