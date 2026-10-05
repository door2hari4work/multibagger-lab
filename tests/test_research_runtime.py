"""Research runtime: freshness, thesis_builder, queue. No network."""
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from mblab import freshness as fr, store, thesis_builder as tb
from mblab.schema import Thesis, Evidence, Scenario, Catalyst, ExitTrigger, validate
from research import queue as rq

TODAY = date(2026, 10, 5)
ROOT = Path(__file__).resolve().parent.parent


def row(**kw):
    r = {"ticker": "abc", "market": "in", "company": "ABC Ltd", "price": 912.5, "price_ts": "2026-10-02", "rank": 3, "score": 0.81, "momentum_pct": 0.93, "signal": "momentum"}
    r.update(kw); return r


def deep_payload(**kw):
    ev = [{"id": f"e{i}", "claim": f"Disclosed figure {i}", "kind": "FACT", "source_type": t, "source_url": f"https://x/{i}", "source_date": "2026-09-20", "period": "Q1 FY27"}
          for i, t in ((10, "filing"), (11, "exchange"), (12, "call"))]
    ev.append({"id": "e13", "claim": "Margin expansion looks consistent with operating leverage", "kind": "INFERENCE", "note": "from e10,e11"})
    p = {"ticker": "ABC", "market": "IN", "company": "ABC Ltd", "research_level": 3, "status": "watchlist", "thesis": "The evidence suggests order growth is accelerating.",
         "risks": ["Customer concentration"], "evidence": ev,
         "base_case": {"description": "Growth continues", "multiple_low": 1.5, "multiple_high": 2.5, "probability": 0.5, "horizon_months": 18},
         "bear_case": {"description": "Orders slip", "multiple_low": 0.5, "multiple_high": 0.9, "probability": 0.3, "horizon_months": 18},
         "bull_case": {"description": "Margin and multiple expand", "multiple_low": 3, "multiple_high": 5, "probability": 0.2, "horizon_months": 18},
         "catalysts": [{"description": "Capacity commissioning", "window": "Q4 FY27", "evidence_ids": ["e10"]}],
         "exit_rules": [{"type": "thesis_invalidation", "condition": "order book falls below Rs 500 crore"}]}
    p.update(kw); return p


# ---------------------------------------------------------------- thesis_builder: snapshot
def test_snapshot_is_honest_and_valid():
    t = tb.build_from_candidate(row(), today=TODAY)
    assert (t.ticker, t.market, t.status, t.research_level, t.currency) == ("ABC", "IN", "research_required", 1, "INR")
    assert validate(t, today=TODAY) == []
    assert {e.source_type for e in t.evidence} == {"price", "model"} and all(e.kind == "FACT" for e in t.evidence)
    assert t.catalysts == [] and t.bull_case is None and t.base_case is None and t.bear_case is None and t.thesis == "" and t.multibagger_mechanism == ""
    assert t.overall_score is None and t.confidence == "low" and t.next_review == "2026-10-19"
    assert [s.name for s in t.scores] == ["market_confirmation"]


def test_snapshot_without_price_or_model_has_no_fake_evidence():
    t = tb.build_from_candidate({"symbol": "zzz", "market": "US"}, today=TODAY)
    assert t.evidence == [] and t.price is None and t.currency == "USD" and validate(t) == []
    with pytest.raises(ValueError): tb.build_from_candidate({"market": "US"})


def test_snapshot_saves_and_never_certainty_language(tmp_path):
    t = tb.build_from_candidate(row(), today=TODAY); store.save_new_version(t, base=tmp_path, today=TODAY)
    assert store.versions("IN", "ABC", base=tmp_path) == [1]


# ---------------------------------------------------------------- thesis_builder: deep assembly
def test_assemble_deep_thesis_valid_and_flags_model_estimate():
    t, problems = tb.assemble_deep_thesis(deep_payload(), today=TODAY)
    assert problems == [], problems
    assert t.base_case.probability_is_model_estimate and t.next_review == "2026-11-04" and t.as_of == "2026-10-05"
    assert t.disclaimer.startswith("Model estimates")


