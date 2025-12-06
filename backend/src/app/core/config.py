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
    chroma_dir: str = "./data/chroma"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"


def get_settings() -> Settings:
    return Settings()


def settings_dependency() -> Settings:
    return get_settings()
