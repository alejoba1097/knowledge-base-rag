from fastapi import HTTPException, UploadFile

from app.application.upload_document import UploadDocumentUseCase
from app.core.config import Settings
from app.domain import EmbeddingService, TextExtractorService, VectorStore
from app.infrastructure import ChromaVectorStore, SentenceTransformerEmbeddingService, TesseractTextExtractor


def _get_vector_store(settings: Settings) -> VectorStore:
    return ChromaVectorStore(
        persist_dir=settings.chroma_dir,
        collection_name="documents",
        embedding_model=settings.embedding_model,
    )


def _get_extractor() -> TextExtractorService:
    return TesseractTextExtractor()


def _get_embedder(settings: Settings) -> EmbeddingService:
    return SentenceTransformerEmbeddingService(settings.embedding_model)


async def handle_upload(file: UploadFile, settings: Settings) -> dict[str, str]:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported.")

    vector_store = _get_vector_store(settings)
    extractor = _get_extractor()
    embedder = _get_embedder(settings)

    data = await file.read()
    use_case = UploadDocumentUseCase(
        extractor=extractor,
        vector_store=vector_store,
        chunk_size=800,
        overlap=100,
    )
    text = extractor.extract_text(data)
    chunks = list(use_case.chunk_text(text))
    embeddings = embedder.embed(chunks)
    doc_id = use_case.embed_and_store(
        filename=file.filename,
        data=data,
        embeddings=embeddings,
        precomputed_chunks=chunks,
        precomputed_text=text,
    )

    return {"document_id": doc_id, "status": "indexed", "filename": file.filename}
