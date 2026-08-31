"""
AI Marketing Content Engine — Content Orchestrator Service

Orchestrates multi-agent parallel execution of platform-specific content generators
(LinkedIn, Twitter, Instagram, Blog) from Master Content.
"""

import asyncio
import logging
import uuid
from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.blog_agent import BlogAgent
from app.agents.instagram_agent import InstagramAgent
from app.agents.linkedin_agent import LinkedInAgent
from app.agents.twitter_agent import TwitterAgent
from app.llm import LLMProvider
from app.models.campaign import CampaignStatus
from app.models.platform_content import PlatformContent
from app.services import campaign_service, content_service

logger = logging.getLogger(__name__)


async def get_platform_contents_by_campaign(
    db: AsyncSession,
    campaign_id: uuid.UUID,
) -> List[PlatformContent]:
    """Retrieve all generated platform content items for a campaign."""
    result = await db.execute(
        select(PlatformContent)
        .where(PlatformContent.campaign_id == campaign_id)
        .order_by(PlatformContent.created_at.desc())
    )
    return list(result.scalars().all())


async def get_single_platform_content(
    db: AsyncSession,
    campaign_id: uuid.UUID,
    platform: str,
) -> Optional[PlatformContent]:
    """Retrieve the latest platform content item for a specific campaign & platform."""
    result = await db.execute(
        select(PlatformContent)
        .where(
            PlatformContent.campaign_id == campaign_id,
            PlatformContent.platform == platform.lower(),
        )
        .order_by(PlatformContent.version.desc())
    )
    return result.scalars().first()


async def generate_all_platform_content(
    db: AsyncSession,
    campaign_id: uuid.UUID,
    llm_provider: Optional[LLMProvider] = None,
) -> List[PlatformContent]:
    """
    Execute LinkedIn, Twitter, Instagram, and Blog agents IN PARALLEL using asyncio.gather().
    Updates Campaign status from master_content_generated -> platform_content_generation -> completed.
    """
    campaign = await campaign_service.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with ID '{campaign_id}' not found.",
        )

    master_content = await content_service.get_master_content_by_campaign(db, campaign_id)
    if not master_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Master content must be generated before generating platform content for campaign '{campaign_id}'.",
        )

    # Transition campaign status
    campaign.status = CampaignStatus.PLATFORM_CONTENT_GENERATION
    db.add(campaign)
    await db.commit()

    try:
        # Instantiate agents
        linkedin_agent = LinkedInAgent(llm_provider=llm_provider)
        twitter_agent = TwitterAgent(llm_provider=llm_provider)
        instagram_agent = InstagramAgent(llm_provider=llm_provider)
        blog_agent = BlogAgent(llm_provider=llm_provider)

        logger.info(f"Orchestrator starting PARALLEL execution of 4 agents for campaign '{campaign.name}'")

        # Execute agents in parallel via asyncio.gather()
        linkedin_task = linkedin_agent.run(master_content, campaign)
        twitter_task = twitter_agent.run(master_content, campaign)
        instagram_task = instagram_agent.run(master_content, campaign)
        blog_task = blog_agent.run(master_content, campaign)

        linkedin_out, twitter_out, instagram_out, blog_out = await asyncio.gather(
            linkedin_task,
            twitter_task,
            instagram_task,
            blog_task,
        )

        outputs: Dict[str, Any] = {
            "linkedin": linkedin_out.model_dump(),
            "twitter": twitter_out.model_dump(),
            "instagram": instagram_out.model_dump(),
            "blog": blog_out.model_dump(),
        }

        saved_records: List[PlatformContent] = []

        for p_name, p_content in outputs.items():
            existing = await get_single_platform_content(db, campaign_id, p_name)
            if existing:
                existing.content = p_content
                existing.status = "completed"
                db.add(existing)
                saved_records.append(existing)
            else:
                record = PlatformContent(
                    campaign_id=campaign_id,
                    platform=p_name,
                    content=p_content,
                    status="completed",
                    version=1,
                )
                db.add(record)
                saved_records.append(record)

        # Transition campaign status to COMPLETED
        campaign.status = CampaignStatus.COMPLETED
        db.add(campaign)

        await db.commit()
        for r in saved_records:
            await db.refresh(r)

        return saved_records

    except Exception as exc:
        campaign.status = CampaignStatus.FAILED
        db.add(campaign)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Platform content generation failed: {exc}",
        ) from exc


async def regenerate_single_platform_content(
    db: AsyncSession,
    campaign_id: uuid.UUID,
    platform: str,
    llm_provider: Optional[LLMProvider] = None,
) -> PlatformContent:
    """
    Independently regenerate content for a single platform (e.g. 'linkedin', 'twitter', 'instagram', 'blog').
    """
    platform_key = platform.lower()
    valid_platforms = ["linkedin", "twitter", "instagram", "blog"]
    if platform_key not in valid_platforms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid platform '{platform}'. Must be one of: {valid_platforms}",
        )

    campaign = await campaign_service.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with ID '{campaign_id}' not found.",
        )

    master_content = await content_service.get_master_content_by_campaign(db, campaign_id)
    if not master_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Master content must be generated before regenerating platform content for campaign '{campaign_id}'.",
        )

    try:
        if platform_key == "linkedin":
            out = await LinkedInAgent(llm_provider=llm_provider).run(master_content, campaign)
        elif platform_key == "twitter":
            out = await TwitterAgent(llm_provider=llm_provider).run(master_content, campaign)
        elif platform_key == "instagram":
            out = await InstagramAgent(llm_provider=llm_provider).run(master_content, campaign)
        else:
            out = await BlogAgent(llm_provider=llm_provider).run(master_content, campaign)

        existing = await get_single_platform_content(db, campaign_id, platform_key)
        if existing:
            existing.content = out.model_dump()
            existing.version += 1
            existing.status = "completed"
            db.add(existing)
            record = existing
        else:
            record = PlatformContent(
                campaign_id=campaign_id,
                platform=platform_key,
                content=out.model_dump(),
                status="completed",
                version=1,
            )
            db.add(record)

        await db.commit()
        await db.refresh(record)
        return record

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Single platform content regeneration failed for '{platform_key}': {exc}",
        ) from exc


async def update_platform_content_by_id(
    db: AsyncSession,
    content_id: uuid.UUID,
    new_content: Dict[str, Any],
) -> PlatformContent:
    """
    Update the JSON content payload of a platform content item by ID.
    """
    result = await db.execute(
        select(PlatformContent).where(PlatformContent.id == content_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Platform content with ID '{content_id}' not found.",
        )

    record.content = new_content
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record

