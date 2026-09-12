# Phase 5: User Interface

Minimal three-column web interface matching the reference design.

## Layout

```
┌──────────────┬──────────────────────────┬──────────────┐
│  Left Panel  │     Main Content         │  Right Panel │
│              │                          │              │
│  AMC Logo    │  Knowledge Engine Hero   │  New Session │
│  Search      │  6 Suggestion Cards      │  Assurance   │
│  Category    │  Chat Messages           │  Recent      │
│  Tabs        │  Query Input Bar         │  Regulatory  │
│  Scheme List │  Disclaimer Footer       │  Footer      │
└──────────────┴──────────────────────────┴──────────────┘
```

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: HTML + CSS + Vanilla JS
- **Styling**: Custom CSS (Inter font, navy/white palette)

## Run

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

## Disclaimer

Displayed prominently in the UI:

> Facts-only. No investment advice.