def test_assemble_rejects_unsourced_fact_certainty_and_overclaimed_level():
    p = deep_payload(); p["evidence"][0].pop("source_url")
    _, problems = tb.assemble_deep_thesis(p, today=TODAY); assert any("FACT needs" in x for x in problems)
    _, problems = tb.assemble_deep_thesis(deep_payload(thesis="This is guaranteed to work"), today=TODAY); assert any("certainty" in x for x in problems)
    p = deep_payload(); p["evidence"] = p["evidence"][:1]
    _, problems = tb.assemble_deep_thesis(p, today=TODAY); assert any("primary-source" in x for x in problems)
    _, problems = tb.assemble_deep_thesis(deep_payload(bogus_field=1), today=TODAY); assert any("unknown field" in x for x in problems)
    p = deep_payload(); p["base_case"]["probability_is_model_estimate"] = False
    _, problems = tb.assemble_deep_thesis(p, today=TODAY); assert any("model estimates" in x for x in problems)


def test_catalyst_without_evidence_is_a_problem():
    p = deep_payload(catalysts=[{"description": "Big order win"}])
    _, problems = tb.assemble_deep_thesis(p, today=TODAY); assert any("catalyst without evidence" in x for x in problems)


def test_evidence_merges_by_id_with_base_and_as_of_refreshes():
    base = tb.build_from_candidate(row(), today=TODAY)
    t, problems = tb.assemble_deep_thesis({"research_level": 2, "status": "watchlist", "as_of": "2026-10-04",
                                           "evidence": [{"kind": "FACT", "claim": "Revenue grew 31% YoY in Q1 FY27", "source_type": "exchange", "source_url": "https://x/r", "source_date": "2026-08-10", "period": "Q1 FY27"}]},
                                          base, today=TODAY)
    assert problems == [], problems
    assert [e.id for e in t.evidence] == ["e1", "e2", "e3"] and t.as_of == "2026-10-04" and t.ticker == "ABC"


def test_adversarial_unanswered_downgrades_and_kill_rejects():
    t, _ = tb.assemble_deep_thesis(deep_payload(), today=TODAY)
    full = {q: "A substantive answer citing e10 and the filing." for q in tb.ADVERSARIAL_QUESTIONS}
    assert len(tb.ADVERSARIAL_QUESTIONS) == 12 and tb.unanswered_questions(full) == []
    part = dict(full); part["is_it_crowded"] = "cannot answer: no ownership data"
    t1 = tb.apply_adversarial(Thesis.from_dict(t.to_dict()), {"verdict": "survives", "questions": part, "strongest_bear_case": "x"})
    assert t1.adversarial.verdict == "downgraded" and t1.confidence == "low"
    t2 = tb.apply_adversarial(Thesis.from_dict(t.to_dict()), {"verdict": "survives", "questions": full, "strongest_bear_case": "x"}); assert t2.adversarial.verdict == "survives"
    t3 = tb.apply_adversarial(Thesis.from_dict(t.to_dict()), {"verdict": "killed", "questions": full, "strongest_bear_case": "mechanism fails"})
    assert t3.status == "rejected" and validate(t3, today=TODAY) == []
    with pytest.raises(ValueError): tb.apply_adversarial(t, {"verdict": "maybe"})


def test_downgrade_removes_entry_status():
    t, _ = tb.assemble_deep_thesis(deep_payload(), today=TODAY)
    t.status, t.research_level = "accumulate", 4
    tb.apply_adversarial(t, {"verdict": "downgraded", "questions": {}, "strongest_bear_case": "x"})
    assert t.status == "watchlist" and validate(t, today=TODAY) == []


