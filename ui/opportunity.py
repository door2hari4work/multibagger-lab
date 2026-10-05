"""One opportunity page, following the master structure. build_opportunity() returns one self-contained HTML string."""
from __future__ import annotations
from typing import Any, Optional

from mblab.schema import Thesis, DISCLAIMER
from ._common import (
    esc, slug, get, num, days_between, money, mult, pct, short, safe_url, page, theme_button, pill, status_pill, entry_pill, est, empty, score_bar,
    STATUS, ENTRY, COMPONENTS, COMPONENT_LABEL, LEVELS, EVIDENCE_HELP, ACTIVE_EXCLUDED,
)

STALE_DAYS = 120
VAL_LABELS = {
    "pe_ttm": "P/E (trailing)", "pe_fwd": "P/E (forward)", "ev_sales": "EV / Sales", "ev_ebitda": "EV / EBITDA", "ev_fcf": "EV / free cash flow",
    "pb": "Price / book", "peg": "PEG", "fcf_yield": "Free-cash-flow yield", "market_cap": "Market cap", "mcap": "Market cap", "mcap_cr": "Market cap (crore)",
    "mcap_usd_m": "Market cap (USD m)", "roe": "Return on equity", "roce": "Return on capital", "net_debt_ebitda": "Net debt / EBITDA",
}
SECTIONS = [("why", "Why now"), ("mechanism", "Mechanism"), ("rerating", "Re-rating"), ("inflection", "Financials"), ("valuation", "Valuation"),
            ("moat", "Competition"), ("catalysts", "Catalysts"), ("entry", "Entry plan"), ("bear", "Bear case"), ("wrong", "Why we could be wrong"),
            ("fit", "Portfolio"), ("monitor", "Monitor"), ("evidence", "Evidence"), ("history", "History")]


def _sec(sid: str, title: str, body: str, lede: str = "") -> str:
    l = f'<p class="muted small">{esc(lede)}</p>' if lede else ""
    return f'<section id="{sid}" aria-labelledby="h-{sid}"><div class="sec-head"><h2 id="h-{sid}">{esc(title)}</h2>{l}</div>{body}</section>'


def _prose(*texts: str) -> str:
    ps = "".join(f"<p>{esc(t)}</p>" for t in texts if t)
    return f'<div class="prose">{ps}</div>' if ps else ""


def _l1_note(t: Thesis, what: str) -> str:
    if t.research_level <= 1:
        return empty("Level 1 discovery only: no deep research yet.", f"{what} will appear after qualification and deep-dive research.")
    return empty("Not yet written.", what)


def _comp(t: Thesis, key: str):
    return next((c for c in t.scores if c.name == key), None)


def _comp_block(t: Thesis, keys: list) -> str:
    out = ""
    for k in keys:
        c = _comp(t, k)
        if c and c.value is not None:
            out += f'<div class="stack" style="gap:4px"><ul class="bars" style="grid-template-columns:1fr">{score_bar(COMPONENT_LABEL[k], c.value, c.data_quality, c.basis)}</ul>{f"<p class=small>{esc(c.basis)}</p>" if c.basis else ""}</div>'
    return out


# ---- sections ------------------------------------------------------------------------------------------

def _levels(t: Thesis) -> str:
    items = "".join(f'<li class="{"done" if i + 1 <= t.research_level else ""}"><span>L{i + 1} {esc(n)}</span></li>' for i, n in enumerate(LEVELS))
    return f'<ol class="levels" aria-label="Research depth: level {t.research_level} of 6">{items}</ol>'


