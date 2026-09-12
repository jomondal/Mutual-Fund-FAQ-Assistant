# Phase 3: Embedding & Indexing

Generates dense vector embeddings and builds a FAISS index for semantic search. A lightweight **keyword store** is also included for Vercel serverless deployment.

## Architecture

```
data/processed/chunks.json
         │
         ├──────────────────────────────┐
         ▼                              ▼
   Embedder (local)              KeywordStore (Vercel)
   all-MiniLM-L6-v2               BM25-style scoring
         │                              │
         ▼                              │
   FAISS IndexFlatIP                    │
         │                              │
         └──────────────┬───────────────┘
                        ▼
              data/index/
                ├── faiss.index          (local only)
                └── chunk_metadata.json  (local + Vercel)
```

## Components

| File | Role |
|------|------|
| `embedder.py` | Sentence-transformer embedding generation (local) |
| `vector_store.py` | FAISS index load + top-k retrieval (local) |
| `keyword_store.py` | BM25-style keyword retrieval (Vercel) |
| `retrieval_types.py` | Shared `RetrievalResult` dataclass |

## Configuration

| Parameter | Default |
|-----------|---------|
| `embedding_model` | all-MiniLM-L6-v2 |
| `top_k` | 5 |
| `use_keyword_retrieval` | `true` when `VERCEL=1` |

## Run

```bash
python -m phase_3_embedding_indexing.run
```

## Retrieval Flow

**Local:** `User Query → Embed Query → FAISS Search → Top-K Chunks`

**Vercel:** `User Query → BM25 Keyword Scoring → Top-K Chunks`
