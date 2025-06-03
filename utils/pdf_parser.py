import fitz  # PyMuPDF
from typing import Dict, List, Optional
from llama_index.core.node_parser import SentenceSplitter

class PDFParser:
    def __init__(self, file_path: str):
        """Initialize PDF parser with file path."""
        self.file_path = file_path
        self.doc = None

    def open(self) -> None:
        """Open the PDF document."""
        self.doc = fitz.open(self.file_path)

    def close(self) -> None:
        """Close the PDF document."""
        if self.doc:
            self.doc.close()
            self.doc = None

    def extract_text(self) -> str:
        """Extract all text from the PDF."""
        if not self.doc:
            self.open()
        
        text = ""
        for page in self.doc:
            text += page.get_text()
        
        return text

    def extract_text_by_page(self) -> List[str]:
        """Extract text from each page separately."""
        if not self.doc:
            self.open()
        
        return [page.get_text() for page in self.doc]

    def get_metadata(self) -> Dict[str, str]:
        """Get PDF metadata."""
        if not self.doc:
            self.open()
        
        metadata = self.doc.metadata
        return {
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "keywords": metadata.get("keywords", ""),
            "creator": metadata.get("creator", ""),
            "producer": metadata.get("producer", ""),
            "creation_date": metadata.get("creationDate", ""),
            "modification_date": metadata.get("modDate", "")
        }

    def chunk_text_with_sentence_splitter(
        self, text: str = None, chunk_size: int = 1024, chunk_overlap: int = 200
    ) -> list:
        """
        Chunk text using LlamaIndex's SentenceSplitter with token constraints.
        If text is None, extract text from the PDF.
        """
        if text is None:
            text = self.extract_text()
        splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return splitter.split_text(text)

    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close() 