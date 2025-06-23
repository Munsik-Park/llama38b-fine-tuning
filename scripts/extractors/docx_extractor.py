from __future__ import annotations

from typing import List
import os

from docx import Document

from .base_extractor import BaseExtractor


class DocxExtractor(BaseExtractor):
    """Extract text from DOCX files using python-docx."""

    def extract_text(self) -> str:
        try:
            document = Document(self.file_path)
            paragraphs: List[str] = [p.text for p in document.paragraphs]
            return "\n".join(paragraphs)
        except Exception as e:
            # DOC 파일이 실제로는 다른 형식일 수 있음
            error_msg = str(e)
            if "not a Word file" in error_msg:
                return f"Extraction failed: 파일이 Word 형식이 아닙니다. 실제 형식: {error_msg}"
            else:
                return f"Extraction failed: {error_msg}"
