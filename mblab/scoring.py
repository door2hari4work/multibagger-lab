"""Decomposable opportunity score. Weights are DECLARED DEFAULTS to be validated, never fitted; the score is never a single opaque number.

Conventions
- Every component value is 0..1 with "higher = better for the opportunity". For `risk` that means risk-ADJUSTED SAFETY (1 = low risk,
  0 = very risky); i.e. the caller passes the inverse of risk. State this in the component's `basis`.
- A component with value None (or data_quality == "missing") is NOT assessed: it is excluded and the remaining weights are renormalised.
  Nothing is ever imputed or defaulted to 0.5.
- data_quality "partial" counts at 0.75 of its weight and "stale" at 0.5 (a discount, not an imputation) and both reduce confidence.
- ScoreComponent.weight (default 1.0) is a MULTIPLIER on the declared weight, so a caller can emphasise one component without re-declaring all.
- `confidence` (low/medium/high) is about EVIDENCE COVERAGE, not about the return forecast.
- Dimensions (upside, probability, timing, downside, fit) are reported separately; the probability-weighted 'asymmetry' exists only when
  every supplied scenario carries a probability, and is always flagged as a model estimate.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from .schema import ScoreComponent, Scenario

DEFAULT_WEIGHTS = {
    "business_quality": 0.12, "growth_acceleration": 0.12, "earnings_inflection": 0.09, "tam_expansion": 0.06,
    "catalyst_strength": 0.08, "competitive_advantage": 0.09, "valuation_asymmetry": 0.12, "market_confirmation": 0.07,
    "timing": 0.06, "risk": 0.10, "thesis_robustness": 0.06, "portfolio_fit": 0.03,
}
assert abs(sum(DEFAULT_WEIGHTS.values()) - 1.0) < 1e-9
KEY_COMPONENTS = ("growth_acceleration", "valuation_asymmetry", "risk")
MIN_COMPONENTS = 5
QUALITY_FACTOR = {"ok": 1.0, "partial": 0.75, "stale": 0.5, "missing": 0.0}


@dataclass
class ScoreResult:
    overall: Optional[float]                 # 0..1 over assessed components only; None when nothing was assessed
    confidence: str                          # low | medium | high
    confidence_reasons: list = field(default_factory=list)
    contributions: list = field(default_factory=list)   # [{name, value, weight, share, contribution, data_quality, basis}], share sums to 1
    coverage: float = 0.0                    # share of the declared weight that was assessed
    assessed: list = field(default_factory=list)
    missing: list = field(default_factory=list)
    missing_key: list = field(default_factory=list)
    note: str = "Weights are declared defaults, not validated. Missing components are excluded, never imputed."


def compute(components: list, weights: Optional[dict] = None) -> ScoreResult:
    w = dict(DEFAULT_WEIGHTS if weights is None else weights)
    if any(v < 0 for v in w.values()): raise ValueError("weights must be non-negative")
    seen = set()
    rows, ignored = [], []
    for c in components:
        if c.name in seen: raise ValueError(f"duplicate component {c.name}")
        seen.add(c.name)
        if c.value is not None and not 0.0 <= c.value <= 1.0: raise ValueError(f"component {c.name} out of range 0..1: {c.value}")
        if c.weight is not None and c.weight < 0: raise ValueError(f"component {c.name}: negative weight multiplier")
        if c.name not in w:
            ignored.append(c.name); continue
        q = QUALITY_FACTOR.get(c.data_quality, 1.0)
        if c.value is None or q == 0.0: continue
        eff = w[c.name] * (c.weight if c.weight is not None else 1.0) * q
        if eff > 0: rows.append((c, eff))
    assessed_names = [c.name for c, _ in rows]
    missing = [n for n in w if n not in assessed_names]
    missing_key = [n for n in KEY_COMPONENTS if n in w and n not in assessed_names]
    total = sum(e for _, e in rows)
    declared_total = sum(w.values())
    coverage = (sum(w[c.name] for c, _ in rows) / declared_total) if declared_total else 0.0
    contributions = []
    overall = None
    if total > 0:
        overall = 0.0
        for c, e in rows:
            share = e / total
            overall += share * c.value
            contributions.append(dict(name=c.name, value=c.value, weight=round(e, 4), share=round(share, 4), contribution=round(share * c.value, 4),
                                      data_quality=c.data_quality, basis=c.basis))
        overall = round(overall, 4)
        contributions.sort(key=lambda r: -r["contribution"])

    reasons, cap = [], False
    if len(rows) < MIN_COMPONENTS:
        cap = True; reasons.append(f"only {len(rows)} component(s) assessed; at least {MIN_COMPONENTS} are needed for more than low confidence")
    if missing_key:
        cap = True; reasons.append("key component(s) not assessed: " + ", ".join(missing_key))
    degraded = [c.name for c, _ in rows if c.data_quality in ("partial", "stale")]
    if degraded: reasons.append("partial or stale data in: " + ", ".join(degraded))
    if ignored: reasons.append("ignored components with no declared weight: " + ", ".join(ignored))
    if cap or not rows:
        conf = "low"
    elif coverage >= 0.85 and len(rows) >= 9 and len(degraded) <= len(rows) // 4:
        conf = "high"
    elif coverage >= 0.60:
        conf = "medium"
    else:
        conf = "low"; reasons.append(f"coverage {coverage:.0%} of declared weight is below 60%")
    if not cap and conf != "high" and coverage < 0.85 and rows: reasons.append(f"coverage {coverage:.0%} of declared weight (high needs >= 85% and >= 9 components)")
    if not reasons: reasons.append("all key components assessed with good coverage")
    return ScoreResult(overall=overall, confidence=conf, confidence_reasons=reasons, contributions=contributions, coverage=round(coverage, 4),
                       assessed=assessed_names, missing=missing, missing_key=missing_key)


# ----------------------------------------------------------------------------------------------------------------------------
def _mid(s: Scenario) -> Optional[float]:
    if s.multiple_low is None and s.multiple_high is None: return None
    lo = s.multiple_low if s.multiple_low is not None else s.multiple_high
    hi = s.multiple_high if s.multiple_high is not None else s.multiple_low
    return (lo + hi) / 2.0


def dimensions(components: list, scenarios: Optional[list] = None, timing_state: Optional[str] = None) -> dict:
    """Upside, probability, timing, downside and fit side by side. A 20x with a tiny probability must not hide behind a blended number.
    scenarios: [schema.Scenario] (bull/base/bear). 'asymmetry' only if every scenario has a multiple AND a probability and they sum to ~1."""
    comp = {c.name: c for c in components}

    def val(n): return None if n not in comp or comp[n].data_quality == "missing" else comp[n].value
    sc = {s.name: s for s in (scenarios or [])}
    out = dict(
        upside=dict(bull_multiple=[sc["bull"].multiple_low, sc["bull"].multiple_high] if "bull" in sc else None,
                    base_multiple=[sc["base"].multiple_low, sc["base"].multiple_high] if "base" in sc else None),
        probability=dict(bull=sc["bull"].probability if "bull" in sc else None, base=sc["base"].probability if "base" in sc else None,
                         bear=sc["bear"].probability if "bear" in sc else None, is_model_estimate=True),
        timing=dict(score=val("timing"), state=timing_state),
        downside=dict(bear_multiple=[sc["bear"].multiple_low, sc["bear"].multiple_high] if "bear" in sc else None, risk_safety_score=val("risk")),
        fit=dict(score=val("portfolio_fit")),
        asymmetry=None,
    )
    reason = None
    if not sc: reason = "no scenarios supplied"
    else:
        probs = [s.probability for s in sc.values()]
        mids = [_mid(s) for s in sc.values()]
        if any(p is None for p in probs): reason = "at least one scenario has no probability"
        elif any(m is None for m in mids): reason = "at least one scenario has no multiple"
        elif any(not 0 <= p <= 1 for p in probs): reason = "a probability is outside 0..1"
        elif abs(sum(probs) - 1) > 0.05: reason = f"scenario probabilities sum to {sum(probs):.2f}, not about 1"
    if reason is None:
        ev = sum(s.probability * _mid(s) for s in sc.values())
        gain = sum(s.probability * (_mid(s) - 1) for s in sc.values() if _mid(s) > 1)
        loss = sum(s.probability * (1 - _mid(s)) for s in sc.values() if _mid(s) < 1)
        out["asymmetry"] = dict(expected_multiple=round(ev, 3), expected_return_pct=round((ev - 1) * 100, 1),
                                gain_loss_ratio=None if loss <= 0 else round(gain / loss, 2), p_loss=round(sum(s.probability for s in sc.values() if _mid(s) < 1), 3),
                                model_estimate=True,
                                note="Probability-weighted over scenario midpoints; every input is a model estimate, not a forecast. Not comparable across theses unless horizons match.")
    else:
        out["asymmetry_unavailable_because"] = reason
    return out