def _header(t: Thesis, assessment: Any) -> str:
    lab, tone, meaning = STATUS.get(t.status, (t.status, "neutral", ""))
    banner = ""
    if t.status in ACTIVE_EXCLUDED:
        banner = f'<div class="banner crit" role="note"><strong>{esc(lab)}.</strong> {esc(meaning)}</div>'
    elif t.research_level <= 1:
        banner = '<div class="banner info" role="note"><strong>Level 1 discovery only: no deep research yet.</strong> Everything below is thin by design. Treat it as a reason to look, not a conclusion.</div>'
    ov = f"{t.overall_score:.2f}" if num(t.overall_score) is not None else "n/a"
    ass = ""
    if assessment:
        if isinstance(assessment, str): head, bullets = assessment, []
        else: head, bullets = get(assessment, "headline") or get(assessment, "summary") or "", list(get(assessment, "bullets") or get(assessment, "notes") or [])
        lis = "".join(f"<li>{esc(b)}</li>" for b in bullets)
        ass = (f'<div class="panel stack"><span class="eyebrow">Latest assessment</span>{f"<p>{esc(head)}</p>" if head else ""}'
               f'{f"<ul class=log>{lis}</ul>" if lis else ""}</div>')
    return f"""<header class="hero panel">
<div class="top"><div class="brand"><span class="eyebrow">Opportunity · thesis v{t.version} · as of {esc(t.as_of or "date unknown")}</span></div>{theme_button()}</div>
<h1>{esc(t.company or t.ticker)}</h1>
<div class="chips"><span class="tag mono">{esc(t.ticker)}</span><span class="tag">{esc(t.market)}</span>{status_pill(t.status)}{entry_pill(t.entry.state)}
<span class="tag">Confidence in evidence: {esc(t.confidence)}</span></div>
<p class="muted">{esc(meaning)}</p>
{banner}
<div class="facts">
<div class="fact"><span class="k">Price</span><span class="v">{esc(money(t.price, t.currency))} <span class="muted small">{esc("as of " + t.price_ts[:10]) if t.price_ts else "price date unknown"}</span></span></div>
<div class="fact"><span class="k">Lab score</span><span class="v">{esc(ov)} <span class="muted small">declared weights, unvalidated</span></span></div>
<div class="fact"><span class="k">Time horizon</span><span class="v">{f"{t.time_horizon_months} months" if t.time_horizon_months else '<span class="muted">not set</span>'}</span></div>
<div class="fact"><span class="k">Next review</span><span class="v">{esc(t.next_review) if t.next_review else '<span class="muted">not scheduled</span>'}</span></div>
</div>
<div class="stack" style="gap:6px"><span class="eyebrow">Research depth: level {t.research_level} of 6</span>{_levels(t)}</div>
{ass}
</header>"""


def _why(t: Thesis) -> str:
    if not (t.why_now or t.thesis):
        return _l1_note(t, "The reason this deserves attention now")
    return _prose(t.why_now, t.thesis)


def _scen_row(s, name: str, axis_max: float, fallback_h) -> str:
    if not s: return ""
    lo, hi = num(s.multiple_low), num(s.multiple_high)
    if lo is None and hi is None:
        return f'<div class="scen"><span class="nm">{esc(name)}</span><span class="muted small">No range estimated.</span><span class="txt">{esc(s.description)}</span></div>'
    lo = lo if lo is not None else hi
    hi = hi if hi is not None else lo
    left, width = lo / axis_max * 100, max((hi - lo) / axis_max * 100, 1.5)
    h = s.horizon_months or fallback_h
    p = f"probability about {pct(s.probability)} {est('estimate')}" if num(s.probability) is not None else "probability not estimated"
    rng = mult(lo) if lo == hi else f"{mult(lo)} to {mult(hi)}"
    return (f'<div class="scen {"bear" if name.lower() == "bear" else ""}"><span class="nm">{esc(name)}</span>'
            f'<span class="rng" role="img" aria-label="{esc(name)} case {esc(rng)}"><span class="seg" style="left:{left:.1f}%;width:{min(width, 100 - left):.1f}%"></span></span>'
            f'<span class="txt"><b class="mono">{esc(rng)}</b>{f" over {h} months" if h else ""}, {p}.<br>{esc(s.description)}</span></div>')


