"""
Phase 1 orchestrator: run all data collection tasks.
"""

from phase_1_data_collection.fetch_amfi_data import fetch_amfi_nav
from phase_1_data_collection.fetch_hdfc_factsheets import fetch_hdfc_data


def run_phase_1() -> None:
    print("=" * 60)
    print("PHASE 1: Data Collection")
    print("Sources: HDFC AMC, AMFI (official public sources only)")
    print("=" * 60)
    fetch_amfi_nav()
    fetch_hdfc_data()
    print("[Phase 1] Complete.")


if __name__ == "__main__":
    run_phase_1()
