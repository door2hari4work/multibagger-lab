"""Decision-first home screen: what deserves attention TODAY. build_today() returns one self-contained HTML string."""
from __future__ import annotations
from typing import Any, Callable, Optional

from mblab.schema import Thesis, DISCLAIMER
from ._common import (
    esc, slug, get, num, parse_date, days_between, money, mult, pct, short, page, theme_button, pill, status_pill, entry_pill, est, empty,
    score_bar, STATUS, ACTIVE_EXCLUDED, LATE_STAGE, REVIEW_STATUSES, GOOD_ENTRY, COMPONENTS, SEVERITY, HONESTY, LEVELS,
)

RECENT_DAYS = 7
MAX_CARDS = 6


# ---- classification (explainable rules, shown in the tile captions) ---------------------------------

def _recent(t: Thesis, as_of: str) -> bool:
    d = days_between(as_of, (t.created_at or "")[:10])
    return d is not None and 0 <= d <= RECENT_DAYS


def is_active(t: Thesis) -> bool:
    return t.status not in ACTIVE_EXCLUDED


def is_high_priority(t: Thesis) -> bool:
    if not is_active(t): return False
    if t.status in LATE_STAGE: return True
    # a high score alone never qualifies: it needs deep research, an adversarial review that SURVIVED, non-low confidence and a workable entry state
    return ((t.overall_score or 0) >= 0.70 and t.research_level >= 4 and t.adversarial.done and t.adversarial.verdict == "survives"
            and t.confidence in ("medium", "high") and t.entry.state not in ("overextended", "wait_for_pullback", "thesis_deteriorating", "too_early"))


def is_changed(t: Thesis, as_of: str) -> bool:
    return t.version > 1 and _recent(t, as_of)


def entry_improved(t: Thesis, as_of: str) -> bool:
    if not (t.version > 1 and _recent(t, as_of) and is_active(t)): return False
    moved = any(str(x).startswith("entry state:") and "unknown ->" not in str(x) for x in t.change_log)  # the first assessment is not an improvement
    return moved and (t.entry.state in GOOD_ENTRY or t.entry.state == "setup_forming")


def exit_triggered(t: Thesis) -> bool:
    return t.status in REVIEW_STATUSES or any(x.status == "triggered" for x in t.exit_rules)


def rank_key(t: Thesis):
    stage = 0 if t.status in LATE_STAGE else (1 if t.research_level >= 3 else 2)  # thin Level 1-2 scores never outrank researched ideas
    return (stage, -(t.overall_score or 0.0), t.ticker)


# ---- small renderers --------------------------------------------------------------------------------

def _link(t: Thesis, href: Optional[Callable[[Thesis], str]]) -> str:
    if not href: return ""
    u = href(t)
    return u if u and not u.lower().startswith(("javascript:", "data:", "vbscript:")) else ""


def _name(t: Thesis, href) -> str:
    u = _link(t, href)
    inner = esc(t.company or t.ticker)
    return f'<a href="{esc(u)}">{inner}</a>' if u else inner


def _zone(z, cur: str) -> str:
    if not z or len(z) != 2 or num(z[0]) is None or num(z[1]) is None: return ""
    return f"{money(z[0], cur)} to {money(z[1], cur)}"


def _scenario_line(s, label: str, fallback_h: Optional[int]) -> str:
    if not s or (num(s.multiple_low) is None and num(s.multiple_high) is None): return ""
    lo, hi = num(s.multiple_low), num(s.multiple_high)
    rng = mult(lo) if hi is None or lo == hi else (mult(hi) if lo is None else f"{mult(lo)} to {mult(hi)}")
    h = s.horizon_months or fallback_h
    p = f", probability about {pct(s.probability)}" if num(s.probability) is not None else ""
    return f"{label} {rng}{f' over {h} months' if h else ''}{p}"


