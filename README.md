# Mutual Fund FAQ Assistant

A **facts-only** Retrieval-Augmented Generation (RAG) assistant for HDFC mutual fund schemes. Answers objective, verifiable queries using official public sources — no investment advice, opinions, or recommendations.

> **Facts-only. No investment advice.**

## Selected AMC & Schemes

**AMC:** HDFC Asset Management Company Limited

| Scheme | Category | AMFI Code |
|--------|----------|-----------|
| HDFC Mid Cap Fund Direct Growth | Mid-cap | 118989 |
| HDFC Small Cap Fund Direct Growth | Small-cap | 130503 |
| HDFC Gold ETF FoF Direct Growth | Gold / FoF | 145552 |
| HDFC Large Cap Fund Direct Growth | Large-cap | 118950 |
| HDFC ELSS Tax Saver Direct Growth | ELSS | 119063 |

Groww links are used as **product reference only**. All data is sourced from official AMC, AMFI, and SEBI websites.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE-WISE RAG ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1: Data Collection          phase_1_data_collection/      │
│  ├── AMFI NAV API (live)                                         │
│  ├── HDFC AMC web pages (official)                               │
│  └── Seed corpus (SID-verified facts)                            │
│           │                                                      │
│           ▼                                                      │
│  Phase 2: Document Processing      phase_2_document_processing/  │
│  ├── Parse JSON → structured documents                           │
│  └── Chunk text (512 chars, 64 overlap)                         │
│           │                                                      │
│           ▼                                                      │
│  Phase 3: Embedding & Indexing     phase_3_embedding_indexing/   │
│  ├── Sentence-transformers (all-MiniLM-L6-v2)                   │
│  └── FAISS vector index (cosine similarity)                     │
│           │                                                      │
│           ▼                                                      │
│  Phase 4: RAG Pipeline             phase_4_rag_pipeline/           │
│  ├── Query classification (factual / advisory / PII)            │
│  ├── Semantic retrieval (top-5 chunks)                          │
│  ├── Groq LLM (openai/gpt-oss-120b)                           │
│  └── Response formatting (max 3 sentences, 1 source link)       │
│           │                                                      │
│           ▼                                                      │
│  Phase 5: User Interface           phase_5_ui/                   │
│  ├── FastAPI backend                                             │
│  └── Three-column web UI (reference design)                     │
│                                                                  │
│  Phase 6: Deployment               (planned — not implemented)   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
Mutual-Fund-FAQ-Assistant/
├── config/                          # Central settings
├── phase_1_data_collection/         # Fetch from AMFI + HDFC AMC
├── phase_2_document_processing/     # Parse & chunk documents
├── phase_3_embedding_indexing/      # Embeddings + FAISS index
├── phase_4_rag_pipeline/            # Retrieval + Groq LLM + refusal
├── phase_5_ui/                      # FastAPI + web frontend
├── data/                            # Generated at runtime
│   ├── raw/                         # Phase 1 output
│   ├── processed/                   # Phase 2 output
│   └── index/                       # Phase 3 output
├── run_pipeline.py                  # Orchestrator (Phases 1–3)
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Groq API key ([console.groq.com](https://console.groq.com/))

### Installation

```bash
# Clone and enter project
cd Mutual-Fund-FAQ-Assistant

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux
# Edit .env and add your GROQ_API_KEY
```

### Build the Knowledge Base

```bash
# Run all data pipeline phases (1 → 2 → 3)
python run_pipeline.py

# Or run phases individually:
python -m phase_1_data_collection.run
python -m phase_2_document_processing.run
python -m phase_3_embedding_indexing.run
```

### Start the Assistant

```bash
python -m phase_5_ui.app
```

Open **http://127.0.0.1:8000** in your browser.

## Response Rules

| Rule | Implementation |
|------|----------------|
| Max 3 sentences | System prompt + token limit |
| Exactly 1 source link | Retriever metadata + prompt |
| Footer with date | `Last updated from sources: <date>` |
| No investment advice | Refusal handler for advisory queries |
| No performance calculations | Redirect to official factsheet |
| No PII processing | Refusal for PAN/Aadhaar/folio queries |

## Refusal Examples

| Query Type | Example | Behavior |
|------------|---------|----------|
| Advisory | "Should I invest in Mid Cap Fund?" | Polite refusal + AMFI education link |
| Performance | "What is the 3-year CAGR?" | Redirect to official factsheet |
| PII | "Check my folio number..." | Privacy refusal + SEBI investor link |

## Data Sources

| Source | URL | Used For |
|--------|-----|----------|
| HDFC AMC | https://www.hdfcfund.com | Scheme details, TER, factsheets |
| AMFI | https://www.amfiindia.com | NAV data, scheme codes |
| SEBI | https://investor.sebi.gov.in | Regulatory references, education |

Third-party aggregators (Groww, blogs) are **not** used as data sources.

## Known Limitations

1. **Seed corpus**: Initial factual data is curated from HDFC SID/SAI disclosures. Live web scraping depends on HDFC website availability.
2. **PDF factsheets**: Monthly PDF factsheets are referenced by URL but not parsed in this version. Future enhancement planned.
3. **Single AMC**: Currently scoped to HDFC AMC only (5 schemes).
4. **Deployment**: Vercel (free tier) — see [phase_6_deployment/README.md](phase_6_deployment/README.md)
5. **Groq dependency**: LLM responses require a valid Groq API key. Retrieval-only fallback is available when the key is missing.

## Disclaimer

```
Facts-only. No investment advice.
```

This assistant provides factual information sourced from official public documents. It does not constitute investment advice, recommendation, or solicitation to buy or sell any mutual fund scheme.

## License

Internal project — HDFC Mutual Fund FAQ Assistant prototype.