def _mechanism(t: Thesis) -> str:
    sc = [s for s in (t.bear_case, t.base_case, t.bull_case) if s]
    his = [num(x) for s in sc for x in (s.multiple_low, s.multiple_high) if num(x) is not None]
    axis = max(his + [1.0]) * 1.05
    scen = "".join(_scen_row(s, n, axis, t.time_horizon_months) for s, n in ((t.bear_case, "Bear"), (t.base_case, "Base"), (t.bull_case, "Bull")))
    body = ""
    if t.multibagger_mechanism: body += _prose(t.multibagger_mechanism)
    else: body += _l1_note(t, "How this could grow several times over")
    if scen:
        body += (f'<div class="panel stack"><div class="chips"><h3>Scenarios</h3>{est()}</div>'
                 f'<p class="small muted">Multiples are of today\'s price. Ranges and probabilities are the lab\'s model estimates, not predictions. A big multiple with a small probability does not outrank a likelier smaller one.</p>{scen}</div>')
    return body


def _rerating(t: Thesis) -> str:
    if not t.expectations_gap: return _l1_note(t, "What the market may be missing and what would change its mind")
    return _prose(t.expectations_gap)


def _inflection(t: Thesis) -> str:
    comps = _comp_block(t, ["earnings_inflection", "growth_acceleration"])
    ev = [e for e in t.evidence if e.period and e.source_type in ("filing", "call", "exchange", "investor_presentation")]
    evh = "".join(f'<li><b>{esc(e.period)}</b>: {esc(e.claim)} <span class="chip k-{slug(e.kind).upper()}">{esc(e.kind)}</span></li>' for e in ev)
    if not comps and not evh: return _l1_note(t, "Revenue, margin and earnings trends with the periods they come from")
    return f'<div class="stack">{comps}{f"<ul class=log>{evh}</ul>" if evh else ""}</div>'


def _fmt_val(v: Any) -> str:
    f = num(v)
    return (f"{f:,.1f}" if abs(f) < 1000 else f"{f:,.0f}") if f is not None else str(v)


def _valuation(t: Thesis) -> str:
    kv = "".join(f'<div class="fact"><span class="k">{esc(VAL_LABELS.get(k, str(k).replace("_", " ")))}</span><span class="v mono">{esc(_fmt_val(v))}</span></div>' for k, v in (t.valuation or {}).items())
    comps = _comp_block(t, ["valuation_asymmetry"])
    if not kv and not comps: return _l1_note(t, "Valuation multiples against growth and peers")
    return f'<div class="stack">{f"<div class=kv>{kv}</div>" if kv else ""}{comps}<p class="small muted">A good company is not always a good investment at today\'s price. This section asks whether the price already assumes the good news.</p></div>'


def _moat(t: Thesis) -> str:
    comps = _comp_block(t, ["competitive_advantage", "business_quality", "tam_expansion"])
    return comps or _l1_note(t, "Where the company wins and why rivals cannot copy it")


def _catalysts(t: Thesis) -> str:
    if not t.catalysts: return _l1_note(t, "Dated events that could change how the market sees the company")
    tone = {"pending": "info", "occurred": "good", "failed": "crit", "delayed": "warn"}
    rows = "".join(f'<li class="row s-{slug(tone.get(c.status, "neutral"))}">{pill(c.status.capitalize(), tone.get(c.status, "neutral"))}'
                   f'<div class="body"><span class="title">{esc(c.description)}</span><span class="small muted">{esc(c.window) if c.window else "timing not set"}'
                   f'{(" · evidence " + esc(", ".join(c.evidence_ids))) if c.evidence_ids else ""}</span></div></li>' for c in t.catalysts)
    return f'<ul class="list">{rows}</ul>'


