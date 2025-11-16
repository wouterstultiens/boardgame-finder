# evaluation/evaluate_extractor.py

import sys
import os
import re

# Add src to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from evaluation.cases import TEST_CASES
from boardgamefinder.services.extractor import JsonNameExtractor
from boardgamefinder.adapters.llm_client import get_llm_client


def normalize_name(s: str) -> str:
    """Normalizes a game name for robust comparison."""
    s = s.lower()
    s = re.sub(r"[^\w\s]", "", s)  # remove punctuation/symbols
    s = re.sub(r"\s+", " ", s)     # collapse whitespace
    return s.strip()


def main():
    """Evaluates the JsonNameExtractor against predefined test cases."""
    print("Initializing components for extractor evaluation...")

    try:
        llm_client = get_llm_client()
        extractor = JsonNameExtractor(client=llm_client)
    except Exception as e:
        print(f"Error initializing components: {e}")
        print("Please ensure your .env file is correctly configured.")
        return

    results = {"Pass": 0, "Uncertain": 0, "Fail": 0}

    print("\n--- Evaluating JsonNameExtractor ---")

    for case in TEST_CASES:
        print(f"\n[TEST CASE]: {case.name}")

        try:
            actual_items = extractor.extract(case.title, case.description, case.image_texts)

            # Normalize names for comparison
            actual_map = {normalize_name(i["llm_name"]): i for i in actual_items}
            expected_map = {normalize_name(i["llm_name"]): i for i in case.expected_extraction}

            actual_names = set(actual_map.keys())
            expected_names = set(expected_map.keys())

            # Determine test status
            if actual_names != expected_names:
                result_label = "Fail"
                emoji = "❌"
            else:
                all_langs_match = all(
                    actual_map[n]["llm_lang"] == expected_map[n]["llm_lang"]
                    for n in expected_map
                )
                if all_langs_match:
                    result_label = "Pass"
                    emoji = "✅"
                else:
                    result_label = "Uncertain"
                    emoji = "⚠️"

            results[result_label] += 1

            # Print details
            print(f"  - Status:     {emoji} {result_label}")
            print(f"  - Expected:   {case.expected_extraction}")
            print(f"  - Actual:     {actual_items}")

            if result_label == "Fail":
                print(f"  - Normalized Expected Names: {sorted(expected_names)}")
                print(f"  - Normalized Actual Names:   {sorted(actual_names)}")

        except Exception as e:
            print(f"  - ERROR processing case: {e}")
            results["Fail"] += 1

    # Summary
    print("\n--- Summary ---")
    total = len(TEST_CASES)
    for label, count in results.items():
        pct = (count / total * 100) if total > 0 else 0
        print(f"{label}: {count}/{total} ({pct:.2f}%)")


if __name__ == "__main__":
    main()
