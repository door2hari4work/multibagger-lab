"""Build Thesis objects WITHOUT an LLM (Level 1/2 snapshots from a discovery candidate row) and assemble deeper theses from a dict an agent supplies.

Honesty rules baked in:
- A snapshot contains only what the candidate row actually says (price, model rank/score) as FACT evidence with source_type price/model.
  It has NO invented catalysts, scenarios, mechanism or entry plan; those fields stay empty and status is research_required.
- assemble_deep_thesis() never lets a payload skip validate(); it also reports 'quality' problems (e.g. level 3 claimed with too few primary-source FACTs,
  adversarial review with unanswered questions) that validate() does not check. Callers must save only when the problem list is empty.

CLI (used by research/PLAYBOOK.md):
    python -m mblab.thesis_builder snapshot  candidate_row.json [--save]
    python -m mblab.thesis_builder assemble  payload.json --reason "why this version" [--save]
"""
from __future__ import annotations
import json
import sys
from dataclasses import fields
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

from .schema import (Thesis, Evidence, Scenario, Catalyst, ExitTrigger, ScoreComponent, EntryPlan, AdversarialReview, PortfolioFit,
                     Status, EntryState, ENTRY_STATUSES, DISCLAIMER, validate, now_iso)

PRIMARY_SOURCE_TYPES = {"filing", "exchange", "call", "investor_presentation"}
DEFAULT_CURRENCY = {"IN": "INR", "US": "USD"}
SNAPSHOT_REVIEW_DAYS = 14
DEEP_REVIEW_DAYS = 30

ADVERSARIAL_QUESTIONS = [
    "what_evidence_would_make_it_wrong", "what_is_missing", "is_catalyst_priced_in", "does_valuation_fit_growth", "great_company_vs_great_stock",
    "merely_an_ai_narrative", "is_it_crowded", "strongest_bear_argument", "what_happened_in_similar_setups", "what_must_happen_for_5x",
    "is_5x_plausible_in_1_2_years", "probability_market_already_right",
]
_UNANSWERED = ("", "cannot answer", "can't answer", "unknown", "n/a", "na", "tbd", "none")


# --------------------------------------------------------------------------- Level 1/2 snapshot (no LLM)
def _first(row: dict, *keys, default=None):
    for k in keys:
        if row.get(k) not in (None, ""): return row[k]
    return default


def _num(x) -> Optional[float]:
    try: return None if x in (None, "") else float(x)
    except (TypeError, ValueError): return None


def _iso(x) -> str:
    return str(x)[:10] if x else ""


