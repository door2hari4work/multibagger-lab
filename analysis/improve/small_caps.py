"""Frozen-style engine on small/micro universes, TUNE WINDOW ONLY. Costs raised for illiquidity (assumption): India small 40 bps, micro 75 bps, US small 15 bps per side.
Universes are today's members = survivor-biased, worst for micro caps. Random baselines = 15 seeds each (same regime/filters = 'random', no filters = 'random_all')."""
import sys, numpy as np, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, "/home/user/multibagger-lab/analysis/improve"); sys.path.insert(0, "/home/user/multibagger-lab")
import backtest as bt
from common import scores, RAW
EV0 = "2010-01-01"
ex_in = pd.read_parquet(RAW/"extra_tune.parquet"); ex_us = pd.read_parquet(RAW/"us_extra_tune.parquet")
n5 = pd.read_parquet(RAW/"prices_tune.parquet")
def _u(f): return set(pd.read_csv(RAW/f)["Symbol"].str.strip() + ".NS")
U = {
 "india_mid": (n5[[c for c in n5.columns if c in _u("ind_niftymidcap150list.csv")]], ex_in["^CRSLDX"].dropna(), ex_in["NIFTYBEES.NS"].dropna(), 25, 0.06),
 "india_small": (n5[[c for c in n5.columns if c in _u("ind_niftysmallcap250list.csv")]], ex_in["^CRSLDX"].dropna(), ex_in["NIFTYBEES.NS"].dropna(), 40, 0.06),
 "india_micro": (pd.read_parquet(RAW/"micro_prices_tune.parquet"), ex_in["^CRSLDX"].dropna(), ex_in["NIFTYBEES.NS"].dropna(), 75, 0.06),
 "us_small": (pd.read_parquet(RAW/"sp600_prices_tune.parquet"), ex_us["^GSPC"].dropna(), ex_us["SPY"].dropna(), 15, 0.01),
}
def mk(u):
    px, idx, tri, cost, cash = U[u]; px = px.ffill(limit=5); reg = idx > idx.rolling(200).mean(); return px, idx, tri, cost, cash, reg, scores(px)["S_mom_vol"]
def st(eq):
    e = eq.loc[EV0:]; e = e / e.iloc[0]; m = bt.metrics(e); return m["CAGR"], m["MaxDD"]
def run(a):
    u, kind, seed = a; px, idx, tri, cost, cash, reg, sc = mk(u)
    kw = dict(top_n=25, stop=0.30, cost_bps=cost, regime=True, regime_series=reg, score=sc, cash_rate=cash, start=EV0)
    if kind == "hold": kw.update(top_n=40, stop=0.40, keep_winners=True)
    if kind in ("random", "random_all"): kw.update(mode=kind, seed=seed)
    eq, tr = bt.backtest(px, idx, **kw); c, d = st(eq); t = pd.DataFrame(tr, columns=["t", "e", "x", "w"]).dropna(); r = t.x / t.e - 1
    return dict(u=u, kind=kind, seed=seed, CAGR=c, MaxDD=d, n3x=int((r >= 2).sum()), n5x=int((r >= 4).sum()), trades=len(t), worst=r.min() if len(r) else np.nan)
if __name__ == "__main__":
    jobs = [(u, k, s) for u in U for k, ss in (("rebal", [0]), ("hold", [0]), ("random", range(15)), ("random_all", range(15))) for s in ss]
    with Pool(4) as p: df = pd.DataFrame(p.map(run, jobs))
    pd.set_option("display.width", 200, "display.float_format", lambda v: f"{v:,.3f}")
    for u in U:
        px, idx, tri, cost, cash, reg, sc = mk(u); c, d = st(tri); r = px.loc[EV0:].pct_change(fill_method=None).mean(axis=1).fillna(0); e = (1 + r).cumprod(); ec, ed = st(e)
        x = df[df.u == u]; print(f"\n== {u} | names alive 2010: {int(px.loc[EV0:].iloc[0].notna().sum())} of {px.shape[1]} | benchmark TRI proxy {c:.3f}/{d:.3f} | EW hold of survivors {ec:.3f}/{ed:.3f}")
        for k in ("rebal", "hold"):
            y = x[x.kind == k].iloc[0]; print(f"  {k:6s} CAGR {y.CAGR:.3f} MaxDD {y.MaxDD:.3f} | trades {y.trades} | >=3x {y.n3x} | >=5x {y.n5x} | worst trade {y.worst:.2f}")
        for k in ("random", "random_all"):
            y = x[x.kind == k]; print(f"  {k:10s} median CAGR {y.CAGR.median():.3f} median MaxDD {y.MaxDD.median():.3f}")
    df.to_csv("/home/user/multibagger-lab/results/tune/small_caps.csv", index=False)
