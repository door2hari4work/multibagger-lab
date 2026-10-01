from common import *
import indep
px, b = load()
pxf = indep.prep(px)
t=time.time(); e1, tr1 = run(px, b); print("bt", met(e1, tr1), round(time.time()-t,1))
t=time.time(); eq, tr = indep.sim(pxf, b); print("sim", round(time.time()-t,1))
e2 = eq.loc[START:]; e2 = e2/e2.iloc[0]
print("indep", met(e2))
d = (e2/e1 - 1).abs(); print("max rel equity diff", d.max(), "mean", d.mean())
print("trades bt", len(tr1), "indep", len(tr))
