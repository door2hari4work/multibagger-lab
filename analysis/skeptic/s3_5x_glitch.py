import pickle
from sk_common import *
px,b=load(); eq,log=pickle.load(open("out/base.pkl","rb"))
pxf=px.ffill(); w=px.loc[START:]
r=pxf.pct_change()
print("=== DATA GLITCH SCAN (single-day moves in tune window) ===")
big=r.loc[START:]
hi=(big>0.5).sum().sum(); lo=(big<-0.4).sum().sum(); print("days with >+50% :",hi," days with < -40%:",lo)
st=big.stack(); ext=st[(st>0.5)|(st<-0.4)].sort_values()
print(ext.head(10).round(2).to_string()); print(ext.tail(10).round(2).to_string())
con=log["contrib"].loc[START:].sum().sort_values(ascending=False)
print("\n=== TOP CONTRIBUTORS: price path check ===")
for t in con.index[:8]:
    s=px[t].loc[START:].dropna(); mx=r[t].loc[START:].max(); mn=r[t].loc[START:].min()
    print(f"{t:14s} first {s.index[0].date()} px {s.iloc[0]:.1f}->{s.iloc[-1]:.1f} max/min over window ratio {s.max()/s.min():.1f}x; max 1d {mx:+.0%} min 1d {mn:+.0%}; NAV contrib {con[t]:.2f}")
tot=con.sum(); pos=con[con>0].sum()
print(f"\nTotal NAV-unit P&L {tot:.2f} (sum of positive {pos:.2f}, negative {con[con<0].sum():.2f}); names ever held: {(log['contrib'].loc[START:]!=0).any().sum()}")
for k in (1,3,5,10,20): print(f"top-{k:2d} names = {con.head(k).sum()/pos:.0%} of gross profit, {con.head(k).sum()/tot:.0%} of net P&L")
# annual
yr=log["contrib"].loc[START:].sum(axis=1).groupby(lambda d:d.year).sum()
print("P&L by year (NAV units, additive):"); print(yr.round(2).to_string())
# --- 5x analysis
print("\n=== MULTI-BAGGER BASE RATES (2010-01 to 2018-12) ===")
P=pxf.loc[START:]; first=P.apply(lambda s:s.first_valid_index())
res=[]
for t in P.columns:
    s=P[t].dropna()
    if len(s)<250: continue
    # max drawup: best later-peak / earlier-trough
    runmin=s.cummin(); du=(s/runmin); pk=du.idxmax(); tr=s.loc[:pk].idxmin()
    res.append(dict(ticker=t,start=s.index[0],end_over_start=s.iloc[-1]/s.iloc[0],drawup=du.max(),trough=tr,peak=pk,run_days=(pk-tr).days))
D=pd.DataFrame(res).set_index("ticker")
alive=px.loc[px.index>=START].iloc[0].notna()
print("names with data at 2010-01-04:",int(alive.sum()),"| total tickers with >=1y data in window:",len(D))
print("buy&hold 5x (2010->2018 end/start>=5) among alive-at-start:", int((D.loc[D.index.intersection(alive[alive].index),'end_over_start']>=5).sum()),
      "| >=3x:",int((D.loc[D.index.intersection(alive[alive].index),'end_over_start']>=3).sum()),"| <1x (lost money):",int((D.loc[D.index.intersection(alive[alive].index),'end_over_start']<1).sum()))
five=D[D.drawup>=5].copy(); print("names with an in-window trough->peak >=5x:",len(five),"(runs <=3y:",int((five.run_days<=1095).sum()),")")
W=log["contrib"]  # NAV units; need weights -> reconstruct held flag from contrib !=0
held=(W!=0)
rows=[]
for t,rw in five.iterrows():
    seg=held[t].loc[rw.trough:rw.peak]; c=W[t].loc[rw.trough:rw.peak].sum()
    rows.append(dict(ticker=t,drawup=rw.drawup,run_days=rw.run_days,pct_days_held=seg.mean(),ever_held=bool(seg.any()),nav_contrib=c))
F=pd.DataFrame(rows).set_index("ticker").sort_values("drawup",ascending=False)
print(F.round(2).head(25).to_string())
print(f"of {len(F)} names with >=5x run: ever held during run {F.ever_held.sum()} ({F.ever_held.mean():.0%}); held >=50% of run days {(F.pct_days_held>=.5).sum()}; mean pct days held {F.pct_days_held.mean():.0%}")
print(f"sum NAV contribution from these during their runs: {F.nav_contrib.sum():.2f} of net {tot:.2f}")
# false positives: names the rule selected that went on to lose >=30% (stop or not)
rb=pd.DataFrame(log["rebal_exits"]); S=pd.DataFrame(log["stops"]); X=pd.concat([rb.assign(k="rebal"),S[["ticker","entry_date","exit_date","entry","exit"]].assign(k="stop")])
X["pnl"]=X.exit/X.entry-1
print(f"\ntrades: {len(X)}, hit rate {(X.pnl>0).mean():.0%}, mean {X.pnl.mean():.1%}, median {X.pnl.median():.1%}, >=+100% {(X.pnl>=1).mean():.1%}, >=+300% {(X.pnl>=4).mean():.1%} (5x) , <=-30% {(X.pnl<=-.3).mean():.1%}, worst {X.pnl.min():.0%}")
print("holding days: median",(X.exit_date-X.entry_date).dt.days.median(),"| share held <365d:",f"{((X.exit_date-X.entry_date).dt.days<365).mean():.0%}")
print("trades >=5x count:",int((X.pnl>=4).sum()))
print("\n=== GLITCH DAYS: was the strategy holding the name? (NAV-unit contribution on that day) ===")
for d,t in [("2010-06-24","KIRLOSENG.NS"),("2015-11-19","JSL.NS"),("2017-02-27","J&KBANK.NS"),("2017-07-03","CDSL.NS"),("2010-01-08","WHIRLPOOL.NS")]:
    print(d,t,"contrib",round(float(log['contrib'].loc[d,t]),4), "ret",round(float(r.loc[d,t]),2))
# top-contributor largest day moves
for t in con.index[:3]:
    c=log['contrib'][t]; print(t,"best single day NAV contrib",round(c.max(),3),c.idxmax().date(),"| share of its total",round(c.max()/con[t],2))

