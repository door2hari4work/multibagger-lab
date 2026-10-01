from common import *
import indep
px, b = load(); pxf = indep.prep(px); dates = pxf.index
def ev(eq):
    e = eq.loc[START:]; return e/e.iloc[0]
sig = indep.signals(pxf, b)
eq, tr = indep.sim(pxf, b, sig=sig); base = met(ev(eq)); print("base", base)
td = indep.trades_df(tr, dates); td = td[td.edate >= pd.Timestamp(START)].copy()

# ---------------- data quality: stale runs / jumps inside held windows
def stale_runs(px, minrep):
    out = []
    for t in px.columns:
        s = px[t].dropna()
        if len(s) < 2: continue
        same = (s.diff() == 0); grp = (~same).cumsum()
        L = same.groupby(grp).sum()
        for g, n in L[L >= minrep].items():
            idx = s.index[grp == g]; out.append((t, idx[0], idx[-1], int(n)))
    return pd.DataFrame(out, columns=["name","start","end","rep"])
sr5 = stale_runs(px, 5)
r = px.pct_change()
def touched(row):
    sub = sr5[(sr5.name == row["name"]) & (sr5.end >= row.edate) & (sr5.start <= row.xdate)]
    jump = (r[row["name"]].loc[row.edate:row.xdate].abs() > 0.40).any()
    return (len(sub) > 0) or jump
td["stale_or_jump"] = td.apply(touched, axis=1)
print("trades overlapping a stale run>=5 bars or a >40%% 1-day move: %d of %d (%.1f%%); share of sum pnl %.1f%%" % (
    td.stale_or_jump.sum(), len(td), 100*td.stale_or_jump.mean(), 100*td[td.stale_or_jump].pnl_frac.sum()/td.pnl_frac.sum()))
print(td[td.stale_or_jump].sort_values("pnl_frac", ascending=False)[["name","edate","xdate","ret","why"]].head(12).to_string())
# cleaned prices: blank everything up to the end of any stale run >=20 bars, and up to any single-day drop < -45%
sr20 = stale_runs(px, 20); pc = px.copy()
for _, x in sr20.iterrows(): pc.loc[:x.end, x["name"]] = np.nan
dd = r[(r < -0.45)].stack().dropna()
for (d, t) in dd.index: pc.loc[:d, t] = np.nan
print("cleaned: masked names", sorted(set(sr20.name) | set(t for _, t in dd.index)))
eqc, trc = indep.sim(indep.prep(pc), b); print("CLEANED data:", met(ev(eqc)))

# ---------------- concentration + drop-top-N
bn = td.groupby("name").pnl_frac.sum().sort_values(ascending=False)
share = bn / bn.sum()
print("\nTop 10 names by share of total P&L (sum over trades of entry value x return):")
print(pd.DataFrame({"share_of_pnl": share.head(10).round(3), "n_trades": td.groupby("name").size().reindex(share.head(10).index)}).to_string())
print("top3 share %.1f%%, top5 %.1f%%, top10 %.1f%% | names traded %d" % (100*share.head(3).sum(), 100*share.head(5).sum(), 100*share.head(10).sum(), len(bn)))
rows = []
for k in (0, 1, 3, 5, 10):
    drop = list(bn.index[:k]); p2 = indep.prep(px.drop(columns=drop))
    e2, t2 = indep.sim(p2, b); m = met(ev(e2)); rows.append(dict(dropped=k, **m)); print("drop top", k, [d for d in drop], {a: round(v, 4) for a, v in m.items()})
# control: drop 3 RANDOM traded names, 60 draws
rng = np.random.default_rng(0); cs = []
traded = list(bn.index)
for _ in range(60):
    drop = list(rng.choice(traded, 3, replace=False)); e2, _ = indep.sim(indep.prep(px.drop(columns=drop)), b); cs.append(met(ev(e2))["CAGR"])
print("drop 3 random traded names: CAGR mean %.4f sd %.4f min %.4f" % (np.mean(cs), np.std(cs), np.min(cs)))
pd.DataFrame(rows).to_csv("out_drop_top.csv", index=False)
# CAGR if the top-3 are removed AND data-cleaned
e3, _ = indep.sim(indep.prep(pc.drop(columns=list(bn.index[:3]))), b); print("cleaned + drop top3:", met(ev(e3)))

# ---------------- ratio of trade-level: hit rate etc.
print("trade P&L: median ret %.3f, mean %.3f; share of trades >= +50%%: %.3f; sum pnl positive from top-decile trades %.1f%%" % (
    td.ret.median(), td.ret.mean(), (td.ret >= .5).mean(), 100*td.sort_values("pnl_frac", ascending=False).pnl_frac.head(int(len(td)*.1)).sum()/td.pnl_frac.sum()))
td.to_csv("out_trades_base.csv", index=False)
