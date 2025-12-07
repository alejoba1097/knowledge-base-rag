from __future__ import annotations

from typing import Protocol, Sequence


class EmbeddingService(Protocol):
    """Service that turns text into vector embeddings."""

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        ...
