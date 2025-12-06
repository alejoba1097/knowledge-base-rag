from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class StoredDocument:
    id: str
    filename: str
    path: str


class DocumentStore(Protocol):
    """Abstraction for persisting uploaded documents."""

    def save(self, filename: str, data: bytes) -> StoredDocument:
        ...

    def get_path(self, document_id: str) -> str:
        ...
