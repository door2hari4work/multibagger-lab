"""Shared helpers and the inline design system for the UI. Every piece of text that originates outside this file goes through esc()."""
from __future__ import annotations
import html
import re
from datetime import date
from typing import Any, Optional

from mblab.schema import DISCLAIMER

# ---- escaping / safe values -------------------------------------------------------------------


def esc(x: Any) -> str:
    """HTML-escape any value (None -> ''). Quotes are escaped so the result is safe in text and attribute context."""
    return "" if x is None else html.escape(str(x), quote=True)


def slug(x: Any) -> str:
    """Restrict a value to [a-z0-9_] for use in class names / ids."""
    return re.sub(r"[^a-z0-9_]", "", str(x or "").lower().replace("-", "_").replace(" ", "_"))


def safe_url(u: Any) -> str:
    u = str(u or "").strip()
    return u if re.match(r"^https?://", u, re.I) else ""


def get(o: Any, k: str, default: Any = None) -> Any:
    """Read a key from a dict or an attribute from an object."""
    if o is None: return default
    if isinstance(o, dict): return o.get(k, default)
    return getattr(o, k, default)


def num(x: Any) -> Optional[float]:
    try:
        if x is None or isinstance(x, bool): return None
        f = float(x)
        return f if f == f and abs(f) != float("inf") else None
    except (TypeError, ValueError):
        return None


def parse_date(s: Any) -> Optional[date]:
    try: return date.fromisoformat(str(s)[:10])
    except (TypeError, ValueError): return None


def days_between(a: Any, b: Any) -> Optional[int]:
    da, db = parse_date(a), parse_date(b)
    return (da - db).days if da and db else None


CURRENCY = {"INR": "₹", "USD": "$", "EUR": "€", "GBP": "£"}


def money(v: Any, cur: str = "") -> str:
    f = num(v)
    if f is None: return "n/a"
    sym = CURRENCY.get((cur or "").upper(), "")
    body = f"{f:,.0f}" if abs(f) >= 1000 else f"{f:,.2f}"
    return f"{sym}{body}" if sym else (f"{body} {cur}".strip())


def mult(v: Any) -> str:
    f = num(v)
    if f is None: return "n/a"
    return f"{f:g}x" if f == int(f) else f"{f:.1f}x"


def pct(v: Any, digits: int = 0, frac: bool = True) -> str:
    f = num(v)
    if f is None: return "n/a"
    return f"{(f * 100 if frac else f):.{digits}f}%"


def short(text: Any, n: int = 150) -> str:
    t = " ".join(str(text or "").split())
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


# ---- vocabulary ----------------------------------------------------------------------------------

STATUS = {  # key: (label, tone, plain-language meaning)
    "early_discovery": ("Early discovery", "info", "Flagged by the quantitative screen. No deep research yet."),
    "research_required": ("Needs research", "info", "Looks interesting enough to research. The work has not been done."),
    "watchlist": ("Watchlist", "neutral", "Researched and worth following. Not yet at an attractive price or setup."),
    "preparing_to_enter": ("Getting ready", "accent", "Research is solid and the setup is forming. Entry zones are being prepared."),
    "attractive_entry": ("Attractive entry", "good", "Research, review and price setup line up under the lab's rules. Your decision."),
    "accumulate": ("Accumulate", "good", "An existing position could be added to within the planned zones."),
    "hold": ("Hold", "neutral", "The thesis is intact. Nothing to do unless a trigger fires."),
    "trim": ("Trim", "warn", "Part of the reason to own it has been used up or has weakened."),
    "exit": ("Exit", "crit", "An exit condition has been met. Review the position."),
    "thesis_broken": ("Thesis broken", "crit", "The core reason for the idea no longer holds."),
    "rejected": ("Rejected", "neutral", "Reviewed and dropped. Kept for the record."),
}
ACTIVE_EXCLUDED = {"rejected", "thesis_broken", "exit"}
LATE_STAGE = {"preparing_to_enter", "attractive_entry", "accumulate"}
REVIEW_STATUSES = {"trim", "exit", "thesis_broken"}

