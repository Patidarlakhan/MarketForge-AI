"""
AI Marketing Content Engine — Master Content API Integration Tests

Integration tests for Master Content generation, retrieval, and regeneration REST endpoints.
"""

import json
import uuid
import pytest
from httpx import AsyncClient

from tests.test_campaign_api import SAMPLE_CAMPAIGN
from tests.test_llm_provider import MockLLMProvider
from app.services import content_service, strategy_service

MOCK_STRATEGY_JSON = json.dumps({
    "audience_insights": ["CEOs care about margin protection.", "Head of Safety wants zero incidents."],
    "content_pillars": ["Autonomous Site Safety", "Delay Reduction"],
    "key_messages": ["Zero delays on active jobsites.", "Automated hazard detection."],
    "topics": ["OSHA penalties reduction", "Computer vision vs manual inspection", "Cost of delays"],
    "content_angles": ["Myth-busting tech adoption", "ROI benchmark report"],
    "cta": {"primary": "Schedule Demo", "secondary": "Learn More"}
})

MOCK_MASTER_CONTENT_JSON = json.dumps({
    "title": "Eliminating Jobsite Delays with Safety Inspection AI",
    "core_idea": "Deploying computer vision AI eliminates inspection bottlenecks.",
    "problem": "Manual safety inspections are slow and cause project delays.",
    "solution": "Physical AI provides 24/7 automated hazard detection.",
    "business_value": [
        "40% reduction in safety-related delays",
        "Zero OSHA non-compliance penalties"
    ],
    "target_personas": ["CEO", "Head of Safety"],
    "key_message": "Transform safety into an operational efficiency advantage.",
    "cta": {
        "primary": "Claim your Free Jobsite AI Assessment",
        "secondary": "Download Report"
    }
})


@pytest.fixture(autouse=True)
def mock_llm_services(monkeypatch):
    """Automatically monkeypatch LLM calls for Strategy & MasterContent services."""
    orig_strat = strategy_service.generate_strategy_for_campaign
    orig_mc = content_service.generate_master_content_for_campaign

    async def _mocked_strat(db, campaign_id, llm_provider=None):
        return await orig_strat(db, campaign_id, llm_provider=MockLLMProvider([MOCK_STRATEGY_JSON]))

    async def _mocked_mc(db, campaign_id, llm_provider=None):
        return await orig_mc(db, campaign_id, llm_provider=MockLLMProvider([MOCK_MASTER_CONTENT_JSON]))

    monkeypatch.setattr(strategy_service, "generate_strategy_for_campaign", _mocked_strat)
    monkeypatch.setattr(content_service, "generate_master_content_for_campaign", _mocked_mc)


@pytest.mark.asyncio
async def test_generate_master_content_api(client: AsyncClient):
    """Test POST /api/v1/campaigns/{id}/master-content/generate."""
    # 1. Create campaign
    c_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = c_res.json()["id"]

    # 2. Generate strategy first
    await client.post(f"/api/v1/campaigns/{campaign_id}/strategy/generate")

    # 3. Generate master content
    mc_res = await client.post(f"/api/v1/campaigns/{campaign_id}/master-content/generate")
    assert mc_res.status_code == 201
    data = mc_res.json()
    assert data["campaign_id"] == campaign_id
    assert data["content"]["title"].startswith("Eliminating Jobsite Delays")
    assert len(data["content"]["business_value"]) == 2

    # 4. Check campaign status updated to master_content_generated
    camp_res = await client.get(f"/api/v1/campaigns/{campaign_id}")
    assert camp_res.json()["status"] == "master_content_generated"


@pytest.mark.asyncio
async def test_generate_master_content_without_strategy_fails(client: AsyncClient):
    """Test generating master content without existing strategy returns 400 Bad Request."""
    c_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = c_res.json()["id"]

    mc_res = await client.post(f"/api/v1/campaigns/{campaign_id}/master-content/generate")
    assert mc_res.status_code == 400
    assert "strategy must be generated" in mc_res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_master_content_api(client: AsyncClient):
    """Test GET /api/v1/campaigns/{id}/master-content."""
    c_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = c_res.json()["id"]

    await client.post(f"/api/v1/campaigns/{campaign_id}/strategy/generate")
    await client.post(f"/api/v1/campaigns/{campaign_id}/master-content/generate")

    get_res = await client.get(f"/api/v1/campaigns/{campaign_id}/master-content")
    assert get_res.status_code == 200
    assert get_res.json()["campaign_id"] == campaign_id


@pytest.mark.asyncio
async def test_regenerate_master_content_api(client: AsyncClient):
    """Test POST /api/v1/master-content/{id}/regenerate."""
    c_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = c_res.json()["id"]

    await client.post(f"/api/v1/campaigns/{campaign_id}/strategy/generate")
    mc_res = await client.post(f"/api/v1/campaigns/{campaign_id}/master-content/generate")
    mc_id = mc_res.json()["id"]

    regen_res = await client.post(f"/api/v1/master-content/{mc_id}/regenerate")
    assert regen_res.status_code == 200
    assert regen_res.json()["id"] == mc_id
