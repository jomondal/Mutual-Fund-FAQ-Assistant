# Phase 1: Data Collection

Collects mutual fund data exclusively from **official public sources**.

**Project:** [Mutual Fund FAQ Assistant](../README.md) · **Live app:** [hdfc-faq-assistant.vercel.app](https://hdfc-faq-assistant.vercel.app)

## Sources

| Source | URL | Data Type |
|--------|-----|-----------|
| HDFC AMC | https://www.hdfcfund.com | Scheme details, TER, factsheets, SID/SAI |
| AMFI | https://www.amfiindia.com | NAV, scheme codes, regulatory data |
| SEBI | https://investor.sebi.gov.in | Investor education, regulatory references |

> **Note:** Groww links in `schemes_config.py` are reference-only for product context. They are **not** used as data sources.

## Selected Schemes (HDFC AMC)

| Scheme | Category | AMFI Code |
|--------|----------|-----------|
| HDFC Mid Cap Fund Direct Growth | Mid-cap | 118989 |
| HDFC Small Cap Fund Direct Growth | Small-cap | 130503 |
| HDFC Gold ETF FoF Direct Growth | Gold / FoF | 145552 |
| HDFC Large Cap Fund Direct Growth | Large-cap | 118950 |
| HDFC ELSS Tax Saver Direct Growth | ELSS | 119063 |

## Scripts

```bash
# Fetch AMFI NAV data
python -m phase_1_data_collection.fetch_amfi_data

# Fetch HDFC AMC pages + seed corpus
python -m phase_1_data_collection.fetch_hdfc_factsheets

# Run all Phase 1 tasks
python -m phase_1_data_collection.run
```

## Output

```
data/raw/
├── amfi_nav_data.json      # Live NAV from AMFI
└── hdfc_corpus.json        # HDFC pages + curated seed facts
```

## Architecture

```
┌─────────────────┐     ┌──────────────────┐
│  AMFI NAV API   │────▶│  amfi_nav_data   │
│  (NAVAll.txt)   │     │  .json           │
└─────────────────┘     └──────────────────┘
                               │
┌─────────────────┐     ┌──────▼───────────┐
│  HDFC AMC Web   │────▶│  hdfc_corpus     │
│  (hdfcfund.com) │     │  .json           │
└─────────────────┘     └──────────────────┘
                               │
                        ┌──────▼───────────┐
                        │  Seed Corpus     │
                        │  (SID-verified   │
                        │   factual data)  │
                        └──────────────────┘
```
