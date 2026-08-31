"""
AI Marketing Content Engine — Google Gemini LLM Provider

Implementation for Google Gemini API.
"""

import logging
from typing import Any, Dict, Optional

import google.generativeai as genai

from app.config import settings
from app.llm.base import LLMProvider, LLMProviderError

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    """Google Gemini API provider implementation."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.api_key = api_key or settings.gemini_api_key
        self.model_name = model or settings.gemini_model

        if not self.api_key:
            logger.warning("Gemini API key is not set in environment settings.")
        else:
            genai.configure(api_key=self.api_key)

    async def generate_raw(
        self,
        system_prompt: str,
        user_prompt: str,
        schema_json: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Call Google Gemini GenerativeModel API."""
        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt,
                generation_config={
                    "temperature": self.temperature,
                    "response_mime_type": "application/json",
                },
            )

            # Generate content asynchronously
            response = await model.generate_content_async(user_prompt)

            content = response.text
            if not content:
                raise LLMProviderError("Gemini returned an empty content response.")
            return content

        except Exception as exc:
            logger.error(f"Gemini completion error: {exc}")
            raise LLMProviderError(f"Gemini API call failed: {exc}") from exc