def test_save_payload_end_to_end_with_adversarial(tmp_path):
    saved, problems = tb.save_payload(deep_payload(), "level 3", base_dir=tmp_path, today=TODAY); assert problems == [] and saved.version == 1
    full = {q: "A substantive answer citing e10 and the filing." for q in tb.ADVERSARIAL_QUESTIONS}
    saved2, problems = tb.save_payload({"ticker": "ABC", "market": "IN", "research_level": 4}, "devil's advocate", base_dir=tmp_path, today=TODAY,
                                       adversarial={"verdict": "survives", "questions": full, "strongest_bear_case": "orders slip"})
    assert problems == [] and saved2.version == 2 and saved2.adversarial.verdict == "survives" and saved2.parent_version == 1
    assert len(saved2.evidence) == 4                        # evidence carried over, nothing dropped
    bad, problems = tb.save_payload({"ticker": "NEW", "market": "US"}, "x", base_dir=tmp_path, today=TODAY); assert bad is None and problems
    dry, problems = tb.save_payload(deep_payload(ticker="DRY"), "x", base_dir=tmp_path, today=TODAY, dry_run=True); assert problems == [] and store.versions("IN", "DRY", base=tmp_path) == []


# ---------------------------------------------------------------- freshness
def test_classify_age_thresholds():
    assert fr.classify_age(1, "price") == "fresh" and fr.classify_age(8, "price") == "aging" and fr.classify_age(30, "price") == "stale"
    assert fr.classify_age(60, "filing") == "fresh" and fr.classify_age(150, "filing") == "aging" and fr.classify_age(400, "filing") == "stale"
    assert fr.classify_age(None, "filing") == "unknown" and fr.classify_age(-3, "price") == "unknown"
    assert fr.age_days("2026-09-25", TODAY) == 10 and fr.age_days("garbage", TODAY) is None


def test_thesis_freshness_flags_stale_price_old_evidence_overdue_review():
    t, _ = tb.assemble_deep_thesis(deep_payload(price=900, price_ts="2026-08-01"), today=TODAY)
    f = fr.thesis_freshness(t, TODAY)
    assert f["price"]["freshness"] == "stale" and f["needs_refresh"] and any("price is stale" in r for r in f["reasons"])
    later = date(2027, 6, 1); f2 = fr.thesis_freshness(t, later)
    assert f2["review_overdue"] and "no current primary-source FACT" in f2["reasons"]
    assert fr.is_fresh_thesis(Thesis(ticker="A", company="A", market="US", created_at="2026-10-01T00:00:00+00:00"), TODAY)
    assert not fr.is_fresh_thesis(Thesis(ticker="A", company="A", market="US", created_at="2026-08-01T00:00:00+00:00"), TODAY)


def test_what_changed_since():
    t, _ = tb.assemble_deep_thesis(deep_payload(price=900, price_ts="2026-10-02", currency="INR", valuation={"pe_ttm": 30.0}, as_of="2026-09-30"), today=TODAY)
    cur = {"price": 1200, "price_ts": "2026-10-04", "currency": "INR", "valuation": {"pe_ttm": 41.0},
           "evidence": [{"id": "n1", "claim": "Q2 revenue missed guidance", "kind": "FACT", "source_type": "filing", "source_date": "2026-10-04"}],
           "events": [{"date": "2026-10-03", "type": "corporate_action", "summary": "1:2 stock split"}]}
    r = fr.what_changed_since(t, cur, TODAY)
    assert r["material"] and r["severity"] == "high"
    txt = " | ".join(r["changes"]); assert "+33.3%" in txt and "pe_ttm" in txt and "new FACT evidence n1" in txt and "stock split" in txt
    calm = fr.what_changed_since(t, {"price": 905, "price_ts": "2026-10-04", "currency": "INR", "evidence": [], "events": []}, TODAY)
    assert not calm["material"] and "valuation" in calm["not_checked"]
    assert "price" in fr.what_changed_since(t, {}, TODAY)["not_checked"]                  # missing data is "not checked", never "no change"
    mism = fr.what_changed_since(t, {"price": 10, "currency": "USD", "price_ts": "2026-10-04"}, TODAY); assert any("currency mismatch" in c for c in mism["changes"])


