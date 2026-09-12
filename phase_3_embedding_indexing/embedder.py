"""
Phase 3: Embedding generation using sentence-transformers.
"""

import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from config.settings import PROCESSED_DATA_DIR, INDEX_DIR, settings, ensure_directories


class Embedder:
    """Generate dense vector embeddings for text chunks."""

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.embedding_model
        self._model: SentenceTransformer | None = None

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            print(f"[Phase 3] Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed_texts(self, texts: list[str]) -> np.ndarray:
        """Embed a list of texts, returning (N, dim) float32 array."""
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        return embeddings.astype(np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        """Embed a single query string."""
        return self.embed_texts([query])[0]


def build_index(
    chunks_path: Path | None = None,
    output_dir: Path | None = None,
) -> tuple[Path, Path]:
    """Generate embeddings and save FAISS-compatible index files."""
    ensure_directories()
    chunks_path = chunks_path or PROCESSED_DATA_DIR / "chunks.json"
    output_dir = output_dir or INDEX_DIR

    data = json.loads(chunks_path.read_text(encoding="utf-8"))
    chunks = data.get("chunks", [])
    if not chunks:
        raise ValueError("No chunks found. Run Phase 2 first.")

    texts = [c["text"] for c in chunks]
    embedder = Embedder()
    embeddings = embedder.embed_texts(texts)

    import faiss

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    index_path = output_dir / "faiss.index"
    faiss.write_index(index, str(index_path))

    metadata_path = output_dir / "chunk_metadata.json"
    metadata = {
        "embedding_model": embedder.model_name,
        "dimension": dimension,
        "chunk_count": len(chunks),
        "chunks": chunks,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[Phase 3] Index built: {len(chunks)} vectors, dim={dimension}")
    print(f"[Phase 3] Saved: {index_path}, {metadata_path}")
    return index_path, metadata_path


if __name__ == "__main__":
    build_index()
