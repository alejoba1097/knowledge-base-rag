from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.upload_document import UploadDocumentUseCase
from app.core.config import get_settings
from app.infrastructure import ChromaVectorStore, SentenceTransformerEmbeddingService, TesseractTextExtractor
from app.interfaces.api import get_api_router


def configure_logging() -> None:
    """Ensure application logs are visible in the console."""
    level = logging.INFO
    root = logging.getLogger()
    if not root.handlers:
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        )
    root.setLevel(level)


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.settings = settings
        app.state.text_extractor = TesseractTextExtractor()
        app.state.embedding_service = SentenceTransformerEmbeddingService(settings.embedding_model)
        app.state.vector_store = ChromaVectorStore(
            host=settings.chroma_host,
            port=settings.chroma_port,
            collection_name=settings.chroma_collection_name,
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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_router = get_api_router()
    app.include_router(api_router, prefix=settings.api_prefix)

    return app


app = create_app()
