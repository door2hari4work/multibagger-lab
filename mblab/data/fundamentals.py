"""Fundamentals loaders and metrics.

US    SEC XBRL companyfacts via fetch_sec.py: ANNUAL (10-K) revenue / EBITDA (= operating income + D&A) / OCF / capex
      with ORIGINAL (earliest-filed) values and `filed_date`.  data/pit/us_fundamentals.parquet covers the S&P 500; names
      outside it (S&P 400/600) are fetched with the same code into data/pit/us_fundamentals_midsmall.parquet.
      Needs env SEC_CONTACT (SEC fair-access User-Agent); the address is never written to any file.
      Rows carry filed dates, so they COULD feed point-in-time tests (backtestable=True), but fetch_sec's universe is
      current index members only (survivor-biased).
IN    yfinance quarterly_income_stmt / quarterly_cashflow: about 5-6 most recent quarters, restated/as-currently-shown by
      Yahoo, NO filing dates.  Rows carry `retrieved_at`.  LATEST-ONLY: backtestable=False, never use in a backtest.

Long table columns: ticker, period_end, period_type ('Q'|'A'), revenue, operating_income, ebitda, net_income, ocf,
filed_date (US) , retrieved_at, source, backtestable.

All metrics here are descriptive evidence/flags.  The lab found the EBITDA/growth/cash-quality gate did NOT improve
results where it could be tested (US), so nothing here is a validated selector.
"""
from __future__ import annotations
import json
import os
import re
import subprocess
import sys
import time
import warnings
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Optional

import numpy as np
import pandas as pd

from . import CACHE_DIR, PIT_DIR, ROOT

COLS = ["ticker", "period_end", "period_type", "revenue", "operating_income", "ebitda", "net_income", "ocf",
        "filed_date", "retrieved_at", "source", "backtestable"]
FINANCIAL_KEYWORDS = ("financ", "bank", "nbfc", "insur", "housing finance", "asset management", "broking")
SEC_MAIN = PIT_DIR / "us_fundamentals.parquet"
SEC_MIDSMALL = PIT_DIR / "us_fundamentals_midsmall.parquet"
SEC_ATTEMPTED = PIT_DIR / "us_fundamentals_midsmall_attempted.json"
IN_CACHE = CACHE_DIR / "fundamentals_IN_v2"
MCAP_CACHE = CACHE_DIR / "market_caps.json"


def is_financial(sector) -> bool:
    if sector is None or (isinstance(sector, float) and np.isnan(sector)):
        return False
    s = str(sector).lower()
    return any(k in s for k in FINANCIAL_KEYWORDS)


def _empty() -> pd.DataFrame:
    return pd.DataFrame(columns=COLS)


# ----------------------------------------------------------------------------------------------- US (SEC)
def _import_fetch_sec():
    if not os.environ.get("SEC_CONTACT"):
        raise RuntimeError("SEC_CONTACT env var (contact email for the SEC User-Agent) is required to fetch SEC data")
    sys.path.insert(0, str(ROOT))
    try:
        import fetch_sec  # module-level code builds the CIK map (network); main block guarded
    finally:
        sys.path.pop(0)
    return fetch_sec


def _sec_to_long(df: pd.DataFrame, retrieved_at: str) -> pd.DataFrame:
    out = pd.DataFrame({
        "ticker": df["symbol"], "period_end": pd.to_datetime(df["period_end"]), "period_type": df.get("period_type", "A"),
        "revenue": df["revenue"].astype(float), "operating_income": np.nan, "ebitda": df["ebitda"].astype(float),
        "net_income": np.nan, "ocf": df["ocf"].astype(float), "filed_date": pd.to_datetime(df["filed_date"]),
        "retrieved_at": retrieved_at, "source": "sec_xbrl_10K", "backtestable": True})
    out.attrs["sector"] = dict(zip(df["symbol"], df.get("sector", pd.Series(dtype=str))))
    return out[COLS]


