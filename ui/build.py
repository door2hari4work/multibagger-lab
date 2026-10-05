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
        alerts, cands, pf, ps, as_of = [], [], None, paper_status_from_md(), as_of or date.today().isoformat()
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
