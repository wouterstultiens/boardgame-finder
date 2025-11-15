# src/boardgamefinder/adapters/llm_client.py
import os
from abc import ABC, abstractmethod
from typing import List, Dict

import together
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

from ..config import settings

class Message(Dict):
    def __init__(self, role: str, content: str):
        super().__init__(role=role, content=content)

class LLM(ABC):
    @abstractmethod
    def get_response(self, messages: List[Message], temperature: float = 0.0, **kwargs) -> str:
        """Sends a chat conversation and returns the assistant's text response."""
        ...

class TogetherLLM(LLM):
    def __init__(self, model: str, api_key: str):
        if not api_key:
            raise ValueError("Together API key is required.")
        if not model:
            raise ValueError("Together LLM model is required.")
        self.model = model
        self.client = together.Together(api_key=api_key)
        print(f"TogetherLLM client initialized for model: {model}")

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
        # These should be set in the environment, not hardcoded.
        os.environ["SSL_CERT_FILE"] = settings.ssl_cert_file
        os.environ["AZURE_CLIENT_ID"] = settings.azure_client_id
        os.environ["AZURE_TENANT_ID"] = settings.azure_tenant_id
        os.environ["AZURE_CLIENT_SECRET"] = settings.azure_client_secret
        
        cred = DefaultAzureCredential()
        # The token provider function should not have hardcoded values.
        # This is a placeholder for a real implementation.
        token_provider = lambda: cred.get_token("https://cognitiveservices.azure.com/.default").token
        
        self.client = AzureOpenAI(
            api_version="2024-02-01",
            azure_endpoint="YOUR_AZURE_ENDPOINT_HERE", # Replace with your actual endpoint
            azure_ad_token_provider=token_provider,
        )
        print("AzureOpenAILLM client initialized.")

    def get_response(self, messages: List[Message], temperature: float = 0.0, **kwargs) -> str:
        resp = self.client.chat.completions.create(
            model="gpt-4o", # Model should be configurable
            messages=messages,
            temperature=temperature,
            **kwargs,
        )
        return resp.choices[0].message.content or ""

def get_llm_client() -> LLM:
    """Factory function to create an LLM client based on app settings."""
    provider = settings.llm_provider
    if provider == "together":
        return TogetherLLM(model=settings.together_llm_model, api_key=settings.together_api_key)
    elif provider == "azure":
        return AzureOpenAILLM()
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")