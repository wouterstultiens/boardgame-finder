# scripts/generate_test_cases.py
import textwrap
from datetime import timezone

from evaluation.cases import TEST_CASES
from boardgamefinder.adapters.firestore_repository import get_listing_repository, ListingRepository
from boardgamefinder.domain.models import Listing

def format_string_for_python_code(s: str) -> str:
    """
    Formats a string to be safely included in Python code as a single-line,
    double-quoted string literal, escaping necessary characters.
    """
    # Escape backslashes first, so we don't escape the backslashes we add for other characters.
    s = s.replace('\\', '\\\\')
    # Escape double quotes.
    s = s.replace('"', '\\"')
    # Replace newline characters with the escape sequence \n.
    s = s.replace('\n', '\\n')
    # Replace carriage return characters with the escape sequence \r.
    s = s.replace('\r', '\\r')
    # Wrap the entire string in double quotes.
    return f'"{s}"'

def generate_test_case_code(listing: Listing, repo: ListingRepository) -> str:
    """Generates the Python code for a single PromptTestCase from a listing."""
    doc_id = repo._doc_id_from_link(str(listing.link))
    # The name is still required by the dataclass, so we generate a unique one.
    name = f"autogen_{doc_id}"

    title = format_string_for_python_code(listing.title)
    description = format_string_for_python_code(listing.description)
    
    image_texts_list = [f"        {format_string_for_python_code(t)}" for t in listing.image_texts]
    image_texts_str = "[\n" + ",\n".join(image_texts_list) + ",\n    ]" if image_texts_list else "[]"

    expected_extraction = [
        {"llm_name": game.llm_name, "llm_lang": game.llm_lang}
        for game in listing.games
    ]

    expected_matches = []
    for game in listing.games:
        if game.bgg_data:
            match = {
                "id": [str(game.bgg_data.id)],
                "name": game.bgg_data.name,
                "lang": game.llm_lang,
                "exact_match": True,  # Placeholder, to be reviewed manually
            }
        else:
            match = {
                "id": [""],
                "name": "",
                "lang": "",
                "exact_match": False, # Placeholder, to be reviewed manually
            }
        expected_matches.append(match)

    # Use an f-string with triple quotes for the main template for readability
    code = f'''
    PromptTestCase(
        name="{name}",
        title={title},
        description={description},
        image_texts={image_texts_str},
        expected_extraction={expected_extraction},
        expected_matches={expected_matches},
    ),
    # Marktplaats URL: {listing.link}
    # Image URLs: {listing.images}'''
    return textwrap.dedent(code).strip()

def main():
    """
    Fetches listings from Firestore and generates new PromptTestCase code
    for those not already having a matching title and description in cases.py,
    writing the output to NEW_TEST_CASES.log.
    """
    LOG_FILENAME = "NEW_TEST_CASES.log"

    # Inform the user on the console where the output is going
    print(f"Starting test case generation. Output will be written to {LOG_FILENAME}")

    try:
        # 1. Open the file in write mode ('w') and use a 'with' statement for safe handling
        with open(LOG_FILENAME, 'w', encoding='utf-8') as log_file:

            # Helper function to print to the log file by default
            def log_print(*args, **kwargs):
                print(*args, file=log_file, **kwargs)

            log_print("Initializing Firestore repository...")
            try:
                repo = get_listing_repository()
            except Exception as e:
                log_print(f"Error initializing repository: {e}")
                log_print("Please ensure your GCP credentials are set up correctly.")
                return

            # Create a set of (title, description) tuples from existing cases for a fast, exact match lookup
            existing_cases = {(case.title, case.description) for case in TEST_CASES}
            log_print(f"Found {len(existing_cases)} existing test cases to check against.")

            log_print("Fetching all listings from Firestore...")
            all_listings = repo.get_all()
            log_print(f"Found {len(all_listings)} total listings.")

            if not all_listings:
                log_print("No listings found. Exiting.")
                return

            # Standardize all datetimes to be timezone-aware (UTC) to prevent comparison errors.
            def make_aware(dt):
                if dt.tzinfo is None:
                    return dt.replace(tzinfo=timezone.utc)
                return dt.astimezone(timezone.utc)

            sorted_listings = sorted(all_listings, key=lambda l: make_aware(l.created_at))

            log_print("\n" + "="*80)
            log_print("Generated New Test Cases (copy and paste into the TEST_CASES list in evaluation/cases.py)")
            log_print("="*80 + "\n")

            new_cases_code = []
            skipped_count = 0
            for listing in sorted_listings:
                # Check if a case with the exact same title and description already exists
                if (listing.title, listing.description) in existing_cases:
                    skipped_count += 1
                    continue

                # Only generate cases for listings that have successfully extracted games
                if listing.games:
                    case_code = generate_test_case_code(listing, repo)
                    new_cases_code.append(case_code)
            
            log_print(f"Skipped {skipped_count} listings with a matching title and description in cases.py.")
            log_print(f"Generating {len(new_cases_code)} new test cases.\n")

            if new_cases_code:
                # Print all new cases together, separated by a blank line for readability
                final_output = "\n\n".join(new_cases_code)
                log_print(final_output) # Use log_print to write to the file
            else:
                log_print("No new test cases to generate.")

            log_print("\n" + "="*80)
            log_print("Generation complete.")
            log_print("="*80)
        
        # 2. Inform the user on the console that the process finished
        print(f"Successfully wrote all output to {LOG_FILENAME}")

    except Exception as e:
        print(f"An error occurred during file operation: {e}")

if __name__ == "__main__":
    main()