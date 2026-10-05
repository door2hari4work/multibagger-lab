"""Append-only versioned thesis store: theses/<MARKET>/<TICKER>/v001.json, v002.json ... Git gives diffs; nothing is ever overwritten."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Optional
from .schema import Thesis, validate, now_iso

ROOT = Path(__file__).resolve().parent.parent
THESES = ROOT / "theses"


class ThesisInvalid(ValueError):
    pass


def _dir(market: str, ticker: str, base: Optional[Path] = None) -> Path:
    return (base or THESES) / market.upper() / ticker.upper().replace("/", "_")


def versions(market: str, ticker: str, base: Optional[Path] = None) -> list:
    d = _dir(market, ticker, base)
    return sorted(int(f.stem[1:]) for f in d.glob("v*.json")) if d.exists() else []


def load(market: str, ticker: str, version: Optional[int] = None, base: Optional[Path] = None) -> Optional[Thesis]:
    vs = versions(market, ticker, base)
    if not vs: return None
    v = version or vs[-1]
    return Thesis.from_dict(json.loads((_dir(market, ticker, base) / f"v{v:03d}.json").read_text()))


def _diff(old: Thesis, new: Thesis) -> list:
    out = []
    for f in ("status", "research_level", "confidence", "why_now", "thesis", "overall_score"):
        a, b = getattr(old, f), getattr(new, f)
        if a != b: out.append(f"{f}: {str(a)[:80]!r} -> {str(b)[:80]!r}")
    if old.entry.state != new.entry.state: out.append(f"entry state: {old.entry.state} -> {new.entry.state}")
    if old.adversarial.verdict != new.adversarial.verdict: out.append(f"adversarial verdict: {old.adversarial.verdict or 'none'} -> {new.adversarial.verdict or 'none'}")
    olde, newe = {e.id for e in old.evidence}, {e.id for e in new.evidence}
    if newe - olde: out.append(f"new evidence: {', '.join(sorted(newe - olde))}")
    if olde - newe: out.append(f"evidence removed: {', '.join(sorted(olde - newe))}")
    return out


def save_new_version(t: Thesis, reason: str = "", base: Optional[Path] = None, today=None) -> Thesis:
    """Validates, assigns the next version, records what changed vs the previous version, writes a NEW file. Raises ThesisInvalid on rule violations."""
    problems = validate(t, today=today)
    if problems: raise ThesisInvalid("; ".join(problems))
    prev = load(t.market, t.ticker, base=base)
    t.version = (prev.version + 1) if prev else 1
    t.parent_version = prev.version if prev else None
    t.created_at = now_iso()
    t.change_log = ([reason] if reason else []) + (_diff(prev, t) if prev else ["initial version"])
    d = _dir(t.market, t.ticker, base); d.mkdir(parents=True, exist_ok=True)
    (d / f"v{t.version:03d}.json").write_text(json.dumps(t.to_dict(), indent=1, ensure_ascii=False) + "\n")
    return t


def latest_all(base: Optional[Path] = None) -> list:
    out = []
    root = base or THESES
    for m in sorted(root.glob("*")):
        for tk in sorted(m.glob("*")):
            t = load(m.name, tk.name, base=base)
            if t: out.append(t)
    return out
