"""create_platform_contents_table

Revision ID: e2763c9ac498
Revises: 9485a4ae3260
Create Date: 2026-08-27 17:27:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e2763c9ac498'
down_revision: Union[str, None] = '9485a4ae3260'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    is_postgres = bind.dialect.name == "postgresql"

    if is_postgres:
        uuid_type = postgresql.UUID(as_uuid=True)
        json_type = postgresql.JSONB(astext_type=sa.Text())
    else:
        uuid_type = sa.String(length=36)
        json_type = sa.JSON()

    op.create_table(
        'platform_contents',
        sa.Column('id', uuid_type, primary_key=True, nullable=False),
        sa.Column('campaign_id', uuid_type, sa.ForeignKey('marketing_campaigns.id', ondelete='CASCADE'), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=False),
        sa.Column('content', json_type, nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='completed'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP' if not is_postgres else 'now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP' if not is_postgres else 'now()')),
        sa.UniqueConstraint('campaign_id', 'platform', 'version', name='uq_campaign_platform_version'),
    )
    op.create_index('ix_platform_contents_id', 'platform_contents', ['id'], unique=False)
    op.create_index('ix_platform_contents_campaign_id', 'platform_contents', ['campaign_id'], unique=False)
    op.create_index('ix_platform_contents_platform', 'platform_contents', ['platform'], unique=False)
    op.create_index('ix_platform_contents_status', 'platform_contents', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_platform_contents_status', table_name='platform_contents')
    op.drop_index('ix_platform_contents_platform', table_name='platform_contents')
    op.drop_index('ix_platform_contents_campaign_id', table_name='platform_contents')
    op.drop_index('ix_platform_contents_id', table_name='platform_contents')
    op.drop_table('platform_contents')
