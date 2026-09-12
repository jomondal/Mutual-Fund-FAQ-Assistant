"""Keyword-based retrieval for serverless deployment (no ML dependencies)."""

import json
import math
import re
from pathlib import Path

from config.settings import INDEX_DIR, settings
from phase_3_embedding_indexing.vector_store import RetrievalResult


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class KeywordStore:
    """Lightweight BM25-style retrieval using chunk metadata only."""

    def __init__(self, index_dir: Path | None = None):
        self.index_dir = index_dir or INDEX_DIR
        self._metadata: list[dict] = []
        self._doc_freq: dict[str, int] = {}
        self._avg_doc_len = 1.0

    def load(self) -> None:
        metadata_path = self.index_dir / "chunk_metadata.json"
        if not metadata_path.exists():
            raise FileNotFoundError(
                f"Index metadata not found in {self.index_dir}. Run Phase 3 first."
            )

        data = json.loads(metadata_path.read_text(encoding="utf-8"))
        self._metadata = data.get("chunks", [])
        self._build_idf()

    def _build_idf(self) -> None:
        n = len(self._metadata)
        if n == 0:
            return

        df: dict[str, int] = {}
        total_len = 0
        for chunk in self._metadata:
            tokens = set(_tokenize(chunk.get("text", "")))
            total_len += len(tokens)
            for token in tokens:
                df[token] = df.get(token, 0) + 1

        self._doc_freq = df
        self._avg_doc_len = total_len / n if n else 1.0

    @property
    def is_loaded(self) -> bool:
        return len(self._metadata) > 0

    def search(self, query: str, top_k: int | None = None) -> list[RetrievalResult]:
        if not self.is_loaded:
            self.load()

        top_k = top_k or settings.top_k
        query_tokens = _tokenize(query)
        if not query_tokens:
            return []

        k1, b = 1.5, 0.75
        n = len(self._metadata)
        scored: list[tuple[float, int]] = []

        for idx, chunk in enumerate(self._metadata):
            text = chunk.get("text", "")
            doc_tokens = _tokenize(text)
            doc_len = len(doc_tokens) or 1
            tf_map: dict[str, int] = {}
            for token in doc_tokens:
                tf_map[token] = tf_map.get(token, 0) + 1

            score = 0.0
            for term in query_tokens:
                if term not in tf_map:
                    continue
                df = self._doc_freq.get(term, 0)
                idf = math.log((n - df + 0.5) / (df + 0.5) + 1)
                tf = tf_map[term]
                num = tf * (k1 + 1)
                den = tf + k1 * (1 - b + b * doc_len / self._avg_doc_len)
                score += idf * (num / den)

            if score > 0:
                scored.append((score, idx))

        scored.sort(key=lambda x: x[0], reverse=True)
        results: list[RetrievalResult] = []
        for score, idx in scored[:top_k]:
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
