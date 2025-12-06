from __future__ import annotations

from typing import Protocol

from app.domain.entities import StoredDocument


class DocumentStore(Protocol):
    """Abstraction for persisting uploaded documents."""

    def save(self, filename: str, data: bytes) -> StoredDocument:
        ...

    def get_path(self, document_id: str) -> str:
        ...
