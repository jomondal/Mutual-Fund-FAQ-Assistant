"""Semantic retrieval for RAG pipeline."""

from config.settings import settings
from phase_3_embedding_indexing.vector_store import RetrievalResult, VectorStore


def _default_store():
    if settings.use_keyword_retrieval:
        from phase_3_embedding_indexing.keyword_store import KeywordStore

        return KeywordStore()
    return VectorStore()


class Retriever:
    """Retrieve relevant chunks for a user query."""

    def __init__(self, vector_store=None):
        self.vector_store = vector_store or _default_store()

    def retrieve(self, query: str, top_k: int | None = None) -> list[RetrievalResult]:
        return self.vector_store.search(query, top_k=top_k)

    def format_context(self, results: list[RetrievalResult]) -> str:
        """Format retrieved chunks into a context string for the LLM."""
        if not results:
            return "No relevant context found."

        parts = []
        for i, r in enumerate(results, 1):
            parts.append(
                f"[Source {i}] Scheme: {r.scheme}\n"
                f"Source URL: {r.source_url}\n"
                f"Content: {r.text}\n"
            )
        return "\n---\n".join(parts)

    def get_primary_source(self, results: list[RetrievalResult]) -> str:
        """Pick the best source URL from retrieved results."""
        if not results:
            return "https://www.hdfcfund.com"
        verified = [r for r in results if r.metadata.get("verified")]
        if verified:
            return verified[0].source_url
        return results[0].source_url
