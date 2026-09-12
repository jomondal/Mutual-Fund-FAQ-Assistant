"""
Phase 4: RAG Pipeline
=====================
End-to-end retrieval-augmented generation with Groq LLM.
"""

import re
from datetime import datetime, timezone

from config.settings import settings
from phase_4_rag_pipeline.groq_llm import GroqLLM
from phase_4_rag_pipeline.prompt_templates import FACT_QUERY_PROMPT, SYSTEM_PROMPT
from phase_4_rag_pipeline.refusal_handler import (
    QueryClassification,
    classify_query,
    get_refusal_response,
)
from phase_4_rag_pipeline.retriever import Retriever

_DISCLAIMER_RE = re.compile(r"Facts-only\.?\s*No investment advice\.?", re.IGNORECASE)
_LAST_UPDATED_RE = re.compile(r"Last updated from sources:.*", re.IGNORECASE | re.MULTILINE)
_SOURCE_LABEL_RE = re.compile(r"[\[【]\s*Source\s*\d+\s*[\]】]", re.IGNORECASE)
_INLINE_URL_RE = re.compile(r"https?://\S+")


class RAGPipeline:
    """Facts-only RAG pipeline for mutual fund FAQ."""

    def __init__(
        self,
        retriever: Retriever | None = None,
        llm: GroqLLM | None = None,
    ):
        self.retriever = retriever or Retriever()
        self.llm = llm or GroqLLM()
        self.last_updated = datetime.now(timezone.utc).strftime("%d %b %Y")

    def _clean_answer(self, answer: str) -> str:
        """Remove disclaimer, footer, source labels, and inline URLs from the answer body."""
        text = _DISCLAIMER_RE.sub("", answer)
        text = _LAST_UPDATED_RE.sub("", text)
        text = _SOURCE_LABEL_RE.sub("", text)
        text = _INLINE_URL_RE.sub("", text)
        text = re.sub(r"[ \t]{2,}", " ", text)
        text = re.sub(r" ?\. ?", ". ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def query(self, question: str, selected_schemes: list[str] | None = None) -> dict:
        """
        Process a user query and return a structured response.

        Returns:
            dict with keys: answer, source_url, footer, refused, classification
        """
        question = question.strip()
        if not question:
            return self._empty_response()

        classification = classify_query(question)
        if classification != QueryClassification.FACTUAL:
            return get_refusal_response(question, classification, self.last_updated)

        search_query = question
        if selected_schemes:
            search_query = f"{question} {' '.join(selected_schemes)}"

        results = self.retriever.retrieve(search_query)
        context = self.retriever.format_context(results)
        source_url = self.retriever.get_primary_source(results)

        try:
            answer = self._clean_answer(
                self.llm.generate(SYSTEM_PROMPT, FACT_QUERY_PROMPT.format(context=context, question=question))
            )
        except ValueError as exc:
            return self._fallback_response(results, str(exc))

        return {
            "answer": answer,
            "source_url": source_url,
            "footer": f"Last updated from sources: {self.last_updated}",
            "refused": False,
            "classification": classification,
            "retrieved_chunks": len(results),
        }

    def _empty_response(self) -> dict:
        return {
            "answer": "Please enter a factual question about HDFC mutual fund schemes.",
            "source_url": "https://www.hdfcfund.com",
            "footer": f"Last updated from sources: {self.last_updated}",
            "refused": False,
            "classification": "empty",
            "retrieved_chunks": 0,
        }

    def _fallback_response(self, results, error: str) -> dict:
        """Fallback when Groq API is unavailable — use retrieved context directly."""
        if results:
            best = results[0]
            return {
                "answer": f"Based on official sources: {best.text[:400]}",
                "source_url": best.source_url,
                "footer": f"Last updated from sources: {self.last_updated}",
                "refused": False,
                "classification": QueryClassification.FACTUAL,
                "retrieved_chunks": len(results),
                "note": f"LLM unavailable ({error}). Showing retrieved context.",
            }
        return {
            "answer": (
                "Unable to generate a response. Please set GROQ_API_KEY in your .env file "
                "and ensure the knowledge index is built."
            ),
            "source_url": "https://www.hdfcfund.com",
            "footer": f"Last updated from sources: {self.last_updated}",
            "refused": False,
            "classification": "error",
            "retrieved_chunks": 0,
        }


_pipeline: RAGPipeline | None = None


def get_pipeline() -> RAGPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = RAGPipeline()
    return _pipeline
