"""
AI Marketing Content Engine — Content Editing Integration Tests

Tests for updating platform content via PUT /api/v1/platform-content/{content_id}.
"""

import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign, CampaignStatus
from app.models.platform_content import PlatformContent


@pytest.mark.asyncio
async def test_update_platform_content_api_success(client: AsyncClient, db_session: AsyncSession):
    """Test editing platform content via PUT /api/v1/platform-content/{id}."""
    # 1. Seed campaign & platform content
    campaign = Campaign(
        name="Edit Test Campaign",
        objective="Lead Generation",
        industry="Tech",
        product_service="SaaS",
        target_audience="CTOs",
        status=CampaignStatus.COMPLETED,
    )
    db_session.add(campaign)
    await db_session.commit()

    pc = PlatformContent(
        campaign_id=campaign.id,
        platform="linkedin",
        content={"post_text": "Original post text before edit", "carousel_slides": []},
        status="completed",
        version=1,
    )
    db_session.add(pc)
    await db_session.commit()
    await db_session.refresh(pc)

    # 2. Update platform content
    updated_payload = {
        "content": {
            "post_text": "Manually edited and polished LinkedIn post text!",
            "carousel_slides": []
        }
    }

    res = await client.put(f"/api/v1/campaigns/platform-content/{pc.id}", json=updated_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == str(pc.id)
    assert data["content"]["post_text"] == "Manually edited and polished LinkedIn post text!"

    # 3. Verify DB record updated
    await db_session.refresh(pc)
    assert pc.content["post_text"] == "Manually edited and polished LinkedIn post text!"


@pytest.mark.asyncio
async def test_update_platform_content_not_found(client: AsyncClient):
    """Test PUT /api/v1/campaigns/platform-content/{fake_id} returns 404."""
    fake_id = str(uuid.uuid4())
    res = await client.put(f"/api/v1/campaigns/platform-content/{fake_id}", json={"content": {}})
    assert res.status_code == 404
