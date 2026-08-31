"""
AI Marketing Content Engine — LLM Provider Abstraction Base

Defines the abstract LLM provider interface, schema validation, retry loop, and exceptions.
"""

import json
import logging
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, TypeVar

from pydantic import BaseModel, ValidationError

from app.config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class LLMProviderError(Exception):
    """Raised when an unrecoverable error occurs during LLM provider execution."""
    pass


class LLMValidationError(LLMProviderError):
    """Raised when LLM output violates Pydantic schema after retries."""
    pass


def extract_json_from_text(text: str) -> str:
    """
    Extract JSON string from raw LLM output text, handling markdown blocks like ```json ... ```.
    """
    text = text.strip()

    # Match ```json ... ``` or ``` ... ``` code blocks
    markdown_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    match = re.search(markdown_pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Otherwise return raw text if it looks like JSON
    if text.startswith("{") and text.endswith("}"):
        return text

    # Search for first '{' and last '}'
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        return text[start_idx : end_idx + 1]

    return text


class LLMProvider(ABC):
    """Abstract Base Class for all LLM Provider implementations."""

    def __init__(
        self,
        max_retries: int = settings.llm_max_retries,
        timeout: int = settings.llm_timeout,
        temperature: float = settings.llm_temperature,
    ):
        self.max_retries = max_retries
        self.timeout = timeout
        self.temperature = temperature

    @abstractmethod
    async def generate_raw(
        self,
        system_prompt: str,
        user_prompt: str,
        schema_json: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Subclasses must implement raw text completion call to the provider API.
        Should return the raw string content from the LLM.
        """
        pass

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: Type[T],
    ) -> T:
        """
        Generate structured output adhering to response_model Pydantic schema.
        Handles JSON extraction, schema validation, and repair retries on validation failure.
        """
        schema_json = response_model.model_json_schema()
        
        # Remove root-level metadata to prevent the LLM from confusing schema keys with content keys
        schema_json.pop("title", None)
        schema_json.pop("description", None)

        # Enhance system prompt with explicit JSON schema instructions
        enhanced_system_prompt = (
            f"{system_prompt}\n\n"
            "CRITICAL OUTPUT INSTRUCTIONS:\n"
            "Return the ACTUAL CONTENT, not the JSON schema.\n"
            "Do NOT return keys such as 'properties', 'required', 'type', or 'description'.\n"
            "Your response must be a JSON OBJECT containing the actual requested values.\n"
            "Do NOT return a schema definition.\n\n"
            "The JSON object must conform to this schema:\n"
            f"{json.dumps(schema_json, indent=2)}\n\n"
            "Do NOT include markdown code fences, commentary, explanations, or text outside the JSON object."
        )

        current_user_prompt = user_prompt
        last_error: Optional[Exception] = None

        for attempt in range(1 + self.max_retries):
            try:
                logger.info(f"LLM generation attempt {attempt + 1}/{1 + self.max_retries}")
                raw_response = await self.generate_raw(
                    system_prompt=enhanced_system_prompt,
                    user_prompt=current_user_prompt,
                    schema_json=schema_json,
                )

                json_str = extract_json_from_text(raw_response)
                
                # Parse and validate with Pydantic
                validated_object = response_model.model_validate_json(json_str)
                logger.info(f"LLM response successfully validated against {response_model.__name__}")
                return validated_object

            except (json.JSONDecodeError, ValidationError) as err:
                last_error = err
                logger.warning(
                    f"LLM output validation failed on attempt {attempt + 1}: {err}"
                )

                if attempt < self.max_retries:
                    # Provide repair feedback to the LLM on retry
                    current_user_prompt = (
                        f"{user_prompt}\n\n"
                        f"[PREVIOUS ATTEMPT FAILED SCHEMA VALIDATION]\n"
                        f"Your previous response produced the following error:\n{err}\n\n"
                        f"Please fix the error and output valid JSON matching the exact schema."
                    )
                else:
                    break
            except Exception as exc:
                logger.error(f"LLM Provider API error: {exc}")
                raise LLMProviderError(f"LLM Provider execution failed: {exc}") from exc

        raise LLMValidationError(
            f"Failed to generate valid output matching {response_model.__name__} after {1 + self.max_retries} attempts. Last error: {last_error}"
        )
