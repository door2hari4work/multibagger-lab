"""Research task queue: build and prioritise tasks from research/candidates_*.json, hand out the next tasks, mark them done, append to research/log.md.

State lives in research/queue.json (committed; git history is the audit trail). No network, no LLM.

CLI (run from the repo root; see research/PLAYBOOK.md):
    python research/queue.py build [--cap 5] [--fresh-days 30]     # add new tasks from candidates_*.json (skips names with a fresh thesis)
    python research/queue.py next  [-n 3] [--types level3_deep_dive,devils_advocate]
    python research/queue.py start|done|blocked|failed TASK_ID [--note "..."]
    python research/queue.py log   TASK_ID --summary "..."       # appends to research/log.md
    python research/queue.py show

candidates_*.json is owned by the discovery agent. Accepted shapes: a list of rows, or {"as_of":..., "candidates"|"rows"|"results": [rows]}.
Each row needs ticker|symbol and market; ordering uses `rank` (lower is better) if present, else `score`|`discovery_score`|`overall_score` (higher is better), else file order.
"""
import sys
from pathlib import Path
if __name__ == "__main__":
    # `queue` is a stdlib module name; running this file as a script puts research/ first on sys.path and would shadow it for other imports.
    sys.path[:] = [p for p in sys.path if Path(p or ".").resolve() != Path(__file__).resolve().parent]
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
import json
from datetime import date, timedelta
from typing import Optional

from mblab import store
from mblab.freshness import is_fresh_thesis

RESEARCH_DIR = Path(__file__).resolve().parent
QUEUE_PATH = RESEARCH_DIR / "queue.json"
LOG_PATH = RESEARCH_DIR / "log.md"

TASK_TYPES = ("level2_qualifier", "level3_deep_dive", "devils_advocate", "source_reliability", "ai_value_chain_mapper", "monitoring", "weekly_digest")
OPEN = ("pending", "in_progress")
DEFAULT_CAP = 5
DEFAULT_FRESH_DAYS = 30
COOLDOWN_DAYS = 3          # do not re-queue the same (type, ticker) within this many days of a done/blocked/failed attempt
STALE_IN_PROGRESS_DAYS = 2  # a session that died leaves in_progress behind; such tasks are re-opened after this long


# ------------------------------------------------------------------ io
def load_queue(path: Path = QUEUE_PATH) -> dict:
    if not Path(path).exists(): return {"version": 1, "tasks": []}
    return json.loads(Path(path).read_text())


def save_queue(q: dict, path: Path = QUEUE_PATH) -> None:
    Path(path).write_text(json.dumps(q, indent=1, ensure_ascii=False) + "\n")


def _rows(doc) -> list:
    if isinstance(doc, list): return doc
    for k in ("candidates", "rows", "results"):
        if isinstance(doc.get(k), list): return doc[k]
    return []


def _num(x) -> Optional[float]:
    try: return None if x in (None, "") else float(x)
    except (TypeError, ValueError): return None


def load_candidates(research_dir: Path = RESEARCH_DIR) -> list:
    """All rows from candidates_*.json, ordered best-first within each file, with priority 100 (top of a file) .. >0 (bottom). Malformed files are skipped."""
    out = []
    for f in sorted(Path(research_dir).glob("candidates_*.json")):
        try: rows = [r for r in _rows(json.loads(f.read_text())) if isinstance(r, dict)]
        except (OSError, ValueError): continue
        rows = [r for r in rows if (r.get("ticker") or r.get("symbol")) and r.get("market")]
        if any(_num(r.get("rank")) is not None for r in rows): rows.sort(key=lambda r: (_num(r.get("rank")) is None, _num(r.get("rank")) or 0))
        else:
            sc = lambda r: _num(r.get("score", r.get("discovery_score", r.get("overall_score"))))
            if any(sc(r) is not None for r in rows): rows.sort(key=lambda r: (sc(r) is None, -(sc(r) or 0)))
        n = len(rows)
        for i, r in enumerate(rows):
            out.append({**r, "ticker": str(r.get("ticker") or r.get("symbol")).upper(), "market": str(r["market"]).upper(), "_file": f.name, "priority": round(100 * (1 - i / n), 2)})
    return out


