from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.audit_log import AuditAction


class AuditLogRead(BaseModel):
    id: UUID
    actor_id: UUID | None
    action: AuditAction
    entity_type: str
    entity_id: str | None
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
