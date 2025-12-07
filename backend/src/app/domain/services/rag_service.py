from __future__ import annotations

from typing import Protocol, Sequence

from app.domain.entities import DocumentChunk


class RagService(Protocol):
    """Interface for generating answers from context plus a user question."""

    def generate_answer(
        self,
        *,
        question: str,
        context: Sequence[DocumentChunk],
        chat_history: Sequence[tuple[str, str]] | None = None,
    ) -> str:
        ...
