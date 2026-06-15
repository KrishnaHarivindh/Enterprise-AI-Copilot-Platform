from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.usage_metric import UsageMetric, UsageMetricType
from app.models.user import User


def record_usage(db: Session, metric_type: UsageMetricType) -> None:
    db.add(UsageMetric(metric_type=metric_type))
    db.commit()


def get_admin_metrics(db: Session) -> dict[str, int]:
    return {
        "users": count(db, User),
        "documents": count(db, Document),
        "chunks": count(db, DocumentChunk),
        "searches": count_metric(db, UsageMetricType.SEARCH),
        "conversations": count(db, Conversation),
    }


def count(db: Session, model) -> int:
    return int(db.scalar(select(func.count()).select_from(model)) or 0)


def count_metric(db: Session, metric_type: UsageMetricType) -> int:
    return int(db.scalar(select(func.count()).select_from(UsageMetric).where(UsageMetric.metric_type == metric_type)) or 0)
