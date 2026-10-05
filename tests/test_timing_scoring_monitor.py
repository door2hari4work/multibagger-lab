"""Synthetic-data tests for mblab.timing / scoring / monitor. No network, no real prices."""
from datetime import date, timedelta
import numpy as np
import pandas as pd
import pytest

from mblab import timing, scoring, monitor
from mblab.schema import (ScoreComponent, Scenario, Thesis, EntryPlan, ExitTrigger, Catalyst, Evidence, Status, EntryState)


# ------------------------------------------------------------------------------------------------------------- synthetic prices
def frame(close, vol=None, spread=0.012, start="2024-01-01"):
    close = np.asarray(close, float)
    idx = pd.bdate_range(start, periods=len(close))
    return pd.DataFrame({"Close": close, "High": close * (1 + spread), "Low": close * (1 - spread),
                         "Volume": np.full(len(close), 1e6) if vol is None else vol}, index=idx)


def uptrend(n=300, g=0.003, p0=100.0):
    return p0 * np.exp(g * np.arange(n))


def pullback_df():
    """Strong uptrend then an ~8% pullback that lands near the 50d MA."""
    up = uptrend(300, 0.003)
    pb = up[-1] * np.exp(np.linspace(0, np.log(0.92), 12))
    return frame(np.concatenate([up, pb]))


def base_breakout_df(vol_mult):
    up = uptrend(260, 0.004)                                         # advance
    base = up[-1] * (1 + 0.03 * np.sin(np.linspace(0, 6 * np.pi, 70)))  # 70-day base, +/-3%
    brk = base[-1] * np.exp(np.cumsum([0.02, 0.012, 0.01, 0.0, 0.0]))   # breakout over the base high
    close = np.concatenate([up, base, brk])
    vol = np.full(len(close), 1e6); vol[-5:] = 1e6 * vol_mult
    return frame(close, vol=vol)


# ------------------------------------------------------------------------------------------------------------- timing
def test_tick_and_rounding():
    assert timing.tick_for(0.5) == 0.01 and timing.tick_for(12) == 0.10 and timing.tick_for(80) == 0.5 and timing.tick_for(2500) == 10 and timing.tick_for(9000) == 50
    z = timing.round_zone(81.23, 83.71, 0.5)
    assert z == [81.0, 84.0]
    assert timing.round_zone(10.0, 10.0, 0.1)[1] > 10.0       # never a zero-width zone


def test_attractive_pullback_in_uptrend():
    a = timing.assess(pullback_df(), regime_on=True)
    assert a.state == "attractive_entry", (a.state, a.metrics)
    lo, hi = a.ideal_zone
    assert lo < hi and a.acceptable_zone[0] <= lo and a.acceptable_zone[1] >= hi
    assert a.chase_zone[0] >= a.acceptable_zone[1] - 1e-9
    assert a.invalidation_price < lo
    t = timing.tick_for(a.metrics["close"])
    for v in (lo, hi, a.acceptable_zone[0], a.acceptable_zone[1], a.chase_zone[0], a.chase_zone[1], a.invalidation_price):
        assert abs(v / t - round(v / t)) < 1e-6, (v, t)         # rounded to the tick
    assert "ATR" in a.rationale and "50d MA" in a.rationale and "rounded" in a.rationale
    plan = a.to_entry_plan()
    assert plan.state == "attractive_entry" and plan.ideal_zone == a.ideal_zone


def test_regime_off_defers_actionable_states_but_records_raw_state():
    a = timing.assess(pullback_df(), regime_on=False)
    assert a.state == "setup_forming" and a.metrics["raw_state"] == "attractive_entry" and a.metrics["regime_downgraded"]
    assert "regime" in a.rationale.lower()


def test_overextended_vertical_move():
    up = uptrend(300, 0.003)
    spike = up[-1] * np.exp(np.cumsum(np.full(15, 0.02)))          # +35% in 15 days
    a = timing.assess(frame(np.concatenate([up, spike])), regime_on=True)
    assert a.state == "overextended", (a.state, a.metrics)
    assert a.metrics["ext_atr"] >= timing.TH["ext_over"] or a.metrics["ext_pct"] >= timing.TH["ext_pct_over"]


def test_downtrend_is_too_early_with_no_zones():
    a = timing.assess(frame(uptrend(300, -0.003, 400)), regime_on=True)
    assert a.state == "too_early"
    assert a.ideal_zone is None and a.chase_zone is None and a.invalidation_price is None
    assert "200d MA" in a.rationale


