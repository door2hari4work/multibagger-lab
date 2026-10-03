"""US applicability check: India-frozen rule logic on US S&P 500 survivors, TUNE WINDOW 2010-2018 ONLY, no re-tuning. US assumptions: 10 bps/side, 1% cash."""
import sys, pandas as pd, numpy as np
from multiprocessing import Pool
sys.path.insert(0, "/home/user/multibagger-lab/analysis/improve"); sys.path.insert(0, "/home/user/multibagger-lab")
import backtest as bt
from common import scores, RAW
px = pd.read_parquet(RAW/"us_prices_tune.parquet"); ex = pd.read_parquet(RAW/"us_extra_tune.parquet")
g = ex["^GSPC"].dropna(); spy = ex["SPY"].dropna(); reg = g > g.rolling(200).mean(); SC = scores(px)["S_mom_vol"]; EV0 = "2010-01-01"
K = dict(top_n=25, stop=0.30, cost_bps=10, regime=True, regime_series=reg, score=SC, cash_rate=0.01, start=EV0)
def st(e):
    e = e.loc[EV0:]; e = e/e.iloc[0]; m = bt.metrics(e); return m["CAGR"], m["MaxDD"]
def rnd(a):
    m, s = a; eq, _ = bt.backtest(px, g, mode=m, seed=s, **K); return (m,) + st(eq)
if __name__ == "__main__":
    eq, tr = bt.backtest(px, g, **K); c, d = st(eq); sc_, sd = st(spy)
    r1 = (px.loc[EV0:].pct_change(fill_method=None).mean(axis=1).fillna(0)+1).cumprod(); ec, ed = st(r1)
    print(f"US strategy: CAGR {c:.3f} MaxDD {d:.3f} final Rs {1e6*eq.loc[EV0:].iloc[-1]/eq.loc[EV0:].iloc[0]:,.0f} (USD index terms, Rs 10 lakh illustrative)")
    print(f"SPY (TRI proxy): {sc_:.3f} / {sd:.3f} | equal-weight S&P survivors hold: {ec:.3f} / {ed:.3f}")
    yrs = eq.loc[EV0:].resample("YE").last().pct_change(); print("years", yrs.round(3).dropna().to_dict())
    with Pool(4) as p: rr = p.map(rnd, [(m, s) for m in ("random", "random_all") for s in range(40)])
    df = pd.DataFrame(rr, columns=["m", "CAGR", "MaxDD"])
    for m, x in df.groupby("m"): print(m, "median CAGR", round(x.CAGR.median(), 3), "median MaxDD", round(x.MaxDD.median(), 3), "| seeds with CAGR below strategy", round((x.CAGR < c).mean(), 2), "| seeds with worse MaxDD", round((x.MaxDD < d).mean(), 2))
