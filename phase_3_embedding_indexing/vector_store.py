"""
FAISS vector store for semantic retrieval.
"""

import json
from pathlib import Path

import faiss
import numpy as np

from config.settings import INDEX_DIR, settings
from phase_3_embedding_indexing.embedder import Embedder
from phase_3_embedding_indexing.retrieval_types import RetrievalResult


class VectorStore:
    """FAISS-backed vector store for chunk retrieval."""

    def __init__(
        self,
        index_dir: Path | None = None,
        embedder: Embedder | None = None,
    ):
        self.index_dir = index_dir or INDEX_DIR
        self.embedder = embedder or Embedder()
        self._index: faiss.Index | None = None
        self._metadata: list[dict] = []

    def load(self) -> None:
        index_path = self.index_dir / "faiss.index"
        metadata_path = self.index_dir / "chunk_metadata.json"

        if not index_path.exists() or not metadata_path.exists():
            raise FileNotFoundError(
                f"Index not found in {self.index_dir}. Run Phase 3 first."
            )

        self._index = faiss.read_index(str(index_path))
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
        self._metadata = data.get("chunks", [])

    @property
    def is_loaded(self) -> bool:
        return self._index is not None and len(self._metadata) > 0

    def search(self, query: str, top_k: int | None = None) -> list[RetrievalResult]:
        """Retrieve top-k most similar chunks for a query."""
        if not self.is_loaded:
            self.load()

        top_k = top_k or settings.top_k
        query_embedding = self.embedder.embed_query(query).reshape(1, -1).astype(np.float32)
        faiss.normalize_L2(query_embedding)

        scores, indices = self._index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self._metadata):
                continue
            chunk = self._metadata[idx]
            results.append(
                RetrievalResult(
                    chunk_id=chunk["chunk_id"],
                    text=chunk["text"],
                    scheme=chunk.get("scheme", ""),
                    source_url=chunk.get("source_url", ""),
                    source_type=chunk.get("source_type", ""),
                    score=float(score),
                    metadata=chunk.get("metadata", {}),
                )
            )
        return results
