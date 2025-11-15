# evaluation/evaluate_matcher.py
import sys
import os

# Add src to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tests.cases import TEST_CASES
from boardgamefinder.services.matcher import FuzzyNameMatcher
from boardgamefinder.adapters.bgg_repository import get_bgg_repository

def main():
    """
    Evaluates the FuzzyNameMatcher against a predefined set of test cases.
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
        
        if not case.expected_matches:
            print("  - No matches to test for this case.")
            continue
            
        for llm_name, expected_match in case.expected_matches.items():
            total_matches_to_test += 1
            
            try:
                actual_match = matcher.match(llm_name)
                
                actual_id = str(actual_match.id) if actual_match else None
                expected_id = expected_match.id if expected_match else None
                
                status = "Fail"
                # Pass if both are None or if they are equal strings
                if actual_id == expected_id:
                    status = "Pass"
                
                results[status] += 1
                
                print(f"  - Input: '{llm_name}'")
                print(f"    - Status:          {status}")
                print(f"    - Expected BGG ID: {expected_id}")
                print(f"    - Actual BGG ID:   {actual_id}")
                if actual_match:
                    print(f"    - Actual BGG Name: '{actual_match.name}'")

            except Exception as e:
                print(f"  - ERROR processing match for '{llm_name}': {e}")
                results["Fail"] += 1


    print("\n--- Summary ---")
    total = total_matches_to_test
    print(f"Total Match Assertions: {total}")
    for status, count in results.items():
        percentage = (count / total * 100) if total > 0 else 0
        print(f"{status}: {count}/{total} ({percentage:.2f}%)")

if __name__ == "__main__":
    main()