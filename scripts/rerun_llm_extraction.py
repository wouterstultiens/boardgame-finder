# scripts/rerun_llm_extraction.py
import argparse
import json
from boardgamefinder.adapters.firestore_repository import get_listing_repository
from boardgamefinder.adapters.llm_client import get_llm_client
from boardgamefinder.services.extractor import JsonNameExtractor
from boardgamefinder.domain.models import Game

def main():
    """
    Reruns LLM extraction on all listings in Firestore and updates them if the
    extracted games have changed.
    """
    parser = argparse.ArgumentParser(description="Rerun LLM extraction on Firestore data.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the script without writing any changes to Firestore."
    )
    args = parser.parse_args()

    print("Initializing components...")
    repo = get_listing_repository()
    llm_client = get_llm_client()
    extractor = JsonNameExtractor(client=llm_client)

    print("Fetching all listings from Firestore...")
    all_listings = repo.get_all()
    print(f"Found {len(all_listings)} listings to process.")

    updated_count = 0
    for listing in all_listings:
        print(f"\nProcessing listing: {listing.title} ({listing.link})")

        # Rerun extraction
        newly_extracted_data = extractor.extract(
            title=listing.title,
            description=listing.description,
            image_texts=listing.image_texts
        )
        new_games = [Game(**data) for data in newly_extracted_data]
        
        # Compare old and new games
        # A simple but effective comparison is to dump them to sorted JSON strings
        old_games_json = json.dumps(sorted([g.model_dump() for g in listing.games], key=lambda x: x['llm_name']), sort_keys=True)
        new_games_json = json.dumps(sorted([g.model_dump() for g in new_games], key=lambda x: x['llm_name']), sort_keys=True)

        if old_games_json == new_games_json:
            print("  -> No change in extracted games. Skipping.")
            continue
        
        updated_count += 1
        print(f"  -> Change detected!")
        print(f"     Old games: {old_games_json}")
        print(f"     New games: {new_games_json}")

        if not args.dry_run:
            # Update the listing object and save
            listing.games = new_games
            # NOTE: After LLM extraction, name matching should be rerun.
            # For simplicity, this script only handles extraction. A second script
            # or a combined workflow could handle the full re-enrichment.
            print("     Clearing BGG data since LLM names have changed.")
            for game in listing.games:
                game.bgg_data = None # Clear old matches
            
            repo.save(listing)
            print("     -> Successfully updated in Firestore.")
        else:
            print("     -> [Dry Run] No changes were written.")

    print(f"\n--- Script Finished ---")
    print(f"Processed {len(all_listings)} listings.")
    print(f"Found and processed changes for {updated_count} listings.")
    if args.dry_run:
        print("This was a dry run. No data was modified.")

if __name__ == "__main__":
    main()