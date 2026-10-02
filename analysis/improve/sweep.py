import itertools, sys, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, "/home/user/multibagger-lab/analysis/improve")
from common import *

px, b, n500, tri = load()
REG = regimes(px, b, n500); SC = scores(px)
GRID = list(itertools.product(REG.keys(), SC.keys(), [None, 0.15, 0.20], [15, 25]))

def run(cfg):
    r, s, brk, n = cfg
    eq, tr = bt.backtest(px, b, top_n=n, stop=0.30, cost_bps=25, regime=(r != "R5_none"), regime_series=REG[r],
                         score=SC[s], dd_breaker=brk, cash_rate=CASH, start=START)
    c, d = stats(eq); c1, d1 = stats(eq, START, "2014-12-31"); c2, d2 = stats(eq, "2015-01-01", "2018-12-31")
    e18 = eq.loc["2018-01-01":"2018-12-31"]; y18 = e18.iloc[-1] / e18.iloc[0] - 1
    fin = config.START_CAPITAL_INR * eq.iloc[-1] / eq.loc[START:].iloc[0]
    return dict(regime=r, score=s, breaker=brk, top_n=n, CAGR=c, MaxDD=d, CAGR_1014=c1, DD_1014=d1, CAGR_1518=c2, DD_1518=d2,
                ret2018=y18, final_rs=round(fin), trades=len(tr))

if __name__ == "__main__":
    with Pool(4) as p: rows = p.map(run, GRID)
    df = pd.DataFrame(rows); df.to_csv("/home/user/multibagger-lab/results/tune/improve_grid.csv", index=False)
    pd.set_option("display.width", 250, "display.float_format", lambda x: f"{x:,.3f}")
    print(df.sort_values("MaxDD", ascending=False).head(15).to_string(index=False))
    c, d = stats(tri); print("\nNifty BeES (TRI proxy) CAGR/MaxDD:", round(c, 3), round(d, 3))
    print("cells with MaxDD better than -27.3%:", int((df.MaxDD > -0.273).sum()), "of", len(df))
