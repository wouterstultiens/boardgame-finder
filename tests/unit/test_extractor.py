# tests/unit/test_extractor.py
import pytest
import json
from boardgamefinder.services.extractor import JsonNameExtractor
from boardgamefinder.adapters.llm_client import LLM, Message
from tests.cases import TEST_CASES

class MockLLM(LLM):
    """A mock LLM client that returns a pre-defined response."""
    def __init__(self, response_map: dict):
        self.response_map = response_map

    def get_response(self, messages: list[Message], temperature: float = 0, **kwargs) -> str:
        # Use the title as a key to get the expected response
        user_message_content = messages[-1]['content']
        title = user_message_content.split('\n')[1] # Simple way to get title
        return self.response_map.get(title, "[]")

# Prepare a response map for the mock LLM from our test cases
mock_responses = {
    case.title: json.dumps([
        {"name": item["llm_name"], "lang": item["llm_lang"]} 
        for item in case.expected_extraction
    ])
    for case in TEST_CASES
}

mock_llm_client = MockLLM(response_map=mock_responses)

@pytest.mark.parametrize("case", TEST_CASES)
def test_json_name_extractor(case):
    extractor = JsonNameExtractor(client=mock_llm_client)

    actual_items = extractor.extract(
        title=case.title,
        description=case.description,
        image_texts=case.image_texts
    )
    
    # Compare sorted lists of dicts to ignore order
    actual_sorted = sorted(actual_items, key=lambda x: x['llm_name'])
    expected_sorted = sorted(case.expected_extraction, key=lambda x: x['llm_name'])

    assert actual_sorted == expected_sorted