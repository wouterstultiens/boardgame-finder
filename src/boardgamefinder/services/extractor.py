# src/boardgamefinder/services/extractor.py
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any

from ..adapters.llm_client import LLM, Message
from ..prompts import GAME_EXTRACT_SYSTEM

class NameExtractor(ABC):
    """Abstract interface for extracting game names from listing text."""
    @abstractmethod
    def extract(self, title: str, description: str, image_texts: List[str]) -> List[Dict[str, str]]:
        ...

class JsonNameExtractor(NameExtractor):
    """Extracts game names using an LLM that returns a JSON array."""
    def __init__(self, client: LLM):
        self.client = client
        print("JsonNameExtractor initialized.")

    def _normalize_items(self, items: Any) -> List[Dict[str, str]]:
        if not isinstance(items, list):
            return []
        
        out: List[Dict[str, str]] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            llm_name = str(item.get("llm_name", "")).strip()
            llm_lang = str(item.get("llm_lang", "unknown")).strip().lower()
            if llm_lang not in ["nl", "en", "unknown"]:
                llm_lang = "unknown"
            if llm_name: # Only include items with a name
                out.append({"llm_name": llm_name, "llm_lang": llm_lang})
        return out

    def _parse_json(self, raw_message: str) -> List[Dict[str, str]]:
        """Safely parses a JSON array from a raw LLM response string."""
        try:
            # Find the start and end of the JSON array
            start = raw_message.find('[')
            end = raw_message.rfind(']') + 1
            if start == -1 or end == 0:
                return []
            
            json_str = raw_message[start:end]
            return self._normalize_items(json.loads(json_str))
        except (json.JSONDecodeError, IndexError):
            print(f"Warning: Failed to parse JSON from LLM response: {raw_message}")
            return []

    def extract(self, title: str, description: str, image_texts: List[str]) -> List[Dict[str, str]]:
        print("Extracting game names with LLM...")
        image_text_block = "\n\n".join(
            [f"--- OCR Result for Image {i+1} ---\n{text}" for i, text in enumerate(image_texts) if text]
        )
        
        user_content = f"Title:\n{title}\n\nDescription:\n{description}"
        if image_text_block:
            user_content += f"\n\nImage texts (OCR Results):\n{image_text_block}"

        messages = [
            Message("system", GAME_EXTRACT_SYSTEM),
            Message("user", user_content)
        ]
        
        raw_response = self.client.get_response(messages)
        extracted = self._parse_json(raw_response)
        print(f"LLM extraction found {len(extracted)} potential games.")
        return extracted