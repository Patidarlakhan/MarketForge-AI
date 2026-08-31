"""
AI Marketing Content Engine — Platform Content API Integration Tests

Integration tests for generating, retrieving, and independently regenerating platform content.
"""

import json
import uuid
from typing import Any, Dict, Optional, Type
import pytest
from httpx import AsyncClient
from pydantic import BaseModel

from app.llm import LLMProvider
from app.services import content_service, orchestrator_service, strategy_service
from tests.test_campaign_api import SAMPLE_CAMPAIGN

MOCK_STRATEGY_JSON = json.dumps({
    "audience_insights": ["Insight 1", "Insight 2"],
    "content_pillars": ["Pillar 1", "Pillar 2"],
    "key_messages": ["Msg 1", "Msg 2"],
    "topics": ["Topic 1", "Topic 2", "Topic 3"],
    "content_angles": ["Angle 1", "Angle 2"],
    "cta": {"primary": "CTA 1", "secondary": "CTA 2"}
})

MOCK_MASTER_CONTENT_JSON = json.dumps({
    "title": "Master Title",
    "core_idea": "Core idea text summary",
    "problem": "Problem text breakdown",
    "solution": "Solution text positioning",
    "business_value": ["Value 1", "Value 2"],
    "target_personas": ["Persona 1"],
    "key_message": "Overarching key message",
    "cta": {"primary": "Primary CTA", "secondary": "Secondary CTA"}
})

MOCK_LINKEDIN_JSON = json.dumps({
    "post_text": "Long form LinkedIn post text for testing orchestrator service. " * 3,
    "carousel_slides": [
        {"slide_number": 1, "header": "Title", "body_points": ["Point 1"]},
        {"slide_number": 2, "header": "Problem", "body_points": ["Point 2"]},
        {"slide_number": 3, "header": "Solution", "body_points": ["Point 3"]}
    ]
})

MOCK_TWITTER_JSON = json.dumps({
    "thread": [
        {"tweet_number": 1, "text": "Tweet 1 text for orchestrator service testing."},
        {"tweet_number": 2, "text": "Tweet 2 text breakdown of the problem statement."},
        {"tweet_number": 3, "text": "Tweet 3 text call to action and hashtags #AI #Tech"}
    ],
    "single_post": "Single standalone tweet text under 280 chars."
})

MOCK_INSTAGRAM_JSON = json.dumps({
    "caption": "Instagram caption with #Construction #AI hashtags. " * 2,
    "image_prompt": "Midjourney visual prompt style raw --ar 4:5 detailed lighting and photorealistic elements",
    "reel_script": [
        {"scene_number": 1, "visual_direction": "Zoom in", "audio_cue": "Chime", "spoken_text": "Hello text"},
        {"scene_number": 2, "visual_direction": "Cut to product", "audio_cue": "Beep", "spoken_text": "Problem text"},
        {"scene_number": 3, "visual_direction": "Show results", "audio_cue": "Cheer", "spoken_text": "Solution text"}
    ]
})

MOCK_BLOG_JSON = json.dumps({
    "title": "Blog Title SEO Headline",
    "meta_description": "Comprehensive meta description summary for search engines and targeted audience.",
    "slug": "blog-title-seo-headline",
    "target_keywords": ["keyword 1", "keyword 2"],
    "markdown_content": """# Blog Title SEO Headline

Commercial construction leaders face an ongoing dilemma: maintaining strict safety standards without delaying critical path timelines.

## The Problem
Traditional safety management relies on paper checklists and periodic physical walkthroughs.

## The Solution
Physical AI integrates high-resolution computer vision cameras across active jobsites to provide 24/7 automated hazard detection.
"""
})


class FullSchemaMockLLMProvider(LLMProvider):
    """Mock LLM Provider that maps response_model to appropriate mock JSON."""

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: Type[BaseModel],
    ) -> BaseModel:
        model_name = response_model.__name__

        if model_name == "StrategyOutput":
            json_str = MOCK_STRATEGY_JSON
        elif model_name == "MasterContentOutput":
            json_str = MOCK_MASTER_CONTENT_JSON
        elif model_name == "LinkedInOutput":
            json_str = MOCK_LINKEDIN_JSON
        elif model_name == "TwitterOutput":
            json_str = MOCK_TWITTER_JSON
        elif model_name == "InstagramOutput":
            json_str = MOCK_INSTAGRAM_JSON
        elif model_name == "BlogOutput":
            json_str = MOCK_BLOG_JSON
        else:
            json_str = MOCK_STRATEGY_JSON

        return response_model.model_validate_json(json_str)

    async def generate_raw(
        self,
        system_prompt: str,
        user_prompt: str,
        schema_json: Optional[Dict[str, Any]] = None,
    ) -> str:
        return MOCK_STRATEGY_JSON


@pytest.fixture(autouse=True)
def mock_api_llm_services(monkeypatch):
    """Automatically monkeypatch LLM execution with FullSchemaMockLLMProvider."""
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
async def test_generate_all_platform_content_api(client: AsyncClient):
    """Test POST /api/v1/campaigns/{id}/platform-content/generate."""
    # Create campaign
    c_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = c_res.json()["id"]

    # Generate strategy & master content
    await client.post(f"/api/v1/campaigns/{campaign_id}/strategy/generate")
    await client.post(f"/api/v1/campaigns/{campaign_id}/master-content/generate")

    # Generate all platform content
    pc_res = await client.post(f"/api/v1/campaigns/{campaign_id}/platform-content/generate")
    assert pc_res.status_code == 201
    items = pc_res.json()
    assert len(items) == 4
    platforms = {item["platform"] for item in items}
    assert platforms == {"linkedin", "twitter", "instagram", "blog"}

    # Check campaign status is COMPLETED
    camp_res = await client.get(f"/api/v1/campaigns/{campaign_id}")
    assert camp_res.json()["status"] == "completed"


@pytest.mark.asyncio
async def test_get_all_and_single_platform_content_api(client: AsyncClient):
    """Test GET all and GET single platform content endpoints."""
    c_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = c_res.json()["id"]

    await client.post(f"/api/v1/campaigns/{campaign_id}/strategy/generate")
    await client.post(f"/api/v1/campaigns/{campaign_id}/master-content/generate")
    await client.post(f"/api/v1/campaigns/{campaign_id}/platform-content/generate")

    # Get all
    all_res = await client.get(f"/api/v1/campaigns/{campaign_id}/platform-content")
    assert all_res.status_code == 200
    assert len(all_res.json()) == 4

    # Get single (LinkedIn)
    single_res = await client.get(f"/api/v1/campaigns/{campaign_id}/platform-content/linkedin")
    assert single_res.status_code == 200
    assert single_res.json()["platform"] == "linkedin"
    assert "post_text" in single_res.json()["content"]


@pytest.mark.asyncio
async def test_regenerate_single_platform_content_api(client: AsyncClient):
    """Test POST /api/v1/campaigns/{id}/platform-content/{platform}/regenerate."""
    c_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = c_res.json()["id"]

    await client.post(f"/api/v1/campaigns/{campaign_id}/strategy/generate")
    await client.post(f"/api/v1/campaigns/{campaign_id}/master-content/generate")
    await client.post(f"/api/v1/campaigns/{campaign_id}/platform-content/generate")

    # Regenerate Twitter single asset
    regen_res = await client.post(f"/api/v1/campaigns/{campaign_id}/platform-content/twitter/regenerate")
    assert regen_res.status_code == 200
    assert regen_res.json()["platform"] == "twitter"
    assert regen_res.json()["version"] == 2
