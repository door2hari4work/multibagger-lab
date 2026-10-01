"""Diagnostics on the base run (tune window only)."""
import pickle
from sk_common import *
px,b=load()
eq,log=pickle.load(open("out/base.pkl","rb"))
E=eq.loc[START:]; E=E/E.iloc[0]; B=b.loc[START:]/b.loc[START:].iloc[0]
cap=config.START_CAPITAL_INR
print("=== HEADLINE ===")
print(f"strategy CAGR {cagr(eq):.2%} MaxDD {mdd(eq):.2%} final {rs(cap*E.iloc[-1])}; Nifty price CAGR {cagr(b):.2%} MaxDD {mdd(b):.2%}")
print("Rs max drawdown on Rs 10L:", rs(((E.cummax()-E)*cap).max()))

# ---- drawdown episodes
def episodes(s, n=4):
    dd=s/s.cummax()-1; out=[]; dd2=dd.copy()
    for _ in range(n):
        t=dd2.idxmin(); 
        if dd2[t]>-0.05: break
        pk=s.loc[:t].idxmax(); rec=s.loc[t:][s.loc[t:]>=s.loc[pk]]; rd=rec.index[0] if len(rec) else None
        out.append((pk,t,rd,dd2[t])); 
        hi=rd if rd is not None else s.index[-1]
        dd2.loc[pk:hi]=0
    return out
print("\n=== WORST STRATEGY DRAWDOWN EPISODES ===")
mon=pd.DataFrame(log["months"]).set_index("date")
bx=(b>b.rolling(200).mean())
brd=(px>px.rolling(200).mean()).sum(axis=1)/px.notna().sum(axis=1)
for pk,t,rd,d in episodes(E):
    bret=B.loc[t]/B.loc[pk]-1
    bdd=(B.loc[pk:t]/B.loc[pk:t].cummax()-1).min()
    con=log["contrib"].loc[pk:t].sum().sort_values()
    held=mon.loc[:pk].iloc[-1]["cands"] if len(mon.loc[:pk]) else []
    rec_s=rd.date() if rd is not None else "NOT RECOVERED"
    on=bx.loc[pk:t].mean()
    print(f"peak {pk.date()} trough {t.date()} recover {rec_s} | strat {d:.1%} (Rs {rs((E.loc[pk]-E.loc[t])*cap)}) | Nifty {bret:+.1%} (maxdd in window {bdd:.1%}) | {(t-pk).days}d down | Nifty>200DMA {on:.0%} of days | breadth(%>200d) at peak {brd.loc[pk]:.0%} trough {brd.loc[t]:.0%}")
    print("   worst contributors (NAV units):", ", ".join(f"{k.replace('.NS','')} {v:+.3f}" for k,v in con.head(5).items()))
    print("   regime state at month-ends in window:", mon.loc[pk:t,"regime_on"].mean().round(2), " n_eligible avg", mon.loc[pk:t,"n_elig"].mean().round(1))
# underwater duration
dd=E/E.cummax()-1
under=(dd<-1e-9); grp=(~under).cumsum(); lens=under.groupby(grp).sum()
print("longest underwater stretch (days):", lens.max(), " | % of days >10% below peak:", f"{(dd<-0.10).mean():.0%}", "| >20% below:", f"{(dd<-0.20).mean():.0%}")
# rolling 12m
r12=E.pct_change(252).dropna(); b12=B.pct_change(252).dropna().reindex(r12.index)
print(f"rolling 12m: strat <0 {(r12<0).mean():.0%} | strat<Nifty {(r12<b12).mean():.0%} | worst 12m {r12.min():.1%} | 5th pct {r12.quantile(.05):.1%}")
cal=E.resample("YE").last().pct_change(); cal.iloc[0]=E.resample("YE").last().iloc[0]-1
bc=B.resample("YE").last().pct_change(); bc.iloc[0]=B.resample("YE").last().iloc[0]-1
print("calendar-year strat vs Nifty:"); print(pd.DataFrame({"strat":cal,"nifty":bc}).assign(diff=lambda d:d.strat-d.nifty).round(3).to_string())

