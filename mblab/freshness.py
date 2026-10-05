"""Staleness classification for evidence and prices, and 'what changed since thesis version N'.

Pure functions, no network. 'Current data' is a plain dict supplied by the caller (a monitoring/research session or a data module):

    {"as_of": "2026-10-05", "price": 912.5, "price_ts": "2026-10-03", "currency": "INR",
     "valuation": {"pe_ttm": 28.0, "ev_sales": 5.2},
     "evidence": [ {Evidence-shaped dict, id/claim/kind/source_type/source_url/source_date/period}, ... ],   # NEW items found since
     "events":   [ {"date": "2026-09-30", "type": "filing|results|guidance|8-K|news|corporate_action", "summary": "..."} ]}

Freshness classes: fresh | aging | stale | unknown (unknown = missing or unparseable date; never silently treated as fresh).
"""
from __future__ import annotations
from datetime import date, datetime
from typing import Optional

# (fresh_up_to_days, aging_up_to_days); older than the second number = stale. Calendar days.
FRESHNESS_DAYS = {
    "price": (3, 10),                  # a quote older than ~a week is not a current price
    "model": (7, 30),                  # quantitative model output
    "news": (14, 45),
    "analyst": (30, 90),
    "filing": (100, 200),              # a 10-K/10-Q/annual report is current for roughly one reporting cycle
    "exchange": (100, 200),
    "call": (100, 200),                # earnings-call transcripts
    "investor_presentation": (100, 200),
    "other": (90, 180),
}
PRICE_MOVE_MATERIAL_PCT = 15.0         # price move since a thesis version that deserves a look
VALUATION_MOVE_MATERIAL_PCT = 20.0


def _d(x) -> Optional[date]:
    if not x: return None
    if isinstance(x, datetime): return x.date()
    if isinstance(x, date): return x
    try: return date.fromisoformat(str(x)[:10])
    except ValueError: return None


def age_days(source_date, today: Optional[date] = None) -> Optional[int]:
    d = _d(source_date)
    return None if d is None else ((today or date.today()) - d).days


def classify_age(age: Optional[int], source_type: str = "other") -> str:
    if age is None: return "unknown"
    fresh, aging = FRESHNESS_DAYS.get(source_type or "other", FRESHNESS_DAYS["other"])
    if age < 0: return "unknown"                       # dated in the future: suspect, not fresh
    return "fresh" if age <= fresh else "aging" if age <= aging else "stale"


def evidence_freshness(e, today: Optional[date] = None) -> dict:
    """e: Evidence or dict. SPECULATION/INFERENCE items carry no source date and are reported as 'unknown' (they are judgments, not data)."""
    g = (lambda k: getattr(e, k, "")) if not isinstance(e, dict) else (lambda k: e.get(k, ""))
    a = age_days(g("source_date"), today)
    return {"id": g("id"), "kind": g("kind"), "source_type": g("source_type"), "source_date": g("source_date"), "age_days": a, "freshness": classify_age(a, g("source_type"))}


def price_freshness(price_ts, today: Optional[date] = None) -> dict:
    a = age_days(price_ts, today)
    return {"price_ts": price_ts or "", "age_days": a, "freshness": classify_age(a, "price")}


def thesis_freshness(t, today: Optional[date] = None) -> dict:
    """Overall staleness picture of a Thesis. needs_refresh is True when the price is stale, no FACT is fresh/aging, or next_review has passed."""
    today = today or date.today()
    facts = [evidence_freshness(e, today) for e in t.evidence if e.kind == "FACT"]
    dated = [f for f in facts if f["age_days"] is not None]
    counts = {k: sum(1 for f in facts if f["freshness"] == k) for k in ("fresh", "aging", "stale", "unknown")}
    pf = price_freshness(t.price_ts, today)
    nr = _d(t.next_review)
    review_overdue = bool(nr and nr < today)
    newest = min((f["age_days"] for f in dated), default=None)
    oldest = max((f["age_days"] for f in dated), default=None)
    # ignore price/model snapshot facts when asking "is any primary evidence still current?"
    prim = [f for f in dated if f["source_type"] not in ("price", "model")]
    no_current_primary = not any(f["freshness"] in ("fresh", "aging") for f in prim)
    reasons = []
    if pf["freshness"] in ("stale", "unknown"): reasons.append(f"price is {pf['freshness']}")
    if t.research_level >= 2 and no_current_primary: reasons.append("no current primary-source FACT")
    if review_overdue: reasons.append(f"next_review {t.next_review} has passed")
    if counts["stale"]: reasons.append(f"{counts['stale']} stale FACT(s)")
    return {"ticker": t.ticker, "market": t.market, "version": t.version, "price": pf, "fact_counts": counts, "newest_fact_age_days": newest,
            "oldest_fact_age_days": oldest, "review_overdue": review_overdue, "needs_refresh": bool(reasons), "reasons": reasons}


def is_fresh_thesis(t, today: Optional[date] = None, max_age_days: int = 30) -> bool:
    """Used by the queue to skip names that were researched recently: version created within max_age_days AND next_review not passed."""
    today = today or date.today()
    c = _d(t.created_at)
    if c is None or (today - c).days > max_age_days: return False
    nr = _d(t.next_review)
    return not (nr and nr < today)


