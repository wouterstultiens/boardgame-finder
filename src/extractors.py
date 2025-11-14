# src/extractors.py
from abc import ABC, abstractmethod
from typing import List
import json
from llm_client import LLM, Message


class NameExtractor(ABC):
    @abstractmethod
    def extract(self, title: str, description: str) -> List[str]:
        ...


class JsonNameExtractor(NameExtractor):
    def __init__(self, client: LLM):
        self.client = client

    @staticmethod
    def _parse_json(raw_message: str):
        try:
            return [str(x).strip() for x in json.loads(raw_message) if str(x).strip()]
        except json.JSONDecodeError:
            return [f"Error decoding JSON: {raw_message}"]

    def extract(self, title: str, description: str) -> List[str]:
        messages = [
            Message("system", "Return ONLY a JSON array of board game titles. If none, return []."),
            Message("user", f"Title: {title}\nDescription: {description}")
        ]
        raw = self.client.get_response(messages)
        names = self._parse_json(raw)
        return names


# --- Factory ---
def make_name_extractor(method: str, client: LLM) -> NameExtractor:
    if method == "json":
        return JsonNameExtractor(client=client)
    else:
        raise ValueError("Wrong value for method NameExtractor")