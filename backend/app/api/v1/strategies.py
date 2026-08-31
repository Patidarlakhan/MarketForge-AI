"""
AI Marketing Content Engine — Strategy API Endpoints

REST API routes for generating, retrieving, and regenerating marketing strategies.
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.strategy import StrategyResponse
from app.services import strategy_service

router = APIRouter(prefix="/campaigns", tags=["Strategies"])


@router.post(
    "/{campaign_id}/strategy/generate",
    response_model=StrategyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate marketing strategy for a campaign",
    description="Executes the StrategyAgent to generate buyer insights, content pillars, key messages, topics, angles, and CTAs.",
)
async def generate_strategy(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Generate marketing strategy for campaign."""
    return await strategy_service.generate_strategy_for_campaign(db, campaign_id)


@router.get(
    "/{campaign_id}/strategy",
    response_model=StrategyResponse,
    status_code=status.HTTP_200_OK,
    summary="Get stored campaign strategy",
    description="Retrieve the stored marketing strategy for a given campaign UUID.",
)
async def get_strategy(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get stored marketing strategy."""
    strategy = await strategy_service.get_strategy_by_campaign(db, campaign_id)
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No strategy found for campaign ID '{campaign_id}'. Please generate a strategy first.",
        )
    return strategy


@router.post(
    "/{campaign_id}/strategy/regenerate",
    response_model=StrategyResponse,
    status_code=status.HTTP_200_OK,
    summary="Regenerate marketing strategy",
    description="Re-executes the StrategyAgent to produce a fresh marketing strategy for the campaign.",
)
async def regenerate_strategy(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Regenerate marketing strategy."""
    return await strategy_service.regenerate_strategy_for_campaign(db, campaign_id)