# ---- regime filter whipsaw
print("\n=== REGIME FILTER ===")
on=mon["regime_on"]; flips=(on!=on.shift()).sum()-1
print(f"month-ends: {len(mon)}; filter ON {on.mean():.0%}; state flips {flips}; months in cash(<15 sel) {(mon.n_sel==0).sum()}; avg names selected {mon.n_sel.mean():.1f}/15; months with <15 eligible {(mon.n_sel<15).sum()}")
nxt=B.resample("ME").last().pct_change().shift(-1)
ms=mon.copy(); ms.index=ms.index.to_period("M"); nx=nxt.copy(); nx.index=nx.index.to_period("M"); ms["bench_next"]=nx.reindex(ms.index)
ms=ms.loc["2010-01":]
print("Nifty next-month return when filter ON  : mean %.2f%%, %%pos %.0f%%"%(ms[ms.regime_on].bench_next.mean()*100,(ms[ms.regime_on].bench_next>0).mean()*100))
print("Nifty next-month return when filter OFF : mean %.2f%%, %%pos %.0f%%  (n=%d)"%(ms[~ms.regime_on].bench_next.mean()*100,(ms[~ms.regime_on].bench_next>0).mean()*100,(~ms.regime_on).sum()))
offs=ms[~ms.regime_on]; print("OFF months where Nifty rose >3% next month (missed):", (offs.bench_next>0.03).sum(), "of", len(offs), "; avg missed gain", offs[offs.bench_next>0.03].bench_next.mean())
# strategy returns by regime state
Em=E.resample("ME").last().pct_change(); Em.index=Em.index.to_period("M")
st=ms.regime_on.shift(1)  # state set at prev month-end governs this month's holdings (executed next day)
dfm=pd.DataFrame({"strat":Em,"bench":B.resample("ME").last().pct_change().set_axis(Em.index),"state_prev":st}).dropna()
for s,g in dfm.groupby("state_prev"): print(f"prev month-end state ON={s}: n={len(g)} strat mean {g.strat.mean():.2%} bench mean {g.bench.mean():.2%}")

# ---- stops
print("\n=== STOPS ===")
S=pd.DataFrame(log["stops"]); print("stop exits:",len(S),"| rebalance exits:",len(log["rebal_exits"]),"| per year ~", round(len(S)/9,1))
S["gap_vs_trigger"]=S.exit/(S.peak*0.70)-1; S["exit_vs_peak"]=S.exit/S.peak-1; S["pnl"]=S.exit/S.entry-1
print(f"stop exits: avg exit vs peak {S.exit_vs_peak.mean():.1%} (nominal -30%), worst {S.exit_vs_peak.min():.1%}; avg gap below trigger {S.gap_vs_trigger.mean():.1%}; avg trade pnl {S.pnl.mean():.1%}, %winners {(S.pnl>0).mean():.0%}")
pxf=px.ffill()
res=[]
for _,r in S.iterrows():
    s=pxf[r.ticker]; idx=s.index.get_loc(r.exit_date)
    row={}
    for h in (63,126,252):
        if idx+h<len(s): row[h]=s.iloc[idx+h]/r.exit-1
    # regained peak within 252d
    fut=s.iloc[idx:idx+252]; row["regain_peak"]=bool((fut>=r.peak).any()) if len(fut)>=126 else np.nan
    row["rebought_3m"]=any(r.ticker in m["cands"] for m in log["months"] if r.exit_date<m["date"]<=r.exit_date+pd.Timedelta(days=95))
    res.append(row)
R=pd.DataFrame(res)
for h in (63,126,252):
    c=R[h].dropna(); print(f"after stop, +{h}d: price above exit price {(c>0).mean():.0%} (n={len(c)}), mean {c.mean():+.1%}, median {c.median():+.1%}")
print(f"regained prior peak within 252d: {R.regain_peak.dropna().mean():.0%}; re-selected by rule within ~3m: {R.rebought_3m.mean():.0%}")
# equal-weight stop-sell/rebuy cost
T=pd.DataFrame(log["turnover"],columns=["d","t"]).set_index("d").t; C=pd.DataFrame(log["cost"],columns=["d","c"]).set_index("d").c
T=T.loc[START:]; C=C.loc[START:]
yrs=(E.index[-1]-E.index[0]).days/365.25
print(f"\n=== TURNOVER / COST === one-way traded/yr {T.sum()/yrs:.2f}x NAV; model cost drag {C.sum()/yrs:.2%} NAV/yr (25bps/side)")
print(f"  at 50bps/side drag {2*C.sum()/yrs:.2%}/yr; STT 0.1% each side + stamp 0.015% buy alone = {(T.sum()/yrs)*(0.0010*0.5+0.0010*0.5)+ (T.sum()/yrs)*0.5*0.00015:.2%}/yr (before spread/impact)")
pickle.dump((S,R),open("out/stops.pkl","wb"))
