from fastapi import APIRouter, Depends, File, UploadFile
from app.core.config import Settings, settings_dependency
from app.interfaces.api.schemas import ChatRequest, ChatResponse
from app.interfaces.api.controllers import handle_upload, handle_chat

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    settings: Settings = Depends(settings_dependency),
) -> dict[str, str]:
    return await handle_upload(file, settings)


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    settings: Settings = Depends(settings_dependency),
) -> ChatResponse:
    return await handle_chat(payload, settings)
