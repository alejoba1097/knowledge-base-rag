from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import BaseModel

from app.core.config import Settings, settings_dependency

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    document_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    source: str | None = None


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    settings: Settings = Depends(settings_dependency),
) -> dict[str, str]:
    # Placeholder: integrate document store + chunking + vector index
    _ = settings
    return {"filename": file.filename, "status": "uploaded"}


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    settings: Settings = Depends(settings_dependency),
) -> ChatResponse:
    _ = settings
    return ChatResponse(
        answer="Placeholder answer. Connect to embeddings + Chroma + generator.",
        source=payload.document_id,
    )