def build_from_candidate(row: dict, today: Optional[date] = None, research_level: int = 1) -> Thesis:
    """Level-1 (or 2) factual snapshot from one discovery candidate row. Tolerant of key aliases; raises ValueError only if ticker/market cannot be determined.
    Recognised keys: ticker|symbol, company|name, market, price|last_price|close, price_ts|price_date|as_of|date, currency, rank, score|discovery_score,
    momentum_pct|momentum_rank_pct (0..1 percentile), market_cap, valuation (dict), source|signal|reason."""
    today = today or date.today()
    ticker = str(_first(row, "ticker", "symbol", default="")).strip()
    market = str(_first(row, "market", default="")).strip().upper()
    if not ticker or not market: raise ValueError("candidate row needs ticker and market")
    price = _num(_first(row, "price", "last_price", "close"))
    price_ts = _iso(_first(row, "price_ts", "price_date", "as_of", "date"))
    currency = str(_first(row, "currency", default=DEFAULT_CURRENCY.get(market, ""))).upper()
    rank, score = _first(row, "rank"), _num(_first(row, "score", "discovery_score"))
    mom = _num(_first(row, "momentum_pct", "momentum_rank_pct"))
    asof = price_ts or today.isoformat()

    ev = []
    if price is not None and price_ts:
        ev.append(Evidence(id="e1", claim=f"Last price {price:g} {currency} on {price_ts} (market data snapshot).", kind="FACT", source_type="price",
                           source_url=str(_first(row, "price_source", default="")), source_date=price_ts, retrieved_at=now_iso(),
                           note="Price snapshot only; says nothing about business quality."))
    model_bits = []
    if rank is not None: model_bits.append(f"rank {rank}")
    if score is not None: model_bits.append(f"score {score:g}")
    if mom is not None: model_bits.append(f"momentum percentile {mom:g}")
    if model_bits:
        sig = _first(row, "signal", "source", "reason", default="")
        ev.append(Evidence(id=f"e{len(ev) + 1}", claim=f"Quantitative discovery output for {ticker}: {', '.join(model_bits)}" + (f" ({sig})" if sig else "") + ". Model output, not a verified business fact.",
                           kind="FACT", source_type="model", source_date=asof, retrieved_at=now_iso(),
                           note="Momentum rank is the only selector validated in this lab, and only modestly; it is a reason to spend research time, not a thesis."))

    scores = []
    if mom is not None and 0 <= mom <= 1:
        scores.append(ScoreComponent(name="market_confirmation", value=mom, basis="momentum percentile from discovery run (price-based only)", data_quality="partial"))

    valuation = {k: v for k, v in (row.get("valuation") or {}).items() if isinstance(v, (int, float))}
    if _num(row.get("market_cap")) is not None: valuation["market_cap"] = _num(row["market_cap"])

    return Thesis(
        ticker=ticker.upper(), company=str(_first(row, "company", "name", default=ticker)), market=market, status=Status.RESEARCH_REQUIRED.value,
        research_level=research_level, as_of=asof, price=price, price_ts=price_ts, currency=currency,
        why_now="Flagged by the quantitative discovery screen; no qualitative research has been done yet.",
        thesis="", multibagger_mechanism="", expectations_gap="",
        risks=["Not yet researched: business quality, financials, valuation, catalysts and adversarial review are all unassessed."],
        valuation=valuation, scores=scores, overall_score=None, confidence="low", entry=EntryPlan(state=EntryState.UNKNOWN.value),
        evidence=ev, next_review=(today + timedelta(days=SNAPSHOT_REVIEW_DAYS)).isoformat(),
    )


# --------------------------------------------------------------------------- deeper theses from an agent-supplied dict
def _scenario(x, default_name: str) -> Optional[Scenario]:
    if x is None: return None
    if isinstance(x, Scenario): return x
    d = dict(x); d.setdefault("name", default_name); d.setdefault("probability_is_model_estimate", True)
    return Scenario(**d)


def _normalise(payload: dict, base: Optional[Thesis], today: date) -> dict:
    d = base.to_dict() if base else {}
    for k in ("version", "parent_version", "change_log", "created_at"): d.pop(k, None)
    p = dict(payload)
    for k in ("version", "parent_version", "change_log", "created_at", "disclaimer", "overall_score"): p.pop(k, None)   # store / scoring own these
    # evidence: merge by id (append-only spirit) unless explicitly replaced
    new_ev = []
    for i, e in enumerate(p.pop("evidence", []) or [], 1):
        e = dict(e); e.setdefault("retrieved_at", now_iso()); new_ev.append(e)
    old_ev = [] if p.pop("replace_evidence", False) else list(d.get("evidence", []))
    used = {e["id"] for e in old_ev} | {e["id"] for e in new_ev if e.get("id")}
    n = 0
    for e in new_ev:
        if not e.get("id"):
            while f"e{n + 1}" in used: n += 1
            n += 1; e["id"] = f"e{n}"; used.add(e["id"])
    by_id = {e["id"]: e for e in old_ev}
    for e in new_ev: by_id[e["id"]] = e
    d.update(p)
    d["evidence"] = list(by_id.values())
    for key, nm in (("bull_case", "bull"), ("base_case", "base"), ("bear_case", "bear")):
        s = _scenario(d.get(key), nm); d[key] = None if s is None else s.__dict__.copy()
    d["catalysts"] = [c if isinstance(c, dict) else {"description": str(c)} for c in d.get("catalysts", [])]
    d["disclaimer"] = DISCLAIMER
    d["as_of"] = p.get("as_of") or today.isoformat()      # a new version is current as of the supplied date, never silently inherits the old one
    return d


