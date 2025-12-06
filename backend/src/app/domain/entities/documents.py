from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StoredDocument:
    id: str
    filename: str
    path: str


@dataclass
class DocumentChunk:
    id: str
    content: str
    metadata: dict[str, str] | None = None


@dataclass
class QueryResult:
    chunk: DocumentChunk
    score: float
