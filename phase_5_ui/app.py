"""
Phase 5: FastAPI web application.
Serves the facts-only FAQ assistant UI.
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from config.settings import settings
from phase_1_data_collection.schemes_config import SELECTED_SCHEMES, get_schemes_by_category
from phase_4_rag_pipeline.rag_engine import get_pipeline

app = FastAPI(
    title="HDFC Mutual Fund FAQ Assistant",
    description="Facts-only RAG assistant for HDFC mutual fund schemes",
    version="1.0.0",
)

STATIC_DIR = Path(__file__).parent / "static"
TEMPLATES_DIR = Path(__file__).parent / "templates"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

recent_queries: list[dict] = []


class QueryRequest(BaseModel):
    question: str
    selected_schemes: list[str] = []


class QueryResponse(BaseModel):
    answer: str
    source_url: str
    footer: str
    refused: bool
    classification: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    template_path = TEMPLATES_DIR / "index.html"
    return HTMLResponse(content=template_path.read_text(encoding="utf-8"))


@app.get("/api/schemes")
async def list_schemes(category: str = "all"):
    schemes = get_schemes_by_category(category)
    return {
        "amc": "HDFC Asset Management Company Limited",
        "disclaimer": settings.disclaimer,
        "schemes": [
            {
                "name": s.name,
                "short_name": s.short_name,
                "category": s.category,
                "sub_category": s.sub_category,
                "tags": s.tags,
            }
            for s in schemes
        ],
        "categories": [
            {"id": "all", "label": "All", "count": len(SELECTED_SCHEMES)},
            {
                "id": "equity",
                "label": "Equity",
                "count": len(get_schemes_by_category("equity")),
            },
            {
                "id": "index",
                "label": "Index",
                "count": len(get_schemes_by_category("index")),
            },
        ],
    }


@app.post("/api/query", response_model=QueryResponse)
async def ask_question(body: QueryRequest):
    pipeline = get_pipeline()
    result = pipeline.query(body.question, body.selected_schemes or None)

    recent_queries.insert(
        0,
        {
            "question": body.question[:80],
            "classification": result.get("classification", "factual"),
            "refused": result.get("refused", False),
        },
    )
    if len(recent_queries) > 10:
        recent_queries.pop()

    return QueryResponse(
        answer=result["answer"],
        source_url=result["source_url"],
        footer=result["footer"],
        refused=result.get("refused", False),
        classification=result.get("classification", "factual"),
    )


@app.get("/api/recent")
async def get_recent():
    return {"queries": recent_queries[:8]}


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "disclaimer": settings.disclaimer,
        "model": settings.groq_model,
    }


def run_server():
    import uvicorn

    uvicorn.run(
        "phase_5_ui.app:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )


if __name__ == "__main__":
    run_server()
