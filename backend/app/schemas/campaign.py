"""
AI Marketing Content Engine — Campaign Schemas

Pydantic v2 validation models for Campaign creation, update, and API responses.
"""

import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.models.campaign import CampaignStatus


class CampaignBase(BaseModel):
    """Base schema for campaign properties."""

    name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Name of the marketing campaign",
        examples=["Construction AI Leads"],
    )
    objective: str = Field(
        ...,
        min_length=2,
        description="Primary goal of the campaign",
        examples=["Generate MQLs"],
    )
    industry: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Target industry",
        examples=["Construction"],
    )
    product_service: str = Field(
        ...,
        min_length=2,
        description="Product or service being promoted",
        examples=["Physical AI Solutions"],
    )
    target_audience: str = Field(
        ...,
        min_length=2,
        description="Broader target audience description",
        examples=["Construction Companies"],
    )
    target_personas: List[str] = Field(
        default_factory=list,
        description="Specific decision maker personas",
        examples=[["CEO", "COO", "Head of Construction"]],
    )
    pain_points: List[str] = Field(
        default_factory=list,
        description="Key customer pain points",
        examples=[[
            "Construction delays",
            "Safety issues",
            "Manual inspections",
            "Labor shortage",
        ]],
    )
    offer: Optional[str] = Field(
        None,
        description="Promotional offer or lead magnet",
        examples=["Free AI Construction Assessment"],
    )
    landing_page: Optional[str] = Field(
        None,
        max_length=2048,
        description="Campaign landing page URL",
        examples=["https://example.com/ai-assessment"],
    )
    brand_info: Optional[str] = Field(
        None,
        description="Brand identity, guidelines, or background context",
        examples=["Leading provider of autonomous robotics for jobsites."],
    )
    tone: str = Field(
        default="Professional",
        description="Desired communication tone",
        examples=["Professional"],
    )


class CampaignCreate(CampaignBase):
    """Schema for creating a new campaign."""
    pass


class CampaignUpdate(BaseModel):
    """Schema for updating an existing campaign (all fields optional)."""

    name: Optional[str] = Field(None, min_length=2, max_length=255)
    objective: Optional[str] = Field(None, min_length=2)
    industry: Optional[str] = Field(None, min_length=2, max_length=255)
    product_service: Optional[str] = Field(None, min_length=2)
    target_audience: Optional[str] = Field(None, min_length=2)
    target_personas: Optional[List[str]] = None
    pain_points: Optional[List[str]] = None
    offer: Optional[str] = None
    landing_page: Optional[str] = None
    brand_info: Optional[str] = None
    tone: Optional[str] = None
    status: Optional[CampaignStatus] = None


class CampaignResponse(CampaignBase):
    """Schema for campaign API responses."""

    id: uuid.UUID
    status: CampaignStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
