from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol


@dataclass
class DocumentChunk:
    id: str
    content: str
    metadata: dict[str, str] | None = None


@dataclass
class QueryResult:
    chunk: DocumentChunk
    score: float


class VectorStore(Protocol):
    """Abstract interface for vector storage/backends."""

    def add_documents(self, chunks: Iterable[DocumentChunk]) -> None:
        ...

    def query(self, text: str, limit: int = 5) -> list[QueryResult]:
        ...
