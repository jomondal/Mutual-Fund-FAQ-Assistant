# Phase 4: RAG Pipeline

Retrieval-Augmented Generation engine using **Groq LLM** for facts-only responses.

## Architecture

```
User Query
    │
    ▼
┌─────────────────┐
│ Refusal Handler │──▶ Advisory / Performance / PII → Refusal Response
└────────┬────────┘
         │ (Factual)
         ▼
┌─────────────────┐
│   Retriever     │──▶ Top-K chunks from FAISS
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Groq LLM       │──▶ Facts-only answer (max 3 sentences)
│  (llama-3.3)    │
└────────┬────────┘
         │
         ▼
   Response + Source Link + Footer
```

## Response Rules

| Rule | Enforcement |
|------|-------------|
| Max 3 sentences | System prompt + max_tokens=300 |
| Exactly 1 source link | Prompt instruction + retriever metadata |
| Footer with date | Appended programmatically |
| No investment advice | Refusal handler for advisory patterns |
| No performance calcs | Refusal handler for performance patterns |

## Refusal Categories

- **Advisory**: "Should I invest?", "Which fund is better?"
- **Performance**: CAGR, returns, comparisons
- **PII**: PAN, Aadhaar, folio numbers, OTPs

## Configuration

Set in `.env`:
```
GROQ_API_KEY=your_key
GROQ_MODEL=openai/gpt-oss-120b
```

## Usage

```python
from phase_4_rag_pipeline.rag_engine import get_pipeline

pipeline = get_pipeline()
response = pipeline.query("What is the expense ratio of HDFC Mid Cap Fund?")
print(response["answer"])
```
