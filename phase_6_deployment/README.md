# Phase 6: Deployment — Vercel (Free Tier)

Deploy the Mutual Fund FAQ Assistant to Vercel for a permanent public URL.

## Why keyword retrieval on Vercel?

Vercel serverless functions cannot run heavy ML packages (`sentence-transformers`, `faiss-cpu`, PyTorch) due to size and cold-start limits. On Vercel, the app automatically uses **keyword-based retrieval** from `data/index/chunk_metadata.json`. Local development still uses full semantic search with FAISS.

## Prerequisites

- [Vercel account](https://vercel.com/signup) (free)
- [Groq API key](https://console.groq.com/)
- GitHub repo connected to Vercel

## One-time setup

### 1. Push code to GitHub

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

`VERCEL=1` is set automatically by Vercel.

### 4. Deploy

Click **Deploy**. Vercel assigns a permanent URL like:

`https://mutual-fund-faq-assistant.vercel.app`

Every push to `main` triggers automatic redeployment.

## CLI deploy (optional)

```bash
npm i -g vercel
vercel login
vercel link
vercel env add GROQ_API_KEY
vercel --prod
```

## Free tier limits

- **Serverless timeout:** 10 seconds per request (Hobby)
- **Groq API:** Free tier rate limits apply — footer warns users to wait if limits are hit
- **Recent queries:** Stored in memory per instance (resets on cold start)

## Local vs Vercel

| Feature | Local | Vercel |
|---------|-------|--------|
| Retrieval | FAISS + embeddings | Keyword (BM25-style) |
| LLM | Groq | Groq |
| UI | Full | Full |
| Cost | Free (local) | Free (Hobby) |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 500 on `/api/query` | Check `GROQ_API_KEY` in Vercel env vars |
| Empty answers | Ensure `data/index/chunk_metadata.json` is deployed |
| Timeout | Groq cold start + query; retry after a few seconds |
| Build fails | Check Vercel build logs; Python 3.12 is used by default |
