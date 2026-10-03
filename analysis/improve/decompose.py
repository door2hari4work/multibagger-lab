"""Where does the edge/drawdown protection come from? TUNE WINDOW ONLY, India and US, same engine, 20 seeds for random variants."""
import sys, numpy as np, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, "/home/user/multibagger-lab/analysis/improve"); sys.path.insert(0, "/home/user/multibagger-lab")
import backtest as bt
from common import scores, RAW
MK = sys.argv[1]; EV0 = "2010-01-01"
if MK == "india":
    px = pd.read_parquet(RAW/"prices_tune.parquet"); ex = pd.read_parquet(RAW/"extra_tune.parquet"); idx = ex["^CRSLDX"].dropna(); b = pd.read_parquet(RAW/"bench_tune.parquet").iloc[:,0]; tri = ex["NIFTYBEES.NS"].dropna(); cost, cash = 25, 0.06
else:
    px = pd.read_parquet(RAW/"us_prices_tune.parquet"); ex = pd.read_parquet(RAW/"us_extra_tune.parquet"); idx = ex["^GSPC"].dropna(); b = idx; tri = ex["SPY"].dropna(); cost, cash = 10, 0.01
reg = idx > idx.rolling(200).mean(); on = pd.Series(True, index=px.index); SC = scores(px); N = 25
def cfg(regime, score, mode="momentum", n=N): return dict(top_n=n, stop=0.30, cost_bps=cost, regime=regime, regime_series=reg if regime else on, score=score, cash_rate=cash, start=EV0, mode=mode)
V = {
 "D0 regime + random 200 of ALL names (no selection)": (cfg(True, SC["S_mom"], "random_all", 200), True),
 "D1 regime + filters + random 25": (cfg(True, SC["S_mom"], "random"), True),
 "D2 regime + filters + momentum rank 25": (cfg(True, SC["S_mom"]), False),
 "D3 regime + filters + mom/vol rank 25 (candidate)": (cfg(True, SC["S_mom_vol"]), False),
 "D4 NO regime + filters + mom/vol rank 25": (cfg(False, SC["S_mom_vol"]), False),
 "D5 NO regime + random 25 of ALL names": (cfg(False, SC["S_mom"], "random_all"), True),
 "D6 NO regime + filters + random 25": (cfg(False, SC["S_mom"], "random"), True),
}
def st(eq):
    e = eq.loc[EV0:]; e = e / e.iloc[0]; m = bt.metrics(e); return m["CAGR"], m["MaxDD"]
def run(a):
    name, seed = a; k, rnd = V[name]; eq, _ = bt.backtest(px, b, seed=seed, **k); return name, seed, *st(eq)
if __name__ == "__main__":
    jobs = [(n, s) for n, (k, r) in V.items() for s in (range(20) if r else [0])]
    with Pool(4) as p: rows = p.map(run, jobs)
    df = pd.DataFrame(rows, columns=["variant", "seed", "CAGR", "MaxDD"]).groupby("variant").agg(CAGR=("CAGR", "median"), MaxDD=("MaxDD", "median"), runs=("seed", "count"))
    c, d = st(tri); pd.set_option("display.width", 200, "display.float_format", lambda v: f"{v:,.3f}")
    print(f"== {MK.upper()} tune 2010-2018 (random variants = median of 20 seeds) | benchmark TRI proxy {c:.3f} / {d:.3f}"); print(df.to_string())
