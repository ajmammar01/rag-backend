# Production-Ready RAG Backend Pipeline

A high-performance Retrieval-Augmented Generation (RAG) backend engineered with Python, FastAPI, and ChromaDB. This system goes beyond basic vector search by implementing query expansion, cross-encoder semantic re-ranking, and strict production error boundaries to deliver highly accurate context retrieval for Large Language Models.

## 🚀 Key Engineering Features
* **Modern Packaging with `uv`:** Utilizes Astral's lightning-fast `uv` toolchain for deterministic package resolution and minimal Docker layer sizes.
* **Two-Stage Retrieval Engine:** 1. **Dense Retrieval:** Generates vector embeddings and queries a persistent `ChromaDB` collection.
  2. **Reranking Pipeline:** Employs a HuggingFace Cross-Encoder model (`BAAI/bge-reranker-base`) to score and re-rank the retrieved chunks, mitigating LLM "lost in the middle" phenomena.
* **Query Expansion:** Automatically expands user questions into multiple variations to maximize search recall across the vector space.
* **Production Error Boundaries:** Implements global FastAPI exception middleware, structural validation using Pydantic, empty-retrieval short-circuiting, and explicit database missing-collection handling.
* **Dockerized Infrastructure:** Containerized configuration designed to cleanly isolate application dependencies from local system states.

---

## 🛠️ Tech Stack
* **Framework:** FastAPI (Python 3.12)
* **Vector Store:** ChromaDB (Local Persistent File Mode)
* **LLM Engine:** OpenAI GPT API
* **Re-ranker Model:** HuggingFace Cross-Encoder (`bge-reranker-base`)
* **Environment & Tooling:** `uv`, Docker

---

## 📦 Getting Started (Local Development)

### Prerequisites
* Python 3.12+ Installed
* An OpenAI API Key configured in your environment

### 1. Installation
Clone the repository and install the locked dependencies using `uv`:
```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/rag-backend.git](https://github.com/YOUR_USERNAME/rag-backend.git)
cd rag-backend

# Install virtual env and locked dependencies
uv sync