"""Integration step: attaches timing assessment, portfolio fit and a decomposed score to researched theses (new versions; never overwrites).
All mappings from evidence to 0..1 are DECLARED heuristics stated in each component's `basis`; nothing is imputed; weights are unvalidated defaults."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Optional
import pandas as pd

from . import store, scoring, timing
from .portfolio import fit_score
from .schema import ScoreComponent, Thesis, EntryState, Status

ROOT = Path(__file__).resolve().parent.parent


def _mid(s) -> Optional[float]:
    return None if s is None or s.multiple_low is None or s.multiple_high is None else (s.multiple_low + s.multiple_high) / 2


def scenario_ev(t: Thesis) -> Optional[float]:
    """Probability-weighted midpoint multiple across bull/base/bear (MODEL ESTIMATE). None unless all three have a probability and range."""
    parts = [(s.probability, _mid(s)) for s in (t.bull_case, t.base_case, t.bear_case) if s]
    if len(parts) != 3 or any(p is None or m is None for p, m in parts): return None
    return sum(p * m for p, m in parts)


def candidate_row(market: str, ticker: str) -> Optional[dict]:
    f = ROOT / "research" / f"candidates_{market}.json"
    if not f.exists(): return None
    d = json.loads(f.read_text()); rows = d if isinstance(d, list) else (d.get("candidates") or d.get("rows") or d.get("results") or [])
    return next((r for r in rows if str(r.get("ticker", "")).upper() == ticker.upper()), None)


def build_components(t: Thesis, cand: Optional[dict], fit) -> list:
    comps = []
    for k, c in ((cand or {}).get("scores") or {}).items():
        if k in ("market_confirmation", "growth_acceleration", "earnings_inflection", "valuation_asymmetry") and c.get("value") is not None and k != "valuation_asymmetry":
            comps.append(ScoreComponent(k, float(c["value"]), 1.0, "discovery screen: " + str(c.get("basis", ""))[:160], c.get("data_quality", "ok")))
    ev = scenario_ev(t)
    if ev is not None:   # replaces the screen's rough valuation proxy with the researched, probability-weighted view
        v = max(0.0, min(1.0, (ev - 0.6) / 1.0))
        comps.append(ScoreComponent("valuation_asymmetry", round(v, 3), 1.0, f"declared map of the scenario-weighted expected multiple ({ev:.2f}x, model estimate): 0.6x -> 0, 1.6x -> 1", "ok"))
        if t.bear_case and t.bear_case.probability is not None and _mid(t.bear_case) is not None:
            loss = t.bear_case.probability * max(0.0, 1 - _mid(t.bear_case))
            comps.append(ScoreComponent("risk", round(max(0.0, min(1.0, 1 - loss / 0.5)), 3), 1.0, f"risk-adjusted SAFETY (higher = safer) from the thesis bear case: probability-weighted loss {loss:.0%} mapped so 0% -> 1 and 50% -> 0", "ok"))
    if t.adversarial.done:
        comps.append(ScoreComponent("thesis_robustness", {"survives": 0.8, "downgraded": 0.4, "killed": 0.0}.get(t.adversarial.verdict), 1.0, f"independent adversarial review verdict '{t.adversarial.verdict}' (declared map: survives 0.8, downgraded 0.4, killed 0)", "ok"))
    if fit is not None and fit.score is not None:
        comps.append(ScoreComponent("portfolio_fit", float(fit.score), 1.0, "portfolio_fit: 0.5 neutral; below 0.5 mostly adds to exposure already held heavily", "partial"))
    return comps


def refresh(t: Thesis, ohlcv: Optional[pd.DataFrame], regime_on: Optional[bool], cand: Optional[dict], analytics: Optional[dict]) -> Thesis:
    """Mutates and returns the thesis (caller saves a new version)."""
    if ohlcv is not None and regime_on is not None:
        a = timing.assess(ohlcv, regime_on=regime_on, thesis_ok=(t.adversarial.verdict != "killed"))
        gated = a.state in (EntryState.ATTRACTIVE_ENTRY.value, EntryState.CONFIRMATION_ENTRY.value, EntryState.BREAKOUT_ENTRY.value)
        if gated and not (t.research_level >= 4 and t.adversarial.done):   # never let timing alone imply an entry call
            a.rationale = f"[{a.state} on the chart but the thesis has not cleared research gates] " + a.rationale; a.state = EntryState.SETUP_FORMING.value
        t.entry.state, t.entry.ideal_zone, t.entry.acceptable_zone, t.entry.chase_zone, t.entry.add_zone = a.state, a.ideal_zone, a.acceptable_zone, a.chase_zone, a.add_zone
        if a.invalidation_price is not None: t.entry.invalidation_price = a.invalidation_price
        t.entry.rationale = a.rationale + " Timing describes entry price risk, not a forecast: validation on history found no return edge from timing states."
    fit = None
    if analytics is not None and cand is not None:
        fit = fit_score({"ticker": t.ticker, "name": t.company, "sector": cand.get("sector"), "market": t.market,
                         "market_cap_bucket": "mid" if cand.get("segment") == "mid" else "small"}, analytics)
        t.portfolio_fit = fit
    comps = build_components(t, cand, fit); t.scores = comps
    r = scoring.compute(comps); t.overall_score = None if r.overall is None else round(r.overall, 3)
    return t
