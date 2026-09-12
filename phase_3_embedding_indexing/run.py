"""Phase 3 orchestrator."""

from phase_3_embedding_indexing.embedder import build_index


def run() -> None:
    print("=" * 60)
    print("PHASE 3: Embedding & Indexing")
    print("=" * 60)
    build_index()
    print("[Phase 3] Complete.")


if __name__ == "__main__":
    run()