ENTRY = {  # key: (label, tone)
    "too_early": ("Too early", "neutral"), "setup_forming": ("Setup forming", "accent"), "attractive_entry": ("In attractive zone", "good"),
    "confirmation_entry": ("Wait for confirmation", "accent"), "breakout_entry": ("Breakout entry", "good"), "overextended": ("Overextended", "warn"),
    "wait_for_pullback": ("Wait for pullback", "warn"), "thesis_deteriorating": ("Thesis weakening", "crit"), "unknown": ("Entry timing not assessed", "neutral"),
}
GOOD_ENTRY = {"attractive_entry", "confirmation_entry", "breakout_entry"}

COMPONENTS = [  # (key, label)
    ("business_quality", "Business quality"), ("growth_acceleration", "Growth acceleration"), ("earnings_inflection", "Earnings inflection"),
    ("tam_expansion", "Market expansion"), ("catalyst_strength", "Catalyst strength"), ("competitive_advantage", "Competitive edge"),
    ("valuation_asymmetry", "Valuation asymmetry"), ("market_confirmation", "Market confirmation"), ("timing", "Timing"),
    ("risk", "Risk (higher = safer)"), ("thesis_robustness", "Thesis robustness"), ("portfolio_fit", "Portfolio fit"),
]
COMPONENT_LABEL = dict(COMPONENTS)

LEVELS = ["Discovery", "Qualification", "Deep dive", "Adversarial review", "Portfolio fit", "Timing"]
SEVERITY = {"critical": (0, "Critical", "crit"), "high": (1, "High", "crit"), "medium": (2, "Medium", "warn"), "low": (3, "Low", "neutral"), "info": (4, "Info", "info")}
EVIDENCE_HELP = {"FACT": "Documented and sourced", "INFERENCE": "Our reasoning from facts", "SPECULATION": "A guess, treat with care"}

HONESTY = [
    ("What the lab has shown", "Ranking stocks by recent price momentum has beaten simple benchmarks in past tests, mainly in India large and mid caps. The edge is modest, weak in the US and close to absent in micro caps."),
    ("What it has not shown", "The earnings, growth and cash-quality filters did not improve results in the one market tested. Thesis quality cannot be back-tested, because there is no record of what was knowable on past dates."),
    ("Survivor bias", "Historical tests use companies that exist today. Firms that failed or were delisted are missing, so past results look better than a real investor would have seen."),
    ("Forward tracking only", "The paper-trading books start on 2026-10-30 with frozen rules. Nothing before that date counts as proof. Judgement comes after 12 months of live tracking."),
    ("Not advice", DISCLAIMER + " Probabilities and upside ranges are model estimates. They can be wrong by a wide margin."),
]

# ---- design system ---------------------------------------------------------------------------------

