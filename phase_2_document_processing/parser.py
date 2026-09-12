"""
Phase 2: Document Processing
============================
Parses raw JSON corpus into structured document chunks with metadata.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from config.settings import PROCESSED_DATA_DIR, RAW_DATA_DIR, ensure_directories


@dataclass
class Document:
    """A single processable document unit."""

    doc_id: str
    text: str
    scheme: str
    category: str
    source_url: str
    source_type: str
    metadata: dict[str, Any] = field(default_factory=dict)


def load_raw_corpus(raw_dir: Path | None = None) -> list[dict]:
    """Load all raw JSON files from Phase 1."""
    raw_dir = raw_dir or RAW_DATA_DIR
    documents = []

    hdfc_path = raw_dir / "hdfc_corpus.json"
    if hdfc_path.exists():
        documents.append(json.loads(hdfc_path.read_text(encoding="utf-8")))

    amfi_path = raw_dir / "amfi_nav_data.json"
    if amfi_path.exists():
        documents.append(json.loads(amfi_path.read_text(encoding="utf-8")))

    return documents


def parse_seed_corpus(hdfc_data: dict) -> list[Document]:
    """Convert seed corpus facts into searchable documents."""
    docs = []
    for idx, entry in enumerate(hdfc_data.get("seed_corpus", [])):
        scheme = entry.get("scheme", "Unknown")
        category = entry.get("category", "")
        source_url = entry.get("source_url", "")
        source_type = entry.get("source_type", "hdfc_amc")

        facts = entry.get("facts", {})
        for fact_key, fact_value in facts.items():
            text = f"Scheme: {scheme}. {fact_key.replace('_', ' ').title()}: {fact_value}"
            docs.append(
                Document(
                    doc_id=f"seed_{idx}_{fact_key}",
                    text=text,
                    scheme=scheme,
                    category=category,
                    source_url=source_url,
                    source_type=source_type,
                    metadata={"fact_type": fact_key, "verified": True},
                )
            )
    return docs


def parse_web_pages(hdfc_data: dict) -> list[Document]:
    """Convert fetched web page content into documents."""
    docs = []
    for idx, page in enumerate(hdfc_data.get("web_pages", [])):
        content = page.get("content", "")
        if not content or len(content) < 50:
            continue
        docs.append(
            Document(
                doc_id=f"web_{idx}",
                text=content[:4000],
                scheme=page.get("label", "General"),
                category="Web Content",
                source_url=page.get("url", ""),
                source_type=page.get("source_type", "hdfc_amc"),
                metadata={"title": page.get("title", "")},
            )
        )
    return docs


def parse_amfi_nav(amfi_data: dict) -> list[Document]:
    """Convert AMFI NAV records into documents."""
    docs = []
    for idx, scheme in enumerate(amfi_data.get("schemes", [])):
        text = (
            f"Scheme: {scheme.get('scheme_name', '')}. "
            f"NAV: Rs. {scheme.get('nav', 'N/A')}. "
            f"NAV Date: {scheme.get('date', 'N/A')}. "
            f"AMC: {scheme.get('amc', '')}. "
            f"AMFI Scheme Code: {scheme.get('scheme_code', '')}."
        )
        docs.append(
            Document(
                doc_id=f"amfi_{idx}",
                text=text,
                scheme=scheme.get("scheme_name", ""),
                category="NAV Data",
                source_url=scheme.get("source", "https://www.amfiindia.com"),
                source_type="amfi_nav",
                metadata={
                    "nav": scheme.get("nav"),
                    "nav_date": scheme.get("date"),
                    "amfi_code": scheme.get("scheme_code"),
                },
            )
        )
    return docs


def process_all(raw_dir: Path | None = None) -> list[Document]:
    """Run full document processing pipeline."""
    raw_corpus = load_raw_corpus(raw_dir)
    all_docs: list[Document] = []

    for data in raw_corpus:
        if "seed_corpus" in data:
            all_docs.extend(parse_seed_corpus(data))
            all_docs.extend(parse_web_pages(data))
        if "schemes" in data and "fetched_at" in data:
            all_docs.extend(parse_amfi_nav(data))

    return all_docs


def save_processed_documents(docs: list[Document], output_dir: Path | None = None) -> Path:
    """Save processed documents to JSON."""
    ensure_directories()
    output_dir = output_dir or PROCESSED_DATA_DIR
    output_path = output_dir / "documents.json"

    payload = {
        "processed_at": datetime.utcnow().isoformat(),
        "document_count": len(docs),
        "documents": [
            {
                "doc_id": d.doc_id,
                "text": d.text,
                "scheme": d.scheme,
                "category": d.category,
                "source_url": d.source_url,
                "source_type": d.source_type,
                "metadata": d.metadata,
            }
            for d in docs
        ],
    }
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[Phase 2] Processed {len(docs)} documents -> {output_path}")
    return output_path


def run_phase_2(raw_dir: Path | None = None) -> Path:
    docs = process_all(raw_dir)
    return save_processed_documents(docs)


if __name__ == "__main__":
    run_phase_2()
