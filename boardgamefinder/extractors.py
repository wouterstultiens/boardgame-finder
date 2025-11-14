# src/extractors.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json

from llm_client import LLM, Message
from prompts import GAME_EXTRACT_SYSTEM


class NameExtractor(ABC):
    @abstractmethod
    def extract(self, title: str, description: str) -> List[str]:
        ...


class JsonNameExtractor(NameExtractor):
    def __init__(self, client: LLM):
        self.client = client

    @staticmethod
    def _normalize_items(items: Any) -> List[Dict[str, str]]:
        """
        Normalizes LLM output into a list of {"name": str, "lang": str}.
        """
        out: List[Dict[str, str]] = []

        for x in items:
            name = str(x.get("name", "")).strip()
            lang = str(x.get("lang", "unknown")).strip().lower()

            out.append({"name": name, "lang": lang})

        return out

    @staticmethod
    def _parse_json(raw_message: str) -> List[Dict[str, str]]:
        try:
            data = json.loads(raw_message)
        except json.JSONDecodeError:
            # Return empty on invalid JSON to fail safely
            return []
        return JsonNameExtractor._normalize_items(data)

    def extract(self, title: str, description: str) -> List[Dict[str, str]]:
        messages = [
            Message("system", GAME_EXTRACT_SYSTEM),
            Message("user", f"Title:\n{title}\n\nDescription:\n{description}")
        ]
        raw = self.client.get_response(messages)
        return self._parse_json(raw)


# --- Factory ---
def make_name_extractor(method: str, client: LLM) -> NameExtractor:
    if method == "json":
        return JsonNameExtractor(client=client)
    else:
        raise ValueError("Wrong value for method NameExtractor")