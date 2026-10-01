"""Unit tests for analysis/fundamentals/pit_gate.py -- all on SYNTHETIC toy data; they prove the no-look-ahead
mechanics, not anything about Indian markets."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from analysis.fundamentals.pit_gate import (GateParams, pit_eligibility, prepare, coverage, eligibility_matrix,
                                            is_financial, symbol_quarter_coverage)

QE = pd.date_range("2013-03-31", periods=12, freq="QE")  # 12 consecutive quarter-ends 2013-03 .. 2015-12


def quarters(symbol="AAA", n=12, rev0=100.0, rev_g=0.04, m0=0.10, dm=0.004, ocf_ratio=0.8, filed_lag=None, start=0):
    """Healthy compounder: revenue +4%/qtr, margin rising, OCF = ocf_ratio * EBITDA."""
    rows = []
    for i in range(start, start + n):
        pe = QE[i]
        rev = rev0 * (1 + rev_g) ** i
        e = rev * (m0 + dm * i)
        rows.append(dict(symbol=symbol, period_end=pe,
                         filed_date=pe + pd.Timedelta(days=filed_lag) if filed_lag is not None else pd.NaT,
                         revenue=rev, ebitda=e, ocf=ocf_ratio * e, period_type="Q"))
    return pd.DataFrame(rows)


def elig_at(fund, d, **kw):
    kw.setdefault("allow_post_tune", True)
    r = pit_eligibility(fund, [d], **kw)
    return r.set_index("symbol")


D_LATE = pd.Timestamp("2016-03-31")  # well after all toy quarters are filed


def test_healthy_name_passes():
    r = elig_at(quarters(), D_LATE, symbols=["AAA"])
    assert r.loc["AAA", "eligible"], r.loc["AAA", "reason"]


def test_missing_data_is_not_eligible():
    r = elig_at(quarters(n=5), D_LATE, symbols=["AAA", "ZZZ"])
    assert not r.loc["AAA", "eligible"] and r.loc["AAA", "reason"] == "insufficient_history"
    assert not r.loc["ZZZ", "eligible"] and r.loc["ZZZ", "reason"] == "no_data"


@pytest.mark.parametrize("lag", [45, 60, 90, 120])
def test_future_quarter_filed_after_date_cannot_change_eligibility(lag):
    base = quarters(n=11, filed_lag=lag)
    d = QE[10] + pd.Timedelta(days=lag + 5)           # 11th quarter known, 12th not yet filed
    before = elig_at(base, d, symbols=["AAA"]).loc["AAA"]
    assert before.eligible
    # 12th quarter: collapse in margin and revenue, filed AFTER d
    filed_bad = QE[11] + pd.Timedelta(days=lag)          # strictly after d
    assert filed_bad > d
    bad = pd.DataFrame([dict(symbol="AAA", period_end=QE[11], filed_date=filed_bad,
                             revenue=1.0, ebitda=-50.0, ocf=-60.0, period_type="Q")])
    after = elig_at(pd.concat([base, bad]), d, symbols=["AAA"]).loc["AAA"]
    assert after.eligible == before.eligible and after.reason == before.reason
    assert after.margin_now == before.margin_now          # identical diagnostics, not just identical verdict
    # and the same row filed ON the date DOES change the verdict (inclusive boundary, proves the test has teeth)
    assert not elig_at(pd.concat([base, bad]), filed_bad, symbols=["AAA"]).loc["AAA"].eligible


@pytest.mark.parametrize("lag", [45, 60, 90, 120])
def test_lag_sensitivity_boundary_without_filed_date(lag):
    """No filed_date: latest quarter becomes usable exactly at period_end + lag, not a day earlier."""
    f = quarters(n=12)
    f.loc[f.period_end == QE[11], ["revenue", "ebitda", "ocf"]] = [1.0, -5.0, -5.0]  # decisive collapse in last quarter
    p = GateParams(quarterly_lag_days=lag, max_staleness_days=400)
    day_before = QE[11] + pd.Timedelta(days=lag - 1)
    on_day = QE[11] + pd.Timedelta(days=lag)
    assert elig_at(f, day_before, params=p, symbols=["AAA"]).loc["AAA"].eligible      # collapse not yet visible
    assert not elig_at(f, on_day, params=p, symbols=["AAA"]).loc["AAA"].eligible      # visible exactly at lag


def test_default_lag_comes_from_config():
    assert GateParams().quarterly_lag_days == config.QUARTERLY_LAG_DAYS
    assert GateParams().annual_lag_days == config.ANNUAL_LAG_DAYS


def test_annual_uses_annual_lag():
    a = pd.DataFrame([
        dict(symbol="AAA", period_end=pd.Timestamp("2013-03-31"), revenue=100, ebitda=10, ocf=8, period_type="A"),
        dict(symbol="AAA", period_end=pd.Timestamp("2014-03-31"), revenue=125, ebitda=16, ocf=12, period_type="A")])
    p = GateParams()
    assert elig_at(a, pd.Timestamp("2014-03-31") + pd.Timedelta(days=p.annual_lag_days - 1), symbols=["AAA"]).loc["AAA", "reason"] == "insufficient_history"
    r = elig_at(a, pd.Timestamp("2014-03-31") + pd.Timedelta(days=p.annual_lag_days), symbols=["AAA"]).loc["AAA"]
    assert r.eligible and r.trend_basis == "FY"


def test_filed_date_overrides_lag_unless_forced():
    f = quarters(n=12, filed_lag=30)                     # filed 30d after period end (earlier than 60d default lag)
    d = QE[11] + pd.Timedelta(days=31)
    f.loc[f.period_end == QE[11], ["revenue", "ebitda", "ocf"]] = [1.0, -5.0, -5.0]
    assert not elig_at(f, d, symbols=["AAA"]).loc["AAA"].eligible                         # filed_date honoured
    assert elig_at(f, d, params=GateParams(force_lag=True), symbols=["AAA"]).loc["AAA"].eligible  # lag forced


def test_original_values_not_restated():
    f = quarters(n=12, filed_lag=45)
    d = QE[11] + pd.Timedelta(days=50)
    restated = f[f.period_end == QE[11]].assign(filed_date=QE[11] + pd.Timedelta(days=400), ebitda=-99.0, ocf=-99.0)
    assert elig_at(pd.concat([f, restated]), d, symbols=["AAA"]).loc["AAA"].eligible          # later restatement ignored
    # even once the restatement is public, the ORIGINAL value is still the one used
    d2 = QE[11] + pd.Timedelta(days=500)
    d2 = min(d2, pd.Timestamp("2018-12-31"))
    assert elig_at(pd.concat([f, restated]), d2, symbols=["AAA"], params=GateParams(max_staleness_days=10_000)).loc["AAA"].eligible
    p = prepare(pd.concat([f, restated]))
    assert len(p) == len(f) and (p.ebitda > 0).all()


def test_truncation_invariance_all_dates():
    """Output at date d must be identical when computed on the full table or on only rows usable by d."""
    rng = np.random.default_rng(0)
    parts = []
    for i in range(6):
        parts.append(quarters(symbol=f"S{i}", n=12, rev_g=rng.uniform(-0.02, 0.06), dm=rng.uniform(-0.004, 0.006),
                              ocf_ratio=rng.uniform(0.2, 1.1), filed_lag=int(rng.choice([40, 55, 70]))))
    full = pd.concat(parts, ignore_index=True)
    dates = pd.date_range("2013-06-30", "2016-06-30", freq="QE")
    res_full = pit_eligibility(full, dates, allow_post_tune=True)
    prep = prepare(full)
    for d in dates:
        trunc = full[(full.filed_date <= d)]
        res_tr = pit_eligibility(trunc, [d], symbols=sorted(full.symbol.unique()), allow_post_tune=True)
        a = res_full[res_full.rebalance_date == d].set_index("symbol")[["eligible", "reason"]].sort_index()
        b = res_tr.set_index("symbol")[["eligible", "reason"]].sort_index()
        assert a.equals(b), d


def test_future_row_values_irrelevant_fuzz():
    base = quarters(n=10, filed_lag=45)
    d = QE[9] + pd.Timedelta(days=46)
    ref = elig_at(base, d, symbols=["AAA"]).loc["AAA"]
    rng = np.random.default_rng(1)
    for _ in range(25):
        fut = quarters(n=2, start=10, filed_lag=45)
        fut[["revenue", "ebitda", "ocf"]] = rng.normal(0, 1e4, size=(2, 3))
        r = elig_at(pd.concat([base, fut]), d, symbols=["AAA"]).loc["AAA"]
        assert (r.eligible, r.reason) == (ref.eligible, ref.reason)


def test_margin_trend_must_improve():
    r = elig_at(quarters(dm=-0.001), D_LATE, symbols=["AAA"]).loc["AAA"]
    assert not r.eligible and r.reason == "margin_not_improving"


def test_growth_required():
    r = elig_at(quarters(rev_g=0.0, dm=0.004), D_LATE, symbols=["AAA"]).loc["AAA"]
    assert not r.eligible and r.reason in ("revenue_growth_low", "ebitda_growth_low")


def test_ocf_quality_required():
    r = elig_at(quarters(ocf_ratio=0.2), D_LATE, symbols=["AAA"]).loc["AAA"]
    assert not r.eligible and r.reason == "ocf_quality_low"
    r2 = elig_at(quarters(ocf_ratio=0.2), D_LATE, symbols=["AAA"], params=GateParams(min_ocf_ebitda=0.1)).loc["AAA"]
    assert r2.eligible


def test_missing_ocf_fails_closed():
    f = quarters(); f["ocf"] = np.nan
    assert elig_at(f, D_LATE, symbols=["AAA"]).loc["AAA", "reason"] == "no_ocf_data"


def test_gap_in_quarters_fails_closed():
    f = quarters(); f = f[f.period_end != QE[8]]
    assert elig_at(f, D_LATE, symbols=["AAA"], params=GateParams(max_staleness_days=10_000)).loc["AAA", "reason"] == "insufficient_history"


def test_stale_data_fails_closed():
    assert elig_at(quarters(), pd.Timestamp("2018-12-31"), symbols=["AAA"]).loc["AAA", "reason"] == "insufficient_history"


def test_negative_ebitda_never_passes():
    f = quarters(m0=-0.5, dm=0.02)
    assert not elig_at(f, D_LATE, symbols=["AAA"]).loc["AAA"].eligible


def test_financials_excluded():
    f = pd.concat([quarters("BANK"), quarters("IND")])
    r = elig_at(f, D_LATE, sectors={"BANK": "Financial Services", "IND": "Fast Moving Consumer Goods"})
    assert not r.loc["BANK", "eligible"] and r.loc["BANK", "reason"] == "financials_excluded"
    assert r.loc["IND", "eligible"]
    off = elig_at(f, D_LATE, sectors={"BANK": "Financial Services"}, params=GateParams(exclude_financials=False))
    assert off.loc["BANK", "eligible"]
    assert is_financial("Banks - Private") and is_financial("NBFC") and not is_financial("Capital Goods")


def test_unknown_sector_policy():
    f = quarters()
    assert elig_at(f, D_LATE).loc["AAA", "eligible"]
    assert elig_at(f, D_LATE, params=GateParams(unknown_sector="exclude")).loc["AAA", "reason"] == "unknown_sector"


def test_post_tune_dates_refused():
    with pytest.raises(ValueError):
        pit_eligibility(quarters(), [pd.Timestamp("2019-01-31")])


def test_corrupt_dates_rejected():
    f = quarters(filed_lag=45); f.loc[0, "filed_date"] = f.loc[0, "period_end"] - pd.Timedelta(days=1)
    with pytest.raises(ValueError):
        prepare(f)


def test_matrix_and_coverage():
    f = pd.concat([quarters("AAA"), quarters("BBB", n=4)])
    e = pit_eligibility(f, [D_LATE], symbols=["AAA", "BBB", "CCC"], allow_post_tune=True)
    m = eligibility_matrix(e)
    assert m.shape == (1, 3) and m.dtypes.eq(bool).all()
    c = coverage(e)
    assert c["evaluable_pct"] == pytest.approx(100 / 3)
    assert symbol_quarter_coverage(quarters("AAA"), ["AAA", "BBB"], start="2013-01-01", end="2015-12-31") == pytest.approx(50.0)
