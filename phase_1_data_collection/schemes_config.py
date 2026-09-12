"""
Phase 1: Data Collection
========================
Collects mutual fund scheme data from official public sources only:
- HDFC AMC (www.hdfcfund.com)
- AMFI (www.amfiindia.com)
- SEBI (investor.sebi.gov.in)

Groww links are reference-only for product context; they are NOT used as data sources.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MutualFundScheme:
    """Metadata for a single mutual fund scheme."""

    name: str
    short_name: str
    category: str
    sub_category: str
    amfi_code: str
    groww_reference_url: str  # Reference only, not a data source
    hdfc_product_url: str
    hdfc_factsheet_url: str
    amfi_scheme_url: str
    sebi_sid_url: Optional[str] = None
    tags: list[str] = field(default_factory=list)


AMC_NAME = "HDFC Asset Management Company Limited"
AMC_SHORT = "HDFC MF"
AMC_WEBSITE = "https://www.hdfcfund.com"
AMFI_BASE = "https://www.amfiindia.com"
SEBI_INVESTOR = "https://investor.sebi.gov.in"

# Official statutory disclosure URLs (HDFC AMC)
HDFC_TER_URL = (
    "https://www.hdfcfund.com/statutory-disclosure/"
    "total-expense-ratio-of-mutual-fund-schemes/reports"
)
HDFC_FACTSHEETS_URL = "https://www.hdfcfund.com/investor-services/factsheets"
HDFC_MONTHLY_PORTFOLIO_URL = (
    "https://www.hdfcfund.com/statutory-disclosure/portfolio/monthly-portfolio"
)
HDFC_SAI_URL = "https://www.hdfcfund.com/statutory-disclosure/scheme-information-document"

SELECTED_SCHEMES: list[MutualFundScheme] = [
    MutualFundScheme(
        name="HDFC Mid Cap Fund Direct Plan Growth",
        short_name="Mid Cap Fund",
        category="Equity",
        sub_category="Mid Cap",
        amfi_code="118989",
        groww_reference_url="https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
        hdfc_product_url="https://www.hdfcfund.com/explore/mutual-funds/hdfc-mid-cap-fund/direct",
        hdfc_factsheet_url=HDFC_FACTSHEETS_URL,
        amfi_scheme_url="https://www.amfiindia.com/net-asset-value/nav-details?SchemeCode=118989",
        tags=["equity", "mid-cap"],
    ),
    MutualFundScheme(
        name="HDFC Small Cap Fund Direct Plan Growth",
        short_name="Small Cap Fund",
        category="Equity",
        sub_category="Small Cap",
        amfi_code="130503",
        groww_reference_url="https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth",
        hdfc_product_url="https://www.hdfcfund.com/explore/mutual-funds/hdfc-small-cap-fund/direct",
        hdfc_factsheet_url=HDFC_FACTSHEETS_URL,
        amfi_scheme_url="https://www.amfiindia.com/net-asset-value/nav-details?SchemeCode=130503",
        tags=["equity", "small-cap"],
    ),
    MutualFundScheme(
        name="HDFC Gold ETF Fund of Fund Direct Plan Growth",
        short_name="Gold ETF FoF",
        category="Index, ETFs & FoF",
        sub_category="Gold FoF",
        amfi_code="145552",
        groww_reference_url=(
            "https://groww.in/mutual-funds/"
            "hdfc-gold-etf-fund-of-fund-direct-plan-growth"
        ),
        hdfc_product_url=(
            "https://www.hdfcfund.com/explore/mutual-funds/"
            "hdfc-gold-etf-fund-of-fund/direct"
        ),
        hdfc_factsheet_url=HDFC_FACTSHEETS_URL,
        amfi_scheme_url="https://www.amfiindia.com/net-asset-value/nav-details?SchemeCode=145552",
        tags=["index", "gold", "fof"],
    ),
    MutualFundScheme(
        name="HDFC Large Cap Fund Direct Plan Growth",
        short_name="Large Cap Fund",
        category="Equity",
        sub_category="Large Cap",
        amfi_code="118950",
        groww_reference_url="https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
        hdfc_product_url="https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct",
        hdfc_factsheet_url=HDFC_FACTSHEETS_URL,
        amfi_scheme_url="https://www.amfiindia.com/net-asset-value/nav-details?SchemeCode=118950",
        tags=["equity", "large-cap"],
    ),
    MutualFundScheme(
        name="HDFC ELSS Tax Saver Fund Direct Plan Growth",
        short_name="ELSS Tax Saver",
        category="Equity",
        sub_category="ELSS",
        amfi_code="119063",
        groww_reference_url=(
            "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth"
        ),
        hdfc_product_url=(
            "https://www.hdfcfund.com/explore/mutual-funds/"
            "hdfc-elss-tax-saver/direct"
        ),
        hdfc_factsheet_url=HDFC_FACTSHEETS_URL,
        amfi_scheme_url="https://www.amfiindia.com/net-asset-value/nav-details?SchemeCode=119063",
        tags=["equity", "elss", "tax-saver"],
    ),
]


def get_scheme_by_name(query: str) -> Optional[MutualFundScheme]:
    """Find a scheme by partial name match."""
    query_lower = query.lower()
    for scheme in SELECTED_SCHEMES:
        if query_lower in scheme.name.lower() or query_lower in scheme.short_name.lower():
            return scheme
    return None


def get_schemes_by_category(category: str) -> list[MutualFundScheme]:
    """Filter schemes by category tab (All, Equity, Hybrid, Index)."""
    if category.lower() == "all":
        return SELECTED_SCHEMES
    if category.lower() == "equity":
        return [s for s in SELECTED_SCHEMES if s.category == "Equity"]
    if category.lower() == "index":
        return [s for s in SELECTED_SCHEMES if "index" in s.tags or "gold" in s.tags]
    return SELECTED_SCHEMES
