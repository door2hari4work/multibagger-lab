from common import *
import indep
px, b = load(); pxf = indep.prep(px); dates = pxf.index
def ev(eq, a=START, z=None):
    e = eq.loc[a:z]; return e/e.iloc[0]
sig = indep.signals(pxf, b)
eq, tr = indep.sim(pxf, b, sig=sig)
# EW buy&hold with the CURRENT (fixed) buy_hold, raw and cleaned
def clean(px):
    pc = px.copy(); r = px.pct_change(fill_method=None)
    import importlib
    for t in px.columns:
        s = px[t].dropna()
        if len(s) < 2: continue
        same = (s.diff() == 0); grp = (~same).cumsum(); L = same.groupby(grp).sum()
        for g, n in L[L >= 20].items(): pc.loc[:s.index[grp == g][-1], t] = np.nan
    for (d, t), v in r[r < -0.45].stack().dropna().items(): pc.loc[:d, t] = np.nan
    return pc
pc = clean(px)
for nm, p in (("raw", px), ("cleaned", pc)):
    print("EW buy&hold", nm, met(bt.buy_hold(p.loc[START:])))
for a, z in (("2010-01-01", "2014-12-31"), ("2015-01-01", "2018-12-31")):
    print(a, z, "strategy", met(ev(eq, a, z)), "| EW", met(bt.buy_hold(px.loc[a:z])), "| ^NSEI price", met(b.loc[a:z]/b.loc[a:z].iloc[0]))
# year by year
e = ev(eq); y = e.resample("YE").last(); y = y.pct_change(); y.iloc[0] = e.resample("YE").last().iloc[0] - 1
ew = bt.buy_hold(px.loc[START:]); ey = ew.resample("YE").last().pct_change(); ey.iloc[0] = ew.resample("YE").last().iloc[0]/1 - 1
by = b.loc[START:]; bq = by.resample("YE").last().pct_change(); bq.iloc[0] = by.resample("YE").last().iloc[0]/by.iloc[0] - 1
Y = pd.DataFrame({"strategy": y.values, "EW survivors": ey.values, "^NSEI price": bq.values}, index=y.index.year); print(Y.round(3).to_string())
yrs = (e.index[-1]-e.index[0]).days/365.25
for drop in ([2014], [2017], [2014, 2017]):
    g = np.prod([1+Y.loc[k, "strategy"] for k in Y.index if k not in drop]); n = len(Y) - len(drop)
    print("strategy geometric mean/yr excluding years", drop, "=%.3f" % (g**(1/n)-1))
# stale-signal placebo, older lists (past) up to 12 months  (positive shift in 06 = FUTURE list; here negative = PAST list)
keys = sorted(k for k in sig if dates[k] >= pd.Timestamp(START)); rows = []
for m in (-12, -6):
    perm = {k: keys[min(max(j+m, 0), len(keys)-1)] for j, k in enumerate(keys)}
    rows.append((m, met(ev(indep.sim(pxf, b, sig=sig, perm=perm)[0]))))
print("past-list placebo:", rows)
# dividend gap: ^NSEI is a price index. Assume ~1.3%/yr dividend yield (assumption, not measured) -> approx TRI CAGR
bm = met(b.loc[START:]/b.loc[START:].iloc[0]); print("bench price CAGR %.4f ; with assumed +1.3%% div yield ~ %.4f" % (bm["CAGR"], bm["CAGR"]+0.013))
# first-year effect: 2010-2011 signal coverage
print("strategy MaxDD window:", (e/e.cummax()-1).idxmin().date(), "peak", e.loc[:(e/e.cummax()-1).idxmin()].idxmax().date())
