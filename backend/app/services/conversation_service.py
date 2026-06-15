from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.conversation import Conversation, Message
from app.models.user import User
from app.services.search_service import generate_grounded_answer, semantic_search
from app.models.usage_metric import UsageMetricType
from app.services.metrics_service import record_usage


def create_conversation(db: Session, user: User, title: str) -> Conversation:
    conversation = Conversation(user_id=user.id, title=title.strip())
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def list_conversations(db: Session, user: User) -> list[Conversation]:
    return list(
        db.scalars(
            select(Conversation)
            .where(Conversation.user_id == user.id)
            .order_by(Conversation.updated_at.desc())
        )
    )


def get_conversation(db: Session, user: User, conversation_id: UUID) -> Conversation:
    conversation = db.get(Conversation, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")
    if conversation.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conversation access denied.")
    return conversation


def delete_conversation(db: Session, user: User, conversation_id: UUID) -> None:
    conversation = get_conversation(db, user, conversation_id)
    db.delete(conversation)
    db.commit()


def add_chat_message(db: Session, user: User, conversation_id: UUID, question: str) -> Message:
    conversation = get_conversation(db, user, conversation_id)
    results = semantic_search(db, user, question)
    response = generate_grounded_answer(question, results)
    record_usage(db, UsageMetricType.CHAT)

    message = Message(
        conversation_id=conversation.id,
        question=question,
        answer=response["answer"],
        sources=response["sources"],
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