def _upside(t: Thesis) -> str:
    parts = [_scenario_line(t.base_case, "Base", t.time_horizon_months), _scenario_line(t.bull_case, "Bull", t.time_horizon_months)]
    parts = [p for p in parts if p]
    if not parts:
        return '<span class="muted">No upside range yet. Needs research beyond Level 1.</span>'
    return f'{est()} ' + "<br>".join(esc(p) for p in parts)


def _downside(t: Thesis) -> str:
    return esc(_scenario_line(t.bear_case, "Bear", t.time_horizon_months)) if t.bear_case else ""


def _risk(t: Thesis) -> str:
    if not t.risks: return '<span class="muted">No risks recorded yet.</span>'
    more = f' <span class="muted">(+{len(t.risks) - 1} more)</span>' if len(t.risks) > 1 else ""
    return esc(short(t.risks[0], 130)) + more


def _fit(t: Thesis) -> str:
    pf = t.portfolio_fit
    if num(pf.score) is None and not pf.summary:
        return '<span class="muted">Not assessed. No portfolio loaded.</span>'
    sc = f"{num(pf.score):.2f}. " if num(pf.score) is not None else ""
    return esc(sc + short(pf.summary, 110))


def _score_block(t: Thesis) -> str:
    by = {c.name: c for c in t.scores}
    shown = [(k, lab) for k, lab in COMPONENTS if k in by and by[k].value is not None]
    if not shown:
        return empty("No score yet.", "Level 1 discovery only: no deep research yet." if t.research_level <= 1 else "Scores have not been assessed.")
    bars = "".join(score_bar(lab, by[k].value, by[k].data_quality, by[k].basis) for k, lab in shown)
    n_missing = len(COMPONENTS) - len(shown)
    ov = (f'<b>{t.overall_score:.2f}</b>' if num(t.overall_score) is not None else "<b>n/a</b>")
    return (f'<div class="overall"><span>Lab score {ov}</span><span class="muted">confidence {esc(t.confidence)}; {len(shown)} of {len(COMPONENTS)} parts assessed'
            f'{f", {n_missing} not assessed" if n_missing else ""}; weights are declared, not yet validated</span></div>'
            f'<ul class="bars" aria-label="Score parts">{bars}</ul>')


def _card(t: Thesis, rank: int, href) -> str:
    cur = t.currency
    price = f'<b>{esc(money(t.price, cur))}</b><span class="muted small">{esc("as of " + t.price_ts[:10]) if t.price_ts else "price date unknown"}</span>'
    zone = _zone(t.entry.ideal_zone, cur)
    entry_extra = f'<span class="small muted">Ideal zone {esc(zone)}</span>' if zone else ""
    why = short(t.why_now, 170) or "No why-now note yet."
    lvl = f"Level {t.research_level} of {len(LEVELS)}: {LEVELS[t.research_level - 1]}" if 1 <= t.research_level <= len(LEVELS) else "Level unknown"
    down = _downside(t)
    return f"""<li class="card" id="opp-{slug(t.market)}-{slug(t.ticker)}">
<div class="card-head"><span class="rank" aria-label="Rank {rank}">{rank}</span>
<div class="who stack" style="gap:6px"><h3>{_name(t, href)}</h3>
<div class="chips"><span class="tag mono">{esc(t.ticker)}</span><span class="tag">{esc(t.market)}</span>{status_pill(t.status)}{entry_pill(t.entry.state)}</div></div>
<div class="price">{price}</div></div>
<p class="why"><span class="eyebrow">Why now</span><br>{esc(why)}</p>
{_score_block(t)}
<div class="facts">
<div class="fact"><span class="k">Upside range and timeframe</span><span class="v">{_upside(t)}</span></div>
<div class="fact"><span class="k">Downside</span><span class="v">{down or '<span class="muted">Not estimated.</span>'}</span></div>
<div class="fact"><span class="k">Main risk</span><span class="v">{_risk(t)}</span></div>
<div class="fact"><span class="k">Portfolio fit</span><span class="v">{_fit(t)}</span></div>
<div class="fact"><span class="k">Entry</span><span class="v">{entry_pill(t.entry.state)} {entry_extra}</span></div>
<div class="fact"><span class="k">Research depth</span><span class="v">{esc(lvl)}</span></div>
</div></li>"""


