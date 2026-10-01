from common import *
import indep
px, b = load(); pxf = indep.prep(px)
sig = indep.signals(pxf, b)
rows = []
for k in (-1, 0, 1, 2, 5):
    eq, tr = indep.sim(pxf, b, sig=sig, k=k)
    e = eq.loc[START:]; e = e/e.iloc[0]
    m = met(e); rows.append(dict(k=k, **m)); 
df = pd.DataFrame(rows); print(df.round(4).to_string(index=False))
df.to_csv("out_lookahead_shift.csv", index=False)
# also shift the SIGNAL date only (stale signals): use list from previous month-end
# ---- independent re-derivation of 4 trades, using nothing from indep.py/backtest.py
eq, tr = indep.sim(pxf, b, sig=sig, k=0)
td = indep.trades_df(tr, pxf.index)
td = td[td.why=="rebal"].sort_values("edate")
import random; random.seed(1)
sample = td.iloc[[5, 60, 150, 240]]
bm = b.reindex(pxf.index).ffill()
for _, r in sample.iterrows():
    nme = r["name"]; s = px[nme]               # RAW (un-ffilled) series
    ei = r.ei; sd = pxf.index[ei-1]           # signal bar = bar before fill
    # month-end check: signal bar must be last trading day of its month
    last_of_month = pxf.index[ei-1].month != pxf.index[ei].month
    c = s.loc[:sd]
    mom = c.iloc[-22] / c.iloc[-253] - 1
    ma200 = c.iloc[-200:].mean(); hi = c.iloc[-252:].max()
    cond = (c.iloc[-1] > ma200, mom > 0, c.iloc[-1] >= .75*hi)
    # rank among all names at signal bar
    allm = {}
    for t in px.columns:
        x = pxf[t].loc[:sd]
        if len(x) < 253 or x.iloc[-252:].isna().any(): continue
        m_ = x.iloc[-22]/x.iloc[-253]-1
        if x.iloc[-1] > x.iloc[-200:].mean() and m_ > 0 and x.iloc[-1] >= .75*x.iloc[-252:].max(): allm[t] = m_
    rank = sorted(allm, key=allm.get, reverse=True).index(nme) + 1
    regime = bm.loc[:sd].iloc[-1] > bm.loc[:sd].iloc[-200:].mean()
    print(f"{nme:14s} signal bar {sd.date()} (month-end={last_of_month}) fill bar {pxf.index[ei].date()} fill px {r.epx:.2f} "
          f"== raw close on fill bar {s.loc[pxf.index[ei]]:.2f}; conds(>MA200,mom>0,>=75%hi)={cond} rank={rank}/{len(allm)} regime={bool(regime)}")
    # exit
    print(f"    exit bar {r.xdate.date()} px {r.xpx:.2f}  ret {r.ret:+.1%}  why {r.why}")
