# Phase 2: Document Processing

Transforms raw JSON corpus into searchable text chunks.

## Pipeline

```
data/raw/*.json
       │
       ▼
  parser.py ──▶ Structured Document objects
       │
       ▼
  chunker.py ──▶ Overlapping text chunks
       │
       ▼
data/processed/
  ├── documents.json
  └── chunks.json
```

## Document Types Parsed

| Source | Parser Function | Output |
|--------|----------------|--------|
| Seed corpus | `parse_seed_corpus()` | One doc per fact (TER, exit load, etc.) |
| HDFC web pages | `parse_web_pages()` | Page content excerpts |
| AMFI NAV | `parse_amfi_nav()` | NAV records with dates |

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `chunk_size` | 512 | Characters per chunk |
| `chunk_overlap` | 64 | Overlap between chunks |

## Run

```bash
python -m phase_2_document_processing.run
```
