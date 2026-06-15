from pydantic import BaseModel


class AdminMetrics(BaseModel):
    users: int
    documents: int
    chunks: int
    searches: int
    conversations: int
