import pickle
from sk_common import *
px,b=load(); eq,log=pickle.load(open("out/base.pkl","rb"))
E=eq.loc[START:]; E=E/E.iloc[0]; B=b.loc[START:]/b.loc[START:].iloc[0]
pxf=px.ffill()
mon=pd.DataFrame(log["months"]).set_index("date")
brd=((px>px.rolling(200).mean()).sum(axis=1)/px.notna().sum(axis=1))
mid=(pxf.pct_change(126).rank(axis=1,pct=True))
# universe equal-weight index as small/mid proxy
U=(1+pxf.pct_change().fillna(0).mean(axis=1)).cumprod().loc[START:]; U=U/U.iloc[0]
print("=== BREADTH / NARROWNESS: strategy next-month return by breadth tercile at month-end ===")
Em=E.resample("ME").last().pct_change().shift(-1); Bm=B.resample("ME").last().pct_change().shift(-1); Um=U.resample("ME").last().pct_change().shift(-1)
df=pd.DataFrame({"breadth":brd.reindex(Em.index,method="ffill"),"strat":Em,"nifty":Bm,"ew":Um}).dropna()
df["terc"]=pd.qcut(df.breadth,3,labels=["low","mid","high"])
print(df.groupby("terc",observed=True)[["strat","nifty","ew"]].agg(["mean"]).round(4).to_string()); print("n per bucket",df.terc.value_counts().to_dict())
print("share of months strat<0:", df.groupby("terc",observed=True).apply(lambda g:(g.strat<0).mean()).round(2).to_dict())
# breadth drop (narrowing): change in breadth over 3m
df["dB"]=brd.diff(63).reindex(df.index,method="ffill")
d2=df.dropna(); d2["bchg"]=pd.qcut(d2.dB,3,labels=["falling","flat","rising"])
print("by 3m change in breadth:"); print(d2.groupby("bchg",observed=True)[["strat","nifty","ew"]].mean().round(4).to_string())
# divergence: Nifty above 200DMA but breadth < 30% (narrow market where regime filter is blind)
bx=(b>b.rolling(200).mean()).reindex(brd.index).ffill()
div=((bx)&(brd<0.30)).reindex(Em.index,method="ffill")
print("\n'Nifty>200DMA but <30% of names above own 200DMA' (filter ON, market narrow): months",int(div.reindex(df.index).sum()),
      "| strat next-month mean", round(df.strat[div.reindex(df.index).fillna(False)].mean(),4),"| ew mean",round(df.ew[div.reindex(df.index).fillna(False)].mean(),4))
print("2018 detail (month-end breadth, regime state, strategy month return):")
x=pd.DataFrame({"breadth":brd.reindex(E.resample('ME').last().index,method='ffill'),"regime_on":mon.regime_on.reindex(E.resample('ME').last().index,method='ffill'),"strat_m":E.resample('ME').last().pct_change(),"nifty_m":B.resample('ME').last().pct_change(),"ew_m":U.resample('ME').last().pct_change()}).loc["2017-12":"2018-12"]
print(x.round(3).to_string())
# momentum crash / rebound: months after Nifty 6m drawdown <-10% then rebound
print("\n=== MOMENTUM-CRASH CHECK: worst 8 strategy months vs Nifty/EW same month ===")
sm=E.resample("ME").last().pct_change().dropna(); w8=sm.nsmallest(8)
for d,v in w8.items(): print(d.strftime("%Y-%m"),f"strat {v:+.1%}  nifty {B.resample('ME').last().pct_change()[d]:+.1%}  ew-universe {U.resample('ME').last().pct_change()[d]:+.1%}  regime_on(prev ME) {mon.regime_on.shift(1).reindex([d],method='nearest').iloc[0]}")
# rebound months: Nifty up >5% in month following a month where it was <200DMA
print("worst 12m strategy window: ", E.pct_change(252).idxmin().date(), f"{E.pct_change(252).min():.1%}")
# strategy beta / downside capture
sr=sm; br=B.resample("ME").last().pct_change().reindex(sm.index)
print(f"monthly beta to Nifty {np.cov(sr,br)[0,1]/br.var():.2f}; downside capture (Nifty<0 months) {sr[br<0].mean()/br[br<0].mean():.2f}; strat avg in Nifty<-3% months {sr[br<-0.03].mean():.2%} (n={(br<-0.03).sum()}) vs nifty {br[br<-0.03].mean():.2%}")

