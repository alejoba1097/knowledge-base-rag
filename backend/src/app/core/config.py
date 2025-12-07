from fastapi import Request
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="KB_", extra="ignore")

    app_name: str = "Knowledge Base RAG Backend"
    api_prefix: str = "/api"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

    # Storage / vector config
    data_dir: str = "./data"
    chroma_host: str = "chroma"
    chroma_port: int = 8000
    chroma_collection_name: str = "documents"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    rag_model_name: str = "google/flan-t5-small"
    rag_top_k: int = 5
    rag_max_new_tokens: int = 256
    rag_temperature: float = 0.0

    # API / CORS
    cors_origins: list[str] = ["*"]


def get_settings() -> Settings:
    return Settings()


def settings_dependency(request: Request) -> Settings:
    existing = getattr(request.app.state, "settings", None)
    if isinstance(existing, Settings):
        return existing
    return get_settings()
