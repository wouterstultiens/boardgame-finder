# tests/test_extractor.py
import re
import pytest

from boardgamefinder.config import settings
from boardgamefinder.llm_client import make_llm
from boardgamefinder.extractors import JsonNameExtractor

from tests.cases import TEST_CASES

# --- Test Utilities (kept tiny / KISS) ---

def _wordset(name: str) -> frozenset[str]:
    """
    Represent a name as a set of lowercase alphanumeric 'words',
    stripping spaces and special characters.
    Example: "Ticket to Ride: Europe" -> {"ticket", "to", "ride", "europe"}
    """
    return frozenset(w.lower() for w in re.findall(r"[A-Za-z0-9]+", name))


def _to_signature(item: dict) -> tuple[frozenset[str], str]:
    """
    Convert an extracted/expected item into a signature:
    (wordset(name), lang)
    """
    return (_wordset(item.get("name", "")), item.get("lang", ""))

# --- Parametrized Tests ---

@pytest.mark.parametrize("case", TEST_CASES, ids=[c.name for c in TEST_CASES])
def test_json_name_extractor_contract(case):
    llm_client = make_llm(
        provider=settings.llm_provider,
        model=settings.together_llm_model,
        api_key=settings.together_api_key,
    )
    extractor = JsonNameExtractor(client=llm_client)

    # Act
    actual_items = extractor.extract(title=case.title, description=case.description)

    # Assert: Same number of results
    assert len(actual_items) == len(case.expected), (
        f"{case.name}: expected {len(case.expected)} items, got {len(actual_items)}"
    )

    # Build multisets of signatures to compare irrespective of order
    expected_signatures = [_to_signature(it) for it in case.expected]
    actual_signatures = [_to_signature(it) for it in actual_items]

    # Compare as multisets (order-agnostic, count-aware)
    # We'll remove matches one-by-one to give better diffs on failure.
    remaining_actual = actual_signatures.copy()
    for es in expected_signatures:
        assert es in remaining_actual, (
            f"{case.name}: missing item {es} in actual {remaining_actual}"
        )
        remaining_actual.remove(es)

    # If anything is left, those are unexpected extras
    assert not remaining_actual, (
        f"{case.name}: unexpected extra items {remaining_actual}"
    )