# ------------------------------------------------------------------ deciding what a name needs next
def decide_task(thesis, today: date, fresh_days: int = DEFAULT_FRESH_DAYS) -> tuple:
    """Returns (task_type | None, mode, reason). mode is 'new' or 'refresh'.
    Level 1 snapshots and level 2 theses always advance (the snapshot's own next_review is not 'freshness'); finished theses are skipped while fresh."""
    if thesis is None: return "level2_qualifier", "new", "no thesis yet"
    if thesis.status in ("rejected", "thesis_broken", "exit"): return None, "", f"status {thesis.status}"
    if thesis.research_level <= 1: return "level2_qualifier", "new", "level-1 snapshot only"
    if thesis.research_level == 2: return "level3_deep_dive", "new", "qualified at level 2"
    if not thesis.adversarial.done: return "devils_advocate", "new", "no adversarial review yet"
    if is_fresh_thesis(thesis, today, fresh_days): return None, "", f"fresh thesis v{thesis.version} (created {thesis.created_at[:10]}, review {thesis.next_review or 'unset'})"
    return "level3_deep_dive", "refresh", f"thesis v{thesis.version} is stale or review is due"


def _key(t: dict) -> tuple: return (t["type"], t["market"], t["ticker"])


def build_queue(candidates: list, queue: dict, today: Optional[date] = None, cap: int = DEFAULT_CAP, fresh_days: int = DEFAULT_FRESH_DAYS,
                theses_base: Optional[Path] = None) -> dict:
    """Adds at most `cap` new tasks (best candidates first). Mutates and returns the queue; adds queue['last_build'] with what was skipped and why."""
    today = today or date.today()
    reopen_stale(queue, today)
    open_keys = {_key(t) for t in queue["tasks"] if t["status"] in OPEN}
    recent = {}
    for t in queue["tasks"]:
        if t["status"] in ("done", "blocked", "failed") and t.get("finished_at"):
            recent[_key(t)] = max(recent.get(_key(t), ""), t["finished_at"])
    added, skipped = [], []
    for c in sorted(candidates, key=lambda c: -c["priority"]):
        if len(added) >= cap: break
        th = store.load(c["market"], c["ticker"], base=theses_base)
        typ, mode, why = decide_task(th, today, fresh_days)
        if typ is None: skipped.append({"ticker": c["ticker"], "market": c["market"], "reason": why}); continue
        key = (typ, c["market"], c["ticker"])
        if key in open_keys: skipped.append({"ticker": c["ticker"], "market": c["market"], "reason": f"{typ} already open"}); continue
        last = recent.get(key)
        if last and (today - date.fromisoformat(last[:10])).days < COOLDOWN_DAYS: skipped.append({"ticker": c["ticker"], "market": c["market"], "reason": f"{typ} attempted {last[:10]}, cooling down"}); continue
        task = {"id": f"{typ}:{c['market']}:{c['ticker']}:{today.isoformat()}", "type": typ, "mode": mode, "ticker": c["ticker"], "market": c["market"],
                "company": str(c.get("company") or c.get("name") or c["ticker"]), "priority": c["priority"], "status": "pending", "reason": why,
                "source": c["_file"], "created_at": today.isoformat(), "started_at": "", "finished_at": "", "note": ""}
        queue["tasks"].append(task); open_keys.add(key); added.append(task["id"])
    queue["last_build"] = {"date": today.isoformat(), "added": added, "skipped": skipped[:50], "cap": cap}
    return queue


def reopen_stale(queue: dict, today: date) -> list:
    out = []
    for t in queue["tasks"]:
        if t["status"] == "in_progress" and t.get("started_at") and (today - date.fromisoformat(t["started_at"][:10])).days >= STALE_IN_PROGRESS_DAYS:
            t["status"], t["note"] = "pending", (t.get("note", "") + " [re-opened: previous session did not finish]").strip(); out.append(t["id"])
    return out


