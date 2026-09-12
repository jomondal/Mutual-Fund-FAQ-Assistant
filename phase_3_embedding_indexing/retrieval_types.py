"""Shared retrieval types (no ML dependencies)."""

from dataclasses import dataclass


@dataclass
class RetrievalResult:
    """A retrieved chunk with similarity score."""

    chunk_id: str
    text: str
    scheme: str
    source_url: str
    source_type: str
    score: float
    metadata: dict
