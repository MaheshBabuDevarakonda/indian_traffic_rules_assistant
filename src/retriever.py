# src/retriever.py

import os
import json
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables (for OPENAI_API_KEY)
load_dotenv()

class Retriever:
    def __init__(self, index_path: str, chunk_json_path: str):
        """
        Initializes the Retriever with FAISS index, chunk texts, and OpenAI Embeddings.
        """
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index not found at {index_path}")
        if not os.path.exists(chunk_json_path):
            raise FileNotFoundError(f"Chunk file not found at {chunk_json_path}")

        self.index = faiss.read_index(index_path)
        self.chunks = self._load_chunks(chunk_json_path)
        self.model = OpenAIEmbeddings(model="text-embedding-3-small")

    def _load_chunks(self, json_path: str) -> list[dict]:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def query(self, question: str, top_k: int = 3) -> list[dict]:
        """
        Takes a user question and returns top_k relevant chunks using cosine similarity.
        """
        question_embedding = self.model.embed_query(question)
        embedding_array = np.array([question_embedding], dtype=np.float32)
        faiss.normalize_L2(embedding_array)
        D, I = self.index.search(embedding_array, top_k)
        
        results = []
        for idx in I[0]:
            if idx < len(self.chunks):
                results.append(self.chunks[idx])
        return results

# For testing this module independently
if __name__ == "__main__":
    # base_dir = os.path.join("..", "data", "processed")
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    retriever = Retriever(
            index_path=os.path.join(BASE_DIR, "data", "processed", "faiss_cosine_index.idx"),
            chunk_json_path=os.path.join(BASE_DIR, "data", "processed", "indian_traffic_rules_chunks.json")
    )

    query = "What is the fine for not wearing a helmet?"
    top_chunks = retriever.query(query, top_k=10)

    print("\nTop Matching Chunks:\n")
    for i, chunk in enumerate(top_chunks, 1):
        print(f"[Chunk {chunk['chunk_id']}]\n{chunk['text']}\n{'-'*60}")
