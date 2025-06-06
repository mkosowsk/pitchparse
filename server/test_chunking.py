import sys
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

def chunk_pdf(pdf_path):
    print(f"Extracting and chunking text from: {pdf_path}")
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return False
    
    try:
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        # Combine all pages into one text
        text = " ".join([page.page_content for page in pages])
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)
        
        # Write chunks to file
        with open("chunks1.txt", "w") as f:
            for i, chunk in enumerate(chunks):
                f.write(f"Chunk {i+1}:\n{chunk}\n{'='*80}\n")
        
        print(f"\nTotal chunks: {len(chunks)}")
        print("\nChunk 1 (first 200 chars):")
        print(chunks[0][:200])
        print("...and", len(chunks) - 1, "more chunks.")
        
        return True
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_chunking.py <pdf_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    success = chunk_pdf(pdf_path)
    sys.exit(0 if success else 1) 