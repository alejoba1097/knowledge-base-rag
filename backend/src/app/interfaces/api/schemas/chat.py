from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    document_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    source: str | None = None
