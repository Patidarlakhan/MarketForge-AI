"""
AI Marketing Content Engine — API v1 Router Registration

Aggregates all version 1 endpoints under /api/v1.
"""

from fastapi import APIRouter

from app.api.v1.campaigns import router as campaigns_router
from app.api.v1.master_content import router as master_content_router
from app.api.v1.platform_content import router as platform_content_router
from app.api.v1.strategies import router as strategies_router

api_v1_router = APIRouter(prefix="/api/v1")

# Mount sub-routers
api_v1_router.include_router(campaigns_router)
api_v1_router.include_router(strategies_router)
api_v1_router.include_router(master_content_router)
api_v1_router.include_router(platform_content_router)
