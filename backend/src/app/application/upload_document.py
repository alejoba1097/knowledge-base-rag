from __future__ import annotations

from typing import Iterable, Sequence

from app.domain import DocumentChunk, TextExtractorService, VectorStore


class UploadDocumentUseCase:
    """Use case: extract text from an uploaded document, chunk it, and store embeddings."""

    def __init__(
        self,
        *,
        extractor: TextExtractorService,
        vector_store: VectorStore,
        chunk_size: int = 800,
        overlap: int = 100,
    ) -> None:
        self.extractor = extractor
        self.vector_store = vector_store
        self.chunk_size = chunk_size
        self.overlap = overlap

    def _chunk_text(self, text: str) -> Iterable[str]:
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

    def execute(self, *, filename: str, data: bytes, embeddings: Sequence[Sequence[float]]) -> str:
        text = self.extractor.extract_text(data)
        chunks = self._chunk_text(text)

        doc_id = filename
        chunk_models: list[DocumentChunk] = []
        for idx, chunk in enumerate(chunks):
            chunk_models.append(
                DocumentChunk(
                    id=f"{doc_id}::chunk-{idx}",
                    content=chunk,
                    metadata={"filename": filename, "chunk": str(idx)},
                )
            )

        self.vector_store.add_documents(chunk_models, embeddings)
        return doc_id
