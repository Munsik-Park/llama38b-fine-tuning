from __future__ import annotations

from typing import List

from docx import Document

from .base_extractor import BaseExtractor


class DocxExtractor(BaseExtractor):
    """Extract text from DOCX files using python-docx."""

    def extract_text(self) -> str:
        try:
            document = Document(self.file_path)
            paragraphs: List[str] = [p.text for p in document.paragraphs]
            return "\n".join(paragraphs)
        except Exception as e:  # pragma: no cover - simple error handling
            return f"Extraction failed: {e}"
