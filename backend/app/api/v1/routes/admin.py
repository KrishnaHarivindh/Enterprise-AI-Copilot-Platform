from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_role
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.admin import AdminMetrics
from app.services.metrics_service import get_admin_metrics

router = APIRouter(prefix="/admin")


@router.get("/metrics", response_model=AdminMetrics)
def metrics(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_role(UserRole.ADMIN))],
):
    return get_admin_metrics(db)
