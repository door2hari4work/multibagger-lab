"""UI tests: builds from fixtures, required sections, escaping, no external resources, empty states."""
import re
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import date
from html.parser import HTMLParser

from mblab.schema import Thesis, Evidence, Catalyst, Scenario, ExitTrigger, DISCLAIMER, validate
from ui.today import build_today
from ui.opportunity import build_opportunity
from ui.fixtures import sample_data as fx
from ui import build as ui_build

XSS = "<script>alert(1)</script>"


def _today(**kw):
    args = dict(theses=fx.sample_theses(), alerts=fx.sample_alerts(), candidates=fx.sample_candidates(), portfolio_summary=fx.sample_portfolio_summary(),
                paper_status=fx.sample_paper_status(), as_of=fx.SAMPLE_AS_OF)
    args.update(kw)
    return build_today(**args)


def test_fixtures_are_valid_theses():
    for t in fx.sample_theses():
        assert validate(t, today=date.fromisoformat(fx.SAMPLE_AS_OF)) == [], t.ticker
        assert "(sample)" in t.company


def test_today_builds_with_required_sections():
    h = _today(sample=True)
    assert h.startswith("<!doctype html>") and "<title>MultibaggerLab Today</title>" in h
    for needle in ["What deserves your attention today", "High-priority ideas", "Theses changed", "Entry setups improved", "Exit conditions triggered", "New discoveries",
                   "Alerts", "Opportunities, ranked", "Paper-trading books", "What the lab has and has not proven", "Survivor bias", "Forward tracking only", "Not advice",
                   DISCLAIMER, "Model estimate", "Sample data"]:
        assert needle in h, needle
    assert "Quillon Grid Systems" in h and 'class="bar' in h and "Upside range and timeframe" in h and "Portfolio fit" in h and "Why now" in h
    assert "NAV vs benchmark" in h and "Drawdown" in h and "Regime" in h


def test_today_counts_from_fixtures():
    h = _today()
    tiles = re.findall(r'<span class="n[^"]*">(\d+)</span><span class="l">([^<]+)</span>', h)
    d = {l: int(n) for n, l in tiles}
    assert d["High-priority ideas"] == 2          # QGRD attractive_entry, VLDM preparing_to_enter
    assert d["Exit conditions triggered"] == 2    # KLNR trim (+triggered rule), BRXT thesis_broken
    assert d["Theses changed"] >= 3 and d["Entry setups improved"] == 1
    assert d["New discoveries"] == 4              # 3 candidates + MRWL early discovery created this week


def test_opportunity_page_has_master_structure():
    for t in fx.sample_theses():
        h = build_opportunity(t, sample=True)
        for sid in ["why", "mechanism", "rerating", "inflection", "valuation", "moat", "catalysts", "entry", "bear", "wrong", "fit", "monitor", "evidence", "history"]:
            assert f'id="{sid}"' in h, (t.ticker, sid)
        assert DISCLAIMER in h and "Sample data" in h
    q = build_opportunity(next(t for t in fx.sample_theses() if t.ticker == "QGRD"))
    for chip in ["k-FACT", "k-INFERENCE", "k-SPECULATION"]:
        assert chip in q
    assert "source date 2026-09-18" in q and "Ideal zone" in q and "Invalidation" in q and "<svg" in q and "MODEL ESTIMATE".lower() in q.lower()
    assert "Certain" not in q and "guaranteed" not in q.lower()


def test_level1_empty_states_are_plain():
    t = next(t for t in fx.sample_theses() if t.ticker == "MRWL")
    h = build_opportunity(t)
    assert "Level 1 discovery only: no deep research yet." in h
    assert "No entry zones yet." in h and "Not assessed." in h and "Adversarial review not done." in h


