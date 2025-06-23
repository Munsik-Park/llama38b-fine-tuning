from __future__ import annotations

import subprocess

from .base_extractor import BaseExtractor


class HWPExtractor(BaseExtractor):
    """Extract text from HWP files using the hwp5txt CLI tool."""

    def extract_text(self) -> str:
        try:
            result = subprocess.run(
                ["hwp5txt", self.file_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return result.stdout
        except Exception as e:  # pragma: no cover - simple error handling
            return f"Extraction failed: {e}"
