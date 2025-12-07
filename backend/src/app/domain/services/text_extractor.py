from __future__ import annotations

from typing import Protocol


class TextExtractorService(Protocol):
    """Service that extracts raw text from a document payload."""

    def extract_text(self, data: bytes) -> str:
        ...
