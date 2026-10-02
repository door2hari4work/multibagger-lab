"""Post-test DATA-INTEGRITY sensitivity (not tuning; frozen rules unchanged). Reads sealed files directly -> logged in DEVIATIONS.md.
Re-runs the frozen strategy with names that show >45% single-day moves in 2019+ (likely unadjusted corporate actions / bad prints) removed."""
import sys, pandas as pd, numpy as np
sys.path.insert(0, "/home/user/multibagger-lab/analysis/improve"); sys.path.insert(0, "/home/user/multibagger-lab")
import backtest as bt
from common import CASH, scores, RAW
px = pd.concat([pd.read_parquet(RAW / "prices_tune.parquet"), pd.read_parquet(RAW / "prices_test_SEALED.parquet")]).sort_index()
ex = pd.concat([pd.read_parquet(RAW / "extra_tune.parquet"), pd.read_parquet(RAW / "extra_test_SEALED.parquet")]).sort_index()
b = pd.concat([pd.read_parquet(RAW / "bench_tune.parquet"), pd.read_parquet(RAW / "bench_test_SEALED.parquet")]).iloc[:, 0].sort_index()
n500 = ex["^CRSLDX"].dropna(); reg = n500 > n500.rolling(200).mean()
r = px.loc["2019-01-01":].pct_change(fill_method=None).stack(); bad = sorted(set(r[r.abs() > 0.45].index.get_level_values(1)))
print("removed:", bad)
EV0 = "2019-01-01"
for label, p in [("all names (official)", px), ("flagged names removed", px.drop(columns=bad))]:
    sc = scores(p)["S_mom_vol"]
    eq, tr = bt.backtest(p, b, top_n=25, stop=0.30, cost_bps=25, regime=True, regime_series=reg, score=sc, cash_rate=CASH, start=EV0)
    e = eq.loc[EV0:"2026-09-30"]; e = e / e.iloc[0]; m = bt.metrics(e)
    print(f"{label}: CAGR {m['CAGR']:.3f} MaxDD {m['MaxDD']:.3f} final Rs {1e6*e.iloc[-1]:,.0f}")
