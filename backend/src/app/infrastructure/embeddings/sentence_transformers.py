from __future__ import annotations

from typing import Sequence

from sentence_transformers import SentenceTransformer

from app.domain.services import EmbeddingService


class SentenceTransformerEmbeddingService(EmbeddingService):
    """Embedding service using a SentenceTransformers model."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        embeddings = self.model.encode(list(texts), convert_to_numpy=False, show_progress_bar=False)
        return [list(map(float, emb)) for emb in embeddings]
