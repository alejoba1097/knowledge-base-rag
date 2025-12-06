from fastapi import FastAPI

from app.api import get_api_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    api_router = get_api_router()
    app.include_router(api_router, prefix=settings.api_prefix)

    return app


app = create_app()
