"""Interface adapters (HTTP APIs, CLI, etc.)."""

from app.interfaces.api import get_api_router

__all__ = ["get_api_router"]
