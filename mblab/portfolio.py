"""Portfolio intelligence: import holdings, look through funds, measure concentration, and score how a candidate fits.

PRIVACY: real holdings live ONLY under private/ (gitignored). This module never writes anywhere else (write_private() refuses),
never logs holdings, and its reports contain counts/percentages, not names. Tests and docs use synthetic data only.

Honest limits (also in docs/PORTFOLIO_IMPORT.md):
- Fund look-through is as good as the data the source exposes. IndMoney's get_mf_funds_details gives COMPLETE sector / market-cap / asset-class
  splits but only ~20 (arbitrary, not top-weighted) disclosed stock holdings per fund. Stock-level and theme look-through is therefore a
  lower bound plus an explicitly labelled extrapolation; every output carries a look-through quality label.
- Theme tags are a keyword/ticker map (THEME_RULES below), a coarse lens and not a classification of truth.
- fit_score is a decision aid. Concentration can be appropriate; the score never assumes diversification is always good.
"""
from __future__ import annotations

import csv
import difflib
import io
import json
import math
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field, asdict, fields
from pathlib import Path
from typing import Any, Optional

from .schema import PortfolioFit

ROOT = Path(__file__).resolve().parent.parent
PRIVATE_DIR = ROOT / "private"
DEFAULT_USDINR = 88.0  # used ONLY when a USD value has no INR counterpart and no fx was supplied; always reported as an assumption
KINDS = ("stock", "mutual_fund", "etf", "bond", "other")
ASSET_CLASSES = ("equity", "debt", "cash", "gold", "other")


# =====================================================================================================================
# Data classes
# =====================================================================================================================
@dataclass
class Holding:
    instrument_id: str                      # ticker / scheme code / ISIN / slug
    name: str
    kind: str = "stock"                     # stock | mutual_fund | etf | bond | other
    market: str = "IN"                      # IN | US | OTHER
    currency: str = "INR"
    quantity: Optional[float] = None
    avg_cost: Optional[float] = None        # per unit, local currency
    price: Optional[float] = None           # per unit, local currency
    value_local: Optional[float] = None
    value_inr: float = 0.0
    sector: str = ""
    industry: str = ""
    themes: list = field(default_factory=list)
    asset_class: str = "equity"             # equity | debt | cash | gold | other
    market_cap_bucket: str = ""             # large | mid | small | micro | ""
    category: str = ""                      # fund category as reported by the source
    source: str = ""
    fx_rate: Optional[float] = None         # INR per 1 unit of local currency
    notes: list = field(default_factory=list)


@dataclass
class FundProfile:
    """Everything the source tells us about what a fund holds. All weights are FRACTIONS (0..1) of the fund's value."""
    fund_id: str
    name: str = ""
    category: str = ""
    benchmark: str = ""
    asset_mix: dict = field(default_factory=dict)      # equity/debt/cash/gold/other -> fraction
    sector: dict = field(default_factory=dict)         # canonical sector -> fraction of fund (equity sectors + 'Debt & Cash')
    market_cap: dict = field(default_factory=dict)     # large/mid/small/unknown -> fraction of fund (equity part)
    country: dict = field(default_factory=dict)        # IN/US/OTHER -> fraction of fund
    top_holdings: list = field(default_factory=list)   # [{name, key, weight, sector, country}] weight = fraction of fund
    disclosed_fraction: float = 0.0                    # sum of top_holdings weights
    quality: str = "partial"                           # full | partial | category | none
    assumptions: list = field(default_factory=list)    # what had to be assumed


@dataclass
class Portfolio:
    holdings: list = field(default_factory=list)       # [Holding]
    fund_profiles: dict = field(default_factory=dict)  # instrument_id -> FundProfile
    as_of: str = ""
    source: str = ""
    notes: list = field(default_factory=list)
    reconciliation: dict = field(default_factory=dict)

    def total_inr(self) -> float:
        return sum(h.value_inr or 0.0 for h in self.holdings)

    def to_dict(self) -> dict:
        return {"holdings": [asdict(h) for h in self.holdings], "fund_profiles": {k: asdict(v) for k, v in self.fund_profiles.items()},
                "as_of": self.as_of, "source": self.source, "notes": self.notes, "reconciliation": self.reconciliation}

    @staticmethod
    def from_dict(d: dict) -> "Portfolio":
        hn = {f.name for f in fields(Holding)}
        fn = {f.name for f in fields(FundProfile)}
        return Portfolio(holdings=[Holding(**{k: v for k, v in h.items() if k in hn}) for h in d.get("holdings", [])],
                         fund_profiles={k: FundProfile(**{kk: vv for kk, vv in v.items() if kk in fn}) for k, v in d.get("fund_profiles", {}).items()},
                         as_of=d.get("as_of", ""), source=d.get("source", ""), notes=list(d.get("notes", [])), reconciliation=dict(d.get("reconciliation", {})))


# =====================================================================================================================
# Canonicalisation helpers (sector, market cap, names)
# =====================================================================================================================
SECTOR_ALIASES = {
    "tech": "Technology", "technology": "Technology", "information technology": "Technology", "it": "Technology", "software": "Technology",
    "health": "Healthcare", "healthcare": "Healthcare", "health care": "Healthcare", "pharma": "Healthcare", "pharmaceuticals": "Healthcare",
    "industrial": "Industrials", "industrials": "Industrials", "capital goods": "Industrials",
    "communication": "Communication Services", "communication services": "Communication Services", "telecom": "Communication Services", "telecommunication": "Communication Services",
    "financial": "Financial Services", "financials": "Financial Services", "financial services": "Financial Services", "banks": "Financial Services", "banking": "Financial Services",
    "consumer cyclical": "Consumer Cyclical", "consumer discretionary": "Consumer Cyclical", "automobile": "Consumer Cyclical", "auto": "Consumer Cyclical",
    "consumer defensive": "Consumer Defensive", "consumer staples": "Consumer Defensive", "fmcg": "Consumer Defensive",
    "basic materials": "Basic Materials", "materials": "Basic Materials", "metals": "Basic Materials", "chemicals": "Basic Materials",
    "energy": "Energy", "oil & gas": "Energy", "oil and gas": "Energy",
    "utilities": "Utilities", "utility": "Utilities", "power": "Utilities",
    "real estate": "Real Estate", "realty": "Real Estate",
    "cash equivalent": "Debt & Cash", "cash": "Debt & Cash", "corporate": "Debt & Cash", "government": "Debt & Cash", "debt & cash": "Debt & Cash", "debt": "Debt & Cash",
    "commodity": "Commodity", "gold": "Commodity", "precious metals": "Commodity",
}


def canon_sector(s: Any) -> str:
    s = (str(s) if s is not None else "").strip()
    if not s:
        return "Unclassified"
    return SECTOR_ALIASES.get(s.lower(), s.title() if s.islower() else s)


def canon_mcap(s: Any) -> str:
    t = (str(s) if s is not None else "").lower()
    if not t:
        return ""
    if "micro" in t:
        return "micro"
    if "small" in t:
        return "small"
    if "mid" in t:
        return "mid"
    if "large" in t or "mega" in t or "blue" in t:
        return "large"
    return ""


_SUFFIX = re.compile(r"\b(ltd|limited|inc|incorporated|corp|corporation|co|company|plc|nv|sa|ag|holdings|holding|ordinary shares|class [a-c]|adr|the)\b")


def name_key(name: Any) -> str:
    """Normalised company key so 'Alphabet Inc. Class A' (direct) and 'Alphabet Inc Class C' (inside a fund) match."""
    s = str(name or "").lower().replace("&", " and ").replace("-", " ").replace("_", " ")
    s = re.sub(r"[^a-z0-9 ]", "", s)
    s = _SUFFIX.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()


# A few well known tickers -> name keys so a candidate given only as a ticker can be matched against fund look-through names.
TICKER_NAME_ALIASES = {
    "MSFT": "microsoft", "GOOGL": "alphabet", "GOOG": "alphabet", "AMZN": "amazoncom", "META": "meta platforms", "NVDA": "nvidia",
    "AAPL": "apple", "TSLA": "tesla", "AVGO": "broadcom", "AMD": "advanced micro devices", "MU": "micron technology", "TSM": "taiwan semiconductor manufacturing",
    "NFLX": "netflix", "ORCL": "oracle", "PLTR": "palantir technologies", "TCS": "tata consultancy services", "INFY": "infosys", "HAL": "hindustan aeronautics",
    "BEL": "bharat electronics", "HDFCBANK": "hdfc bank", "ICICIBANK": "icici bank", "RELIANCE": "reliance industries", "ABB": "abb india",
}


def base_ticker(t: Any) -> str:
    t = str(t or "").upper().strip()
    t = re.sub(r"^(NSE|BSE|NYSE|NASDAQ)[:.]", "", t)
    return re.sub(r"\.(NS|BO|NSE|BSE)$", "", t)


