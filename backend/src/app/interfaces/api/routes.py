from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.core.config import Settings, settings_dependency
from app.infrastructure import ChromaVectorStore, SentenceTransformerEmbeddingService, TesseractTextExtractor
from app.application.upload_document import UploadDocumentUseCase
from app.domain import VectorStore, EmbeddingService, TextExtractorService

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    document_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    source: str | None = None


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    settings: Settings = Depends(settings_dependency),
) -> dict[str, str]:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported.")

    vector_store: VectorStore = ChromaVectorStore(
        persist_dir=settings.chroma_dir,
        collection_name="documents",
        embedding_model=settings.embedding_model,
    )
    extractor: TextExtractorService = TesseractTextExtractor()
    embedder: EmbeddingService = SentenceTransformerEmbeddingService(settings.embedding_model)

    use_case = UploadDocumentUseCase(
        extractor=extractor,
        vector_store=vector_store,
        chunk_size=800,
        overlap=100,
    )
    data = await file.read()
    text = extractor.extract_text(data)
    chunks = list(use_case.chunk_text(text))
    embeddings = embedder.embed(chunks)
    doc_id = use_case.execute(
        filename=file.filename,
        data=data,
        embeddings=embeddings,
        precomputed_chunks=chunks,
        precomputed_text=text,
    )

    return {"document_id": doc_id, "status": "indexed", "filename": file.filename}


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    settings: Settings = Depends(settings_dependency),
) -> ChatResponse:
    _ = settings
    return ChatResponse(
        answer="Placeholder answer. Connect to embeddings + Chroma + generator.",
        source=payload.document_id,
    )
