"""L1 Discovery: screen the mid/small-cap universe and emit candidates with DECOMPOSED, unweighted sub-scores.

WHAT IS VALIDATED AND WHAT IS NOT (read before trusting any number here)
  * The ONLY price signal the lab has validated is the 12-1 month momentum RANK (strong in India, weak/unstable in the
    US, ~none in micro caps; survivor-inflated even where strong).  The screen below orders names by it.
  * Trend filters (close > 200d MA, 12-1 momentum > 0, close within 25% of the 52-week high) and the index regime
    (Nifty 500 / S&P 500 above its 200d MA) gave drawdown protection, not selection, in the lab's tests.
  * Fundamentals (growth acceleration, margin expansion/operating leverage, valuation vs growth) are EVIDENCE and
    FLAGS.  The one fundamentals gate that could be tested (US) did NOT improve results.  They never affect ranking.
  * Sub-score mappings (e.g. "+20pp acceleration = 1.0") are declared heuristics, not fitted or validated values.
  * NO combined buy score is produced here.  Combining sub-scores is mblab/scoring.py's job.
  * Universe = CURRENT index members (survivor bias); Yahoo prices are unaudited; Indian fundamentals are the latest
    ~5-6 quarters only (latest-only, not backtestable); US fundamentals are annual SEC 10-K data (can be up to
    ~15 months old).

SCREEN (explicit, in this order)
  1. liquidity: median 20d traded value (Close*Volume) >= floor (IN Rs 5 cr, US $5M; configurable)
  2. data reliability: not stale (>7d behind the market), >= 273 daily observations, no single-day move > 45% in the
     last ~13 months (likely unadjusted corporate action) -- excluded names are listed in meta, not silently dropped
  3. trend filters: close > 200d MA, 12-1 momentum > 0, close >= 75% of 52-week high
  4. rank by 12-1 momentum percentile among step-2 survivors (ties: momentum/volatility percentile); keep top N (40)
The regime flag is reported, not applied (a regime-OFF market still shows candidates; the lab's rule says cash).
"""
from __future__ import annotations
import json
import math
from datetime import datetime, timezone
from typing import Optional

import numpy as np
import pandas as pd

from .data import ROOT, fundamentals as F, prices as P, universe as U

REGIME_TICKERS = {"IN": ["^CRSLDX", "^NSEI"], "US": ["^GSPC"]}   # Nifty 500, fallback Nifty 50; S&P 500
COMPONENTS = ["market_confirmation", "growth_acceleration", "earnings_inflection", "valuation_asymmetry"]
SCREEN_DOC = ("liquidity floor -> data-reliability exclusion -> trend filters (close>200dMA, 12-1 mom>0, close>=75% of 52w high) "
              "-> rank by 12-1 momentum percentile (tie: mom/vol percentile) -> top N. Fundamentals do not affect the ranking.")
LIMITATIONS = [
    "Survivor bias: universe is current index members; delisted/merged/dropped names are absent.",
    "Yahoo prices are unaudited; unadjusted corporate actions and stale series are flagged, not repaired.",
    "Momentum rank is the only price signal validated by the lab (India strong, US weak, micro ~none); validated on survivors in a tune window only.",
    "Fundamental sub-scores are evidence/flags: the one fundamentals gate tested (US) did not improve results; mappings are declared heuristics.",
    "India fundamentals: latest ~5-6 quarters from Yahoo, no filing dates, latest-only, never backtestable; US: annual SEC 10-K only.",
    "Valuation uses market cap (not EV) vs a single-period growth rate: always marked partial.",
    "No overall buy score is produced here; combination is left to mblab/scoring.py.",
]


def _f(x) -> Optional[float]:
    if x is None:
        return None
    try:
        if isinstance(x, (float, np.floating)) and (math.isnan(x) or math.isinf(x)):
            return None
        return float(x)
    except Exception:
        return None


def _clip01(x: float) -> float:
    return float(min(1.0, max(0.0, x)))


def component(name: str, value, basis: str, data_quality: str, raw: Optional[dict] = None) -> dict:
    """Sub-score record, same field names as mblab.schema.ScoreComponent (value None = not assessed)."""
    v = _f(value)
    return {"name": name, "value": None if v is None else round(_clip01(v), 4), "basis": basis,
            "data_quality": data_quality if v is not None else ("missing" if data_quality == "ok" else data_quality),
            "raw": {k: (round(_f(x), 4) if _f(x) is not None else None) if isinstance(x, (int, float, np.floating)) and not isinstance(x, bool) else x
                    for k, x in (raw or {}).items()}}


