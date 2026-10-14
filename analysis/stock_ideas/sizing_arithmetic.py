"""Risk-budget arithmetic for position sizing. loss (pp of net worth) = position weight (% NW) x plausible drawdown.
Sleeve limit L = the investor's stated 20-25% fall on money invested (midpoint 22.5% used). Data: yfinance adjusted closes."""
import numpy as np, pandas as pd, os
from common import load_prices, OUT
from weights import HOLDINGS
P = load_prices(); pd.set_option("display.width", 200); pd.set_option("display.float_format", lambda x: f"{x:,.3f}")
L = [0.20, 0.225, 0.25]
print("== 1. Max share of a sleeve that can sit in an asset with stress drawdown d, if the sleeve may lose L (rest in cash at 0%):  share = L / d")
tab = pd.DataFrame({f"L={int(l*1000)/10}%": {f"d={int(d*100)}%": min(1.0, l / d) for d in [0.25, 0.30, 0.35, 0.40, 0.50, 0.60, 0.70, 0.90]} for l in L}); print(tab.round(2).to_string())

print("\n== 2. Plausible drawdown inputs measured on the investor's instruments (adjusted closes; start 2005 or listing)")
def maxdd(s):
    s = s.dropna(); dd = s / s.cummax() - 1; return dd.min()
rows = []
for t in ["MSFT", "GOOGL", "AMZN", "META", "TSM", "NVDA", "MU", "APH", "BNY", "QQQ", "SMH", "SPY"]:
    s = P[t].dropna(); w20 = s.loc["2020-02-19":"2020-03-23"]; w22 = s.loc["2021-11-01":"2022-12-31"]
    rows.append((t, maxdd(s), maxdd(w22), w20.min() / w20.iloc[0] - 1))
for t, nm in [("^NSEI", "Nifty 50 (price)"), ("MID150BEES.NS", "Nifty Midcap 150 ETF")]:
    s = P[t].dropna(); w20 = s.loc["2020-02-19":"2020-03-23"]; w22 = s.loc["2021-11-01":"2022-12-31"]; rows.append((nm, maxdd(s), maxdd(w22), w20.min() / w20.iloc[0] - 1))
I = pd.DataFrame(rows, columns=["inst", "worst_since_start", "worst_2021-11..2022-12", "own_min_Feb19-Mar23_2020"]).set_index("inst"); print(I.round(3).to_string())
I.to_csv(os.path.join(OUT, "dd_inputs.csv"))

print("\n== 3. Sleeve-level evidence: equal-weight basket of the 8 US names (monthly rebalanced) since 2012-06; within-12m worst dip on money invested")
names = ["MSFT", "GOOGL", "TSM", "AMZN", "NVDA", "MU", "META", "APH"]
r = P[names].loc["2012-06-01":].pct_change().dropna()
def basket(r, cols, inv=1.0):
    m = r[cols].resample("ME").apply(lambda x: (1 + x).prod() - 1)   # monthly return of each name; equal weight rebalanced monthly
    # daily path with monthly rebalance:
    out = []; 
    for _, g in r[cols].groupby(pd.Grouper(freq="ME")):
        cum = (1 + g).cumprod().mean(axis=1); out.append(cum / 1.0)
    # chain months
    v = 1.0; path = []
    for _, g in r[cols].groupby(pd.Grouper(freq="ME")):
        cum = (1 + g).cumprod().mean(axis=1) * v; path.append(cum); v = cum.iloc[-1]
    b = pd.concat(path); return b
b = basket(r, names); dd = (b / b.cummax() - 1)
print("basket max drawdown %.1f%% (trough %s); worst 12m dip share below -22.5%% at inv=100%%: " % (dd.min() * 100, dd.idxmin().date()), end="")
def dips(b, inv, win=252, step=5):
    out = []; v = b.values
    for i in range(0, len(v) - win, step): out.append((v[i:i + win + 1] / v[i] - 1).min() * inv)
    return np.array(out)
for inv in (1.0, 0.75, 0.5):
    d = dips(b, inv); print("\n   invested %3d%%: share of 12m windows with dip beyond -22.5%% on the sleeve: %.1f%% ; median dip %.1f%% ; p5 dip %.1f%% ; worst %.1f%%" % (inv * 100, (d < -0.225).mean() * 100, np.median(d) * 100, np.percentile(d, 5) * 100, d.min() * 100))
sub = ["MSFT", "GOOGL", "AMZN", "META"]; bq = basket(r, sub); ddq = bq / bq.cummax() - 1
print("   mega-cap 4 only: basket maxDD %.1f%% ; share of 12m windows beyond -22.5%% at inv 100%%: %.1f%%" % (ddq.min() * 100, (dips(bq, 1.0) < -0.225).mean() * 100))
sem = ["TSM", "NVDA", "MU"]; bs = basket(r, sem); dds = bs / bs.cummax() - 1
print("   semis 3 only: basket maxDD %.1f%% ; share of 12m windows beyond -22.5%% at inv 100%%: %.1f%%" % (dds.min() * 100, (dips(bs, 1.0) < -0.225).mean() * 100))
print("   correlation of daily returns, avg pairwise among 8 names: %.2f ; in the 10%% worst SPY days: %.2f" % (r.corr().values[np.triu_indices(8, 1)].mean(),
      r[P['SPY'].pct_change().reindex(r.index) <= P['SPY'].pct_change().reindex(r.index).quantile(0.10)].corr().values[np.triu_indices(8, 1)].mean()))

print("\n== 4. Position and theme loss arithmetic (pp of net worth = weight x drawdown)")
cases = [("core mega-cap 7%", 7, 0.40), ("core mega-cap 7%, bad (2022 META-like -77%)", 7, 0.77), ("satellite 3%", 3, 0.60), ("satellite 3% total loss", 3, 1.0), ("satellite 2%", 2, 0.60), ("satellite 2% total loss", 2, 1.0),
         ("semis name 4% at -65%", 4, 0.65), ("employer 5% at -40%", 5, 0.40), ("employer 5.8% at -50%", 5.8, 0.50), ("employer 5.8% total loss", 5.8, 1.0)]
for c in cases: print("   %-45s %5.2f pp NW" % (c[0], c[1] * c[2]))
print("   AI theme look-through 31.3%%: at -25%% (Nasdaq-100 AI-bust implied) %.1f pp ; at -35%% %.1f pp ; at -45%% (SMH 2022) %.1f pp" % (31.32 * .25, 31.32 * .35, 31.32 * .45))
print("   Semis look-through 14.6%%: at -40%% %.1f pp ; at -65%% (SMH 2008 -64%%) %.1f pp" % (14.6 * .40, 14.6 * .64))
print("   If caps: AI 30%% x 35%% = %.1f pp ; AI 25%% x 35%% = %.1f ; semis 10%% x 55%% = %.1f ; semis 12%% x 55%% = %.1f" % (30 * .35, 25 * .35, 10 * .55, 12 * .55))
print("   Sector cap 25%% x 35%% = %.2f pp ; 20%% x 35%% = %.2f pp" % (25 * .35, 20 * .35))