def test_thesis_not_ok_overrides_everything():
    a = timing.assess(pullback_df(), regime_on=True, thesis_ok=False)
    assert a.state == "thesis_deteriorating" and a.ideal_zone is None


def test_short_history_is_unknown_not_guessed():
    a = timing.assess(frame(uptrend(120)), regime_on=True)
    assert a.state == "unknown" and a.ideal_zone is None


def test_breakout_needs_volume_confirmation_when_volume_exists():
    ok = timing.assess(base_breakout_df(2.5), regime_on=True)
    weak = timing.assess(base_breakout_df(1.0), regime_on=True)
    assert ok.state == "breakout_entry", (ok.state, ok.metrics, ok.rationale)
    assert ok.metrics["volume_confirmed"] is True
    assert weak.state == "wait_for_pullback" and weak.metrics["volume_confirmed"] is False
    assert "volume" in weak.rationale.lower()


def test_breakout_without_volume_data_is_flagged_unverified():
    df = base_breakout_df(2.5).drop(columns=["Volume"])
    a = timing.assess(df, regime_on=True)
    assert a.state == "breakout_entry" and a.metrics["volume_confirmed"] is None and "UNVERIFIED" in a.rationale


def test_close_only_and_lowercase_columns_work():
    df = pullback_df()[["Close"]].rename(columns=str.lower)
    a = timing.assess(df, regime_on=True)
    assert a.state in {s.value for s in EntryState} and a.metrics["rows"] == len(df)
    with pytest.raises(ValueError): timing.assess(pd.DataFrame({"x": [1, 2, 3]}), True)


def test_no_lookahead_features():
    df = pullback_df()
    full = timing.compute_features(df)
    part = timing.compute_features(df.iloc[:-20])
    pd.testing.assert_frame_equal(full.iloc[:-20], part, check_exact=False, atol=1e-9)


def test_classify_matches_assess():
    df = pullback_df()
    f = timing.compute_features(df).iloc[-1].to_dict()
    assert timing.classify(f, True)[0] == timing.assess(df, True).state


def test_every_state_value_is_a_schema_entry_state():
    valid = {s.value for s in EntryState}
    assert set(timing.ENTRY_RANK) <= valid
    for df in (pullback_df(), base_breakout_df(2.5), frame(uptrend(300, -0.003, 400))):
        assert timing.assess(df, True).state in valid


# ------------------------------------------------------------------------------------------------------------- scoring
def comps(names_values, **kw):
    return [ScoreComponent(n, v, **kw) for n, v in names_values.items()]


FULL = {k: 0.6 for k in scoring.DEFAULT_WEIGHTS}


def test_default_weights_declared_and_sum_to_one():
    assert set(scoring.DEFAULT_WEIGHTS) == {"business_quality", "growth_acceleration", "earnings_inflection", "tam_expansion", "catalyst_strength", "competitive_advantage",
                                            "valuation_asymmetry", "market_confirmation", "timing", "risk", "thesis_robustness", "portfolio_fit"}
    assert abs(sum(scoring.DEFAULT_WEIGHTS.values()) - 1) < 1e-9


def test_full_assessment_high_confidence_and_exact_average():
    r = scoring.compute(comps(FULL))
    assert r.overall == pytest.approx(0.6) and r.confidence == "high" and r.coverage == pytest.approx(1.0)
    assert sum(c["share"] for c in r.contributions) == pytest.approx(1, abs=1e-3)


def test_reweights_over_assessed_only_and_never_imputes():
    vals = {"business_quality": 0.9, "growth_acceleration": 0.5, "valuation_asymmetry": 0.3, "risk": 0.7, "catalyst_strength": 0.4, "timing": None, "portfolio_fit": None}
    r = scoring.compute(comps(vals))
    w = scoring.DEFAULT_WEIGHTS
    used = [k for k, v in vals.items() if v is not None]
    expect = sum(w[k] * vals[k] for k in used) / sum(w[k] for k in used)
    assert r.overall == pytest.approx(expect, abs=1e-4)
    assert "timing" in r.missing and "portfolio_fit" in r.missing and "timing" not in r.assessed
    # a missing component is not the same as a 0.5 or a 0
    vals2 = dict(vals); vals2["timing"] = 0.0
    assert scoring.compute(comps(vals2)).overall < r.overall


