from sqlalchemy.orm import Session

from app.models.audit_log import AuditAction, AuditLog
from app.models.user import User


def record_audit_log(
    db: Session,
    action: AuditAction,
    entity_type: str,
    description: str,
    actor: User | None = None,
    entity_id: str | None = None,
) -> AuditLog:
    audit_log = AuditLog(
        actor_id=actor.id if actor else None,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
    )
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    return audit_log
