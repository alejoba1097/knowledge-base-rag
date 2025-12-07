from __future__ import annotations

import logging
from typing import Iterable

from app.domain import DocumentChunk, EmbeddingService, TextExtractorService, VectorStore

logger = logging.getLogger(__name__)


class UploadDocumentUseCase:
    """Use case: extract text from an uploaded document, chunk it, and store embeddings."""

    def __init__(
        self,
        *,
        text_extractor: TextExtractorService,
        embedder: EmbeddingService,
        vector_store: VectorStore,
        chunk_size: int = 800,
        overlap: int = 100,
    ) -> None:
        self.text_extractor = text_extractor
        self.embedder = embedder
        self.vector_store = vector_store
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> Iterable[str]:
        if not text:
            return []
        chunks: list[str] = []
        length = len(text)
        start = 0
        # Ensure forward progress even if overlap is accidentally large
        step = max(self.chunk_size - self.overlap, 1)

        while start < length:
            end = min(start + self.chunk_size, length)
            chunks.append(text[start:end].strip())
            if end == length:
                break
            start += step
        return [c for c in chunks if c]

    def embed_and_store(
        self,
        *,
        filename: str,
        data: bytes,
    ) -> str:
        logger.info("Starting upload pipeline for filename=%s", filename)

        text = self.text_extractor.extract_text(data)
        if not text:
            logger.warning("No text extracted for filename=%s; skipping.", filename)
            return filename

        chunks = list(self.chunk_text(text))
        if not chunks:
            logger.warning("No chunks generated for filename=%s; skipping.", filename)
            return filename

        logger.info("Generated %d chunks for filename=%s", len(chunks), filename)

        embeddings = self.embedder.embed(chunks)
        logger.info("Computed embeddings for %d chunks for filename=%s", len(embeddings), filename)

        doc_id = filename
        chunk_models: list[DocumentChunk] = []
        if len(embeddings) < len(chunks):
            logger.error(
                "Embedding count %d is less than chunk count %d for filename=%s; aborting store.",
                len(embeddings),
                len(chunks),
                filename,
            )
            return doc_id

        for idx, chunk in enumerate(chunks):
            chunk_models.append(
                DocumentChunk(
                    id=f"{doc_id}::chunk-{idx}",
                    content=chunk,
                    metadata={"filename": filename, "chunk": str(idx)},
                    embedding=list(embeddings[idx]),
                )
            )

        self.vector_store.add_documents(chunk_models)
        logger.info("Stored %d chunks for filename=%s", len(chunk_models), filename)
        return doc_id
