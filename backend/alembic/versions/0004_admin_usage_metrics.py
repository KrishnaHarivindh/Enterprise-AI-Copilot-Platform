"""admin usage metrics

Revision ID: 0004_metrics
Revises: 0003_chat
Create Date: 2026-06-13
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0004_metrics"
down_revision: Union[str, None] = "0003_chat"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    metric_type = postgresql.ENUM("SEARCH", "CHAT", name="usagemetrictype")
    metric_type.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "usage_metrics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("metric_type", metric_type, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_usage_metrics_metric_type", "usage_metrics", ["metric_type"])


def downgrade() -> None:
    op.drop_index("ix_usage_metrics_metric_type", table_name="usage_metrics")
    op.drop_table("usage_metrics")
    postgresql.ENUM(name="usagemetrictype").drop(op.get_bind(), checkfirst=True)
