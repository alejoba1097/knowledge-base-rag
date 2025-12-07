from app.core.config import Settings
from app.interfaces.api.schemas import ChatRequest, ChatResponse


async def handle_chat(payload: ChatRequest, settings: Settings) -> ChatResponse:
    _ = settings
    return ChatResponse(
        answer="Placeholder answer. Connect to retrieval and generation to respond.",
        source=payload.document_id,
    )
