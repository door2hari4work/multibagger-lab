"""Entry timing for ONE stock: a rule-based state machine over price (and volume when available). Not a forecast.

Design rules
- Pure function of the price history, a market-regime flag and a thesis-health flag. No network, no hidden state.
- Features are computed vectorised (compute_features) and classified by ONE scalar function (classify), so the production path
  (assess) and the validation script (analysis/timing/state_validation.py) cannot drift apart.
- Zones are ROUNDED ranges (tick depends on price level) and every rationale spells out the derivation (MA band, ATR multiples).
- Thresholds in TH are declared a priori from common practice, NOT fitted. analysis/timing/state_validation.py reports honestly
  whether the states carry any information in the tune window (survivor-biased); see reports/TIMING_VALIDATION.md.
- The states are descriptions of where the price sits relative to its trend, never "buy" instructions.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd

from .schema import EntryState, EntryPlan

# ----------------------------------------------------------------------------------------------------------------------------
# Declared thresholds (a priori; do not tune on the validation windows without recording it in the report)
TH = dict(
    min_rows=210,            # need a 200d MA plus a few days; otherwise state = unknown
    atr_n=14,
    ext_wait=2.5,            # > this many ATR above the 50d MA: wait_for_pullback (a confirmed breakout is exempt up to ext_over: see classify)
    ext_over=4.0,            # >= this many ATR above the 50d MA: overextended
    ext_pct_over=0.30,       # or >= 30% above the 50d MA
    attr_ext_lo=-2.0, attr_ext_hi=1.0,   # attractive: within [-2, +1] ATR of the 50d MA
    attr_dd_lo=-0.30, attr_dd_hi=-0.05,  # and 5%..30% below the 52w high
    conf_dd=-0.10,           # confirmation: within 10% of the 52w high, rising 50d MA, not extended
    base_tight=0.15,         # 40-day close range (max/min - 1) at or under this = "tight base"
    base60_max=0.25,         # a breakout must come out of a 60-day base no wider than this
    breakout_vol=1.5,        # max volume of last 5 days / avg volume of the prior 50 days
    below200_near=0.10,      # setup_forming below the 200d MA only if within 10% of it ...
    deep_dd=-0.30,           # ... and the drawdown from the 52w high is not worse than this
)


def tick_for(price: float) -> float:
    """Sensible rounding tick by price level (no false precision)."""
    for lim, t in ((1, 0.01), (5, 0.05), (20, 0.10), (50, 0.25), (100, 0.50), (500, 1.0), (1000, 5.0), (5000, 10.0)):
        if price < lim: return t
    return 50.0


def _snap(x: float, tick: float, how: str) -> float:
    n = x / tick
    n = math.floor(n + 1e-9) if how == "down" else math.ceil(n - 1e-9) if how == "up" else round(n)
    return round(n * tick, 6)


def round_zone(lo: float, hi: float, tick: float) -> list:
    """Round outward (low down, high up) so the displayed range never understates the derived one; guarantees hi > lo."""
    lo, hi = min(lo, hi), max(lo, hi)
    a, b = _snap(lo, tick, "down"), _snap(hi, tick, "up")
    if b <= a: b = round(a + tick, 6)
    return [a, b]


# ----------------------------------------------------------------------------------------------------------------------------
@dataclass
class EntryAssessment:
    state: str                              # schema.EntryState value
    ideal_zone: Optional[list] = None       # [low, high] local currency, rounded
    acceptable_zone: Optional[list] = None
    chase_zone: Optional[list] = None
    add_zone: Optional[list] = None
    invalidation_price: Optional[float] = None   # TECHNICAL level (trend break); thesis exits are separate
    rationale: str = ""
    metrics: dict = field(default_factory=dict)

    def to_entry_plan(self) -> EntryPlan:
        return EntryPlan(state=self.state, ideal_zone=self.ideal_zone, acceptable_zone=self.acceptable_zone, chase_zone=self.chase_zone,
                         add_zone=self.add_zone, invalidation_price=self.invalidation_price, rationale=self.rationale)


# Ordering used by the monitor: higher = a better place to be entering from (thesis_deteriorating is the worst, attractive the best).
ENTRY_RANK = {"thesis_deteriorating": 0, "too_early": 1, "overextended": 2, "wait_for_pullback": 3, "setup_forming": 4,
              "breakout_entry": 5, "confirmation_entry": 6, "attractive_entry": 7, "unknown": -1}
ACTIONABLE = {"attractive_entry", "confirmation_entry", "breakout_entry"}


# ----------------------------------------------------------------------------------------------------------------------------
def _prep(ohlcv: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(ohlcv, pd.DataFrame): raise TypeError("ohlcv must be a DataFrame")
    d = ohlcv.copy()
    d.columns = [str(c).strip().lower() for c in d.columns]
    if "close" not in d: raise ValueError("ohlcv needs a Close column")
    d = d.sort_index()
    d = d[~d.index.duplicated(keep="last")]
    d = d[d["close"].notna() & (d["close"] > 0)]
    for c in ("high", "low"):
        if c not in d: d[c] = d["close"]
        d[c] = d[c].fillna(d["close"])
    if "volume" not in d: d["volume"] = np.nan
    return d[["close", "high", "low", "volume"]].astype(float)


def compute_features(ohlcv: pd.DataFrame) -> pd.DataFrame:
    """Per-day features, using only data up to and including each day. Close-only input degrades gracefully
    (ATR becomes mean absolute close-to-close change, volume features are NaN)."""
    d = _prep(ohlcv)
    c, h, l, v = d["close"], d["high"], d["low"], d["volume"]
    f = pd.DataFrame(index=d.index)
    f["close"] = c
    f["ma50"], f["ma200"] = c.rolling(50).mean(), c.rolling(200).mean()
    f["ma50_slope"] = f["ma50"] / f["ma50"].shift(20) - 1
    f["ma200_slope"] = f["ma200"] / f["ma200"].shift(20) - 1
    pc = c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    f["atr"] = tr.rolling(TH["atr_n"]).mean()
    f["atr_pct"] = f["atr"] / c
    f["hi52"] = h.rolling(252, min_periods=200).max()
    f["dist_hi"] = c / f["hi52"] - 1
    f["ext_atr"] = (c - f["ma50"]) / f["atr"].where(f["atr"] > 0)
    f["ext_pct"] = c / f["ma50"] - 1
    f["range40"] = c.rolling(40).max() / c.rolling(40).min() - 1
    # breakout: a close in the last 5 days above the highest close of the 60 days before that, still above it now, out of a base
    prior = c.shift(5)
    prior_hi, prior_lo = prior.rolling(60).max(), prior.rolling(60).min()
    f["base60"] = prior_hi / prior_lo - 1
    f["prior_high"] = prior_hi
    f["breakout"] = ((c.rolling(5).max() > prior_hi) & (c > prior_hi) & (f["base60"] <= TH["base60_max"])).astype(float)
    f["swing_low60"] = l.rolling(60).min()
    avgv = v.shift(5).rolling(50).mean()
    f["vol_ratio"] = v.rolling(5).max() / avgv.where(avgv > 0)
    return f


def _num(x) -> Optional[float]:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(x) or math.isinf(x) else x


def classify(f: dict, regime_on: bool = True, thesis_ok: bool = True) -> tuple:
    """f: one row of compute_features as a dict. Returns (state, reason, flags). Pure; used by assess() and by the validation script."""
    flags = {}
    if not thesis_ok:
        return EntryState.THESIS_DETERIORATING.value, "The thesis check failed (thesis_ok=False): price levels are secondary until it is re-reviewed.", flags
    g = {k: _num(f.get(k)) for k in ("close", "ma50", "ma200", "ma50_slope", "ma200_slope", "atr", "dist_hi", "ext_atr", "ext_pct", "range40", "breakout", "vol_ratio")}
    need = ("close", "ma50", "ma200", "ma50_slope", "ma200_slope", "atr", "dist_hi", "ext_atr", "ext_pct")
    if any(g[k] is None for k in need):
        return EntryState.UNKNOWN.value, "Not enough clean price history to measure trend, extension and drawdown.", flags
    c, ma50, ma200 = g["close"], g["ma50"], g["ma200"]
    ext, ext_pct, dd = g["ext_atr"], g["ext_pct"], g["dist_hi"]
    tight = g["range40"] is not None and g["range40"] <= TH["base_tight"]
    vol_known = g["vol_ratio"] is not None
    vol_ok = (g["vol_ratio"] >= TH["breakout_vol"]) if vol_known else None
    flags.update(tight_base=bool(tight), volume_confirmed=vol_ok)
    up = c > ma200 and g["ma200_slope"] > 0 and ma50 > ma200

    if c <= ma200:
        near = c >= ma200 * (1 - TH["below200_near"])
        if near and tight and g["ma50_slope"] >= -0.01 and dd >= TH["deep_dd"]:
            return EntryState.SETUP_FORMING.value, f"Below the 200d MA but within {TH['below200_near']:.0%} of it, with a tight 40-day base ({g['range40']:.0%} range) and a flattening 50d MA: a base may be forming; wait for a close back above the 200d MA.", flags
        why = f"Price is below its 200d MA ({c / ma200 - 1:+.0%}) and {dd:+.0%} from the 52w high: the trend is down or unrepaired, so it is early."
        return EntryState.TOO_EARLY.value, why, flags
    if not up:
        return EntryState.SETUP_FORMING.value, "Price is above the 200d MA but the trend is not established yet (200d MA not rising and/or 50d MA still below it): a setup is forming, not confirmed.", flags
    if ext >= TH["ext_over"] or ext_pct >= TH["ext_pct_over"]:
        return EntryState.OVEREXTENDED.value, f"Price is {ext:.1f} ATR ({ext_pct:+.0%}) above its 50d MA, beyond the {TH['ext_over']:.0f} ATR / {TH['ext_pct_over']:.0%} limits: stretched, so a normal pullback to the trend would cost a lot from here. (Tune-window evidence did NOT show overextended names underperform; this label is about entry price, not a forecast.)", flags
    if g["breakout"] == 1.0:
        if vol_known and not vol_ok:
            return EntryState.WAIT_FOR_PULLBACK.value, f"Price broke above its prior 60-day high, but volume confirmation is missing (peak volume {g['vol_ratio']:.1f}x its 50d average, need {TH['breakout_vol']:.1f}x): an unconfirmed breakout often retests; wait.", flags
        note = f"volume confirmed ({g['vol_ratio']:.1f}x the 50d average)" if vol_known else "volume data not available, so confirmation is UNVERIFIED"
        return EntryState.BREAKOUT_ENTRY.value, f"Price closed above the prior 60-day high out of a base no wider than {TH['base60_max']:.0%}, {ext:.1f} ATR above the 50d MA (under the {TH['ext_over']:.0f} ATR overextension limit); {note}.", flags
    if ext > TH["ext_wait"]:
        return EntryState.WAIT_FOR_PULLBACK.value, f"Price is {ext:.1f} ATR above its 50d MA (limit {TH['ext_wait']:.1f}): trend is intact but entry is stretched; a pullback toward the 50d MA would improve it.", flags
    if TH["attr_ext_lo"] <= ext <= TH["attr_ext_hi"] and TH["attr_dd_lo"] <= dd <= TH["attr_dd_hi"]:
        return EntryState.ATTRACTIVE_ENTRY.value, f"Uptrend intact (above a rising 200d MA, 50d MA above 200d) and price has pulled back to {ext:+.1f} ATR of the 50d MA, {dd:+.0%} from the 52w high: a normal pullback inside the trend.", flags
    if dd >= TH["conf_dd"] and g["ma50_slope"] > 0:
        return EntryState.CONFIRMATION_ENTRY.value, f"Uptrend confirmed: within {-dd:.0%} of the 52w high, 50d MA rising, {ext:+.1f} ATR above it (not stretched).", flags
    return EntryState.SETUP_FORMING.value, f"Uptrend intact but price is {ext:+.1f} ATR from the 50d MA and {dd:+.0%} from the 52w high: neither a clean pullback nor a confirmed push to highs.", flags


# ----------------------------------------------------------------------------------------------------------------------------
def _zones(state: str, f: dict) -> dict:
    c, ma50, ma200, atr = f["close"], f["ma50"], f["ma200"], max(f["atr"], 0.005 * f["close"])
    t = tick_for(c)
    out = dict(ideal=None, acceptable=None, chase=None, add=None, invalid=None, text="")
    if state in ("too_early", "unknown", "thesis_deteriorating"):
        if state == "too_early":
            out["text"] = f"No entry zone is offered: the trend is not repaired. A first sign of repair would be a close above the 200d MA ({_snap(ma200, t, 'nearest')})."
        return out
    anchor = ma50 if (ma50 > ma200 and c > ma200) else ma200
    aname = "50d MA" if anchor == ma50 else "200d MA"
    lo_floor = ma200 * 0.99 if aname == "50d MA" else -1e18
    ideal = round_zone(max(anchor - 0.5 * atr, lo_floor), anchor + 0.5 * atr, t)
    acc = round_zone(max(anchor - 1.0 * atr, lo_floor), anchor + 2.0 * atr, t)
    chase = round_zone(anchor + 2.5 * atr, anchor + 4.0 * atr, t)
    swing = f.get("swing_low60")
    inv_trend = ma200 - 1.0 * atr
    inv = max(inv_trend, (swing - 0.5 * atr) if swing is not None and not math.isnan(swing) else -1e18)
    if inv >= ideal[0]: inv = ideal[0] - 1.0 * atr
    inv = _snap(max(inv, 0.01), t, "down")
    add = None
    if aname == "50d MA":
        a_lo, a_hi = max(ma200 + 0.5 * atr, ma50 - 1.5 * atr), ma50 - 0.5 * atr
        if a_hi > a_lo: add = round_zone(a_lo, a_hi, t)
    out.update(ideal=ideal, acceptable=acc, chase=chase, add=add, invalid=inv)
    out["text"] = (f"Ideal zone = {aname} ({anchor:.4g}) +/- 0.5 ATR(14) ({atr:.3g}) = {ideal[0]}-{ideal[1]}; acceptable = {aname} -1.0/+2.0 ATR = {acc[0]}-{acc[1]}; "
                   f"chase zone = {aname} +2.5..+4.0 ATR = {chase[0]}-{chase[1]} (a stretched entry). "
                   + (f"Add zone (only if the thesis is intact) = a pullback of 0.5-1.5 ATR below the 50d MA that still holds above the 200d MA = {add[0]}-{add[1]}. " if add else "No add zone: it would sit below the 200d MA band. ")
                   + f"Technical invalidation = the higher of (200d MA {ma200:.4g} - 1 ATR) and (60-day swing low - 0.5 ATR), pushed below the ideal zone if needed = {inv}. All levels rounded outward to a {t:g} tick.")
    return out


def assess(ohlcv: pd.DataFrame, regime_on: bool, thesis_ok: bool = True) -> EntryAssessment:
    """ohlcv: Close/High/Low/Volume for ONE stock (case-insensitive; only Close is mandatory), daily, oldest first.
    regime_on: broad-market trend regime (e.g. index above its 200d MA). thesis_ok: False when research says the thesis is deteriorating."""
    f = compute_features(ohlcv)
    if len(f) < TH["min_rows"]:
        return EntryAssessment(EntryState.THESIS_DETERIORATING.value if not thesis_ok else EntryState.UNKNOWN.value,
                               rationale=f"Only {len(f)} clean daily rows; {TH['min_rows']} are needed for a 200d MA and 52w range." + ("" if thesis_ok else " The thesis check also failed."),
                               metrics={"rows": len(f)})
    last = f.iloc[-1].to_dict()
    state, why, flags = classify(last, regime_on=regime_on, thesis_ok=thesis_ok)
    raw_state = state
    downgraded = False
    if not regime_on and state in ACTIONABLE:
        state, downgraded = EntryState.SETUP_FORMING.value, True
        why = f"[{raw_state} on the stock's own chart, deferred because the market regime filter is OFF] " + why
    empty = dict(ideal=None, acceptable=None, chase=None, add=None, invalid=None, text="")
    zones = empty if state in ("unknown", "thesis_deteriorating") else _zones(state, last)
    metrics = {k: (None if _num(last.get(k)) is None else round(_num(last[k]), 4)) for k in
               ("close", "ma50", "ma200", "ma50_slope", "ma200_slope", "atr", "atr_pct", "hi52", "dist_hi", "ext_atr", "ext_pct", "range40", "base60", "vol_ratio", "swing_low60")}
    metrics.update(flags); metrics.update(regime_on=bool(regime_on), regime_downgraded=downgraded, raw_state=raw_state, rows=len(f), as_of=str(f.index[-1])[:10])
    rationale = why + (" " + zones["text"] if zones["text"] else "")
    if not regime_on and not downgraded and state not in ("thesis_deteriorating", "unknown"): rationale += " Market regime filter is OFF: treat any new position with extra caution."
    return EntryAssessment(state=state, ideal_zone=zones["ideal"], acceptable_zone=zones["acceptable"], chase_zone=zones["chase"], add_zone=zones["add"],
                           invalidation_price=zones["invalid"], rationale=rationale, metrics=metrics)
