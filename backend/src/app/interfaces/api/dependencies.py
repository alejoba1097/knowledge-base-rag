from __future__ import annotations

from typing import cast

from fastapi import Request

from app.application.upload_document import UploadDocumentUseCase
from app.application.chat import ChatUseCase
from app.domain import EmbeddingService, RagService, TextExtractorService, VectorStore


def get_vector_store(request: Request) -> VectorStore:
    vector_store = getattr(request.app.state, "vector_store", None)
    if vector_store is None:
        raise RuntimeError("Vector store has not been initialized.")
    return cast(VectorStore, vector_store)


def get_text_extractor(request: Request) -> TextExtractorService:
    extractor = getattr(request.app.state, "text_extractor", None)
    if extractor is None:
        raise RuntimeError("Text extractor has not been initialized.")
    return cast(TextExtractorService, extractor)


def get_embedding_service(request: Request) -> EmbeddingService:
    embedding_service = getattr(request.app.state, "embedding_service", None)
    if embedding_service is None:
        raise RuntimeError("Embedding service has not been initialized.")
    return cast(EmbeddingService, embedding_service)


def get_upload_use_case(request: Request) -> UploadDocumentUseCase:
    upload_use_case = getattr(request.app.state, "upload_use_case", None)
    if upload_use_case is None:
        raise RuntimeError("UploadDocumentUseCase has not been initialized.")
    return cast(UploadDocumentUseCase, upload_use_case)


def get_rag_service(request: Request) -> RagService:
    rag_service = getattr(request.app.state, "rag_service", None)
    if rag_service is None:
        raise RuntimeError("RagService has not been initialized.")
    return cast(RagService, rag_service)


def get_chat_use_case(request: Request) -> ChatUseCase:
    chat_use_case = getattr(request.app.state, "chat_use_case", None)
    if chat_use_case is None:
        raise RuntimeError("ChatUseCase has not been initialized.")
    return cast(ChatUseCase, chat_use_case)