def test_fewer_than_five_components_caps_confidence_low_with_reason():
    r = scoring.compute(comps({"growth_acceleration": 0.9, "valuation_asymmetry": 0.9, "risk": 0.9, "business_quality": 0.9}))
    assert r.confidence == "low" and any("only 4" in x for x in r.confidence_reasons) and r.overall == pytest.approx(0.9)


def test_missing_key_component_caps_confidence_low():
    v = dict(FULL); v["valuation_asymmetry"] = None
    r = scoring.compute(comps(v))
    assert r.confidence == "low" and r.missing_key == ["valuation_asymmetry"] and any("valuation_asymmetry" in x for x in r.confidence_reasons)
    v = dict(FULL); v["risk"] = None
    assert scoring.compute(comps(v)).confidence == "low"


def test_missing_data_quality_is_excluded_and_stale_is_discounted():
    c = comps(FULL); c[0] = ScoreComponent("business_quality", 0.1, data_quality="missing")
    r = scoring.compute(c)
    assert "business_quality" not in r.assessed and r.overall == pytest.approx(0.6)
    c = comps(FULL); c[0] = ScoreComponent("business_quality", 0.0, data_quality="stale")
    r2 = scoring.compute(c)
    assert 0.5 < r2.overall < 0.6 and any("stale" in x for x in r2.confidence_reasons)


def test_nothing_assessed_gives_none_not_zero():
    r = scoring.compute([ScoreComponent("timing", None)])
    assert r.overall is None and r.confidence == "low"
    assert scoring.compute([]).overall is None


def test_custom_weights_and_validation_errors():
    r = scoring.compute(comps({"a": 1.0, "b": 0.0}), weights={"a": 3, "b": 1})
    assert r.overall == pytest.approx(0.75)
    with pytest.raises(ValueError): scoring.compute([ScoreComponent("timing", 1.5)])
    with pytest.raises(ValueError): scoring.compute([ScoreComponent("timing", 0.5), ScoreComponent("timing", 0.4)])
    with pytest.raises(ValueError): scoring.compute([ScoreComponent("a", 0.5)], weights={"a": -1})


def test_dimensions_asymmetry_only_with_probabilities():
    sc = [Scenario("bull", "x", 4.0, 6.0, 0.25), Scenario("base", "x", 1.5, 2.0, 0.45), Scenario("bear", "x", 0.4, 0.6, 0.30)]
    d = scoring.dimensions(comps({"timing": 0.7, "risk": 0.4, "portfolio_fit": 0.5}), sc, timing_state="attractive_entry")
    assert d["asymmetry"]["model_estimate"] is True
    assert d["asymmetry"]["expected_multiple"] == pytest.approx(0.25 * 5 + 0.45 * 1.75 + 0.30 * 0.5, abs=1e-3)
    assert d["asymmetry"]["p_loss"] == pytest.approx(0.30)
    assert d["timing"]["state"] == "attractive_entry" and d["fit"]["score"] == 0.5 and d["downside"]["bear_multiple"] == [0.4, 0.6]
    # a 20x with a tiny probability stays visible as its own dimension and does not silently hide
    d2 = scoring.dimensions([], [Scenario("bull", "x", 20, 20, 0.02), Scenario("base", "x", 1.0, 1.2, 0.58), Scenario("bear", "x", 0.5, 0.7, 0.40)])
    assert d2["upside"]["bull_multiple"] == [20, 20] and d2["probability"]["bull"] == 0.02


def test_dimensions_refuses_asymmetry_without_probabilities_or_bad_sum():
    d = scoring.dimensions([], [Scenario("bull", "x", 4, 6), Scenario("bear", "x", 0.5, 0.7, 0.5)])
    assert d["asymmetry"] is None and "no probability" in d["asymmetry_unavailable_because"]
    d = scoring.dimensions([], [Scenario("bull", "x", 4, 6, 0.9), Scenario("bear", "x", 0.5, 0.7, 0.5)])
    assert d["asymmetry"] is None and "sum" in d["asymmetry_unavailable_because"]
    assert scoring.dimensions([], None)["asymmetry"] is None


# ------------------------------------------------------------------------------------------------------------- monitor
TODAY = "2026-10-05"


