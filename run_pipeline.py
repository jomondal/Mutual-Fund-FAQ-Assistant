"""
Pipeline Orchestrator
=====================
Runs all phases sequentially: Data Collection → Processing → Indexing → Ready for UI.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import ensure_directories


def run_full_pipeline(skip_fetch: bool = False) -> None:
    """Execute Phases 1–3 to build the knowledge base."""
    ensure_directories()

    print("\n" + "=" * 60)
    print("  MUTUAL FUND FAQ ASSISTANT - FULL PIPELINE")
    print("  AMC: HDFC Asset Management Company Limited")
    print("=" * 60 + "\n")

    if not skip_fetch:
        from phase_1_data_collection.run import run_phase_1
        run_phase_1()
    else:
        print("[Skip] Phase 1 data collection skipped (using existing data)")

    from phase_2_document_processing.run import run as run_phase_2
    run_phase_2()

    from phase_3_embedding_indexing.run import run as run_phase_3
    run_phase_3()

    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print("  Start the UI: python -m phase_5_ui.app")
    print("  Open: http://127.0.0.1:8000")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    skip = "--skip-fetch" in sys.argv
    run_full_pipeline(skip_fetch=skip)
