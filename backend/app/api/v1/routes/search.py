from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.search import ChatRequest, ChatResponse, SearchRequest, SearchResult
from app.services.search_service import generate_grounded_answer, semantic_search
from app.models.usage_metric import UsageMetricType
from app.services.metrics_service import record_usage

router = APIRouter()


@router.post("/search", response_model=list[SearchResult])
def search_documents(
    payload: SearchRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    record_usage(db, UsageMetricType.SEARCH)
    return semantic_search(db, current_user, payload.query)


@router.post("/chat", response_model=ChatResponse)
def rag_chat(
    payload: ChatRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    results = semantic_search(db, current_user, payload.question)
    record_usage(db, UsageMetricType.CHAT)
    return generate_grounded_answer(payload.question, results)
