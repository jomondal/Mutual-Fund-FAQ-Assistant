# Phase 5: User Interface

Three-column web interface for the Mutual Fund FAQ Assistant.

**Live demo:** [https://hdfc-faq-assistant.vercel.app](https://hdfc-faq-assistant.vercel.app)

## Layout

```
┌──────────────┬──────────────────────────┬──────────────┐
│  Left Panel  │     Main Content         │  Right Panel │
│              │                          │              │
│  Home + AMC  │  FAQ Knowledge Assistant │  New Session │
│  Search      │  Hero + Suggestions      │  Assurance   │
│  Category    │  Chat Messages           │  Recent      │
│  Tabs        │  Query Input Bar         │  Inquiries   │
│  Scheme List │  Disclaimer Footer       │              │
└──────────────┴──────────────────────────┴──────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI |
| Frontend | HTML + CSS + Vanilla JS |
| Font | Inter |
| Styling | Custom CSS (navy/white palette, responsive) |

## Run Locally

```bash
python -m phase_5_ui.app
```

Open http://127.0.0.1:8000

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Main UI |
| GET | `/api/schemes` | List schemes with categories |
| POST | `/api/query` | Submit a factual question |
| GET | `/api/recent` | Recent query history |
| GET | `/api/health` | Health check |

## UI Features

- Scheme filter by category (All / Equity / Index)
- Multi-select scheme scope for queries
- Suggestion cards with sample factual questions
- Refusal handling with classification labels in recent history
- Facts-only disclaimer in input bar and footer
- Responsive layout with mobile slide-out sidebars

## Disclaimer

Displayed in the UI:

> Facts-only. No investment advice.

Additional footer: AI generated responses — verify with cited sources.
