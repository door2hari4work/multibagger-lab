import pickle
from sk_common import *
px,b=load(); eq,log=pickle.load(open("out/base.pkl","rb"))
pxf=px.ffill()
E=eq.loc[START:]; E=E/E.iloc[0]; B=b.loc[START:]/b.loc[START:].iloc[0]
ma=pxf.rolling(200,min_periods=200).mean()
above=(pxf>ma); valid=ma.notna()
brd=above.sum(axis=1)/valid.sum(axis=1)
print("breadth (% of valid names above own 200DMA) -- ffilled prices; sample:",brd.loc["2010-11-10"].round(2),brd.loc["2013-01-29"].round(2),brd.loc["2018-01-15"].round(2),brd.loc["2018-10-09"].round(2),brd.loc["2016-10-25"].round(2),brd.loc["2016-12-26"].round(2))
pickle.dump(brd,open("out/breadth.pkl","wb"))
mon=pd.DataFrame(log["months"]).set_index("date")
U=(1+pxf.pct_change().fillna(0).loc[START:].mean(axis=1)).cumprod()
# EW variants
alive=px.columns[px.loc[px.index>=START].iloc[0].notna()]
r=pxf[alive].pct_change().loc[START:].fillna(0)
bh=(1+r).cumprod().mean(axis=1)      # buy&hold equal initial weights
dly=(1+r.mean(axis=1)).cumprod()
mlt=[];v=1.0
w=pd.Series(1/len(alive),index=alive); 
last=None
for d,row in r.iterrows():
    v*=1+float((w*row).sum()); w=w*(1+row); w=w/w.sum()
    if last is None or d.month!=last: w=pd.Series(1/len(alive),index=alive)
    last=d.month; mlt.append(v)
mlt=pd.Series(mlt,index=r.index)
print("\nEW 272 survivors: buy&hold CAGR %.2f%% MaxDD %.1f%% | monthly-rebal %.2f%% / %.1f%% | daily-rebal %.2f%% / %.1f%%"%(cagr(bh)*100,mdd(bh)*100,cagr(mlt)*100,mdd(mlt)*100,cagr(dly)*100,mdd(dly)*100))
print("bt.buy_hold(all 499, ffill, fillna0 mean):", "%.2f%% / %.1f%%"%(cagr(bt.buy_hold(px))*100, mdd(bt.buy_hold(px))*100))
yrs=(E.index[-1]-E.index[0]).days/365.25; cap=config.START_CAPITAL_INR
g=cap*(bh.iloc[-1]/bh.iloc[0]-1); tax=max(g-125000,0)*0.125*1.04
print(f"EW survivors buy&hold, one LTCG exit at end: pre-tax {cagr(bh):.2%} -> after-tax {((cap*bh.iloc[-1]/bh.iloc[0]-tax)/cap)**(1/yrs)-1:.2%}")
# who made the money: alive at start vs later listed
con=log["contrib"].loc[START:].sum()
late=[c for c in px.columns if c not in alive]
print(f"\nNAV-unit P&L: names alive 2010-01-04 {con[alive].sum():.2f} ({con[alive].sum()/con.sum():.0%}); names first priced after 2010-01-04 {con[late].sum():.2f} ({con[late].sum()/con.sum():.0%}); the latter = {len(late)} later-listed/ later-priced tickers (IPOs, demergers, or data starts) -> in 2010 they were NOT index members")
top=con.sort_values(ascending=False).head(10)
fv=pxf.apply(lambda s:s.first_valid_index())
print("top-10 contributors: first price date / 2010 adj price :")
for t,v in top.items():
    s=px[t].dropna(); print(f"  {t:14s} {v:5.2f}  first {s.index[0].date()}  px at first {s.iloc[0]:.1f}  px 2018-12 {s.iloc[-1]:.1f}")
# rerun breadth tables
Em=E.resample("ME").last().pct_change().shift(-1); Bm=B.resample("ME").last().pct_change().shift(-1); Um=(U.loc[START:]/U.loc[START:].iloc[0]).resample("ME").last().pct_change().shift(-1)
df=pd.DataFrame({"breadth":brd.reindex(Em.index,method="ffill"),"strat":Em,"nifty":Bm,"ew":Um}).dropna()
df["terc"]=pd.qcut(df.breadth,3,labels=["low","mid","high"])
print("\nBREADTH TERCILE (month-end breadth -> NEXT month): ranges",df.groupby("terc",observed=True).breadth.agg(["min","max"]).round(2).to_dict("index"))
print(df.groupby("terc",observed=True)[["strat","nifty","ew"]].mean().round(4).to_string())
print("share of months strat<0:", df.groupby("terc",observed=True).apply(lambda g:(g.strat<0).mean()).round(2).to_dict())
# divergence: nifty>200dma and breadth<40%
bx=(b>b.rolling(200).mean()).reindex(brd.index).ffill()
for th in (0.35,0.45):
    dv=((bx)&(brd<th)).reindex(df.index,method="ffill").fillna(False)
    print(f"Nifty>200DMA but breadth<{th:.0%}: months {int(dv.sum())}; strat next-mo mean {df.strat[dv].mean():.2%} (<0 in {(df.strat[dv]<0).mean():.0%}), nifty {df.nifty[dv].mean():.2%}, ew {df.ew[dv].mean():.2%}")
print("\n2017-12..2018-12 month-end breadth / strat / nifty / ew")
idx=E.resample("ME").last().index
x=pd.DataFrame({"breadth":brd.reindex(idx,method="ffill"),"regime_on":mon.regime_on.reindex(idx,method="ffill"),"strat":E.resample("ME").last().pct_change(),"nifty":B.resample("ME").last().pct_change(),"ew":(U.loc[START:]/U.loc[START:].iloc[0]).resample("ME").last().pct_change()}).loc["2017-12":"2018-12"]
print(x.round(3).to_string())
# breadth at drawdown peaks/troughs
for pk,t in [("2018-01-15","2018-10-09"),("2016-10-25","2016-12-26"),("2010-11-10","2011-04-01"),("2013-01-29","2013-04-12")]:
    print(f"DD {pk}->{t}: breadth {brd.loc[pk]:.0%} -> {brd.loc[t]:.0%}")
# peak-breadth euphoria: months where breadth>80%: subsequent 3m strat return
hi=brd.reindex(E.index,method="ffill")
f3=E.pct_change(63).shift(-63)
for lo,hi_ in [(0,.3),(.3,.6),(.6,.8),(.8,1.01)]:
    m=(brd.reindex(E.index)>=lo)&(brd.reindex(E.index)<hi_)
    print(f"breadth {lo:.0%}-{min(hi_,1):.0%}: days {int(m.sum())}, next-63d strat mean {f3[m].mean():.1%}, worst {f3[m].min():.1%}, %neg {(f3[m]<0).mean():.0%}")
