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

# Load embeddings from chunk_embeddings1.json
def load_embeddings(file_path="chunk_embeddings1.json"):
    with open(file_path, "r") as f:
        return json.load(f)

# Create a Qdrant collection
def create_collection(collection_name="chunks1"):
    client.recreate_collection(
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
    search_results = client.search(
        collection_name="chunks1",
        query_vector=query_embedding,
        limit=10,  # Increased from 5 to 10 to get more potential matches
        score_threshold=0.5  # Lowered threshold to get more results
    )
    results = []
    print("\nSearch Results:")
    for hit in search_results:
        text = hit.payload.get("text", "")
        results.append(text)
        print(f"\nScore: {hit.score}")
        print(f"Text: {text}")
    
    # Improved extraction logic for each field
    sector = "Sector: Not found"
    hq = "HQ: Not found"
    revenue = "Revenue: Not found"
    growth = "Growth: Not found"
    margin = "Margin: Not found"
    
    for text in results:
        # SECTOR
        if "sector" in text.lower() or "industry" in text.lower() or "software and services" in text.lower():
            # Try to extract after 'Sector' or 'Industry' or just grab the phrase
            sector_match = re.search(r"Sector\s*:?\s*([A-Za-z &]+)", text)
            if sector_match:
                sector = f"Sector: {sector_match.group(1).strip()}"
            else:
                # Fallback: look for 'industry' or 'software and services'
                industry_match = re.search(r"Industry\s*:?\s*([A-Za-z &]+)", text)
                if industry_match:
                    sector = f"Sector: {industry_match.group(1).strip()}"
                elif "software and services" in text:
                    sector = "Sector: College Admissions Software and Services"

        # HQ
        if "headquarters" in text.lower() or "headquartered in" in text.lower() or "based in" in text.lower() or "location" in text.lower():
            hq_match = re.search(r"Headquarters\s*:?\s*([A-Za-z, ]+)", text)
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
            # Look for $ amounts near revenue/ARR
            revenue_match = re.search(r"\$([\d,.]+[MB]?)\s*(?:in\s+)?(?:revenue|arr|income)", text, re.IGNORECASE)
            if revenue_match:
                revenue = f"Revenue: ${revenue_match.group(1)}"
            else:
                # Look for sentences like 'revenue grew ... from $X to $Y'
                revenue_range = re.search(r"revenue grew.*?from \$([\d,.]+[MB]?).*?to \$([\d,.]+[MB]?)", text, re.IGNORECASE)
                if revenue_range:
                    revenue = f"Revenue: ${revenue_range.group(2)}"
                else:
                    # Look for 'generated $X in revenue'
                    revenue_gen = re.search(r"generated \$([\d,.]+[MB]?) in revenue", text, re.IGNORECASE)
                    if revenue_gen:
                        revenue = f"Revenue: ${revenue_gen.group(1)}"

        # GROWTH
        if "growth" in text.lower() or "cagr" in text.lower() or "increase" in text.lower():
            # Look for % near growth/CAGR
            growth_match = re.search(r"(\d{1,3}(?:\.\d+)?%)\s*(?:growth|cagr|increase)", text, re.IGNORECASE)
            if growth_match:
                growth = f"Growth: {growth_match.group(1)}"
            else:
                # Look for 'grew at a CAGR of X%'
                cagr_match = re.search(r"CAGR of (\d{1,3}(?:\.\d+)?%)", text, re.IGNORECASE)
                if cagr_match:
                    growth = f"Growth: {cagr_match.group(1)}"
                else:
                    # Look for 'ARR YoY Growth (2024) XX%'
                    arr_growth = re.search(r"ARR YoY Growth.*?(\d{1,3}(?:\.\d+)?%)", text, re.IGNORECASE)
                    if arr_growth:
                        growth = f"Growth: {arr_growth.group(1)}"

        # MARGIN
        if "margin" in text.lower() or "ebitda" in text.lower() or "profit" in text.lower():
            # Look for % near margin/EBITDA
            margin_match = re.search(r"(\d{1,3}(?:\.\d+)?%)\s*(?:margin|ebitda)", text, re.IGNORECASE)
            if margin_match:
                margin = f"Margin: {margin_match.group(1)}"
            else:
                # Look for 'Adjusted EBITDA margin of XX%'
                adj_margin = re.search(r"Adjusted EBITDA margin[s]? of (\d{1,3}(?:\.\d+)?%)", text, re.IGNORECASE)
                if adj_margin:
                    margin = f"Margin: {adj_margin.group(1)}"
                else:
                    # Look for 'strong XX% Adjusted EBITDA margin'
                    strong_margin = re.search(r"strong (\d{1,3}(?:\.\d+)?%) Adjusted EBITDA margin", text, re.IGNORECASE)
                    if strong_margin:
                        margin = f"Margin: {strong_margin.group(1)}"
    
    with open("company_snapshot1.txt", "w") as f:
        f.write(f"{sector}\n{hq}\n{revenue}\n{growth}\n{margin}\n")
    print("company_snapshot1.txt written with queried fields.")

def main():
    embeddings = load_embeddings()
    create_collection()
    store_embeddings(embeddings)
    print("Embeddings stored in Qdrant successfully.")
    write_company_snapshot2()

if __name__ == "__main__":
    main() 