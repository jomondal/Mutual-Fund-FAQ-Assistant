"""Central configuration for the Mutual Fund FAQ Assistant."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Phase directories
PHASE_1_DIR = PROJECT_ROOT / "phase_1_data_collection"
PHASE_2_DIR = PROJECT_ROOT / "phase_2_document_processing"
PHASE_3_DIR = PROJECT_ROOT / "phase_3_embedding_indexing"
PHASE_4_DIR = PROJECT_ROOT / "phase_4_rag_pipeline"
PHASE_5_DIR = PROJECT_ROOT / "phase_5_ui"

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
INDEX_DIR = DATA_DIR / "index"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-120b"
    embedding_model: str = "all-MiniLM-L6-v2"
    host: str = "127.0.0.1"
    port: int = 8000

    # RAG parameters
    top_k: int = 5
    chunk_size: int = 512
    chunk_overlap: int = 64
    max_response_sentences: int = 3

    # Compliance
    disclaimer: str = "Facts-only. No investment advice."
    amfi_education_url: str = "https://www.amfiindia.com/investor-corner/knowledge-center.html"
    sebi_education_url: str = "https://investor.sebi.gov.in/"

    # Serverless deployment (Vercel) uses keyword retrieval instead of FAISS/embeddings
    use_keyword_retrieval: bool = os.getenv("VERCEL") == "1"


settings = Settings()


def ensure_directories() -> None:
    """Create all required data directories."""
    for directory in (RAW_DATA_DIR, PROCESSED_DATA_DIR, INDEX_DIR):
        directory.mkdir(parents=True, exist_ok=True)
