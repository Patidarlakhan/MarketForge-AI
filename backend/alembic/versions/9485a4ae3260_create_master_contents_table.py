"""create_master_contents_table

Revision ID: 9485a4ae3260
Revises: f2066d210515
Create Date: 2026-08-27 17:16:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9485a4ae3260'
down_revision: Union[str, None] = 'f2066d210515'
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
        'master_contents',
        sa.Column('id', uuid_type, primary_key=True, nullable=False),
        sa.Column('campaign_id', uuid_type, sa.ForeignKey('marketing_campaigns.id', ondelete='CASCADE'), nullable=False),
        sa.Column('content', json_type, nullable=False),
        sa.Column("status",sa.String(length=50),nullable=False,server_default="completed"),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP' if not is_postgres else 'now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP' if not is_postgres else 'now()')),
    )
    op.create_index('ix_master_contents_id', 'master_contents', ['id'], unique=False)
    op.create_index('ix_master_contents_campaign_id', 'master_contents', ['campaign_id'], unique=True)
    op.create_index('ix_master_contents_status', 'master_contents', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_master_contents_campaign_id', table_name='master_contents')
    op.drop_index('ix_master_contents_id', table_name='master_contents')
    op.drop_index('ix_master_contents_status', table_name='master_contents')
    op.drop_table('master_contents')
