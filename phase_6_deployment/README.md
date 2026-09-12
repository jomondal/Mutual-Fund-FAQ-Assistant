# Phase 6: Deployment — Vercel (Free Tier)

The Mutual Fund FAQ Assistant is deployed permanently on Vercel.

## Live URLs

| URL | Purpose |
|-----|---------|
| [https://hdfc-faq-assistant.vercel.app](https://hdfc-faq-assistant.vercel.app) | Primary production URL |
| [https://mutual-fund-faq-assistant-ebon.vercel.app](https://mutual-fund-faq-assistant-ebon.vercel.app) | Alternate production URL |
| [https://hdfc-faq-assistant.vercel.app/api/health](https://hdfc-faq-assistant.vercel.app/api/health) | Health check endpoint |

**GitHub repository:** [github.com/jomondal/Mutual-Fund-FAQ-Assistant](https://github.com/jomondal/Mutual-Fund-FAQ-Assistant)

---

## Why keyword retrieval on Vercel?

Vercel serverless functions cannot run heavy ML packages (`sentence-transformers`, `faiss-cpu`, PyTorch) due to bundle size and cold-start limits. On Vercel, the app automatically uses **keyword-based retrieval** from `data/index/chunk_metadata.json`. Local development still uses full semantic search with FAISS.

---

## Deployment Files

| File | Purpose |
|------|---------|
| `api/index.py` | Vercel serverless entrypoint (exports FastAPI `app`) |
| `vercel.json` | Install command, function timeout |
| `requirements-vercel.txt` | Lightweight Python dependencies |
| `pyproject.toml` | Vercel entrypoint configuration |
| `.python-version` | Python 3.12 |
| `.vercelignore` | Excludes venv, raw data, secrets |
| `data/index/chunk_metadata.json` | Knowledge base for cloud retrieval |

---

## Prerequisites

- [Vercel account](https://vercel.com/signup) (free)
- [Groq API key](https://console.groq.com/)
- GitHub repo: `jomondal/Mutual-Fund-FAQ-Assistant`

---

## One-Time Setup

### 1. Clone and push to GitHub

```bash
git clone https://github.com/jomondal/Mutual-Fund-FAQ-Assistant.git
cd Mutual-Fund-FAQ-Assistant
```

Ensure `data/index/chunk_metadata.json` is committed (required for retrieval on Vercel).

### 2. Import project on Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import `jomondal/Mutual-Fund-FAQ-Assistant`
3. Framework Preset: **Other**
4. Root Directory: `.` (project root)
5. Build settings are read from `vercel.json` automatically

### 3. Add environment variables

In Vercel → Project → Settings → Environment Variables:

| Name | Value |
|------|-------|
| `GROQ_API_KEY` | Your Groq API key |
| `GROQ_MODEL` | `openai/gpt-oss-120b` (optional) |

`VERCEL=1` is set automatically by Vercel (enables keyword retrieval).

### 4. Deploy

Click **Deploy**. Production URL:

**https://hdfc-faq-assistant.vercel.app**

Every push to `main` can trigger automatic redeployment when Git is connected.

---

## CLI Deploy (Optional)

```bash
npm i -g vercel
vercel login
vercel link
vercel env add GROQ_API_KEY
vercel --prod
```

---

## Local vs Vercel

| Feature | Local | Vercel |
|---------|-------|--------|
| Retrieval | FAISS + embeddings | Keyword (BM25-style) |
| LLM | Groq | Groq |
| UI | Full | Full |
| Recent queries | In-memory session | In-memory (resets on cold start) |
| Cost | Free (local) | Free (Hobby) |

---

## Free Tier Limits

- **Serverless timeout:** 10 seconds per request (Hobby)
- **Groq API:** Free tier rate limits apply — UI footer warns users to wait if limits are hit
- **Bundle size:** Heavy ML packages excluded from Vercel build

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 500 on `/api/query` | Check `GROQ_API_KEY` in Vercel env vars |
| Empty answers | Ensure `data/index/chunk_metadata.json` is deployed |
| Timeout | Groq cold start + query; retry after a few seconds |
| Build fails | Check Vercel build logs; Python 3.12 is used by default |
| Login wall on URL | Disable Vercel SSO deployment protection in project settings |
