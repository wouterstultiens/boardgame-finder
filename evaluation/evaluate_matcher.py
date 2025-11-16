# evaluation/evaluate_matcher.py
from evaluation.cases import TEST_CASES
from boardgamefinder.services.matcher import LLMNameMatcher
from boardgamefinder.adapters.bgg_repository import get_bgg_repository
from boardgamefinder.adapters.llm_client import get_llm_client

def main():
    """
    Evaluates the LLMNameMatcher against a predefined set of test cases.
    It validates if the correct BGG ID is retrieved for an extracted game name.
    """
    print("Initializing components for matcher evaluation...")
    try:
        bgg_repo = get_bgg_repository()
        llm_client = get_llm_client()
        matcher = LLMNameMatcher(repository=bgg_repo, llm_client=llm_client)
    except Exception as e:
        print(f"Error initializing components: {e}")
        print("Please ensure your BGG data source and LLM client are correctly configured.")
        return

    results = {"Pass": 0, "Fail": 0}
    total_matches_to_test = 0

    print("\n--- Evaluating LLMNameMatcher ---")

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
            expected_id = expected_matches[0].get('id', '') if expected_matches else ''
            if not expected_id:
                 print("  - ✅ Pass: Correctly extracted no games to match, as expected.")
                 results["Pass"] += 1
            else:
                 print(f"  - ❌ Fail: No items to match, but expected ID {expected_id}.")
                 results["Fail"] += 1
            total_matches_to_test += 1
            continue

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