# =====================================================================================================================
# Theme map (maintained here, deliberately simple and documented in docs/PORTFOLIO_IMPORT.md)
# A holding gets a theme if its (base) ticker is listed OR a keyword occurs as a whole word/phrase in its name/industry. Tags are a coarse lens.
# =====================================================================================================================
THEME_RULES = {
    "ai": {"tickers": {"NVDA", "MSFT", "GOOGL", "GOOG", "META", "AMZN", "ORCL", "AVGO", "AMD", "PLTR", "TSM", "MU", "SMCI", "ARM", "SNOW", "ANET", "MRVL", "VRT"},
           "keywords": ["artificial intelligence", "machine learning", "nvidia", "palantir", "generative ai"]},
    "semiconductors": {"tickers": {"NVDA", "TSM", "MU", "AMD", "AVGO", "INTC", "ASML", "QCOM", "AMAT", "LRCX", "KLAC", "ARM", "MRVL", "TXN", "ADI", "ON", "MCHP", "NXPI", "MPWR"},
                       "keywords": ["semiconductor", "semiconductors", "micron", "nvidia", "broadcom", "foundry", "chipmaker", "advanced micro devices", "applied materials"]},
    "data_centre_power": {"tickers": {"VRT", "ETN", "GEV", "CEG", "VST", "NRG", "DELL", "SMCI", "ANET", "EQIX", "DLR", "PWR", "HUBB", "NVT",
                                       "POWERGRID", "TATAPOWER", "ADANIPOWER", "ADANIENSOL", "CGPOWER", "VOLTAMP", "ABB", "SIEMENS", "THERMAX", "NTPC", "BHEL"},
                          "keywords": ["data cent", "data center", "data centre", "transformers", "switchgear", "power", "grid", "energy solutions", "bharat heavy electricals"]},
    "defence_aerospace": {"tickers": {"LMT", "RTX", "NOC", "GD", "LHX", "HII", "KTOS", "RKLB", "AVAV", "HAL", "BEL", "BDL", "MAZDOCK", "COCHINSHIP", "GRSE", "DATAPATTNS"},
                          "keywords": ["aeronautics", "defence", "defense", "shipyard", "aerospace", "ordnance", "rocket", "bharat electronics", "bharat dynamics", "mazagon", "garden reach"]},
    "cloud_software": {"tickers": {"MSFT", "ORCL", "CRM", "NOW", "SNOW", "ADBE", "DDOG", "NET", "CRWD", "PANW", "PLTR", "WDAY", "INTU", "CDNS", "SNPS"},
                       "keywords": ["software", "cloud", "cyber security", "cybersecurity", "saas"]},
    "it_services": {"tickers": {"TCS", "INFY", "WIPRO", "HCLTECH", "TECHM", "COFORGE", "PERSISTENT", "MPHASIS", "LTIM", "LTM", "ACN"},
                    "keywords": ["tata consultancy", "infosys", "wipro", "hcl tech", "tech mahindra", "coforge", "persistent systems", "mphasis", "hexaware", "firstsource", "eclerx", "rategain", "it services"]},
    "internet_platforms": {"tickers": {"GOOGL", "GOOG", "META", "AMZN", "NFLX", "UBER", "BKNG", "SHOP", "SPOT", "ETERNAL", "NYKAA", "PAYTM", "SWIGGY", "NAUKRI"},
                           "keywords": ["eternal", "zomato", "meesho", "nykaa", "paytm", "policybazaar", "swiggy", "info edge", "cartrade", "internet"]},
    "ev_clean_energy": {"tickers": {"TSLA", "ENPH", "FSLR", "RIVN", "NEE", "PLUG", "BE", "SUZLON", "WAAREEENER", "PREMIERENE", "ATHERENERG"},
                        "keywords": ["solar", "renewable", "green energy", "waaree", "premier energies", "suzlon", "ather", "electric vehicle", "battery", "lithium", "wind energy"]},
    "infrastructure": {"tickers": {"LT", "CONCOR", "IRB", "NCC"},
                       "keywords": ["infrastructure", "infra", "construction", "cement", "railway", "larsen", "container corporation", "engineers"]},
    "precious_metals": {"tickers": {"GLD", "IAU", "SLV", "GOLDBEES"}, "keywords": ["gold", "silver", "bullion", "precious metals"]},
}
_THEME_RX = {t: [re.compile(r"(?<![a-z0-9])" + re.escape(k) + r"(?![a-z0-9])") if " " in k or len(k) > 4 else re.compile(r"(?<![a-z0-9])" + re.escape(k) + r"(?![a-z0-9])") for k in r["keywords"]]
             for t, r in THEME_RULES.items()}

# category-level themes for funds whose stock list is only sampled (used as a floor for theme exposure, flagged as category-level)
CATEGORY_THEMES = [
    (re.compile(r"infrastructure|infra\b"), ["infrastructure"]),
    (re.compile(r"sector\s*-\s*technology|technology fund|digital|\bit fund\b"), ["it_services"]),
    (re.compile(r"precious|gold|silver"), ["precious_metals"]),
    (re.compile(r"defen[cs]e"), ["defence_aerospace"]),
    (re.compile(r"semiconductor"), ["semiconductors"]),
]


def tag_themes(ticker: str = "", name: str = "", sector: str = "", industry: str = "") -> list:
    tk = base_ticker(ticker)
    text = " ".join(str(x or "") for x in (name, industry)).lower().replace("&", " and ")
    out = []
    for theme, rule in THEME_RULES.items():
        if (tk and tk in rule["tickers"]) or any(rx.search(text) for rx in _THEME_RX[theme]):
            out.append(theme)
    return out


# Sector / industry hints for well known tickers (used only when the source does not report them)
SECTOR_BY_TICKER = {"MSFT": "Technology", "NVDA": "Technology", "AAPL": "Technology", "AVGO": "Technology", "AMD": "Technology", "MU": "Technology", "TSM": "Technology",
                    "ORCL": "Technology", "GOOGL": "Communication Services", "GOOG": "Communication Services", "META": "Communication Services", "NFLX": "Communication Services",
                    "AMZN": "Consumer Cyclical", "TSLA": "Consumer Cyclical", "JPM": "Financial Services", "V": "Financial Services", "LLY": "Healthcare"}
INDUSTRY_BY_TICKER = {"MSFT": "Software - Infrastructure", "NVDA": "Semiconductors", "AMD": "Semiconductors", "MU": "Semiconductors", "TSM": "Semiconductors", "AVGO": "Semiconductors",
                      "GOOGL": "Internet Content & Information", "META": "Internet Content & Information", "AMZN": "Internet Retail", "AAPL": "Consumer Electronics", "TSLA": "Auto Manufacturers"}


# =====================================================================================================================
# Private storage guard
# =====================================================================================================================
def write_private(obj: Any, relpath: str) -> Path:
    """Write JSON under private/ ONLY. Refuses any other location (real holdings must never reach a tracked path)."""
    p = (PRIVATE_DIR / relpath).resolve()
    if PRIVATE_DIR.resolve() not in p.parents:
        raise ValueError("write_private refuses to write outside private/")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=1, ensure_ascii=False), encoding="utf-8")
    return p


def private_is_ignored(root: Optional[Path] = None) -> bool:
    """True iff git ignores private/ (used by the privacy test)."""
    r = subprocess.run(["git", "check-ignore", "-q", "private/x"], cwd=str(root or ROOT), capture_output=True)
    return r.returncode == 0


# =====================================================================================================================
# Importers: CSV / Excel with heuristic header detection
# =====================================================================================================================
FIELD_ALIASES = {
    "instrument_id": ["symbol", "ticker", "scrip", "scrip code", "scripcode", "isin", "isin code", "code", "trading symbol", "tradingsymbol", "stock symbol", "scheme code", "security code", "instrument code", "instrument"],
    "name": ["name", "stock name", "scheme name", "security", "security name", "company", "company name", "fund name", "instrument name", "asset name", "holding", "holdings", "description", "scrip name", "stock", "script"],
    "kind": ["type", "asset type", "instrument type", "security type", "investment type", "product type", "product"],
    "asset_class": ["asset class", "asset category", "assetclass"],
    "market": ["market", "exchange", "country", "region", "geography"],
    "currency": ["currency", "ccy", "curr"],
    "quantity": ["quantity", "qty", "units", "shares", "no of shares", "number of shares", "balance", "holding qty", "total units", "current quantity", "net qty", "available quantity"],
    "avg_cost": ["avg cost", "average cost", "avg price", "average price", "avg buy price", "average buy price", "buy avg", "buy average", "purchase price", "cost price", "avg cost price", "buy price", "avg nav", "average nav"],
    "price": ["ltp", "price", "current price", "last price", "cmp", "market price", "nav", "current nav", "close price", "closing price", "unit price", "live price", "last traded price"],
    "invested": ["invested", "invested amount", "invested value", "cost", "total cost", "buy value", "amount invested", "purchase value", "cost value", "book value", "investment amount", "total investment"],
    "value_local": ["current value", "market value", "value", "present value", "current amount", "curr value", "total value", "valuation", "holding value", "mkt value", "current market value"],
    "value_inr": [],  # filled by header currency hints (e.g. 'Current Value (INR)')
    "sector": ["sector", "sector name"],
    "industry": ["industry", "sub sector", "subsector", "industry name"],
    "market_cap": ["market cap", "market cap bucket", "cap", "cap type", "market capitalisation", "market capitalization", "size"],
    "themes": ["theme", "themes", "tags", "tag"],
}
IMPORTANT_FIELDS = ("name", "instrument_id", "quantity", "value_local", "price")
_CCY_TOKENS = {"inr": "INR", "rs": "INR", "₹": "INR", "rupees": "INR", "usd": "USD", "$": "USD", "dollar": "USD", "dollars": "USD"}


def _norm_header(h: Any) -> str:
    s = str(h if h is not None else "").lower().replace("&", " and ").replace("₹", " inr ").replace("$", " usd ")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _split_ccy(h: str) -> tuple:
    """'current value inr' -> ('current value', 'INR')"""
    toks = h.split()
    ccy = ""
    keep = []
    for t in toks:
        if t in _CCY_TOKENS:
            ccy = _CCY_TOKENS[t]
        else:
            keep.append(t)
    return " ".join(keep), ccy


_ALIAS_NORM = {f: [(a, re.sub(r"\s+", " ", a)) for a in al] for f, al in FIELD_ALIASES.items()}