CSS = """
/* Layout: one calm column of decisions; summary first, detail on demand. Colour carries state only; the blue accent marks the lab's own estimates and links. */
:root{
  --bg:#F2F4F6; --surface:#FFFFFF; --surface2:#E8ECF0; --fg:#121A24; --muted:#4A5767; --line:#D0D8E0;
  --accent:#1B4DB3; --accent-soft:#E0E9FA; --bar:#1B4DB3; --bar-track:#DCE2E8;
  --good:#11643A; --good-bg:#DAF1E3; --warn:#85500A; --warn-bg:#FAEACB; --crit:#A01F1A; --crit-bg:#F9DAD7; --info:#33566E; --info-bg:#DEEAF1;
  --font-display:Charter,"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  --font-body:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --font-data:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0D131A; --surface:#151D27; --surface2:#1D2834; --fg:#E7EDF3; --muted:#9DABBA; --line:#2B3846;
  --accent:#86ABFF; --accent-soft:#1B2B4A; --bar:#7CA3FA; --bar-track:#2A3745;
  --good:#6FD49C; --good-bg:#13331F; --warn:#F0BB6C; --warn-bg:#3A2C11; --crit:#FF918A; --crit-bg:#401B19; --info:#8DBBD6; --info-bg:#172C38; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0D131A; --surface:#151D27; --surface2:#1D2834; --fg:#E7EDF3; --muted:#9DABBA; --line:#2B3846;
  --accent:#86ABFF; --accent-soft:#1B2B4A; --bar:#7CA3FA; --bar-track:#2A3745;
  --good:#6FD49C; --good-bg:#13331F; --warn:#F0BB6C; --warn-bg:#3A2C11; --crit:#FF918A; --crit-bg:#401B19; --info:#8DBBD6; --info-bg:#172C38; color-scheme:dark}
*,*::before,*::after{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font:15px/1.55 var(--font-body);padding-inline:16px;padding-block:0 40px;-webkit-text-size-adjust:100%}
.wrap{max-width:1080px;margin-inline:auto;display:flex;flex-direction:column;gap:28px;padding-block:16px 0}
h1,h2,h3,h4,p,ul,ol,dl,dd,figure{margin:0}
h1,h2,h3{font-family:var(--font-display);text-wrap:balance;font-weight:700;line-height:1.2}
h1{font-size:1.7rem} h2{font-size:1.3rem} h3{font-size:1.05rem}
a{color:var(--accent);text-underline-offset:2px}
a:focus-visible,button:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--accent);outline-offset:2px;border-radius:4px}
.muted{color:var(--muted)} .small{font-size:.85rem} .mono{font-family:var(--font-data);font-variant-numeric:tabular-nums}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.top{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;justify-content:space-between}
.top .brand{display:flex;flex-direction:column;gap:2px;min-width:0}
.eyebrow{font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:600}
.btn{font:inherit;font-size:.85rem;color:var(--fg);background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:6px 12px;cursor:pointer;min-height:36px}
.btn:hover{background:var(--surface2)}
.banner{border:1px dashed var(--warn);background:var(--warn-bg);color:var(--warn);border-radius:8px;padding:10px 14px;font-size:.9rem}
.banner strong{font-weight:700}
.banner.crit{border-color:var(--crit);background:var(--crit-bg);color:var(--crit)}
.banner.info{border-color:var(--info);background:var(--info-bg);color:var(--info)}
section{display:flex;flex-direction:column;gap:12px;min-width:0;scroll-margin-top:12px}
.sec-head{display:flex;flex-direction:column;gap:2px}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px;min-width:0}
.stack{display:flex;flex-direction:column;gap:10px;min-width:0}
.grid2{display:grid;grid-template-columns:1fr;gap:12px}
@media (min-width:860px){.grid2{grid-template-columns:1fr 1fr}}
/* counts */
.tiles{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;list-style:none;padding:0;margin:0}
.tiles>li:last-child:nth-child(odd){grid-column:1/-1}
@media (min-width:760px){.tiles{grid-template-columns:repeat(5,1fr)}.tiles>li:last-child:nth-child(odd){grid-column:auto}}
.tile{display:flex;flex-direction:column;gap:2px;height:100%;padding:12px 14px;background:var(--surface);border:1px solid var(--line);border-radius:10px;text-decoration:none;color:var(--fg)}
.tile:hover{border-color:var(--accent)}
.tile .n{font-family:var(--font-display);font-size:2rem;line-height:1.1;font-variant-numeric:tabular-nums}
.tile .n.on{color:var(--accent)} .tile.hot .n{color:var(--crit)}
.tile .l{font-weight:600;font-size:.92rem;line-height:1.3} .tile .d{font-size:.78rem;color:var(--muted);line-height:1.35}
/* pills and chips */
.pill{display:inline-flex;align-items:center;gap:5px;font-size:.78rem;font-weight:600;line-height:1.2;padding:3px 9px;border-radius:999px;border:1px solid transparent;white-space:nowrap}
.pill::before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor;flex:none}
.t-good{background:var(--good-bg);color:var(--good)} .t-warn{background:var(--warn-bg);color:var(--warn)} .t-crit{background:var(--crit-bg);color:var(--crit)}
.t-info{background:var(--info-bg);color:var(--info)} .t-accent{background:var(--accent-soft);color:var(--accent)} .t-neutral{background:var(--surface2);color:var(--fg)}
.chips{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.chip{display:inline-block;font-family:var(--font-data);font-size:.72rem;font-weight:700;letter-spacing:.04em;padding:2px 7px;border-radius:4px;border:1.5px solid var(--fg);background:transparent;color:var(--fg);white-space:nowrap}
.chip.k-FACT{background:var(--fg);color:var(--bg)}
.chip.k-INFERENCE{border-style:solid;border-color:var(--accent);color:var(--accent)}
.chip.k-SPECULATION{border-style:dashed;border-color:var(--warn);color:var(--warn)}
.est{display:inline-block;font-size:.68rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);border:1px dashed var(--accent);border-radius:4px;padding:1px 6px;white-space:nowrap}
.tag{font-size:.74rem;color:var(--muted);border:1px solid var(--line);border-radius:4px;padding:1px 6px;white-space:nowrap}
/* opportunity cards */
.cards{display:grid;grid-template-columns:1fr;gap:14px;list-style:none;padding:0;margin:0}
@media (min-width:900px){.cards{grid-template-columns:1fr 1fr}}
.card{display:flex;flex-direction:column;gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px;height:100%;min-width:0}
.card-head{display:flex;gap:12px;align-items:flex-start;justify-content:space-between}
.card-head .who{min-width:0}
.card h3 a{color:var(--fg);text-decoration:none} .card h3 a:hover{text-decoration:underline}
.rank{font-family:var(--font-display);font-size:1.3rem;color:var(--muted);line-height:1;flex:none;min-width:1.4em}
.price{text-align:right;flex:none;font-variant-numeric:tabular-nums}
.price b{font-size:1.05rem;display:block}
.why{font-size:.95rem;padding-left:10px;border-left:3px solid var(--accent)}
.facts{display:grid;grid-template-columns:1fr;gap:8px 16px}
@media (min-width:520px){.facts{grid-template-columns:1fr 1fr}}
.fact{min-width:0;display:flex;flex-direction:column;gap:1px}
.fact .k{font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600}
.fact .v{font-size:.92rem;overflow-wrap:anywhere}
/* score bars */
.bars{display:grid;grid-template-columns:1fr;gap:4px 20px;list-style:none;padding:0;margin:0}
@media (min-width:520px){.bars{grid-template-columns:1fr 1fr}}
.bar{display:grid;grid-template-columns:minmax(0,1fr) 40px;gap:0 8px;align-items:center;font-size:.8rem}
.bar .lab{grid-column:1/-1;display:flex;justify-content:space-between;gap:8px;line-height:1.3}
.bar .track{height:7px;background:var(--bar-track);border-radius:4px;overflow:hidden;grid-column:1}
.bar .fill{display:block;height:100%;background:var(--bar);border-radius:4px}
.bar .val{font-family:var(--font-data);font-size:.76rem;text-align:right;grid-column:2}
.bar.na .track{background:repeating-linear-gradient(135deg,var(--bar-track) 0 4px,transparent 4px 8px);border:1px solid var(--line)}
.bar .dq{font-size:.68rem;color:var(--warn)}
.overall{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:baseline;font-size:.85rem}
.overall b{font-family:var(--font-display);font-size:1.4rem}
/* alerts */
.list{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px}
.row{display:flex;gap:12px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-left-width:5px;border-radius:8px;padding:10px 12px;min-width:0}
.row.s-crit{border-left-color:var(--crit)} .row.s-warn{border-left-color:var(--warn)} .row.s-good{border-left-color:var(--good)} .row.s-accent{border-left-color:var(--accent)} .row.s-neutral{border-left-color:var(--muted)} .row.s-info{border-left-color:var(--info)}
.row .body{display:flex;flex-direction:column;gap:2px;min-width:0;flex:1}
.row .title{font-weight:600;overflow-wrap:anywhere}
/* books strip */
.books{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;list-style:none;padding:0;margin:0}
.book{display:flex;flex-direction:column;gap:6px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px;min-width:0}
.book .name{font-weight:700;display:flex;justify-content:space-between;gap:8px;align-items:center}
.book dl{display:grid;grid-template-columns:auto 1fr;gap:2px 10px;font-size:.84rem}
.book dt{color:var(--muted)} .book dd{text-align:right;font-variant-numeric:tabular-nums}
/* compact table */
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:.88rem}
th,td{text-align:left;padding:8px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
tr:last-child td{border-bottom:0}
td.r,th.r{text-align:right}
/* empty state */
.empty{border:1px dashed var(--line);border-radius:10px;padding:14px 16px;color:var(--muted);background:transparent}
.empty strong{color:var(--fg)}
/* honesty footer */
.honesty{border-top:2px solid var(--fg);padding-top:16px;display:flex;flex-direction:column;gap:12px}
.honesty dl{display:grid;grid-template-columns:1fr;gap:10px}
@media (min-width:860px){.honesty dl{grid-template-columns:1fr 1fr}}
.honesty dt{font-weight:700;font-size:.9rem} .honesty dd{font-size:.88rem;color:var(--muted)}
.disclaimer{font-size:.85rem;font-weight:600}
/* opportunity page */
.navchips{display:flex;gap:6px;overflow-x:auto;padding-bottom:4px;list-style:none;margin:0;padding-inline:0}
.navchips a{display:block;white-space:nowrap;font-size:.8rem;text-decoration:none;color:var(--fg);border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:5px 12px}
.navchips a:hover{border-color:var(--accent);color:var(--accent)}
.hero{display:flex;flex-direction:column;gap:14px}
.hero h1{overflow-wrap:anywhere}
.levels{display:grid;grid-template-columns:repeat(6,1fr);gap:4px;list-style:none;padding:0;margin:0}
.levels li{font-size:.68rem;line-height:1.2;color:var(--muted);display:flex;flex-direction:column;gap:3px}
.levels li::before{content:"";height:6px;border-radius:3px;background:var(--bar-track);display:block}
.levels li.done{color:var(--fg)} .levels li.done::before{background:var(--accent)}
.levels li span{overflow-wrap:anywhere}
.prose{max-width:68ch;display:flex;flex-direction:column;gap:8px}
.scen{display:grid;grid-template-columns:5.5rem minmax(0,1fr);gap:4px 12px;align-items:center}
.scen .nm{font-weight:700;text-transform:capitalize}
.scen .rng{position:relative;height:12px;background:var(--bar-track);border-radius:6px}
.scen .seg{position:absolute;top:0;bottom:0;background:var(--bar);border-radius:6px;min-width:6px}
.scen .txt{grid-column:2;font-size:.85rem}
.scen.bear .seg{background:var(--crit)}
.zones{display:flex;flex-direction:column;gap:6px;list-style:none;padding:0;margin:0}
.zones li{display:flex;gap:8px;align-items:center;font-size:.9rem}
.sw{width:14px;height:14px;border-radius:3px;flex:none;border:1.5px solid var(--fg)}
.sw.z-ideal{background:var(--good)} .sw.z-ok{background:var(--accent)} .sw.z-chase{background:var(--warn)} .sw.z-inv{background:var(--crit)}
.ladder{width:100%;height:auto;display:block}
.ladder .band-ideal{fill:var(--good)} .ladder .band-ok{fill:var(--accent)} .ladder .band-chase{fill:var(--warn)} .ladder .band-add{fill:var(--info)}
.ladder .axis{fill:var(--bar-track)} .ladder .now{fill:var(--fg);stroke:var(--fg)} .ladder .inv{stroke:var(--crit);stroke-width:3;fill:none}
.ev{display:flex;flex-direction:column;gap:6px;padding:12px 0;border-bottom:1px solid var(--line)}
.ev:last-child{border-bottom:0}
.ev p{overflow-wrap:anywhere}
details>summary{cursor:pointer;font-weight:600;padding:6px 0}
details.qa{border-top:1px solid var(--line);padding:4px 0}
.kv{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.kv .fact{background:var(--surface2);border-radius:8px;padding:10px 12px}
.log{padding-left:1.1rem;display:flex;flex-direction:column;gap:4px} .log li{overflow-wrap:anywhere}
@media (prefers-reduced-motion:no-preference){.tile,.navchips a,.btn{transition:border-color .15s,background .15s}}
"""

