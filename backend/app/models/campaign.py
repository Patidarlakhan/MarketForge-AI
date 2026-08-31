"""
AI Marketing Content Engine — Campaign Model

SQLAlchemy ORM model for marketing_campaigns entity with Postgres/SQLite compatibility.
"""

import enum
import uuid
from datetime import datetime, timezone
from typing import Any, List, Optional

from sqlalchemy import DateTime, Enum, JSON, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import CHAR, TypeDecorator


from app.database import Base


class CampaignStatus(str, enum.Enum):
    """Execution status of a marketing campaign workflow."""
    DRAFT = "draft"
    STRATEGY_GENERATION = "strategy_generation"
    STRATEGY_GENERATED = "strategy_generated"
    MASTER_CONTENT_GENERATION = "master_content_generation"
    MASTER_CONTENT_GENERATED = "master_content_generated"
    PLATFORM_CONTENT_GENERATION = "platform_content_generation"
    COMPLETED = "completed"
    FAILED = "failed"


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.
    Uses PostgreSQL's native UUID type, otherwise uses CHAR(36).
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == "postgresql":
            return value if isinstance(value, uuid.UUID) else uuid.UUID(str(value))
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(str(value))


# Type variants for SQLite test compatibility vs PostgreSQL production
JSONType = JSONB().with_variant(JSON(), "sqlite")


class Campaign(Base):
    """Marketing Campaign ORM entity."""

    __tablename__ = "marketing_campaigns"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    objective: Mapped[str] = mapped_column(Text, nullable=False)
    industry: Mapped[str] = mapped_column(String(255), nullable=False)
    product_service: Mapped[str] = mapped_column(Text, nullable=False)
    target_audience: Mapped[str] = mapped_column(Text, nullable=False)
    
    # JSONB columns for flexible list structures with SQLite JSON variant
    target_personas: Mapped[List[str]] = mapped_column(
        JSONType, nullable=False, default=list
    )
    pain_points: Mapped[List[str]] = mapped_column(
        JSONType, nullable=False, default=list
    )
    
    offer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    landing_page: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    brand_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tone: Mapped[str] = mapped_column(String(255), nullable=False, default="Professional")

    status: Mapped[CampaignStatus] = mapped_column(
        Enum(CampaignStatus, name="campaign_status_enum", create_type=True, native_enum=False),
        nullable=False,
        default=CampaignStatus.DRAFT,
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
    master_content = relationship("MasterContent", back_populates="campaign", uselist=False, passive_deletes=True)
    platform_contents = relationship("PlatformContent", back_populates="campaign", cascade="all, delete-orphan", passive_deletes=True)
    strategy = relationship("MarketingStrategy", back_populates="campaign", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    def __repr__(self) -> str:
        return f"<Campaign(id={self.id}, name='{self.name}', status='{self.status}')>"
