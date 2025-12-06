from fastapi import APIRouter

from .routes import router as api_router

__all__ = ["get_api_router"]


def get_api_router() -> APIRouter:
    router = APIRouter()
    router.include_router(api_router)
    return router
