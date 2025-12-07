from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.application.upload_document import UploadDocumentUseCase
from app.core.config import get_settings
from app.infrastructure import ChromaVectorStore, SentenceTransformerEmbeddingService, TesseractTextExtractor
from app.interfaces.api import get_api_router


def create_app() -> FastAPI:
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.settings = settings
        app.state.text_extractor = TesseractTextExtractor()
        app.state.embedding_service = SentenceTransformerEmbeddingService(settings.embedding_model)
        app.state.vector_store = ChromaVectorStore(
            host=settings.chroma_host,
            port=settings.chroma_port,
            collection_name="documents",
            embedding_model=settings.embedding_model,
        )
        app.state.upload_use_case = UploadDocumentUseCase(
            text_extractor=app.state.text_extractor,
            embedder=app.state.embedding_service,
            vector_store=app.state.vector_store,
            chunk_size=800,
            overlap=100,
        )
        yield

    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    api_router = get_api_router()
    app.include_router(api_router, prefix=settings.api_prefix)

    return app


app = create_app()
