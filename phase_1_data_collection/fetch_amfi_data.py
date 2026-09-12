"""
Fetch scheme data from AMFI official NAV API.
Source: https://www.amfiindia.com/spages/NAVAll.txt
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import httpx

from config.settings import RAW_DATA_DIR, ensure_directories
from phase_1_data_collection.schemes_config import SELECTED_SCHEMES

AMFI_NAV_URL = "https://www.amfiindia.com/spages/NAVAll.txt"


def parse_amfi_nav(text: str, target_codes: set[str]) -> list[dict]:
    """Parse AMFI NAVAll.txt format and extract matching schemes."""
    results = []
    current_amc = ""

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        if ";" not in line:
            current_amc = line
            continue

        parts = [p.strip() for p in line.split(";")]
        if len(parts) < 6:
            continue

        scheme_code = parts[0]
        if scheme_code not in target_codes:
            continue

        results.append(
            {
                "scheme_code": scheme_code,
                "isin_div_payout": parts[1],
                "isin_div_reinvest": parts[2],
                "scheme_name": parts[3],
                "nav": parts[4],
                "date": parts[5],
                "amc": current_amc,
                "source": AMFI_NAV_URL,
                "source_type": "amfi_nav",
            }
        )

    return results


def fetch_amfi_nav(output_dir: Path | None = None) -> Path:
    """Download and parse AMFI NAV data for selected schemes."""
    ensure_directories()
    output_dir = output_dir or RAW_DATA_DIR
    target_codes = {s.amfi_code for s in SELECTED_SCHEMES}

    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        response = client.get(AMFI_NAV_URL)
        response.raise_for_status()
        nav_text = response.text

    parsed = parse_amfi_nav(nav_text, target_codes)
    output_path = output_dir / "amfi_nav_data.json"
    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": AMFI_NAV_URL,
        "schemes": parsed,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[Phase 1] AMFI NAV data saved: {output_path} ({len(parsed)} schemes)")
    return output_path


if __name__ == "__main__":
    fetch_amfi_nav()
