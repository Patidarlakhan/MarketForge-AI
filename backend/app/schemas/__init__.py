"""
AI Marketing Content Engine — Schemas Package

Export all Pydantic v2 validation models.
"""

from app.schemas.campaign import (
    CampaignBase,
    CampaignCreate,
    CampaignResponse,
    CampaignUpdate,
)
from app.schemas.blog import BlogOutput
from app.schemas.instagram import InstagramOutput, ReelScene
from app.schemas.linkedin import CarouselSlide, LinkedInOutput
from app.schemas.master_content import MasterContentOutput, MasterContentResponse
from app.schemas.platform_content import PlatformContentResponse, PlatformContentUpdate
from app.schemas.strategy import CallToAction, StrategyOutput, StrategyResponse
from app.schemas.twitter import TweetItem, TwitterOutput

__all__ = [
    "CampaignBase",
    "CampaignCreate",
    "CampaignUpdate",
    "CampaignResponse",
    "CallToAction",
    "StrategyOutput",
    "StrategyResponse",
    "MasterContentOutput",
    "MasterContentResponse",
    "CarouselSlide",
    "LinkedInOutput",
    "TweetItem",
    "TwitterOutput",
    "ReelScene",
    "InstagramOutput",
    "BlogOutput",
    "PlatformContentResponse",
    "PlatformContentUpdate",
]