# ------------------------------------------------------------------------------------------------ sub-scores
def score_market_confirmation(mom_rank, momvol_rank, trend_passed: Optional[int], trend_total: int = 3, regime_on: Optional[bool] = None) -> dict:
    """0.40*mom12-1 pct rank + 0.15*mom/vol pct rank + 0.30*(trend filters passed / 3) + 0.15*regime (1 on / 0 off).
    Missing parts are dropped and weights renormalised (data_quality 'partial'); no momentum rank -> None.
    Weights are declared, unvalidated; only the momentum rank itself has lab evidence."""
    raw = dict(mom_rank=mom_rank, momvol_rank=momvol_rank, trend_passed=trend_passed, regime_on=regime_on)
    if _f(mom_rank) is None:
        return component("market_confirmation", None, "12-1 momentum rank unavailable", "missing", raw)
    parts, notes = [(0.40, float(mom_rank))], ["0.40 mom12-1 rank"]
    if _f(momvol_rank) is not None:
        parts.append((0.15, float(momvol_rank))); notes.append("0.15 mom/vol rank")
    if trend_passed is not None:
        parts.append((0.30, trend_passed / trend_total)); notes.append("0.30 trend filters")
    if regime_on is not None:
        parts.append((0.15, 1.0 if regime_on else 0.0)); notes.append("0.15 index regime")
    w = sum(p[0] for p in parts)
    val = sum(p[0] * p[1] for p in parts) / w
    dq = "ok" if len(parts) == 4 else "partial"
    return component("market_confirmation", val, "weighted " + " + ".join(notes) + " (declared weights, unvalidated)", dq, raw)


def _data_quality_from_metrics(m: dict) -> str:
    if m.get("staleness_days") is None:
        return "missing"
    limit = 200 if m.get("freq") == "Q" else 460
    return "stale" if m["staleness_days"] > limit else "ok"


def score_growth_acceleration(m: dict, financial: bool = False) -> dict:
    """0.5*level + 0.5*acceleration.  level = clip(YoY revenue growth / 50%, 0..1); acceleration = 0.5 + clip(change in YoY
    growth vs the previous period / 20pp, -1..1)/2.  Only a YoY growth rate -> level only, 'partial'. None if no YoY."""
    raw = dict(rev_yoy0=m.get("rev_yoy0"), rev_yoy1=m.get("rev_yoy1"), rev_accel=m.get("rev_accel"), freq=m.get("freq"),
               latest_period=m.get("latest_period"))
    g0, acc = m.get("rev_yoy0"), m.get("rev_accel")
    if g0 is None:
        return component("growth_acceleration", None, "no YoY revenue growth computable (history too short or non-positive base)", "missing", raw)
    level = _clip01(g0 / 0.5)
    q = _data_quality_from_metrics(m)
    unit = "quarter" if m.get("freq") == "Q" else "fiscal year"
    if acc is None:
        return component("growth_acceleration", level, f"level only: latest {unit} revenue YoY {g0:+.1%}; no prior-period YoY so acceleration unknown", "partial" if q == "ok" else q, raw)
    accel = 0.5 + max(-1.0, min(1.0, acc / 0.20)) / 2
    basis = f"latest {unit} revenue YoY {g0:+.1%} vs previous {unit} YoY {m['rev_yoy1']:+.1%} (change {acc * 100:+.1f}pp); 0.5*level(50%=1) + 0.5*accel(+20pp=1)"
    if financial:
        return component("growth_acceleration", 0.5 * level + 0.5 * accel, basis + "; financial company: revenue definition differs", "partial", raw)
    return component("growth_acceleration", 0.5 * level + 0.5 * accel, basis, q, raw)