def _alert_row(a: dict) -> str:
    sev = str(get(a, "severity", "info")).lower()
    order, label, tone = SEVERITY.get(sev, SEVERITY["info"])
    title = get(a, "title") or get(a, "message") or "Alert"
    tk = get(a, "ticker")
    detail = get(a, "detail") or ""
    ts = str(get(a, "ts") or get(a, "date") or "")[:10]
    meta = " · ".join(x for x in [esc(tk) if tk else "", esc(get(a, "kind") or ""), esc(ts)] if x)
    meta_html = '<span class="small muted">' + meta + "</span>" if meta else ""
    return (f'<li class="row s-{slug(tone)}">{pill(label, tone)}<div class="body"><span class="title">{esc(title)}</span>'
            f'{f"<span class=small>{esc(short(detail, 220))}</span>" if detail else ""}'
            f'{meta_html}</div></li>')


def _alerts(alerts: list, exit_theses: list, href) -> str:
    items = sorted([a for a in (alerts or []) if isinstance(a, dict)], key=lambda a: SEVERITY.get(str(get(a, "severity", "info")).lower(), SEVERITY["info"])[0])
    rows = "".join(_alert_row(a) for a in items)
    ex = ""
    for t in exit_theses:
        trig = [x for x in t.exit_rules if x.status == "triggered"]
        cond = "; ".join(short(x.condition, 120) for x in trig) or STATUS.get(t.status, ("", "", ""))[2]
        ex += (f'<li class="row s-crit">{pill("Exit check", "crit")}<div class="body"><span class="title">{_name(t, href)} '
               f'<span class="tag mono">{esc(t.ticker)}</span></span><span class="small">{esc(cond)}</span>'
               f'<span class="small muted">Status: {esc(STATUS.get(t.status, (t.status,))[0])}. Review the position yourself.</span></div></li>')
    if not rows and not ex:
        return empty("No alerts today.", "Alerts only appear when something material changes. Quiet days are normal.")
    return f'<ul class="list">{ex}{rows}</ul>'


def _fmt_money_or_text(v: Any, cur: str = "") -> str:
    f = num(v)
    return money(f, cur) if f is not None else (str(v) if v not in (None, "") else "n/a")


def _fmt_pct_or_text(v: Any) -> str:
    f = num(v)
    return f"{f * 100:.1f}%" if f is not None else (str(v) if v not in (None, "") else "n/a")


def _books(ps: Optional[dict]) -> str:
    books = (ps or {}).get("books") if isinstance(ps, dict) else None
    if not books:
        return empty("Paper books not connected.", "Run paper/paper_trade.py to produce a status. Nothing is being tracked in this view yet.")
    out = ""
    for b in books:
        nav, bm = num(get(b, "nav")), num(get(b, "benchmark"))
        rel = f"{(nav / bm - 1) * 100:+.1f}%" if nav is not None and bm not in (None, 0) else "n/a"
        regime = str(get(b, "regime", "")).upper()
        rt = {"ON": "good", "OFF": "warn"}.get(regime, "neutral")
        started = get(b, "started") or "not yet"
        flags = get(b, "flags") or ""
        cur = get(b, "currency") or ""
        out += (f'<li class="book"><span class="name"><span class="mono">{esc(get(b, "name", "book"))}</span>{pill("Regime " + (regime or "n/a"), rt)}</span>'
                f'<dl><dt>NAV</dt><dd>{esc(_fmt_money_or_text(get(b, "nav"), cur))}</dd><dt>Benchmark</dt><dd>{esc(_fmt_money_or_text(get(b, "benchmark"), cur))}</dd>'
                f'<dt>NAV vs benchmark</dt><dd>{esc(rel)}</dd><dt>Drawdown</dt><dd>{esc(_fmt_pct_or_text(get(b, "drawdown")))}</dd>'
                f'<dt>Started</dt><dd>{esc(started)}</dd></dl>'
                f'{f"<span class=small>Flags: {esc(flags)}</span>" if flags and flags != "-" else ""}</li>')
    note = esc(get(ps, "note") or "")
    return f'<ul class="books">{out}</ul>' + (f'<p class="small muted">{note}</p>' if note else "")


