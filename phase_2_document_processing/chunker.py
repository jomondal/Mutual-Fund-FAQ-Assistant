"""
Text chunking for RAG retrieval.
Splits long documents into overlapping chunks while preserving metadata.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from config.settings import PROCESSED_DATA_DIR, settings, ensure_directories


@dataclass
class Chunk:
    """A text chunk ready for embedding."""

    chunk_id: str
    text: str
    doc_id: str
    scheme: str
    source_url: str
    source_type: str
    metadata: dict[str, Any] = field(default_factory=dict)


def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping chunks by character count."""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks


def chunk_documents(
    documents_path: Path | None = None,
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """Load processed documents and split into chunks."""
    documents_path = documents_path or PROCESSED_DATA_DIR / "documents.json"
    chunk_size = chunk_size or settings.chunk_size
    overlap = overlap or settings.chunk_overlap

    data = json.loads(documents_path.read_text(encoding="utf-8"))
    all_chunks: list[Chunk] = []

    for doc in data.get("documents", []):
        text_parts = split_text(doc["text"], chunk_size, overlap)
        for i, part in enumerate(text_parts):
            all_chunks.append(
                Chunk(
                    chunk_id=f"{doc['doc_id']}_chunk_{i}",
                    text=part,
                    doc_id=doc["doc_id"],
                    scheme=doc.get("scheme", ""),
                    source_url=doc.get("source_url", ""),
                    source_type=doc.get("source_type", ""),
                    metadata=doc.get("metadata", {}),
                )
            )

    return all_chunks


def save_chunks(chunks: list[Chunk], output_dir: Path | None = None) -> Path:
    """Persist chunks to JSON."""
    ensure_directories()
    output_dir = output_dir or PROCESSED_DATA_DIR
    output_path = output_dir / "chunks.json"

    payload = {
        "chunk_count": len(chunks),
        "chunk_size": settings.chunk_size,
        "chunk_overlap": settings.chunk_overlap,
        "chunks": [
            {
                "chunk_id": c.chunk_id,
                "text": c.text,
                "doc_id": c.doc_id,
                "scheme": c.scheme,
                "source_url": c.source_url,
                "source_type": c.source_type,
                "metadata": c.metadata,
            }
            for c in chunks
        ],
    }
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[Phase 2] Created {len(chunks)} chunks -> {output_path}")
    return output_path


def run_chunking(documents_path: Path | None = None) -> Path:
    chunks = chunk_documents(documents_path)
    return save_chunks(chunks)


if __name__ == "__main__":
    run_chunking()
