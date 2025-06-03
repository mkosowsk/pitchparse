from pdf_parser import PDFParser

def main():
    # Example usage of PDFParser
    pdf_path = "path/to/your/pdf/file.pdf"
    
    # Using context manager (recommended)
    with PDFParser(pdf_path) as parser:
        # Get all text
        text = parser.extract_text()
        print("Full text:", text[:200], "...")  # Print first 200 chars
        
        # Get text by page
        pages = parser.extract_text_by_page()
        print(f"\nNumber of pages: {len(pages)}")
        
        # Get metadata
        metadata = parser.get_metadata()
        print("\nMetadata:")
        for key, value in metadata.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main() 