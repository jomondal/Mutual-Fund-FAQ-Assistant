"""
Detect and handle advisory, opinion, or non-factual queries.
"""

import re

from config.settings import settings

ADVISORY_PATTERNS = [
    r"\bshould i (invest|buy|sell|hold|redeem|switch)\b",
    r"\bwhich (fund|scheme) is (better|best|good|recommended)\b",
    r"\b(recommend|suggest|advice|advise)\b",
    r"\bwhat (fund|scheme) should i\b",
    r"\bbuy or sell\b",
    r"\bworth investing\b",
    r"\bgood time to invest\b",
    r"\bwill (it|this fund) (go up|rise|fall|drop|perform)\b",
    r"\bpredict\b",
    r"\boutlook\b",
    r"\bmarket trend\b",
]

PERFORMANCE_PATTERNS = [
    r"\b(cagr|returns?|performance|alpha|beta|sharpe)\b",
    r"\bhow (much|well) (did|has|have) .* (return|perform)\b",
    r"\bcompare.*(return|performance)\b",
    r"\bwhich.*(better|higher) return\b",
    r"\b1[- ]?year return\b",
    r"\b3[- ]?year return\b",
    r"\b5[- ]?year return\b",
    r"\bstandard deviation\b",
]

PII_PATTERNS = [
    r"\bpan\b",
    r"\baadhaar\b",
    r"\botp\b",
    r"\baccount number\b",
    r"\bfolio number\b",
]

OUT_OF_SCOPE_PATTERNS = [
    r"\bebitda\b",
    r"\bebit\b",
    r"\beps\b",
    r"\bp\s*/\s*e\b",
    r"\bpe ratio\b",
    r"\brevenue\b",
    r"\bprofit margin\b",
    r"\bbalance sheet\b",
    r"\bcash flow\b",
    r"\bstock price\b",
    r"\bshare price\b",
    r"\bcryptocurrency\b",
    r"\bbitcoin\b",
    r"\bforex\b",
    r"\bipo\b",
    r"\bderivatives\b",
    r"\boptions trading\b",
    r"\bfutures trading\b",
]

MF_SCOPE_KEYWORDS = [
    r"\bmutual fund",
    r"\bmf\b",
    r"\bscheme",
    r"\bfund manager",
    r"\bfunds?\b",
    r"\bsip\b",
    r"\bswp\b",
    r"\bnav\b",
    r"\bter\b",
    r"\bexpense ratio",
    r"\bexit load",
    r"\block[- ]?in",
    r"\belss",
    r"\briskometer",
    r"\bbenchmark",
    r"\bamfi",
    r"\bhdfc",
    r"\bmid cap",
    r"\bsmall cap",
    r"\blarge cap",
    r"\bgold etf",
    r"\btax saver",
    r"\bdirect plan",
    r"\baum\b",
    r"\bfactsheet",
    r"\bstatement",
    r"\bredemption",
    r"\ballotment",
    r"\bminimum (sip|investment|lumpsum)",
    r"\bamc\b",
    r"\bportfolio",
    r"\bsebi",
    r"\bregistrar",
    r"\bcams\b",
    r"\bkfin",
]


class QueryClassification:
    FACTUAL = "factual"
    ADVISORY = "advisory"
    PERFORMANCE = "performance"
    PII = "pii"
    OUT_OF_SCOPE = "out_of_scope"


def _is_mf_scoped(query_lower: str) -> bool:
    return any(re.search(pattern, query_lower) for pattern in MF_SCOPE_KEYWORDS)


def classify_query(query: str) -> str:
    """Classify a user query into factual, advisory, performance, PII, or out-of-scope."""
    query_lower = query.lower().strip()

    for pattern in PII_PATTERNS:
        if re.search(pattern, query_lower):
            return QueryClassification.PII

    for pattern in ADVISORY_PATTERNS:
        if re.search(pattern, query_lower):
            return QueryClassification.ADVISORY

    for pattern in PERFORMANCE_PATTERNS:
        if re.search(pattern, query_lower):
            return QueryClassification.PERFORMANCE

    for pattern in OUT_OF_SCOPE_PATTERNS:
        if re.search(pattern, query_lower):
            return QueryClassification.OUT_OF_SCOPE

    if not _is_mf_scoped(query_lower):
        return QueryClassification.OUT_OF_SCOPE

    return QueryClassification.FACTUAL


def get_refusal_response(query: str, classification: str, last_updated: str) -> dict:
    """Generate a refusal response without calling the LLM."""
    if classification == QueryClassification.PII:
        return {
            "answer": (
                "For your privacy and security, I cannot process personal identifiers "
                "such as PAN, Aadhaar, folio numbers, or OTPs. "
                "Please contact HDFC AMC investor services directly for account-specific queries."
            ),
            "source_url": settings.sebi_education_url,
            "classification": classification,
            "refused": True,
            "footer": f"Last updated from sources: {last_updated}",
        }

    if classification == QueryClassification.ADVISORY:
        return {
            "answer": (
                "I can only answer factual questions about mutual fund schemes, "
                "such as expense ratios, exit loads, or lock-in periods. "
                "I cannot provide investment advice or recommend whether to buy, sell, or hold any fund."
            ),
            "source_url": settings.amfi_education_url,
            "classification": classification,
            "refused": True,
            "footer": f"Last updated from sources: {last_updated}",
        }

    if classification == QueryClassification.PERFORMANCE:
        return {
            "answer": (
                "I cannot calculate or compare fund returns or performance metrics. "
                "For verified performance data, please refer to the official HDFC AMC monthly factsheets "
                "which contain NAV history, portfolio composition, and risk metrics."
            ),
            "source_url": "https://www.hdfcfund.com/investor-services/factsheets",
            "classification": classification,
            "refused": True,
            "footer": f"Last updated from sources: {last_updated}",
        }

    if classification == QueryClassification.OUT_OF_SCOPE:
        return {
            "answer": (
                "This question is outside the scope of this assistant. "
                "I can only answer factual questions about HDFC mutual fund schemes, "
                "such as expense ratios, exit loads, lock-in periods, benchmarks, and fund managers."
            ),
            "source_url": settings.amfi_education_url,
            "classification": classification,
            "refused": True,
            "footer": f"Last updated from sources: {last_updated}",
        }

    return {}