def _portfolio(ps: Optional[dict]) -> str:
    if not ps:
        return empty("No portfolio loaded.", "Portfolio fit is not assessed until you connect IndMoney (read-only) or upload a Finboom CSV. Holdings stay on your machine.")
    cur = get(ps, "currency") or ""
    parts = []
    if get(ps, "value") is not None: parts.append(("Value", money(get(ps, "value"), cur)))
    if get(ps, "n_holdings") is not None: parts.append(("Holdings", str(get(ps, "n_holdings"))))
    if get(ps, "cash_pct") is not None: parts.append(("Cash", _fmt_pct_or_text(get(ps, "cash_pct"))))
    facts = "".join(f'<div class="fact"><span class="k">{esc(k)}</span><span class="v">{esc(v)}</span></div>' for k, v in parts)
    notes = "".join(f"<li>{esc(n)}</li>" for n in (get(ps, "notes") or []))
    return (f'<div class="panel stack"><div class="facts">{facts}</div>'
            f'{f"<ul class=log>{notes}</ul>" if notes else ""}'
            f'<p class="small muted">Summary only. Individual holdings are never shown or stored here.</p></div>')


def _discoveries(cands: list) -> str:
    if not cands:
        return empty("No new discoveries today.", "The daily screen found nothing new above the threshold.")
    rows = ""
    for c in cands:
        sc = num(get(c, "score"))
        rows += (f'<tr><td><b>{esc(get(c, "name") or get(c, "company") or get(c, "ticker"))}</b><br><span class="mono small muted">{esc(get(c, "ticker"))} · {esc(get(c, "market"))}</span></td>'
                 f'<td>{esc(short(get(c, "note") or get(c, "reason") or "", 140)) or "<span class=muted>No note.</span>"}</td>'
                 f'<td class="r mono">{f"{sc:.2f}" if sc is not None else "n/a"}</td></tr>')
    return ('<div class="scroll"><table><thead><tr><th>Company</th><th>Why it surfaced</th><th class="r">Screen score</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>'
            '<p class="small muted">Level 1 discovery only: a quantitative screen with no deep research yet. Not a recommendation to research or buy.</p>')