def score_earnings_inflection(m: dict, financial: bool = False) -> dict:
    """0.6*margin component + 0.4*operating-leverage component.  Margin: EBITDA (else operating) margin change vs the
    year-ago period, +5pp = 1.0, -5pp = 0.  Leverage: (EBITDA growth - revenue growth), +30pp = 1.0; EBITDA turning
    positive from <=0 = 1.0, EBITDA <= 0 now = 0.0.  Banks/NBFCs/insurers: None (EBITDA is not meaningful)."""
    raw = dict(margin0=m.get("margin0"), margin_delta=m.get("margin_delta"), margin_basis=m.get("margin_basis"),
               ebitda_yoy0=m.get("ebitda_yoy0"), op_leverage=m.get("op_leverage"), ocf_ebitda=m.get("ocf_ebitda"))
    if financial:
        return component("earnings_inflection", None, "financial company: EBITDA/operating margin not meaningful", "missing", raw)
    md = m.get("margin_delta")
    if md is None:
        return component("earnings_inflection", None, "no year-ago margin comparison available", "missing", raw)
    mscore = 0.5 + max(-1.0, min(1.0, md / 0.05)) / 2
    q = _data_quality_from_metrics(m)
    now, prevnp = m.get("ebitda_now"), m.get("ebitda_prev_nonpositive")
    ol = m.get("op_leverage")
    if now is not None and now <= 0:
        lscore, lbasis = 0.0, "EBITDA not positive"
    elif prevnp and now is not None and now > 0:
        lscore, lbasis = 1.0, "EBITDA turned positive vs year-ago"
    elif ol is not None:
        lscore, lbasis = 0.5 + max(-1.0, min(1.0, ol / 0.30)) / 2, f"EBITDA growth minus revenue growth {ol * 100:+.1f}pp"
    else:
        lscore, lbasis = None, None
    mb = m.get("margin_basis", "ebitda").replace("_", " ")
    base = f"{mb} margin {m['margin0']:.1%} ({md * 100:+.1f}pp YoY)"
    if lscore is None:
        return component("earnings_inflection", mscore, base + "; margin component only", "partial" if q == "ok" else q, raw)
    dq = q if m.get("margin_basis") == "ebitda" else ("partial" if q == "ok" else q)
    return component("earnings_inflection", 0.6 * mscore + 0.4 * lscore, f"{base}; {lbasis}; 0.6*margin(+5pp=1) + 0.4*leverage", dq, raw)


def score_valuation_asymmetry(m: dict, mcap: Optional[float], financial: bool = False) -> dict:
    """Valuation relative to growth, ALWAYS data_quality 'partial' (market cap not EV; single-period growth; no estimates).
    P/S-to-growth = (mcap / TTM revenue) / (YoY growth in %): 0.1 -> 1.0, 0.7 -> 0.  PEG-like = (mcap / TTM net income) /
    growth% when net income > 0: 0.5 -> 1.0, 2.5 -> 0.  Score = mean of available.  Growth <= 0: 0.1 (no growth to pay for).
    Growth is capped at 100% to blunt one-quarter spikes.  None without market cap or revenue or growth."""
    g = m.get("rev_yoy0")
    ttm = m.get("ttm_revenue")
    raw = dict(mcap=mcap, ttm_revenue=ttm, growth_used=g, ps=None, ps_to_growth=None, pe=None, peg=None)
    if _f(mcap) is None or _f(ttm) is None or ttm <= 0 or g is None:
        return component("valuation_asymmetry", None, "needs market cap, TTM/latest revenue and a revenue growth rate", "missing", raw)
    ps = mcap / ttm
    raw["ps"] = ps
    if g <= 0:
        return component("valuation_asymmetry", 0.1, f"P/S {ps:.1f}x with non-positive growth ({g:+.1%}): nothing growing to pay for", "partial", raw)
    gp = min(g, 1.0) * 100
    psg = ps / gp
    raw["ps_to_growth"] = psg
    scores = [_clip01(1 - (psg - 0.1) / 0.6)]
    desc = f"P/S {ps:.1f}x / growth {gp:.0f}% = {psg:.2f}"
    ni = m.get("ttm_net_income")
    if not financial and _f(ni) is not None and ni > 0:
        pe = mcap / ni
        peg = pe / gp
        raw.update(pe=pe, peg=peg)
        scores.append(_clip01(1 - (peg - 0.5) / 2.0))
        desc += f"; P/E {pe:.0f}x -> PEG-like {peg:.2f}"
    return component("valuation_asymmetry", float(np.mean(scores)), desc + " (market cap not EV; single-period growth; lower is better)", "partial", raw)