def test_changes_since_version_loads_from_store(tmp_path):
    tb.save_payload(deep_payload(price=900, price_ts="2026-10-02"), "l3", base_dir=tmp_path, today=TODAY)
    r = fr.changes_since_version("IN", "ABC", 1, {"price": 1100, "price_ts": "2026-10-04"}, base=tmp_path, today=TODAY); assert r["material"] and r["since_version"] == 1
    with pytest.raises(LookupError): fr.changes_since_version("IN", "NOPE", 1, {}, base=tmp_path)


# ---------------------------------------------------------------- queue
def write_cands(d, name, rows): (d / name).write_text(json.dumps(rows))


def test_queue_build_priority_cap_and_skip_fresh(tmp_path):
    rd, th = tmp_path / "r", tmp_path / "theses"; rd.mkdir()
    write_cands(rd, "candidates_in.json", {"as_of": "2026-10-05", "candidates": [
        {"ticker": "C", "market": "IN", "rank": 3}, {"ticker": "A", "market": "IN", "rank": 1}, {"ticker": "B", "market": "IN", "rank": 2}, {"ticker": "D", "market": "IN", "rank": 4}]})
    write_cands(rd, "candidates_us.json", [{"symbol": "x", "market": "US", "score": 0.2}, {"symbol": "y", "market": "US", "score": 0.9}, {"market": "US"}])   # row without ticker ignored
    (rd / "candidates_bad.json").write_text("{not json")
    cands = rq.load_candidates(rd)
    assert [c["ticker"] for c in cands if c["market"] == "IN"] == ["A", "B", "C", "D"] and [c["ticker"] for c in cands if c["market"] == "US"] == ["Y", "X"]
    # B has a fresh, adversarially-reviewed thesis -> skipped
    t, _ = tb.assemble_deep_thesis(deep_payload(ticker="B"), today=TODAY)
    full = {q: "A substantive answer citing e10 and the filing." for q in tb.ADVERSARIAL_QUESTIONS}; tb.apply_adversarial(t, {"verdict": "survives", "questions": full, "strongest_bear_case": "x"}, TODAY)
    t.research_level = 4; store.save_new_version(t, base=th, today=TODAY)
    q = rq.build_queue(cands, {"version": 1, "tasks": []}, today=TODAY, cap=3, theses_base=th)
    ids = [x["ticker"] for x in q["tasks"]]
    assert len(ids) == 3 and "B" not in ids and ids[0] in ("A", "Y") and all(x["type"] == "level2_qualifier" for x in q["tasks"])
    assert any(s["ticker"] == "B" and "fresh" in s["reason"] for s in q["last_build"]["skipped"])
    # rebuilding does not duplicate open tasks
    rq.build_queue(cands, q, today=TODAY, cap=10, theses_base=th)
    keys = [(x["type"], x["market"], x["ticker"]) for x in q["tasks"]]; assert len(keys) == len(set(keys))


def test_decide_task_ladder():
    d = lambda t: rq.decide_task(t, TODAY)[0]
    assert d(None) == "level2_qualifier"
    snap = tb.build_from_candidate(row(), today=TODAY); assert d(snap) == "level2_qualifier"            # snapshot's next_review is not "freshness"
    l2 = Thesis.from_dict({**snap.to_dict(), "research_level": 2}); assert d(l2) == "level3_deep_dive"
    l3, _ = tb.assemble_deep_thesis(deep_payload(), today=TODAY); l3.created_at = "2026-10-04T00:00:00+00:00"; assert d(l3) == "devils_advocate"
    tb.apply_adversarial(l3, {"verdict": "downgraded", "questions": {}, "strongest_bear_case": "x"}); assert d(l3) is None
    l3.created_at = "2026-06-01T00:00:00+00:00"; assert rq.decide_task(l3, TODAY)[:2] == ("level3_deep_dive", "refresh")
    l3.status = "rejected"; assert d(l3) is None


