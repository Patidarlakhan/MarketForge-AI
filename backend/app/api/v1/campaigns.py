"""
AI Marketing Content Engine — Campaign API Endpoints

REST API routes for managing marketing campaigns.
"""

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.campaign import (
    CampaignCreate,
    CampaignResponse,
    CampaignUpdate,
)
from app.services import campaign_service

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.post(
    "",
    response_model=CampaignResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new marketing campaign",
    description="Create a campaign brief containing objective, audience, personas, pain points, offer, and brand context.",
)
async def create_campaign(
    campaign_in: CampaignCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new marketing campaign."""
    return await campaign_service.create_campaign(db, campaign_in)


@router.get(
    "",
    response_model=List[CampaignResponse],
    status_code=status.HTTP_200_OK,
    summary="List all campaigns",
    description="Retrieve a paginated list of marketing campaigns ordered by creation date descending.",
)
async def list_campaigns(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of items to return"),
    db: AsyncSession = Depends(get_db),
):
    """List marketing campaigns."""
    return await campaign_service.list_campaigns(db, skip=skip, limit=limit)


@router.get(
    "/{campaign_id}",
    response_model=CampaignResponse,
    status_code=status.HTTP_200_OK,
    summary="Get campaign details",
    description="Retrieve a single marketing campaign by its UUID.",
)
async def get_campaign(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a single campaign by ID."""
    campaign = await campaign_service.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with ID '{campaign_id}' not found.",
        )
    return campaign


@router.patch(
    "/{campaign_id}",
    response_model=CampaignResponse,
    status_code=status.HTTP_200_OK,
    summary="Update campaign details",
    description="Update non-null fields of an existing marketing campaign.",
)
async def update_campaign(
    campaign_id: uuid.UUID,
    campaign_in: CampaignUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a campaign by ID."""
    campaign = await campaign_service.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with ID '{campaign_id}' not found.",
        )
    return await campaign_service.update_campaign(db, campaign, campaign_in)


@router.delete(
    "/{campaign_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a campaign",
    description="Delete an existing marketing campaign by its UUID.",
)
async def delete_campaign(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a campaign by ID."""
    campaign = await campaign_service.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with ID '{campaign_id}' not found.",
        )
    await campaign_service.delete_campaign(db, campaign)
    return None
