"""Staged-entry / averaging-down simulation on daily adjusted closes (yfinance). Mechanical comparison of ENTRY SCHEDULES only.
CAUTION (survivorship / hindsight): the single stocks are today's winners (the investor's own holdings); their up-drift flatters every schedule that
invests early. Read the DIFFERENCES between schedules and the bad-start rows, not the absolute returns. QQQ, SPY and the Nifty 50 are the less-biased references.
Planned position = 1.0. Un-invested part sits in cash at 0%. Horizon = 252 trading days after the first purchase. No costs/taxes."""
import numpy as np, pandas as pd
from common import load_prices, OUT
import os
P = load_prices()
TICK = ["MSFT", "GOOGL", "TSM", "AMZN", "NVDA", "MU", "META", "APH", "BNY"]
REF = ["QQQ", "SPY", "^NSEI"]
H = 252; STEP = 5; Q = 0.225   # stress threshold = midpoint of the investor's 20-25% limit

def run(p, i, strat):
    """p: np array of prices; i: start index. Returns (final P&L on planned capital, worst P&L within horizon, invested fraction at end)."""
    end = i + H; ma200 = pd.Series(p).rolling(200).mean().values if "ma" in strat else None
    buys = []                                    # (day index, fraction)
    kind = strat["kind"]; n = strat.get("n", 1); gap = strat.get("gap", 21)
    if kind == "lump": buys = [(i, 1.0)]
    elif kind == "time":
        for k in range(n): buys.append((i + k * gap, 1.0 / n))
    elif kind in ("time_pause_dd", "time_pause_ma"):
        buys = [(i, 1.0 / n)]; nxt = i + gap; k = 1
        while k < n and nxt <= end:
            ok = (p[nxt] >= (1 - strat["dd"]) * p[i]) if kind == "time_pause_dd" else (p[nxt] > ma200[nxt])
            if ok: buys.append((nxt, 1.0 / n)); k += 1
            nxt += gap                          # a skipped tranche is retried each `gap` days until the window ends
    elif kind == "ladder":                      # first tranche now; next tranche when price is `step` below the PREVIOUS tranche price
        buys = [(i, 1.0 / n)]; last = p[i]; k = 1
        for t in range(i + 1, end + 1):
            if k >= n: break
            if p[t] <= last * (1 - strat["step"]): buys.append((t, 1.0 / n)); last = p[t]; k += 1
    idx = np.arange(i, end + 1); sh = np.zeros(len(idx)); cost = np.zeros(len(idx))
    for d, f in buys:
        if d > end: continue
        sh[d - i:] += f / p[d]; cost[d - i:] += f
    pnl = sh * p[i:end + 1] - cost
    return pnl[-1], pnl.min(), cost[-1]

STRATS = {
    "LUMP now": dict(kind="lump"),
    "3 tranches / 21d": dict(kind="time", n=3, gap=21),
    "4 tranches / 21d": dict(kind="time", n=4, gap=21),
    "6 tranches / 21d": dict(kind="time", n=6, gap=21),
    "3 x 21d, skip if >15% below 1st": dict(kind="time_pause_dd", n=3, gap=21, dd=0.15),
    "3 x 21d, skip if below 200d MA": dict(kind="time_pause_ma", n=3, gap=21, ma=1),
    "ladder 3: add at -10% steps": dict(kind="ladder", n=3, step=0.10),
    "ladder 3: add at -20% steps": dict(kind="ladder", n=3, step=0.20),
}
rows = []
for t in TICK + REF:
    s = P[t].dropna(); p = s.values
    first = 200 if any("ma" in v for v in STRATS.values()) else 0
    for i in range(first, len(p) - H - 1, STEP):
        lump_ret = p[i + H] / p[i] - 1
        for name, st in STRATS.items():
            f, w, inv = run(p, i, st); rows.append((t, s.index[i], name, f, w, inv, lump_ret))
D = pd.DataFrame(rows, columns=["t", "start", "strat", "final", "worst", "invested", "lump_ret"])
def summ(d):
    g = d.groupby("strat", sort=False)
    return pd.DataFrame({"n": g.size(), "median_12m": g["final"].median(), "p10_12m": g["final"].quantile(0.10), "worst_12m": g["final"].min(),
                         "pct_dip_beyond_-22.5%": g["worst"].apply(lambda x: (x < -Q).mean()), "median_worst_dip": g["worst"].median(), "p5_worst_dip": g["worst"].quantile(0.05),
                         "avg_invested_end": g["invested"].mean()})
pd.set_option("display.width", 220); pd.set_option("display.float_format", lambda x: f"{x:,.3f}")
stocks = D[D.t.isin(TICK)]
print("== A. Pooled 9 single stocks (equal weight by start; survivorship-biased up-drift), all start dates"); print(summ(stocks).to_string())
print("\n== B. Same, only BAD starts (lump-sum 12m return < -20%): n =", (stocks[stocks.strat == "LUMP now"].lump_ret < -0.20).sum())
bad = stocks[stocks.lump_ret < -0.20]; print(summ(bad).to_string())
print("\n== C. Same, only STRONG starts (lump-sum 12m return > +50%)")
good = stocks[stocks.lump_ret > 0.50]; print(summ(good).to_string()[:3000])
for r in REF:
    print("\n== D. Reference:", r); print(summ(D[D.t == r]).to_string())
# per-ticker lump vs 3x21 vs ladder
print("\n== E. Per ticker: share of starts whose within-12m dip on the planned position exceeded -22.5%  (LUMP / 3x21d / 6x21d / ladder-20)")
tab = D[D.strat.isin(["LUMP now", "3 tranches / 21d", "6 tranches / 21d", "ladder 3: add at -20% steps"])].groupby(["t", "strat"])["worst"].apply(lambda x: (x < -Q).mean()).unstack()
print(tab.round(3).to_string())
# worked failure case for averaging down: starts at known peaks
print("\n== F. Averaging-down failure case: start on the last ATH before the big drawdown, 12m outcome on the planned position")
for t, d in [("META", "2021-09-07"), ("NVDA", "2007-10-17"), ("MU", "2006-09-11"), ("TSM", "2022-01-14"), ("MSFT", "2007-11-01"), ("QQQ", "2021-12-27"), ("^NSEI", "2008-01-08")]:
    s = P[t].dropna(); i = s.index.get_indexer([pd.Timestamp(d)], method="nearest")[0]; p = s.values
    out = {n: run(p, i, st) for n, st in STRATS.items() if i + H < len(p)}
    print(t, d, " | ".join("%s: end %+.0f%% worst %+.0f%% inv %.2f" % (n.split(":")[0][:22], 100 * v[0], 100 * v[1], v[2]) for n, v in out.items() if n in ("LUMP now", "3 tranches / 21d", "ladder 3: add at -10% steps", "ladder 3: add at -20% steps")))
