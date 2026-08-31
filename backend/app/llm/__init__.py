"""
AI Marketing Content Engine — LLM Provider Factory

Provides get_llm_provider() factory function for selecting OpenAI, Anthropic, or Gemini.
"""

from typing import Optional

from app.config import settings
from app.llm.anthropic_provider import AnthropicProvider
from app.llm.base import LLMProvider, LLMProviderError, LLMValidationError
from app.llm.gemini_provider import GeminiProvider
from app.llm.openai_provider import OpenAIProvider


def get_llm_provider(provider_name: Optional[str] = None) -> LLMProvider:
    """
    Factory function returning an LLMProvider instance based on provider name or configuration.
    
    Supported providers:
    - 'openai': OpenAI API (GPT-4o, GPT-4o-mini) or OpenAI-compatible endpoint
    - 'anthropic': Anthropic Claude API (Claude 3.5 Sonnet, etc.)
    - 'gemini': Google Gemini API (Gemini 2.0 Flash, etc.)
    """
    target = (provider_name or settings.llm_provider).lower().strip()

    if target == "openai":
        return OpenAIProvider()
    elif target == "anthropic":
        return AnthropicProvider()
    elif target == "gemini":
        return GeminiProvider()
    else:
        raise LLMProviderError(
            f"Unsupported LLM provider: '{target}'. Supported providers: 'openai', 'anthropic', 'gemini'."
        )


__all__ = [
    "LLMProvider",
    "LLMProviderError",
    "LLMValidationError",
    "OpenAIProvider",
    "AnthropicProvider",
    "GeminiProvider",
    "get_llm_provider",
]
