import logging

from app.application.chat import ChatUseCase
from app.interfaces.api.schemas import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)


async def handle_chat(payload: ChatRequest, chat_use_case: ChatUseCase) -> ChatResponse:
    logger.info("Chat request received for document_id=%s", payload.document_id)
    result = chat_use_case.chat(question=payload.question, document_id=payload.document_id)
    return ChatResponse(answer=result.answer, source=result.source)
