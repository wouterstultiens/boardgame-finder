from abc import ABC, abstractmethod
from typing import List
import json
from pydantic import BaseModel
from config import settings
import together


class BaseLLM(ABC):
    @abstractmethod
    def extract_names(self, title: str, description: str) -> List[str]: ...


class TogetherLLM(BaseLLM):
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = together.Together(api_key=api_key)

    def extract_names(self, title: str, description: str) -> List[str]:
        prompt = f"""
        Return ONLY JSON: an array of distinct board game titles detected in the text.
        Prefer canonical names as listed on BoardGameGeek.
        If no board games are present, return [].

        Text title:
        {title}

        Text description:
        {description}
        """
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        text = resp.choices[0].message.content.strip()
        data = json.loads(text)
        return [str(x).strip() for x in data if str(x).strip()]