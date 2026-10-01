from common import *
import indep
px, b = load(); pxf = indep.prep(px); dates = pxf.index
def ev(eq, cap=None):
    e = eq.loc[START:]; return e/e.iloc[0]
sig = indep.signals(pxf, b)
print("== cost stress (bps per side), indep engine ==")
for c in (25, 50, 75, 100, 150, 200):
    eq, tr = indep.sim(pxf, b, sig=sig, cost_bps=c); m = met(ev(eq)); print(c, {k: round(v, 4) for k, v in m.items()})
print("== circuit-lock proxies (close-to-close move >= threshold treated as locked: buys skipped, sells retried next bar) ==")
for th in (0.048, 0.095, 0.19):
    eq, tr = indep.sim(pxf, b, sig=sig, circ=th); m = met(ev(eq)); print(th, {k: round(float(v), 4) for k, v in m.items()}, indep.sim.stats)
print("== whole shares, Rs 10,00,000 start ==")
eqf, trf = indep.sim(pxf, b, sig=sig, capital=1_000_000.0)
eqw, trw = indep.sim(pxf, b, sig=sig, capital=1_000_000.0, whole_shares=True)
print("fractional", met(ev(eqf)), "NAV end Rs {:,.0f}".format(eqf.iloc[-1]))
print("whole-share", met(ev(eqw)), "NAV end Rs {:,.0f}".format(eqw.iloc[-1]))
td = indep.trades_df(trf, dates); td = td[td.edate >= pd.Timestamp(START)].copy()
# position size at entry = entry value; compare with 1 share price
td["one_share_pct_of_pos"] = td.epx / td["eval"]
print("entries where ONE share > 10%% of the position: %.1f%%; > 50%%: %.1f%% (adjusted prices)" % (100*(td.one_share_pct_of_pos > .1).mean(), 100*(td.one_share_pct_of_pos > .5).mean()))
print("entry value Rs: min %.0f median %.0f max %.0f" % (td["eval"].min(), td["eval"].median(), td["eval"].max()))
print("first-year (2010) position size Rs %.0f; adjusted price max over window of names held: %.0f" % (1e6/15, td.epx.max()))
print("max adj close in tune file (any name):", float(px.max().max()))
# zero-return-day illiquidity proxy (Lesmond): share of zero-return days over the 60 bars before entry
zr = (pxf.diff() == 0).astype(float)
td["zero60"] = [zr[n].iloc[max(i-60, 0):i].mean() for n, i in zip(td.name, td.ei)]
print("trades w/ >=10%% zero-return days in prior 60 bars: %.1f%% of trades; %.1f%% of sum pnl; median zero60 %.3f" % (
    100*(td.zero60 >= .1).mean(), 100*td[td.zero60 >= .1].pnl_frac.sum()/td.pnl_frac.sum(), td.zero60.median()))
# low-priced names (adjusted price < Rs 20): tick-size / impact proxy
print("trades with adjusted entry price < Rs 20: %.1f%% of trades, %.1f%% of pnl" % (100*(td.epx < 20).mean(), 100*td[td.epx < 20].pnl_frac.sum()/td.pnl_frac.sum()))
# exclude zero-return>=10% names entirely (crude ADV floor) and re-run
bad = set(td[td.zero60 >= .1].name)
e2, _ = indep.sim(indep.prep(px.drop(columns=list(bad))), b); print("re-run excluding %d names flagged illiquid by zero-return proxy:" % len(bad), met(ev(e2)))
# stop-exit gap cost: how far below the 30% trailing level do stop exits actually fill?
st = td[td.why == "stop"].copy()
st["gap"] = st.ret
print("stop exits: n=%d, median ret %.3f, worst %.3f; share of stop exits worse than -35%%: %.1f%%" % (len(st), st.ret.median(), st.ret.min(), 100*(st.ret < -.35).mean()))
