from __future__ import annotations

from pathlib import Path

from .base_extractor import BaseExtractor
from .docx_extractor import DocxExtractor
from .excel_extractor import ExcelExtractor
from .hwp_extractor import HWPExtractor
from .pdf_extractor import PDFExtractor
from .ppt_extractor import PPTExtractor


EXTENSION_MAP = {
    ".pdf": PDFExtractor,
    ".hwp": HWPExtractor,
    ".docx": DocxExtractor,
    ".doc": DocxExtractor,
    ".pptx": PPTExtractor,
    ".ppt": PPTExtractor,
    ".xlsx": ExcelExtractor,
    ".xls": ExcelExtractor,
}


def get_extractor(file_path: str) -> BaseExtractor:
    ext = Path(file_path).suffix.lower()
    extractor_cls = EXTENSION_MAP.get(ext)
    if extractor_cls is None:
        raise ValueError(f"Unsupported file extension: {ext}")
    return extractor_cls(file_path)
