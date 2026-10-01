from common import *
pd.set_option("display.width", 250)
rb = pd.read_csv(ROOT/"results/tune/random_baselines.csv")
base = summ(*[run()[0]]) if False else None
eq, tr = run(); S = summ(eq, tr)
print("strategy", round(S["CAGR"],4), round(S["MaxDD"],4))
print("\n### Random baselines (200 seeds each, base params top_n=15 stop=30% regime ON, 25 bps)")
print("| Mode | n | CAGR mean | CAGR median | CAGR p5 | p95 | MaxDD median | MaxDD p5 (worst) | p95 (best) | Final Rs median | Sharpe median |\n|---|---|---|---|---|---|---|---|---|---|---|")
for mode, d in rb.groupby("mode"):
    q = lambda c, p: d[c].quantile(p)
    print(f"| {mode} | {len(d)} | {d.CAGR.mean():.1%} | {d.CAGR.median():.1%} | {q('CAGR',.05):.1%} | {q('CAGR',.95):.1%} | {d.MaxDD.median():.1%} | {q('MaxDD',.05):.1%} | {q('MaxDD',.95):.1%} | {inr(d.FinalRs.median())} | {d.Sharpe.median():.2f} |")
    print(f"   strategy CAGR percentile in {mode}: {(d.CAGR<S['CAGR']).mean():.1%} of seeds below it; MaxDD: {(d.MaxDD>S['MaxDD']).mean():.1%} of seeds had SHALLOWER drawdown than strategy; seeds beating strategy on CAGR: {(d.CAGR>=S['CAGR']).sum()}, shallower DD: {(d.MaxDD>S['MaxDD']).sum()}, both: {((d.CAGR>=S['CAGR'])&(d.MaxDD>S['MaxDD'])).sum()}")
    print(f"   seeds with BOTH higher CAGR and shallower MDD than strategy: see above; seeds with CAGR<8.5% (Nifty price): {(d.CAGR<0.085).sum()}")
# break-even
cs = pd.read_csv(ROOT/"results/tune/cost_stress.csv").sort_values("cost_bps")
def be(target):
    x, y = cs.cost_bps.values, cs.CAGR.values
    for i in range(len(x)-1):
        if y[i] >= target >= y[i+1]: return x[i] + (y[i]-target)/(y[i]-y[i+1])*(x[i+1]-x[i])
    return np.nan
c = pd.read_csv(ROOT/"results/tune/base_curves.csv", index_col=0, parse_dates=True)
tg = {"Nifty price 8.5%": summ(c["Nifty 50 price (^NSEI)"])["CAGR"], "Nifty TRI approx": summ(c["Nifty approx TRI (+1.3%/yr)"])["CAGR"],
      "EW daily-rebal all names": summ(c["EW daily-rebal, all names with data"])["CAGR"], "EW buy&hold 272": summ(c["EW buy&hold, 272 names live 2010"])["CAGR"],
      "random_all median @25bps": rb[rb['mode']=='random_all'].CAGR.median(), "random median @25bps": rb[rb['mode']=='random'].CAGR.median()}
print("\n### Break-even cost bps/side (linear interp of CAGR vs cost) vs target CAGR")
for k, v in tg.items(): print(f"| {k} | {v:.1%} | {be(v):.0f} |")
print("\ncost table")
print("| cost bps/side | CAGR | MaxDD | Sharpe | Final value |\n|---|---|---|---|---|")
for _, r in cs.iterrows(): print(f"| {int(r.cost_bps)} | {r.CAGR:.1%} | {r.MaxDD:.1%} | {r.Sharpe:.2f} | {inr(r.FinalRs)} |")
# turnover proxy
print("\nTrades base:", S["Trades"], " (~", round(S["Trades"]/9.0), "/yr)")
# grid plateau
g = pd.read_csv(ROOT/"results/tune/grid.csv"); g["stop"] = g["stop"].where(g["stop"] < 1, np.nan)
print("\nGrid CAGR>Nifty price(8.5%):", (g.CAGR>0.085).mean(), " >EW buy&hold 22.9%:", (g.CAGR>0.229).mean(), " >random_all median:", (g.CAGR>tg['random_all median @25bps']).mean())
ra = rb[rb['mode']=='random_all']
print("grid cells with MaxDD shallower than Nifty -27.9%:", (g.MaxDD>-0.279).sum(), "of", len(g), "; shallower than random_all median:", (g.MaxDD>ra.MaxDD.median()).sum(), ";CAGR>rand_all median & MDD shallower than rand_all median:", ((g.CAGR>ra.CAGR.median())&(g.MaxDD>ra.MaxDD.median())).sum())
print("grid CAGR quantiles", g.CAGR.quantile([0,.1,.25,.5,.75,.9,1]).round(3).tolist())
# neighbours of the best cell
b = g.sort_values("CAGR", ascending=False).iloc[0]; print("best", b.to_dict())
# for each cell: mean CAGR of its one-step neighbours (differ in exactly one param)
params = ["top_n","stop","regime","lookback","ma"]
g["stopk"]=g["stop"].fillna(9)
def nb(row):
    m = g[(g[["top_n","stopk","regime","lookback","ma"]] != row[["top_n","stopk","regime","lookback","ma"]]).sum(axis=1)==1]
    return m.CAGR.mean(), m.CAGR.min()
g[["nbmean","nbmin"]] = g.apply(lambda r: pd.Series(nb(r)), axis=1)
g["drop"] = g.CAGR - g.nbmean
print(g.sort_values("CAGR",ascending=False).head(6)[params+["CAGR","nbmean","nbmin","drop"]].round(3).to_string())
print("median drop top-decile cells:", g.sort_values("CAGR",ascending=False).head(14)["drop"].median().round(3), "; overall CAGR std", g.CAGR.std().round(3))
print("base cell nbmean", g[(g.top_n==15)&(g.stop==0.3)&(g.regime)&(g.lookback==252)&(g.ma==200)][["CAGR","nbmean","nbmin"]].round(3).to_string())
print("corr of CAGR with MaxDD", g.CAGR.corr(g.MaxDD).round(2))
# grid summary tables per param, regime split
for c_ in ["top_n","stop","lookback","ma"]:
    print(g.groupby([c_,"regime"],dropna=False)[["CAGR","MaxDD"]].mean().round(3).unstack().to_string())