def thesis(**kw):
    t = Thesis(ticker="ABC", company="ABC Ltd", market="IN", status=kw.pop("status", Status.WATCHLIST.value), research_level=5,
               evidence=[Evidence(id="e1", claim="rev +30%", kind="FACT", source_type="filing", source_url="https://x", source_date="2026-09-01")], price=100.0)
    for k, v in kw.items(): setattr(t, k, v)
    return t


def snap(df=None, **kw): return monitor.Snapshot(as_of=TODAY, ohlcv=df, **kw)


def kinds(alerts): return {a.kind for a in alerts}


def test_empty_snapshot_does_not_crash_or_invent_alerts():
    assert monitor.evaluate(thesis(), snap()) == []


def test_invalidation_breach_is_critical():
    t = thesis(status=Status.HOLD.value); t.entry = EntryPlan(invalidation_price=95.0)
    al = monitor.evaluate(t, snap(price=90.0))
    assert al[0].kind == "invalidation_breached" and al[0].severity == "critical" and "95" in al[0].reason
    assert not monitor.evaluate(t, snap(price=96.0))


def test_entry_zone_entered_only_on_transition():
    t = thesis(); t.entry = EntryPlan(ideal_zone=[100.0, 110.0])
    idx = pd.bdate_range(end=TODAY, periods=3)
    entered = pd.DataFrame({"Close": [120.0, 112.0, 105.0]}, index=idx)
    inside_before = pd.DataFrame({"Close": [105.0, 106.0, 105.0]}, index=idx)
    assert "entry_zone_entered" in kinds(monitor.evaluate(t, snap(entered)))
    assert "entry_zone_entered" not in kinds(monitor.evaluate(t, snap(inside_before)))


def test_entry_state_improved_and_deteriorated():
    df = pullback_df()
    t = thesis(); t.entry = EntryPlan(state="setup_forming")
    s = monitor.Snapshot(as_of=str(df.index[-1].date()), ohlcv=df)
    al = monitor.evaluate(t, s)
    imp = [a for a in al if a.kind == "entry_state_improved"]
    assert imp and imp[0].severity == "high" and imp[0].data["new"] == "attractive_entry"
    t2 = thesis(status=Status.ACCUMULATE.value); t2.entry = EntryPlan(state="attractive_entry")
    s2 = monitor.Snapshot(as_of=str(df.index[-1].date()), ohlcv=frame(uptrend(300, -0.003, 400)))
    det = [a for a in monitor.evaluate(t2, s2) if a.kind == "entry_state_deteriorated"]
    assert det and det[0].data["new"] == "too_early" and det[0].severity == "medium"
    t3 = thesis(); t3.entry = EntryPlan(state="attractive_entry")      # unchanged -> no state alert
    assert not [a for a in monitor.evaluate(t3, s) if a.kind.startswith("entry_state")]


def test_numeric_exit_triggers_fire_and_text_triggers_are_ignored():
    t = thesis(status=Status.HOLD.value)
    t.exit_rules = [ExitTrigger("technical", "price below 90"), ExitTrigger("earnings_deterioration", "ebitda_margin < 12%"),
                    ExitTrigger("thesis_invalidation", "order book falls materially"), ExitTrigger("target", "price > 300")]
    al = monitor.evaluate(t, snap(price=85.0, fundamentals={"ebitda_margin": 0.10}))
    ex = [a for a in al if a.kind == "exit_trigger_met"]
    assert {a.data["metric"] for a in ex} == {"price", "ebitda_margin"}
    assert {a.severity for a in ex} == {"high", "critical"}
    assert not [a for a in monitor.evaluate(t, snap(price=150.0, fundamentals={"ebitda_margin": 0.20})) if a.kind == "exit_trigger_met"]
    t.exit_rules[0].status = "triggered"                               # already known: not re-alerted
    assert "price" not in {a.data["metric"] for a in monitor.evaluate(t, snap(price=85.0)) if a.kind == "exit_trigger_met"}


def test_parse_condition_and_window():
    assert monitor.parse_condition("close below 120") == ("close", "<", 120.0)
    assert monitor.parse_condition("drawdown_from_entry < -30%") == ("drawdown_from_entry", "<", -0.30)
    assert monitor.parse_condition("order book weakens") is None
    assert monitor.parse_window("Q4 FY27 results (Feb 2027)") == date(2027, 2, 28)
    assert monitor.parse_window("by 2026-12-15") == date(2026, 12, 15)
    assert monitor.parse_window("sometime soon") is None


