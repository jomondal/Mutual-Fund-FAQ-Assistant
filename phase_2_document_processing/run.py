"""Phase 2 orchestrator."""

from phase_2_document_processing.parser import run_phase_2
from phase_2_document_processing.chunker import run_chunking


def run() -> None:
    print("=" * 60)
    print("PHASE 2: Document Processing")
    print("=" * 60)
    run_phase_2()
    run_chunking()
    print("[Phase 2] Complete.")


if __name__ == "__main__":
    run()