# ----------------------------------------------------------------------------------------------- price signals
def price_signals(pd_: P.PriceData) -> pd.DataFrame:
    """Per-ticker price features at the last row of each series (positional on that ticker's own valid closes)."""
    rows = {}
    for t in pd_.close.columns:
        s = pd_.close[t].dropna()
        s = s[s > 0]
        n = len(s)
        r = dict(price=_f(s.iloc[-1]) if n else None, last_date=s.index[-1] if n else pd.NaT, n_obs=n,
                 mom_12_1=np.nan, vol_ann=np.nan, ma200=np.nan, ma50=np.nan, hi52=np.nan, dd_from_high=np.nan, ext_ma200=np.nan)
        if n >= 253:
            r["mom_12_1"] = s.iloc[-22] / s.iloc[-253] - 1
            ret = s.pct_change().dropna().tail(252)
            r["vol_ann"] = ret.std() * np.sqrt(252)
        if n >= 200:
            r["ma200"] = s.tail(200).mean(); r["ma50"] = s.tail(50).mean()
            r["ext_ma200"] = s.iloc[-1] / r["ma200"] - 1
        if n >= 252:
            r["hi52"] = s.tail(252).max(); r["dd_from_high"] = s.iloc[-1] / r["hi52"] - 1
        rows[t] = r
    df = pd.DataFrame.from_dict(rows, orient="index")
    df.index.name = "ticker"
    df["mom_vol"] = df["mom_12_1"] / df["vol_ann"]
    return df


def trend_filters(sig: pd.DataFrame) -> pd.DataFrame:
    """The lab's three trend filters; NaN inputs count as failed (never as passed)."""
    out = pd.DataFrame(index=sig.index)
    out["above_ma200"] = (sig["price"] > sig["ma200"]).fillna(False)
    out["mom_positive"] = (sig["mom_12_1"] > 0).fillna(False)
    out["near_high"] = (sig["price"] >= 0.75 * sig["hi52"]).fillna(False)
    out["n_passed"] = out[["above_ma200", "mom_positive", "near_high"]].sum(axis=1).astype(int)
    out["passes_all"] = out["n_passed"] == 3
    return out


def get_regime(market: str) -> dict:
    """Index above/below its 200d MA.  IN: Nifty 500 (^CRSLDX, fallback ^NSEI); US: S&P 500 (^GSPC)."""
    for tk in REGIME_TICKERS[market]:
        try:
            d = P.get_ohlcv([tk], max_age_hours=6)
            s = d.close[tk].dropna() if tk in d.close else pd.Series(dtype=float)
            if len(s) >= 200:
                ma = float(s.tail(200).mean())
                return dict(index=tk, close=float(s.iloc[-1]), ma200=ma, regime_on=bool(s.iloc[-1] > ma), as_of=str(s.index[-1].date()))
        except Exception:
            continue
    return dict(index=None, close=None, ma200=None, regime_on=None, as_of=None)


def risk_flags(adv, floor, vol_ann, dd, ext, rel_flags, regime_on, financial, fund_dq, vol_hi=0.60) -> list[str]:
    fl = []
    if _f(adv) is None:
        fl.append("liquidity_unknown")
    elif adv < 2 * floor:
        fl.append("liquidity_thin_lt_2x_floor")
    if _f(vol_ann) is not None and vol_ann > vol_hi:
        fl.append(f"high_volatility_gt_{int(vol_hi * 100)}pct")
    if _f(dd) is not None and dd < -0.20:
        fl.append("drawdown_from_52w_high_gt_20pct")
    if _f(ext) is not None and ext > 0.60:
        fl.append("extended_gt_60pct_above_200dma")
    fl += [f"data:{x}" for x in rel_flags]
    if regime_on is False:
        fl.append("regime_off")
    if financial:
        fl.append("financial_sector_ebitda_not_meaningful")
    if fund_dq in ("missing", "stale"):
        fl.append(f"fundamentals_{fund_dq}")
    return fl