THEME_JS = """
(function(){var b=document.getElementById('theme-toggle');if(!b)return;var r=document.documentElement;
function cur(){var t=r.getAttribute('data-theme');if(t)return t;return(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light'}
function sync(){b.setAttribute('aria-pressed',cur()==='dark'?'true':'false');b.textContent=cur()==='dark'?'Light theme':'Dark theme'}
try{var s=localStorage.getItem('mblab-theme');if(s==='dark'||s==='light')r.setAttribute('data-theme',s)}catch(e){}
sync();b.addEventListener('click',function(){var n=cur()==='dark'?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem('mblab-theme',n)}catch(e){}sync()});})();
"""


def page(title: str, body: str) -> str:
    """Wrap body markup into a complete, self-contained document (no external resources)."""
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f"<title>{esc(title)}</title>\n<style>{CSS}</style>\n</head>\n<body>\n{body}\n<script>{THEME_JS}</script>\n</body>\n</html>\n"
    )


def theme_button() -> str:
    return '<button type="button" class="btn" id="theme-toggle" aria-pressed="false">Dark theme</button>'


def pill(label: str, tone: str = "neutral", title: str = "") -> str:
    t = f' title="{esc(title)}"' if title else ""
    return f'<span class="pill t-{slug(tone)}"{t}>{esc(label)}</span>'


