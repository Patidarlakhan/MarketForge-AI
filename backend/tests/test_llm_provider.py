"""
AI Marketing Content Engine — LLM Provider Unit Tests

Tests for extract_json_from_text, factory function, structured output parsing, and retry handling.
"""

from typing import Any, Dict, Optional
import pytest
from pydantic import BaseModel, Field

from app.llm import (
    AnthropicProvider,
    GeminiProvider,
    LLMProvider,
    LLMProviderError,
    LLMValidationError,
    OpenAIProvider,
    get_llm_provider,
)
from app.llm.base import extract_json_from_text


# Test Pydantic Schema
class DummySchema(BaseModel):
    title: str = Field(..., min_length=2)
    items: list[str] = Field(default_factory=list)
    score: int = Field(..., ge=0)


# Dummy Mock Provider for testing retry and validation logic without external API calls
class MockLLMProvider(LLMProvider):
    def __init__(self, responses: list[str], **kwargs):
        super().__init__(**kwargs)
        self.responses = responses
        self.call_count = 0

    async def generate_raw(
        self,
        system_prompt: str,
        user_prompt: str,
        schema_json: Optional[Dict[str, Any]] = None,
    ) -> str:
        if self.call_count >= len(self.responses):
            return self.responses[-1]
        response = self.responses[self.call_count]
        self.call_count += 1
        return response


# ── Tests for JSON Extractor ────────────────────────────────────
def test_extract_json_raw():
    text = '{"title": "Hello", "score": 10}'
    assert extract_json_from_text(text) == '{"title": "Hello", "score": 10}'


def test_extract_json_markdown():
    text = '```json\n{"title": "Markdown", "score": 99}\n```'
    assert extract_json_from_text(text) == '{"title": "Markdown", "score": 99}'


def test_extract_json_dirty_surroundings():
    text = 'Here is the response:\n{"title": "Dirty", "score": 50}\nHope this helps!'
    assert extract_json_from_text(text) == '{"title": "Dirty", "score": 50}'


# ── Tests for Factory ───────────────────────────────────────────
def test_factory_openai():
    provider = get_llm_provider("openai")
    assert isinstance(provider, OpenAIProvider)


def test_factory_anthropic():
    provider = get_llm_provider("anthropic")
    assert isinstance(provider, AnthropicProvider)


def test_factory_gemini():
    provider = get_llm_provider("gemini")
    assert isinstance(provider, GeminiProvider)


def test_factory_invalid():
    with pytest.raises(LLMProviderError):
        get_llm_provider("unsupported_provider")


# ── Tests for Structured Output & Retry Logic ──────────────────
@pytest.mark.asyncio
async def test_generate_structured_success():
    """Test successful structured output generation on first attempt."""
    valid_json = '{"title": "Test Strategy", "items": ["a", "b"], "score": 95}'
    mock = MockLLMProvider(responses=[valid_json])

    result = await mock.generate_structured(
        system_prompt="System",
        user_prompt="User",
        response_model=DummySchema,
    )
    assert isinstance(result, DummySchema)
    assert result.title == "Test Strategy"
    assert result.score == 95
    assert mock.call_count == 1


@pytest.mark.asyncio
async def test_generate_structured_repair_retry():
    """Test retry repair loop when first attempt fails validation."""
    invalid_json = '{"title": "X", "score": -5}'  # score < 0 violates ge=0
    valid_json = '{"title": "Fixed Strategy", "items": ["fixed"], "score": 10}'
    mock = MockLLMProvider(responses=[invalid_json, valid_json], max_retries=1)

    result = await mock.generate_structured(
        system_prompt="System",
        user_prompt="User",
        response_model=DummySchema,
    )
    assert isinstance(result, DummySchema)
    assert result.title == "Fixed Strategy"
    assert result.score == 10
    assert mock.call_count == 2


@pytest.mark.asyncio
async def test_generate_structured_exhaust_retries():
    """Test LLMValidationError is raised when all retries fail schema validation."""
    invalid_json = '{"title": "X"}'  # missing required 'score'
    mock = MockLLMProvider(responses=[invalid_json, invalid_json], max_retries=1)

    with pytest.raises(LLMValidationError):
        await mock.generate_structured(
            system_prompt="System",
            user_prompt="User",
            response_model=DummySchema,
        )
    assert mock.call_count == 2
