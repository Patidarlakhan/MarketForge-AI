"""
AI Marketing Content Engine — Platform Content Schemas

Pydantic v2 validation models for Platform Content responses and updates.
"""

import uuid
from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel, ConfigDict, Field


class PlatformContentUpdate(BaseModel):
    """Payload model for editing platform content JSON data."""

    content: Dict[str, Any] = Field(..., description="Updated platform content JSON structure")


class PlatformContentResponse(BaseModel):
    """API Response model for a platform content entity (LinkedIn, Twitter, Instagram, Blog)."""

    id: uuid.UUID
    campaign_id: uuid.UUID
    platform: str
    content: Dict[str, Any]
    status: str
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