def get_us_fundamentals(tickers, fetch_missing: bool = True, workers: int = 4) -> pd.DataFrame:
    """Annual SEC fundamentals for `tickers` (Yahoo style, e.g. BRK-B).  Regenerates data/pit/us_fundamentals.parquet
    with fetch_sec.py if it is missing.  Tickers absent from the S&P 500 file are fetched once and cached; tickers the
    SEC has no usable data for are remembered in us_fundamentals_midsmall_attempted.json and not retried for 30 days."""
    tickers = list(dict.fromkeys(tickers))
    PIT_DIR.mkdir(parents=True, exist_ok=True)
    if not SEC_MAIN.exists():
        if not os.environ.get("SEC_CONTACT"):
            raise RuntimeError("data/pit/us_fundamentals.parquet missing and SEC_CONTACT not set; run: SEC_CONTACT=<email> python fetch_sec.py")
        subprocess.run([sys.executable, "fetch_sec.py"], cwd=ROOT, check=True)
    frames = [_sec_to_long(pd.read_parquet(SEC_MAIN), datetime.fromtimestamp(SEC_MAIN.stat().st_mtime, timezone.utc).isoformat())]
    have = set(frames[0]["ticker"])
    if SEC_MIDSMALL.exists():
        ms = pd.read_parquet(SEC_MIDSMALL)
        frames.append(_sec_to_long(ms, datetime.fromtimestamp(SEC_MIDSMALL.stat().st_mtime, timezone.utc).isoformat()))
        have |= set(frames[-1]["ticker"])
    attempted = {}
    if SEC_ATTEMPTED.exists():
        try:
            attempted = json.loads(SEC_ATTEMPTED.read_text())
        except Exception:
            attempted = {}
    cutoff = time.time() - 30 * 86400
    need = [t for t in tickers if t not in have and attempted.get(t, 0) < cutoff]
    if need and fetch_missing:
        fs = _import_fetch_sec()
        rows = []
        with ThreadPoolExecutor(workers) as ex:
            for sym, r in ex.map(fs.one, need):
                attempted[sym] = time.time()
                if r:
                    rows.extend(r)
        if rows:
            new = pd.DataFrame(rows)
            new["sector"] = None
            old = pd.read_parquet(SEC_MIDSMALL) if SEC_MIDSMALL.exists() else None
            new = pd.concat([old, new], ignore_index=True) if old is not None else new
            new = new.drop_duplicates(["symbol", "period_end"], keep="first")
            new.to_parquet(SEC_MIDSMALL)
            frames.append(_sec_to_long(new, datetime.now(timezone.utc).isoformat()))
        SEC_ATTEMPTED.write_text(json.dumps(attempted))
    out = pd.concat(frames, ignore_index=True)
    out = out.drop_duplicates(["ticker", "period_end"], keep="last")
    return out[out["ticker"].isin(tickers)].reset_index(drop=True)


# ------------------------------------------------------------------------------------------ India (yfinance)
def _row(stmt: pd.DataFrame, names):
    for n in names:
        if n in stmt.index:
            return stmt.loc[n]
    return pd.Series(np.nan, index=stmt.columns)


def _stmt_rows(q: pd.DataFrame, ocf: pd.Series, t: str, ptype: str) -> pd.DataFrame:
    out = pd.DataFrame({
        "period_end": pd.to_datetime(q.columns),
        "revenue": _row(q, ["Total Revenue", "Operating Revenue"]).astype(float).values,
        "operating_income": _row(q, ["Operating Income"]).astype(float).values,
        "ebitda": _row(q, ["EBITDA"]).astype(float).values,
        "net_income": _row(q, ["Net Income", "Net Income Common Stockholders"]).astype(float).values,
    })
    out["ocf"] = [float(ocf.get(c, np.nan)) if len(ocf) else np.nan for c in q.columns]
    out = out[out["revenue"].notna()]
    out["ticker"] = t
    out["period_type"] = ptype
    out["filed_date"] = pd.NaT
    out["retrieved_at"] = datetime.now(timezone.utc).isoformat()
    out["source"] = "yfinance_quarterly" if ptype == "Q" else "yfinance_annual"
    out["backtestable"] = False   # no filing dates, Yahoo may restate: LATEST-ONLY
    return out[COLS]


def _fetch_in_one(t: str) -> pd.DataFrame:
    """Quarterly rows ('Q') plus annual rows ('A', used only to bridge TTM when a quarter is missing at Yahoo)."""
    import yfinance as yf
    tk = yf.Ticker(t)
    q = tk.quarterly_income_stmt
    if q is None or q.empty:
        return _empty()
    parts = [_stmt_rows(q, _quarterly_ocf(tk), t, "Q")]
    try:
        a = tk.income_stmt
        if a is not None and not a.empty:
            parts.append(_stmt_rows(a, pd.Series(dtype=float), t, "A"))
    except Exception:
        pass
    return pd.concat(parts, ignore_index=True)


