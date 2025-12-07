from __future__ import annotations

from typing import Iterable, List, Optional

import chromadb
from chromadb.api.models.Collection import Collection
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from app.domain.entities import DocumentChunk, QueryResult
from app.domain.repositories import VectorStore


class ChromaVectorStore(VectorStore):
    """Chroma-backed implementation of the VectorStore protocol."""

    def __init__(
        self,
        *,
        host: str | None = None,
        port: int | None = None,
        persist_dir: str | None = None,
        collection_name: str = "documents",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        if host:
            self.client = chromadb.HttpClient(host=host, port=port or 8000)
        elif persist_dir:
            self.client = chromadb.PersistentClient(path=persist_dir)
        else:
            raise ValueError("ChromaVectorStore requires either host/port for server or persist_dir for local mode.")
        embedding_function = SentenceTransformerEmbeddingFunction(model_name=embedding_model)
        self.collection: Collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_function,
        )

    def add_documents(self, chunks: Iterable[DocumentChunk]) -> None:
        chunk_list = list(chunks)
        if not chunk_list:
            return

        embeddings: list[list[float]] = []
        ids = [chunk.id for chunk in chunk_list]
        documents = [chunk.content for chunk in chunk_list]
        metadatas = [chunk.metadata or {} for chunk in chunk_list]

        for chunk in chunk_list:
            if chunk.embedding is None:
                return
            embeddings.append(chunk.embedding)

        # Upsert to allow idempotent writes when the same chunk ids are provided.
        self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)

    def query(self, text: str, limit: int = 5) -> List[QueryResult]:
        results = self.collection.query(query_texts=[text], n_results=limit)

        ids: list[str] = results.get("ids", [[]])[0] or []
        docs: list[str] = results.get("documents", [[]])[0] or []
        metadatas: list[Optional[dict]] = results.get("metadatas", [[]])[0] or []
        distances: list[Optional[float]] = results.get("distances", [[]])[0] or []

        output: list[QueryResult] = []
        for idx, doc_text in enumerate(docs):
            chunk = DocumentChunk(
                id=ids[idx],
                content=doc_text,
                metadata=metadatas[idx] if idx < len(metadatas) else None,
            )
            score = distances[idx] if idx < len(distances) and distances[idx] is not None else 0.0
            output.append(QueryResult(chunk=chunk, score=score))
        return output
