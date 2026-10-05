"""Thesis monitor: turns (thesis, fresh snapshot) into a short list of MATERIAL alerts, then de-duplicates against an alert log.

What it checks (each only when the data is there; a missing input never raises or fabricates an alert):
  entry zone entered | entry state improved / deteriorated | technical invalidation breached | numeric exit triggers |
  catalyst window passed with no status update | evidence going stale (> 120 days) | valuation excess vs the thesis | base-case target reached.
Alerts carry severity, a reason, and a de-dup key. filter_new() applies per-severity cooldowns so the user is not spammed:
the same key is re-sent only after its cooldown, or immediately if its severity ESCALATES. Nothing here trades or edits a thesis.
"""
from __future__ import annotations
import json
import re
from dataclasses import dataclass, field, asdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd

from . import timing
from .schema import Thesis, EvidenceKind, Status

SEVERITIES = ["info", "low", "medium", "high", "critical"]
SEV_RANK = {s: i for i, s in enumerate(SEVERITIES)}
COOLDOWN_DAYS = {"info": 14, "low": 14, "medium": 7, "high": 3, "critical": 1}
MAX_EVIDENCE_AGE_DAYS = 120
VALUATION_KEYS = ("pe", "ev", "ps", "pb", "p_e", "p_s", "p_b")
VAL_WARN, VAL_HIGH = 1.5, 2.0       # current multiple / thesis-time multiple
CATALYST_GRACE_DAYS = 7


@dataclass
class Snapshot:
    """What the monitor knows today. All fields optional except as_of."""
    as_of: str                                   # ISO date of the data
    ohlcv: Optional[pd.DataFrame] = None         # daily Close (High/Low/Volume optional), oldest first, ONE stock
    regime_on: bool = True
    price: Optional[float] = None                # overrides the last close if given
    fundamentals: dict = field(default_factory=dict)   # latest numbers, e.g. {"pe_ttm": 41.0, "ebitda_margin": 0.14, "revenue_growth_yoy": 0.22}
    fundamentals_date: str = ""
    entry_price: Optional[float] = None          # the user's actual entry, for drawdown_from_entry triggers
    catalyst_dates: dict = field(default_factory=dict)  # {catalyst description: ISO date its window ends}; overrides parsing Catalyst.window


@dataclass
class Alert:
    ticker: str
    market: str
    kind: str
    severity: str
    reason: str
    key: str                                     # de-dup key: same key = same underlying situation
    as_of: str = ""
    data: dict = field(default_factory=dict)

    def to_dict(self) -> dict: return asdict(self)


# ----------------------------------------------------------------------------------------------------------------------------
def _d(x) -> Optional[date]:
    if isinstance(x, datetime): return x.date()
    if isinstance(x, date): return x
    try: return date.fromisoformat(str(x)[:10])
    except (ValueError, TypeError): return None


_MONTHS = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}


