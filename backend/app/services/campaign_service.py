"""
AI Marketing Content Engine — Campaign Service Layer

Business logic and database access functions for marketing campaigns.
"""

import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate


async def create_campaign(
    db: AsyncSession,
    campaign_in: CampaignCreate,
) -> Campaign:
    """
    Create a new marketing campaign in the database.
    """
    campaign_data = campaign_in.model_dump()
    db_campaign = Campaign(**campaign_data)
    db.add(db_campaign)
    await db.commit()
    await db.refresh(db_campaign)
    return db_campaign


async def get_campaign(
    db: AsyncSession,
    campaign_id: uuid.UUID,
) -> Optional[Campaign]:
    """
    Retrieve a single campaign by UUID.
    """
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id)
    )
    return result.scalar_one_or_none()


async def list_campaigns(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 50,
) -> List[Campaign]:
    """
    Retrieve a paginated list of campaigns ordered by creation date descending.
    """
    result = await db.execute(
        select(Campaign)
        .order_by(Campaign.created_at.desc(), Campaign.id.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def update_campaign(
    db: AsyncSession,
    db_campaign: Campaign,
    campaign_in: CampaignUpdate,
) -> Campaign:
    """
    Update an existing campaign with non-None fields from CampaignUpdate.
    """
    update_data = campaign_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_campaign, field, value)

    db.add(db_campaign)
    await db.commit()
    await db.refresh(db_campaign)
    return db_campaign


async def delete_campaign(
    db: AsyncSession,
    db_campaign: Campaign,
) -> None:
    """
    Delete a campaign from the database.
    """
    await db.delete(db_campaign)
    await db.commit()
