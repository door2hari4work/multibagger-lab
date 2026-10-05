"""Offline tests (synthetic data, no network) for liquidity floor, reliability flags, sub-score None handling, screen."""
import numpy as np
import pandas as pd
import pytest

from mblab.data import prices as P, fundamentals as F, universe as U
from mblab import discovery as D


def _panel(n=300, tickers=("A.NS", "B.NS"), seed=0, start="2025-01-01"):
    idx = pd.bdate_range(start, periods=n)
    rng = np.random.default_rng(seed)
    close = pd.DataFrame({t: 100 * np.exp(np.cumsum(rng.normal(0.001, 0.01, n))) for t in tickers}, index=idx)
    vol = pd.DataFrame({t: np.full(n, 1e6) for t in tickers}, index=idx)
    return close, vol


# ------------------------------------------------------------------------------------------------ liquidity
def test_liquidity_floor_median_and_threshold():
    close, vol = _panel(60)
    close["A.NS"] = 100.0; vol["A.NS"] = 6e5       # 6e7 / day -> above Rs 5 cr
    close["B.NS"] = 100.0; vol["B.NS"] = 4e5       # 4e7 / day -> below
    liq = P.liquidity_table(close, vol, min_adv=P.DEFAULT_MIN_ADV["IN"])
    assert bool(liq.at["A.NS", "passes_liquidity"]) and not bool(liq.at["B.NS", "passes_liquidity"])
    assert liq.at["A.NS", "adv"] == pytest.approx(6e7)


def test_liquidity_uses_median_not_mean_and_is_configurable():
    close, vol = _panel(40, ("X",))
    close["X"] = 10.0
    vol["X"] = 1e6
    vol.iloc[-3:, 0] = 1e10                       # 3 huge spikes must not lift the 20d median
    assert P.liquidity_table(close, vol, min_adv=2e7)["adv"].iloc[0] == pytest.approx(1e7)
    assert not bool(P.liquidity_table(close, vol, min_adv=2e7).at["X", "passes_liquidity"])
    assert bool(P.liquidity_table(close, vol, min_adv=5e6).at["X", "passes_liquidity"])


def test_liquidity_insufficient_obs_fails_and_defaults():
    close, vol = _panel(40, ("S", "N"))
    close.iloc[:30, 0] = np.nan; vol.iloc[:30, 0] = np.nan      # only 10 valid obs in the window -> not enough evidence
    liq = P.liquidity_table(close, vol, market="US")
    assert not bool(liq.at["S", "passes_liquidity"])
    assert P.DEFAULT_MIN_ADV == {"IN": 5e7, "US": 5e6}
    with pytest.raises(ValueError):
        P.liquidity_table(close, vol)


# ------------------------------------------------------------------------------------------ reliability flags
def test_reliability_flags_jump_stale_short_nodata():
    close, vol = _panel(300, ("OK", "JUMP", "STALE", "SHORT"))
    close.loc[close.index[150]:, "JUMP"] *= 0.45                # -55% in one day, volume flat -> unconfirmed (unadjusted split look)
    close.iloc[-20:, close.columns.get_loc("STALE")] = np.nan   # series ends 20 sessions early
    close.iloc[:-100, close.columns.get_loc("SHORT")] = np.nan
    rel = P.reliability_check(close, volume=vol, tickers=["OK", "JUMP", "STALE", "SHORT", "MISSING"])
    assert rel.at["OK", "flags"] == []
    assert "price_jump" in rel.at["JUMP", "flags"] and "jump_unconfirmed" in rel.at["JUMP", "flags"]
    assert rel.at["JUMP", "max_abs_move"] > 0.45 and rel.at["JUMP", "n_jumps"] == 1
    assert "stale" in rel.at["STALE", "flags"]
    assert "short_history" in rel.at["SHORT", "flags"]
    assert rel.at["MISSING", "flags"] == ["no_data"]


def test_jump_with_volume_spike_is_confirmed_not_unconfirmed():
    close, vol = _panel(300, ("EARN",))
    close.loc[close.index[200]:, "EARN"] *= 1.6                 # +60% earnings gap
    vol.iloc[200, 0] = 2e7                                      # 20x normal volume
    rel = P.reliability_check(close, volume=vol)
    assert "price_jump" in rel.at["EARN", "flags"] and "jump_unconfirmed" not in rel.at["EARN", "flags"]


