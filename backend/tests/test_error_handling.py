"""
AI Marketing Content Engine — Error Handling & Edge Cases Integration Tests

Tests for HTTP 404s, HTTP 400s (missing prerequisites), invalid parameters,
and custom LLM exception handlers.
"""

import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.llm import LLMProviderError
from app.models.campaign import Campaign, CampaignStatus
from app.services import strategy_service
from tests.test_campaign_api import SAMPLE_CAMPAIGN


@pytest.mark.asyncio
async def test_get_nonexistent_campaign_404(client: AsyncClient):
    """GET /api/v1/campaigns/{fake_id} should return 404 Not Found."""
    fake_id = str(uuid.uuid4())
    res = await client.get(f"/api/v1/campaigns/{fake_id}")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_generate_strategy_nonexistent_campaign_404(client: AsyncClient):
    """POST /api/v1/campaigns/{fake_id}/strategy/generate should return 404 Not Found."""
    fake_id = str(uuid.uuid4())
    res = await client.post(f"/api/v1/campaigns/{fake_id}/strategy/generate")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_generate_master_content_without_strategy_400(client: AsyncClient):
    """POST /api/v1/campaigns/{id}/master-content/generate should return 400 if strategy is missing."""
    c_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = c_res.json()["id"]

    res = await client.post(f"/api/v1/campaigns/{campaign_id}/master-content/generate")
    assert res.status_code == 400
    assert "strategy must be generated before" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_generate_platform_content_without_master_content_400(client: AsyncClient):
    """POST /api/v1/campaigns/{id}/platform-content/generate should return 400 if master content is missing."""
    c_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = c_res.json()["id"]

    res = await client.post(f"/api/v1/campaigns/{campaign_id}/platform-content/generate")
    assert res.status_code == 400
    assert "master content must be generated before" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_regenerate_invalid_platform_400(client: AsyncClient, db_session: AsyncSession):
    """POST /api/v1/campaigns/{id}/platform-content/tiktok/regenerate should return 400 Bad Request."""
    c_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = c_res.json()["id"]

    res = await client.post(f"/api/v1/campaigns/{campaign_id}/platform-content/tiktok/regenerate")
    assert res.status_code == 400
    assert "invalid platform" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_llm_provider_error_exception_handler_502(client: AsyncClient, monkeypatch):
    """Test LLMProviderError triggers 502 Bad Gateway response with custom message."""
    c_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = c_res.json()["id"]

    async def _failing_strat(db, campaign_id, llm_provider=None):
        raise LLMProviderError("API Rate Limit Exceeded (429)")

    monkeypatch.setattr(strategy_service, "generate_strategy_for_campaign", _failing_strat)

    res = await client.post(f"/api/v1/campaigns/{campaign_id}/strategy/generate")
    assert res.status_code == 502
    assert "llm provider error" in res.json()["detail"].lower()
