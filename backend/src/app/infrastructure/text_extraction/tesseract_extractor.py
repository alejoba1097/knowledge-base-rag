from __future__ import annotations

import tempfile
from pathlib import Path

import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes

from app.domain.services import TextExtractorService


class TesseractTextExtractor(TextExtractorService):
    """
    OCR-based text extractor using Tesseract.

    Notes:
    - Requires Tesseract OCR to be installed and available in PATH.
    - Uses pdf2image + PIL to render PDF pages for OCR. Best suited for small PDFs.
    """

    def __init__(self, *, dpi: int = 200, lang: str = "eng") -> None:
        self.dpi = dpi
        self.lang = lang

    def extract_text(self, data: bytes) -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            images = convert_from_bytes(data, dpi=self.dpi, output_folder=tmpdir, fmt="png")
            texts: list[str] = []
            for image in images:
                if isinstance(image, Image.Image):
                    text = pytesseract.image_to_string(image, lang=self.lang)
                    texts.append(text)
            return "\n".join(texts)
