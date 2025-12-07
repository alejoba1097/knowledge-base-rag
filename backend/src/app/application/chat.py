from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from app.domain import DocumentChunk, RagService, VectorStore


@dataclass
class ChatResult:
    answer: str
    source: str | None
    context: list[DocumentChunk]


class ChatUseCase:
    """Use case: retrieve relevant chunks and generate an answer with RAG."""

    def __init__(self, *, vector_store: VectorStore, rag_service: RagService, top_k: int = 5) -> None:
        self.vector_store = vector_store
        self.rag_service = rag_service
        self.top_k = top_k

    def chat(
        self,
        *,
        question: str,
        document_id: str | None = None,
        chat_history: Sequence[tuple[str, str]] | None = None,
    ) -> ChatResult:
        results = self.vector_store.query(question, limit=self.top_k)

        def _matches_document(chunk: DocumentChunk) -> bool:
            if document_id is None:
                return True
            if chunk.metadata is None:
                return False
            return chunk.metadata.get("filename") == document_id or chunk.metadata.get("document_id") == document_id

        context_chunks = [result.chunk for result in results if _matches_document(result.chunk)]
        if not context_chunks:
            # Fall back to whatever we have to avoid empty context when filtering removes everything.
            context_chunks = [result.chunk for result in results]

        answer = self.rag_service.generate_answer(
            question=question,
            context=context_chunks,
            chat_history=chat_history,
        )
        source = None
        if context_chunks and context_chunks[0].metadata:
            source = context_chunks[0].metadata.get("filename") or context_chunks[0].metadata.get("document_id")

        return ChatResult(answer=answer, source=source, context=context_chunks)
