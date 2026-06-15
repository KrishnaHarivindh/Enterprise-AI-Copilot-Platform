from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.audit_log import AuditLog
from app.models.user import User, UserRole
from app.schemas.audit_log import AuditLogRead

router = APIRouter(prefix="/audit-logs")


@router.get("", response_model=list[AuditLogRead])
def list_audit_logs(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    query = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(25)
    if current_user.role != UserRole.ADMIN:
        query = query.where(AuditLog.actor_id == current_user.id)
    return list(db.scalars(query))
