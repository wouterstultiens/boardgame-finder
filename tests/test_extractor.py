import json
import re
from typing import Dict, List

from ragas.metrics.collections import ExactMatch

from boardgamefinder.config import settings
from boardgamefinder.llm_client import make_llm
from boardgamefinder.extractors import JsonNameExtractor
from tests.cases import TEST_CASES


_exact_match = ExactMatch()


def _wordset(name: str) -> List[str]:
    """
    Same normalization idea as your pytest test:
    - keep only alphanumeric 'words'
    - lowercase
    - ignore punctuation and order
    """
    return sorted(w.lower() for w in re.findall(r"[A-Za-z0-9]+", name))


def _canonical_items(items: List[Dict[str, str]]) -> str:
    """
    Turn a list of {"name", "lang"} dicts into a canonical string so that
    'equivalent' outputs become exactly equal strings.

    This mirrors the logic of your current pytest test:
    - represent each item as (wordset(name), lang)
    - treat the list as a multiset (order-independent)
    """
    sigs = []
    for it in items:
        words = _wordset(it.get("name", ""))
        lang = (it.get("lang") or "").lower()
        sigs.append({"words": words, "lang": lang})

    # sort for deterministic representation
    sigs.sort(key=lambda s: (s["lang"], s["words"]))

    # ExactMatch works on strings, so JSON-encode
    return json.dumps(sigs, ensure_ascii=False, sort_keys=True)


def run() -> List[Dict[str, object]]:
    """
    Run the extractor on all TEST_CASES and evaluate with ragas ExactMatch.

    Returns a list of result dicts so you *could* re-use this from pytest
    later if you want, but it's fully usable as a standalone script.
    """
    llm_client = make_llm(
        provider=settings.llm_provider,
        model=settings.together_llm_model,
        api_key=settings.together_api_key,
    )
    extractor = JsonNameExtractor(client=llm_client)

    results: List[Dict[str, object]] = []

    for case in TEST_CASES:
        actual_items = extractor.extract(
            title=case.title,
            description=case.description,
            image_texts=case.image_texts
        )

        reference = _canonical_items(case.expected)
        response = _canonical_items(actual_items)

        score_obj = _exact_match.score(reference=reference, response=response)
        score = float(score_obj.value)  # 1.0 for exact match, 0.0 otherwise

        passed = score == 1.0

        results.append(
            {
                "case": case.name,
                "title": case.title,
                "description": case.description,  
                "image_texts": case.image_texts,
                "passed": passed,
                "score": score,
                "expected": case.expected,
                "actual": actual_items,
            }
        )

    # Pretty CLI summary
    total = len(results)
    passed_count = sum(1 for r in results if r["passed"])

    print(
        f"\nExtractor evaluation with ragas ExactMatch: "
        f"{passed_count}/{total} cases passed\n"
    )

    for r in results:
        status = "✅ PASS" if r["passed"] else "❌ FAIL"
        print(f"{status} {r['case']} (score={r['score']:.3f})")
        print(f"  title    : {r['title']}")         # 👈 added
        print(f"  desc     : {r['description']}")   # 👈 added
        print(f"image_texts: {r['image_texts']}")
        print("  expected :", json.dumps(r["expected"], ensure_ascii=False))
        print("  actual   :", json.dumps(r["actual"], ensure_ascii=False))
        print()

    return results


if __name__ == "__main__":
    run()
