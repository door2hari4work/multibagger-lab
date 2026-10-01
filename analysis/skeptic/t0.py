import time
from sk_common import *
px,b=load()
t=time.time(); eq0,tr0=bt.backtest(px,b,start=START); print("orig",time.time()-t)
t=time.time(); eq1,log=bt_instr(px,b); print("instr",time.time()-t)
print("max abs diff", (eq0-eq1).abs().max())
print(cagr(eq0), mdd(eq0), cagr(b), mdd(b))
