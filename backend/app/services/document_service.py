from pathlib import Path
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.audit_log import AuditAction
from app.models.document import Document, DocumentStatus
from app.models.user import User, UserRole
from app.services.audit_service import record_audit_log
from app.services.document_parser import extract_text
from app.services.search_service import index_document_chunks


def get_storage_root() -> Path:
    return Path(settings.document_storage_dir)


def get_extension(filename: str) -> str:
    return Path(filename).suffix.lower().lstrip(".")


def validate_upload_file(file: UploadFile, size_bytes: int) -> str:
    extension = get_extension(file.filename or "")
    if extension not in settings.allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed: {', '.join(sorted(settings.allowed_extensions))}",
        )

    if size_bytes <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty.")

    if size_bytes > settings.max_upload_size_bytes:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File is too large.")

    return extension


def get_latest_document_version(db: Session, owner: User, original_filename: str) -> Document | None:
    return db.scalar(
        select(Document).where(
            Document.owner_id == owner.id,
            Document.original_filename == original_filename,
        ).order_by(Document.version_number.desc())
    )


def create_document_from_upload(db: Session, owner: User, file: UploadFile, contents: bytes) -> Document:
    original_filename = Path(file.filename or "document").name
    size_bytes = len(contents)
    extension = validate_upload_file(file, size_bytes)
    latest_version = get_latest_document_version(db, owner, original_filename)

    storage_dir = get_storage_root() / extension
    storage_dir.mkdir(parents=True, exist_ok=True)

    stored_filename = f"{uuid4()}.{extension}"
    file_path = storage_dir / stored_filename
    file_path.write_bytes(contents)

    document = Document(
        filename=stored_filename,
        original_filename=original_filename,
        file_path=str(file_path),
        file_type=extension,
        mime_type=file.content_type or "application/octet-stream",
        size_bytes=size_bytes,
        owner_id=owner.id,
        parent_document_id=latest_version.id if latest_version else None,
        version_number=(latest_version.version_number + 1) if latest_version else 1,
        status=DocumentStatus.UPLOADED,
    )

    try:
        parsed_text = extract_text(file_path, extension)
        document.extracted_text = parsed_text
        document.chunk_count = estimate_chunk_count(parsed_text)
        document.status = DocumentStatus.PROCESSED
    except Exception:
        document.status = DocumentStatus.FAILED
        document.extracted_text = None
        document.chunk_count = 0

    db.add(document)
    db.commit()
    db.refresh(document)
    if document.status == DocumentStatus.PROCESSED:
        index_document_chunks(db, document)

    record_audit_log(
        db,
        action=AuditAction.DOCUMENT_UPLOAD,
        entity_type="document",
        entity_id=str(document.id),
        actor=owner,
        description=f"{owner.full_name} uploaded {original_filename}",
    )
    return document


def estimate_chunk_count(text: str | None, chunk_size: int = 1200) -> int:
    if not text:
        return 0
    return max(1, (len(text) + chunk_size - 1) // chunk_size)


def list_accessible_documents(db: Session, user: User, search: str | None = None) -> list[Document]:
    query = select(Document)
    if user.role != UserRole.ADMIN:
        query = query.where(Document.owner_id == user.id)

    if search:
        pattern = f"%{search}%"
        query = query.where(
            or_(
                Document.original_filename.ilike(pattern),
                Document.extracted_text.ilike(pattern),
            )
        )

    return list(db.scalars(query.order_by(Document.created_at.desc())))


def get_accessible_document(db: Session, document_id: UUID, user: User) -> Document:
    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    if user.role != UserRole.ADMIN and document.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Document access denied.")

    return document


def delete_document(db: Session, document: Document, actor: User) -> None:
    path = Path(document.file_path)
    if path.exists():
        path.unlink()

    original_filename = document.original_filename
    document_id = str(document.id)
    db.delete(document)
    db.commit()

    record_audit_log(
        db,
        action=AuditAction.DOCUMENT_DELETE,
        entity_type="document",
        entity_id=document_id,
        actor=actor,
        description=f"{actor.full_name} deleted {original_filename}",
    )
