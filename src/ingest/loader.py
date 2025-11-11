# ingest/loader.py

import os
from abc import ABC, abstractmethod
from PyPDF2 import PdfReader
from docx import Document

# Base class
class _BaseLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> str:
        pass

# Loader classes
class _DocxLoader(_BaseLoader):
    def load(self, file_path: str) -> str:
        """Load a DOCX file and return the text."""
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

class _TextLoader(_BaseLoader):
    def load(self, file_path: str) -> str:
        """Load a text file and return the text."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

class _PdfLoader(_BaseLoader):
    def load(self, file_path: str) -> str:
        """Load a PDF file and return the text."""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

_LOADERS = {
    '.txt': _TextLoader(),
    '.pdf': _PdfLoader(),
    '.docx': _DocxLoader(),
}

# Load function
def load(file_path: str) -> str:
    """Load a file and return the text."""
    try:
        file_ext = os.path.splitext(file_path)[1].lower()
        loader = _LOADERS.get(file_ext)
        if not loader:
            raise ValueError(f"Unsupported file format: {file_ext}")
        return loader.load(file_path)
    except Exception as e:
        raise ValueError(f"Error loading file {file_path}: {e}")