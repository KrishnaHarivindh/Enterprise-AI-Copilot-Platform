from pathlib import Path
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Query, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.audit_log import AuditAction
from app.models.user import User
from app.schemas.document import DocumentDetail, DocumentRead
from app.services.audit_service import record_audit_log
from app.services.document_service import (
    create_document_from_upload,
    delete_document,
    get_accessible_document,
    list_accessible_documents,
)

router = APIRouter(prefix="/documents")


@router.post("/upload", response_model=DocumentRead)
async def upload_document(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    file: UploadFile = File(...),
):
    contents = await file.read()
    return create_document_from_upload(db, current_user, file, contents)


@router.get("", response_model=list[DocumentRead])
def list_documents(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    search: str | None = Query(default=None, max_length=120),
):
    return list_accessible_documents(db, current_user, search=search)


@router.get("/{document_id}", response_model=DocumentDetail)
def get_document_details(
    document_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    document = get_accessible_document(db, document_id, current_user)
    preview = document.extracted_text[:1200] if document.extracted_text else None
    return DocumentDetail.model_validate(document).model_copy(update={"extracted_text_preview": preview})


@router.get("/{document_id}/download")
def download_document(
    document_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    document = get_accessible_document(db, document_id, current_user)
    record_audit_log(
        db,
        action=AuditAction.DOCUMENT_DOWNLOAD,
        entity_type="document",
        entity_id=str(document.id),
        actor=current_user,
        description=f"{current_user.full_name} downloaded {document.original_filename}",
    )
    return FileResponse(
        path=Path(document.file_path),
        media_type=document.mime_type,
        filename=document.original_filename,
    )


@router.delete("/{document_id}", status_code=204)
def remove_document(
    document_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    document = get_accessible_document(db, document_id, current_user)
    delete_document(db, document, current_user)
    return None
