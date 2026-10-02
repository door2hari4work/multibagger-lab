import sys, numpy as np, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, "/home/user/multibagger-lab/analysis/improve")
from common import *

px, b, n500, tri = load()
REG = regimes(px, b, n500); SC = scores(px)
CAND = dict(top_n=25, stop=0.30, cost_bps=25, regime=True, regime_series=REG["R1_nifty500_ma200"], score=SC["S_mom_vol"], cash_rate=CASH, start=START)

def rnd(a):
    mode, seed = a
    eq, _ = bt.backtest(px, b, mode=mode, seed=seed, **CAND); return mode, seed, *stats(eq)
def cost(c):
    k = dict(CAND); k["cost_bps"] = c; eq, tr = bt.backtest(px, b, **k); return c, *stats(eq)

if __name__ == "__main__":
    out = []
    with Pool(4) as p:
        rows = p.map(rnd, [(m, s) for m in ("random", "random_all") for s in range(150)])
        costs = p.map(cost, [25, 50, 75, 100, 150])
    df = pd.DataFrame(rows, columns=["mode", "seed", "CAGR", "MaxDD"]); df.to_csv("/home/user/multibagger-lab/results/tune/cand_random.csv", index=False)
    eq, tr = bt.backtest(px, b, **CAND); c, d = stats(eq)
    print("CANDIDATE", round(c, 3), round(d, 3), "final Rs", f"{config.START_CAPITAL_INR*eq.iloc[-1]/eq.loc[START:].iloc[0]:,.0f}")
    for m in ("random", "random_all"):
        x = df[df["mode"] == m]
        print(m, "CAGR median", round(x.CAGR.median(), 3), "| share of seeds with CAGR below cand", round((x.CAGR < c).mean(), 3),
              "| MaxDD median", round(x.MaxDD.median(), 3), "| share of seeds with MaxDD WORSE than cand", round((x.MaxDD < d).mean(), 3))
    print("costs", [(a, round(b_, 3), round(c_, 3)) for a, b_, c_ in costs])
    t = pd.DataFrame(tr, columns=["t", "e", "x", "why"]).dropna(); t["r"] = t.x / t.e - 1
    print("trades", len(t), "hit", round((t.r > 0).mean(), 3), "5x", int((t.r >= 4).sum()), "worst", round(t.r.min(), 3))
    # drop top-3 contributing names (by sum of trade pnl proportion)
    top = t.groupby("t").r.sum().sort_values(ascending=False).head(3).index.tolist(); print("top3", top)
    px2 = px.drop(columns=top); k = dict(CAND); eq2, _ = bt.backtest(px2, b, **k); print("drop top3 names ->", [round(v, 3) for v in stats(eq2)])
    ey = eq.loc[START:].resample("YE").last().pct_change(); print("by year", ey.round(3).to_dict())
