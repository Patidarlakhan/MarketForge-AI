"""
AI Marketing Content Engine — Independent Regeneration Integration Tests

Tests for independent single-platform regeneration, isolated version incrementing,
and verifying other platform assets remain unchanged.
"""

import pytest
from httpx import AsyncClient

from app.services import content_service, orchestrator_service, strategy_service
from tests.test_campaign_api import SAMPLE_CAMPAIGN
from tests.test_platform_content_api import FullSchemaMockLLMProvider


@pytest.fixture(autouse=True)
def mock_all_llm_services(monkeypatch):
    """Monkeypatch all agent services with FullSchemaMockLLMProvider."""
    orig_strat = strategy_service.generate_strategy_for_campaign
    orig_mc = content_service.generate_master_content_for_campaign
    orig_orch_all = orchestrator_service.generate_all_platform_content
    orig_orch_one = orchestrator_service.regenerate_single_platform_content

    async def _mocked_strat(db, campaign_id, llm_provider=None):
        return await orig_strat(db, campaign_id, llm_provider=FullSchemaMockLLMProvider())

    async def _mocked_mc(db, campaign_id, llm_provider=None):
        return await orig_mc(db, campaign_id, llm_provider=FullSchemaMockLLMProvider())

    async def _mocked_orch_all(db, campaign_id, llm_provider=None):
        return await orig_orch_all(db, campaign_id, llm_provider=FullSchemaMockLLMProvider())

    async def _mocked_orch_one(db, campaign_id, platform, llm_provider=None):
        return await orig_orch_one(db, campaign_id, platform, llm_provider=FullSchemaMockLLMProvider())

    monkeypatch.setattr(strategy_service, "generate_strategy_for_campaign", _mocked_strat)
    monkeypatch.setattr(content_service, "generate_master_content_for_campaign", _mocked_mc)
    monkeypatch.setattr(orchestrator_service, "generate_all_platform_content", _mocked_orch_all)
    monkeypatch.setattr(orchestrator_service, "regenerate_single_platform_content", _mocked_orch_one)


@pytest.mark.asyncio
async def test_independent_regeneration_versioning_flow(client: AsyncClient):
    """Test full multi-platform suite generation followed by targeted single-platform regeneration."""
    # 1. Create campaign & generate strategy + master content + all platform content
    c_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = c_res.json()["id"]

    await client.post(f"/api/v1/campaigns/{campaign_id}/strategy/generate")
    await client.post(f"/api/v1/campaigns/{campaign_id}/master-content/generate")
    pc_gen_res = await client.post(f"/api/v1/campaigns/{campaign_id}/platform-content/generate")
    assert pc_gen_res.status_code == 201

    initial_items = pc_gen_res.json()
    assert len(initial_items) == 4
    for item in initial_items:
        assert item["version"] == 1

    # 2. Regenerate Twitter single asset -> Version should become 2 for Twitter
    t1_res = await client.post(f"/api/v1/campaigns/{campaign_id}/platform-content/twitter/regenerate")
    assert t1_res.status_code == 200
    assert t1_res.json()["platform"] == "twitter"
    assert t1_res.json()["version"] == 2

    # 3. Regenerate Twitter a second time -> Version should become 3 for Twitter
    t2_res = await client.post(f"/api/v1/campaigns/{campaign_id}/platform-content/twitter/regenerate")
    assert t2_res.status_code == 200
    assert t2_res.json()["platform"] == "twitter"
    assert t2_res.json()["version"] == 3

    # 4. Regenerate LinkedIn -> Version should become 2 for LinkedIn
    l1_res = await client.post(f"/api/v1/campaigns/{campaign_id}/platform-content/linkedin/regenerate")
    assert l1_res.status_code == 200
    assert l1_res.json()["platform"] == "linkedin"
    assert l1_res.json()["version"] == 2

    # 5. Fetch all platform assets -> Twitter=v3, LinkedIn=v2, Instagram=v1, Blog=v1
    all_res = await client.get(f"/api/v1/campaigns/{campaign_id}/platform-content")
    assert all_res.status_code == 200
    version_map = {item["platform"]: item["version"] for item in all_res.json()}

    assert version_map["twitter"] == 3
    assert version_map["linkedin"] == 2
    assert version_map["instagram"] == 1
    assert version_map["blog"] == 1
