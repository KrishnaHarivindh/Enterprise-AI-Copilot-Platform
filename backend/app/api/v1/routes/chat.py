from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.conversation import (
    ChatMessageCreate,
    ConversationCreate,
    ConversationDetail,
    ConversationRead,
    MessageRead,
)
from app.services.conversation_service import (
    add_chat_message,
    create_conversation,
    delete_conversation,
    get_conversation,
    list_conversations,
)

router = APIRouter(prefix="/chat/conversations")


@router.post("", response_model=ConversationRead)
def create_chat_conversation(
    payload: ConversationCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return create_conversation(db, current_user, payload.title)


@router.get("", response_model=list[ConversationRead])
def read_chat_conversations(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return list_conversations(db, current_user)


@router.get("/{conversation_id}", response_model=ConversationDetail)
def read_chat_conversation(
    conversation_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return get_conversation(db, current_user, conversation_id)


@router.post("/{conversation_id}/messages", response_model=MessageRead)
def create_chat_message(
    conversation_id: UUID,
    payload: ChatMessageCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return add_chat_message(db, current_user, conversation_id, payload.question)


@router.delete("/{conversation_id}", status_code=204)
def remove_chat_conversation(
    conversation_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    delete_conversation(db, current_user, conversation_id)
    return None