def _quarterly_ocf(tk) -> pd.Series:
    try:
        cf = tk.quarterly_cashflow
    except Exception:
        return pd.Series(dtype=float)
    return _row(cf, ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"]) if cf is not None and not cf.empty else pd.Series(dtype=float)


def get_india_fundamentals(tickers, max_age_days: float = 3.0, workers: int = 8) -> pd.DataFrame:
    """Latest ~5-6 quarters from Yahoo for each .NS ticker.  LATEST-ONLY (backtestable=False), cached under
    data/cache/fundamentals_IN/ and refreshed after `max_age_days`."""
    tickers = list(dict.fromkeys(tickers))
    IN_CACHE.mkdir(parents=True, exist_ok=True)

    def one(t):
        p = IN_CACHE / f"{re.sub(r'[^A-Za-z0-9_.-]', '_', t)}.parquet"
        if p.exists() and (time.time() - p.stat().st_mtime) < max_age_days * 86400:
            try:
                return pd.read_parquet(p)
            except Exception:
                pass
        for attempt in range(2):
            try:
                d = _fetch_in_one(t)
                d.to_parquet(p)
                return d
            except Exception:
                time.sleep(1.5)
        return _empty()

    with ThreadPoolExecutor(workers) as ex:
        parts = list(ex.map(one, tickers))
    parts = [p for p in parts if len(p)]
    return pd.concat(parts, ignore_index=True)[COLS] if parts else _empty()


def get_fundamentals(market: str, tickers, **kw) -> pd.DataFrame:
    m = str(market).upper()
    return get_us_fundamentals(tickers, **kw) if m == "US" else get_india_fundamentals(tickers, **kw)


# ------------------------------------------------------------------------------------------------ market caps
def get_market_caps(tickers, max_age_days: float = 3.0, workers: int = 8) -> pd.Series:
    """Market capitalisation (local currency) from Yahoo fast_info; NaN if unavailable.  Cached in data/cache/."""
    import yfinance as yf
    tickers = list(dict.fromkeys(tickers))
    cache = {}
    if MCAP_CACHE.exists():
        try:
            cache = json.loads(MCAP_CACHE.read_text())
        except Exception:
            cache = {}
    now = time.time()
    need = [t for t in tickers if t not in cache or now - cache[t][1] > max_age_days * 86400]

    def one(t):
        try:
            v = yf.Ticker(t).fast_info["marketCap"]
            return t, (float(v) if v else None)
        except Exception:
            return t, None
    if need:
        with ThreadPoolExecutor(workers) as ex:
            for t, v in ex.map(one, need):
                if v:                     # failures are not cached (retried next run)
                    cache[t] = [v, now]
        try:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            MCAP_CACHE.write_text(json.dumps(cache))
        except Exception:
            pass
    return pd.Series({t: (cache[t][0] if cache.get(t) else np.nan) for t in tickers}, dtype=float)


# --------------------------------------------------------------------------------------------------- metrics
def _growth(cur, prev) -> Optional[float]:
    if cur is None or prev is None or pd.isna(cur) or pd.isna(prev) or prev <= 0:
        return None
    return float(cur / prev - 1)


def _near(days: float, target: float, tol: float) -> bool:
    return abs(days - target) <= tol


def _bridge_ttm(q: pd.DataFrame, a: Optional[pd.DataFrame], col: str) -> Optional[float]:
    """TTM via the latest annual figure: FY + sum(quarters after FY end) - sum(same quarters one year earlier).
    Requires every quarter after FY end (up to the latest) and its year-ago counterpart to be present."""
    if a is None or len(a) == 0 or pd.isna(a[col].iloc[-1]) if a is not None and len(a) else True:
        return None
    pa = a.index[-1]
    p0 = q.index[-1]
    if (p0 - pa).days < 0 or (p0 - pa).days > 300:
        return None
    n_expected = int(round((p0 - pa).days / 91.3))
    since = [p for p in q.index if p > pa + pd.Timedelta(days=20)]
    if n_expected == 0:
        return float(a[col].iloc[-1])
    if len(since) != n_expected:
        return None
    prior = []
    for p in since:
        m = [x for x in q.index if _near((p - x).days, 365, 25)]
        if not m:
            return None
        prior.append(m[0])
    cur_v, prev_v = q.loc[since, col], q.loc[prior, col]
    if cur_v.isna().any() or prev_v.isna().any():
        return None
    return float(a[col].iloc[-1] + cur_v.sum() - prev_v.sum())


def compute_metrics(rows: pd.DataFrame, today=None) -> dict:
    """Growth / margin / operating-leverage metrics for ONE ticker from the long table (any period_type).

    Returns a dict (values None when not computable).  YoY pairs must be ~1 year apart (+-25d); the 'prior' YoY
    pair must be exactly one period (quarter or year) earlier, otherwise rev_accel is None.
      rev_yoy0 / rev_yoy1   latest and previous-period YoY revenue growth
      rev_accel             rev_yoy0 - rev_yoy1 (percentage points as a fraction)
      margin0, margin_delta EBITDA margin (operating margin if EBITDA missing) and its change vs year-ago period
      ebitda_yoy0, op_leverage   EBITDA growth minus revenue growth (positive = operating leverage)
      ttm_revenue / ttm_net_income   sum of last 4 contiguous quarters (Q) or latest fiscal year (A)
    """
    today = pd.Timestamp(today) if today is not None else pd.Timestamp.now().normalize()
    base = dict(freq=None, latest_period=None, staleness_days=None, source=None, filed_date=None, retrieved_at=None,
                backtestable=None, n_periods=0, rev_yoy0=None, rev_yoy1=None, rev_accel=None, margin0=None,
                margin_delta=None, margin_basis=None, ebitda_yoy0=None, op_leverage=None, ebitda_prev_nonpositive=None,
                ebitda_now=None, ttm_revenue=None, ttm_net_income=None, ocf_ebitda=None)
    if rows is None or len(rows) == 0:
        return base
    d_all = rows.copy()
    d_all["period_end"] = pd.to_datetime(d_all["period_end"])
    d_all["period_type"] = d_all["period_type"].astype(str).str[0].str.upper()
    qrows = d_all[d_all["period_type"] == "Q"]
    arows = d_all[d_all["period_type"] == "A"]
    d = (qrows if len(qrows) else arows).sort_values("period_end").drop_duplicates("period_end", keep="first").reset_index(drop=True)
    arows = arows.sort_values("period_end").drop_duplicates("period_end", keep="first").set_index("period_end") if len(qrows) else None
    if len(d) == 0:
        return base
    freq = str(d["period_type"].iloc[-1])[0].upper()
    step = 91 if freq == "Q" else 365
    base.update(freq=freq, n_periods=len(d), latest_period=str(d["period_end"].iloc[-1].date()),
                staleness_days=int((today - d["period_end"].iloc[-1]).days), source=str(d["source"].iloc[-1]),
                backtestable=bool(d["backtestable"].iloc[-1]),
                retrieved_at=str(d["retrieved_at"].iloc[-1]),
                filed_date=(str(pd.to_datetime(d["filed_date"].iloc[-1]).date()) if pd.notna(d["filed_date"].iloc[-1]) else None))
    by = d.set_index("period_end")

    def yearago(p):
        c = [q for q in by.index if _near((p - q).days, 365, 25)]
        return c[0] if c else None

    p0 = by.index[-1]
    q0 = yearago(p0)
    if q0 is not None:
        base["rev_yoy0"] = _growth(by.at[p0, "revenue"], by.at[q0, "revenue"])
    # previous period (one step earlier)
    p1 = next((p for p in by.index[:-1][::-1] if _near((p0 - p).days, step, 25 if freq == "Q" else 25)), None)
    if p1 is not None:
        q1 = yearago(p1)
        if q1 is not None:
            base["rev_yoy1"] = _growth(by.at[p1, "revenue"], by.at[q1, "revenue"])
    if base["rev_yoy0"] is not None and base["rev_yoy1"] is not None:
        base["rev_accel"] = base["rev_yoy0"] - base["rev_yoy1"]
    # margins: EBITDA preferred, operating income fallback (same basis for both periods)
    for col, nm in (("ebitda", "ebitda"), ("operating_income", "operating_income")):
        if q0 is not None and pd.notna(by.at[p0, col]) and pd.notna(by.at[q0, col]) and by.at[p0, "revenue"] > 0 and by.at[q0, "revenue"] > 0:
            m0 = by.at[p0, col] / by.at[p0, "revenue"]
            mq = by.at[q0, col] / by.at[q0, "revenue"]
            base.update(margin0=float(m0), margin_delta=float(m0 - mq), margin_basis=nm)
            e_now, e_prev = float(by.at[p0, col]), float(by.at[q0, col])
            base["ebitda_now"] = e_now
            base["ebitda_prev_nonpositive"] = bool(e_prev <= 0)
            base["ebitda_yoy0"] = _growth(e_now, e_prev)
            if base["ebitda_yoy0"] is not None and base["rev_yoy0"] is not None:
                base["op_leverage"] = base["ebitda_yoy0"] - base["rev_yoy0"]
            break
    # cash conversion (latest period)
    if pd.notna(by.at[p0, "ocf"]) and pd.notna(by.at[p0, "ebitda"]) and by.at[p0, "ebitda"] > 0:
        base["ocf_ebitda"] = float(by.at[p0, "ocf"] / by.at[p0, "ebitda"])
    # TTM
    if freq == "Q":
        last4 = by.index[-4:]
        if len(last4) == 4 and all(_near((last4[i + 1] - last4[i]).days, 91, 25) for i in range(3)):
            base["ttm_revenue"] = float(by.loc[last4, "revenue"].sum())
            ni = by.loc[last4, "net_income"]
            base["ttm_net_income"] = float(ni.sum()) if ni.notna().all() else None
        else:   # a quarter is missing at Yahoo: bridge TTM = last FY + quarters since FY end - same quarters a year earlier
            for col, key in (("revenue", "ttm_revenue"), ("net_income", "ttm_net_income")):
                base[key] = _bridge_ttm(by, arows, col)
    else:
        base["ttm_revenue"] = float(by.at[p0, "revenue"])
    return base
