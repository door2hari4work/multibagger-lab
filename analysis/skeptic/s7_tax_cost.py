import pickle
from sk_common import *
px,b=load(); eq,log=pickle.load(open("out/base.pkl","rb"))
cap=config.START_CAPITAL_INR
E=eq.loc[START:]; E=E/E.iloc[0]; yrs=(E.index[-1]-E.index[0]).days/365.25
def fin(c): return cap*(1+c)**yrs
print("Rs final from 10L: base",rs(fin(cagr(eq))),"| no regime (30.48%)",rs(fin(0.30477)),"-> regime filter cost in tune",rs(fin(0.30477)-fin(cagr(eq))),"| no stop (25.59%)",rs(fin(0.25589)),"| no regime/no stop (32.54%)",rs(fin(0.32542)))
def tax_run(eq,log,stcg,ltcg,exm,label):
    E=eq.loc[START:]; E=E/E.iloc[0]
    real=pd.DataFrame(log["realized"],columns=["date","ticker","gain","age"]); real=real[real.date>=START]
    real["fy"]=real.date.map(lambda d:d.year if d.month<=3 else d.year+1); real["short"]=real.age<365
    fac=1.0; paid=0; cs=cl=0.0
    for fy in sorted(real.fy.unique()):
        g=real[real.fy==fy]; fe=min(pd.Timestamp(year=fy,month=3,day=31),E.index[-1]); nav=cap*E.loc[:fe].iloc[-1]*fac
        sc=cap*fac; st=g[g.short].gain.sum()*sc-cs; lt=g[~g.short].gain.sum()*sc-cl
        if st<0<lt: lt+=st; st=0
        elif lt<0<st: st+=lt; lt=0
        cs=max(-st,0); cl=max(-lt,0)
        tax=(max(st,0)*stcg+max(lt-exm,0)*ltcg)*1.04; paid+=tax; fac*=1-tax/nav
    f=cap*E.iloc[-1]*fac; c=(f/cap)**(1/yrs)-1
    print(f"{label}: pre-tax {cagr(eq):.2%} {rs(cap*E.iloc[-1])} -> after-tax {c:.2%} {rs(f)}; tax paid {rs(paid)}; drag {(cagr(eq)-c)*100:.1f}pp")
    return c
tax_run(eq,log,0.20,0.125,125000,"25bps, STCG20/LTCG12.5")
tax_run(eq,log,0.30,0.125,125000,"25bps, taxed as business income at ~30% slab (STCG->30%)")
eq100,log100=bt_instr(px,b,cost_bps=100)
tax_run(eq100,log100,0.20,0.125,125000,"100bps/side, STCG20/LTCG12.5")
eq50,log50=bt_instr(px,b,cost_bps=50)
tax_run(eq50,log50,0.20,0.125,125000,"50bps/side, STCG20/LTCG12.5")
# cash yield credit
cashdays=1-(log["contrib"].loc[START:]!=0).any(axis=1).mean()
print("share of days fully in cash:", f"{(~(log['contrib'].loc[START:]!=0).any(axis=1)).mean():.1%}")
# Rs table at account sizes
print("\nAccount size -> Rs loss at drawdown levels")
for A in (10e5,25e5,50e5,1e7):
    print(f"{rs(A):>16s}: -34% {rs(.344*A)} | -50% {rs(.5*A)} | -60% {rs(.6*A)} | 2018-style -22.9% yr {rs(.229*A)} | worst month -15.8% {rs(.158*A)}")
# whipsaw: stop+cash cost in Rs? stopped names that recovered: sum of foregone
S,R=pickle.load(open("out/stops.pkl","rb"))
print("stops n",len(S)," ; per stop avg weight ~ 1/15")
# capacity arithmetic
for A in (10e5,1e7,5e7,1e8):
    pos=A/15; print(f"AUM {rs(A)}: position {rs(pos)}; ADV needed at 10% participation {rs(pos/0.10)}/day; exit-in-1-day at 20% part {rs(pos/0.2)}; annual traded value {rs(7.1*A)}")
