# Mutual Fund FAQ Assistant

A **facts-only** Retrieval-Augmented Generation (RAG) assistant for HDFC mutual fund schemes. It answers objective, verifiable queries using official public sources — no investment advice, opinions, or recommendations.

> **Facts-only. No investment advice.**

## Description

The **Mutual Fund FAQ Knowledge Assistant** is a phase-wise RAG application built for **HDFC Asset Management Company Limited**. It helps users get quick, factual answers about five selected HDFC schemes — expense ratios, exit loads, lock-in periods, fund managers, risk classifications, and investment minimums.

The system collects data from **official AMC, AMFI, and SEBI sources**, processes it into searchable chunks, retrieves relevant context, and generates concise answers via **Groq LLM** — with strict refusal handling for advisory, performance, PII, and out-of-scope queries.

| Aspect | Detail |
|--------|--------|
| **Scope** | HDFC AMC — 5 schemes (Mid Cap, Small Cap, Large Cap, ELSS, Gold ETF FoF) |
| **Stack** | Python, FastAPI, FAISS, sentence-transformers, Groq LLM |
| **UI** | Three-column responsive web interface |
| **Deployment** | Vercel (free tier) — [Live demo](https://hdfc-faq-assistant.vercel.app) |
| **Compliance** | Facts-only; no buy/sell/hold advice; verify AI responses with cited sources |

## Live Demo

| Resource | Link |
|----------|------|
| **Live app** | [https://hdfc-faq-assistant.vercel.app](https://hdfc-faq-assistant.vercel.app) |
| **GitHub** | [github.com/jomondal/Mutual-Fund-FAQ-Assistant](https://github.com/jomondal/Mutual-Fund-FAQ-Assistant) |
| **Health check** | [https://hdfc-faq-assistant.vercel.app/api/health](https://hdfc-faq-assistant.vercel.app/api/health) |

Alternate production URL: [https://mutual-fund-faq-assistant-ebon.vercel.app](https://mutual-fund-faq-assistant-ebon.vercel.app)

---

## Selected AMC & Schemes

**AMC:** HDFC Asset Management Company Limited

| Scheme | Category | AMFI Code |
|--------|----------|-----------|
| HDFC Mid Cap Fund Direct Growth | Mid-cap | 118989 |
| HDFC Small Cap Fund Direct Growth | Small-cap | 130503 |
| HDFC Gold ETF FoF Direct Growth | Gold / FoF | 145552 |
| HDFC Large Cap Fund Direct Growth | Large-cap | 118950 |
| HDFC ELSS Tax Saver Direct Growth | ELSS | 119063 |

Groww links are used as **product reference only**. All factual data is sourced from official AMC, AMFI, and SEBI websites.

---

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
│  ├── Sentence-transformers (all-MiniLM-L6-v2) — local           │
│  ├── FAISS vector index — local                                 │
│  └── Keyword retrieval (BM25-style) — Vercel                    │
│           │                                                      │
│           ▼                                                      │
│  Phase 4: RAG Pipeline             phase_4_rag_pipeline/           │
│  ├── Query classification (factual / advisory / PII)            │
│  ├── Retrieval (top-5 chunks)                                   │
│  ├── Groq LLM (openai/gpt-oss-120b)                           │
│  └── Response formatting (max 3 sentences, 1 source link)       │
│           │                                                      │
│           ▼                                                      │
│  Phase 5: User Interface           phase_5_ui/                   │
│  ├── FastAPI backend                                             │
│  └── Three-column web UI                                        │
│           │                                                      │
│           ▼                                                      │
│  Phase 6: Deployment               phase_6_deployment/           │
│  └── Vercel serverless (free tier)                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
Mutual-Fund-FAQ-Assistant/
├── api/                             # Vercel serverless entrypoint
├── config/                          # Central settings
├── phase_1_data_collection/         # Fetch from AMFI + HDFC AMC
├── phase_2_document_processing/     # Parse & chunk documents
├── phase_3_embedding_indexing/      # Embeddings + FAISS + keyword store
├── phase_4_rag_pipeline/            # Retrieval + Groq LLM + refusal
├── phase_5_ui/                      # FastAPI + web frontend
├── phase_6_deployment/              # Vercel deployment guide
├── data/
│   └── index/                       # Committed for cloud deployment
├── run_pipeline.py                  # Orchestrator (Phases 1–3)
├── requirements.txt                 # Local development
├── requirements-vercel.txt          # Vercel serverless (lightweight)
├── vercel.json                      # Vercel configuration
├── .env.example
└── README.md
```

---

## Documentation

| Phase | Description | Guide |
|-------|-------------|-------|
| Phase 1 | Data collection from AMFI & HDFC AMC | [phase_1_data_collection/README.md](phase_1_data_collection/README.md) |
| Phase 2 | Document parsing & chunking | [phase_2_document_processing/README.md](phase_2_document_processing/README.md) |
| Phase 3 | Embeddings, FAISS index & keyword store | [phase_3_embedding_indexing/README.md](phase_3_embedding_indexing/README.md) |
| Phase 4 | RAG pipeline, Groq LLM & refusal handling | [phase_4_rag_pipeline/README.md](phase_4_rag_pipeline/README.md) |
| Phase 5 | FastAPI backend & three-column UI | [phase_5_ui/README.md](phase_5_ui/README.md) |
| Phase 6 | Vercel deployment (free tier) | [phase_6_deployment/README.md](phase_6_deployment/README.md) |

---

## Quick Start (Local)

### Prerequisites

- Python 3.10+
- Groq API key — [console.groq.com](https://console.groq.com/)

### Installation

```bash
git clone https://github.com/jomondal/Mutual-Fund-FAQ-Assistant.git
cd Mutual-Fund-FAQ-Assistant

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt

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

### Run Locally

```bash
python -m phase_5_ui.app
```

Open **http://127.0.0.1:8000** in your browser.

---

## Deployment (Vercel)

The app is hosted permanently on Vercel (free tier):

**https://hdfc-faq-assistant.vercel.app**

For setup, environment variables, and redeployment steps, see [phase_6_deployment/README.md](phase_6_deployment/README.md).

| Environment | Retrieval | LLM |
|-------------|-----------|-----|
| Local | FAISS + sentence-transformers | Groq |
| Vercel | Keyword (BM25-style) | Groq |

---

## Response Rules

| Rule | Implementation |
|------|----------------|
| Max 3 sentences | System prompt + token limit |
| Exactly 1 source link | Retriever metadata + prompt |
| Footer with date | `Last updated from sources: <date>` |
| No investment advice | Refusal handler for advisory queries |
| No performance calculations | Redirect to official factsheet |
| No PII processing | Refusal for PAN/Aadhaar/folio queries |

---

## Refusal Examples

| Query Type | Example | Behavior |
|------------|---------|----------|
| Advisory | "Should I invest in Mid Cap Fund?" | Polite refusal + AMFI education link |
| Performance | "What is the 3-year CAGR?" | Redirect to official factsheet |
| PII | "Check my folio number..." | Privacy refusal + SEBI investor link |
| Out of scope | "What is EBITDA?" | Out-of-scope refusal |

---

## Data Sources

| Source | URL | Used For |
|--------|-----|----------|
| HDFC AMC | https://www.hdfcfund.com | Scheme details, TER, factsheets |
| AMFI | https://www.amfiindia.com | NAV data, scheme codes |
| SEBI | https://investor.sebi.gov.in | Regulatory references, education |

Third-party aggregators (Groww, blogs) are **not** used as data sources.

---

## Known Limitations

1. **Seed corpus**: Initial factual data is curated from HDFC SID/SAI disclosures. Live web scraping depends on HDFC website availability.
2. **PDF factsheets**: Monthly PDF factsheets are referenced by URL but not parsed in this version.
3. **Single AMC**: Currently scoped to HDFC AMC only (5 schemes).
4. **Vercel retrieval**: Cloud deployment uses keyword search instead of semantic FAISS (serverless size limits).
5. **Groq dependency**: LLM responses require a valid Groq API key. Retrieval-only fallback is available when the key is missing.
6. **Free tier limits**: Groq and Vercel free tiers have rate limits; wait and retry if limits are hit.

---

## Disclaimer

```
Facts-only. No investment advice.
```

This assistant provides factual information sourced from official public documents. It does not constitute investment advice, recommendation, or solicitation to buy or sell any mutual fund scheme. AI-generated responses should be verified against cited official sources.

---

## License

Internal project — HDFC Mutual Fund FAQ Assistant prototype.
