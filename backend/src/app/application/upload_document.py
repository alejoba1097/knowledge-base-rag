from __future__ import annotations

from typing import Iterable

from app.domain import DocumentChunk, EmbeddingService, TextExtractorService, VectorStore


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
        start = 0
        length = len(text)
        while start < length:
            end = min(start + self.chunk_size, length)
            chunks.append(text[start:end].strip())
            start = max(end - self.overlap, 0 if end == length else end - self.overlap)
            if start >= length:
                break
        return [c for c in chunks if c]

    def embed_and_store(
        self,
        *,
        filename: str,
        data: bytes,
    ) -> str:
        text = self.text_extractor.extract_text(data)
        if not text:
            return filename

        chunks = list(self.chunk_text(text))
        if not chunks:
            return filename

        embeddings = self.embedder.embed(chunks)
        doc_id = filename
        chunk_models: list[DocumentChunk] = []
        if len(embeddings) < len(chunks):
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
        return doc_id