def test_small_moves_do_not_flag_and_threshold_is_configurable():
    close, vol = _panel(300, ("A",))
    close.loc[close.index[100]:, "A"] *= 1.30                   # +30% < 45%
    assert "price_jump" not in P.reliability_check(close, volume=vol).at["A", "flags"]
    assert "price_jump" in P.reliability_check(close, volume=vol, max_move=0.25).at["A", "flags"]


# ---------------------------------------------------------------------------------------------- sub-scores
def _q_rows(revs, ebitda, ni=None, start="2025-06-30"):
    ends = pd.to_datetime(pd.date_range(start, periods=len(revs), freq="QE"))
    return pd.DataFrame(dict(ticker="T", period_end=ends, period_type="Q", revenue=revs, operating_income=np.nan, ebitda=ebitda,
                             net_income=ni if ni is not None else np.nan, ocf=np.nan, filed_date=pd.NaT, retrieved_at="2026-10-05",
                             source="yfinance_quarterly", backtestable=False))


def test_metrics_none_when_history_too_short():
    m = F.compute_metrics(_q_rows([100, 110, 120], [10, 11, 12]), today="2026-10-05")
    assert m["rev_yoy0"] is None and m["rev_accel"] is None and m["margin_delta"] is None
    assert D.score_growth_acceleration(m)["value"] is None
    assert D.score_growth_acceleration(m)["data_quality"] == "missing"
    assert D.score_earnings_inflection(m)["value"] is None
    assert F.compute_metrics(None)["freq"] is None


def test_growth_and_earnings_scores_accelerating_company():
    # 6 quarters: yoy(latest)=+60%, yoy(prev)=+30% -> acceleration +30pp; margin 10% -> 20%
    revs = [100, 100, 100, 130, 130, 160]
    eb = [10, 10, 10, 13, 20, 32]
    m = F.compute_metrics(_q_rows(revs, eb, start="2025-03-31"), today="2026-10-05")
    assert m["rev_yoy0"] == pytest.approx(0.6) and m["rev_accel"] is not None
    g = D.score_growth_acceleration(m)
    e = D.score_earnings_inflection(m)
    assert 0.8 < g["value"] <= 1.0 and g["basis"] and g["data_quality"] in ("ok", "partial")
    assert e["value"] > 0.8 and "margin" in e["basis"]


def test_scores_stay_in_unit_interval_and_flat_company_is_midrange():
    m = F.compute_metrics(_q_rows([100] * 6, [10] * 6, start="2025-03-31"), today="2026-10-05")
    g, e = D.score_growth_acceleration(m), D.score_earnings_inflection(m)
    assert 0 <= g["value"] <= 1 and 0 <= e["value"] <= 1
    assert e["value"] == pytest.approx(0.5 * 0.6 + 0.4 * 0.5)


def test_financials_have_no_earnings_inflection_and_stale_is_labelled():
    m = F.compute_metrics(_q_rows([100] * 6, [10] * 6, start="2024-03-31"), today="2026-10-05")
    assert m["staleness_days"] > 200
    assert D.score_growth_acceleration(m)["data_quality"] == "stale"
    fe = D.score_earnings_inflection(m, financial=True)
    assert fe["value"] is None and fe["data_quality"] == "missing"
    assert F.is_financial("Financial Services") and F.is_financial("Financials") and not F.is_financial("Information Technology")


def test_valuation_none_without_marketcap_partial_otherwise():
    m = F.compute_metrics(_q_rows([100, 100, 100, 100, 130, 130], [10] * 6, ni=[5] * 6, start="2025-03-31"), today="2026-10-05")
    assert D.score_valuation_asymmetry(m, None)["value"] is None
    v = D.score_valuation_asymmetry(m, 5000.0)
    assert v["value"] is not None and 0 <= v["value"] <= 1 and v["data_quality"] == "partial"
    assert D.score_valuation_asymmetry({}, 5000.0)["value"] is None