def _score_header(h: Any) -> tuple:
    """Best (field, score, ccy_hint) for one header cell; score 0 if no plausible match."""
    n = _norm_header(h)
    if not n or len(n) > 60:
        return ("", 0.0, "")
    base, ccy = _split_ccy(n)
    if not base:
        return ("", 0.0, ccy)
    best = ("", 0.0)
    for f, aliases in _ALIAS_NORM.items():
        for _, a in aliases:
            if base == a:
                sc = 1.0
            elif len(a) >= 5 and (re.search(r"(?<![a-z])" + re.escape(a) + r"(?![a-z])", base)):
                sc = 0.8
            else:
                r = difflib.SequenceMatcher(None, base, a).ratio()
                sc = 0.7 if r >= 0.86 else 0.0
            if sc > best[1]:
                best = (f, sc)
    field_, sc = best
    # content like 'invested value' also contains 'value'; prefer the longer/more specific alias match
    if field_ == "value_local" and re.search(r"invest|cost|purchase|buy", base):
        field_, sc = "invested", max(sc, 0.8)
    if field_ == "price" and re.search(r"avg|average|buy|purchase|cost", base):
        field_, sc = "avg_cost", max(sc, 0.8)
    if field_ == "value_local" and ccy == "INR":
        field_ = "value_inr"
    return (field_, sc, ccy)


