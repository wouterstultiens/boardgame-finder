# scripts/rerun_name_matching.py
import argparse
from boardgamefinder.adapters.firestore_repository import get_listing_repository
from boardgamefinder.adapters.bgg_repository import get_bgg_repository
from boardgamefinder.services.matcher import FuzzyNameMatcher

def main():
    """
    Reruns BGG name matching on all games within all listings in Firestore.
    """
    parser = argparse.ArgumentParser(description="Rerun BGG name matching on Firestore data.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the script without writing any changes to Firestore."
    )
    args = parser.parse_args()

    print("Initializing components...")
    repo = get_listing_repository()
    bgg_repo = get_bgg_repository()
    matcher = FuzzyNameMatcher(repository=bgg_repo)

    print("Fetching all listings from Firestore...")
    all_listings = repo.get_all()
    print(f"Found {len(all_listings)} listings to process.")

    updated_count = 0
    for listing in all_listings:
        print(f"\nProcessing listing: {listing.title} ({listing.link})")
        has_changed = False
        
        if not listing.games:
            print("  -> No games to process. Skipping.")
            continue

        for game in listing.games:
            old_bgg_id = game.bgg_data.id if game.bgg_data else None
            
            # Rerun matching
            new_bgg_data = matcher.match(game.llm_name)
            new_bgg_id = new_bgg_data.id if new_bgg_data else None

            if old_bgg_id != new_bgg_id:
                has_changed = True
                print(f"  -> Match changed for '{game.llm_name}': {old_bgg_id} -> {new_bgg_id}")
                game.bgg_data = new_bgg_data

        if has_changed:
            updated_count += 1
            if not args.dry_run:
                repo.save(listing)
                print("     -> Successfully updated in Firestore.")
            else:
                print("     -> [Dry Run] No changes were written.")
        else:
            print("  -> No changes in matches for this listing.")

    print(f"\n--- Script Finished ---")
    print(f"Processed {len(all_listings)} listings.")
    print(f"Found and processed changes for {updated_count} listings.")
    if args.dry_run:
        print("This was a dry run. No data was modified.")

if __name__ == "__main__":
    main()