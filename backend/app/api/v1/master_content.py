"""
AI Marketing Content Engine — Master Content API Endpoints

REST API routes for generating, retrieving, and regenerating Master Content.
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.master_content import MasterContentResponse
from app.services import content_service

router = APIRouter(tags=["Master Content"])


@router.post(
    "/campaigns/{campaign_id}/master-content/generate",
    response_model=MasterContentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate master content for a campaign",
    description="Executes MasterContentAgent to produce a platform-neutral master narrative from Campaign Brief + Strategy.",
)
async def generate_master_content(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Generate master content for campaign."""
    return await content_service.generate_master_content_for_campaign(db, campaign_id)


@router.get(
    "/campaigns/{campaign_id}/master-content",
    response_model=MasterContentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get stored master content",
    description="Retrieve stored master content for a given campaign UUID.",
)
async def get_master_content_by_campaign(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get stored master content by campaign ID."""
    mc = await content_service.get_master_content_by_campaign(db, campaign_id)
    if not mc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No master content found for campaign ID '{campaign_id}'. Please generate master content first.",
        )
    return mc


@router.post(
    "/master-content/{master_content_id}/regenerate",
    response_model=MasterContentResponse,
    status_code=status.HTTP_200_OK,
    summary="Regenerate master content",
    description="Re-executes MasterContentAgent to produce a fresh platform-neutral master content blueprint.",
)
async def regenerate_master_content(
    master_content_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Regenerate master content by master content ID."""
    return await content_service.regenerate_master_content(db, master_content_id)