def _ladder(t: Thesis) -> str:
    e, cur = t.entry, t.currency
    zones = [("ideal", "Ideal zone", e.ideal_zone, "z-ideal", "band-ideal"), ("ok", "Acceptable zone", e.acceptable_zone, "z-ok", "band-ok"),
             ("chase", "Chase zone (higher risk of overpaying)", e.chase_zone, "z-chase", "band-chase")]
    valid = [(k, lab, z, sw, bc) for k, lab, z, sw, bc in zones if z and len(z) == 2 and num(z[0]) is not None and num(z[1]) is not None]
    pts = [num(x) for _, _, z, _, _ in valid for x in z] + [num(t.price), num(e.invalidation_price)]
    pts = [p for p in pts if p is not None]
    if not valid and num(e.invalidation_price) is None:
        return empty("No entry zones yet.", "Entry zones need Level 4 research and a completed adversarial review. Until then there is no price at which the lab calls this attractive.")
    lo, hi = min(pts), max(pts)
    pad = (hi - lo) * 0.06 or hi * 0.05 or 1
    lo, hi = lo - pad, hi + pad
    X = lambda v: (v - lo) / (hi - lo) * 600
    shapes = '<rect class="axis" x="0" y="34" width="600" height="14" rx="3"/>'
    for k, lab, z, sw, bc in valid:
        a, b = sorted((num(z[0]), num(z[1])))
        shapes += f'<rect class="{bc}" x="{X(a):.1f}" y="30" width="{max(X(b) - X(a), 3):.1f}" height="22" rx="3"/>'
    if num(e.invalidation_price) is not None:
        x = X(num(e.invalidation_price)); shapes += f'<path class="inv" d="M{x:.1f} 22 V60"/>'
    if num(t.price) is not None:
        x = X(num(t.price)); shapes += f'<path class="now" d="M{x:.1f} 28 l-7 -14 h14 z"/>'
    desc = "; ".join(f"{lab} {money(z[0], cur)} to {money(z[1], cur)}" for _, lab, z, _, _ in valid)
    aria = f"Price ladder. Now {money(t.price, cur)}. {desc}. Invalidation {money(e.invalidation_price, cur)}."
    svg = f'<svg class="ladder" viewBox="0 0 600 66" role="img" aria-label="{esc(aria)}" preserveAspectRatio="xMidYMid meet">{shapes}</svg>'
    leg = "".join(f'<li><span class="sw {sw}"></span><span><b>{esc(lab)}</b>: <span class="mono">{esc(money(z[0], cur))} to {esc(money(z[1], cur))}</span></span></li>' for _, lab, z, sw, _ in valid)
    if num(t.price) is not None: leg = f'<li><span class="mono" aria-hidden="true">&#9660;</span><span><b>Now</b>: <span class="mono">{esc(money(t.price, cur))}</span></span></li>' + leg
    if num(e.invalidation_price) is not None:
        leg += f'<li><span class="sw z-inv"></span><span><b>Invalidation</b>: <span class="mono">{esc(money(e.invalidation_price, cur))}</span>. A close below this means the idea is wrong or the setup has failed.</span></li>'
    return f'{svg}<ul class="zones">{leg}</ul>'


def _entry(t: Thesis) -> str:
    e = t.entry
    lab = ENTRY.get(e.state, ENTRY["unknown"])[0]
    exits = ""
    if t.exit_rules:
        tone = {"armed": "neutral", "warning": "warn", "triggered": "crit"}
        exits = ('<h3>What would make us exit</h3><ul class="list">' + "".join(
            f'<li class="row s-{slug(tone.get(x.status, "neutral"))}">{pill(x.status.capitalize(), tone.get(x.status, "neutral"))}<div class="body"><span class="title">{esc(x.condition)}</span>'
            f'<span class="small muted">{esc(x.type.replace("_", " "))}</span></div></li>' for x in t.exit_rules) + "</ul>")
    else:
        exits = empty("No exit rules yet.", "The lab will not call an entry without explicit exit conditions.")
    return (f'<div class="stack"><p>Timing now: {entry_pill(e.state)} <span class="sr">{esc(lab)}</span></p>{_ladder(t)}'
            f'{_prose(e.rationale) if e.rationale else ""}'
            f'<p class="small muted">Zones are rounded ranges, not exact prices. Prices move; check the current quote before acting.</p>{exits}</div>')


