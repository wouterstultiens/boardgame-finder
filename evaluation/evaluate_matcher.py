# evaluation/evaluate_matcher.py
import sys
import os

# Add src to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from evaluation.cases import TEST_CASES
from boardgamefinder.services.matcher import FuzzyNameMatcher
from boardgamefinder.adapters.bgg_repository import get_bgg_repository

def main():
    """
    Evaluates the FuzzyNameMatcher against a predefined set of test cases.
    It validates if the correct BGG ID is retrieved for an extracted game name.
    """
    print("Initializing components for matcher evaluation...")
    try:
        bgg_repo = get_bgg_repository()
        matcher = FuzzyNameMatcher(repository=bgg_repo)
    except Exception as e:
        print(f"Error initializing components: {e}")
        print("Please ensure your BGG data source is correctly configured.")
        return

    results = {"Pass": 0, "Fail": 0}
    total_matches_to_test = 0

    print("\n--- Evaluating FuzzyNameMatcher ---")

    for case in TEST_CASES:
        print(f"\n[TEST CASE]: {case.name}")

        names_to_match = [item['llm_name'] for item in case.expected_extraction]
        expected_matches = case.expected_matches

        if len(names_to_match) != len(expected_matches):
            print(f"  - ❌ ERROR: Mismatch between number of extracted names ({len(names_to_match)}) and expected matches ({len(expected_matches)}). Skipping.")
            num_items = max(len(names_to_match), len(expected_matches))
            results["Fail"] += num_items
            total_matches_to_test += num_items
            continue

        if not names_to_match:
            print("  - No items to match for this case.")
            continue

        # Iterate over the extracted names and their corresponding expected BGG match
        for i, llm_name in enumerate(names_to_match):
            total_matches_to_test += 1
            expected_match = expected_matches[i]

            try:
                actual_match = matcher.match(llm_name)

                actual_id = str(actual_match.id) if actual_match else ""
                expected_id = expected_match.get('id', '')

                if actual_id == expected_id:
                    status = "Pass"
                    emoji = "✅"
                else:
                    status = "Fail"
                    emoji = "❌"

                results[status] += 1

                print(f"  - Input: '{llm_name}'")
                print(f"    - Status:          {emoji} {status}")
                print(f"    - Expected BGG ID: {expected_id or 'None'}")
                print(f"    - Actual BGG ID:   {actual_id or 'None'}")
                if actual_match:
                    print(f"    - Actual BGG Name: '{actual_match.name}'")
                if status == "Fail" and expected_id:
                    expected_name = expected_match.get('name', 'N/A')
                    print(f"    - Expected BGG Name: '{expected_name}'")

            except Exception as e:
                print(f"  - ❌ ERROR processing match for '{llm_name}': {e}")
                results["Fail"] += 1


    print("\n--- Summary ---")
    total = total_matches_to_test
    print(f"Total Match Assertions: {total}")
    for status, count in results.items():
        percentage = (count / total * 100) if total > 0 else 0
        print(f"{status}: {count}/{total} ({percentage:.2f}%)")

if __name__ == "__main__":
    main()