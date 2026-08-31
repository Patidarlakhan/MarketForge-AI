"""
AI Marketing Content Engine — Platform Content Model

SQLAlchemy ORM model for platform_contents entity.
"""

import uuid
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.campaign import GUID, JSONType


class PlatformContent(Base):
    """Platform Content ORM entity storing generated platform assets (LinkedIn, Twitter, Instagram, Blog)."""

    __tablename__ = "platform_contents"
    __table_args__ = (
        UniqueConstraint("campaign_id", "platform", "version", name="uq_campaign_platform_version"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    campaign_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("marketing_campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    platform: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    # JSON content storing platform specific schema
    content: Mapped[Dict[str, Any]] = mapped_column(
        JSONType,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="completed",
        index=True,
    )
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationship to Campaign
    campaign = relationship("Campaign", back_populates="platform_contents")

    def __repr__(self) -> str:
        return (
            f"<PlatformContent(id={self.id}, campaign_id={self.campaign_id}, "
            f"platform='{self.platform}', version={self.version}, status='{self.status}')>"
        )
