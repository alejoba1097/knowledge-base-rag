from __future__ import annotations

from typing import Iterable, Protocol, Sequence

from app.domain.entities import DocumentChunk, QueryResult


class VectorStore(Protocol):
    """Abstract interface for vector storage/backends."""

    def add_documents(self, chunks: Iterable[DocumentChunk], embeddings: Sequence[Sequence[float]]) -> None:
        ...

    def query(self, text: str, limit: int = 5) -> list[QueryResult]:
        ...
