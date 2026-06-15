from uuid import UUID

from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    document_id: UUID


class SummaryResponse(BaseModel):
    summary: str
    sources: list[str]


class ReportRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500)


class ReportResponse(BaseModel):
    executive_summary: str
    key_findings: list[str]
    recommendations: list[str]
    risks: list[str]
    sources: list[str]


class MeetingNotesRequest(BaseModel):
    transcript: str = Field(min_length=10, max_length=20000)


class MeetingNotesResponse(BaseModel):
    summary: str
    action_items: list[str]
    decisions: list[str]
    follow_ups: list[str]
