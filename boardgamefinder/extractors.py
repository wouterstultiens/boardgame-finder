# src/extractors.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json

from .llm_client import LLM, Message
from .prompts import GAME_EXTRACT_SYSTEM


class NameExtractor(ABC):
    @abstractmethod
    def extract(self, title: str, description: str, image_texts: List[str]) -> List[str]:
        ...


class JsonNameExtractor(NameExtractor):
    def __init__(self, client: LLM):
        self.client = client

    @staticmethod
    def _normalize_items(items: Any) -> List[Dict[str, str]]:
        out: List[Dict[str, str]] = []
        for x in items:
            name = str(x.get("name", "")).strip()
            lang = str(x.get("lang", "unknown")).strip().lower()
            out.append({"name": name, "lang": lang})
        return out

    @staticmethod
    def _parse_json(raw_message: str) -> List[Dict[str, str]]:
        try:
            start = raw_message.index('[')
            end = raw_message.rindex(']') + 1
            return JsonNameExtractor._normalize_items(json.loads(raw_message[start:end]))
        except:
            return []

    def extract(self, title: str, description: str, image_texts: List[str]) -> List[Dict[str, str]]:
        image_text_block = "\n\n".join(
            [f"--- OCR Result for Image {i+1} ---\n{text}" for i, text in enumerate(image_texts)]
        )
        messages = [
            Message("system", GAME_EXTRACT_SYSTEM),
            Message("user", f"Title:\n{title}\n\nDescription:\n{description}\n\nImage texts (OCR Results):\n{image_text_block}")
        ]
        raw = self.client.get_response(messages)
        return self._parse_json(raw)


def make_name_extractor(method: str, client: LLM) -> NameExtractor:
    if method == "json":
        return JsonNameExtractor(client=client)
    else:
        raise ValueError("Wrong value for method NameExtractor")
