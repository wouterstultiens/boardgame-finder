import os
from typing import Dict, List, Any
from datetime import datetime, timezone, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..adapters.firestore_repository import ListingRepository
from ..config import settings


class WebGenerator:
    """Generates the static website from Firestore data."""

    def __init__(self, repo: ListingRepository):
        self.repo = repo
        template_dir = os.path.join(os.path.dirname(__file__), "templates")

        # Initialize Jinja environment
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )

        # Add helper: now() → current UTC datetime
        self.env.globals["now"] = lambda: datetime.now(timezone.utc)

        # Add strftime filter so template can use |strftime("%Y-%m-%d %H:%M:%S")
        self.env.filters["strftime"] = lambda value, fmt="%Y-%m-%d %H:%M:%S": (
            value.strftime(fmt) if hasattr(value, "strftime") else str(value)
        )

        print(f"WebGenerator initialized. Output directory: {settings.web_output_dir}")

    def generate_site(self):
        """Fetches data, renders HTML, and saves it to the output directory."""
        print("Starting website generation...")

        # 1. Fetch all listings from the repository
        all_listings = self.repo.get_all()

        # Define a cutoff date for listings older than a month
        one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)

        # 2. Aggregate and filter games
        games_map: Dict[int, Dict[str, Any]] = {}

        for listing in all_listings:
            # If the listing is older than a month, it should no longer be displayed.
            # Assume listing.date is timezone-naive and in UTC, make it aware for comparison.
            listing_date_aware = (
                listing.date.replace(tzinfo=timezone.utc) if listing.date.tzinfo is None else listing.date
            )
            if listing_date_aware < one_month_ago:
                continue

            for game in listing.games:
                if game.bgg_data:
                    bgg_id = game.bgg_data.id

                    # Apply filters from settings
                    if not (settings.bgg_min_rating <= game.bgg_data.rating <= 10.0):
                        continue
                    if not (
                        settings.bgg_min_weight
                        <= game.bgg_data.weight
                        <= settings.bgg_max_weight
                    ):
                        continue

                    if bgg_id not in games_map:
                        games_map[bgg_id] = {
                            "name": game.bgg_data.name,
                            "rating": game.bgg_data.rating,
                            "weight": game.bgg_data.weight,
                            "year": game.bgg_data.year_published,
                            "bgg_link": str(game.bgg_data.link),
                            "image": (
                                str(game.bgg_data.image_path)
                                if game.bgg_data.image_path
                                else ""
                            ),
                            "listings": [],
                        }

                    games_map[bgg_id]["listings"].append(
                        {
                            "price": listing.price,
                            "link": str(listing.link),
                            "city": listing.city,
                            "date": listing.date,  # Add listing date for filtering
                        }
                    )

        # Add newest listing date to each game for client-side filtering
        for game_id, game_data in games_map.items():
            if game_data["listings"]:
                newest_listing_date = max(l["date"] for l in game_data["listings"])
                games_map[game_id]["newest_listing_date"] = newest_listing_date

        # 3. Sort games by BGG rating (descending)
        sorted_games = sorted(
            games_map.values(), key=lambda g: g["rating"], reverse=True
        )
        print(f"Found {len(sorted_games)} unique, filtered games to display.")

        # 4. Render the template
        template = self.env.get_template("index.html.j2")
        html_content = template.render(games=sorted_games, zip_code=settings.zip_code)

        # 5. Write to output file
        os.makedirs(settings.web_output_dir, exist_ok=True)
        output_path = os.path.join(settings.web_output_dir, "index.html")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ Website successfully generated at: {output_path}")