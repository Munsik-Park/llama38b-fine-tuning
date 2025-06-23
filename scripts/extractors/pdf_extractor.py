from __future__ import annotations

from typing import List

import fitz  # PyMuPDF

from .base_extractor import BaseExtractor


class PDFExtractor(BaseExtractor):
    """Extract text from PDF files using PyMuPDF."""

    def extract_text(self) -> str:
        texts: List[str] = []
        try:
            with fitz.open(self.file_path) as doc:
                for page in doc:
                    texts.append(page.get_text())
            return "\n".join(texts)
        except Exception as e:  # pragma: no cover - simple error handling
            return f"Extraction failed: {e}"