def status_pill(status: str) -> str:
    lab, tone, meaning = STATUS.get(status, (str(status).replace("_", " ").capitalize() or "Unknown", "neutral", ""))
    return pill(lab, tone, meaning)


def entry_pill(state: str) -> str:
    lab, tone = ENTRY.get(state, ENTRY["unknown"])
    return pill(lab, tone)


def est(label: str = "Model estimate") -> str:
    return f'<span class="est">{esc(label)}</span>'


def empty(msg_strong: str, rest: str = "") -> str:
    return f'<div class="empty"><strong>{esc(msg_strong)}</strong>{(" " + esc(rest)) if rest else ""}</div>'


def score_bar(label: str, value: Any, dq: str = "ok", basis: str = "") -> str:
    v = num(value)
    tip = f' title="{esc(basis)}"' if basis else ""
    dqs = f' <span class="dq">({esc(dq)})</span>' if dq and dq != "ok" and v is not None else ""
    if v is None:
        return (f'<li class="bar na"{tip}><span class="lab"><span>{esc(label)}</span><span class="muted">not assessed</span></span>'
                f'<span class="track"></span><span class="val">n/a</span></li>')
    v = max(0.0, min(1.0, v))
    return (f'<li class="bar"{tip}><span class="lab"><span>{esc(label)}{dqs}</span></span>'
            f'<span class="track" role="img" aria-label="{esc(label)} {v:.2f} out of 1"><span class="fill" style="width:{v * 100:.0f}%"></span></span>'
            f'<span class="val">{v:.2f}</span></li>')
