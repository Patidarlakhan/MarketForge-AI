"""
AI Marketing Content Engine — Schema Tests

Unit tests for Campaign Pydantic schemas validation.
"""

import uuid
from datetime import datetime, timezone
import pytest
from pydantic import ValidationError

from app.models.campaign import CampaignStatus
from app.schemas.campaign import CampaignCreate, CampaignResponse, CampaignUpdate


def test_campaign_create_valid():
    """Test creating a valid CampaignCreate object."""
    data = {
        "name": "Construction AI Leads",
        "objective": "Generate MQLs",
        "industry": "Construction",
        "product_service": "Physical AI Solutions",
        "target_audience": "Construction Companies",
        "target_personas": ["CEO", "COO", "Head of Construction"],
        "pain_points": [
            "Construction delays",
            "Safety issues",
            "Manual inspections",
            "Labor shortage",
        ],
        "offer": "Free AI Construction Assessment",
        "landing_page": "https://example.com/assessment",
        "brand_info": "Leading provider of physical AI solutions",
        "tone": "Professional",
    }
    campaign = CampaignCreate(**data)
    assert campaign.name == "Construction AI Leads"
    assert len(campaign.target_personas) == 3
    assert len(campaign.pain_points) == 4
    assert campaign.tone == "Professional"


def test_campaign_create_missing_required_fields():
    """Test CampaignCreate fails when required fields are missing."""
    with pytest.raises(ValidationError) as exc_info:
        CampaignCreate(
            name="Incomplete Campaign",
            # missing objective, industry, product_service, target_audience
        )
    errors = exc_info.value.errors()
    missing_fields = {e["loc"][0] for e in errors}
    assert "objective" in missing_fields
    assert "industry" in missing_fields
    assert "product_service" in missing_fields
    assert "target_audience" in missing_fields


def test_campaign_update_optional_fields():
    """Test CampaignUpdate accepts partial updates."""
    update = CampaignUpdate(
        name="Updated Campaign Name",
        status=CampaignStatus.STRATEGY_GENERATED,
    )
    assert update.name == "Updated Campaign Name"
    assert update.status == CampaignStatus.STRATEGY_GENERATED
    assert update.objective is None


def test_campaign_response_serialization():
    """Test CampaignResponse model serialization."""
    now = datetime.now(timezone.utc)
    campaign_id = uuid.uuid4()
    data = {
        "id": campaign_id,
        "name": "Test Campaign",
        "objective": "Test Objective",
        "industry": "Tech",
        "product_service": "Software",
        "target_audience": "Developers",
        "target_personas": ["CTO"],
        "pain_points": ["Legacy code"],
        "offer": "Free Trial",
        "landing_page": "https://test.com",
        "brand_info": "Test Brand",
        "tone": "Casual",
        "status": CampaignStatus.DRAFT,
        "created_at": now,
        "updated_at": now,
    }
    response = CampaignResponse(**data)
    assert response.id == campaign_id
    assert response.status == CampaignStatus.DRAFT
    assert response.created_at == now
