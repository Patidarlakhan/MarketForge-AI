"""
AI Marketing Content Engine — Content Orchestrator Unit Tests

Tests for parallel multi-agent orchestration and single-platform independent regeneration.
"""

import json
from typing import Any, Dict, Optional, Type
import pytest
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.llm import LLMProvider
from app.models.campaign import Campaign, CampaignStatus
from app.models.master_content import MasterContent
from app.models.strategy import MarketingStrategy
from app.services import orchestrator_service

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


class SchemaAwareMockLLMProvider(LLMProvider):
    """Mock LLM Provider that inspects response_model to return schema-matched JSON responses for parallel execution."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_count = 0

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: Type[BaseModel],
    ) -> BaseModel:
        self.call_count += 1
        model_name = response_model.__name__

        if model_name == "LinkedInOutput":
            json_str = MOCK_LINKEDIN_JSON
        elif model_name == "TwitterOutput":
            json_str = MOCK_TWITTER_JSON
        elif model_name == "InstagramOutput":
            json_str = MOCK_INSTAGRAM_JSON
        elif model_name == "BlogOutput":
            json_str = MOCK_BLOG_JSON
        else:
            json_str = MOCK_LINKEDIN_JSON

        return response_model.model_validate_json(json_str)

    async def generate_raw(
        self,
        system_prompt: str,
        user_prompt: str,
        schema_json: Optional[Dict[str, Any]] = None,
    ) -> str:
        return MOCK_LINKEDIN_JSON


@pytest.mark.asyncio
async def test_generate_all_platform_content_success(db_session: AsyncSession):
    """Test parallel generation of LinkedIn, Twitter, Instagram, and Blog assets."""
    campaign = Campaign(
        name="Orchestrator Test Campaign",
        objective="Lead Generation",
        industry="Technology",
        product_service="Test Product",
        target_audience="CTOs",
        status=CampaignStatus.MASTER_CONTENT_GENERATED,
    )
    db_session.add(campaign)
    await db_session.commit()

    strategy = MarketingStrategy(
        campaign_id=campaign.id,
        content={
            "audience_insights": ["Insight 1", "Insight 2"],
            "content_pillars": ["Pillar 1", "Pillar 2"],
            "key_messages": ["Msg 1", "Msg 2"],
            "topics": ["Topic 1", "Topic 2", "Topic 3"],
            "content_angles": ["Angle 1", "Angle 2"],
            "cta": {"primary": "CTA 1", "secondary": "CTA 2"}
        }
    )
    db_session.add(strategy)

    master_content = MasterContent(
        campaign_id=campaign.id,
        content={
            "title": "Master Title",
            "core_idea": "Core idea text summary",
            "problem": "Problem text breakdown",
            "solution": "Solution text positioning",
            "business_value": ["Value 1", "Value 2"],
            "target_personas": ["Persona 1"],
            "key_message": "Overarching key message",
            "cta": {"primary": "Primary CTA", "secondary": "Secondary CTA"}
        }
    )
    db_session.add(master_content)
    await db_session.commit()

    mock_llm = SchemaAwareMockLLMProvider()

    results = await orchestrator_service.generate_all_platform_content(
        db=db_session,
        campaign_id=campaign.id,
        llm_provider=mock_llm,
    )

    assert len(results) == 4
    platforms_generated = {r.platform for r in results}
    assert platforms_generated == {"linkedin", "twitter", "instagram", "blog"}

    await db_session.refresh(campaign)
    assert campaign.status == CampaignStatus.COMPLETED


@pytest.mark.asyncio
async def test_regenerate_single_platform_content_success(db_session: AsyncSession):
    """Test independent single-platform regeneration increments version."""
    campaign = Campaign(
        name="Regen Test Campaign",
        objective="Lead Generation",
        industry="Tech",
        product_service="SaaS",
        target_audience="DevOps",
        status=CampaignStatus.COMPLETED,
    )
    db_session.add(campaign)
    await db_session.commit()

    master_content = MasterContent(
        campaign_id=campaign.id,
        content={
            "title": "Master Title",
            "core_idea": "Core idea",
            "problem": "Problem",
            "solution": "Solution",
            "business_value": ["Value 1", "Value 2"],
            "target_personas": ["Persona 1"],
            "key_message": "Key Message",
            "cta": {"primary": "Primary CTA", "secondary": "Secondary CTA"}
        }
    )
    db_session.add(master_content)
    await db_session.commit()

    mock_llm = SchemaAwareMockLLMProvider()

    record = await orchestrator_service.regenerate_single_platform_content(
        db=db_session,
        campaign_id=campaign.id,
        platform="twitter",
        llm_provider=mock_llm,
    )

    assert record.platform == "twitter"
    assert record.version == 1
    assert "single_post" in record.content

    record_v2 = await orchestrator_service.regenerate_single_platform_content(
        db=db_session,
        campaign_id=campaign.id,
        platform="twitter",
        llm_provider=mock_llm,
    )
    assert record_v2.version == 2
