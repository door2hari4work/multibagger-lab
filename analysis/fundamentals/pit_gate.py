"""Point-in-time fundamentals gate (Agent 4).

Gate = EBITDA-margin trend improving + revenue/EBITDA growth + OCF/EBITDA cash quality,
with financials (banks/NBFCs/insurers) excluded because EBITDA is meaningless for them.

NO-LOOK-AHEAD CONTRACT
  * A reported period becomes usable on its `filed_date`; if that is missing, on
    `period_end + QUARTERLY_LAG_DAYS` (period_type 'Q') or `+ ANNUAL_LAG_DAYS` ('A'), from config.py.
  * Eligibility at rebalance date d depends ONLY on rows with usable_date <= d (inclusive).
  * ORIGINAL values: if a (symbol, period_type, period_end) appears more than once (restatements), only the
    earliest-filed version is ever used; a later restatement can neither change values nor availability.
  * Nothing is ever back-filled, forward-filled across missing quarters, or inferred from later data.
  * Missing/insufficient data => NOT eligible (reason recorded). Silence is never read as "pass".

INPUT (long table, one row per symbol x reported period; see reports/4_fundamentals_tester.md)
  symbol, period_end, [filed_date], revenue, ebitda, ocf, [capex], [period_type 'Q'|'A' (default 'Q')], [sector]
  Quarterly rows must be single-quarter figures (Q4 = FY - 9M if the company only files FY), in Rs.

THIS MODULE HAS NOT BEEN RUN ON REAL DATA (none exists in the repo). See the report.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from datetime import date
import numpy as np
import pandas as pd
import config

FINANCIAL_KEYWORDS = ("financ", "bank", "nbfc", "insur", "housing finance", "asset management", "broking")

REQUIRED = ["symbol", "period_end", "revenue", "ebitda", "ocf"]


@dataclass(frozen=True)
class GateParams:
    quarterly_lag_days: int = config.QUARTERLY_LAG_DAYS
    annual_lag_days: int = config.ANNUAL_LAG_DAYS
    force_lag: bool = False            # True: ignore filed_date and use period_end + lag (for lag-sensitivity tests)
    min_margin_delta: float = 0.0      # EBITDA margin (TTM / FY) must exceed year-ago by MORE than this (abs, e.g. 0.005)
    min_rev_growth: float = 0.10       # YoY TTM / FY revenue growth, >=
    min_ebitda_growth: float = 0.10    # YoY TTM / FY EBITDA growth, >=
    min_ocf_ebitda: float = 0.50       # OCF / EBITDA, >=  (cash quality)
    require_fcf_positive: bool = False # if True and `capex` supplied: OCF - capex > 0
    max_staleness_days: int = 200      # latest usable Q period_end must be this recent, else data counts as stale
    exclude_financials: bool = True
    unknown_sector: str = "allow"      # 'allow' | 'exclude' when no sector given for a symbol


def is_financial(sector) -> bool:
    if sector is None or (isinstance(sector, float) and np.isnan(sector)):
        return False
    s = str(sector).lower()
    return any(k in s for k in FINANCIAL_KEYWORDS)


def prepare(fund: pd.DataFrame, params: GateParams = GateParams()) -> pd.DataFrame:
    """Validate, keep ORIGINAL (earliest-filed) version per period, attach usable_date. No future information used."""
    missing = [c for c in REQUIRED if c not in fund.columns]
    if missing:
        raise ValueError(f"fundamentals table missing columns: {missing}")
    f = fund.copy()
    f["period_end"] = pd.to_datetime(f["period_end"])
    f["filed_date"] = pd.to_datetime(f["filed_date"]) if "filed_date" in f else pd.NaT
    if "period_type" not in f:
        f["period_type"] = "Q"
    f["period_type"] = f["period_type"].astype(str).str.upper().str[0]
    if not f["period_type"].isin(["Q", "A"]).all():
        raise ValueError("period_type must be 'Q' or 'A'")
    bad = f["filed_date"].notna() & (f["filed_date"] < f["period_end"])
    if bad.any():
        raise ValueError(f"{int(bad.sum())} rows have filed_date before period_end (corrupt dates)")
    lag = np.where(f["period_type"] == "Q", params.quarterly_lag_days, params.annual_lag_days)
    lag_date = f["period_end"] + pd.to_timedelta(lag, unit="D")
    use_filed = f["filed_date"].notna() & (not params.force_lag)
    f["usable_date"] = np.where(use_filed, f["filed_date"], lag_date)
    f["usable_date"] = pd.to_datetime(f["usable_date"])
    # originally reported value = earliest usable version of the same period; later restatements are discarded
    f["_ord"] = np.arange(len(f))
    f = f.sort_values(["symbol", "period_type", "period_end", "usable_date", "_ord"])
    f = f.drop_duplicates(["symbol", "period_type", "period_end"], keep="first")
    return f.drop(columns="_ord").reset_index(drop=True)


def _contiguous_quarters(pe: pd.Series) -> bool:
    gaps = pe.sort_values().diff().dropna().dt.days
    return bool(((gaps >= 75) & (gaps <= 105)).all())


def _evaluate_symbol(rows: pd.DataFrame, d: pd.Timestamp, p: GateParams):
    """rows: prepared rows of ONE symbol already filtered to usable_date <= d. Returns (eligible, reason, diag)."""
    diag = dict(trend_basis=None, rev_g=np.nan, ebitda_g=np.nan, margin_now=np.nan, margin_prev=np.nan,
                ocf_ebitda=np.nan, asof_period_end=pd.NaT)
    q = rows[rows.period_type == "Q"].sort_values("period_end", ascending=False)
    a = rows[rows.period_type == "A"].sort_values("period_end", ascending=False)

    ocf_ratio = None
    fcf_ok = True
    have_q = False
    if len(q) >= 8:
        q8 = q.head(8)
        if (d - q8.period_end.iloc[0]).days <= p.max_staleness_days and _contiguous_quarters(q8.period_end) \
                and q8[["revenue", "ebitda"]].notna().all().all():
            now, prev = q8.iloc[:4], q8.iloc[4:]
            have_q = True
            rev_n, rev_p = now.revenue.sum(), prev.revenue.sum()
            e_n, e_p = now.ebitda.sum(), prev.ebitda.sum()
            diag["trend_basis"] = "TTM"
            diag["asof_period_end"] = q8.period_end.iloc[0]
            if now.ocf.notna().all():
                ocf_ratio = (now.ocf.sum() / e_n) if e_n > 0 else np.nan
                if p.require_fcf_positive and "capex" in now and now.capex.notna().all():
                    fcf_ok = (now.ocf.sum() - now.capex.abs().sum()) > 0
    if not have_q:
        if len(a) >= 2 and a.head(2)[["revenue", "ebitda"]].notna().all().all() \
                and 300 <= (a.period_end.iloc[0] - a.period_end.iloc[1]).days <= 430:
            now, prev = a.iloc[0], a.iloc[1]
            rev_n, rev_p, e_n, e_p = now.revenue, prev.revenue, now.ebitda, prev.ebitda
            diag["trend_basis"] = "FY"
            diag["asof_period_end"] = now.period_end
            if pd.notna(now.ocf):
                ocf_ratio = now.ocf / e_n if e_n > 0 else np.nan
                if p.require_fcf_positive and "capex" in a and pd.notna(now.capex):
                    fcf_ok = (now.ocf - abs(now.capex)) > 0
        else:
            return False, "insufficient_history", diag

    if rev_p <= 0 or rev_n <= 0:
        return False, "nonpositive_revenue", diag
    if e_p <= 0 or e_n <= 0:
        diag.update(margin_now=e_n / rev_n, margin_prev=e_p / rev_p)
        return False, "nonpositive_ebitda", diag
    m_n, m_p = e_n / rev_n, e_p / rev_p
    diag.update(rev_g=rev_n / rev_p - 1, ebitda_g=e_n / e_p - 1, margin_now=m_n, margin_prev=m_p)
    # cash quality: prefer latest usable annual OCF if quarterly OCF not supplied
    if ocf_ratio is None and len(a) and pd.notna(a.iloc[0].ocf) and pd.notna(a.iloc[0].ebitda) and a.iloc[0].ebitda > 0:
        ocf_ratio = a.iloc[0].ocf / a.iloc[0].ebitda
    diag["ocf_ebitda"] = np.nan if ocf_ratio is None else ocf_ratio

    if not (m_n - m_p > p.min_margin_delta):
        return False, "margin_not_improving", diag
    if diag["rev_g"] < p.min_rev_growth:
        return False, "revenue_growth_low", diag
    if diag["ebitda_g"] < p.min_ebitda_growth:
        return False, "ebitda_growth_low", diag
    if ocf_ratio is None or np.isnan(ocf_ratio):
        return False, "no_ocf_data", diag
    if ocf_ratio < p.min_ocf_ebitda:
        return False, "ocf_quality_low", diag
    if not fcf_ok:
        return False, "fcf_negative", diag
    return True, "pass", diag


def pit_eligibility(fund: pd.DataFrame, rebalance_dates, symbols=None, sectors=None,
                    params: GateParams = GateParams(), allow_post_tune: bool = False) -> pd.DataFrame:
    """Long frame (rebalance_date, symbol, eligible, reason, diagnostics...), one row per symbol per rebalance date.

    sectors: dict/Series symbol -> industry string (or a `sector` column in `fund`).
    symbols: universe to report on; defaults to every symbol in `fund`. Symbols with no data are ineligible ('no_data').
    Uses only rows with usable_date <= rebalance_date.
    """
    dates = pd.DatetimeIndex(pd.to_datetime(list(rebalance_dates)))
    if not allow_post_tune and len(dates) and dates.max() > pd.Timestamp(config.TUNE_END):
        raise ValueError(f"rebalance date {dates.max().date()} is after TUNE_END {config.TUNE_END}; tune window only")
    if "sector" in fund.columns and sectors is None:
        sectors = fund.dropna(subset=["sector"]).drop_duplicates("symbol").set_index("symbol")["sector"].to_dict()
    sectors = dict(sectors) if sectors is not None else {}
    prep = prepare(fund, params)
    syms = list(symbols) if symbols is not None else sorted(prep.symbol.unique())
    by_sym = {s: g for s, g in prep.groupby("symbol")}
    out = []
    for s in syms:
        sec = sectors.get(s)
        fin = is_financial(sec)
        unknown = sec is None or (isinstance(sec, float) and np.isnan(sec))
        g = by_sym.get(s)
        for d in dates:
            base = dict(rebalance_date=d, symbol=s)
            if params.exclude_financials and fin:
                out.append({**base, "eligible": False, "reason": "financials_excluded"}); continue
            if params.exclude_financials and unknown and params.unknown_sector == "exclude":
                out.append({**base, "eligible": False, "reason": "unknown_sector"}); continue
            if g is None:
                out.append({**base, "eligible": False, "reason": "no_data"}); continue
            avail = g[g.usable_date <= d]            # <-- the ONLY place data is admitted
            if avail.empty:
                out.append({**base, "eligible": False, "reason": "no_data"}); continue
            ok, why, diag = _evaluate_symbol(avail, d, params)
            out.append({**base, "eligible": bool(ok), "reason": why, **diag})
    return pd.DataFrame(out)


def eligibility_matrix(elig: pd.DataFrame) -> pd.DataFrame:
    """dates x symbols boolean matrix, ready to AND with a backtest candidate mask at month-end."""
    return elig.pivot(index="rebalance_date", columns="symbol", values="eligible").astype(bool)


def coverage(elig: pd.DataFrame) -> dict:
    """Share of (symbol, date) pairs the gate could actually EVALUATE (had enough PIT data), excluding financials.
    Low coverage => any with/without comparison is a biased subset."""
    nonfin = elig[elig.reason != "financials_excluded"]
    evaluable = ~nonfin.reason.isin(["no_data", "insufficient_history", "unknown_sector"])
    return dict(n_pairs=int(len(nonfin)), evaluable_pct=float(100 * evaluable.mean()) if len(nonfin) else 0.0,
                pass_pct_of_evaluable=float(100 * nonfin[evaluable].eligible.mean()) if evaluable.any() else 0.0)


def symbol_quarter_coverage(fund: pd.DataFrame, symbols, start=config.TUNE_START, end=config.TUNE_END) -> float:
    """% of expected (symbol, calendar quarter-end) pairs in [start, end] present as 'Q' rows. Data-supply diagnostic."""
    qe = pd.date_range(pd.Timestamp(start), pd.Timestamp(end), freq="QE")
    have = fund[fund.get("period_type", "Q").astype(str).str.upper().str[0] == "Q"] if "period_type" in fund else fund
    have = have.assign(pe=pd.to_datetime(have.period_end))
    have = have[(have.pe >= qe[0] - pd.Timedelta(days=15)) & (have.pe <= qe[-1] + pd.Timedelta(days=15))]
    got = 0
    for s, g in have.groupby("symbol"):
        if s not in set(symbols):
            continue
        pes = g.pe.values
        got += sum(np.any(np.abs((pes - np.datetime64(q)) / np.timedelta64(1, "D")) <= 15) for q in qe)
    total = len(list(symbols)) * len(qe)
    return 100.0 * got / total if total else 0.0


def main():
    """CLI: runs only if real PIT data exists. Otherwise states UNTESTABLE and exits non-zero."""
    import sys
    path = config.ROOT / "data" / "pit" / "fundamentals.parquet"
    if not path.exists():
        print("UNTESTABLE: data/pit/fundamentals.parquet not found. See reports/4_fundamentals_tester.md for requirements.")
        sys.exit(2)
    fund = pd.read_parquet(path)
    fund = fund[pd.to_datetime(fund.period_end) <= pd.Timestamp(config.TUNE_END)]  # never read beyond tune window
    dates = pd.date_range(config.TUNE_START, config.TUNE_END, freq="ME")
    elig = pit_eligibility(fund, dates)
    print(coverage(elig))
    print("symbol-quarter coverage %:", symbol_quarter_coverage(fund, fund.symbol.unique()))


if __name__ == "__main__":
    main()
