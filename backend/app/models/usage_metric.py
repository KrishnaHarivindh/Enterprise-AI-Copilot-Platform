from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from sqlalchemy import DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class UsageMetricType(StrEnum):
    SEARCH = "SEARCH"
    CHAT = "CHAT"


class UsageMetric(Base):
    __tablename__ = "usage_metrics"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    metric_type: Mapped[UsageMetricType] = mapped_column(Enum(UsageMetricType), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