def _bear(t: Thesis) -> str:
    a, s = t.adversarial, t.bear_case
    parts = ""
    if s:
        rng = ""
        if num(s.multiple_low) is not None or num(s.multiple_high) is not None:
            lo, hi = num(s.multiple_low), num(s.multiple_high)
            rng = f"<p><b class='mono'>{esc(mult(lo) if hi in (None, lo) else mult(lo) + ' to ' + mult(hi))}</b> of today's price {est()}</p>"
        parts += f'<div class="panel stack"><h3>If it goes wrong</h3>{rng}<p>{esc(s.description)}</p></div>'
    if a.strongest_bear_case:
        parts += f'<div class="panel stack"><h3>Strongest case against, from the adversarial reviewer</h3><p>{esc(a.strongest_bear_case)}</p></div>'
    if a.done:
        tone = {"survives": "good", "downgraded": "warn", "killed": "crit"}.get(a.verdict, "neutral")
        parts += f'<p>Adversarial review: {pill((a.verdict or "no verdict").capitalize(), tone)} <span class="muted small">{esc(a.reviewer)} {esc(a.reviewed_at[:10])}</span></p>'
    else:
        parts += empty("Adversarial review not done.", "No one has tried to kill this idea yet, so treat any enthusiasm with caution. Entry calls are blocked until it is done.")
    return f'<div class="stack">{parts}</div>' if (s or a.strongest_bear_case or a.done) else parts


