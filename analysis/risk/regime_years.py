"""Year-by-year effect of regime filter (stop 30%, top15) and of the stop (regime on)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pandas as pd, risk_lib as R, data_loader as dl
px, b = dl.load_tune(); P = R.prep(px, b)
runs = {"regime on": R.run(P), "regime off": R.run(P, regime=False), "no stop, regime on": R.run(P, stop=None), "no stop, regime off": R.run(P, stop=None, regime=False)}
out = {}
for k, r in runs.items():
    e = R.rs_curve(r["eq"]); s = R.risk_stats(e); out[k] = s["year_rets"].values
yrs = R.risk_stats(R.rs_curve(runs["regime on"]["eq"]))["year_rets"].index.year
df = pd.DataFrame(out, index=yrs); print((df*100).round(1).to_string())
g = runs["regime on"]["gross"].loc["2010-01-01":]
cash = (g < 1e-9)
# contiguous cash stretches > 20 days
grp = (cash != cash.shift()).cumsum(); 
st = [(x.index[0].date(), x.index[-1].date(), len(x)) for _, x in cash[cash].groupby(grp[cash]) if len(x) > 20]
print("cash stretches >20d:", st)
bn = dl.window(b, "2010-01-01")
for a, c, n in st:
    print(a, c, "Nifty move over stretch %.1f%%" % ((bn.loc[:str(c)].iloc[-1]/bn.loc[:str(a)].iloc[-1]-1)*100),
          "| regime-off strategy move %.1f%%" % ((R.rs_curve(runs["regime off"]["eq"]).loc[:str(c)].iloc[-1]/R.rs_curve(runs["regime off"]["eq"]).loc[:str(a)].iloc[-1]-1)*100))
