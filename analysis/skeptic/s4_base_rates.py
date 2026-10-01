import pickle
from sk_common import *
px,b=load(); eq,log=pickle.load(open("out/base.pkl","rb"))
pxf=px.ffill(); r=pxf.pct_change()
print("=== KIRLOSENG around 2010-06-24 ==="); print(px["KIRLOSENG.NS"].loc["2010-06-18":"2010-06-30"].round(2).to_string())
print("\n=== all days >+25% or <-25% in tune window, with strategy NAV-unit contribution that day ===")
big=r.loc[START:].stack(); big=big[(big>0.25)|(big<-0.25)]
C=log["contrib"]
rows=[(d,t,v,float(C.loc[d,t])) for (d,t),v in big.items()]
X=pd.DataFrame(rows,columns=["date","ticker","ret","contrib"]); print("n:",len(X),"| held on the day:",int((X.contrib!=0).sum()))
print(X[X.contrib!=0].round(3).to_string())
print("\n=== Forward 3y 5x base rate by month-end entry (names with data) ===")
me=pxf.groupby([pxf.index.year,pxf.index.month]).tail(1).index; me=me[(me>=START)&(me<=pd.Timestamp("2015-12-31"))]
mon=pd.DataFrame(log["months"]).set_index("date")
tot=0;hit=0;sel=0;selhit=0;hit2=0;sel2=0;tot2=0
for d in me:
    i=pxf.index.get_loc(d); fut=pxf.iloc[i+1:i+1+756]
    e=pxf.iloc[i+1] # execute next day
    ok=e.notna()&(px.iloc[i].notna())
    mx=(fut.max()/e)[ok]
    tot+=len(mx); hit+=(mx>=5).sum(); tot2+=len(mx); hit2+=(mx>=2).sum()
    if d in mon.index and mon.loc[d,"regime_on"]:
        c=[x for x in mon.loc[d,"cands"] if x in mx.index]; sel+=len(c); selhit+=(mx[c]>=5).sum(); sel2+=len(c); selhit2=0
        selhit2 = (mx[c]>=2).sum() if True else 0
        globals().setdefault("S2",0); globals()["S2"]+=selhit2
print(f"unconditional: P(max within 3y >=5x) = {hit/tot:.1%}  (n={tot}); >=2x {hit2/tot2:.1%}")
print(f"rule-selected (top-15, regime on): P(5x in 3y) = {selhit/sel:.1%} (n={sel}); P(2x in 3y) = {S2/sel2:.1%}")
print("-> rule's precision for 5x over ex-ante; compare with unconditional (hindsight on survivors).")
# false-positive cost: selected names that fell >=30% from entry within 12m
fp=0;n=0
for d in me:
    if d in mon.index and mon.loc[d,"regime_on"]:
        i=pxf.index.get_loc(d); 
        for t in mon.loc[d,"cands"]:
            e=pxf[t].iloc[i+1]; f=pxf[t].iloc[i+1:i+253]
            n+=1; fp+= (f.min()/e-1<=-0.30)
print(f"selected names drawing down >=30% below entry within 12m (ignoring stop): {fp/n:.1%} (n={n})")
