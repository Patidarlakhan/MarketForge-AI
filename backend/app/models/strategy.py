"""
AI Marketing Content Engine — Strategy Model

SQLAlchemy ORM model for marketing_strategies entity.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.campaign import GUID, JSONType


class MarketingStrategy(Base):
    """Marketing Strategy ORM entity (1:1 with Campaign)."""

    __tablename__ = "marketing_strategies"

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
        unique=True,
        index=True,
    )

    # JSON content storing StrategyOutput structure
    content: Mapped[Dict[str, Any]] = mapped_column(
        JSONType,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="completed",
        server_default="completed",
        index=True,
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
    campaign = relationship("Campaign", back_populates="strategy")

    def __repr__(self) -> str:
        return f"<MarketingStrategy(id={self.id}, campaign_id={self.campaign_id}, status='{self.status}')>"
