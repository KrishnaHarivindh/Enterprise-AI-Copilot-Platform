from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.agent import (
    MeetingNotesRequest,
    MeetingNotesResponse,
    ReportRequest,
    ReportResponse,
    SummarizeRequest,
    SummaryResponse,
)
from app.services.agent_service import create_meeting_notes, generate_report, summarize_document

router = APIRouter(prefix="/agents")


@router.post("/summarize", response_model=SummaryResponse)
def summarize(
    payload: SummarizeRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return summarize_document(db, current_user, payload.document_id)


@router.post("/report", response_model=ReportResponse)
def report(
    payload: ReportRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return generate_report(db, current_user, payload.query)


@router.post("/meeting-notes", response_model=MeetingNotesResponse)
def meeting_notes(payload: MeetingNotesRequest):
    return create_meeting_notes(payload.transcript)
