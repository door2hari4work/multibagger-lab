"""Writes ui/out/today.html (and one page per thesis in ui/out/opportunity/) from the real store (theses/), falling back to synthetic fixtures when empty.
Usage: python -m ui.build [--fixtures] [--out DIR]"""
from __future__ import annotations
import argparse
import re
from datetime import date
from pathlib import Path
from typing import Optional

from mblab import store
from mblab.schema import Thesis
from .today import build_today
from .opportunity import build_opportunity

OUT = Path(__file__).resolve().parent / "out"
PAPER_STATUS = store.ROOT / "paper" / "STATUS.md"


def _num(s: str):
    s = s.replace(",", "").replace("%", "").strip()
    try: return float(s)
    except ValueError: return None


def paper_status_from_md(path: Path = PAPER_STATUS) -> Optional[dict]:
    """Parse the markdown table written by paper/paper_trade.py. Returns None when the file is missing or has no rows."""
    if not path.exists(): return None
    rows, head = [], None
    for ln in path.read_text().splitlines():
        if not ln.startswith("|"): continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if head is None: head = [c.lower() for c in cells]; continue
        if set("".join(cells)) <= set("-: "): continue
        d = dict(zip(head, cells))
        dd = _num(d.get("drawdown now", ""))
        rows.append({"name": d.get("book", "?"), "started": d.get("started", ""), "regime": d.get("regime", ""), "nav": _num(d.get("nav (rs)", "")) or d.get("nav (rs)"),
                     "benchmark": _num(d.get("benchmark (rs)", "")) or d.get("benchmark (rs)"), "drawdown": None if dd is None else dd / 100, "flags": d.get("flags", "")})
    first = path.read_text().splitlines()[0].lstrip("# ").strip() if path.stat().st_size else ""
    return {"books": rows, "note": first} if rows else None


def portfolio_summary_from_private() -> Optional[dict]:
    """Aggregate-only portfolio summary from the gitignored private/ analytics. Percentages only: no holding names, no rupee values."""
    import json
    f = store.ROOT / "private" / "portfolio_analytics.json"
    if not f.exists(): return None
    try: a = json.loads(f.read_text())
    except Exception: return None
    if a.get("empty"): return None
    notes = []
    th = a.get("by_theme", {})
    for k, label in (("ai", "AI-related"), ("semiconductors", "Semiconductor")):
        if k in th:
            v = th[k]; notes.append(f"{label} exposure: about {v['direct_pct']:.0f}% direct, {v['estimated_pct']:.0f}% estimated including funds ({v['multiple_of_direct']:.1f}x direct; fund look-through is partial).")
    c = a.get("by_country", {})
    if c: notes.append("Geography: " + ", ".join(f"{k} {v:.0f}%" for k, v in sorted(c.items(), key=lambda kv: -kv[1])[:3]) + ".")
    sec = a.get("by_sector", {})
    if sec:
        k, v = max(sec.items(), key=lambda kv: kv[1]); notes.append(f"Largest sector: {k} at {v:.0f}%.")
    notes.append(f"Largest single position: {a.get('concentration', {}).get('top1_pct', 0):.0f}% of the portfolio; top 3 = {a.get('concentration', {}).get('top3_pct', 0):.0f}%.")
    lt = a.get("look_through_quality", {}).get("label")
    if lt: notes.append(f"Look-through quality: {lt}.")
    return {"currency": "", "value": None, "n_holdings": a.get("n_holdings"), "cash_pct": None, "notes": notes, "as_of": date.today().isoformat()}


def discoveries_from_candidates(theses: list, limit: int = 10) -> list:
    """Candidates from the latest discovery run that do not have a thesis yet (anything with a Level-1 snapshot is already a ranked card)."""
    import json
    have = {(t.market.upper(), t.ticker.upper().replace(".NS", "")) for t in theses}
    out = []
    for m in ("IN", "US"):
        f = store.ROOT / "research" / f"candidates_{m}.json"
        if not f.exists(): continue
        d = json.loads(f.read_text()); rows = d if isinstance(d, list) else (d.get("candidates") or d.get("rows") or d.get("results") or [])
        for r in rows:
            tk = str(r.get("ticker", "")).upper().replace(".NS", "")
            if (m, tk) in have: continue
            out.append({"ticker": r.get("ticker"), "market": m, "name": r.get("name"), "score": None,
                        "note": f"Momentum rank {r.get('rank')} in the {m} mid/small-cap screen (12-1 month return {r.get('mom_12_1', 0):+.0%}). Discovery screen only: no business research yet."})
            if len(out) >= limit * 2: break
    return out[:limit]


def _attach_private_fit(theses: list) -> None:
    """In-memory only: sets t.portfolio_fit from private/portfolio_analytics.json. Nothing here is written to theses/."""
    import json
    from mblab.integrate import candidate_row
    from mblab.portfolio import fit_score
    f = store.ROOT / "private" / "portfolio_analytics.json"
    if not f.exists(): return
    try: a = json.loads(f.read_text())
    except Exception: return
    for t in theses:
        c = candidate_row(t.market, t.ticker) or {}
        t.portfolio_fit = fit_score({"ticker": t.ticker, "name": t.company, "sector": c.get("sector"), "market": t.market,
                                     "market_cap_bucket": "mid" if c.get("segment") == "mid" else "small"}, a)


def link_for(t: Thesis) -> str:
    return f"opportunity/{t.market.upper()}_{re.sub(r'[^A-Za-z0-9_.-]', '_', t.ticker.upper())}.html"


def build(out_dir: Path = OUT, force_fixtures: bool = False, as_of: Optional[str] = None) -> Path:
    theses = [] if force_fixtures else store.latest_all()
    sample = not theses
    if sample:
        from .fixtures import sample_data as fx
        theses, alerts, cands = fx.sample_theses(), fx.sample_alerts(), fx.sample_candidates()
        pf, ps, as_of = fx.sample_portfolio_summary(), fx.sample_paper_status(), as_of or fx.SAMPLE_AS_OF
    else:
        alerts, cands, pf, ps, as_of = [], discoveries_from_candidates(theses), portfolio_summary_from_private(), paper_status_from_md(), as_of or date.today().isoformat()
    if not sample:   # portfolio fit is computed at display time from the private analytics and is never saved into theses/ (public repo)
        _attach_private_fit(theses)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "opportunity").mkdir(exist_ok=True)
    for t in theses:
        hist = [] if sample else [h for h in (store.load(t.market, t.ticker, v) for v in store.versions(t.market, t.ticker)) if h]
        (out_dir / link_for(t)).write_text(build_opportunity(t, history=hist, sample=sample), encoding="utf-8")
    p = out_dir / "today.html"
    p.write_text(build_today(theses, alerts, cands, pf, ps, as_of, sample=sample, opportunity_href=link_for), encoding="utf-8")
    return p


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fixtures", action="store_true", help="use synthetic sample data even if theses exist")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    print(build(Path(a.out), a.fixtures))