def _num(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return None if (isinstance(x, float) and math.isnan(x)) else float(x)
    s = str(x).strip()
    if not s or s.lower() in {"-", "--", "—", "na", "n/a", "nan", "none", "null"}:
        return None
    neg = s.startswith("(") and s.endswith(")")
    s = re.sub(r"(?i)(inr|usd|rs\.?|₹|\$|%|,|\s)", "", s.strip("()"))
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


@dataclass
class ImportResult:
    holdings: list = field(default_factory=list)
    column_map: dict = field(default_factory=dict)       # field -> header text that was used
    unmapped_columns: list = field(default_factory=list)  # headers we could not map (reported, never silently dropped)
    missing_fields: list = field(default_factory=list)    # important fields with no column
    skipped_rows: list = field(default_factory=list)      # [(row_number, reason)]
    warnings: list = field(default_factory=list)
    header_row: int = -1
    preamble_rows: int = 0
    source: str = ""

    @property
    def ok(self) -> bool:
        return bool(self.holdings)

    def report(self) -> str:
        """Plain summary: mapping and counts only, never holding contents."""
        lines = [f"source={self.source} header_row={self.header_row} preamble_rows={self.preamble_rows} holdings={len(self.holdings)} skipped_rows={len(self.skipped_rows)}",
                 "mapped: " + ", ".join(f"{k}<-'{v}'" for k, v in self.column_map.items())]
        if self.unmapped_columns:
            lines.append("could not map columns: " + ", ".join(f"'{c}'" for c in self.unmapped_columns))
        if self.missing_fields:
            lines.append("no column found for: " + ", ".join(self.missing_fields))
        lines += [f"warning: {w}" for w in self.warnings]
        return "\n".join(lines)


def _detect_table(rows: list, mapping: Optional[dict] = None) -> tuple:
    """Find the header row and a field->column-index map. Returns (header_idx, colmap{field: idx}, ccy_hints{field: ccy}, scores)."""
    best = (-1, 0.0, {}, {})
    for i, row in enumerate(rows[:40]):
        cmap, ccy, total = {}, {}, 0.0
        cand = defaultdict(list)
        for j, cell in enumerate(row):
            f, sc, cc = _score_header(cell)
            if f and sc > 0:
                cand[f].append((sc, -j, j, cc))
        for f, lst in cand.items():
            sc, _, j, cc = max(lst)
            cmap[f] = j
            ccy[f] = cc
            total += sc
        if len(cmap) >= 2 and total > best[1]:
            best = (i, total, cmap, ccy)
    return best[0], best[2], best[3], best[1]


def _infer_kind(raw_kind: str, name: str, ident: str) -> str:
    k, n, i = (raw_kind or "").lower(), (name or "").lower(), (ident or "").upper()
    if re.search(r"\betf\b|bees\b|exchange traded", k + " " + n):
        return "etf"
    if re.search(r"mutual|\bmf\b|\bfund\b|\bfof\b|scheme", k) or re.search(r"\bfund\b|\bfof\b|index fund|direct (growth|plan)|growth plan", n) or i.startswith("INF"):
        return "mutual_fund"
    if re.search(r"bond|debenture|\bncd\b|g-?sec|\bsgb\b|treasury|t-bill", k + " " + n):
        return "bond"
    if re.search(r"fd|deposit|epf|ppf|nps|cash|savings|insurance|crypto|real estate", k):
        return "other"
    return "stock"


def _infer_asset_class(raw: str, kind: str, name: str) -> str:
    r, n = (raw or "").lower(), (name or "").lower()
    txt = r + " " + n
    if re.search(r"\bgold\b|\bsilver\b|precious", txt):
        return "gold"
    if re.search(r"liquid|overnight|money market|\bcash\b|savings", txt) and kind != "stock":
        return "cash"
    if re.search(r"\bdebt\b|bond|gilt|debenture|\bncd\b|treasury|g-?sec|fixed income|short duration|\bfd\b|deposit", txt) or kind == "bond":
        return "debt"
    if r in ASSET_CLASSES:
        return r
    return "equity" if kind in ("stock", "mutual_fund", "etf") else "other"


def _infer_market(raw: str, ident: str, ccy: str, exch_hint: str = "") -> str:
    r = (raw or "").upper()
    if r in {"IN", "INDIA", "NSE", "BSE", "IND"} or "INDIA" in r:
        return "IN"
    if r in {"US", "USA", "NYSE", "NASDAQ", "UNITED STATES"} or "US" == r[:2] and len(r) <= 3:
        return "US"
    i = (ident or "").upper()
    if i.startswith("INE") or i.startswith("INF") or re.search(r"\.(NS|BO)$", i):
        return "IN"
    if i.startswith("US") and len(i) == 12:
        return "US"
    if ccy == "USD":
        return "US"
    return "IN"


def _build_holdings(rows: list, hdr: int, cmap: dict, ccy_hint: dict, fx: Optional[dict], res: ImportResult) -> None:
    fx = {k.upper(): float(v) for k, v in (fx or {}).items()}
    assumed_fx_used = False
    for ri in range(hdr + 1, len(rows)):
        row = rows[ri]
        if row is None or all((c is None or str(c).strip() == "") for c in row):
            continue
        g = lambda f: (row[cmap[f]] if f in cmap and cmap[f] < len(row) else None)
        name = str(g("name") or "").strip()
        ident = str(g("instrument_id") or "").strip()
        if not name and not ident:
            res.skipped_rows.append((ri + 1, "no name or id"))
            continue
        if re.match(r"(?i)^\s*(grand\s+)?(sub\s*)?total\b|^\s*net\b|^\s*summary\b", name or ident):
            res.skipped_rows.append((ri + 1, "total row"))
            continue
        kind = _infer_kind(str(g("kind") or ""), name, ident)
        ccy = str(g("currency") or "").strip().upper() or ccy_hint.get("value_local", "") or ccy_hint.get("price", "") or ""
        market = _infer_market(str(g("market") or ""), ident, ccy)
        ccy = ccy or ("USD" if market == "US" else "INR")
        qty, price, avg, inv = _num(g("quantity")), _num(g("price")), _num(g("avg_cost")), _num(g("invested"))
        vloc, vinr = _num(g("value_local")), _num(g("value_inr"))
        if vloc is None and qty is not None and price is not None:
            vloc = qty * price
        if vloc is None and vinr is not None and ccy == "INR":
            vloc = vinr
        if vloc is None and inv is not None:
            vloc = inv
            res.warnings.append(f"row {ri + 1}: no current value; used invested amount")
        if price is None and vloc is not None and qty:
            price = vloc / qty
        if avg is None and inv is not None and qty:
            avg = inv / qty
        rate = 1.0 if ccy == "INR" else None
        if vinr is None and vloc is not None:
            if ccy == "INR":
                vinr = vloc
            elif ccy in fx:
                rate = fx[ccy]; vinr = vloc * rate
            else:
                rate = DEFAULT_USDINR; vinr = vloc * rate; assumed_fx_used = True
        elif vinr is not None and vloc and ccy != "INR":
            rate = vinr / vloc
        if vinr is None:
            res.skipped_rows.append((ri + 1, "no value could be determined"))
            continue
        sector = canon_sector(g("sector")) if g("sector") else SECTOR_BY_TICKER.get(base_ticker(ident), "")
        industry = str(g("industry") or "").strip() or INDUSTRY_BY_TICKER.get(base_ticker(ident), "")
        themes = sorted(set(tag_themes(ident, name, sector, industry)) | {t.strip().lower().replace(" ", "_") for t in re.split(r"[;,|]", str(g("themes") or "")) if t.strip()})
        res.holdings.append(Holding(instrument_id=ident or name, name=name or ident, kind=kind, market=market, currency=ccy, quantity=qty, avg_cost=avg, price=price,
                                    value_local=vloc, value_inr=float(vinr), sector=sector, industry=industry, themes=themes,
                                    asset_class=_infer_asset_class(str(g("asset_class") or ""), kind, name), market_cap_bucket=canon_mcap(g("market_cap")),
                                    source=res.source, fx_rate=rate))
    if assumed_fx_used:
        res.warnings.append(f"some non-INR values had no INR counterpart; assumed fx {DEFAULT_USDINR} INR/USD (pass fx={{'USD': rate}} to override)")


def parse_table(rows: list, source: str = "table", mapping: Optional[dict] = None, fx: Optional[dict] = None) -> ImportResult:
    """Core of both importers. `rows` is a list of lists of cell values. `mapping` optionally forces {field: header_text}."""
    res = ImportResult(source=source)
    rows = [list(r) for r in rows]
    hdr, cmap, ccy, _ = _detect_table(rows)
    if hdr < 0:
        res.warnings.append("no header row recognised in the first 40 rows; supply mapping={field: header} and check the file")
        return res
    if mapping:
        header_cells = [_norm_header(c) for c in rows[hdr]]
        for f, h in mapping.items():
            hn = _norm_header(h)
            if hn in header_cells:
                cmap[f] = header_cells.index(hn)
            else:
                res.warnings.append(f"mapping for '{f}' names header '{h}' which is not in the file")
    res.header_row, res.preamble_rows = hdr + 1, hdr
    used = set(cmap.values())
    header_cells_raw = rows[hdr]
    res.column_map = {f: str(header_cells_raw[j]).strip() for f, j in cmap.items()}
    res.unmapped_columns = [str(c).strip() for j, c in enumerate(header_cells_raw) if j not in used and str(c or "").strip()]
    if "invested" not in cmap and "avg_cost" not in cmap:
        res.warnings.append("no cost column found: cost basis / P&L-based fields will be empty")
    res.missing_fields = [f for f in IMPORTANT_FIELDS if f not in cmap]
    if "name" not in cmap and "instrument_id" not in cmap:
        res.warnings.append("neither a name nor an id column was found; nothing can be identified")
        return res
    if not any(f in cmap for f in ("value_local", "value_inr")) and not ("quantity" in cmap and "price" in cmap):
        res.warnings.append("no value column and no quantity+price columns; holdings values cannot be computed")
    _build_holdings(rows, hdr, cmap, ccy, fx, res)
    return res


def _read_csv_rows(path_or_text: Any) -> list:
    if isinstance(path_or_text, (str, Path)) and Path(str(path_or_text)).exists():
        text = Path(path_or_text).read_text(encoding="utf-8-sig", errors="replace")
    else:
        text = str(path_or_text)
    try:
        dialect = csv.Sniffer().sniff(text[:4096], delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    return list(csv.reader(io.StringIO(text), dialect))


def load_holdings_csv(path_or_text: Any, mapping: Optional[dict] = None, fx: Optional[dict] = None) -> ImportResult:
    """Load holdings from a CSV file path (or CSV text). Headers are detected heuristically; see ImportResult.report() for what was/was not mapped."""
    src = Path(path_or_text).name if isinstance(path_or_text, (str, Path)) and len(str(path_or_text)) < 400 and Path(str(path_or_text)).exists() else "csv-text"
    return parse_table(_read_csv_rows(path_or_text), source=src, mapping=mapping, fx=fx)


def load_holdings_excel(path: Any, sheet: Optional[Any] = None, mapping: Optional[dict] = None, fx: Optional[dict] = None) -> ImportResult:
    """Load holdings from .xlsx/.xls. Without `sheet`, tries every sheet and uses the one with the best header match."""
    try:
        import pandas as pd
        sheets = pd.read_excel(path, sheet_name=sheet if sheet is not None else None, header=None, dtype=object)
    except ImportError as e:
        raise ImportError("reading Excel needs openpyxl (.xlsx) or xlrd (.xls): pip install openpyxl") from e
    if not isinstance(sheets, dict):
        sheets = {str(sheet): sheets}
    best, best_score = None, -1.0
    for nm, df in sheets.items():
        rows = [[None if (isinstance(c, float) and math.isnan(c)) else c for c in r] for r in df.values.tolist()]
        _, cm, _, sc = _detect_table(rows)
        if sc > best_score and len(cm) >= 2:
            best, best_score = (nm, rows), sc
    if best is None:
        r = ImportResult(source=Path(str(path)).name)
        r.warnings.append("no sheet with a recognisable holdings header")
        return r
    res = parse_table(best[1], source=f"{Path(str(path)).name}[{best[0]}]", mapping=mapping, fx=fx)
    if len(sheets) > 1:
        res.warnings.append(f"{len(sheets)} sheets present; used the best match")
    return res


def load_holdings(path: Any, **kw) -> ImportResult:
    p = Path(str(path))
    return load_holdings_excel(p, **kw) if p.suffix.lower() in (".xlsx", ".xlsm", ".xls") else load_holdings_csv(p, **kw)


def portfolio_from_import(res: ImportResult) -> Portfolio:
    return Portfolio(holdings=list(res.holdings), source=res.source, notes=[f"imported from file; {len(res.holdings)} holdings; funds use category-level look-through only"])


# =====================================================================================================================
# Fund look-through profiles
# =====================================================================================================================
# Category-level exposure assumptions, used only when a fund's real breakdown is unavailable. Quality is then 'category'.
CATEGORY_RULES = [
    (re.compile(r"nasdaq|s&p ?500|us equity|us total|\bus (large|growth)|fang"), {"asset": {"equity": 1.0}, "mcap": {"large": 1.0}, "country": {"US": 1.0}, "tag": "US large-cap equity"}),
    (re.compile(r"next 50|nifty next"), {"asset": {"equity": 1.0}, "mcap": {"large": 0.85, "mid": 0.15}, "country": {"IN": 1.0}, "tag": "India large/mid index"}),
    (re.compile(r"nifty 50|sensex|nifty50|large ?cap|bluechip|blue chip|nifty 100"), {"asset": {"equity": 1.0}, "mcap": {"large": 1.0}, "country": {"IN": 1.0}, "tag": "India large-cap equity"}),
    (re.compile(r"mid ?cap"), {"asset": {"equity": 1.0}, "mcap": {"mid": 0.80, "large": 0.12, "small": 0.08}, "country": {"IN": 1.0}, "tag": "India mid-cap equity"}),
    (re.compile(r"small ?cap"), {"asset": {"equity": 1.0}, "mcap": {"small": 0.75, "mid": 0.20, "large": 0.05}, "country": {"IN": 1.0}, "tag": "India small-cap equity"}),
    (re.compile(r"flexi|multi ?cap|focused|elss|value|contra|dividend yield|equity"), {"asset": {"equity": 0.95, "cash": 0.05}, "mcap": {"large": 0.60, "mid": 0.20, "small": 0.15}, "country": {"IN": 1.0}, "tag": "India diversified equity"}),
    (re.compile(r"gold|silver|precious"), {"asset": {"gold": 1.0}, "mcap": {}, "country": {"IN": 1.0}, "tag": "precious metals"}),
    (re.compile(r"liquid|overnight|money market|ultra short"), {"asset": {"cash": 1.0}, "mcap": {}, "country": {"IN": 1.0}, "tag": "cash-like debt"}),
    (re.compile(r"debt|bond|gilt|short duration|treasury|credit|banking and psu|corporate bond|income"), {"asset": {"debt": 1.0}, "mcap": {}, "country": {"IN": 1.0}, "tag": "debt"}),
    (re.compile(r"hybrid|balanced|arbitrage|asset allocation"), {"asset": {"equity": 0.65, "debt": 0.35}, "mcap": {"large": 0.5, "mid": 0.1, "small": 0.05}, "country": {"IN": 1.0}, "tag": "hybrid"}),
    (re.compile(r"international|global|world|overseas|emerging"), {"asset": {"equity": 1.0}, "mcap": {"large": 0.8, "mid": 0.2}, "country": {"OTHER": 1.0}, "tag": "international equity"}),
]


def category_profile(fund_id: str, name: str, category: str = "") -> FundProfile:
    txt = f"{name} {category}".lower().replace("&", " and ")
    for rx, p in CATEGORY_RULES:
        if rx.search(txt):
            eq = p["asset"].get("equity", 0.0) + p["asset"].get("cash", 0.0) * 0  # equity share
            return FundProfile(fund_id=fund_id, name=name, category=category, asset_mix=dict(p["asset"]), sector={"Unclassified": eq} if eq else {},
                               market_cap={k: v * eq for k, v in p["mcap"].items()}, country=dict(p["country"]), top_holdings=[], disclosed_fraction=0.0, quality="category",
                               assumptions=[f"category-level assumption '{p['tag']}' (no holdings data); sector unknown"])
    return FundProfile(fund_id=fund_id, name=name, category=category, asset_mix={"other": 1.0}, sector={}, market_cap={}, country={"IN": 1.0}, quality="none",
                       assumptions=["fund not recognised; treated as unclassified"])


def _pct(s: Any) -> float:
    v = _num(s)
    return 0.0 if v is None else v


def _holding_country(name: str) -> str:
    n = str(name or "")
    if re.search(r"(?i)\b(ltd|limited)\b", n):
        return "IN"
    if re.search(r"(?i)\b(inc|corp|corporation|co)\b\.?|\.com\b", n):
        return "US"
    return "OTHER"


def fund_profile_from_indmoney(fund_id: Any, data: dict, holding_name: str = "") -> FundProfile:
    """Normalise one fund entry of get_mf_funds_details (includes asset_allocation, sector_allocation, holdings) into a FundProfile.

    Observed shape: data = {fund_detail:{name,category,benchmark_name,...}, asset_allocation:[{name:'Equity'|'Debt & Cash', PercentageVal,
    market_cap_distribution:{market_cap:[{name,value}]}}], sector_allocation:[{name, PercentageVal, sectors:[{name, percValue}]}],
    holdings:{holdings:[{name:'Equity', holds:[{name, perc:'1.2%', sector}]}]}}.
    NOTE: 'holds' contains ~20 arbitrary holdings (not necessarily the largest), so it is a partial disclosure.
    """
    fd = data.get("fund_detail", {}) or {}
    name = fd.get("name") or holding_name or str(fund_id)
    category, bench = str(fd.get("category", "")), str(fd.get("benchmark_name", "") or "")
    bench = "" if bench.lower() == "null" else bench
    prof = FundProfile(fund_id=str(fund_id), name=name, category=category, benchmark=bench)
    txt = f"{name} {category} {bench}".lower()

    # asset mix
    eq = deb = 0.0
    for a in data.get("asset_allocation", []) or []:
        v = _pct(a.get("PercentageVal", a.get("perc"))) / 100.0
        if str(a.get("name", "")).lower().startswith("equity"):
            eq += v
        else:
            deb += v
    tot = eq + deb
    holds = []
    for g in (data.get("holdings", {}) or {}).get("holdings", []) or []:
        holds += g.get("holds", []) or []
    metals = bool(holds) and all(re.search(r"(?i)gold|silver", str(h.get("name", ""))) for h in holds)
    if metals:
        prof.asset_mix = {"gold": 1.0}
        prof.assumptions.append("fund-of-funds over gold/silver ETFs: classified as precious metals (source reports it as cash)")
        eq = 0.0
    elif tot < 0.5:
        cp = category_profile(prof.fund_id, name, category)
        prof.asset_mix, prof.assumptions = dict(cp.asset_mix), cp.assumptions + ["asset allocation missing at source"]
        eq = cp.asset_mix.get("equity", 0.0)
    else:
        eq, deb = eq / tot, deb / tot
        prof.asset_mix = {"equity": eq}
        if deb > 0:
            deb_sub = {}
            for s in data.get("sector_allocation", []) or []:
                if not str(s.get("name", "")).lower().startswith("equity"):
                    for x in s.get("sectors", []) or []:
                        deb_sub[str(x.get("name", "")).lower()] = _pct(x.get("percValue"))
            cash_share = (deb_sub.get("cash equivalent", 100.0 if not deb_sub else 0.0)) / 100.0 if deb_sub else 1.0
            prof.asset_mix["cash"] = deb * min(1.0, cash_share)
            if deb * (1 - min(1.0, cash_share)) > 0:
                prof.asset_mix["debt"] = deb * (1 - min(1.0, cash_share))
    # sector (of fund value)
    sec = defaultdict(float)
    for s in data.get("sector_allocation", []) or []:
        is_eq = str(s.get("name", "")).lower().startswith("equity")
        for x in s.get("sectors", []) or []:
            v = _pct(x.get("percValue")) / 100.0
            if is_eq:
                sec[canon_sector(x.get("name"))] += v * eq
    if metals:
        sec = {"Commodity": 1.0}
    else:
        got = sum(sec.values())
        if eq - got > 0.005:
            sec["Unclassified"] = eq - got
        non_eq = sum(v for k, v in prof.asset_mix.items() if k != "equity")
        if non_eq > 0:
            sec["Debt & Cash"] = non_eq
    prof.sector = {k: round(v, 6) for k, v in sec.items() if v > 0}
    # market cap (of fund value, equity part)
    mc = defaultdict(float)
    for a in data.get("asset_allocation", []) or []:
        if str(a.get("name", "")).lower().startswith("equity"):
            for m in (a.get("market_cap_distribution", {}) or {}).get("market_cap", []) or []:
                mc[canon_mcap(m.get("name")) or "unknown"] += _pct(m.get("value")) / 100.0 * eq
    if eq > 0 and not mc:
        cp = category_profile(prof.fund_id, name, category)
        if cp.market_cap:
            mc = defaultdict(float, {k: v / max(cp.asset_mix.get("equity", 1.0), 1e-9) * eq for k, v in cp.market_cap.items()})
            prof.assumptions.append("market-cap split not reported; category-level assumption used")
        else:
            mc["unknown"] = eq
    prof.market_cap = {k: round(v, 6) for k, v in mc.items() if v > 0}
    # disclosed holdings
    th, disclosed = [], 0.0
    for h in holds:
        w = _pct(h.get("perc")) / 100.0
        if w <= 0 and not metals:
            # 0% rounds tiny holdings away; keep the name for duplicate detection with a minimal weight
            w = 0.0005
        th.append({"name": h.get("name", ""), "key": name_key(h.get("name", "")), "weight": w, "sector": canon_sector(h.get("sector")) if h.get("sector") else "", "country": _holding_country(h.get("name", ""))})
        disclosed += w
    prof.top_holdings, prof.disclosed_fraction = th, round(disclosed, 6)
    # country
    if eq <= 0:
        prof.country = {"IN": 1.0}
    elif re.search(r"nasdaq|s&p ?500|\bus\b", txt):
        prof.country = {"US": 1.0}
        prof.assumptions.append("country from benchmark/name (US index)")
    elif re.search(r"nifty|sensex|\bbse\b|india|infrastructure|digital india", txt) and not re.search(r"global|international", txt):
        prof.country = {"IN": 1.0}
        prof.assumptions.append("country from benchmark/name (India index/sector)")
    elif th:
        cw = defaultdict(float)
        for t in th:
            cw[t["country"]] += t["weight"]
        s = sum(cw.values()) or 1.0
        prof.country = {k: v / s * eq for k, v in cw.items()}
        for k, v in (prof.asset_mix.items()):
            if k != "equity":
                prof.country["IN"] = prof.country.get("IN", 0.0) + v
        prof.assumptions.append("country mix extrapolated from the disclosed holdings sample (estimate)")
    else:
        prof.country = {"IN": 1.0}
    if metals or (disclosed >= 0.9):
        prof.quality = "full"
    elif prof.sector and prof.market_cap:
        prof.quality = "partial"
    else:
        prof.quality = "category"
    if prof.quality == "partial":
        prof.assumptions.append(f"stock-level look-through covers only {disclosed * 100:.0f}% of the fund (source lists ~{len(th)} arbitrary holdings); sector and market-cap splits are complete")
    return prof


# =====================================================================================================================
# IndMoney snapshot normaliser
# =====================================================================================================================
def _unwrap(x: Any) -> Any:
    """Tool responses arrive as {'result': '<json string>'}; accept that or the already-parsed dict."""
    if isinstance(x, str):
        try:
            x = json.loads(x)
        except ValueError:
            return x
    if isinstance(x, dict) and set(x.keys()) == {"result"}:
        return _unwrap(x["result"])
    return x


def _slug_name(s: str) -> str:
    return " ".join(w.capitalize() for w in re.split(r"[-_ ]+", s or "") if w)


def normalise_indmoney_snapshot(raw: dict, fund_details: Any = None, overrides: Optional[dict] = None) -> Portfolio:
    """Normalise responses of the READ-ONLY IndMoney tools into a Portfolio.

    raw = {
      "holdings": {"MF": <networth_holdings MF>, "US_STOCK": <...>, "IND_STOCK": <...>, "BOND": <...> (any asset_type the tool supports)},
      "esops_rsus": <get_family_asset_holdings asset=esops_rsus>,          (optional; also 'family_holdings': {asset: resp} for gold/fd/epf/... )
      "snapshot": <networth_snapshot>,                                       (optional; used for reconciliation and for cash-like totals with no rows)
      "us_details": {symbol: {sector, market_cap, name}} or <get_us_stocks_details response>   (optional; sector / cap for US stocks)
    }
    fund_details = get_mf_funds_details response (with includes asset_allocation, sector_allocation, holdings), or None.
    overrides = {'sector': {name: sector}, 'market': {name: 'US'}, 'market_cap': {name: 'large'}} user-maintained (private/overrides.json).
    Observed row shapes: MF rows {investment_code (scheme id), investment, assetclass_l2, invested_amount, market_value (INR), total_units, unit_price (NAV)};
    US_STOCK rows add invested_value_usd/current_value_usd and a market_cap string, unit_price is INR per unit. IND_STOCK rows are assumed to follow the
    same row shape (the account used to develop this had none).
    """
    overrides = overrides or {}
    pf = Portfolio(source="indmoney", as_of=str(raw.get("as_of", "")))
    hold = {k: _unwrap(v) for k, v in (raw.get("holdings") or {}).items()}
    usd = {}
    us_det = _unwrap(raw.get("us_details") or {})
    for sym, d in (us_det or {}).items():
        eb = d.get("entity_basic", d) if isinstance(d, dict) else {}
        usd[str(sym).upper()] = {"sector": eb.get("sector", ""), "market_cap": eb.get("market_cap", ""), "name": eb.get("name", "")}
    # fund profiles
    fd = _unwrap(fund_details) if fund_details is not None else None
    fund_data = {}
    if isinstance(fd, dict):
        for e in fd.get("data", []) or []:
            fund_data[str(e.get("fund_id"))] = e.get("data", {})

    ov_sector = {name_key(k): v for k, v in (overrides.get("sector") or {}).items()}
    ov_market = {name_key(k): v for k, v in (overrides.get("market") or {}).items()}
    ov_mcap = {name_key(k): v for k, v in (overrides.get("market_cap") or {}).items()}
    implied_fx = []

    for atype, resp in hold.items():
        rows = (resp or {}).get("holdings", []) if isinstance(resp, dict) else []
        for r in rows:
            code, nm = str(r.get("investment_code", "")), str(r.get("investment", ""))
            vinr = float(r.get("market_value") or 0.0)
            qty = r.get("total_units")
            inv_inr = r.get("invested_amount")
            if atype == "MF":
                kind = "etf" if re.search(r"(?i)\betf\b|bees\b", nm) else "mutual_fund"
                h = Holding(instrument_id=code, name=nm, kind=kind, market="IN", currency="INR", quantity=qty, avg_cost=(inv_inr / qty if qty and inv_inr is not None else None),
                            price=r.get("unit_price"), value_local=vinr, value_inr=vinr, asset_class=_infer_asset_class(str(r.get("assetclass_l2", "")).replace("global_equity", "equity"), kind, nm),
                            category="", source="indmoney:MF", fx_rate=1.0)
                fdat = fund_data.get(code)
                if fdat is not None:
                    prof = fund_profile_from_indmoney(code, fdat, nm)
                    h.category = prof.category
                    pf.fund_profiles[code] = prof
                    h.themes = sorted(set(h.themes))
                    if prof.asset_mix.get("gold", 0) > 0.9:
                        h.asset_class = "gold"
                else:
                    pf.notes.append("a mutual fund had no get_mf_funds_details data; category-level look-through used")
                pf.holdings.append(h)
            elif atype == "US_STOCK":
                sym = code.upper()
                vusd = r.get("current_value_usd")
                fx = (vinr / vusd) if vusd else None
                if fx:
                    implied_fx.append(fx)
                det = usd.get(sym, {})
                mcap = canon_mcap(r.get("market_cap")) or canon_mcap(det.get("market_cap"))
                sector = canon_sector(det.get("sector")) if det.get("sector") else SECTOR_BY_TICKER.get(sym, "Unclassified")
                h = Holding(instrument_id=sym, name=nm, kind="stock", market="US", currency="USD", quantity=qty,
                            avg_cost=(r["invested_value_usd"] / qty if qty and r.get("invested_value_usd") is not None else None),
                            price=(vusd / qty if qty and vusd else None), value_local=vusd, value_inr=vinr, sector=sector, industry=INDUSTRY_BY_TICKER.get(sym, ""),
                            asset_class="equity", market_cap_bucket=mcap, source="indmoney:US_STOCK", fx_rate=fx)
                h.themes = tag_themes(sym, nm, sector, h.industry)
                pf.holdings.append(h)
            else:  # IND_STOCK, BOND, EPF, NPS, FD, ... assumed to share the row shape
                kind = {"IND_STOCK": "stock", "BOND": "bond"}.get(atype, "other")
                h = Holding(instrument_id=code or nm, name=nm, kind=kind, market="IN", currency="INR", quantity=qty, avg_cost=(inv_inr / qty if qty and inv_inr is not None else None),
                            price=r.get("unit_price"), value_local=vinr, value_inr=vinr, asset_class=("equity" if kind == "stock" else "debt" if kind == "bond" else "other"),
                            market_cap_bucket=canon_mcap(r.get("market_cap")), source=f"indmoney:{atype}", fx_rate=1.0)
                if kind == "stock":
                    h.sector = SECTOR_BY_TICKER.get(base_ticker(code), "Unclassified")
                    h.themes = tag_themes(code, nm, h.sector)
                pf.holdings.append(h)
        if isinstance(resp, dict) and any(resp.get(k) for k in ("derivative_positions", "positions", "mtf_positions")):
            pf.notes.append("IND_STOCK response contained F&O/derivative/position data; it is not included in holdings analytics")

    usdinr = sorted(implied_fx)[len(implied_fx) // 2] if implied_fx else None

    def family_rows(resp):
        resp = _unwrap(resp)
        out = []
        for m in (resp or {}).get("family_asset_holdings", []) or []:
            if m.get("is_you", True):
                out += m.get("holdings", []) or []
        return out

    # ESOP / RSU rows (family_asset_holdings shape: name slug, current_value INR, quantity, unit_price INR)
    for r in family_rows(raw.get("esops_rsus")) if raw.get("esops_rsus") else []:
        nm = _slug_name(str(r.get("name", "")))
        key = name_key(nm)
        market = ov_market.get(key) or ("US" if re.search(r"(?i)\b(corp|inc|incorporated|plc|co)\b", nm) and not re.search(r"(?i)\b(ltd|limited|india)\b", nm) else "IN")
        sector = ov_sector.get(key, "Unclassified")
        v = float(r.get("current_value") or 0.0)
        pf.holdings.append(Holding(instrument_id=str(r.get("name", nm)), name=nm, kind="stock", market=market, currency="INR", quantity=r.get("quantity"), price=r.get("unit_price"),
                                   value_local=v, value_inr=v, sector=sector, themes=tag_themes("", nm, sector), asset_class="equity", market_cap_bucket=canon_mcap(ov_mcap.get(key)), source="indmoney:esops_rsus",
                                   notes=["ESOP/RSU: market assumed from issuer name unless overridden; ticker unknown; value reported in INR only"]))
    for asset, resp in (raw.get("family_holdings") or {}).items():
        for r in family_rows(resp):
            v = float(r.get("current_value") or 0.0)
            nm = _slug_name(str(r.get("name", asset)))
            ac = {"gold": "gold", "silver": "gold", "fd": "debt", "bond": "debt", "ppf": "debt", "epf": "debt", "savings_account": "cash", "cash_investments": "cash"}.get(asset, "other")
            pf.holdings.append(Holding(instrument_id=str(r.get("name", nm)), name=nm, kind="bond" if ac == "debt" else "other", market="IN", currency="INR", quantity=r.get("quantity"),
                                       value_local=v, value_inr=v, asset_class=ac, source=f"indmoney:{asset}", fx_rate=1.0))

    # cash-like asset types that only appear as totals in the snapshot (savings accounts, wallets)
    snap = _unwrap(raw.get("snapshot")) if raw.get("snapshot") else None
    covered = {"MF", "US_STOCK", "ESOPS_RSUS", "IND_STOCK", "BOND"} | set(hold.keys())
    if isinstance(snap, dict):
        for inv in snap.get("investments", []) or []:
            at = str(inv.get("asset_type", ""))
            v = float(inv.get("current_value") or 0.0)
            if at in covered or v <= 0:
                continue
            if at == "US_STOCK_WALLET":
                pf.holdings.append(Holding(instrument_id=at, name="US stock wallet (cash)", kind="other", market="US", currency="USD", value_inr=v, value_local=(v / usdinr if usdinr else None),
                                           asset_class="cash", source="indmoney:snapshot", fx_rate=usdinr))
            else:
                pf.holdings.append(Holding(instrument_id=at, name=f"{at} (total only)", kind="other", market="IN", currency="INR", value_inr=v, value_local=v,
                                           asset_class="cash" if at in ("SA",) else "other", source="indmoney:snapshot", fx_rate=1.0))
        tw = snap.get("total_networth")
        if tw:
            s = pf.total_inr()
            pf.reconciliation = {"sum_of_holdings_inr": round(s, 2), "snapshot_total_inr": round(float(tw), 2), "difference_pct": round((s - float(tw)) / float(tw) * 100, 3)}
    if usdinr:
        pf.notes.append(f"USD/INR implied by US holdings: {usdinr:.2f}")
    pf.notes.append("IndMoney exposes ~20 arbitrary holdings per fund; stock-level look-through is partial (see FundProfile.quality)")
    return pf


# =====================================================================================================================
# Analytics
# =====================================================================================================================
def _acc_add(d: dict, k: str, v: float) -> None:
    d[k] = d.get(k, 0.0) + v


def _composition(h: Holding, prof: Optional[FundProfile]) -> dict:
    v = h.value_inr or 0.0
    if h.kind in ("mutual_fund", "etf"):
        if prof is None:
            prof = category_profile(h.instrument_id, h.name, h.category)
        eq = prof.asset_mix.get("equity", 0.0)
        return {"asset": prof.asset_mix, "sector": prof.sector, "mcap": prof.market_cap, "country": prof.country, "legs": prof.top_holdings, "quality": prof.quality,
                "disclosed": prof.disclosed_fraction, "equity": eq, "prof": prof}
    if h.kind == "stock":
        return {"asset": {"equity": 1.0}, "sector": {canon_sector(h.sector): 1.0}, "mcap": {h.market_cap_bucket or "unknown": 1.0}, "country": {h.market or "OTHER": 1.0},
                "legs": [], "quality": "direct", "disclosed": 1.0, "equity": 1.0, "prof": None}
    ac = h.asset_class if h.asset_class in ASSET_CLASSES else "other"
    return {"asset": {ac: 1.0}, "sector": {"Commodity" if ac == "gold" else "Debt & Cash" if ac in ("debt", "cash") else "Other": 1.0}, "mcap": {}, "country": {h.market or "IN": 1.0},
            "legs": [], "quality": "direct", "disclosed": 1.0, "equity": 0.0, "prof": None}


def _round_map(d: dict, total: float, nd: int = 2) -> dict:
    return {k: round(v / total * 100, nd) for k, v in sorted(d.items(), key=lambda kv: -kv[1]) if v / total * 100 >= 0.005}


def analyze_portfolio(pf: Portfolio, top_n: int = 10) -> dict:
    """All exposures are percentages of TOTAL portfolio value (INR). JSON-serialisable. Contains holding names: keep it under private/."""
    total = pf.total_inr()
    if not pf.holdings or total <= 0:
        return {"total_value_inr": 0.0, "n_holdings": 0, "empty": True, "warnings": ["no holdings"], "look_through_quality": {}}
    asset, sector, mcap, country, ccy_held, ccy_econ, industry = ({} for _ in range(7))
    stock = {}      # key -> {name, tickers, direct, indirect, sources{holding:value}}
    theme = {}      # theme -> {direct, lower, est}
    quality_w = {}
    kind_w = {}
    fund_names = {}
    E_ECON = {"IN": "INR", "US": "USD"}
    legs_by_fund = {}
    eq_total = 0.0
    for h in pf.holdings:
        v = h.value_inr or 0.0
        if v <= 0:
            continue
        c = _composition(h, pf.fund_profiles.get(h.instrument_id))
        _acc_add(kind_w, h.kind, v)
        _acc_add(quality_w, c["quality"] if h.kind in ("mutual_fund", "etf") else "direct", v)
        _acc_add(ccy_held, h.currency or "INR", v)
        for k, f in c["asset"].items():
            _acc_add(asset, k, v * f)
        for k, f in c["sector"].items():
            _acc_add(sector, k, v * f)
        for k, f in c["mcap"].items():
            _acc_add(mcap, k, v * f)
        for k, f in c["country"].items():
            _acc_add(country, k, v * f)
            _acc_add(ccy_econ, E_ECON.get(k, "OTHER"), v * f)
        eq_total += v * c["equity"]
        if h.kind == "stock":
            _acc_add(industry, h.industry or f"{canon_sector(h.sector)} (industry not reported)", v)
            key = name_key(h.name)
            e = stock.setdefault(key, {"name": h.name, "tickers": set(), "direct": 0.0, "indirect": 0.0, "sources": {}})
            e["direct"] += v
            e["tickers"].add(base_ticker(h.instrument_id))
            e["sources"][h.name] = e["sources"].get(h.name, 0.0) + v
            for t in h.themes or tag_themes(h.instrument_id, h.name, h.sector, h.industry):
                d = theme.setdefault(t, {"direct": 0.0, "lower": 0.0, "est": 0.0})
                d["direct"] += v; d["lower"] += v; d["est"] += v
        elif h.kind in ("mutual_fund", "etf"):
            fund_names[h.instrument_id] = h.name
            prof = c["prof"]
            eqv = v * c["equity"]
            disc = sum(t["weight"] for t in c["legs"])
            legs_by_fund[h.instrument_id] = {t["key"]: t["weight"] * v for t in c["legs"]}
            tw = {}
            for t in c["legs"]:
                lv = t["weight"] * v
                key = t["key"]
                e = stock.setdefault(key, {"name": t["name"], "tickers": set(), "direct": 0.0, "indirect": 0.0, "sources": {}})
                e["indirect"] += lv
                e["sources"][h.name] = e["sources"].get(h.name, 0.0) + lv
                for th in tag_themes("", t["name"], t.get("sector", "")):
                    tw[th] = tw.get(th, 0.0) + lv
            for th, lv in tw.items():
                d = theme.setdefault(th, {"direct": 0.0, "lower": 0.0, "est": 0.0})
                d["lower"] += lv
                d["est"] += eqv * (lv / (disc * v)) if disc * v > 0 and disc >= 0.02 else lv
            txt = f"{h.name} {h.category} {prof.category if prof else ''}".lower()
            for rx, ths in CATEGORY_THEMES:
                if rx.search(txt):
                    for th in ths:
                        d = theme.setdefault(th, {"direct": 0.0, "lower": 0.0, "est": 0.0})
                        # category-level floor: the fund's whole equity (or metals) sleeve is tagged; never double count with the sampled estimate
                        d["est"] = max(d["est"], d["direct"] + eqv + (v * c["asset"].get("gold", 0.0) if th == "precious_metals" else 0.0))
    # theme est can double count direct+fund; fine because direct and fund parts are separate holdings, but cap at total
    for d in theme.values():
        d["est"] = min(d["est"], total)
        d["lower"] = min(d["lower"], total)

    # concentration over direct (position-level) weights
    pos = sorted(((h.name, h.kind, (h.value_inr or 0.0) / total) for h in pf.holdings if (h.value_inr or 0) > 0), key=lambda x: -x[2])
    hhi = sum(w * w for _, _, w in pos)
    # stock-level effective exposure (direct + disclosed look-through = lower bound)
    eff = sorted(((e["name"], (e["direct"] + e["indirect"]) / total) for e in stock.values()), key=lambda x: -x[1])
    sec_eq = {k: v for k, v in sector.items() if k not in ("Debt & Cash", "Commodity", "Other")}
    sec_tot = sum(sec_eq.values()) or 1.0
    sector_hhi = sum((v / sec_tot) ** 2 for v in sec_eq.values())
    conc = {"top_positions": [{"name": n, "kind": k, "weight_pct": round(w * 100, 2)} for n, k, w in pos[:top_n]],
            "top1_pct": round(pos[0][2] * 100, 2), "top3_pct": round(sum(w for *_, w in pos[:3]) * 100, 2), "top5_pct": round(sum(w for *_, w in pos[:5]) * 100, 2),
            "top10_pct": round(sum(w for *_, w in pos[:10]) * 100, 2), "hhi_positions": round(hhi, 4), "effective_n_positions": round(1 / hhi, 2) if hhi else None,
            "hhi_equity_sectors": round(sector_hhi, 4), "effective_n_sectors": round(1 / sector_hhi, 2) if sector_hhi else None,
            "top_underlying_stocks_lower_bound": [{"name": n, "weight_pct": round(w * 100, 2)} for n, w in eff[:top_n]],
            "note": "underlying stock weights are a lower bound: funds disclose only a sample of their holdings"}

    stock_list = []
    for key, e in stock.items():
        tot = e["direct"] + e["indirect"]
        stock_list.append({"key": key, "name": e["name"], "tickers": sorted(t for t in e["tickers"] if t), "direct_pct": round(e["direct"] / total * 100, 3),
                           "indirect_pct": round(e["indirect"] / total * 100, 3), "total_pct": round(tot / total * 100, 3), "n_sources": len(e["sources"]),
                           "sources": {k: round(v / total * 100, 3) for k, v in e["sources"].items()}})
    stock_list.sort(key=lambda x: -x["total_pct"])

    duplicates = [{"name": s["name"], "total_pct": s["total_pct"], "sources": s["sources"]} for s in stock_list if s["n_sources"] >= 2]

    # fund-pair overlap
    overlaps = []
    fids = [h.instrument_id for h in pf.holdings if h.kind in ("mutual_fund", "etf") and h.instrument_id in pf.fund_profiles]
    for i in range(len(fids)):
        for j in range(i + 1, len(fids)):
            a, b = pf.fund_profiles[fids[i]], pf.fund_profiles[fids[j]]
            shared = set(legs_by_fund.get(fids[i], {})) & set(legs_by_fund.get(fids[j], {}))
            same_bench = bool(a.benchmark and a.benchmark == b.benchmark)
            if same_bench or len(shared) >= 2:
                wa, wb = {t["key"]: t["weight"] for t in a.top_holdings}, {t["key"]: t["weight"] for t in b.top_holdings}
                ov = sum(min(wa[k], wb[k]) for k in shared)
                overlaps.append({"funds": [fund_names[fids[i]], fund_names[fids[j]]], "same_benchmark": same_bench, "shared_disclosed_names": len(shared),
                                 "overlap_of_disclosed_pct": round(ov * 100, 2),
                                 "combined_pct_of_portfolio": round((_val(pf, fids[i]) + _val(pf, fids[j])) / total * 100, 2)})
    overlaps.sort(key=lambda x: (not x["same_benchmark"], -x["combined_pct_of_portfolio"]))

    th_out = {t: {"direct_pct": round(d["direct"] / total * 100, 2), "lower_bound_pct": round(d["lower"] / total * 100, 2), "estimated_pct": round(d["est"] / total * 100, 2),
                  "multiple_of_direct": (round(d["est"] / d["direct"], 2) if d["direct"] > 0 else None)} for t, d in sorted(theme.items(), key=lambda kv: -kv[1]["est"])}

    ql = {k: round(v / total * 100, 2) for k, v in quality_w.items()}
    fund_pct = sum(v for k, v in kind_w.items() if k in ("mutual_fund", "etf")) / total * 100
    lt_label = "none (no funds)" if fund_pct == 0 else ("full" if ql.get("full", 0) >= fund_pct - 0.01 else "partial" if ql.get("category", 0) + ql.get("none", 0) < fund_pct * 0.5 else "mostly category-level")
    out = {
        "total_value_inr": round(total, 2), "n_holdings": len(pf.holdings), "n_funds": len(fids), "empty": False,
        "by_kind": _round_map(kind_w, total), "by_asset_class": _round_map(asset, total),
        "by_sector": _round_map(sector, total), "by_industry_direct": _round_map(industry, total), "by_theme": th_out,
        "by_country": _round_map(country, total), "by_currency_held": _round_map(ccy_held, total), "by_currency_economic": _round_map(ccy_econ, total),
        "by_market_cap": _round_map(mcap, total),
        "direct_vs_indirect": {"direct_stocks_pct": round(kind_w.get("stock", 0) / total * 100, 2), "via_funds_pct": round(fund_pct, 2),
                               "other_pct": round((total - kind_w.get("stock", 0) - sum(v for k, v in kind_w.items() if k in ("mutual_fund", "etf"))) / total * 100, 2)},
        "equity_pct": round(eq_total / total * 100, 2),
        "concentration": conc, "stock_exposure": stock_list[:100], "duplicates": duplicates, "fund_overlaps": overlaps,
        "look_through_quality": {"label": lt_label, "pct_of_portfolio_by_quality": ql,
                                 "notes": sorted({a for p in pf.fund_profiles.values() for a in p.assumptions})},
    }
    out["warnings"] = _warnings(out)
    return out


def _val(pf: Portfolio, fid: str) -> float:
    return sum(h.value_inr or 0.0 for h in pf.holdings if h.instrument_id == fid)


def _warnings(a: dict) -> list:
    w = []
    for t, d in a["by_theme"].items():
        label = t.replace("_", " ")
        if d["direct_pct"] >= 1.0 and d["multiple_of_direct"] and d["multiple_of_direct"] >= 1.5:
            w.append(f"Effective exposure to {label} is about {d['multiple_of_direct']:.1f} times your direct holdings (direct {d['direct_pct']:.1f}% of portfolio, "
                     f"~{d['estimated_pct']:.1f}% including fund look-through; look-through is an estimate from partially disclosed fund holdings).")
        elif d["direct_pct"] < 1.0 and d["estimated_pct"] >= 10.0:
            w.append(f"About {d['estimated_pct']:.1f}% of the portfolio is effectively exposed to {label}, almost entirely through funds rather than direct holdings (estimate).")
    for s in a["stock_exposure"]:
        if s["direct_pct"] >= 1.0 and s["indirect_pct"] > 0 and s["total_pct"] / s["direct_pct"] >= 1.5:
            w.append(f"Effective exposure to {s['name']} is {s['total_pct'] / s['direct_pct']:.1f} times your direct holding ({s['direct_pct']:.1f}% direct, {s['indirect_pct']:.1f}% via funds; lower bound).")
    for o in a["fund_overlaps"]:
        if o["same_benchmark"]:
            w.append(f"Two funds track the same benchmark ({o['funds'][0]} and {o['funds'][1]}), together {o['combined_pct_of_portfolio']:.1f}% of the portfolio: this is duplication, not diversification.")
    c = a["concentration"]
    if c["top1_pct"] >= 25:
        w.append(f"The largest single position is {c['top1_pct']:.0f}% of the portfolio. That can be a deliberate choice; just make sure it is one.")
    sec = {k: v for k, v in a["by_sector"].items() if k not in ("Debt & Cash", "Commodity", "Other", "Unclassified")}
    if sec:
        k, v = max(sec.items(), key=lambda kv: kv[1])
        if v >= 35:
            w.append(f"{k} is {v:.0f}% of the portfolio (look-through).")
    return w


# =====================================================================================================================
# Candidate fit
# =====================================================================================================================
MAX_WEIGHT_BY_CAP = {"large": 8.0, "mid": 5.0, "small": 3.0, "micro": 1.0, "": 4.0}
THEME_CEILING_PCT = 50.0


def _clip(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _novelty_crowd(e: float, nov_full: float, crowd_start: float, crowd_full: float) -> float:
    """1.0 when the exposure is absent, 0.5 around nov_full, falling towards 0 as the exposure grows past crowd_full."""
    novelty = _clip(1 - e / nov_full)
    crowd = _clip((e - crowd_start) / (crowd_full - crowd_start))
    return _clip(0.5 + 0.5 * novelty - 0.5 * crowd)


def fit_score(candidate: dict, portfolio_analytics: Optional[dict]) -> PortfolioFit:
    """candidate = {ticker, sector, themes[list], market, market_cap_bucket, name (optional), industry (optional)}.

    Returns schema.PortfolioFit. score is 0..1 where ~0.5 is neutral, higher means the position adds something the portfolio lacks, lower means it
    mostly adds to what you already own heavily. It is a TRADEOFF indicator, not a verdict: concentration in a thesis you hold with conviction can
    be appropriate, and diversification is not automatically good. With no portfolio the score is None.
    """
    if not portfolio_analytics or portfolio_analytics.get("empty") or not portfolio_analytics.get("total_value_inr"):
        return PortfolioFit(score=None, summary="No portfolio is available (nothing imported yet), so portfolio fit cannot be assessed. Import holdings to see overlap and concentration effects.",
                            overlap_notes=[], suggested_max_weight_pct=None)
    a = portfolio_analytics
    tk = base_ticker(candidate.get("ticker", ""))
    nm = candidate.get("name") or TICKER_NAME_ALIASES.get(tk, "")
    ckey = name_key(nm) if nm else ""
    themes = [str(t).lower().replace(" ", "_") for t in (candidate.get("themes") or [])] or tag_themes(tk, nm, candidate.get("sector", ""), candidate.get("industry", ""))
    sector = canon_sector(candidate.get("sector")) if candidate.get("sector") else ""
    market = str(candidate.get("market") or "").upper()
    cap = canon_mcap(candidate.get("market_cap_bucket"))
    notes, parts, summary_bits = [], [], []
    lt = a.get("look_through_quality", {}).get("label", "")

    # 1 themes (weight .35)
    cur_theme = {}
    if themes:
        scs = []
        for t in themes:
            e = a["by_theme"].get(t, {}).get("estimated_pct", 0.0)
            cur_theme[t] = e
            scs.append(_novelty_crowd(e, 10.0, 20.0, 50.0))
            d = a["by_theme"].get(t, {})
            if e < 2.0:
                notes.append(f"Theme '{t}': essentially absent from the portfolio ({e:.1f}%); this would add a missing exposure.")
            elif e >= 20.0:
                m = f", {d['multiple_of_direct']:.1f}x your direct holdings" if d.get("multiple_of_direct") else ""
                notes.append(f"Theme '{t}': already ~{e:.0f}% of the portfolio including fund look-through{m}; this would add to an existing concentration.")
            else:
                notes.append(f"Theme '{t}': currently ~{e:.0f}% of the portfolio (moderate).")
        parts.append((0.35, sum(scs) / len(scs)))
    # 2 sector (.25)
    if sector:
        e = a["by_sector"].get(sector, 0.0)
        parts.append((0.25, _novelty_crowd(e, 15.0, 30.0, 60.0)))
        if e >= 30:
            notes.append(f"Sector '{sector}' is already {e:.0f}% of the portfolio.")
        elif e < 3:
            notes.append(f"Sector '{sector}' is nearly absent ({e:.1f}%).")
    # 3 same company already held (.15)
    held = None
    for s in a.get("stock_exposure", []):
        if (ckey and s["key"] == ckey) or (tk and tk in s.get("tickers", [])):
            held = s
            break
    if held:
        tot = held["total_pct"]
        parts.append((0.15, _clip(1 - tot / 8.0) * 0.8))
        via = f" ({held['direct_pct']:.1f}% direct, {held['indirect_pct']:.1f}% via funds)" if held["indirect_pct"] else ""
        notes.append(f"You already own this company: ~{tot:.1f}% of the portfolio{via}; adding more raises single-name concentration.")
    elif ckey or tk:
        parts.append((0.15, 1.0))
    # 4 market/country (.10)
    if market:
        e = a["by_country"].get(market, 0.0)
        parts.append((0.10, _novelty_crowd(e, 10.0, 70.0, 95.0)))
        if e >= 80:
            notes.append(f"{e:.0f}% of the portfolio is already in {market}-exposed assets.")
        elif e < 5:
            notes.append(f"Almost nothing ({e:.1f}%) is currently {market}-exposed.")
    # 5 market-cap (.15)
    if cap:
        e = a["by_market_cap"].get(cap, 0.0)
        eq = max(a.get("equity_pct", 0.0), 1e-9)
        share = e / eq * 100
        parts.append((0.15, _novelty_crowd(share, 15.0, 55.0, 85.0)))
        if share < 10:
            notes.append(f"{cap.capitalize()}-cap is only ~{share:.0f}% of your equity exposure.")
    if not parts:
        score = 0.5
        summary = "The candidate carries no sector, theme, market or market-cap information, so only a neutral fit can be reported. Fill those fields for a meaningful assessment."
        return PortfolioFit(score=0.5, summary=summary, overlap_notes=notes, suggested_max_weight_pct=MAX_WEIGHT_BY_CAP.get(cap, 4.0))
    wsum = sum(w for w, _ in parts)
    score = round(_clip(sum(w * s for w, s in parts) / wsum), 2)

    # suggested max weight: size cap, scaled by fit, limited by headroom under the theme ceiling
    base = MAX_WEIGHT_BY_CAP.get(cap, MAX_WEIGHT_BY_CAP[""])
    mw = base * (0.5 + score)
    headroom_flags = []
    for t, e in cur_theme.items():
        room = THEME_CEILING_PCT - e
        if room < mw:
            mw = max(room, 0.0)
            headroom_flags.append(t)
    mw = round(max(mw, 0.5 if score >= 0.15 and not headroom_flags else 0.0) * 2) / 2
    if headroom_flags and mw < 1.0:
        notes.append("Theme headroom under a 50% ceiling is nearly used up: a new position here mostly raises an exposure you already have a lot of.")

    crowded = [t for t, e in cur_theme.items() if e >= 20]
    missing = [t for t, e in cur_theme.items() if e < 2]
    if held and held["total_pct"] >= 4:
        lead = f"This is mainly an add-on to a company you already effectively own at ~{held['total_pct']:.1f}% of the portfolio."
    elif crowded and not missing:
        lead = f"This leans into themes you already hold heavily ({', '.join(crowded)}). That can be a deliberate, high-conviction concentration, but it adds correlated risk rather than new exposure."
    elif missing and not crowded:
        lead = f"This would add exposure the portfolio largely lacks ({', '.join(missing)}), which improves breadth, though a gap is not by itself a reason to buy."
    elif crowded and missing:
        lead = f"Mixed: it adds a missing theme ({', '.join(missing)}) but also stacks on a crowded one ({', '.join(crowded)})."
    else:
        lead = "It sits roughly in line with the existing mix: neither a clear diversifier nor a major concentration."
    summary = (f"{lead} Fit score {score:.2f} (0..1; about 0.5 is neutral). Suggested maximum position about {mw:g}% of the portfolio as a heuristic from market-cap risk and "
               f"headroom under a {THEME_CEILING_PCT:.0f}% theme ceiling. Concentration can be appropriate and diversification is not always better; the score shows the tradeoff, it does not decide it.")
    if lt and lt != "full":
        notes.append(f"Fund look-through quality is '{lt}': exposures through funds are estimates from partially disclosed holdings.")
    return PortfolioFit(score=score, summary=summary, overlap_notes=notes, suggested_max_weight_pct=mw)


# =====================================================================================================================
# Private snapshot builder (CLI):  python -m mblab.portfolio build-snapshot
# =====================================================================================================================
def build_private_snapshot(raw_path: Optional[Path] = None) -> dict:
    """Read private/raw/indmoney_raw.json (+ fund details) -> private/portfolio_snapshot.json and private/portfolio_analytics.json.
    Returns ONLY aggregate counts/shape (safe to print)."""
    raw_path = Path(raw_path or PRIVATE_DIR / "raw" / "indmoney_raw.json")
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    fd = None
    if raw.get("fund_details_file"):
        fd = json.loads((raw_path.parent / raw["fund_details_file"]).read_text(encoding="utf-8"))
    ovp = PRIVATE_DIR / "overrides.json"
    ov = json.loads(ovp.read_text(encoding="utf-8")) if ovp.exists() else {}
    pf = normalise_indmoney_snapshot(raw, fd, ov)
    ana = analyze_portfolio(pf)
    write_private(pf.to_dict(), "portfolio_snapshot.json")
    write_private(ana, "portfolio_analytics.json")
    return {"holdings": len(pf.holdings), "by_kind": ana["by_kind"], "n_funds": ana["n_funds"], "fund_profiles": len(pf.fund_profiles),
            "look_through": ana["look_through_quality"]["label"], "reconciliation_diff_pct": pf.reconciliation.get("difference_pct"), "n_warnings": len(ana["warnings"]),
            "themes_found": len(ana["by_theme"]), "n_duplicate_names": len(ana["duplicates"]), "n_fund_overlaps": len(ana["fund_overlaps"])}


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "build-snapshot":
        print(json.dumps(build_private_snapshot(), indent=1))
    else:
        print("usage: python -m mblab.portfolio build-snapshot   (reads private/raw/indmoney_raw.json; writes only under private/)")
