# tests/unit/test_matcher.py
import pytest
import pandas as pd
from boardgamefinder.adapters.bgg_repository import BGGRepository, COLS
from boardgamefinder.services.matcher import FuzzyNameMatcher
from tests.cases import TEST_CASES

class MockBGGRepository(BGGRepository):
    """A mock BGG repository that uses a predefined DataFrame."""
    def get_all_games(self) -> pd.DataFrame:
        # Create a sample DataFrame based on the expected matches in test cases
        data = []
        for case in TEST_CASES:
            for llm_name, match in case.expected_matches.items():
                if match.id:
                    data.append({
                        "BGGId": int(match.id),
                        "Name": match.name,
                        "YearPublished": 2000,
                        "GameWeight": 2.5,
                        "AvgRating": 7.5,
                        "ImagePath": "http://example.com/image.jpg"
                    })
        return pd.DataFrame(data, columns=COLS).drop_duplicates()

@pytest.fixture(scope="module")
def name_matcher():
    """Provides a FuzzyNameMatcher instance initialized with mock data."""
    repo = MockBGGRepository()
    return FuzzyNameMatcher(repository=repo)

@pytest.mark.parametrize("case", TEST_CASES)
def test_fuzzy_name_matcher(name_matcher, case):
    for llm_name, expected_match in case.expected_matches.items():
        result = name_matcher.match(llm_name)
        
        if expected_match.id is None:
            assert result is None
        else:
            assert result is not None
            assert result.id == int(expected_match.id)
            assert result.name == expected_match.name