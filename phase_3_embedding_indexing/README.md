# Phase 3: Embedding & Indexing

Generates dense vector embeddings and builds a FAISS index for semantic search.

## Architecture

```
data/processed/chunks.json
         │
         ▼
   Embedder (all-MiniLM-L6-v2)
         │
         ▼
   FAISS IndexFlatIP (cosine similarity)
         │
         ▼
data/index/
  ├── faiss.index
  └── chunk_metadata.json
```

## Components

| File | Role |
|------|------|
| `embedder.py` | Sentence-transformer embedding generation |
| `vector_store.py` | FAISS index load + top-k retrieval |

## Configuration

| Parameter | Default |
|-----------|---------|
| `embedding_model` | all-MiniLM-L6-v2 |
| `top_k` | 5 |

## Run

```bash
python -m phase_3_embedding_indexing.run
```

## Retrieval Flow

```
User Query → Embed Query → FAISS Search → Top-K Chunks + Metadata
```
