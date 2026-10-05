"""Portfolio intelligence tests. ALL data here is synthetic (tests/fixtures); no real holdings anywhere."""
import json
import subprocess
from pathlib import Path

import pytest

from mblab import portfolio as P
from mblab.schema import PortfolioFit

FIX = Path(__file__).parent / "fixtures"
ROOT = Path(__file__).resolve().parent.parent


def _raw():
    return json.loads((FIX / "synthetic_indmoney_raw.json").read_text())


def _funds():
    return json.loads((FIX / "synthetic_fund_details.json").read_text())


@pytest.fixture(scope="module")
def pf():
    return P.normalise_indmoney_snapshot(_raw(), _funds(), overrides={"sector": {"Acme Widgets Corp": "Industrials"}})


@pytest.fixture(scope="module")
def ana(pf):
    return P.analyze_portfolio(pf)


# ---------------------------------------------------------------- privacy
def test_private_dir_is_gitignored_and_untracked():
    r = subprocess.run(["git", "check-ignore", "-q", "private/portfolio_snapshot.json"], cwd=ROOT)
    assert r.returncode == 0, "private/ must be gitignored"
    tracked = subprocess.run(["git", "ls-files", "private"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    assert tracked == "", "nothing under private/ may be tracked"
    assert P.private_is_ignored()


def test_write_private_refuses_other_locations():
    with pytest.raises(ValueError):
        P.write_private({"x": 1}, "../outside.json")
    with pytest.raises(ValueError):
        P.write_private({"x": 1}, "/tmp/outside.json")


def test_import_report_contains_no_holding_names():
    res = P.load_holdings_csv(FIX / "synthetic_finboom_like.csv")
    rep = res.report()
    assert all(h.name not in rep for h in res.holdings)


# ---------------------------------------------------------------- importers
def test_csv_header_detection_with_preamble_and_unmapped_columns():
    res = P.load_holdings_csv(FIX / "synthetic_finboom_like.csv")
    assert res.header_row == 4 and res.preamble_rows == 3
    assert res.column_map["name"] == "Scrip Name"
    assert res.column_map["quantity"] == "Qty."
    assert res.column_map["avg_cost"].startswith("Avg. Buy Price")
    assert res.column_map["price"] == "LTP"
    assert res.column_map["value_inr"].startswith("Current Value")
    assert res.unmapped_columns == ["Mystery Column"]
    assert "Mystery Column" in res.report()
    assert len(res.holdings) == 3                          # 'Total' row skipped
    assert any(reason == "total row" for _, reason in res.skipped_rows)
    by = {h.name: h for h in res.holdings}
    assert by["Alpha Widgets Ltd"].value_inr == 150000 and by["Alpha Widgets Ltd"].sector == "Industrials"
    assert by["Beta Chips Ltd"].value_inr == pytest.approx(50 * 220)       # derived from qty * price
    assert "defence_aerospace" in by["Gamma Defence Aeronautics Ltd"].themes
    assert "semiconductors" not in by["Beta Chips Ltd"].themes     # keyword 'chips' alone is deliberately not a semis tag


def test_csv_semicolon_usd_and_isin_inference():
    res = P.load_holdings_csv(FIX / "synthetic_semicolon_usd.csv", fx={"USD": 80})
    by = {h.instrument_id: h for h in res.holdings}
    assert by["ZZZ"].market == "US" and by["ZZZ"].currency == "USD" and by["ZZZ"].value_inr == pytest.approx(500 * 80)
    assert by["QQQ"].market == "IN" and by["QQQ"].currency == "INR" and by["QQQ"].value_inr == 1200
    assert by["ZZZ"].avg_cost == pytest.approx(100)


def test_csv_missing_fx_is_reported_not_silent():
    res = P.load_holdings_csv(FIX / "synthetic_semicolon_usd.csv")
    assert any("assumed fx" in w for w in res.warnings)


def test_csv_unrecognisable_file_reports_instead_of_guessing():
    res = P.load_holdings_csv("foo,bar\n1,2\n")
    assert not res.ok and res.warnings


def test_mapping_override_for_unknown_headers():
    txt = "Company,Holding Qty,Pelf\nAlpha Ltd,5,100\nBeta Ltd,2,40\n"
    plain = P.load_holdings_csv(txt)
    assert "Pelf" in plain.unmapped_columns                              # reported, not silently dropped
    res = P.load_holdings_csv(txt, mapping={"value_local": "Pelf"})
    assert [h.value_inr for h in res.holdings] == [100, 40]


def test_number_parsing():
    assert P._num("(1,234.50)") == -1234.5 and P._num("₹ 1,50,000") == 150000 and P._num("12.5%") == 12.5 and P._num("-") is None and P._num("") is None


def test_excel_import(tmp_path):
    pd = pytest.importorskip("pandas")
    pytest.importorskip("openpyxl")
    rows = [["Synthetic Export"], [], ["Stock Name", "Quantity", "Average Price", "Current Price", "Sector"], ["Alpha Ltd", 10, 100, 150, "Tech"], ["Beta Ltd", 5, 50, 40, "Health"]]
    f = tmp_path / "h.xlsx"
    pd.DataFrame(rows).to_excel(f, header=False, index=False)
    res = P.load_holdings_excel(f)
    assert len(res.holdings) == 2 and res.header_row == 3
    assert {h.sector for h in res.holdings} == {"Technology", "Healthcare"}
    assert res.holdings[0].value_inr == 1500


# ---------------------------------------------------------------- IndMoney normaliser
def test_indmoney_normaliser_structure(pf):
    kinds = {}
    for h in pf.holdings:
        kinds[h.kind] = kinds.get(h.kind, 0) + 1
    assert kinds == {"mutual_fund": 6, "stock": 3, "other": 1}      # 6 funds, 2 US + 1 ESOP stock, savings total
    assert pf.reconciliation["difference_pct"] == pytest.approx(0.0, abs=1e-6)
    assert len(pf.fund_profiles) == 5                                   # one fund had no detail data
    alph = next(h for h in pf.holdings if h.instrument_id == "ALPH")
    assert alph.market == "US" and alph.currency == "USD" and alph.fx_rate == pytest.approx(80) and alph.avg_cost == pytest.approx(200) and alph.sector == "Technology"
    esop = next(h for h in pf.holdings if h.source == "indmoney:esops_rsus")
    assert esop.market == "US" and esop.sector == "Industrials"          # market from issuer-name heuristic, sector from override
    assert next(h for h in pf.holdings if h.instrument_id == "9005").asset_class == "gold"


def test_fund_profile_math_and_quality(pf):
    z1 = pf.fund_profiles["9001"]
    assert z1.quality == "partial" and z1.disclosed_fraction == pytest.approx(0.25)
    assert z1.sector["Technology"] == pytest.approx(0.6) and z1.sector["Financial Services"] == pytest.approx(0.4)
    assert z1.country == {"US": 1.0}                                    # from the benchmark / name
    z2 = pf.fund_profiles["9002"]
    assert z2.asset_mix["equity"] == pytest.approx(0.9) and z2.asset_mix["cash"] == pytest.approx(0.1)
    assert z2.sector["Technology"] == pytest.approx(0.9 * 0.3)
    assert z2.sector["Debt & Cash"] == pytest.approx(0.1)
    assert z2.market_cap["large"] == pytest.approx(0.63)
    assert pf.fund_profiles["9005"].quality == "full" and pf.fund_profiles["9005"].asset_mix == {"gold": 1.0}


def test_response_wrappers_accepted():
    a = P._unwrap({"result": json.dumps({"a": 1})})
    assert a == {"a": 1} and P._unwrap({"a": 1}) == {"a": 1}


# ---------------------------------------------------------------- look-through math
def test_total_and_asset_mix(pf, ana):
    total = 200000 + 430000 + 30000 + 25000          # US stocks + funds + esop + savings
    assert ana["total_value_inr"] == pytest.approx(total)
    assert ana["by_asset_class"]["gold"] == pytest.approx(20000 / total * 100, abs=0.01)
    assert ana["direct_vs_indirect"]["direct_stocks_pct"] == pytest.approx((200000 + 30000) / total * 100, abs=0.01)
    assert ana["direct_vs_indirect"]["via_funds_pct"] == pytest.approx(430000 / total * 100, abs=0.01)


def test_single_name_lookthrough_adds_direct_and_indirect(ana):
    total = ana["total_value_inr"]
    alph = next(s for s in ana["stock_exposure"] if "alpha semiconductor" in s["key"])
    # direct 100k; Zeta fund 200k * 10% = 20k; Omega fund 100k * 5% = 5k
    assert alph["direct_pct"] == pytest.approx(100000 / total * 100, abs=0.01)
    assert alph["indirect_pct"] == pytest.approx(25000 / total * 100, abs=0.01)
    assert alph["total_pct"] == pytest.approx(125000 / total * 100, abs=0.01)
    assert alph["n_sources"] == 3


def test_theme_lookthrough_estimate_and_lower_bound(ana):
    total = ana["total_value_inr"]
    s = ana["by_theme"]["semiconductors"]
    assert s["direct_pct"] == pytest.approx(100000 / total * 100, abs=0.01)
    # lower bound: direct 100k + Zeta (Alpha 20k + Gamma 10k) + Omega (Alpha 5k) = 135k
    assert s["lower_bound_pct"] == pytest.approx(135000 / total * 100, abs=0.01)
    # estimate extrapolates the disclosed sample over each fund's equity: Zeta 200k*(30k/50k)=120k ; Omega 90k*(5k/20k)=22.5k
    assert s["estimated_pct"] == pytest.approx((100000 + 120000 + 22500) / total * 100, abs=0.01)
    assert s["estimated_pct"] > s["lower_bound_pct"] > s["direct_pct"]
    assert s["multiple_of_direct"] == pytest.approx(2.425, abs=0.01)


def test_effective_exposure_warning_text(ana):
    msgs = [w for w in ana["warnings"] if "semiconductors" in w]
    assert msgs and "times your direct holdings" in msgs[0] and "estimate" in msgs[0]


def test_sector_country_currency_and_market_cap(ana):
    total = ana["total_value_inr"]
    # Technology: 2 direct (200k) + Zeta 200k*0.6 + Omega 100k*0.27 + Sigma A/B 50k*0.3 each
    tech = 200000 + 120000 + 27000 + 15000 + 15000
    assert ana["by_sector"]["Technology"] == pytest.approx(tech / total * 100, abs=0.02)
    assert ana["by_country"]["US"] > 50 and set(ana["by_country"]) <= {"US", "IN"}
    assert ana["by_currency_held"]["USD"] == pytest.approx(200000 / total * 100, abs=0.01)
    assert ana["by_currency_economic"]["USD"] > ana["by_currency_held"]["USD"]       # US fund counts economically as USD
    assert ana["by_market_cap"]["large"] > 70


# ---------------------------------------------------------------- overlap / duplication / concentration
def test_duplicate_names_across_funds_detected(ana):
    names = {d["name"]: d for d in ana["duplicates"]}
    assert any("Alpha Semiconductor" in n for n in names)
    delta = next(d for n, d in names.items() if "Delta Bank" in n)
    assert len(delta["sources"]) >= 3                      # Zeta + Sigma A + Sigma B


def test_identical_benchmark_funds_flagged(ana):
    twins = [o for o in ana["fund_overlaps"] if o["same_benchmark"]]
    assert len(twins) == 1
    assert twins[0]["overlap_of_disclosed_pct"] == pytest.approx(20.0)
    assert any("same benchmark" in w for w in ana["warnings"])


def test_concentration_metrics(ana):
    c = ana["concentration"]
    total = ana["total_value_inr"]
    weights = [200000 / 2, 200000 / 2, 200000, 100000, 50000, 50000, 20000, 10000, 30000, 25000]
    weights = [w / total for w in [100000, 100000, 200000, 100000, 50000, 50000, 20000, 10000, 30000, 25000]]
    assert c["hhi_positions"] == pytest.approx(sum(w * w for w in weights), abs=1e-3)
    assert c["effective_n_positions"] == pytest.approx(1 / sum(w * w for w in weights), abs=0.05)
    assert c["top_positions"][0]["name"].startswith("Zeta") and c["top1_pct"] == pytest.approx(200000 / total * 100, abs=0.01)
    assert c["top3_pct"] >= c["top1_pct"] and c["top10_pct"] == pytest.approx(100.0, abs=0.01)


def test_look_through_quality_reporting(ana):
    q = ana["look_through_quality"]
    assert q["label"] in ("partial", "mostly category-level")
    assert q["pct_of_portfolio_by_quality"]["full"] > 0 and q["pct_of_portfolio_by_quality"]["partial"] > 0
    assert any("only" in n and "of the fund" in n for n in q["notes"])        # the partial disclosure caveat is surfaced


def test_fund_without_details_falls_back_to_category_level(pf):
    unknown = next(h for h in pf.holdings if h.instrument_id == "9999")
    comp = P._composition(unknown, pf.fund_profiles.get("9999"))
    assert comp["quality"] in ("category", "none")                      # never claims more than it knows


# ---------------------------------------------------------------- fit scoring
def test_no_portfolio_returns_none_score():
    fit = P.fit_score({"ticker": "XYZ", "sector": "Technology", "themes": ["ai"], "market": "US", "market_cap_bucket": "small"}, None)
    assert isinstance(fit, PortfolioFit) and fit.score is None and "No portfolio" in fit.summary and fit.suggested_max_weight_pct is None
    assert P.fit_score({"ticker": "XYZ"}, {"empty": True}).score is None


def test_fit_adds_missing_theme_scores_higher_than_adding_to_crowded_theme(ana):
    crowded = P.fit_score({"ticker": "NEWSEMI", "sector": "Technology", "themes": ["semiconductors", "ai"], "market": "US", "market_cap_bucket": "small"}, ana)
    missing = P.fit_score({"ticker": "NEWDEF", "sector": "Industrials", "themes": ["defence_aerospace"], "market": "IN", "market_cap_bucket": "small"}, ana)
    assert 0 <= crowded.score <= 1 and 0 <= missing.score <= 1
    assert missing.score > crowded.score + 0.15
    assert missing.suggested_max_weight_pct > crowded.suggested_max_weight_pct
    assert any("missing exposure" in n or "absent" in n for n in missing.overlap_notes)
    assert any("existing concentration" in n or "already" in n for n in crowded.overlap_notes)
    # honest framing in both directions
    for f in (crowded, missing):
        assert "Concentration can be appropriate" in f.summary and "diversification is not always better" in f.summary


def test_fit_flags_company_already_held_directly_and_via_funds(ana):
    fit = P.fit_score({"ticker": "ALPH", "name": "Alpha Semiconductor Corp", "sector": "Technology", "themes": ["semiconductors"], "market": "US", "market_cap_bucket": "large"}, ana)
    assert any("already own this company" in n for n in fit.overlap_notes)
    other = P.fit_score({"ticker": "NEWDEF", "sector": "Industrials", "themes": ["defence_aerospace"], "market": "IN", "market_cap_bucket": "large"}, ana)
    assert fit.score < other.score


def test_fit_with_no_candidate_attributes_is_neutral_and_says_so(ana):
    fit = P.fit_score({"ticker": "QQ"}, ana)
    assert fit.score is not None and "neutral" in fit.summary


def test_snapshot_roundtrip(pf):
    again = P.Portfolio.from_dict(json.loads(json.dumps(pf.to_dict())))
    assert len(again.holdings) == len(pf.holdings) and again.fund_profiles.keys() == pf.fund_profiles.keys()
    assert P.analyze_portfolio(again)["total_value_inr"] == pytest.approx(P.analyze_portfolio(pf)["total_value_inr"])