def test_market_confirmation_missing_parts_renormalise_and_mark_partial():
    full = D.score_market_confirmation(0.9, 0.8, 3, 3, True)
    assert full["data_quality"] == "ok" and 0.85 < full["value"] < 0.95
    part = D.score_market_confirmation(0.9, None, 3, 3, None)
    assert part["data_quality"] == "partial" and part["value"] is not None
    none = D.score_market_confirmation(None, 0.8, 3, 3, True)
    assert none["value"] is None and none["data_quality"] == "missing"


def test_ttm_bridge_when_a_quarter_is_missing():
    q = _q_rows([100, 100, 120, 130], [10] * 4, ni=[1] * 4, start="2025-06-30")
    q = q.drop(index=1)                                   # Sep-2025 quarter missing at Yahoo
    q["period_end"] = pd.to_datetime(["2025-06-30", "2025-12-31", "2026-03-31"])
    q.loc[:, "revenue"] = [100, 120, 130]
    a = pd.DataFrame(dict(ticker="T", period_end=[pd.Timestamp("2025-03-31"), pd.Timestamp("2026-03-31")], period_type="A", revenue=[380, 460.0],
                          operating_income=np.nan, ebitda=[40, 50.0], net_income=[4, 5.0], ocf=np.nan, filed_date=pd.NaT,
                          retrieved_at="2026-10-05", source="yfinance_annual", backtestable=False))
    m = F.compute_metrics(pd.concat([q, a]), today="2026-04-30")
    assert m["ttm_revenue"] == pytest.approx(460.0)       # latest quarter == FY end -> TTM is the FY itself


# ------------------------------------------------------------------------------------------------- screen
def test_build_candidates_screen_end_to_end_synthetic():
    n = 320
    idx = pd.bdate_range("2025-06-02", periods=n)
    rng = np.random.default_rng(1)
    names = ["UP1.NS", "UP2.NS", "DOWN.NS", "ILLIQ.NS", "JUMP.NS", "SHORT.NS"]
    close = pd.DataFrame(index=idx)
    drift = {"UP1.NS": 0.003, "UP2.NS": 0.002, "DOWN.NS": -0.002, "ILLIQ.NS": 0.003, "JUMP.NS": 0.002, "SHORT.NS": 0.002}
    for t in names:
        close[t] = 100 * np.exp(np.cumsum(rng.normal(drift[t], 0.008, n)))
    vol = pd.DataFrame({t: np.full(n, 5e6) for t in names}, index=idx)
    vol["ILLIQ.NS"] = 1e3                                     # ~1e5 INR/day
    close.loc[idx[-100]:, "JUMP.NS"] *= 0.4                   # unadjusted-split look
    close.iloc[:-150, close.columns.get_loc("SHORT.NS")] = np.nan
    pdata = P.PriceData(close, close, close, vol)
    uni = pd.DataFrame(dict(ticker=names, name=names, market="IN", sector="Industrials", segment="small"))
    df, meta = D.build_candidates(pdata, uni, "IN", dict(regime_on=True, index="X"), fund=None, mcaps=None, top_n=10)
    assert meta["excluded_counts"].get("illiquid") == 1
    assert meta["excluded_counts"].get("short_history") == 1
    assert meta["excluded_counts"].get("jump_gt45pct_unconfirmed_by_volume") == 1
    assert "DOWN.NS" not in set(df["ticker"])                 # fails the trend filters
    assert "ILLIQ.NS" not in set(df["ticker"]) and "JUMP.NS" not in set(df["ticker"])
    assert list(df["mom_12_1"]) == sorted(df["mom_12_1"], reverse=True)   # ordered by 12-1 momentum, highest first
    assert list(df["rank"]) == list(range(1, len(df) + 1))
    sc = df.iloc[0]["scores"]
    assert set(sc) == set(D.COMPONENTS)
    for c in sc.values():
        assert {"value", "basis", "data_quality"} <= set(c)
    assert sc["growth_acceleration"]["value"] is None and sc["growth_acceleration"]["data_quality"] == "missing"   # no fundamentals supplied
    assert "overall" not in df.columns and "buy_score" not in df.columns


def test_universe_rejects_unknown_market_and_us_yahoo_symbols():
    with pytest.raises(ValueError):
        U.get_universe("JP")
    assert U._yahoo_us("BRK.B") == "BRK-B"
    assert U._norm_market("india") == "IN"
