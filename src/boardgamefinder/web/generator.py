# src/boardgamefinder/web/generator.py
import os
from typing import Dict, List, Any
from jinja2 import Environment, FileSystemLoader

from ..adapters.firestore_repository import ListingRepository
from ..config import settings

class WebGenerator:
    """Generates the static website from Firestore data."""

    def __init__(self, repo: ListingRepository):
        self.repo = repo
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
        print(f"WebGenerator initialized. Output directory: {settings.web_output_dir}")

    def generate_site(self):
        """Fetches data, renders HTML, and saves it to the output directory."""
        print("Starting website generation...")

        # 1. Fetch all listings from the repository
        all_listings = self.repo.get_all()

        # 2. Aggregate and filter games
        games_map: Dict[int, Dict[str, Any]] = {}

        for listing in all_listings:
            for game in listing.games:
                if game.bgg_data:
                    bgg_id = game.bgg_data.id
                    # Apply filters
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
                            "listings": []
                        }
                    
                    games_map[bgg_id]["listings"].append({
                        "price": listing.price,
                        "link": str(listing.link),
                        "city": listing.city
                    })
        
        # 3. Sort games by BGG rating (descending)
        sorted_games = sorted(games_map.values(), key=lambda g: g["rating"], reverse=True)
        print(f"Found {len(sorted_games)} unique, filtered games to display.")

        # 4. Render the template
        template = self.env.get_template("index.html.j2")
        html_content = template.render(games=sorted_games)

        # 5. Write to output file
        os.makedirs(settings.web_output_dir, exist_ok=True)
        output_path = os.path.join(settings.web_output_dir, "index.html")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"Website successfully generated at: {output_path}")