def _more_rows(ts: list, href) -> str:
    if not ts: return ""
    rows = "".join(
        f'<tr><td>{_name(t, href)}<br><span class="mono small muted">{esc(t.ticker)} · {esc(t.market)}</span></td><td>{status_pill(t.status)}</td>'
        f'<td>{entry_pill(t.entry.state)}</td><td class="r mono">{f"{t.overall_score:.2f}" if num(t.overall_score) is not None else "n/a"}</td></tr>' for t in ts)
    return ('<div class="scroll"><table><thead><tr><th>Company</th><th>Status</th><th>Entry</th><th class="r">Lab score</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def _tile(n: int, label: str, desc: str, href: str, hot: bool = False) -> str:
    return (f'<li><a class="tile{" hot" if hot and n else ""}" href="{href}"><span class="n{" on" if n else ""}">{n}</span>'
            f'<span class="l">{esc(label)}</span><span class="d">{esc(desc)}</span></a></li>')


def build_today(theses: list, alerts: list, candidates: list, portfolio_summary: Optional[dict], paper_status: Optional[dict], as_of: str,
                sample: bool = False, opportunity_href: Optional[Callable[[Thesis], str]] = None) -> str:
    theses = [t for t in (theses or []) if isinstance(t, Thesis)]
    alerts, candidates = list(alerts or []), list(candidates or [])
    active = sorted([t for t in theses if is_active(t)], key=rank_key)
    top, rest = active[:MAX_CARDS], active[MAX_CARDS:]
    exits = [t for t in theses if exit_triggered(t)]
    n_high = sum(1 for t in theses if is_high_priority(t))
    n_changed = sum(1 for t in theses if is_changed(t, as_of))
    n_improved = sum(1 for t in theses if entry_improved(t, as_of))
    n_disc = len(candidates) + sum(1 for t in theses if t.status == "early_discovery" and t.version == 1 and _recent(t, as_of))

    banner = ""
    if sample:
        banner = ('<div class="banner" role="note"><strong>Sample data.</strong> Every company, ticker, price and thesis on this page is synthetic and fictional. '
                  'It shows the layout only. It is not research and not about any real company.</div>')

    if top:
        cards = "".join(_card(t, i + 1, opportunity_href) for i, t in enumerate(top))
        opp = (f'<ol class="cards">{cards}</ol>'
               '<p class="small muted">Ranked by research stage first, then lab score, so a thin early screen never outranks a researched idea. Scores come from declared default weights that have not been validated. Upside ranges and probabilities are model estimates, not forecasts.</p>')
    else:
        opp = empty("No opportunities to rank yet.", "No theses exist in the store. Run discovery, then the research queue, to produce Level 1 candidates and deeper theses.")

    more = ""
    if rest:
        more = f'<section aria-labelledby="h-more"><div class="sec-head"><h2 id="h-more">Also on the list</h2><p class="muted small">Lower-ranked ideas, in brief.</p></div>{_more_rows(rest, opportunity_href)}</section>'

    as_of_txt = esc(as_of or "date unknown")
    body = f"""<div class="wrap">
<header class="top"><div class="brand"><span class="eyebrow">MultibaggerLab · as of {as_of_txt}</span><h1>What deserves your attention today</h1></div>{theme_button()}</header>
{banner}
<section aria-labelledby="h-counts"><h2 class="sr" id="h-counts">Today in numbers</h2>
<ul class="tiles">
{_tile(n_high, "High-priority ideas", "Late-stage status, or score 0.70+ with a surviving adversarial review and a workable entry state", "#opportunities")}
{_tile(n_changed, "Theses changed", f"New version in the last {RECENT_DAYS} days", "#opportunities")}
{_tile(n_improved, "Entry setups improved", "Timing moved closer to an entry zone", "#opportunities")}
{_tile(len(exits), "Exit conditions triggered", "Review before anything else", "#alerts", hot=True)}
{_tile(n_disc, "New discoveries", "Level 1 screen only, no research yet", "#discoveries")}
</ul></section>
<section id="alerts" aria-labelledby="h-alerts"><div class="sec-head"><h2 id="h-alerts">Alerts</h2><p class="muted small">Only material changes, most severe first.</p></div>{_alerts(alerts, exits, opportunity_href)}</section>
<section id="opportunities" aria-labelledby="h-opp"><div class="sec-head"><h2 id="h-opp">Opportunities, ranked</h2><p class="muted small">Showing {len(top)} of {len(active)} active ideas. Each is a research thesis with reasons to doubt it, not a call to buy.</p></div>{opp}</section>
{more}
<section id="discoveries" aria-labelledby="h-disc"><div class="sec-head"><h2 id="h-disc">New discoveries</h2></div>{_discoveries(candidates)}</section>
<div class="grid2">
<section id="books" aria-labelledby="h-books"><div class="sec-head"><h2 id="h-books">Paper-trading books</h2><p class="muted small">Forward test with frozen rules. Not real money.</p></div>{_books(paper_status)}</section>
<section id="portfolio" aria-labelledby="h-pf"><div class="sec-head"><h2 id="h-pf">Your portfolio</h2></div>{_portfolio(portfolio_summary)}</section>
</div>
<footer class="honesty" aria-labelledby="h-honest"><h2 id="h-honest">What the lab has and has not proven</h2>
<dl>{"".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in HONESTY)}</dl>
<p class="disclaimer">{esc(DISCLAIMER)}</p></footer>
</div>"""
    return page("MultibaggerLab Today", body)