def parse_window(window: str) -> Optional[date]:
    """End of a catalyst window from free text: ISO date, or 'Mon YYYY' (-> last day of that month). None if it cannot be read."""
    if not window: return None
    m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", window)
    if m: return _d(m.group(1))
    m = re.search(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*,?\s*(20\d{2})\b", window, re.I)
    if m:
        y, mo = int(m.group(2)), _MONTHS[m.group(1).lower()]
        return (date(y + (mo == 12), mo % 12 + 1, 1) - timedelta(days=1))
    return None


def _in_zone(p: Optional[float], z) -> bool:
    return p is not None and z is not None and len(z) == 2 and z[0] is not None and z[1] is not None and z[0] <= p <= z[1]


_COND = re.compile(r"^\s*([a-z_][a-z0-9_]*)\s*(<=|>=|<|>|below|above)\s*(-?\d+(?:\.\d+)?)\s*(%?)", re.I)


def parse_condition(cond: str):
    """'price < 120', 'close below 120', 'ebitda_margin < 12%', 'drawdown_from_entry < -30%' -> (metric, op, value) or None for non-numeric text."""
    m = _COND.match(cond or "")
    if not m: return None
    metric, op, num, pct = m.group(1).lower(), m.group(2).lower(), float(m.group(3)), m.group(4)
    op = {"below": "<", "above": ">"}.get(op, op)
    return metric, op, (num / 100.0 if pct else num)


def _cmp(a: float, op: str, b: float) -> bool:
    return {"<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]


def _latest_fact_date(t: Thesis) -> Optional[date]:
    ds = [_d(e.source_date) for e in t.evidence if e.kind == EvidenceKind.FACT.value and e.source_date]
    ds = [x for x in ds if x]
    return max(ds) if ds else None


def _key(t: Thesis, kind: str, disc: str = "") -> str:
    return f"{t.market.upper()}:{t.ticker.upper()}:{kind}" + (f":{disc}" if disc else "")


# ----------------------------------------------------------------------------------------------------------------------------
def evaluate(thesis: Thesis, snapshot: Snapshot) -> list:
    """Returns alerts ordered by severity (highest first). Not yet de-duplicated: pass through filter_new() with the alert log."""
    t, s = thesis, snapshot
    today = _d(s.as_of)
    if today is None: raise ValueError("snapshot.as_of must be an ISO date")
    out: list = []
    mk = lambda kind, sev, reason, disc="", **data: out.append(Alert(t.ticker, t.market, kind, sev, reason, _key(t, kind, disc), str(today), data))
    live = t.status not in (Status.REJECTED.value, Status.THESIS_BROKEN.value, Status.EXIT.value)
    holding = t.status in (Status.ACCUMULATE.value, Status.HOLD.value, Status.TRIM.value)

    price, prev, df = s.price, None, s.ohlcv
    if df is not None and len(df):
        cl = df[[c for c in df.columns if str(c).lower() == "close"][0]].dropna() if any(str(c).lower() == "close" for c in df.columns) else None
        if cl is not None and len(cl):
            if price is None: price = float(cl.iloc[-1])
            if len(cl) >= 2: prev = float(cl.iloc[-2])
    e = t.entry

    # 1. technical invalidation breached
    if live and price is not None and e.invalidation_price is not None and price < e.invalidation_price:
        mk("invalidation_breached", "critical", f"Price {price:g} is below the invalidation level {e.invalidation_price:g}. Review the thesis now; this is the stated point where the setup no longer holds.", f"{e.invalidation_price:g}", price=price, level=e.invalidation_price)

    # 2. entry zone entered (transition into the zone; if no prior close is known, report being inside)
    if live and price is not None and not holding:
        for name, z in (("ideal", e.ideal_zone), ("acceptable", e.acceptable_zone)):
            if _in_zone(price, z):
                if prev is not None and _in_zone(prev, z): break    # already inside yesterday: not news
                if name == "acceptable" and _in_zone(price, e.ideal_zone): break
                mk("entry_zone_entered", "medium" if name == "acceptable" else "high", f"Price {price:g} entered the {name} entry zone {z[0]:g}-{z[1]:g}. Whether to act still depends on the thesis gates (research level, adversarial review, fresh evidence).", f"{name}:{z[0]:g}-{z[1]:g}", price=price, zone=z)
                break

    # 3. entry state improved / deteriorated (re-assess from the price history)
    new_state, assessment = None, None
    if df is not None and len(df) >= timing.TH["min_rows"]:
        thesis_ok = live and not any(x.status == "triggered" for x in t.exit_rules)
        assessment = timing.assess(df, regime_on=s.regime_on, thesis_ok=thesis_ok)
        new_state = assessment.state
    old_state = e.state
    if live and new_state and old_state in timing.ENTRY_RANK and new_state != old_state and old_state != "unknown" and new_state != "unknown":
        ro, rn = timing.ENTRY_RANK[old_state], timing.ENTRY_RANK[new_state]
        if rn > ro:
            sev = "high" if new_state in timing.ACTIONABLE else "low"
            mk("entry_state_improved", sev, f"Entry state improved: {old_state} -> {new_state}. {assessment.rationale.split('. ')[0]}.", f"{old_state}>{new_state}", old=old_state, new=new_state)
        else:
            sev = "high" if new_state == "thesis_deteriorating" else ("medium" if (old_state in timing.ACTIONABLE or holding) else "low")
            mk("entry_state_deteriorated", sev, f"Entry state deteriorated: {old_state} -> {new_state}. {assessment.rationale.split('. ')[0]}.", f"{old_state}>{new_state}", old=old_state, new=new_state)

    # 4. numeric exit triggers
    metrics = {k.lower(): v for k, v in (s.fundamentals or {}).items() if isinstance(v, (int, float))}
    if price is not None:
        metrics["price"] = metrics["close"] = price
        if s.entry_price: metrics["drawdown_from_entry"] = price / s.entry_price - 1
    if assessment is not None and assessment.metrics.get("dist_hi") is not None: metrics["drawdown_52w"] = assessment.metrics["dist_hi"]
    for x in t.exit_rules:
        if x.status == "triggered": continue                       # already known
        pc = parse_condition(x.condition)
        if not pc: continue                                         # non-numeric: needs human/agent judgement, not this monitor
        metric, op, val = pc
        if metric in metrics and _cmp(metrics[metric], op, val):
            sev = "critical" if x.type in ("thesis_invalidation", "earnings_deterioration", "catalyst_failure") else "high"
            mk("exit_trigger_met", sev, f"Exit trigger ({x.type}) condition met: '{x.condition.strip()}' (current {metric} = {metrics[metric]:.4g}).", re.sub(r"\W+", "_", x.condition.strip().lower())[:60], type=x.type, metric=metric, value=metrics[metric])

    # 5. catalyst window passed without a status update
    for c in t.catalysts:
        if c.status != "pending": continue
        end = _d(s.catalyst_dates.get(c.description)) if s.catalyst_dates.get(c.description) else parse_window(c.window)
        if end and today > end + timedelta(days=CATALYST_GRACE_DAYS):
            mk("catalyst_overdue", "medium" if live else "low", f"Catalyst window '{c.window or c.description}' ended {end.isoformat()} ({(today - end).days} days ago) but the catalyst is still marked pending. Update it as occurred / failed / delayed.", re.sub(r"\W+", "_", c.description.lower())[:40], catalyst=c.description, window_end=str(end))

    # 6. evidence going stale
    if live and t.status not in (Status.EARLY_DISCOVERY.value,):
        lf = _latest_fact_date(t)
        if lf is None: mk("evidence_stale", "medium", "The thesis has no dated FACT evidence, so nothing supports its current status.", "no_fact")
        elif (today - lf).days > MAX_EVIDENCE_AGE_DAYS:
            mk("evidence_stale", "high" if (holding or t.status == Status.PREPARING_TO_ENTER.value) else "medium",
               f"Newest FACT is {(today - lf).days} days old ({lf.isoformat()}), beyond the {MAX_EVIDENCE_AGE_DAYS}-day limit. Entry/accumulate calls need fresher evidence.", "age>120", newest_fact=str(lf), age_days=(today - lf).days)

    # 7. valuation excess vs the thesis
    if live:
        for k, v0 in (t.valuation or {}).items():
            kl = k.lower()
            if not any(kl.startswith(p) for p in VALUATION_KEYS) or not isinstance(v0, (int, float)) or v0 <= 0: continue
            v1 = metrics.get(kl)
            if v1 is None or v1 <= 0: continue
            r = v1 / v0
            if r >= VAL_WARN:
                mk("valuation_excess", "high" if r >= VAL_HIGH else "medium", f"{k} is {v1:.3g} now versus {v0:.3g} when the thesis was written ({r:.1f}x). The expectations gap the thesis relied on may have closed.", f"{kl}:{int(r * 2) / 2:.1f}x", metric=k, thesis_value=v0, now=v1, ratio=round(r, 2))
        if t.price and t.base_case and t.base_case.multiple_high and price is not None and price >= t.price * t.base_case.multiple_high:
            mk("target_reached", "medium", f"Price {price:g} has reached the thesis base-case upper multiple ({t.base_case.multiple_high:g}x from {t.price:g}). Revisit trim / hold criteria.", "base_high", price=price)

    out.sort(key=lambda a: -SEV_RANK[a.severity])
    return out


# ----------------------------------------------------------------------------------------------------------------------------
# De-duplication against an alert log: [{"key", "severity", "ts"}]. The log is plain data; load/save helpers take an explicit path.
def filter_new(alerts: list, log: list, today, cooldown_days: Optional[dict] = None) -> tuple:
    """Returns (fresh, suppressed). An alert is suppressed if the same key was sent within its severity's cooldown
    AND the severity has not escalated since. Duplicates within `alerts` itself are collapsed (highest severity kept)."""
    cd = {**COOLDOWN_DAYS, **(cooldown_days or {})}
    td = _d(today)
    last: dict = {}
    for r in log:
        ts = _d(r.get("ts"))
        if ts is None: continue
        k = r["key"]
        if k not in last or ts > last[k][0] or (ts == last[k][0] and SEV_RANK[r["severity"]] > SEV_RANK[last[k][1]]): last[k] = (ts, r["severity"])
    best: dict = {}
    for a in alerts:
        if a.key not in best or SEV_RANK[a.severity] > SEV_RANK[best[a.key].severity]: best[a.key] = a
    fresh, suppressed = [], []
    for a in sorted(best.values(), key=lambda a: -SEV_RANK[a.severity]):
        prev = last.get(a.key)
        if prev is None: fresh.append(a); continue
        ts, sev = prev
        if SEV_RANK[a.severity] > SEV_RANK[sev] or (td - ts).days >= cd[a.severity]: fresh.append(a)
        else: suppressed.append(a)
    suppressed += [a for a in alerts if a.key in best and a is not best[a.key]]
    return fresh, suppressed


def record(log: list, fresh: list, today) -> list:
    """Appends the alerts that were actually sent; returns a new list."""
    ts = str(_d(today))
    return list(log) + [dict(key=a.key, severity=a.severity, ts=ts, kind=a.kind) for a in fresh]


def load_log(path) -> list:
    p = Path(path)
    return json.loads(p.read_text()) if p.exists() else []


def save_log(path, log: list, keep_days: int = 400, today=None) -> None:
    td = _d(today) or date.today()
    kept = [r for r in log if (_d(r.get("ts")) or td) >= td - timedelta(days=keep_days)]
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(kept, indent=1) + "\n")
