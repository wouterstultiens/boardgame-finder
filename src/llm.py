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
        You are an extractor that returns ONLY valid JSON arrays of board game titles.

        Your task:
        - Detect board game titles inside the provided text (title + description).
        - Prefer canonical BoardGameGeek names.
        - If none are found, return [].
        - IMPORTANT: Output must be *only* a JSON array. No explanation.

        Examples:

        Input:
        Title: "Kolonisten te koop!"
        Description: "Complete set van Catan met uitbreiding Zeerovers."
        Output:
        ["Catan", "Catan: Seafarers"]

        Input:
        Title: "Games bundle"
        Description: " Monopoly, Risk, and a puzzle included."
        Output:
        ["Monopoly", "Risk"]

        Input:
        Title: "Boeken te koop"
        Description: "Romans, thrillers, geen spellen."
        Output:
        []

        Now extract games from the following listing:

        Title:
        {title}

        Description:
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