def _evil() -> Thesis:
    t = fx.sample_theses()[0]
    e = XSS
    t.company = e + '"><img src=x onerror=alert(2)>'
    t.ticker = e; t.why_now = e; t.thesis = e; t.multibagger_mechanism = e; t.expectations_gap = e
    t.risks = [e]; t.entry.rationale = e; t.portfolio_fit.summary = e; t.portfolio_fit.overlap_notes = [e]; t.confidence = e; t.status = e; t.entry.state = e; t.currency = e
    t.catalysts = [Catalyst(e, e, e, [e])]; t.exit_rules = [ExitTrigger(e, e, e)]
    t.bull_case = Scenario(e, e, 2, 3, 0.2, 12); t.adversarial.strongest_bear_case = e; t.adversarial.questions = {e: e}; t.adversarial.reviewer = e
    t.evidence = [Evidence(e, e, e, e, "javascript:alert(3)", e, e, "", e), Evidence("x2", e, "FACT", "filing", e + "https://ok.example/", e)]
    t.valuation = {e: e}; t.change_log = [e]; t.next_review = e; t.as_of = e; t.price_ts = e
    t.scores[0].basis = e; t.scores[0].name = "business_quality"
    return t


def test_xss_is_escaped_everywhere():
    t = _evil()
    pages = [build_opportunity(t, assessment={"headline": XSS, "bullets": [XSS]}, portfolio_fit={"summary": XSS, "overlap_notes": [XSS], "score": 0.5}, history=[t]),
             _today(theses=[t], alerts=[{"severity": XSS, "title": XSS, "detail": XSS, "ticker": XSS}], candidates=[{"ticker": XSS, "name": XSS, "note": XSS}],
                    portfolio_summary={"notes": [XSS], "currency": XSS}, paper_status={"books": [{"name": XSS, "regime": XSS, "nav": XSS, "flags": XSS}], "note": XSS}, as_of=XSS,
                    opportunity_href=lambda th: "javascript:alert(4)")]
    for h in pages:
        assert "<script>alert" not in h and "<img src=x" not in h
        assert "&lt;script&gt;alert(1)&lt;/script&gt;" in h
        assert 'href="javascript:' not in h.lower()
        assert h.count("<script>") == 1  # only the theme toggle
    assert "&lt;img src=x onerror" in pages[0] or "&quot;&gt;&lt;img" in pages[0]


class _Res(HTMLParser):
    def __init__(self): super().__init__(); self.bad = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and "src" in a and not a["src"].startswith("https://cdnjs.cloudflare.com/"): self.bad.append(a["src"])
        if tag in ("img", "iframe", "embed", "object", "video", "audio", "source") and re.match(r"^(https?:)?//", a.get("src", "")): self.bad.append(a["src"])
        if tag == "link": self.bad.append(a.get("href", "link"))


def test_no_external_resources():
    pages = [_today(), *[build_opportunity(t) for t in fx.sample_theses()]]
    for h in pages:
        p = _Res(); p.feed(h)
        assert p.bad == []
        assert "@import" not in h and not re.search(r"url\(\s*['\"]?(https?:)?//", h)
        assert "fonts.googleapis" not in h


def test_empty_store_and_none_inputs():
    h = build_today([], [], [], None, None, "2026-10-05")
    for needle in ["No opportunities to rank yet.", "No alerts today.", "No new discoveries today.", "No portfolio loaded.", "Paper books not connected.", DISCLAIMER]:
        assert needle in h, needle
    assert "Sample data" not in h
    assert 'class="n">0<' in h


def test_theme_tokens_and_a11y_basics():
    h = _today()
    assert 'prefers-color-scheme:dark' in h and ':root[data-theme="dark"]' in h and "background:var(--bg)" in h
    assert 'name="viewport"' in h and 'lang="en"' in h and ":focus-visible" in h and "padding-inline:16px" in h


def test_build_writes_files_from_fixtures_when_store_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(ui_build.store, "latest_all", lambda base=None: [])
    p = ui_build.build(tmp_path)
    assert p.name == "today.html" and p.exists()
    h = p.read_text()
    assert "Sample data" in h and 'href="opportunity/US_QGRD.html"' in h
    assert (tmp_path / "opportunity" / "US_QGRD.html").exists()


def test_build_uses_real_store_when_present(tmp_path, monkeypatch):
    real = replace(fx.sample_theses()[0], company="Real Co")
    monkeypatch.setattr(ui_build.store, "latest_all", lambda base=None: [real])
    monkeypatch.setattr(ui_build.store, "versions", lambda m, t, base=None: [1])
    monkeypatch.setattr(ui_build.store, "load", lambda m, t, v=None, base=None: real)
    h = ui_build.build(tmp_path).read_text()
    assert "Real Co" in h and "Sample data" not in h
