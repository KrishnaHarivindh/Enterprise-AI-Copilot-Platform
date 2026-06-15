from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500)


class SearchResult(BaseModel):
    document: str
    document_id: str
    chunk_text: str
    score: float


class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1000)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    citations: list[SearchResult] = []
