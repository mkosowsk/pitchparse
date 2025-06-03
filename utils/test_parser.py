from pdf_parser import PDFParser
import os

def test_parser():
    # Create a test PDF file path
    test_pdf = "test.pdf"
    
    # Check if the test file exists
    if not os.path.exists(test_pdf):
        print(f"Please place a test PDF file named '{test_pdf}' in the current directory")
        return
    
    # Test the parser
    with PDFParser(test_pdf) as parser:
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
    test_parser() 