def next_tasks(queue: dict, n: int = 3, types: Optional[list] = None) -> list:
    """Highest-priority pending tasks. Adversarial reviews go before new deep dives at equal priority (finish what is half-researched)."""
    order = {"devils_advocate": 0, "level3_deep_dive": 1, "level2_qualifier": 2}
    pend = [t for t in queue["tasks"] if t["status"] == "pending" and (not types or t["type"] in types)]
    return sorted(pend, key=lambda t: (-t["priority"], order.get(t["type"], 9), t["id"]))[:n]


def mark(queue: dict, task_id: str, status: str, note: str = "", today: Optional[date] = None) -> dict:
    if status not in ("in_progress", "done", "blocked", "failed", "pending"): raise ValueError(f"bad status {status}")
    today = today or date.today()
    for t in queue["tasks"]:
        if t["id"] == task_id:
            t["status"] = status
            if note: t["note"] = note
            if status == "in_progress": t["started_at"] = today.isoformat()
            if status in ("done", "blocked", "failed"): t["finished_at"] = today.isoformat()
            return t
    raise KeyError(task_id)


def mark_done(queue: dict, task_id: str, note: str = "", today: Optional[date] = None) -> dict:
    return mark(queue, task_id, "done", note, today)


def append_log(task: dict, summary: str, outcome: str = "done", sources: str = "", thesis_version: Optional[int] = None, log_path: Path = LOG_PATH, today: Optional[date] = None) -> None:
    today = today or date.today()
    line = (f"\n## {today.isoformat()} | {task['type']} | {task['market']}/{task['ticker']} | {outcome}\n"
            f"- task: {task['id']}\n" + (f"- thesis version saved: v{thesis_version}\n" if thesis_version else "- thesis version saved: none\n") +
            (f"- sources used: {sources}\n" if sources else "") + f"- summary: {summary}\n")
    p = Path(log_path)
    if not p.exists(): p.write_text("# Research log\nAppend-only. One entry per task attempt, including blocked/failed ones.\n")
    with p.open("a") as f: f.write(line)


# ------------------------------------------------------------------ cli
def _main(argv: list) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build", "next", "start", "done", "blocked", "failed", "log", "show"])
    ap.add_argument("task_id", nargs="?")
    ap.add_argument("--cap", type=int, default=DEFAULT_CAP); ap.add_argument("--fresh-days", type=int, default=DEFAULT_FRESH_DAYS)
    ap.add_argument("-n", type=int, default=3); ap.add_argument("--types", default="")
    ap.add_argument("--note", default=""); ap.add_argument("--summary", default=""); ap.add_argument("--sources", default=""); ap.add_argument("--version", type=int)
    a = ap.parse_args(argv)
    q = load_queue()
    if a.cmd == "build":
        build_queue(load_candidates(), q, cap=a.cap, fresh_days=a.fresh_days); save_queue(q)
        lb = q["last_build"]; print(f"added {len(lb['added'])}: {lb['added']}"); [print(f"  skipped {s['market']}/{s['ticker']}: {s['reason']}") for s in lb["skipped"][:10]]
    elif a.cmd == "next":
        print(json.dumps(next_tasks(q, a.n, [x for x in a.types.split(",") if x] or None), indent=1))
    elif a.cmd == "show":
        for t in q["tasks"]: print(f"{t['status']:<12}{t['priority']:>6}  {t['id']}  {t.get('note', '')[:60]}")
    elif a.cmd == "log":
        t = next(x for x in q["tasks"] if x["id"] == a.task_id); append_log(t, a.summary, t["status"], a.sources, a.version); print("logged")
    else:
        mark(q, a.task_id, {"start": "in_progress"}.get(a.cmd, a.cmd), a.note); save_queue(q); print(f"{a.task_id} -> {a.cmd}")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