print("\n=== TAX (illustrative; assumed live-era rules) ===")
real=pd.DataFrame(log["realized"],columns=["date","ticker","gain_nav","age_days"])
real=real[real.date>=START]
real["fy"]=real.date.map(lambda d:d.year if d.month<=3 else d.year+1)
real["short"]=real.age_days<365
print(f"realised events {len(real)}; share of realised gain that is short-term: {real[real.short].gain_nav.clip(lower=0).sum()/real.gain_nav.clip(lower=0).sum():.1%} (by gross gains)")
def simulate(stcg,ltcg,exempt_rs,label,cost_extra_bps=0):
    cap=config.START_CAPITAL_INR
    # equity path in Rs; taxes paid at FY-end out of portfolio; scale factor applied to subsequent realised gains
    fac=1.0; paid=0.0; carry_st=0.0; carry_lt=0.0; rows=[]
    Eq=E.copy()
    fys=sorted(real.fy.unique())
    tax_hist=[]
    for fy in fys:
        g=real[real.fy==fy]
        fy_end=pd.Timestamp(year=fy,month=3,day=31)
        if fy_end>Eq.index[-1]: fy_end=Eq.index[-1]
        nav_end=cap*Eq.loc[:fy_end].iloc[-1]*fac
        scale=cap*fac   # eq units -> Rs (approx, using factor at FY start)
        st=g[g.short].gain_nav.sum()*scale-carry_st; lt=g[~g.short].gain_nav.sum()*scale-carry_lt
        # set off: ST loss against LT gain and vice versa
        if st<0 and lt>0: lt+=st; st=0
        elif lt<0 and st>0: st+=lt; lt=0
        carry_st=max(-st,0); carry_lt=max(-lt,0)
        taxable_lt=max(lt-exempt_rs,0); tax=max(st,0)*stcg+taxable_lt*ltcg
        tax*=1.04  # cess
        paid+=tax; fac*=1-tax/nav_end if nav_end>0 else 1
        tax_hist.append((fy,round(st),round(lt),round(tax)))
    final=cap*Eq.iloc[-1]*fac; yrs=(E.index[-1]-E.index[0]).days/365.25
    print(f"{label}: pre-tax final {rs(cap*Eq.iloc[-1])} CAGR {cagr(eq):.2%} | after-tax final {rs(final)} CAGR {(final/cap)**(1/yrs)-1:.2%} | total tax paid {rs(paid)} | tax drag {(cagr(eq)-((final/cap)**(1/yrs)-1))*100:.1f} pp/yr")
    return tax_hist
th=simulate(0.20,0.125,125000,"STCG 20% / LTCG 12.5% above Rs 1.25L (post-Jul-2024 rule, ASSUMED for all years)")
for row in th: print("   FY",row)
simulate(0.15,0.10,100000,"STCG 15% / LTCG 10% above Rs 1L (2019-Jul2024 rule)")
# buy-and-hold tax comparison: Nifty LTCG on terminal (single sale at end)
cap=config.START_CAPITAL_INR; gain=cap*(B.iloc[-1]-1); tax=max(gain-125000,0)*0.125*1.04
yrs=(E.index[-1]-E.index[0]).days/365.25; print(f"Nifty buy&hold single exit: pre {(B.iloc[-1])**(1/yrs)-1:.2%} after-tax CAGR {((cap*B.iloc[-1]-tax)/cap)**(1/yrs)-1:.2%}")
# impact of costs beyond model: STT etc.
T=pd.DataFrame(log["turnover"],columns=["d","t"]).set_index("d").t.loc[START:]
print(f"turnover {T.sum()/yrs:.1f}x NAV/yr; on average NAV Rs 30L (illustrative) this is Rs {T.sum()/yrs*30e5/1e5:.0f}L traded per year; STT 0.1%*each side etc")
