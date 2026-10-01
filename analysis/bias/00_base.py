from common import *
px, b = load()
t=time.time()
e, tr = run(px, b)
print(met(e, tr), time.time()-t)
print("bench", met(b.loc[START:]/b.loc[START:].iloc[0]))
print("EW buyhold", met(bt.buy_hold(px.loc[START:])))
print("n trades", len(tr))
print(e.resample("YE").last().pct_change())
