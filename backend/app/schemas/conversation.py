from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ConversationCreate(BaseModel):
    title: str = Field(default="New conversation", min_length=1, max_length=180)


class ChatMessageCreate(BaseModel):
    question: str = Field(min_length=2, max_length=1000)


class MessageRead(BaseModel):
    id: UUID
    question: str
    answer: str
    sources: list
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationRead(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationDetail(ConversationRead):
    messages: list[MessageRead]
