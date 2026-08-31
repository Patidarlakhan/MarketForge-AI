"""
AI Marketing Content Engine — Strategy API Integration Tests

Integration tests for Strategy generation, retrieval, and regeneration REST endpoints.
"""

import json
import uuid
import pytest
from httpx import AsyncClient

from tests.test_campaign_api import SAMPLE_CAMPAIGN
from tests.test_llm_provider import MockLLMProvider
from app.services import strategy_service
from app.schemas.strategy import StrategyOutput

MOCK_STRATEGY_JSON = json.dumps({
    "audience_insights": [
        "CEOs care about overall margin and risk mitigation.",
        "Head of Safety is driven by zero-incident compliance metrics."
    ],
    "content_pillars": [
        "Autonomous Site Safety",
        "Operational Efficiency & Delay Reduction",
        "ROI of Physical AI"
    ],
    "key_messages": [
        "Eliminate jobsite safety risks before they cause costly delays.",
        "Physical AI automates manual safety inspection reporting."
    ],
    "topics": [
        "How AI reduces OSHA safety penalties in commercial construction",
        "5 ways computer vision spots hazards faster than manual inspection",
        "The hidden cost of construction site delays in 2026"
    ],
    "content_angles": [
        "Myth-busting: Why safety technology accelerates projects rather than slowing them down",
        "Data-driven ROI benchmark report"
    ],
    "cta": {
        "primary": "Claim your Free Jobsite AI Assessment",
        "secondary": "Download the 2026 Construction AI Benchmark Report"
    }
})


@pytest.fixture(autouse=True)
def mock_strategy_llm(monkeypatch):
    """Automatically monkeypatch StrategyAgent to use MockLLMProvider in tests."""
    original_generate = strategy_service.generate_strategy_for_campaign

    async def _mocked_generate(db, campaign_id, llm_provider=None):
        mock_llm = MockLLMProvider(responses=[MOCK_STRATEGY_JSON])
        return await original_generate(db, campaign_id, llm_provider=mock_llm)

    monkeypatch.setattr(
        strategy_service,
        "generate_strategy_for_campaign",
        _mocked_generate,
    )


@pytest.mark.asyncio
async def test_generate_strategy_api(client: AsyncClient):
    """Test POST /api/v1/campaigns/{id}/strategy/generate."""
    # 1. Create campaign
    create_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = create_res.json()["id"]

    # 2. Generate strategy
    strat_res = await client.post(f"/api/v1/campaigns/{campaign_id}/strategy/generate")
    assert strat_res.status_code == 201
    data = strat_res.json()
    assert data["campaign_id"] == campaign_id
    assert data["status"] == "completed"
    assert len(data["content"]["content_pillars"]) == 3
    assert data["content"]["cta"]["primary"] == "Claim your Free Jobsite AI Assessment"

    # 3. Check campaign status updated to strategy_generated
    camp_res = await client.get(f"/api/v1/campaigns/{campaign_id}")
    assert camp_res.json()["status"] == "strategy_generated"


@pytest.mark.asyncio
async def test_get_strategy_api(client: AsyncClient):
    """Test GET /api/v1/campaigns/{id}/strategy."""
    create_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = create_res.json()["id"]

    # Generate strategy
    await client.post(f"/api/v1/campaigns/{campaign_id}/strategy/generate")

    # Get strategy
    get_res = await client.get(f"/api/v1/campaigns/{campaign_id}/strategy")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["campaign_id"] == campaign_id
    assert len(data["content"]["audience_insights"]) == 2


@pytest.mark.asyncio
async def test_get_strategy_not_found(client: AsyncClient):
    """Test GET strategy returns 404 when strategy hasn't been generated yet."""
    fake_id = str(uuid.uuid4())
    res = await client.get(f"/api/v1/campaigns/{fake_id}/strategy")
    assert res.status_code == 404
    assert "no strategy found" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_regenerate_strategy_api(client: AsyncClient):
    """Test POST /api/v1/campaigns/{id}/strategy/regenerate."""
    create_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = create_res.json()["id"]

    # Generate initially
    await client.post(f"/api/v1/campaigns/{campaign_id}/strategy/generate")

    # Regenerate
    regen_res = await client.post(f"/api/v1/campaigns/{campaign_id}/strategy/regenerate")
    assert regen_res.status_code == 200
    assert regen_res.json()["campaign_id"] == campaign_id