def quality_problems(t: Thesis) -> list:
    """Checks validate() does not do: is the claimed research level actually supported by the content?"""
    p = []
    non_snap = [e for e in t.evidence if e.kind == "FACT" and e.source_type not in ("price", "model")]
    primary = [e for e in non_snap if e.source_type in PRIMARY_SOURCE_TYPES]
    if t.research_level >= 2 and not non_snap: p.append("level>=2 needs at least one FACT beyond the price/model snapshot")
    if t.research_level >= 3:
        if len(primary) < 3: p.append("level>=3 needs at least 3 primary-source FACTs (filing/exchange/call/investor_presentation)")
        if not t.thesis or not t.risks: p.append("level>=3 needs a written thesis and a non-empty risk list")
        if not any(e.kind != "FACT" for e in t.evidence): p.append("level>=3 should tag its judgments as INFERENCE/SPECULATION evidence, not only FACTs")
        if t.base_case is None or t.bear_case is None: p.append("level>=3 needs at least base and bear scenarios")
    if t.research_level >= 4 or t.adversarial.done:
        un = unanswered_questions(t.adversarial.questions)
        if not t.adversarial.done: p.append("level>=4 needs a completed adversarial review")
        if un and t.adversarial.verdict == "survives": p.append("adversarial verdict 'survives' with unanswered questions: " + ", ".join(un))
    for c in t.catalysts:
        if not c.evidence_ids: p.append(f"catalyst without evidence_ids: {c.description[:50]!r} (label it as speculation in the description if it has no source)")
    ids = {e.id for e in t.evidence}
    for c in t.catalysts:
        for i in c.evidence_ids:
            if i not in ids: p.append(f"catalyst references unknown evidence id {i}")
    return p


def assemble_deep_thesis(payload: dict, base: Optional[Thesis] = None, today: Optional[date] = None) -> tuple:
    """Build a Thesis from agent-supplied fields (any subset of Thesis.to_dict(); evidence merged by id with the base thesis).
    Returns (thesis | None, problems). problems = schema errors + validate() + quality_problems(). Save with store.save_new_version only if problems == []."""
    today = today or date.today()
    names = {f.name for f in fields(Thesis)} | {"replace_evidence"}
    unknown = sorted(set(payload) - names - {"version", "parent_version", "change_log", "created_at", "disclaimer", "overall_score"})
    problems = [f"unknown field in payload: {u}" for u in unknown]
    try: t = Thesis.from_dict(_normalise({k: v for k, v in payload.items() if k not in unknown}, base, today))
    except (TypeError, ValueError, KeyError) as ex: return None, problems + [f"payload could not be built into a Thesis: {ex}"]
    if not t.next_review:
        t.next_review = (today + timedelta(days=DEEP_REVIEW_DAYS if t.research_level >= 3 else SNAPSHOT_REVIEW_DAYS)).isoformat()
    if base and t.research_level < base.research_level and "research_level" not in payload: t.research_level = base.research_level
    problems += validate(t, today=today) + quality_problems(t)
    return t, problems


def unanswered_questions(questions: dict) -> list:
    out = []
    for q in ADVERSARIAL_QUESTIONS:
        a = str((questions or {}).get(q, "")).strip().lower().rstrip(".")
        if a in _UNANSWERED or a.startswith("cannot answer") or len(a) < 15: out.append(q)
    return out


