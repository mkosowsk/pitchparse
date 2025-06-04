from pdf_parser import PDFParser
import os

def main():
    test_pdf = "test1.pdf"
    if not os.path.exists(test_pdf):
        print(f"Please place a test PDF file named '{test_pdf}' in the current directory.")
        return
    with PDFParser(test_pdf) as parser:
        print("Extracting and chunking text with SentenceSplitter...")
        chunks = parser.chunk_text_with_sentence_splitter(chunk_size=512, chunk_overlap=50)
        print(f"\nTotal chunks: {len(chunks)}\n")
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i+1} (first 200 chars):\n{chunk[:200]}\n{'-'*40}")
        if len(chunks) > 5:
            print(f"...and {len(chunks)-5} more chunks.")
        with open("chunks1.txt", "w") as f:
            for i, chunk in enumerate(chunks):
                f.write(f"Chunk {i+1}:\n{chunk}\n{'-'*40}\n")

if __name__ == "__main__":
    main() 