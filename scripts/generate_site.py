# scripts/generate_site.py
from boardgamefinder.adapters.firestore_repository import get_listing_repository
from boardgamefinder.web.generator import WebGenerator


def main():
    repo = get_listing_repository()
    generator = WebGenerator(repo)
    generator.generate_site()


if __name__ == "__main__":
    main()
