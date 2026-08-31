"""
AI Marketing Content Engine — Platform Content API Endpoints

REST API routes for generating, retrieving, and independently regenerating platform content
(LinkedIn, Twitter, Instagram, Blog).
"""

import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.platform_content import PlatformContentResponse
from app.services import orchestrator_service

router = APIRouter(prefix="/campaigns", tags=["Platform Content"])


@router.post(
    "/{campaign_id}/platform-content/generate",
    response_model=List[PlatformContentResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Generate all platform content in parallel",
    description="Executes LinkedIn, Twitter, Instagram, and Blog agents in parallel via Content Orchestrator.",
)
async def generate_all_platform_content(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Generate all platform content assets in parallel."""
    return await orchestrator_service.generate_all_platform_content(db, campaign_id)


@router.get(
    "/{campaign_id}/platform-content",
    response_model=List[PlatformContentResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all generated platform content items",
    description="Retrieve stored platform content assets for a given campaign.",
)
async def get_all_platform_content(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get all platform content assets for a campaign."""
    return await orchestrator_service.get_platform_contents_by_campaign(db, campaign_id)


@router.get(
    "/{campaign_id}/platform-content/{platform}",
    response_model=PlatformContentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get content for a specific platform",
    description="Retrieve the latest content item for a single platform (linkedin, twitter, instagram, or blog).",
)
async def get_single_platform_content(
    campaign_id: uuid.UUID,
    platform: str,
    db: AsyncSession = Depends(get_db),
):
    """Get platform content asset by platform name."""
    pc = await orchestrator_service.get_single_platform_content(db, campaign_id, platform)
    if not pc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No content found for platform '{platform}' in campaign '{campaign_id}'.",
        )
    return pc


@router.post(
    "/{campaign_id}/platform-content/{platform}/regenerate",
    response_model=PlatformContentResponse,
    status_code=status.HTTP_200_OK,
    summary="Independently regenerate content for a single platform",
    description="Re-executes agent for a specific platform (linkedin, twitter, instagram, blog) and increments version.",
)
async def regenerate_single_platform_content(
    campaign_id: uuid.UUID,
    platform: str,
    db: AsyncSession = Depends(get_db),
):
    """Independently regenerate single platform content asset."""
    return await orchestrator_service.regenerate_single_platform_content(db, campaign_id, platform)


@router.put(
    "/platform-content/{content_id}",
    response_model=PlatformContentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update platform content payload",
    description="Allows editing of the platform content JSON payload.",
)
async def update_platform_content(
    content_id: uuid.UUID,
    payload: dict,
    db: AsyncSession = Depends(get_db),
):
    """Update platform content JSON payload by ID."""
    content_data = payload.get("content", payload)
    return await orchestrator_service.update_platform_content_by_id(db, content_id, content_data)