# ------------------------------------------------------------------------------------------------- pipeline
def build_candidates(pd_: P.PriceData, uni: pd.DataFrame, market: str, regime: dict, fund: Optional[pd.DataFrame] = None,
                     mcaps: Optional[pd.Series] = None, top_n: int = 40, min_adv: Optional[float] = None,
                     exclude_flagged: bool = True, today=None) -> tuple[pd.DataFrame, dict]:
    """Pure function over already-loaded data (testable offline).  Returns (top_n candidates DataFrame, meta dict)."""
    floor = float(min_adv if min_adv is not None else P.DEFAULT_MIN_ADV[market])
    uni = uni.set_index("ticker")
    liq = P.liquidity_table(pd_.close, pd_.volume, min_adv=floor)
    sig = price_signals(pd_)
    recent = pd_.close.tail(P.MIN_HISTORY + 7)
    rel_recent = P.reliability_check(recent, tickers=list(uni.index), min_history=P.MIN_HISTORY, as_of=pd_.close.index.max() if len(pd_.close) else None)
    tf = trend_filters(sig)

    n_uni = len(uni)
    have = [t for t in uni.index if t in pd_.close.columns]
    pool_mask = pd.Series(False, index=uni.index)
    reasons = {}
    for t in uni.index:
        fl = rel_recent.at[t, "flags"] if t in rel_recent.index else ["no_data"]
        if "no_data" in fl: reasons[t] = "no_data"
        elif "stale" in fl: reasons[t] = "stale"
        elif "short_history" in fl: reasons[t] = "short_history"
        elif not bool(liq["passes_liquidity"].get(t, False)): reasons[t] = "illiquid"
        elif exclude_flagged and "price_jump" in fl: reasons[t] = "price_jump_gt45pct"
        else: pool_mask[t] = True
    pool = list(pool_mask[pool_mask].index)
    s = sig.loc[pool]
    sig["mom_rank"] = np.nan; sig["momvol_rank"] = np.nan
    sig.loc[pool, "mom_rank"] = s["mom_12_1"].rank(pct=True)
    sig.loc[pool, "momvol_rank"] = s["mom_vol"].rank(pct=True)
    passers = [t for t in pool if bool(tf.at[t, "passes_all"])]
    order = sig.loc[passers].sort_values(["mom_rank", "momvol_rank"], ascending=False)
    top = list(order.index[:top_n])

    # fundamentals metrics for the whole pool (coverage numbers) -------------------------------------------
    metrics: dict = {}
    if fund is not None and len(fund):
        g = {k: v for k, v in fund.groupby("ticker")}
        for t in pool:
            if t in g:
                metrics[t] = F.compute_metrics(g[t], today=today)
    def cov(key):
        n = len(pool)
        return None if n == 0 else round(100 * sum(1 for t in pool if t in metrics and metrics[t].get(key) is not None) / n, 1)

    recs = []
    for rank, t in enumerate(top, 1):
        u = uni.loc[t]; r = sig.loc[t]
        m = metrics.get(t, F.compute_metrics(None))
        fin = F.is_financial(u["sector"])
        mc = _f(mcaps.get(t)) if mcaps is not None else None
        comps = {
            "market_confirmation": score_market_confirmation(r["mom_rank"], r["momvol_rank"], int(tf.at[t, "n_passed"]), 3, regime.get("regime_on")),
            "growth_acceleration": score_growth_acceleration(m, fin),
            "earnings_inflection": score_earnings_inflection(m, fin),
            "valuation_asymmetry": score_valuation_asymmetry(m, mc, fin),
        }
        fdq = _data_quality_from_metrics(m)
        flags = risk_flags(liq.at[t, "adv"], floor, r["vol_ann"], r["dd_from_high"], r["ext_ma200"],
                           rel_recent.at[t, "flags"], regime.get("regime_on"), fin, fdq)
        recs.append(dict(
            rank=rank, ticker=t, name=u["name"], sector=u["sector"], segment=u["segment"], market=market,
            price=_f(r["price"]), price_date=str(r["last_date"].date()) if pd.notna(r["last_date"]) else None,
            mom_12_1=_f(r["mom_12_1"]), mom_rank=_f(r["mom_rank"]), momvol_rank=_f(r["momvol_rank"]),
            vol_ann=_f(r["vol_ann"]), dd_from_52w_high=_f(r["dd_from_high"]), ext_above_200dma=_f(r["ext_ma200"]),
            adv=_f(liq.at[t, "adv"]), adv_floor=floor, market_cap=mc,
            fundamentals=dict(freq=m["freq"], latest_period=m["latest_period"], source=m["source"], filed_date=m["filed_date"],
                              retrieved_at=m["retrieved_at"], backtestable=m["backtestable"], staleness_days=m["staleness_days"],
                              latest_only=(m["backtestable"] is False) if m["backtestable"] is not None else None),
            scores=comps, risk_flags=flags))
    df = pd.DataFrame(recs)
    exc = pd.Series(reasons).value_counts().to_dict()
    jump_list = []
    for t, why in reasons.items():
        if why == "price_jump_gt45pct":
            jump_list.append(dict(ticker=t, max_abs_move=_f(rel_recent.at[t, "max_abs_move"]), date=str(rel_recent.at[t, "max_move_date"].date())))
    meta = dict(
        market=market, generated_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        data_as_of=str(pd_.close.index.max().date()) if len(pd_.close) else None, regime=regime,
        screen=SCREEN_DOC, ranking="12-1 momentum percentile (the only lab-validated price signal); fundamentals are evidence, not a filter",
        liquidity_floor=floor, liquidity_floor_unit="INR per day (median 20d Close*Volume)" if market == "IN" else "USD per day (median 20d Close*Volume)",
        universe_size=n_uni, with_price_data=len(have), excluded_counts=exc, excluded_price_jump=jump_list,
        pool_size=len(pool), pass_trend_filters=len(passers), top_n=len(top),
        fundamentals_coverage_pct_of_pool=dict(any_period=round(100 * len(metrics) / len(pool), 1) if pool else None,
                                              revenue_yoy=cov("rev_yoy0"), growth_acceleration=cov("rev_accel"),
                                              margin_delta=cov("margin_delta"), ttm_revenue=cov("ttm_revenue")),
        market_cap_coverage_pct_of_top=(round(100 * float(mcaps.reindex(top).notna().mean()), 1) if mcaps is not None and top else None),
        survivor_bias="current index members only", limitations=LIMITATIONS)
    df.attrs["meta"] = meta
    return df, meta


