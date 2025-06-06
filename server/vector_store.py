import json
import os
import re
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer

# Initialize Qdrant client
client = QdrantClient(":memory:")  # Use in-memory storage for simplicity

# Load the sentence transformer model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def read_chunks(file_path="chunks1.txt"):
    with open(file_path, "r") as f:
        content = f.read()
    chunks = []
    chunk_regex = r"Chunk \d+:\n([\s\S]*?)(?=\n-{40}|$)"
    for match in re.finditer(chunk_regex, content):
        chunks.append(match.group(1).strip())
    return chunks

def generate_embeddings(chunks):
    embeddings = {}
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        embeddings[f"chunk_{i}"] = {
            "text": chunk,
            "embedding": embedding
        }
    return embeddings

# Create a Qdrant collection
def create_collection(collection_name="chunks1"):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=384,  # Size of the embeddings (adjust if needed)
                distance=models.Distance.COSINE
            )
        )

# Store embeddings in Qdrant
def store_embeddings(embeddings, collection_name="chunks1"):
    points = []
    for chunk_id, data in embeddings.items():
        points.append(
            models.PointStruct(
                id=int(chunk_id.split("_")[1]),
                vector=data["embedding"],
                payload={"text": data["text"]}
            )
        )
    client.upsert(collection_name=collection_name, points=points)

# Query Qdrant for a field using a keyword
def query_field(field, collection_name="chunks1"):
    # Simple keyword search in payloads
    search_results = client.scroll(collection_name=collection_name, scroll_filter=None, limit=100)
    for point in search_results[0]:
        text = point.payload.get("text", "").lower()
        if field in text:
            return point.payload.get("text", "")
    return f"{field.title()}: Not found"

def write_company_snapshot2():
    query = "Represent this sentence for searching relevant passages: What are the key company details including sector, HQ, revenue, growth, margin?"
    query_embedding = model.encode(query).tolist()
    search_results = client.query_points(
        collection_name="chunks1",
        query=query_embedding,
        limit=10,  # Increased from 5 to 10 to get more potential matches
        score_threshold=0.5  # Lowered threshold to get more results
    )
    results = []
    for hit in search_results.points:
        text = hit.payload.get("text", "")
        results.append(text)

    # Improved extraction logic for each field
    sector = "Sector: Not found"
    hq = "HQ: Not found"
    revenue = "Revenue: Not found"
    growth = "Growth: Not found"
    margin = "Margin: Not found"

    for text in results:
        # SECTOR
        if "sector" in text.lower() or "industry" in text.lower() or "software and services" in text.lower():
            sector_match = re.search(r"Sector\s*:?[\s\-]*([A-Za-z &]+)", text)
            if sector_match:
                sector = f"Sector: {sector_match.group(1).strip()}"
            else:
                industry_match = re.search(r"Industry\s*:?[\s\-]*([A-Za-z &]+)", text)
                if industry_match:
                    sector = f"Sector: {industry_match.group(1).strip()}"
                elif "software and services" in text:
                    sector = "Sector: College Admissions Software and Services"
                else:
                    # Try to extract from overview lines
                    overview_match = re.search(r"Overview\s*:?[\s\-]*([A-Za-z &]+)", text)
                    if overview_match:
                        sector = f"Sector: {overview_match.group(1).strip()}"

        # HQ
        if "headquarters" in text.lower() or "headquartered in" in text.lower() or "based in" in text.lower() or "location" in text.lower():
            hq_match = re.search(r"Headquarters\s*:?[\s\-]*([A-Za-z, ]+)", text)
            if hq_match:
                hq = f"HQ: {hq_match.group(1).strip()}"
            else:
                hq_match2 = re.search(r"headquartered in ([A-Za-z, ]+)", text, re.IGNORECASE)
                if hq_match2:
                    hq = f"HQ: {hq_match2.group(1).strip()}"
                else:
                    hq_match3 = re.search(r"based in ([A-Za-z, ]+)", text, re.IGNORECASE)
                    if hq_match3:
                        hq = f"HQ: {hq_match3.group(1).strip()}"

        # REVENUE
        if "revenue" in text.lower() or "arr" in text.lower() or "income" in text.lower():
            revenue_match = re.search(r"\$([\d,.]+[MB]?)\s*(?:in\s+)?(?:revenue|arr|income)", text, re.IGNORECASE)
            if revenue_match:
                revenue = f"Revenue: ${revenue_match.group(1)}"
            else:
                revenue_range = re.search(r"revenue grew.*?from \$([\d,.]+[MB]?).*?to \$([\d,.]+[MB]?)", text, re.IGNORECASE)
                if revenue_range:
                    revenue = f"Revenue: ${revenue_range.group(2)}"
                else:
                    revenue_gen = re.search(r"generated \$([\d,.]+[MB]?) in revenue", text, re.IGNORECASE)
                    if revenue_gen:
                        revenue = f"Revenue: ${revenue_gen.group(1)}"

        # GROWTH
        if "growth" in text.lower() or "cagr" in text.lower() or "increase" in text.lower():
            growth_match = re.search(r"(\d{1,3}(?:\.\d+)?%)\s*(?:growth|cagr|increase)", text, re.IGNORECASE)
            if growth_match:
                growth = f"Growth: {growth_match.group(1)}"
            else:
                cagr_match = re.search(r"CAGR of (\d{1,3}(?:\.\d+)?%)", text, re.IGNORECASE)
                if cagr_match:
                    growth = f"Growth: {cagr_match.group(1)}"
                else:
                    arr_growth = re.search(r"ARR YoY Growth.*?(\d{1,3}(?:\.\d+)?%)", text, re.IGNORECASE)
                    if arr_growth:
                        growth = f"Growth: {arr_growth.group(1)}"

        # MARGIN
        if "margin" in text.lower() or "ebitda" in text.lower() or "profit" in text.lower():
            margin_match = re.search(r"(\d{1,3}(?:\.\d+)?%)\s*(?:margin|ebitda)", text, re.IGNORECASE)
            if margin_match:
                margin = f"Margin: {margin_match.group(1)}"
            else:
                adj_margin = re.search(r"Adjusted EBITDA margin[s]? of (\d{1,3}(?:\.\d+)?%)", text, re.IGNORECASE)
                if adj_margin:
                    margin = f"Margin: {adj_margin.group(1)}"
                else:
                    strong_margin = re.search(r"strong (\d{1,3}(?:\.\d+)?%) Adjusted EBITDA margin", text, re.IGNORECASE)
                    if strong_margin:
                        margin = f"Margin: {strong_margin.group(1)}"

    # Write concise, single-line values for each field
    with open("company_snapshot1.txt", "w") as f:
        f.write(f"{sector}\n{hq}\n{revenue}\n{growth}\n{margin}\n")
    print("company_snapshot1.txt written with queried fields.")

def main():
    # Read chunks from file
    chunks = read_chunks()
    
    # Generate embeddings
    embeddings = generate_embeddings(chunks)
    
    # Create collection and store embeddings
    create_collection()
    store_embeddings(embeddings)
    print("Embeddings stored in Qdrant successfully.")
    
    # Extract and write company details
    write_company_snapshot2()

if __name__ == "__main__":
    main() 