"""Canonical thesis object for MultibaggerLab. ONE shared definition; every agent/module reads and writes this, never its own variant.

Design rules (see docs/PRODUCT_SPEC.md):
- A thesis is VERSIONED and append-only: new evidence => new version, history never overwritten.
- Every evidence item is tagged FACT / INFERENCE / SPECULATION; a FACT needs a source and a source date.
- Probabilities are MODEL ESTIMATES and carry that flag; the product never states certainty.
- Status 'attractive entry' / 'accumulate' cannot be set without research level >= 4, a completed adversarial review, and fresh evidence (validate()).
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict, fields
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Optional
import re


class EvidenceKind(str, Enum):
    FACT = "FACT"; INFERENCE = "INFERENCE"; SPECULATION = "SPECULATION"


class Status(str, Enum):  # opportunity lifecycle
    EARLY_DISCOVERY = "early_discovery"; RESEARCH_REQUIRED = "research_required"; WATCHLIST = "watchlist"; PREPARING_TO_ENTER = "preparing_to_enter"
    ATTRACTIVE_ENTRY = "attractive_entry"; ACCUMULATE = "accumulate"; HOLD = "hold"; TRIM = "trim"; EXIT = "exit"; THESIS_BROKEN = "thesis_broken"; REJECTED = "rejected"


class EntryState(str, Enum):  # timing state machine
    TOO_EARLY = "too_early"; SETUP_FORMING = "setup_forming"; ATTRACTIVE_ENTRY = "attractive_entry"; CONFIRMATION_ENTRY = "confirmation_entry"
    BREAKOUT_ENTRY = "breakout_entry"; OVEREXTENDED = "overextended"; WAIT_FOR_PULLBACK = "wait_for_pullback"; THESIS_DETERIORATING = "thesis_deteriorating"; UNKNOWN = "unknown"


class Action(str, Enum):
    HOLD = "hold"; ADD = "add"; TRIM = "trim"; EXIT = "exit"; EMERGENCY_REVIEW = "emergency_thesis_review"


ENTRY_STATUSES = {Status.ATTRACTIVE_ENTRY, Status.ACCUMULATE}
BANNED_PHRASES = [r"\bwill become a multi-?bagger\b", r"\bguaranteed\b", r"\bcan't lose\b", r"\brisk[- ]free\b", r"\bsure[- ]shot\b", r"\bno downside\b"]
DISCLAIMER = "Model estimates and research notes, not investment advice or a prediction. The user makes every decision."


def now_iso() -> str: return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class Evidence:
    id: str
    claim: str
    kind: str                      # EvidenceKind value
    source_type: str = ""          # filing | call | exchange | investor_presentation | price | news | analyst | model | other
    source_url: str = ""
    source_date: str = ""          # ISO date of the underlying document/data
    period: str = ""               # financial period, e.g. FY2026, Q2FY27
    retrieved_at: str = ""
    note: str = ""


@dataclass
class ScoreComponent:
    name: str                      # e.g. growth_acceleration
    value: Optional[float]         # 0..1, None = not assessed
    weight: float = 1.0
    basis: str = ""                # one-line explanation / metric used
    data_quality: str = "ok"       # ok | partial | missing | stale


@dataclass
class Scenario:
    name: str                      # bull | base | bear
    description: str
    multiple_low: Optional[float] = None    # e.g. 5.0 = 5x from current price
    multiple_high: Optional[float] = None
    probability: Optional[float] = None     # MODEL ESTIMATE 0..1, never a certainty
    horizon_months: Optional[int] = None
    probability_is_model_estimate: bool = True


@dataclass
class Catalyst:
    description: str
    window: str = ""               # e.g. "Q4 FY27 results (Feb 2027)"
    status: str = "pending"        # pending | occurred | failed | delayed
    evidence_ids: list = field(default_factory=list)


@dataclass
class EntryPlan:
    state: str = EntryState.UNKNOWN.value
    ideal_zone: Optional[list] = None        # [low, high] in local currency, rounded; no false precision
    acceptable_zone: Optional[list] = None
    chase_zone: Optional[list] = None
    add_zone: Optional[list] = None
    invalidation_price: Optional[float] = None
    rationale: str = ""


@dataclass
class ExitTrigger:
    type: str                      # thesis_invalidation | earnings_deterioration | catalyst_failure | valuation_excess | narrative_saturation | technical | rotation | target
    condition: str                 # human-readable, testable condition
    status: str = "armed"          # armed | warning | triggered


@dataclass
class AdversarialReview:
    done: bool = False
    reviewer: str = ""
    verdict: str = ""              # survives | downgraded | killed
    strongest_bear_case: str = ""
    questions: dict = field(default_factory=dict)   # the 12 self-critique questions -> answers
    reviewed_at: str = ""


@dataclass
class PortfolioFit:
    score: Optional[float] = None
    summary: str = ""
    overlap_notes: list = field(default_factory=list)
    suggested_max_weight_pct: Optional[float] = None


@dataclass
class Thesis:
    ticker: str
    company: str
    market: str                    # IN | US | other ISO-ish code
    version: int = 1
    status: str = Status.EARLY_DISCOVERY.value
    research_level: int = 1        # 1 discovery .. 6 timing
    as_of: str = ""                # date the underlying information was current
    created_at: str = field(default_factory=now_iso)
    price: Optional[float] = None
    price_ts: str = ""
    currency: str = ""
    why_now: str = ""
    thesis: str = ""
    multibagger_mechanism: str = ""
    expectations_gap: str = ""
    time_horizon_months: Optional[int] = None
    bull_case: Optional[Scenario] = None
    base_case: Optional[Scenario] = None
    bear_case: Optional[Scenario] = None
    catalysts: list = field(default_factory=list)       # [Catalyst]
    risks: list = field(default_factory=list)           # [str]
    valuation: dict = field(default_factory=dict)       # free-form numbers with units, e.g. {"pe_ttm": 31.2, "ev_sales": 6.1}
    scores: list = field(default_factory=list)          # [ScoreComponent]
    overall_score: Optional[float] = None               # computed from scores by mblab.scoring; never hand-typed
    confidence: str = "low"                             # low | medium | high (evidence quality, not a return forecast)
    entry: EntryPlan = field(default_factory=EntryPlan)
    exit_rules: list = field(default_factory=list)      # [ExitTrigger]
    adversarial: AdversarialReview = field(default_factory=AdversarialReview)
    portfolio_fit: PortfolioFit = field(default_factory=PortfolioFit)
    evidence: list = field(default_factory=list)        # [Evidence]
    next_review: str = ""
    change_log: list = field(default_factory=list)      # [str], filled by the store from the previous version
    parent_version: Optional[int] = None
    disclaimer: str = DISCLAIMER

    # ---- (de)serialisation -------------------------------------------------
    def to_dict(self) -> dict: return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Thesis":
        d = dict(d)
        def sc(x): return None if x is None else Scenario(**x)
        d["bull_case"], d["base_case"], d["bear_case"] = sc(d.get("bull_case")), sc(d.get("base_case")), sc(d.get("bear_case"))
        d["catalysts"] = [Catalyst(**c) for c in d.get("catalysts", [])]
        d["scores"] = [ScoreComponent(**c) for c in d.get("scores", [])]
        d["exit_rules"] = [ExitTrigger(**c) for c in d.get("exit_rules", [])]
        d["evidence"] = [Evidence(**c) for c in d.get("evidence", [])]
        d["entry"] = EntryPlan(**d.get("entry", {})); d["adversarial"] = AdversarialReview(**d.get("adversarial", {})); d["portfolio_fit"] = PortfolioFit(**d.get("portfolio_fit", {}))
        names = {f.name for f in fields(Thesis)}
        return Thesis(**{k: v for k, v in d.items() if k in names})


def _text_fields(t: Thesis) -> list:
    out = [t.why_now, t.thesis, t.multibagger_mechanism, t.expectations_gap, t.entry.rationale, t.portfolio_fit.summary, t.adversarial.strongest_bear_case]
    for s in (t.bull_case, t.base_case, t.bear_case):
        if s: out.append(s.description)
    out += [c.description for c in t.catalysts] + list(t.risks) + [e.claim for e in t.evidence]
    return [x for x in out if x]


def validate(t: Thesis, today: Optional[date] = None, max_evidence_age_days: int = 120) -> list:
    """Returns a list of problems (empty = valid). Hard rules that stop the product manufacturing certainty or stale confidence."""
    p, today = [], today or date.today()
    if not t.ticker or not t.market: p.append("ticker and market are required")
    if not 1 <= t.research_level <= 6: p.append("research_level must be 1..6")
    if t.status not in {s.value for s in Status}: p.append(f"unknown status {t.status}")
    if t.entry.state not in {s.value for s in EntryState}: p.append(f"unknown entry state {t.entry.state}")
    ids = [e.id for e in t.evidence]
    if len(ids) != len(set(ids)): p.append("duplicate evidence ids")
    for e in t.evidence:
        if e.kind not in {k.value for k in EvidenceKind}: p.append(f"evidence {e.id}: kind must be FACT/INFERENCE/SPECULATION")
        if e.kind == EvidenceKind.FACT.value and not (e.source_type and e.source_date and (e.source_url or e.source_type in ("price", "model"))):
            p.append(f"evidence {e.id}: a FACT needs source_type, source_date and source_url")
    for s in (t.bull_case, t.base_case, t.bear_case):
        if s and s.probability is not None and not s.probability_is_model_estimate: p.append(f"scenario {s.name}: probabilities must be flagged as model estimates")
        if s and s.probability is not None and not 0 <= s.probability <= 1: p.append(f"scenario {s.name}: probability out of range")
    probs = [s.probability for s in (t.bull_case, t.base_case, t.bear_case) if s and s.probability is not None]
    if len(probs) == 3 and abs(sum(probs) - 1) > 0.05: p.append("scenario probabilities should sum to about 1")
    for txt in _text_fields(t):
        for pat in BANNED_PHRASES:
            if re.search(pat, txt, re.I): p.append(f"certainty language not allowed: '{re.search(pat, txt, re.I).group(0)}'")
    for c in t.scores:
        if c.value is not None and not 0 <= c.value <= 1: p.append(f"score {c.name} out of 0..1")
    if t.status in {s.value for s in ENTRY_STATUSES} or t.entry.state in (EntryState.ATTRACTIVE_ENTRY.value, EntryState.CONFIRMATION_ENTRY.value, EntryState.BREAKOUT_ENTRY.value):
        if t.research_level < 4: p.append("an entry/accumulate call needs research_level >= 4")
        if not (t.adversarial.done and t.adversarial.verdict in ("survives", "downgraded")): p.append("an entry/accumulate call needs a completed adversarial review that did not kill the thesis")
        if not t.exit_rules or t.entry.invalidation_price is None and not any(x.type == "thesis_invalidation" for x in t.exit_rules): p.append("an entry/accumulate call needs explicit invalidation / exit rules")
        dated = []
        for e in t.evidence:
            if e.kind == EvidenceKind.FACT.value and e.source_date:
                try: dated.append(date.fromisoformat(e.source_date[:10]))
                except ValueError: p.append(f"evidence {e.id}: bad source_date")
        if not dated or (today - max(dated)).days > max_evidence_age_days: p.append(f"entry call needs at least one FACT newer than {max_evidence_age_days} days")
    if t.adversarial.verdict == "killed" and t.status not in (Status.REJECTED.value, Status.THESIS_BROKEN.value, Status.EXIT.value): p.append("a killed thesis must have status rejected/thesis_broken/exit")
    return p
