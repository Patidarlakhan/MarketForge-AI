"""
AI Marketing Content Engine — OpenAI LLM Provider

Implementation for OpenAI and OpenAI-compatible endpoints (Azure, vLLM, Ollama, etc.).
"""

import logging
from typing import Any, Dict, Optional

from openai import AsyncOpenAI

from app.config import settings
from app.llm.base import LLMProvider, LLMProviderError

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """OpenAI API provider implementation."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.api_key = api_key or settings.openai_api_key
        self.base_url = base_url or settings.openai_base_url
        self.model = model or settings.openai_model

        if not self.api_key:
            logger.warning("OpenAI API key is not set in environment settings.")

        self.client = AsyncOpenAI(
            api_key=self.api_key or "dummy-key-for-init",
            base_url=self.base_url,
            timeout=self.timeout,
        )

    async def generate_raw(
        self,
        system_prompt: str,
        user_prompt: str,
        schema_json: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Call OpenAI Chat Completions API with JSON mode enabled."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if not content:
                raise LLMProviderError("OpenAI returned an empty content response.")
            return content

        except Exception as exc:
            logger.error(f"OpenAI completion error: {exc}")
            raise LLMProviderError(f"OpenAI API call failed: {exc}") from exc
