"""
AI Marketing Content Engine — Master Content Service Layer

Business logic for generating, retrieving, and regenerating Master Content.
"""

import uuid
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.master_content_agent import MasterContentAgent
from app.llm import LLMProvider
from app.models.campaign import CampaignStatus
from app.models.master_content import MasterContent
from app.services import campaign_service, strategy_service


async def get_master_content_by_campaign(
    db: AsyncSession,
    campaign_id: uuid.UUID,
) -> Optional[MasterContent]:
    """
    Retrieve stored Master Content for a campaign.
    """
    result = await db.execute(
        select(MasterContent).where(MasterContent.campaign_id == campaign_id)
    )
    return result.scalar_one_or_none()


async def get_master_content(
    db: AsyncSession,
    master_content_id: uuid.UUID,
) -> Optional[MasterContent]:
    """
    Retrieve stored Master Content by its UUID primary key.
    """
    result = await db.execute(
        select(MasterContent).where(MasterContent.id == master_content_id)
    )
    return result.scalar_one_or_none()


async def generate_master_content_for_campaign(
    db: AsyncSession,
    campaign_id: uuid.UUID,
    llm_provider: Optional[LLMProvider] = None,
) -> MasterContent:
    """
    Execute MasterContentAgent for campaign and persist master content in database.
    Requires an existing strategy for the campaign.
    Updates Campaign status: strategy_generated -> master_content_generation -> master_content_generated.
    """
    campaign = await campaign_service.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with ID '{campaign_id}' not found.",
        )

    strategy = await strategy_service.get_strategy_by_campaign(db, campaign_id)
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Strategy must be generated before generating master content for campaign '{campaign_id}'.",
        )

    # Transition status to generating
    campaign.status = CampaignStatus.MASTER_CONTENT_GENERATION
    db.add(campaign)
    await db.commit()

    try:
        # Run MasterContentAgent
        agent = MasterContentAgent(llm_provider=llm_provider)
        master_output = await agent.run(campaign_data=campaign, strategy_data=strategy)

        # Upsert MasterContent record
        existing_mc = await get_master_content_by_campaign(db, campaign_id)
        if existing_mc:
            existing_mc.content = master_output.model_dump()
            existing_mc.status = "completed"
            db.add(existing_mc)
            mc_record = existing_mc
        else:
            mc_record = MasterContent(
                campaign_id=campaign_id,
                content=master_output.model_dump(),
                status="completed",
            )
            db.add(mc_record)

        # Transition campaign status to master_content_generated
        campaign.status = CampaignStatus.MASTER_CONTENT_GENERATED
        db.add(campaign)

        await db.commit()
        await db.refresh(mc_record)
        return mc_record

    except Exception as exc:
        campaign.status = CampaignStatus.FAILED
        db.add(campaign)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Master content generation failed: {exc}",
        ) from exc


async def regenerate_master_content(
    db: AsyncSession,
    master_content_id: uuid.UUID,
    llm_provider: Optional[LLMProvider] = None,
) -> MasterContent:
    """
    Regenerate Master Content by MasterContent ID.
    """
    mc = await get_master_content(db, master_content_id)
    if not mc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Master Content with ID '{master_content_id}' not found.",
        )

    return await generate_master_content_for_campaign(
        db=db,
        campaign_id=mc.campaign_id,
        llm_provider=llm_provider,
    )