def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (float, np.floating)):
        return None if (math.isnan(o) or math.isinf(o)) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    return o


def flatten(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in df.iterrows():
        d = {k: v for k, v in r.items() if k not in ("scores", "fundamentals", "risk_flags")}
        for n, c in r["scores"].items():
            d[f"{n}_score"] = c["value"]; d[f"{n}_quality"] = c["data_quality"]; d[f"{n}_basis"] = c["basis"]
        d["fund_latest_period"] = r["fundamentals"]["latest_period"]; d["fund_source"] = r["fundamentals"]["source"]
        d["fund_latest_only"] = r["fundamentals"]["latest_only"]
        d["risk_flags"] = "; ".join(r["risk_flags"])
        rows.append(d)
    return pd.DataFrame(rows)


def run_discovery(market: str, top_n: int = 40, segments=("mid", "small"), min_adv: Optional[float] = None,
                  start=None, exclude_flagged: bool = True, with_fundamentals: bool = True,
                  fund_scope: str = "pool", write: bool = True, out_dir=None, refresh_prices: bool = False) -> pd.DataFrame:
    """Run L1 discovery for 'IN' or 'US'; return the top_n candidates (DataFrame with nested score dicts) and, if
    write=True, research/candidates_<market>.json and .csv.  See module docstring for the screen and its validity."""
    market = U._norm_market(market)
    uni = U.get_universe(market, segments)
    pdata = P.get_ohlcv(uni["ticker"].tolist(), start=start, refresh=refresh_prices)
    regime = get_regime(market)
    fund = mcaps = None
    if with_fundamentals:
        # fundamentals for names that survive liquidity + data checks (coverage is reported against this pool)
        floor = float(min_adv if min_adv is not None else P.DEFAULT_MIN_ADV[market])
        liq = P.liquidity_table(pdata.close, pdata.volume, min_adv=floor)
        rel = P.reliability_check(pdata.close.tail(P.MIN_HISTORY + 7), tickers=list(uni["ticker"]), min_history=P.MIN_HISTORY, as_of=pdata.close.index.max())
        ok = [t for t in uni["ticker"] if bool(liq["passes_liquidity"].get(t, False)) and not {"no_data", "stale", "short_history"} & set(rel.at[t, "flags"])]
        fund = F.get_fundamentals(market, ok)
    df, meta = build_candidates(pdata, uni, market, regime, fund, None, top_n, min_adv, exclude_flagged)
    if with_fundamentals and len(df):
        mcaps = F.get_market_caps(list(df["ticker"]))
        df, meta = build_candidates(pdata, uni, market, regime, fund, mcaps, top_n, min_adv, exclude_flagged)
    if write:
        from pathlib import Path
        out = Path(out_dir) if out_dir else ROOT / "research"
        out.mkdir(parents=True, exist_ok=True)
        payload = _clean(dict(meta=meta, candidates=df.to_dict("records")))
        (out / f"candidates_{market}.json").write_text(json.dumps(payload, indent=1, default=str))
        flatten(df).to_csv(out / f"candidates_{market}.csv", index=False)
    return df
