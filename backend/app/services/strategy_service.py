"""
AI Marketing Content Engine — Strategy Service Layer

Business logic for generating, retrieving, and regenerating marketing strategies.
"""

import uuid
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.strategy_agent import StrategyAgent
from app.llm import LLMProvider
from app.models.campaign import Campaign, CampaignStatus
from app.models.strategy import MarketingStrategy
from app.services import campaign_service


async def get_strategy_by_campaign(
    db: AsyncSession,
    campaign_id: uuid.UUID,
) -> Optional[MarketingStrategy]:
    """
    Retrieve stored marketing strategy for a campaign.
    """
    result = await db.execute(
        select(MarketingStrategy).where(MarketingStrategy.campaign_id == campaign_id)
    )
    return result.scalar_one_or_none()


async def generate_strategy_for_campaign(
    db: AsyncSession,
    campaign_id: uuid.UUID,
    llm_provider: Optional[LLMProvider] = None,
) -> MarketingStrategy:
    """
    Execute StrategyAgent for campaign and persist generated strategy in database.
    Updates Campaign status from DRAFT -> STRATEGY_GENERATION -> STRATEGY_GENERATED.
    """
    campaign = await campaign_service.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with ID '{campaign_id}' not found.",
        )

    # Transition status to generating
    campaign.status = CampaignStatus.STRATEGY_GENERATION
    db.add(campaign)
    await db.commit()

    try:
        # Run StrategyAgent
        agent = StrategyAgent(llm_provider=llm_provider)
        strategy_output = await agent.run(campaign)

        # Upsert MarketingStrategy record
        existing_strategy = await get_strategy_by_campaign(db, campaign_id)
        if existing_strategy:
            existing_strategy.content = strategy_output.model_dump()
            existing_strategy.status = "completed"
            db.add(existing_strategy)
            strategy_record = existing_strategy
        else:
            strategy_record = MarketingStrategy(
                campaign_id=campaign_id,
                content=strategy_output.model_dump(),
                status="completed",
            )
            db.add(strategy_record)

        # Transition campaign status to strategy_generated
        campaign.status = CampaignStatus.STRATEGY_GENERATED
        db.add(campaign)

        await db.commit()
        await db.refresh(strategy_record)
        return strategy_record

    except Exception as exc:
        # Mark campaign as failed on error
        campaign.status = CampaignStatus.FAILED
        db.add(campaign)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Strategy generation failed: {exc}",
        ) from exc


async def regenerate_strategy_for_campaign(
    db: AsyncSession,
    campaign_id: uuid.UUID,
    llm_provider: Optional[LLMProvider] = None,
) -> MarketingStrategy:
    """
    Regenerate marketing strategy for a campaign.
    """
    return await generate_strategy_for_campaign(db, campaign_id, llm_provider=llm_provider)