def test_catalyst_window_passed_without_update():
    t = thesis(); t.catalysts = [Catalyst("Capacity ramp", window="Aug 2026"), Catalyst("Big order", window="Mar 2027"), Catalyst("Done", window="Jul 2026", status="occurred")]
    al = [a for a in monitor.evaluate(t, snap()) if a.kind == "catalyst_overdue"]
    assert len(al) == 1 and al[0].data["catalyst"] == "Capacity ramp"


def test_evidence_staleness_over_120_days():
    t = thesis(status=Status.ACCUMULATE.value)
    assert "evidence_stale" not in kinds(monitor.evaluate(t, snap()))
    old = monitor.Snapshot(as_of=str(date(2026, 9, 1) + timedelta(days=121)))
    al = [a for a in monitor.evaluate(t, old) if a.kind == "evidence_stale"]
    assert al and al[0].severity == "high"


def test_valuation_excess_vs_thesis():
    t = thesis(valuation={"pe_ttm": 20.0, "ev_sales": 4.0, "revenue_cagr": 0.3})
    al = monitor.evaluate(t, snap(fundamentals={"pe_ttm": 42.0, "ev_sales": 4.4, "revenue_cagr": 9}))
    v = [a for a in al if a.kind == "valuation_excess"]
    assert len(v) == 1 and v[0].data["metric"] == "pe_ttm" and v[0].severity == "high"


def test_dead_theses_do_not_generate_entry_or_invalidation_alerts():
    t = thesis(status=Status.THESIS_BROKEN.value); t.entry = EntryPlan(invalidation_price=95.0, ideal_zone=[80, 90])
    assert not [a for a in monitor.evaluate(t, snap(price=85.0)) if a.kind in ("invalidation_breached", "entry_zone_entered")]


def test_dedup_cooldown_and_escalation():
    t = thesis(status=Status.HOLD.value); t.entry = EntryPlan(invalidation_price=95.0)
    a1 = monitor.evaluate(t, snap(price=90.0))
    fresh, supp = monitor.filter_new(a1, [], TODAY)
    assert len(fresh) == 1 and not supp
    log = monitor.record([], fresh, TODAY)
    # next day, same condition: suppressed
    f2, s2 = monitor.filter_new(a1, log, date(2026, 10, 6))
    assert not f2 and len(s2) == 1
    # after the critical cooldown (2 days) it may repeat; medium alerts wait a week
    f3, _ = monitor.filter_new(a1, log, date(2026, 10, 7))
    assert len(f3) == 1
    med = monitor.Alert("ABC", "IN", "k", "medium", "r", "IN:ABC:k")
    logm = [dict(key="IN:ABC:k", severity="medium", ts="2026-10-05")]
    assert not monitor.filter_new([med], logm, date(2026, 10, 10))[0]
    assert monitor.filter_new([med], logm, date(2026, 10, 12))[0]
    # escalation bypasses cooldown
    high = monitor.Alert("ABC", "IN", "k", "high", "r", "IN:ABC:k")
    assert monitor.filter_new([high], logm, date(2026, 10, 6))[0]
    # duplicates inside one batch collapse to the highest severity
    f, s = monitor.filter_new([med, high], [], TODAY)
    assert len(f) == 1 and f[0].severity == "high" and len(s) == 1


def test_log_roundtrip_and_pruning(tmp_path):
    p = tmp_path / "alerts.json"
    log = [dict(key="a", severity="low", ts="2024-01-01"), dict(key="b", severity="low", ts="2026-10-01")]
    monitor.save_log(p, log, keep_days=400, today="2026-10-05")
    assert [r["key"] for r in monitor.load_log(p)] == ["b"]
    assert monitor.load_log(tmp_path / "missing.json") == []


def test_alerts_sorted_by_severity_and_keys_stable():
    t = thesis(status=Status.HOLD.value); t.entry = EntryPlan(invalidation_price=95.0); t.catalysts = [Catalyst("X", window="Aug 2026")]
    al = monitor.evaluate(t, snap(price=90.0))
    sev = [monitor.SEV_RANK[a.severity] for a in al]
    assert sev == sorted(sev, reverse=True) and al[0].kind == "invalidation_breached"
    assert [a.key for a in al] == [a.key for a in monitor.evaluate(t, snap(price=90.0))]
