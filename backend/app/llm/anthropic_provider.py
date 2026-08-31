"""
AI Marketing Content Engine — Anthropic Claude LLM Provider

Implementation for Anthropic Claude API.
"""

import logging
from typing import Any, Dict, Optional

from anthropic import AsyncAnthropic

from app.config import settings
from app.llm.base import LLMProvider, LLMProviderError

logger = logging.getLogger(__name__)


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API provider implementation."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.api_key = api_key or settings.anthropic_api_key
        self.model = model or settings.anthropic_model

        if not self.api_key:
            logger.warning("Anthropic API key is not set in environment settings.")

        self.client = AsyncAnthropic(
            api_key=self.api_key or "dummy-key-for-init",
            timeout=self.timeout,
        )

    async def generate_raw(
        self,
        system_prompt: str,
        user_prompt: str,
        schema_json: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Call Anthropic Messages API."""
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self.temperature,
            )

            text_blocks = [
                block.text for block in response.content if hasattr(block, "text")
            ]
            content = "".join(text_blocks)

            if not content:
                raise LLMProviderError("Anthropic returned an empty content response.")
            return content

        except Exception as exc:
            logger.error(f"Anthropic completion error: {exc}")
            raise LLMProviderError(f"Anthropic API call failed: {exc}") from exc
