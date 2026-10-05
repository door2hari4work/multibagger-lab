"""Investable universe: India (Nifty Midcap 150 + Smallcap 250) and US (S&P 400 + S&P 600).

Segments: 'mid', 'small' (default).  'micro' (India Nifty Microcap 250) is available ONLY if asked for explicitly
and must be treated as very high risk (the lab found ~no momentum selection edge in micro caps).

Survivor bias: these are CURRENT index members.  Names that were delisted, merged or dropped out of the index are
absent, so any historical statistic computed on them is survivor-inflated.  This module never claims otherwise.
"""
from __future__ import annotations
import io
import re
import warnings
import pandas as pd

from . import CACHE_DIR, RAW_DIR

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
NSE_BASE = "https://archives.nseindia.com/content/indices/"
IN_LISTS = {  # segment -> (file on NSE archives, local fallback in data/raw)
    "mid": ("ind_niftymidcap150list.csv", "ind_niftymidcap150list.csv"),
    "small": ("ind_niftysmallcap250list.csv", "ind_niftysmallcap250list.csv"),
    "micro": ("ind_niftymicrocap250_list.csv", "ind_niftymicrocap250_list.csv"),
}
US_PAGES = {
    "mid": "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies",
    "small": "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies",
}
US_LOCAL = {"small": "sp600_current.csv"}
DEFAULT_SEGMENTS = ("mid", "small")
COLUMNS = ["ticker", "name", "market", "sector", "segment"]


def _norm_market(market: str) -> str:
    m = str(market).upper()
    if m in ("IN", "INDIA"):
        return "IN"
    if m in ("US", "USA"):
        return "US"
    raise ValueError(f"unknown market {market!r} (use 'IN' or 'US')")


def _get(url: str, timeout: int = 30) -> str:
    import requests
    r = requests.get(url, headers=UA, timeout=timeout)
    r.raise_for_status()
    return r.text


def _in_segment(segment: str, source_log: dict) -> pd.DataFrame:
    fname, local = IN_LISTS[segment]
    raw = None
    try:
        raw = pd.read_csv(io.StringIO(_get(NSE_BASE + fname)))
        source_log[f"IN:{segment}"] = "nse_archives_live"
    except Exception as e:  # blocked / offline -> local copy committed under data/raw
        p = RAW_DIR / local
        if not p.exists():
            raise RuntimeError(f"cannot load {segment} list: live fetch failed ({e}) and {p} missing")
        raw = pd.read_csv(p)
        source_log[f"IN:{segment}"] = f"local_copy:{p.name}"
    raw.columns = [c.strip() for c in raw.columns]
    out = pd.DataFrame({
        "ticker": raw["Symbol"].astype(str).str.strip() + ".NS",
        "name": raw["Company Name"].astype(str).str.strip(),
        "market": "IN",
        "sector": raw["Industry"].astype(str).str.strip(),
        "segment": segment,
    })
    return out


def _yahoo_us(sym: str) -> str:
    return str(sym).strip().upper().replace(".", "-")


def _us_segment(segment: str, source_log: dict) -> pd.DataFrame:
    if segment not in US_PAGES:
        warnings.warn(f"US has no '{segment}' segment; skipped")
        return pd.DataFrame(columns=COLUMNS)
    raw = None
    try:
        tables = pd.read_html(io.StringIO(_get(US_PAGES[segment])))
        raw = next(t for t in tables if "Symbol" in t.columns and "Security" in t.columns)
        source_log[f"US:{segment}"] = "wikipedia_live"
    except Exception as e:
        loc = US_LOCAL.get(segment)
        p = RAW_DIR / loc if loc else None
        if p is None or not p.exists():
            raise RuntimeError(f"cannot load US {segment} list: {e}")
        raw = pd.read_csv(p)
        source_log[f"US:{segment}"] = f"local_copy:{p.name}"
    return pd.DataFrame({
        "ticker": raw["Symbol"].map(_yahoo_us),
        "name": raw["Security"].astype(str).str.strip(),
        "market": "US",
        "sector": raw["GICS Sector"].astype(str).str.strip(),
        "segment": segment,
    })


def get_universe(market: str, segments=DEFAULT_SEGMENTS, min_adv=None, refresh: bool = False, **price_kwargs) -> pd.DataFrame:
    """Return DataFrame[ticker, name, market, sector, segment] (+ adv, passes_liquidity if min_adv given).

    market   'IN' | 'US'
    segments subset of ('mid','small','micro'); micro (India only) is excluded unless listed explicitly.
    min_adv  None = no liquidity filtering (no price download).  A number (INR/day for IN, USD/day for US) or True
             (market default) downloads ~1y of prices (cached) and keeps only names whose median 20d traded value
             (Close*Volume) >= floor.  The ADV column is kept either way when computed.
    The list is cached under data/cache/universe_<market>_<segments>.parquet and refreshed if older than 7 days.
    df.attrs['sources'] records live/local origin per list; df.attrs['survivor_bias'] states the caveat.
    """
    mk = _norm_market(market)
    segs = tuple(dict.fromkeys(s.lower() for s in segments))
    bad = [s for s in segs if s not in ("mid", "small", "micro")]
    if bad:
        raise ValueError(f"unknown segments {bad}")
    cache = CACHE_DIR / f"universe_{mk}_{'-'.join(segs)}.parquet"
    df = None
    if cache.exists() and not refresh:
        import time
        if time.time() - cache.stat().st_mtime < 7 * 86400:
            df = pd.read_parquet(cache)
            df.attrs["sources"] = {"cache": cache.name}
    if df is None:
        log: dict = {}
        parts = [(_in_segment if mk == "IN" else _us_segment)(s, log) for s in segs]
        df = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=COLUMNS)
        df = df.drop_duplicates("ticker", keep="first").reset_index(drop=True)
        df.attrs["sources"] = log
        try:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            df.to_parquet(cache)
        except Exception:
            pass
    df = df[COLUMNS].copy()
    df.attrs["survivor_bias"] = "current index members only; delisted/merged/dropped names absent"
    if min_adv is not None and min_adv is not False:
        from . import prices
        floor = prices.DEFAULT_MIN_ADV[mk] if min_adv is True else float(min_adv)
        pdta = prices.get_ohlcv(df["ticker"].tolist(), start=price_kwargs.pop("start", None), **price_kwargs)
        liq = prices.liquidity_table(pdta.close, pdta.volume, min_adv=floor)
        df = df.merge(liq[["adv", "passes_liquidity"]], left_on="ticker", right_index=True, how="left")
        df["passes_liquidity"] = df["passes_liquidity"].fillna(False).astype(bool)
        df = df[df["passes_liquidity"]].reset_index(drop=True)
        df.attrs["min_adv"] = floor
    return df
