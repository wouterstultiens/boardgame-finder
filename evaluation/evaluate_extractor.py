# evaluation/evaluate_extractor.py
import sys
import os
import re
import unicodedata

# Add src to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tests.cases import TEST_CASES
from boardgamefinder.services.extractor import JsonNameExtractor
from boardgamefinder.adapters.llm_client import get_llm_client

def normalize_name(s: str) -> str:
    """Normalizes a game name for robust comparison."""
    s = s.lower()
    # Remove punctuation and symbols
    s = re.sub(r"[^\w\s]", "", s)
    # Collapse multiple whitespace characters
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def main():
    """
    Evaluates the JsonNameExtractor against a predefined set of test cases.
    """
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
            
            # Create maps of {normalized_name: original_dict} for comparison
            actual_map = {normalize_name(item['llm_name']): item for item in actual_items}
            expected_map = {normalize_name(item['llm_name']): item for item in case.expected_extraction}

            actual_names = set(actual_map.keys())
            expected_names = set(expected_map.keys())

            status = ""
            if actual_names != expected_names:
                status = "Fail"
            else:
                # Names match, now check if languages correspond correctly
                all_langs_match = True
                for norm_name, expected_item in expected_map.items():
                    actual_item = actual_map[norm_name]
                    if actual_item['llm_lang'] != expected_item['llm_lang']:
                        all_langs_match = False
                        break
                
                status = "Pass" if all_langs_match else "Uncertain"

            results[status] += 1
            
            print(f"  - Status:     {status}")
            print(f"  - Expected:   {case.expected_extraction}")
            print(f"  - Actual:     {actual_items}")
            if status == "Fail":
                print(f"  - Normalized Expected Names: {sorted(list(expected_names))}")
                print(f"  - Normalized Actual Names:   {sorted(list(actual_names))}")


        except Exception as e:
            print(f"  - ERROR processing case: {e}")
            results["Fail"] += 1


    print("\n--- Summary ---")
    total = len(TEST_CASES)
    print(f"Total Cases: {total}")
    for status, count in results.items():
        percentage = (count / total * 100) if total > 0 else 0
        print(f"{status}: {count}/{total} ({percentage:.2f}%)")

if __name__ == "__main__":
    main()