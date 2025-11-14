# src/llm_client.py
from abc import ABC, abstractmethod
from typing import List

import together
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI


class Message(dict):
    def __init__(self, role: str, content: str):
        super().__init__(role=role, content=content)


class LLM(ABC):
    @abstractmethod
    def get_response(self, messages: List[Message], temperature: float = 0.0, **kwargs) -> str:
        """
        Sends a chat conversation and returns assistant text content.
        """
        ...


class TogetherLLM(LLM):
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = together.Together(api_key=api_key)

    def get_response(self, messages: List[Message], temperature: float = 0.0, **kwargs) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            **kwargs,
        )
        return resp.choices[0].message.content or ""


class AzureOpenAILLM(LLM):
    def __init__(self):
        cred = DefaultAzureCredential()
        token_provider = lambda: cred.get_token("https://9da779ce-c73e-408f-9978-962c4ddd596f.abnamro.onmicrosoft.com/.default").token
        self.client = AzureOpenAI(
            api_version="2024-10-21",
            azure_endpoint="https://aziag-dev.nl.eu.abnamro.com/maap-cognitive-services/openai-services/v1",
            azure_ad_token_provider=token_provider,
        )

    def get_response(self, messages: List[Message], temperature: float = 0.0, **kwargs) -> str:
        resp = self.client.chat.completions.create(
            messages=messages,
            temperature=temperature,
            **kwargs,
        )
        return resp.choices[0].message.content or ""