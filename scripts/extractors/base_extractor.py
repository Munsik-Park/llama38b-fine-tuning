from __future__ import annotations

from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """Base class for text extractors."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def extract_text(self) -> str:
        """Extract text from the target file and return it as a string."""
        raise NotImplementedError
