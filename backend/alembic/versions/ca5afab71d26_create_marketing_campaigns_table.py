"""create_marketing_campaigns_table

Revision ID: ca5afab71d26
Revises: 
Create Date: 2026-08-27 16:51:45

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ca5afab71d26'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    is_postgres = bind.dialect.name == "postgresql"

    if is_postgres:
        uuid_type = postgresql.UUID(as_uuid=True)
        json_type = postgresql.JSONB(astext_type=sa.Text())
        status_type = sa.String(length=50)
    else:
        uuid_type = sa.String(length=36)
        json_type = sa.JSON()
        status_type = sa.String(length=50)

    op.create_table(
        'marketing_campaigns',
        sa.Column('id', uuid_type, primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('objective', sa.Text(), nullable=False),
        sa.Column('industry', sa.String(length=255), nullable=False),
        sa.Column('product_service', sa.Text(), nullable=False),
        sa.Column('target_audience', sa.Text(), nullable=False),
        sa.Column('target_personas', json_type, nullable=False, server_default='[]'),
        sa.Column('pain_points', json_type, nullable=False, server_default='[]'),
        sa.Column('offer', sa.Text(), nullable=True),
        sa.Column('landing_page', sa.String(length=2048), nullable=True),
        sa.Column('brand_info', sa.Text(), nullable=True),
        sa.Column('tone', sa.String(length=255), nullable=False, server_default='Professional'),
        sa.Column('status', status_type, nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP' if not is_postgres else 'now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP' if not is_postgres else 'now()')),
    )
    op.create_index('ix_marketing_campaigns_id', 'marketing_campaigns', ['id'], unique=False)
    op.create_index('ix_marketing_campaigns_name', 'marketing_campaigns', ['name'], unique=False)
    op.create_index('ix_marketing_campaigns_status', 'marketing_campaigns', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_marketing_campaigns_status', table_name='marketing_campaigns')
    op.drop_index('ix_marketing_campaigns_name', table_name='marketing_campaigns')
    op.drop_index('ix_marketing_campaigns_id', table_name='marketing_campaigns')
    op.drop_table('marketing_campaigns')
