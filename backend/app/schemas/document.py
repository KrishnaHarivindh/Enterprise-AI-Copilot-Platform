from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.document import DocumentStatus, EmbeddingStatus


class DocumentRead(BaseModel):
    id: UUID
    filename: str
    original_filename: str
    file_type: str
    mime_type: str
    size_bytes: int
    owner_id: UUID
    parent_document_id: UUID | None
    version_number: int
    status: DocumentStatus
    chunk_count: int
    embedding_status: EmbeddingStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentDetail(DocumentRead):
    extracted_text_preview: str | None = None


class DocumentListResponse(BaseModel):
    documents: list[DocumentRead]
