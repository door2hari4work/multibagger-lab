"""Prices via yfinance with a local parquet cache, staleness metadata, a data-reliability check and a liquidity floor.

Prices are split/dividend adjusted by Yahoo (auto_adjust=True).  Yahoo data is NOT audited: unadjusted corporate
actions, bad ticks, silent gaps and stale series happen.  `reliability_check` flags (does not repair) such cases.
Cache: data/cache/prices/<TICKER>.parquet (+ _meta.json).  A cached series is reused if it was fetched less than
`max_age_hours` ago and starts at or before the requested start; otherwise it is re-downloaded in full (adjustments
can change history, so we never splice).
"""
from __future__ import annotations
import json
import re
import time
import warnings
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Optional

import numpy as np
import pandas as pd

from . import CACHE_DIR

FIELDS = ["Close", "High", "Low", "Volume"]
BATCH = 50
DEFAULT_MIN_ADV = {"IN": 5e7, "US": 5e6}   # Rs 5 crore / USD 5M, median 20d traded value (Close*Volume)
MAX_DAILY_MOVE = 0.45                      # |1-day return| above this => likely unadjusted corporate action / bad tick
STALE_DAYS = 7                             # last obs more than this many calendar days behind the market's last obs
MIN_HISTORY = 273                          # obs needed for 12-1 momentum (252 + 21)
PRICE_DIR = CACHE_DIR / "prices"


@dataclass
class PriceData:
    close: pd.DataFrame
    high: pd.DataFrame
    low: pd.DataFrame
    volume: pd.DataFrame
    meta: pd.DataFrame = field(default_factory=pd.DataFrame)   # index ticker: last_date, staleness_days, n_obs, fetched_at, flags...

    def tickers(self):
        return list(self.close.columns)


def _safe(t: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.\-^]", "_", t)


def _path(t: str):
    return PRICE_DIR / f"{_safe(t)}.parquet"


def _naive(d: pd.DataFrame) -> pd.DataFrame:
    idx = pd.DatetimeIndex(pd.to_datetime(d.index))
    d = d.copy()
    d.index = idx.tz_localize(None) if idx.tz is not None else idx
    return d.sort_index()


def _download(batch: list[str], start) -> dict[str, pd.DataFrame]:
    import yfinance as yf
    out: dict[str, pd.DataFrame] = {}
    try:
        raw = yf.download(batch, start=start, auto_adjust=True, progress=False, threads=True, group_by="ticker")
    except Exception as e:
        warnings.warn(f"yfinance batch failed: {e}")
        return out
    if raw is None or raw.empty:
        return out
    for t in batch:
        try:
            d = raw[t] if isinstance(raw.columns, pd.MultiIndex) else raw
            d = d[[c for c in FIELDS if c in d.columns]].dropna(how="all")
            if len(d) and "Close" in d:
                d = d[d["Close"].notna()]
                out[t] = _naive(d)
        except KeyError:
            continue
    return out


def _read_cache(t: str):
    p = _path(t)
    if not p.exists():
        return None
    try:
        d = _naive(pd.read_parquet(p))
        return d, d.attrs.get("fetched_at") or datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat()
    except Exception:
        return None


def _write_cache(t: str, d: pd.DataFrame, fetched_at: str):
    try:
        PRICE_DIR.mkdir(parents=True, exist_ok=True)
        p = _path(t)
        d = d.copy()
        d.to_parquet(p)
        meta_p = PRICE_DIR / (_safe(t) + ".meta.json")
        meta_p.write_text(json.dumps({"fetched_at": fetched_at, "start": str(d.index.min().date()), "end": str(d.index.max().date())}))
    except Exception as e:
        warnings.warn(f"cache write failed for {t}: {e}")


def _cache_info(t: str):
    mp = PRICE_DIR / (_safe(t) + ".meta.json")
    if mp.exists():
        try:
            return json.loads(mp.read_text())
        except Exception:
            return None
    return None


