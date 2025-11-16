# evaluation/evaluate_matcher.py
from evaluation.cases import TEST_CASES
from boardgamefinder.services.matcher import LLMNameMatcher, _normalize_name
from boardgamefinder.adapters.bgg_repository import get_bgg_repository
from boardgamefinder.adapters.llm_client import get_llm_client

def main():
    """
    Evaluates the LLMNameMatcher against a predefined set of test cases.
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

    results = {"Pass": 0, "Fail": 0, "Uncertain": 0}
    total_matches_to_test = 0

    print("\n--- Evaluating LLMNameMatcher ---")

    for case in TEST_CASES:
        print(f"\n[TEST CASE]: {case.name}")

        names_to_match = [item['llm_name'] for item in case.expected_extraction]
        expected_matches = case.expected_matches

        if len(names_to_match) != len(expected_matches):
            print(f"  - ❌ ERROR: Mismatch between extracted names ({len(names_to_match)}) and expected matches ({len(expected_matches)}). Skipping.")
            num_items = max(len(names_to_match), len(expected_matches))
            results["Fail"] += num_items
            total_matches_to_test += num_items
            continue

        if not names_to_match:
            expected_ids = expected_matches[0].get('id', []) if expected_matches else []
            if not expected_ids:
                 print("  - ✅ Pass: Correctly extracted no games to match, as expected.")
                 results["Pass"] += 1
            else:
                 print(f"  - ❌ Fail: No items to match, but expected IDs {expected_ids}.")
                 results["Fail"] += 1
            total_matches_to_test += 1
            continue

        for i, llm_name in enumerate(names_to_match):
            total_matches_to_test += 1
            expected_match_info = expected_matches[i]
            expected_ids = expected_match_info.get('id', [])

            try:
                actual_match = matcher.match(llm_name)
                actual_id = str(actual_match.id) if actual_match else ""

                status = "Fail" # Default to Fail

                if actual_id in expected_ids:
                    status = "Pass"
                # If it's not a direct pass, check for the "Uncertain" case
                elif ":" in llm_name and actual_match:
                    # It's an expansion, and we got a result, but it wasn't the right one.
                    # Is the result the base game?
                    base_llm_name_norm = _normalize_name(llm_name.split(':')[0])
                    actual_name_norm = _normalize_name(actual_match.name)
                    
                    # If actual match is the base game and contains no colon itself
                    if base_llm_name_norm == actual_name_norm and ":" not in actual_match.name:
                        status = "Uncertain"

                if status == "Pass":
                    emoji = "✅"
                elif status == "Uncertain":
                    emoji = "⚠️"
                else: # Fail
                    emoji = "❌"
                
                results[status] += 1

                print(f"  - Input: '{llm_name}'")
                print(f"    - Status:          {emoji} {status}")
                print(f"    - Expected BGG ID: {expected_ids or 'None'}")
                print(f"    - Actual BGG ID:   {actual_id or 'None'}")
                if actual_match:
                    print(f"    - Actual BGG Name: '{actual_match.name}'")
                if status != "Pass" and expected_ids:
                    expected_name = expected_match_info.get('name', 'N/A')
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