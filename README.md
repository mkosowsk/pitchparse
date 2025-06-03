# PitchParse

A PDF parsing and analysis tool built with Python.

## Project Structure

```
pitchparse/
├── client/         # Frontend application
├── server/         # Backend API server
├── utils/          # Utility functions and tools
│   ├── pdf_parser.py
│   └── example.py
└── models/         # Data models and schemas
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The PDF parser utility can be used as follows:

```python
from utils.pdf_parser import PDFParser

# Using context manager (recommended)
with PDFParser("path/to/your/pdf/file.pdf") as parser:
    # Extract all text
    text = parser.extract_text()
    
    # Extract text by page
    pages = parser.extract_text_by_page()
    
    # Get PDF metadata
    metadata = parser.get_metadata()
```

## Features

- PDF text extraction
- Page-by-page text extraction
- PDF metadata extraction
- Context manager support for safe file handling

## Dependencies

- PyMuPDF (fitz)
- python-dotenv
- fastapi
- uvicorn
- pydantic 