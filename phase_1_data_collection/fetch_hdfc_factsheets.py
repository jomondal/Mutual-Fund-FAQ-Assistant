"""
Fetch scheme facts and disclosures from HDFC AMC official website.
Source: www.hdfcfund.com (official AMC website only)
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

from config.settings import RAW_DATA_DIR, ensure_directories
from phase_1_data_collection.schemes_config import (
    AMC_WEBSITE,
    HDFC_FACTSHEETS_URL,
    HDFC_SAI_URL,
    HDFC_TER_URL,
    SELECTED_SCHEMES,
)


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def fetch_hdfc_page(url: str, client: httpx.Client) -> dict:
    """Fetch and extract text content from an HDFC AMC page."""
    try:
        response = client.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        title = soup.title.get_text(strip=True) if soup.title else url
        paragraphs = [
            _clean_text(p.get_text())
            for p in soup.find_all(["p", "li", "td", "h1", "h2", "h3", "h4"])
            if _clean_text(p.get_text())
        ]
        body_text = "\n".join(paragraphs[:200])

        return {
            "url": url,
            "title": title,
            "content": body_text,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "source_type": "hdfc_amc",
        }
    except Exception as exc:
        return {
            "url": url,
            "title": url,
            "content": "",
            "error": str(exc),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "source_type": "hdfc_amc",
        }


def build_seed_corpus() -> list[dict]:
    """
    Curated factual seed corpus from official HDFC SID/SAI disclosures.
    These facts are verifiable against official AMC statutory documents.
    Last verified against HDFC AMC public disclosures (SID dated Nov 2024).
    """
    return [
        {
            "scheme": "HDFC Mid Cap Fund Direct Plan Growth",
            "category": "Equity - Mid Cap",
            "facts": {
                "investment_objective": (
                    "The scheme seeks to provide long-term capital appreciation "
                    "by investing predominantly in equity and equity related "
                    "securities of mid-cap companies."
                ),
                "benchmark": "NIFTY Midcap 150 Total Return Index",
                "riskometer": "Very High",
                "exit_load": "1% if redeemed/switched out within 1 year from date of allotment; Nil thereafter",
                "minimum_sip": "Rs. 100",
                "minimum_lumpsum": "Rs. 100",
                "expense_ratio_direct": "0.75% (as per latest TER disclosure on HDFC AMC website)",
                "fund_manager": "Chirag Setalvad",
                "lock_in_period": "Nil",
            },
            "source_url": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-mid-cap-fund/direct",
            "source_type": "hdfc_amc",
        },
        {
            "scheme": "HDFC Small Cap Fund Direct Plan Growth",
            "category": "Equity - Small Cap",
            "facts": {
                "investment_objective": (
                    "The scheme seeks to provide long-term capital appreciation "
                    "by investing predominantly in equity and equity related "
                    "securities of small-cap companies."
                ),
                "benchmark": "NIFTY Smallcap 250 Total Return Index",
                "riskometer": "Very High",
                "exit_load": "1% if redeemed/switched out within 1 year from date of allotment; Nil thereafter",
                "minimum_sip": "Rs. 100",
                "minimum_lumpsum": "Rs. 100",
                "expense_ratio_direct": "0.68% (as per latest TER disclosure on HDFC AMC website)",
                "fund_manager": "Chirag Setalvad",
                "lock_in_period": "Nil",
            },
            "source_url": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-small-cap-fund/direct",
            "source_type": "hdfc_amc",
        },
        {
            "scheme": "HDFC Gold ETF Fund of Fund Direct Plan Growth",
            "category": "Index, ETFs & FoF - Gold FoF",
            "facts": {
                "investment_objective": (
                    "The scheme seeks to generate returns by investing in units "
                    "of HDFC Gold Exchange Traded Fund (ETF), which invests "
                    "in physical gold."
                ),
                "benchmark": "Domestic Price of Gold",
                "riskometer": "Moderately High",
                "exit_load": "1% if redeemed/switched out within 15 days from date of allotment; Nil thereafter",
                "minimum_sip": "Rs. 100",
                "minimum_lumpsum": "Rs. 100",
                "expense_ratio_direct": "0.18% (as per latest TER disclosure on HDFC AMC website)",
                "fund_manager": "Krishan Daga",
                "lock_in_period": "Nil",
            },
            "source_url": (
                "https://www.hdfcfund.com/explore/mutual-funds/"
                "hdfc-gold-etf-fund-of-fund/direct"
            ),
            "source_type": "hdfc_amc",
        },
        {
            "scheme": "HDFC Large Cap Fund Direct Plan Growth",
            "category": "Equity - Large Cap",
            "facts": {
                "investment_objective": (
                    "The scheme seeks to provide long-term capital appreciation "
                    "by investing predominantly in equity and equity related "
                    "securities of large-cap companies."
                ),
                "benchmark": "NIFTY 100 Total Return Index",
                "riskometer": "Very High",
                "exit_load": "1% if redeemed/switched out within 1 year from date of allotment; Nil thereafter",
                "minimum_sip": "Rs. 100",
                "minimum_lumpsum": "Rs. 100",
                "expense_ratio_direct": "0.97% (as per latest TER disclosure on HDFC AMC website)",
                "fund_manager": "Roshi Jain",
                "lock_in_period": "Nil",
            },
            "source_url": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct",
            "source_type": "hdfc_amc",
        },
        {
            "scheme": "HDFC ELSS Tax Saver Fund Direct Plan Growth",
            "category": "Equity - ELSS",
            "facts": {
                "investment_objective": (
                    "The scheme seeks to generate long-term capital appreciation "
                    "from a diversified portfolio of predominantly equity and "
                    "equity related securities, with tax benefit under Section 80C."
                ),
                "benchmark": "NIFTY 500 Total Return Index",
                "riskometer": "Very High",
                "exit_load": "Nil",
                "minimum_sip": "Rs. 500",
                "minimum_lumpsum": "Rs. 500",
                "expense_ratio_direct": "0.97% (as per latest TER disclosure on HDFC AMC website)",
                "fund_manager": "Roshi Jain",
                "lock_in_period": "3 years from date of allotment (mandatory lock-in under Section 80C)",
            },
            "source_url": (
                "https://www.hdfcfund.com/explore/mutual-funds/"
                "hdfc-elss-tax-saver/direct"
            ),
            "source_type": "hdfc_amc",
        },
        {
            "scheme": "General - HDFC AMC",
            "category": "Regulatory & Process",
            "facts": {
                "statement_download": (
                    "Investors can download account statements, capital gains statements, "
                    "and transaction reports via HDFC MF Online Services at "
                    "https://www.hdfcfund.com/investor-services or through the "
                    "CAMS/KFintech investor portal linked from the AMC website."
                ),
                "registrar": "Computer Age Management Services (CAMS) and KFin Technologies",
                "regulatory_body": "Registered with SEBI; member of AMFI",
                "ter_disclosure_url": HDFC_TER_URL,
                "factsheet_url": HDFC_FACTSHEETS_URL,
                "sai_url": HDFC_SAI_URL,
                "sebi_investor_education": "https://investor.sebi.gov.in/",
                "amfi_investor_education": "https://www.amfiindia.com/investor-corner/knowledge-center.html",
            },
            "source_url": AMC_WEBSITE,
            "source_type": "hdfc_amc",
        },
    ]


def fetch_hdfc_data(output_dir: Path | None = None) -> Path:
    """Fetch HDFC AMC pages and merge with seed corpus."""
    ensure_directories()
    output_dir = output_dir or RAW_DATA_DIR
    documents: list[dict] = []

    urls_to_fetch = {
        HDFC_FACTSHEETS_URL: "factsheets_index",
        HDFC_TER_URL: "ter_disclosure",
        HDFC_SAI_URL: "scheme_information_document",
        AMC_WEBSITE: "amc_homepage",
    }
    for scheme in SELECTED_SCHEMES:
        urls_to_fetch[scheme.hdfc_product_url] = scheme.short_name

    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        for url, label in urls_to_fetch.items():
            page_data = fetch_hdfc_page(url, client)
            page_data["label"] = label
            documents.append(page_data)

    seed = build_seed_corpus()
    output_path = output_dir / "hdfc_corpus.json"
    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "amc": "HDFC Asset Management Company Limited",
        "official_source": AMC_WEBSITE,
        "web_pages": documents,
        "seed_corpus": seed,
    }
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[Phase 1] HDFC corpus saved: {output_path}")
    return output_path


if __name__ == "__main__":
    fetch_hdfc_data()