def apply_adversarial(t: Thesis, review: dict, today: Optional[date] = None) -> Thesis:
    """Apply a devil's-advocate review. Enforces: any unanswered question caps the verdict at 'downgraded'; 'killed' moves the thesis to rejected/thesis_broken.
    Mutates and returns t; caller still runs validate() and saves."""
    today = today or date.today()
    verdict = review.get("verdict", "")
    if verdict not in ("survives", "downgraded", "killed"): raise ValueError("verdict must be survives | downgraded | killed")
    un = unanswered_questions(review.get("questions", {}))
    if un and verdict == "survives": verdict = "downgraded"      # cannot answer -> downgrade
    t.adversarial = AdversarialReview(done=True, reviewer=review.get("reviewer", "devils_advocate"), verdict=verdict,
                                      strongest_bear_case=review.get("strongest_bear_case", ""), questions=dict(review.get("questions", {})), reviewed_at=now_iso())
    if un: t.adversarial.questions = {**t.adversarial.questions, **{q: (t.adversarial.questions.get(q) or "cannot answer") for q in un}}
    entry_states = (EntryState.ATTRACTIVE_ENTRY.value, EntryState.CONFIRMATION_ENTRY.value, EntryState.BREAKOUT_ENTRY.value)
    if verdict == "killed":
        t.status = Status.THESIS_BROKEN.value if t.status in (Status.HOLD.value, Status.ACCUMULATE.value, Status.TRIM.value) else Status.REJECTED.value
        t.entry.state = EntryState.UNKNOWN.value
    elif verdict == "downgraded":
        t.confidence = "low"
        if t.status in {s.value for s in ENTRY_STATUSES} or t.status == Status.PREPARING_TO_ENTER.value: t.status = Status.WATCHLIST.value
        if t.entry.state in entry_states: t.entry.state = EntryState.SETUP_FORMING.value
    return t


def save_payload(payload: dict, reason: str, base_dir: Optional[Path] = None, today: Optional[date] = None, adversarial: Optional[dict] = None, dry_run: bool = False) -> tuple:
    """Load latest thesis (if any) as base, assemble, optionally apply an adversarial review, and save a new version only when there are no problems.
    Returns (saved_thesis | None, problems)."""
    from . import store
    ticker, market = payload.get("ticker"), payload.get("market")
    base = store.load(market, ticker, base=base_dir) if ticker and market else None
    if base is None and not (ticker and market and payload.get("company")): return None, ["payload needs ticker, market and company for a new thesis"]
    t, problems = assemble_deep_thesis(payload, base, today)
    if t is None: return None, problems
    if adversarial:
        apply_adversarial(t, adversarial, today)
        problems = [x for x in problems if "adversarial" not in x] + validate(t, today=today) + quality_problems(t)
        problems = list(dict.fromkeys(problems))
    if problems: return None, problems
    if dry_run: return t, []
    return store.save_new_version(t, reason=reason, base=base_dir, today=today), []


# --------------------------------------------------------------------------- CLI
def _main(argv: list) -> int:
    from . import store
    if len(argv) < 2 or argv[0] not in ("snapshot", "assemble"):
        print(__doc__); return 2
    cmd, path = argv[0], argv[1]
    data = json.loads(Path(path).read_text())
    save = "--save" in argv
    reason = argv[argv.index("--reason") + 1] if "--reason" in argv else ""
    if cmd == "snapshot":
        t = build_from_candidate(data); problems = validate(t)
        if store.load(t.market, t.ticker) is not None: problems.append("a thesis already exists; a snapshot must never become a newer version of a deeper thesis")
        if not problems and save: t = store.save_new_version(t, reason=reason or "level-1 snapshot from discovery candidate")
    else:
        adv = data.pop("adversarial_review", None)
        t, problems = save_payload(data, reason or "agent update", adversarial=adv, dry_run=not save)
    if problems:
        print("NOT SAVED. Problems:"); [print(" -", x) for x in problems]; return 1
    print(("saved " if save else "valid (dry run) ") + f"{t.market}/{t.ticker} v{t.version}"); return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
