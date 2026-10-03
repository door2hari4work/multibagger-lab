"""US quality-gate test, TUNE WINDOW ONLY (2010-2018). SEC annual filings, originally reported values, usable on filing date.
Universe = current S&P 500 members with SEC data (survivor-biased). Gate thresholds are the UNTUNED placeholders from pit_gate.py."""
import sys, pandas as pd, numpy as np
from multiprocessing import Pool
sys.path.insert(0, "/home/user/multibagger-lab/analysis/improve"); sys.path.insert(0, "/home/user/multibagger-lab"); sys.path.insert(0, "/home/user/multibagger-lab/analysis/fundamentals")
import backtest as bt, config
from pit_gate import GateParams, pit_eligibility, prepare, is_financial
from common import scores, RAW
px = pd.read_parquet(RAW/"us_prices_tune.parquet"); ex = pd.read_parquet(RAW/"us_extra_tune.parquet")
g = ex["^GSPC"].dropna(); spy = ex["SPY"].dropna(); reg = g > g.rolling(200).mean(); SC = scores(px)["S_mom_vol"]; EV0 = "2010-01-01"
fund = pd.read_parquet(config.ROOT/"data/pit/us_fundamentals.parquet"); fund = fund[pd.to_datetime(fund.filed_date) <= pd.Timestamp(config.TUNE_END)]  # tune window only
fund = fund[fund.symbol.isin(px.columns)]
sect = fund.drop_duplicates("symbol").set_index("symbol")["sector"].to_dict()
rb = px.loc[EV0:].groupby([px.loc[EV0:].index.year, px.loc[EV0:].index.month]).tail(1).index
K = dict(top_n=25, stop=0.30, cost_bps=10, regime=True, regime_series=reg, score=SC, cash_rate=0.01, start=EV0)
VAR = {
 "G0_no_gate_full_universe": None,
 "G1_no_gate_covered_nonfinancial": "cov",
 "G2_gate_default": GateParams(),
 "G3_gate_default_lag90_ignore_filed_date": GateParams(force_lag=True, annual_lag_days=90),
 "G4_gate_growth5": GateParams(min_rev_growth=0.05, min_ebitda_growth=0.05),
 "G5_gate_growth15": GateParams(min_rev_growth=0.15, min_ebitda_growth=0.15),
 "G6_margin_trend_only": GateParams(min_rev_growth=-9, min_ebitda_growth=-9, min_ocf_ebitda=-9),
 "G7_cash_quality_only": GateParams(min_margin_delta=-9, min_rev_growth=-9, min_ebitda_growth=-9),
}
def build(p):
    if p is None: return None
    if p == "cov":
        prep = prepare(fund); first = prep.groupby("symbol").usable_date.min()
        m = pd.DataFrame({s: (rb >= first[s]) & (not is_financial(sect.get(s))) for s in first.index}, index=rb); return m
    e = pit_eligibility(fund, rb, symbols=list(px.columns), sectors=sect, params=p); return e, e.pivot(index="rebalance_date", columns="symbol", values="eligible").astype(bool)
def st(eq):
    e = eq.loc[EV0:]; e = e/e.iloc[0]; m = bt.metrics(e); return m["CAGR"], m["MaxDD"]
def run(name):
    p = VAR[name]; b_ = build(p); cov = None
    if isinstance(b_, tuple):
        e, gate = b_; ok = e.reason.isin(["pass", "margin_not_improving", "revenue_growth_low", "ebitda_growth_low", "ocf_quality_low", "no_ocf_data", "nonpositive_ebitda", "nonpositive_revenue"])
        cov = float(ok[e.reason != "financials_excluded"].mean()); n = float(gate.sum(axis=1).mean())
    else:
        gate = b_; n = float(gate.sum(axis=1).mean()) if gate is not None else float(px.loc[EV0:].notna().sum(axis=1).mean())
    eq, tr = bt.backtest(px, g, gate=gate, **K); c, d = st(eq); y = eq.loc["2018-01-01":"2018-12-31"]
    t = pd.DataFrame(tr, columns=["t", "e", "x", "w"]).dropna(); r = t.x/t.e-1
    out = dict(variant=name, CAGR=c, MaxDD=d, ret2018=y.iloc[-1]/y.iloc[0]-1, final_rs=round(1e6*eq.loc[EV0:].iloc[-1]/eq.loc[EV0:].iloc[0]), avg_names_passing=n, data_coverage=cov, trades=len(t), hit=(r > 0).mean())
    if name == "G2_gate_default":
        rr = []
        for sd in range(30):
            e_, _ = bt.backtest(px, g, gate=gate, mode="random", seed=sd, **K); e_ = e_.loc[EV0:]; rr.append(bt.metrics(e_ / e_.iloc[0]))
        out["random_gated_median_CAGR"] = float(np.median([x["CAGR"] for x in rr])); out["random_gated_median_MaxDD"] = float(np.median([x["MaxDD"] for x in rr]))
    return out
if __name__ == "__main__":
    with Pool(4) as p: rows = p.map(run, list(VAR))
    df = pd.DataFrame(rows); pd.set_option("display.width", 250, "display.float_format", lambda x: f"{x:,.3f}")
    df.to_csv(config.ROOT/"results/tune/us_gate.csv", index=False); print(df.to_string(index=False))
    c, d = st(spy); print("\nSPY (TRI proxy):", round(c, 3), round(d, 3))
    print("fundamentals rows filed<=2018:", len(fund), "| symbols:", fund.symbol.nunique())