def get_ohlcv(tickers, start=None, max_age_hours: float = 12.0, refresh: bool = False,
              stale_days: int = STALE_DAYS, max_move: float = MAX_DAILY_MOVE) -> PriceData:
    """Close/High/Low/Volume panels (dates x tickers) + per-ticker meta (staleness, reliability flags).

    start default: ~2 years back (enough for 12-1 momentum, 200d MA, 52w high).  Missing tickers appear in meta
    with flag 'no_data' and are absent from the panels.
    """
    tickers = list(dict.fromkeys(tickers))
    if start is None:
        start = (datetime.now(timezone.utc) - timedelta(days=740)).date()
    start_ts = pd.Timestamp(start)
    now = datetime.now(timezone.utc)
    series: dict[str, pd.DataFrame] = {}
    fetched: dict[str, str] = {}
    todo = []
    for t in tickers:
        info = _cache_info(t)
        c = None if refresh else _read_cache(t)
        ok = False
        if c is not None and info:
            age_h = (now - datetime.fromisoformat(info["fetched_at"])).total_seconds() / 3600
            ok = age_h < max_age_hours and pd.Timestamp(info["start"]) <= start_ts + pd.Timedelta(days=7)
        if ok:
            series[t] = c[0]; fetched[t] = info["fetched_at"]
        else:
            todo.append(t)
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        got = _download(batch, start)
        miss = [t for t in batch if t not in got]
        if miss and len(miss) <= 10:       # one retry for stragglers
            time.sleep(1.0); got.update(_download(miss, start))
        ts = datetime.now(timezone.utc).isoformat()
        for t, d in got.items():
            series[t] = d; fetched[t] = ts; _write_cache(t, d, ts)
    series = {t: d[d.index >= start_ts] for t, d in series.items() if t in tickers}
    cols = {f: pd.DataFrame({t: d[f] for t, d in series.items() if f in d}) for f in FIELDS}
    for f in FIELDS:
        cols[f] = cols[f].sort_index()
        idx = pd.DatetimeIndex(pd.to_datetime(cols[f].index))
        cols[f].index = idx.tz_localize(None) if idx.tz is not None else idx
    meta = reliability_check(cols["Close"], stale_days=stale_days, max_move=max_move, tickers=tickers)
    meta["fetched_at"] = pd.Series(fetched)
    return PriceData(cols["Close"], cols["High"], cols["Low"], cols["Volume"], meta)


def reliability_check(close: pd.DataFrame, stale_days: int = STALE_DAYS, max_move: float = MAX_DAILY_MOVE,
                      min_history: int = MIN_HISTORY, tickers=None, as_of=None) -> pd.DataFrame:
    """Per-ticker data-reliability table.

    Columns: last_date, staleness_days (vs the latest date in the panel / `as_of`), n_obs, max_abs_move,
    max_move_date, n_jumps, flags (list of str).  Flags:
      no_data          ticker requested but no series
      stale            last observation more than `stale_days` calendar days before the panel's last date
      price_jump       a single-day |return| > max_move (likely unadjusted split/reverse split/bad tick; also real shocks)
      short_history    fewer than min_history observations (12-1 momentum not computable)
    The check flags; it never repairs or drops data.
    """
    rows = {}
    ref = pd.Timestamp(as_of) if as_of is not None else (close.index.max() if len(close) else pd.NaT)
    for t in (tickers if tickers is not None else close.columns):
        flags: list[str] = []
        if t not in close.columns or close[t].dropna().empty:
            rows[t] = dict(last_date=pd.NaT, staleness_days=np.nan, n_obs=0, max_abs_move=np.nan, max_move_date=pd.NaT, n_jumps=0, flags=["no_data"])
            continue
        s = close[t].dropna()
        s = s[s > 0]
        last = s.index.max()
        stale = (ref - last).days if pd.notna(ref) else np.nan
        r = s.pct_change(fill_method=None).dropna()
        mx = float(r.abs().max()) if len(r) else 0.0
        mxd = r.abs().idxmax() if len(r) else pd.NaT
        nj = int((r.abs() > max_move).sum())
        if pd.notna(stale) and stale > stale_days:
            flags.append("stale")
        if nj:
            flags.append("price_jump")
        if len(s) < min_history:
            flags.append("short_history")
        rows[t] = dict(last_date=last, staleness_days=stale, n_obs=len(s), max_abs_move=mx, max_move_date=mxd, n_jumps=nj, flags=flags)
    out = pd.DataFrame.from_dict(rows, orient="index")
    out.index.name = "ticker"
    return out


def liquidity_table(close: pd.DataFrame, volume: pd.DataFrame, window: int = 20, min_adv: Optional[float] = None,
                    market: Optional[str] = None) -> pd.DataFrame:
    """Median traded value (Close*Volume) over the last `window` observations, per ticker.

    Columns: adv (currency/day: INR for .NS, USD for US), passes_liquidity, zero_volume_days (in the window).
    Floor: min_adv, else DEFAULT_MIN_ADV[market] (IN Rs 5 crore, US $5M).  A ticker with fewer than `window` valid
    observations fails (insufficient evidence of liquidity).  Never forward-fills.
    """
    if min_adv is None:
        if market is None:
            raise ValueError("give min_adv or market")
        min_adv = DEFAULT_MIN_ADV[market]
    tv = (close * volume.reindex_like(close)).tail(window)
    n = tv.notna().sum()
    adv = tv.median()
    adv = adv.where(n >= window)
    zero = (volume.reindex_like(close).tail(window) == 0).sum()
    out = pd.DataFrame({"adv": adv, "zero_volume_days": zero})
    out["passes_liquidity"] = out["adv"].ge(min_adv).fillna(False)
    out["min_adv"] = float(min_adv)
    out.index.name = "ticker"
    return out
