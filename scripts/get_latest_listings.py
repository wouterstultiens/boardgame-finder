# scripts/get_latest_listings.py
from datetime import timezone
from boardgamefinder.adapters.firestore_repository import get_listing_repository
from boardgamefinder.domain.models import Listing # Import Listing for type hints

def make_aware(dt):
    """
    Standardize a datetime object to be timezone-aware (UTC) for safe comparison.
    This fixes the 'can't compare offset-naive and offset-aware datetimes' error.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def format_listing_details(listing: Listing):
    """Formats a listing and its game details into a list of output strings."""
    output = []
    
    aware_created_at = make_aware(listing.created_at)
    date_str = aware_created_at.strftime("%Y-%m-%d")
    time_str = aware_created_at.strftime("%H:%M:%S")

    # Truncate title to fit in the column
    title_str = (listing.title[:35] + '...') if len(listing.title) > 38 else listing.title

    # Base details string for the first line of the listing
    base_line = f"{date_str: <12}| {time_str: <9}| {title_str: <38}| {listing.link}"

    # Get the games with BGG matches
    matched_games = [
        game for game in listing.games if game.bgg_data is not None
    ]

    if not matched_games:
        # If no matched games, just print the listing details with empty game columns
        output.append(f"{base_line}| {'-':<30}| {'-':<10}")
    else:
        # If there are matched games, print them on separate lines
        for i, game in enumerate(matched_games):
            bgg_name_str = (game.bgg_data.name[:27] + '...') if len(game.bgg_data.name) > 30 else game.bgg_data.name
            bgg_id_str = str(game.bgg_data.id)

            # First line gets the main listing info
            if i == 0:
                line = f"{base_line}| {bgg_name_str: <30}| {bgg_id_str: <10}"
            # Subsequent lines only get game info and a link reminder
            else:
                empty_listing_cols = f"{' ': <12}| {' ': <9}| {'': <38}| {'...':<10}"
                line = f"{empty_listing_cols}| {bgg_name_str: <30}| {bgg_id_str: <10}"
            
            output.append(line)
    
    return output


def main():
    """
    Fetches all listings from Firestore, sorts them by creation time,
    and prints the latest listings in a simple format with BGG details.
    """
    print("Initializing Firestore repository...")
    try:
        repo = get_listing_repository()
    except Exception as e:
        print(f"Error initializing repository: {e}")
        print("Please ensure your GCP credentials are set up correctly.")
        return

    print("Fetching all listings...")
    all_listings = repo.get_all()
    print(f"Found {len(all_listings)} total listings.")

    if not all_listings:
        print("No listings found. Exiting.")
        return

    # Sort listings by the 'created_at' attribute in descending order (latest first)
    sorted_listings = sorted(
        all_listings,
        key=lambda l: make_aware(l.created_at), 
        reverse=True
    )

    print("\n--- Latest Listings ---")
    
    # Define a wide header for the new columns
    print(f"{'Date':<12} | {'Time':<9} | {'Listing Title':<38}| {'Marktplaats Link':<10}| {'BGG Game Name':<30}| {'BGG ID'}")
    print("-" * 150) # Extend separator line

    # Print details for each listing
    for listing in sorted_listings:
        for line in format_listing_details(listing):
            print(line)
        # Add a blank line between listings for readability
        print()

if __name__ == "__main__":
    main()