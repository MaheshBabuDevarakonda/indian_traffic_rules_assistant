import os
import json
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables (for OPENAI_API_KEY)
load_dotenv()

def load_chunks(json_path: str):
    """Loads text chunks from a JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_embeddings(texts: list[str]) -> np.ndarray:
    """Generates embeddings using OpenAI's text-embedding-3-small API."""
    model = OpenAIEmbeddings(model="text-embedding-3-small")
    embeddings = model.embed_documents(texts)
    return np.array(embeddings, dtype=np.float32)

def save_faiss_index(embeddings: np.ndarray, output_path: str):
    """Saves normalized embeddings to a FAISS index file using cosine similarity."""
    # Normalize embeddings to unit length
    faiss.normalize_L2(embeddings)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    faiss.write_index(index, output_path)
    print(f"FAISS index (cosine similarity) saved to {output_path}")


if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    chunk_path = os.path.join(BASE_DIR, "data", "processed", "indian_traffic_rules_chunks.json")
    index_path = os.path.join(BASE_DIR, "data", "processed", "faiss_cosine_index.idx")

    chunks = load_chunks(chunk_path)
    texts = [chunk["text"] for chunk in chunks]

    embeddings = generate_embeddings(texts)
    save_faiss_index(embeddings, index_path)
