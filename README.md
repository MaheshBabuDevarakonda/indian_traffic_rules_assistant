# AI Traffic Assistant (RAG Chatbot Prototype)

An interactive, AI-powered assistant built using Retrieval-Augmented Generation (RAG) that provides context-aware answers about Indian traffic rules, penalties, and driver guidelines. It queries a local FAISS vector store generated from official road safety rulebooks and answers via a cloud-based LLM.

---

## Repo Structure
```plaintext
traffic_rules_assistant/
├── data/
│   ├── processed/
│   │    ├── faiss_cosine_index.idx
│   │    ├── indian_traffic_rules_chunks.json
│   │    └── indian_traffic_rules.txt
│   └── Indian traffic rules.pdf
├── src/
│   ├── chunking.py 
│   ├── embedding.py 
│   ├── generator.py
│   ├── retriever.py
│   ├── main.py
│   └── text_extraction.py 
├── api/
│   └── app.py
├── frontend/ 
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── .gitignore
├── README.md
├── requirements.txt
└── pyproject.toml
```

---

## Project Overview

This project extracts legal content from a PDF document containing Indian road regulations and exposes it via a natural language chat interface. 

To optimize performance and resource limits for serverless hosting (such as Render's 512 MB memory limit):
* **Cloud-based Embeddings**: Uses **OpenAI `text-embedding-3-small`** via API. This avoids importing heavy libraries like PyTorch/Transformers locally, keeping the server memory footprint under **50 MB** (instead of 450+ MB).
* **FAISS Indexing**: Stores normalized document vectors in a local flat Inner Product (`IndexFlatIP`) index to perform rapid cosine similarity search.
* **LLM Engine**: Uses **OpenAI `gpt-4o-mini`** via `langchain-openai` for generating structured, context-grounded responses.
* **Web UI Dashboard**: A clean, responsive 3-column citizen portal interface complete with dynamic RAG chat assistance, quick fine check reference tables, and emergency helpline listings.

---

## Prerequisites

* Python 3.11+
* A package manager like `uv` or `pip`
* An OpenAI API Key

---

## Installation & Setup

### 1. Clone the project and initialize virtualenv:
```bash
cd traffic_rules_assistant

# Create virtual environment
uv venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
uv pip install -r requirements.txt
```

### 2. Configure Environment:
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your-openai-api-key-here
```

---

## Data Pipeline Usage

If you modify the source PDF document (`data/Indian traffic rules.pdf`), run the following pipeline scripts to rebuild the database:

### 1. Extract text from PDF:
```bash
uv run python -m src.text_extraction
```

### 2. Chunk text:
```bash
uv run python -m src.chunking
```

### 3. Generate OpenAI embeddings and FAISS index:
```bash
uv run python -m src.embedding
```

---

## Running the Application

### 1. Start the Backend API (FastAPI):
```bash
uv run uvicorn api.app:app --reload
```
The interactive API documentation will be available at **[http://localhost:8000/docs](http://localhost:8000/docs)**.

### 2. Run the Local Frontend:
Serve the `frontend` directory using any HTTP server:
```bash
python -m http.server 8080 -d frontend
```
Visit **[http://localhost:8080](http://localhost:8080)** in your browser to interact with the portal!

---

## Configuration Settings

* **Chunking**: `chunk_size = 300` characters, with `overlap = 50` characters.
* **Embeddings**: OpenAI `text-embedding-3-small` (1536 dimensions).
* **Vector Index**: `faiss.IndexFlatIP` (Cosine similarity search).
* **Generation**: OpenAI `gpt-4o-mini` (Temperature: `0.3`).

---

## Performance
* **Build Time**: Installs dependencies in under 15 seconds.
* **RAM Footprint**: Under **50 MB** in production (perfect for Render Free Tier).
* **Latency**: Fast semantic search matching in ~20ms.

---

## Changelog

### v1.2.0 (July 2026)
* **Rebranded Interface**: Renamed to "AI Traffic Assistant" and created an interactive mockup dashboard.
* **OpenAI Integration**: Switched generator to OpenAI `gpt-4o-mini` and retriever to `text-embedding-3-small` API.
* **Memory Optimization**: Removed PyTorch and local transformer downloads to guarantee stability on 512MB RAM servers.
* **GitHub Actions & Deployment Config**: Created clean `.gitignore` rules to isolate secrets and push clean initial codebase.
