from fastapi import APIRouter, Depends, File, UploadFile

from app.application.upload_document import UploadDocumentUseCase
from app.application.chat import ChatUseCase
from app.interfaces.api.controllers import handle_chat, handle_upload
from app.interfaces.api.dependencies import get_chat_use_case, get_upload_use_case
from app.interfaces.api.schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    upload_use_case: UploadDocumentUseCase = Depends(get_upload_use_case),
) -> dict[str, str]:
    return await handle_upload(file, upload_use_case)


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    chat_use_case: ChatUseCase = Depends(get_chat_use_case),
) -> ChatResponse:
    return await handle_chat(payload, chat_use_case)
