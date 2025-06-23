from __future__ import annotations

from typing import List

import pandas as pd

from .base_extractor import BaseExtractor


class ExcelExtractor(BaseExtractor):
    """Extract text from Excel files using pandas."""

    def extract_text(self) -> str:
        texts: List[str] = []
        try:
            xls = pd.ExcelFile(self.file_path)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)
                texts.append(df.to_string())
            return "\n\n".join(texts)
        except Exception as e:  # pragma: no cover - simple error handling
            return f"Extraction failed: {e}"