def test_queue_next_mark_done_cooldown_and_reopen(tmp_path):
    rd = tmp_path; write_cands(rd, "candidates_a.json", [{"ticker": "A", "market": "US"}, {"ticker": "B", "market": "US"}])
    q = rq.build_queue(rq.load_candidates(rd), {"version": 1, "tasks": []}, today=TODAY, cap=5, theses_base=tmp_path / "t")
    first = rq.next_tasks(q, 1)[0]; assert first["ticker"] == "A"
    rq.mark(q, first["id"], "in_progress", today=TODAY); assert [t["ticker"] for t in rq.next_tasks(q, 5)] == ["B"]
    rq.mark_done(q, first["id"], "saved v1", today=TODAY); assert first["status"] == "done" and first["finished_at"] == "2026-10-05"
    # cooldown: same type for A is not re-queued right after an attempt (thesis still missing in this test)
    q2 = rq.build_queue(rq.load_candidates(rd), q, today=TODAY, cap=5, theses_base=tmp_path / "t")
    assert sum(1 for t in q2["tasks"] if t["ticker"] == "A") == 1
    stale = rq.mark(q, "level2_qualifier:US:B:2026-10-05", "in_progress", today=date(2026, 10, 1)); assert rq.reopen_stale(q, TODAY) == [stale["id"]] and stale["status"] == "pending"
    with pytest.raises(KeyError): rq.mark(q, "nope", "done")
    with pytest.raises(ValueError): rq.mark(q, first["id"], "weird")


def test_queue_roundtrip_log_and_cli_script_does_not_shadow_stdlib(tmp_path):
    p = tmp_path / "queue.json"; assert rq.load_queue(p) == {"version": 1, "tasks": []}
    q = {"version": 1, "tasks": [{"id": "t1", "type": "level2_qualifier", "ticker": "A", "market": "US"}]}; rq.save_queue(q, p); assert rq.load_queue(p) == q
    log = tmp_path / "log.md"; rq.append_log(q["tasks"][0], "blocked: EDGAR unreachable", "blocked", "sec.gov", log_path=log, today=TODAY); rq.append_log(q["tasks"][0], "ok", "done", thesis_version=2, log_path=log, today=TODAY)
    s = log.read_text(); assert s.startswith("# Research log") and "blocked: EDGAR unreachable" in s and "thesis version saved: v2" in s and s.count("## 2026-10-05") == 2
    r = subprocess.run([sys.executable, str(ROOT / "research" / "queue.py"), "show"], capture_output=True, text=True, cwd=ROOT); assert r.returncode == 0, r.stderr


# ---------------------------------------------------------------- prompts
ROLES = ["level2_qualifier", "level3_deep_dive", "devils_advocate", "source_reliability", "monitoring_agent", "weekly_digest", "ai_value_chain_mapper"]


def test_every_role_prompt_exists_and_embeds_common_rules():
    common = (ROOT / "research/prompts/_common_rules.md").read_text().split("\n", 1)[1].strip()
    for r in ROLES:
        s = (ROOT / f"research/prompts/{r}.md").read_text()
        assert common in s, r
        assert "NEVER evidence" in s and "disclaimer" in s.lower()


def test_devils_advocate_lists_all_12_question_keys_and_kill_authority():
    s = (ROOT / "research/prompts/devils_advocate.md").read_text()
    assert all(f"`{q}`" in s for q in tb.ADVERSARIAL_QUESTIONS) and "KILL" in s and "downgrade" in s
    assert "AI spend slows" in (ROOT / "research/prompts/ai_value_chain_mapper.md").read_text()
    assert "SEC_CONTACT" in (ROOT / "research/prompts/level3_deep_dive.md").read_text()
    for f in ("PLAYBOOK.md", "log.md", "queue.json"): assert (ROOT / "research" / f).exists()
