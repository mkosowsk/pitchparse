from pdf_parser import PDFParser
import os
import sys

def test_parser(pdf_path: str):
    # Check if the file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found")
        return
    
    # Test the parser
    with PDFParser(pdf_path) as parser:
        # Test text extraction
        text = parser.extract_text()
        print("\nExtracted text (first 200 chars):")
        print("-" * 50)
        print(text[:200])
        print("-" * 50)
        
        # Test page-by-page extraction
        pages = parser.extract_text_by_page()
        print(f"\nNumber of pages: {len(pages)}")
        
        # Test metadata extraction
        metadata = parser.get_metadata()
        print("\nPDF Metadata:")
        print("-" * 50)
        for key, value in metadata.items():
            print(f"{key}: {value}")
        print("-" * 50)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_parser.py <pdf_file_path>")
        sys.exit(1)
    
    test_parser(sys.argv[1]) 