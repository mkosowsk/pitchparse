import json
import os
from sentence_transformers import SentenceTransformer

# Load the sentence transformer model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def read_chunks(file_path="chunks1.txt"):
    with open(file_path, "r") as f:
        content = f.read()
    # Split by the separator to get individual chunks
    chunks = content.split("-" * 40)
    # Clean up each chunk (remove leading/trailing whitespace and empty chunks)
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    return chunks

def get_embedding(text):
    return model.encode(text).tolist()

def main():
    chunks = read_chunks()
    embeddings = {}
    for i, chunk in enumerate(chunks):
        print(f"Embedding chunk {i+1}/{len(chunks)}...")
        embedding = get_embedding(chunk)
        embeddings[f"chunk_{i+1}"] = {
            "text": chunk,
            "embedding": embedding
        }

    with open("chunk_embeddings1.json", "w") as f:
        json.dump(embeddings, f, indent=2)
    print("Embeddings saved to chunk_embeddings1.json")

if __name__ == "__main__":
    main() 