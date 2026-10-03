"""Hold-winners engine grid. TUNE WINDOW ONLY. 36 declared configs per market: score x stop x N x exit-on-200dMA-break."""
import sys, itertools, numpy as np, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, "/home/user/multibagger-lab/analysis/improve"); sys.path.insert(0, "/home/user/multibagger-lab")
import backtest as bt
from common import scores, RAW
MK = sys.argv[1]; EV0 = "2010-01-01"
if MK == "india":
    px = pd.read_parquet(RAW/"prices_tune.parquet"); ex = pd.read_parquet(RAW/"extra_tune.parquet"); idx = ex["^CRSLDX"].dropna(); b = pd.read_parquet(RAW/"bench_tune.parquet").iloc[:,0]; tri = ex["NIFTYBEES.NS"].dropna(); cost, cash = 25, 0.06
else:
    px = pd.read_parquet(RAW/"us_prices_tune.parquet"); ex = pd.read_parquet(RAW/"us_extra_tune.parquet"); idx = ex["^GSPC"].dropna(); b = idx; tri = ex["SPY"].dropna(); cost, cash = 10, 0.01
reg = idx > idx.rolling(200).mean(); SC = scores(px)
GRID = list(itertools.product(["S_mom", "S_mom_vol"], [0.30, 0.40, 0.50], [15, 25, 40], [True, False]))
def run(c):
    sc, stop, n, xma = c
    eq, tr = bt.backtest(px, b, top_n=n, stop=stop, cost_bps=cost, regime=True, regime_series=reg, score=SC[sc], cash_rate=cash, start=EV0, keep_winners=True, exit_ma_break=xma)
    e = eq.loc[EV0:]; e = e / e.iloc[0]; m = bt.metrics(e); t = pd.DataFrame(tr, columns=["t", "e", "x", "w"]).dropna(); r = t.x / t.e - 1
    return dict(score=sc, stop=stop, top_n=n, exit_ma=xma, CAGR=m["CAGR"], MaxDD=m["MaxDD"], trades=len(t), hit=(r > 0).mean(), n3x=int((r >= 2).sum()), n5x=int((r >= 4).sum()), avg_win=r[r > 0].mean(), worst=r.min())
if __name__ == "__main__":
    with Pool(4) as p: rows = p.map(run, GRID)
    df = pd.DataFrame(rows); df.to_csv(f"/home/user/multibagger-lab/results/tune/hold_grid_{MK}.csv", index=False)
    pd.set_option("display.width", 220, "display.float_format", lambda v: f"{v:,.3f}")
    c, d = (lambda e: (bt.metrics(e.loc[EV0:] / e.loc[EV0:].iloc[0])["CAGR"], bt.metrics(e.loc[EV0:] / e.loc[EV0:].iloc[0])["MaxDD"]))(tri)
    print(f"== {MK.upper()} hold-winners grid (benchmark {c:.3f}/{d:.3f}); cells with MaxDD better than benchmark: {(df.MaxDD > d).sum()}/36; median CAGR {df.CAGR.median():.3f}, median MaxDD {df.MaxDD.median():.3f}")
    print(df.sort_values("MaxDD", ascending=False).head(10).to_string(index=False)); print("\nbest CAGR:"); print(df.sort_values("CAGR", ascending=False).head(5).to_string(index=False))
    print("\nby stop:", df.groupby("stop")[["CAGR", "MaxDD", "n3x", "n5x"]].mean().round(3).to_dict("index")); print("by exit_ma:", df.groupby("exit_ma")[["CAGR", "MaxDD", "n3x", "n5x"]].mean().round(3).to_dict("index"))
