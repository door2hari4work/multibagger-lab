"""Baselines, ablations, random picks, leave-top-k-out, cost stress. Tune window only."""
import pickle, time
from sk_common import *
px,b=load()
eq,log=bt_instr(px,b)
pickle.dump((eq,log),open("out/base.pkl","wb"))
res={}
def rec(name,e): res[name]=(cagr(e),mdd(e)); print(f"{name:38s} CAGR {cagr(e):7.3%} MaxDD {mdd(e):7.2%}",flush=True)
rec("BASE (15,30%,regime,25bps)",eq)
bb=b.loc[START:]/b.loc[START:].iloc[0]; rec("Nifty price idx (^NSEI)",bb)
# equal weight buy&hold of the 272 names alive at start (survivors, rebalanced daily) and all
alive=px.columns[px.loc[START:].iloc[0].notna()]
ew=(1+px[alive].ffill().pct_change().fillna(0).mean(axis=1)).cumprod(); rec("EW daily-rebal, 272 survivors",ew)
# ablations
rec("no regime filter", bt.backtest(px,b,regime=False,start=START)[0])
rec("no stop (99%)", bt.backtest(px,b,stop=0.99,start=START)[0])
rec("no regime, no stop", bt.backtest(px,b,regime=False,stop=0.99,start=START)[0])
rec("stop 20%", bt.backtest(px,b,stop=0.20,start=START)[0])
rec("stop 40%", bt.backtest(px,b,stop=0.40,start=START)[0])
for c in (50,100,200): rec(f"cost {c} bps/side", bt.backtest(px,b,cost_bps=c,start=START)[0])
# random baselines
rf=[];ra=[]
for s in range(8):
    rf.append(bt.backtest(px,b,mode="random",seed=s,start=START)[0])
for s in range(8):
    ra.append(bt.backtest(px,b,mode="random_all",seed=s,start=START)[0])
for nm,L in (("random same filters",rf),("random_all (no filters)",ra)):
    cs=[cagr(e) for e in L]; ds=[mdd(e) for e in L]
    print(f"{nm:38s} CAGR mean {np.mean(cs):.3%} [{min(cs):.3%},{max(cs):.3%}]  MaxDD mean {np.mean(ds):.2%} [{min(ds):.2%},{max(ds):.2%}]",flush=True)
pickle.dump((rf,ra),open("out/rand.pkl","wb"))
# leave-top-k winners out (rank by NAV-units contribution)
con=log["contrib"].loc[START:].sum().sort_values(ascending=False)
print("\nTop 10 contributors (NAV units, 1.0 = start capital):"); print(con.head(10).round(3).to_string())
for k in (3,5,10):
    drop=list(con.index[:k]); e=bt.backtest(px.drop(columns=drop),b,start=START)[0]; rec(f"drop top-{k} winners from universe",e)
# prior-trade survivorship stress: drop random 10%/25% of names (proxy for 'names that would have been in the universe and died') - not same thing, just variance of universe
rs_=[]
rng=np.random.default_rng(1)
for s in range(5):
    keep=rng.choice(px.columns,int(0.75*px.shape[1]),replace=False)
    rs_.append(cagr(bt.backtest(px[keep],b,start=START)[0]))
print("random 75% subuniverse CAGR:",np.round(rs_,3),flush=True)
