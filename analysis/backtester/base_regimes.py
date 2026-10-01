"""Base case, regime table, baselines (benchmark, TRI approx, equal-weight). Prints markdown; saves curves."""
from common import *
eq, tr = run()
m = summ(eq, tr)
bench = data_loader.window(BENCH.loc[START:], START)
yrs_idx = (bench.index - bench.index[0]).days / 365.25
tri = bench * (1.013 ** np.asarray(yrs_idx))
live0 = PX.loc[START:].iloc[0].notna()
cols = live0[live0].index
bh = PX[cols].ffill().loc[START:]; bh = bh / bh.iloc[0]; bh = bh.mean(axis=1)           # true buy&hold of 272 names live on 2010-01-04
ewd = PX.ffill().pct_change().loc[START:]; ewd = ewd.where(PX.loc[START:].notna() | PX.shift(1).loc[START:].notna())
ewd_r = ewd.mean(axis=1).fillna(0); ewd_curve = (1 + ewd_r).cumprod()                      # daily-rebalanced EW of names with data (universe grows 272->361)
curves = {"Strategy (base)": eq, "Nifty 50 price (^NSEI)": bench, "Nifty approx TRI (+1.3%/yr)": tri,
          "EW buy&hold, 272 names live 2010": bh * config.START_CAPITAL_INR / 1.0,
          "EW daily-rebal, all names with data": ewd_curve * config.START_CAPITAL_INR}
curves["EW buy&hold, 272 names live 2010"] = curves["EW buy&hold, 272 names live 2010"].reindex(eq.index).ffill()
curves["EW daily-rebal, all names with data"] = curves["EW daily-rebal, all names with data"].reindex(eq.index).ffill()
pd.DataFrame(curves).to_csv(ROOT / "results/tune/base_curves.csv")

print("BASE", {k: (round(float(v), 4)) for k, v in m.items()})
print("\n### Full window 2010-01-04 to 2018-12-31")
print("| Series | CAGR | MaxDD | MaxDD Rs | Sharpe | Final value |\n|---|---|---|---|---|---|")
for n, c in curves.items():
    s = summ(c.dropna()); print(f"| {n} | {s['CAGR']:.1%} | {s['MaxDD']:.1%} | {inr(s['MaxDD_Rs'])} | {s['Sharpe']:.2f} | {inr(s['FinalRs'])} |")

regs = {"2010-11 (weak)": ("2010-01-01", "2011-12-31"), "2012-13 (sideways)": ("2012-01-01", "2013-12-31"),
        "2014-15 (bull)": ("2014-01-01", "2015-12-31"), "2016": ("2016-01-01", "2016-12-31"),
        "2017 (bull)": ("2017-01-01", "2017-12-31"), "2018 (mid/small DD)": ("2018-01-01", "2018-12-31")}
def seg(c, a, b):
    s = c.loc[a:b]; return s / s.iloc[0]
print("\n### Regimes (each segment rebased to Rs 10,00,000 at start; strategy trades continuously)")
print("| Regime | Series | CAGR/Return | MaxDD | End value | Months up |\n|---|---|---|---|---|---|")
for rn, (a, b) in regs.items():
    for n in ["Strategy (base)", "Nifty 50 price (^NSEI)", "Nifty approx TRI (+1.3%/yr)", "EW buy&hold, 272 names live 2010"]:
        s = seg(curves[n], a, b); mm = bt.metrics(s)
        tot = s.iloc[-1] - 1
        mo = s.resample("ME").last().pct_change().dropna(); mo = (mo > 0).mean()
        print(f"| {rn} | {n} | ret {tot:+.1%} (CAGR {mm['CAGR']:.1%}) | {mm['MaxDD']:.1%} | {inr(s.iloc[-1]*1e6)} | {mo:.0%} |")
print("\nTrade stats (whole window, base):", {k: round(float(v), 4) for k, v in m.items() if k in ["Trades","HitRate","Over2x","Over5x","WorstTrade","AvgWin","AvgLoss"]})
# exposure: share of days in cash
r = eq.pct_change().dropna(); print("Days with exactly zero return (flat/cash proxy):", f"{(r==0).mean():.1%}")
# calendar-year
print("\n### Calendar years")
print("| Year | Strategy | Nifty price | Nifty TRI approx | Strat MDD | Nifty MDD |\n|---|---|---|---|---|---|")
for y in range(2010, 2019):
    a, b = f"{y}-01-01", f"{y}-12-31"
    def yr(c):
        s = c.loc[:b]; prev = c.loc[:str(y-1)+"-12-31"]
        base = prev.iloc[-1] if len(prev) else c.iloc[0]
        s = c.loc[a:b]; return s.iloc[-1]/base-1, (s/s.cummax()-1).min()
    ys, ds = yr(curves["Strategy (base)"]); yb, db = yr(curves["Nifty 50 price (^NSEI)"]); yt, _ = yr(curves["Nifty approx TRI (+1.3%/yr)"])
    print(f"| {y} | {ys:+.1%} | {yb:+.1%} | {yt:+.1%} | {ds:.1%} | {db:.1%} |")