def _pct(old, new) -> Optional[float]:
    try:
        if old in (None, 0) or new is None: return None
        return round((float(new) / float(old) - 1) * 100, 1)
    except (TypeError, ValueError): return None


def what_changed_since(thesis, current: dict, today: Optional[date] = None) -> dict:
    """Compare a stored thesis version with current data. Never fetches anything. Returns {'changes': [...], 'material': bool, 'severity': 'none|low|medium|high', ...}.
    Only reports differences it can SEE in the supplied data; missing current data is reported as 'not checked', not as 'no change'."""
    today = today or date.today()
    changes, checked, not_checked, sev = [], [], [], 0
    def add(level, text): nonlocal sev; sev = max(sev, level); changes.append(text)

    # price
    cp = current.get("price")
    if cp is not None and thesis.price:
        checked.append("price")
        mv = _pct(thesis.price, cp)
        if mv is not None and abs(mv) >= PRICE_MOVE_MATERIAL_PCT: add(2, f"price {mv:+.1f}% since v{thesis.version} ({thesis.price} -> {cp} {current.get('currency') or thesis.currency}, price date {current.get('price_ts') or 'unknown'})")
        elif mv is not None: changes.append(f"price {mv:+.1f}% since v{thesis.version} (within normal range)")
        if current.get("currency") and thesis.currency and current["currency"] != thesis.currency: add(3, f"currency mismatch: thesis {thesis.currency} vs current {current['currency']}; compare nothing until resolved")
    else: not_checked.append("price")
    pf = price_freshness(current.get("price_ts"), today)
    if cp is not None and pf["freshness"] in ("stale", "unknown"): add(1, f"current price is {pf['freshness']} (price_ts {pf['price_ts'] or 'missing'})")

    # valuation
    cv = current.get("valuation") or {}
    if cv and thesis.valuation:
        checked.append("valuation")
        for k, new in cv.items():
            old = thesis.valuation.get(k)
            mv = _pct(old, new) if isinstance(old, (int, float)) and isinstance(new, (int, float)) else None
            if mv is not None and abs(mv) >= VALUATION_MOVE_MATERIAL_PCT: add(2, f"valuation {k} {mv:+.1f}% ({old} -> {new})")
    else: not_checked.append("valuation")

    # new evidence / events dated after the thesis' as_of (or created_at date)
    since = _d(thesis.as_of) or _d(thesis.created_at)
    have = {e.id for e in thesis.evidence}
    new_ev = [e for e in current.get("evidence", []) if e.get("id") not in have and (_d(e.get("source_date")) is None or since is None or _d(e.get("source_date")) > since)]
    if "evidence" in current: checked.append("evidence")
    else: not_checked.append("evidence")
    for e in new_ev:
        kind = e.get("kind", "?")
        add(2 if kind == "FACT" and e.get("source_type") in ("filing", "exchange", "call") else 1, f"new {kind} evidence {e.get('id', '?')} ({e.get('source_type', '?')}, {e.get('source_date', 'undated')}): {str(e.get('claim', ''))[:100]}")
    ev_events = [x for x in current.get("events", []) if (_d(x.get("date")) is None or since is None or _d(x.get("date")) > since)]
    if "events" in current: checked.append("events")
    else: not_checked.append("events")
    for x in ev_events:
        add(3 if x.get("type") == "corporate_action" else 2 if x.get("type") in ("results", "guidance", "filing", "8-K") else 1, f"event {x.get('date', 'undated')} [{x.get('type', 'other')}]: {str(x.get('summary', ''))[:120]}")

    # catalyst windows / review dates that have passed without a recorded outcome
    nr = _d(thesis.next_review)
    if nr and nr < today: add(1, f"next_review {thesis.next_review} has passed")
    for c in thesis.catalysts:
        if c.status == "pending" and c.window: changes.append(f"catalyst still pending, check window: {c.window}")

    # staleness of the thesis' own evidence today
    tf = thesis_freshness(thesis, today)
    if tf["fact_counts"]["stale"]: add(1, f"{tf['fact_counts']['stale']} FACT(s) in v{thesis.version} are now stale")

    severity = ["none", "low", "medium", "high"][sev]
    return {"ticker": thesis.ticker, "market": thesis.market, "since_version": thesis.version, "compared_on": today.isoformat(), "changes": changes,
            "checked": checked, "not_checked": not_checked, "material": sev >= 2, "severity": severity}


def changes_since_version(market: str, ticker: str, version: int, current: dict, base=None, today: Optional[date] = None) -> dict:
    """Loads thesis version N from the store and compares it with current data."""
    from . import store
    t = store.load(market, ticker, version, base=base)
    if t is None: raise LookupError(f"no thesis {market}/{ticker} v{version}")
    return what_changed_since(t, current, today)


if __name__ == "__main__":   # python -m mblab.freshness MARKET TICKER VERSION current.json
    import json, sys
    m, tk, v, f = sys.argv[1:5]
    print(json.dumps(changes_since_version(m, tk, int(v), json.load(open(f))), indent=1))