def _wrong(t: Thesis) -> str:
    risks = "".join(f"<li>{esc(r)}</li>" for r in t.risks)
    qa = "".join(f'<details class="qa"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in (t.adversarial.questions or {}).items())
    if not risks and not qa: return _l1_note(t, "The main ways this could fail")
    return f'<div class="stack">{f"<ul class=log>{risks}</ul>" if risks else ""}{f"<h3>Self-critique questions</h3>{qa}" if qa else ""}</div>'


def _fit(t: Thesis, pf: Any) -> str:
    pf = pf if pf is not None else t.portfolio_fit
    sc, summ = num(get(pf, "score")), get(pf, "summary") or ""
    notes, mw = list(get(pf, "overlap_notes") or []), num(get(pf, "suggested_max_weight_pct"))
    if sc is None and not summ and not notes:
        return empty("Not assessed.", "No portfolio is loaded, so overlap, concentration and position size are unknown. Connect IndMoney (read-only) or upload a Finboom CSV.")
    facts = ""
    if sc is not None: facts += f'<div class="fact"><span class="k">Fit score</span><span class="v mono">{sc:.2f}</span></div>'
    if mw is not None: facts += f'<div class="fact"><span class="k">Suggested ceiling</span><span class="v mono">{mw:g}% of portfolio</span></div>'
    nl = "".join(f"<li>{esc(n)}</li>" for n in notes)
    return f'<div class="stack"><div class="facts">{facts}</div>{_prose(summ)}{f"<ul class=log>{nl}</ul>" if nl else ""}<p class="small muted">A size ceiling is a risk-control idea, not an instruction.</p></div>'


def _monitor(t: Thesis) -> str:
    items = []
    if t.next_review: items.append(("Scheduled review", t.next_review))
    for c in t.catalysts:
        if c.status in ("pending", "delayed"): items.append(("Catalyst" + (" (delayed)" if c.status == "delayed" else ""), f"{c.description}" + (f" ({c.window})" if c.window else "")))
    for x in t.exit_rules:
        if x.status != "triggered": items.append(("Exit trigger" + (" (warning)" if x.status == "warning" else ""), x.condition))
    for e in t.evidence:
        if e.kind == "SPECULATION": items.append(("Unproven assumption", e.claim))
    if not items: return _l1_note(t, "A short watch-list of events and numbers that would change the view")
    rows = "".join(f"<li><b>{esc(k)}:</b> {esc(v)}</li>" for k, v in items)
    return f'<ul class="log">{rows}</ul>'


def _evidence(t: Thesis) -> str:
    if not t.evidence: return _l1_note(t, "Sourced facts, our inferences and open guesses, each labelled and dated")
    order = {"FACT": 0, "INFERENCE": 1, "SPECULATION": 2}
    out = ""
    for e in sorted(t.evidence, key=lambda e: (order.get(e.kind, 3), e.source_date or "")):
        k = e.kind if e.kind in order else "SPECULATION"
        age = days_between(t.as_of or t.price_ts, e.source_date)
        stale = f' {pill("Over 120 days old", "warn")}' if k == "FACT" and age is not None and age > STALE_DAYS else ""
        u = safe_url(e.source_url)
        src = (f'<a href="{esc(u)}" target="_blank" rel="noopener noreferrer">{esc(e.source_type or "source")}</a>' if u else esc(e.source_type or "no source"))
        out += (f'<div class="ev"><div class="chips"><span class="chip k-{k}" title="{esc(EVIDENCE_HELP[k])}">{k}</span><span class="small">{esc(EVIDENCE_HELP[k])}</span>{stale}</div>'
                f'<p>{esc(e.claim)}</p><p class="small muted">{src} · source date {esc(e.source_date or "unknown")}{f" · period {esc(e.period)}" if e.period else ""}{f" · {esc(e.note)}" if e.note else ""}'
                f' · <span class="mono">{esc(e.id)}</span></p></div>')
    return f'<div class="panel">{out}</div>'


def _history(t: Thesis, history: Optional[list]) -> str:
    log = "".join(f"<li>{esc(x)}</li>" for x in t.change_log)
    parent = f", built on v{t.parent_version}" if t.parent_version else ""
    cur = (f'<div class="panel stack"><h3>v{t.version}{parent}</h3><p class="small muted">Created {esc(t.created_at[:16].replace("T", " "))} UTC</p>'
           f'{f"<ul class=log>{log}</ul>" if log else "<p class=muted>No change log recorded.</p>"}</div>')
    prev = ""
    for h in sorted([x for x in (history or []) if isinstance(x, Thesis) and x.version != t.version], key=lambda x: -x.version):
        hl = "".join(f"<li>{esc(x)}</li>" for x in h.change_log)
        prev += (f'<details class="qa"><summary>v{h.version}: {esc(STATUS.get(h.status, (h.status,))[0])}, level {h.research_level}, {esc(h.created_at[:10])}</summary>'
                 f'{f"<ul class=log>{hl}</ul>" if hl else "<p class=muted>No change log recorded.</p>"}</details>')
    return f'<div class="stack">{cur}{prev}<p class="small muted">Versions are append-only. Earlier versions are never overwritten, so you can see how the view changed.</p></div>'


def build_opportunity(thesis: Thesis, assessment: Any = None, portfolio_fit: Any = None, history: Optional[list] = None, sample: bool = False) -> str:
    t = thesis
    nav = "".join(f'<li><a href="#{i}">{esc(n)}</a></li>' for i, n in SECTIONS)
    sample_b = ('<div class="banner" role="note"><strong>Sample data.</strong> This company and thesis are synthetic and fictional. Layout demonstration only.</div>' if sample else "")
    body = f"""<div class="wrap">
{sample_b}
{_header(t, assessment)}
<nav aria-label="Sections"><ul class="navchips">{nav}</ul></nav>
{_sec("why", "Why this matters now", _why(t))}
{_sec("mechanism", "The multibagger mechanism", _mechanism(t), "How the stock could grow several times over, and how likely the lab thinks that is.")}
{_sec("rerating", "What could drive the re-rating", _rerating(t), "What the market may be missing, and what would change its mind.")}
{_sec("inflection", "Financial inflection", _inflection(t))}
{_sec("valuation", "Valuation", _valuation(t))}
{_sec("moat", "Competitive position", _moat(t))}
{_sec("catalysts", "Catalysts", _catalysts(t))}
{_sec("entry", "Entry plan", _entry(t), "Where the lab would and would not be comfortable, and what proves the idea wrong.")}
{_sec("bear", "Bear case", _bear(t))}
{_sec("wrong", "Why we could be wrong", _wrong(t))}
{_sec("fit", "Portfolio impact", _fit(t, portfolio_fit))}
{_sec("monitor", "What to monitor", _monitor(t))}
{_sec("evidence", "Source evidence", _evidence(t), "FACT is documented and sourced. INFERENCE is our reasoning. SPECULATION is a guess.")}
{_sec("history", "Thesis version history", _history(t, history))}
<footer class="honesty"><p class="disclaimer">{esc(DISCLAIMER)}</p><p class="small muted">Past tests have survivor bias and forward tracking has only just begun. Nothing here is a prediction.</p></footer>
</div>"""
    return page(f"{t.company or t.ticker} thesis", body)
