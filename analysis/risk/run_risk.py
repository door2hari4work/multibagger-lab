"""Agent 3 risk analysis. Run: python analysis/risk/run_risk.py   (single process, tune window only, ~1 min)"""
import sys, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np, pandas as pd
import risk_lib as R, data_loader as dl, backtest as bt, config

OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
def _md(self, index=True, **kw):
    df = self.reset_index() if index else self
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows(): lines.append("| " + " | ".join(str(v) for v in r.values) + " |")
    return "\n".join(lines)
pd.DataFrame.to_markdown = _md
px, bench = dl.load_tune()
P = R.prep(px, bench)
f = lambda x: f"{x*100:.1f}%"
d = lambda x: "-" if x is None or pd.isna(x) else pd.Timestamp(x).strftime("%Y-%m-%d")
md = []

def row(name, s, extra=None):
    r = dict(name=name, CAGR=f(s["CAGR"]), final=R.inr(s["final"]), MaxDD=f(s["mdd"]), MaxDD_Rs=R.inr(-s["mdd_rs"]),
             peak=d(s["mdd_peak"]), trough=d(s["mdd_trough"]),
             recovery=("not recovered by 2018-12-31" if s["mdd_recovery"] is None else f'{d(s["mdd_recovery"])} ({s["mdd_days_to_recover"]}d peak-to-recovery)'),
             worst_year=f'{s["worst_year"]}: {f(s["worst_year_ret"])}', worst_12m=f'{f(s["worst_12m"])} ({d(s["worst_12m_start"])} to {d(s["worst_12m_end"])}, {R.inr(s["worst_12m_rs"])})',
             worst_month=f'{s["worst_month"]}: {f(s["worst_month_ret"])}', worst_day=f'{f(s["worst_day"])} ({d(s["worst_day_date"])})',
             longest_uw=f'{s["uw_days"]}d ({d(s["uw_peak"])} to {d(s["uw_recovery"])})', vol=f(s["vol"]), calmar=f'{s["calmar"]:.2f}',
             pct_time_dd_gt10=f(s["pct_time_underwater_10"]))
    if extra: r.update(extra)
    return r

def table(rows, cols):
    df = pd.DataFrame(rows)[cols]
    return df.to_markdown(index=False) if hasattr(df, "to_markdown") else df.to_string(index=False)

# ---------- 1. base case vs Nifty vs baselines ----------
base = R.run(P)
eb = R.rs_curve(base["eq"]); sb = R.risk_stats(eb)
en = dl.window(bench, "2010-01-01"); sn = R.risk_stats(en)
ew = dl.window(bt.buy_hold(px.loc["2009-01-01":]).reindex(px.index).ffill(), "2010-01-01")  # EW universe B&H (survivors)
sew = R.risk_stats(ew)
rnd = []
for sd in range(10):
    r = R.run(P, mode="random_all", seed=sd); rnd.append(R.risk_stats(R.rs_curve(r["eq"])))
rnd_mdd = np.median([x["mdd"] for x in rnd]); rnd_cagr = np.median([x["CAGR"] for x in rnd])
rnd_f = R.run(P, mode="random", seed=0); 
md.append("## 1. Base case vs Nifty\n")
cols = ["name","CAGR","final","MaxDD","MaxDD_Rs","peak","trough","recovery","worst_year","worst_12m","worst_month","worst_day","longest_uw","vol","calmar","pct_time_dd_gt10"]
md.append(table([row("BASE top15/stop30/regime", sb), row("Nifty 50 price (^NSEI)", sn), row("EW buy&hold of survivors", sew)], cols))
md.append(f"\nRandom unfiltered picks (15 names, same stops/regime), 10 seeds: median MaxDD {f(rnd_mdd)}, median CAGR {f(rnd_cagr)}, "
          f"MaxDD range {f(min(x['mdd'] for x in rnd))} to {f(max(x['mdd'] for x in rnd))}")
md.append("\nCalendar-year returns (Rs terms from Rs 10,00,000 at start of each year in brackets is not shown; % only):\n")
yr = pd.DataFrame({"Base": sb["year_rets"].values, "Nifty": sn["year_rets"].values, "EW survivors": sew["year_rets"].values}, index=sb["year_rets"].index.year)
yr["Base Rs P&L on start-of-year value"] = [R.inr(v) for v in (eb.resample("YE").last() - pd.concat([pd.Series([eb.iloc[0]]), eb.resample("YE").last().reset_index(drop=True)]).values[:-1])]
md.append((yr.assign(**{c: yr[c].map(f) for c in ["Base","Nifty","EW survivors"]})).to_markdown())
# all underwater stretches > 90d
uw = [s for s in R.underwater_stretches(eb) if s["days"] > 90]
md.append("\nUnderwater stretches > 90 calendar days (base):\n")
md.append(pd.DataFrame([dict(peak=d(s["peak"]), trough=d(s["trough"]), depth=f(s["depth"]), recovery=d(s["recovery"]) if s["recovery"] is not None else "not recovered", days=s["days"]) for s in uw]).to_markdown(index=False))
uwn = [s for s in R.underwater_stretches(en) if s["days"] > 90]
md.append("\nNifty underwater stretches > 90 days:\n")
md.append(pd.DataFrame([dict(peak=d(s["peak"]), trough=d(s["trough"]), depth=f(s["depth"]), recovery=d(s["recovery"]) if s["recovery"] is not None else "not recovered", days=s["days"]) for s in uwn]).to_markdown(index=False))
# regime exposure
g = base["gross"].loc["2010-01-01":]
md.append(f"\nBase case average gross exposure {f(g.mean())}; days fully in cash {f((g<1e-9).mean())}; days with <50% invested {f((g<0.5).mean())}.")
g18 = g.loc["2018-01-01":]
md.append(f"In 2018: average exposure {f(g18.mean())}; exposure on MDD-peak date {f(g.loc[sb['mdd_peak']])}, on MDD-trough date {f(g.loc[sb['mdd_trough']])}.")
# DD by calendar year for context
md.append("\nMax drawdown inside each calendar year (base / Nifty):\n")
rows = []
for y in range(2010, 2019):
    a = eb.loc[str(y)]; b = en.loc[str(y)]
    rows.append(dict(year=y, base=f((a/a.cummax()-1).min()), nifty=f((b/b.cummax()-1).min())))
md.append(pd.DataFrame(rows).to_markdown(index=False))

# ---------- 2. position sizing ----------
variants = [
 ("equal top10", dict(top_n=10)), ("equal top15 (BASE)", dict(top_n=15)), ("equal top25", dict(top_n=25)),
 ("equal top40", dict(top_n=40)),
 ("invvol top15", dict(top_n=15, sizing="invvol")), ("invvol top25", dict(top_n=25, sizing="invvol")),
 ("invvol top15 cap8%", dict(top_n=15, sizing="invvol", cap=0.08)),
 ("equal top10 cap7% (cash remainder)", dict(top_n=10, cap=0.07)),
 ("equal top15 cap5% (cash remainder)", dict(top_n=15, cap=0.05)),
 ("equal top15 + vol-target 15%", dict(top_n=15, vol_target=0.15)),
 ("equal top15 + vol-target 20%", dict(top_n=15, vol_target=0.20)),
 ("equal top25 + vol-target 20%", dict(top_n=25, vol_target=0.20)),
]
rows = []; curves = {}
for name, kw in variants:
    r = R.run(P, **kw); e = R.rs_curve(r["eq"]); s = R.risk_stats(e); curves[name] = e
    mw = r["maxw"].loc["2010-01-01":]
    tr = [t for t in r["trades"] if t["entry"]]
    rets = np.array([t["exit"]/t["entry"]-1 for t in tr])
    rows.append(row(name, s, dict(avg_gross=f(r["gross"].loc["2010-01-01":].mean()), max_weight_seen=f(mw.max()), worst_trade=f(rets.min()), trades=len(tr))))
md.append("\n## 2. Position sizing (stop 30%, regime on)\n")
md.append(table(rows, ["name","CAGR","final","MaxDD","MaxDD_Rs","trough","worst_year","worst_12m","worst_month","longest_uw","calmar","avg_gross","max_weight_seen","worst_trade","trades"]))
pd.DataFrame(rows).to_csv(OUT / "sizing.csv", index=False)

# ---------- 3. stop / regime grid ----------
rows = []; runs = {}
for stop in [None, 0.15, 0.20, 0.30, 0.40]:
    for rg in [True, False]:
        r = R.run(P, stop=stop, regime=rg); runs[(stop, rg)] = r
        e = R.rs_curve(r["eq"]); s = R.risk_stats(e)
        tr = [t for t in r["trades"] if t["entry"]]; rets = np.array([t["exit"]/t["entry"]-1 for t in tr])
        ns = sum(1 for t in tr if t["why"] == "stop")
        rows.append(row(f"stop={stop} regime={rg}", s, dict(trades=len(tr), n_stops=ns, worst_trade=f(rets.min()), p5_trade=f(np.percentile(rets,5)),
                       trades_lt_m30=int((rets < -0.30).sum()), trades_lt_m50=int((rets < -0.50).sum()), avg_gross=f(r["gross"].loc["2010-01-01":].mean()))))
md.append("\n## 3. Stop-loss and regime-filter effect (top_n=15, equal weight)\n")
md.append(table(rows, ["name","CAGR","MaxDD","MaxDD_Rs","trough","worst_year","worst_12m","worst_month","longest_uw","calmar","avg_gross","trades","n_stops","worst_trade","p5_trade","trades_lt_m30","trades_lt_m50"]))
pd.DataFrame(rows).to_csv(OUT / "stop_regime_grid.csv", index=False)

# ---------- 4. stop fills / gap risk / whipsaw ----------
def stop_stats(r, label):
    st = pd.DataFrame(r["stops"]);
    if st.empty: return None
    st = st[st.entry.notna()]
    st["trig_over"] = st.trig_close / st.level - 1          # how far below the stop level the trigger close already was
    st["next_gap"] = st.fill / st.trig_close - 1            # move between trigger close and execution close
    st["short"] = st.fill / st.level - 1                    # total shortfall vs stop level
    st["trade_ret"] = st.fill / st.entry - 1
    px_ = r["px"]; out = dict(label=label, n=len(st), fill_below_level=f((st.short < 0).mean()),
        median_shortfall=f(st.short.median()), mean_shortfall=f(st.short.mean()), p10_shortfall=f(st.short.quantile(.1)), worst_shortfall=f(st.short.min()),
        median_trig_over=f(st.trig_over.median()), mean_next_gap=f(st.next_gap.mean()), worst_next_gap=f(st.next_gap.min()),
        trade_ret_median=f(st.trade_ret.median()), trade_ret_worst=f(st.trade_ret.min()))
    cols = list(r["cols"])
    for h in (21, 63, 126):
        fw = []
        for _, x in st.iterrows():
            j = int(x.fill_i); k = min(j + h, px_.shape[0] - 1); c = cols.index(x.t)
            if j + h < px_.shape[0]: fw.append(px_[k, c] / x.fill - 1)
        fw = np.array(fw)
        out[f"fwd{h}d_mean"] = f(fw.mean()); out[f"fwd{h}d_pct_up"] = f((fw > 0).mean()); out[f"fwd{h}d_pct_up_gt10"] = f((fw > .10).mean())
    return out, st
rows = []; sts = {}
for stop in [0.15, 0.20, 0.30, 0.40]:
    o, st = stop_stats(runs[(stop, True)], f"stop {stop}"); rows.append(o); sts[stop] = st
md.append("\n## 4. Stop fills, gap risk, whipsaw (regime on)\n")
md.append(pd.DataFrame(rows).T.to_markdown())
st = sts[0.30]
md.append("\nWorst 8 stop executions at stop=30% (base):\n")
w8 = st.sort_values("short").head(8).copy()
w8["date"] = [d(base["dates"][int(i)]) for i in w8.fill_i]
w8["shortfall"] = w8.short.map(f); w8["trade_ret"] = w8.trade_ret.map(f); w8["weight_at_exit"] = w8.w.map(f)
md.append(w8[["t","date","shortfall","trade_ret","weight_at_exit"]].to_markdown(index=False))
# exposure to single-day gaps in holdings (close-to-close proxy for overnight gap)
rr = base["px"]; 
pxdf = pd.DataFrame(base["px"], index=base["dates"], columns=base["cols"])
retd = pxdf.pct_change()
# held mask: reconstruct weights via trades is heavy; use entry/exit intervals
held = pd.DataFrame(False, index=base["dates"], columns=base["cols"])
for t in base["trades"]:
    if t["entry_i"] is not None: held.iloc[t["entry_i"]:t["exit_i"], base["cols"].get_loc(t["t"])] = True
hr = retd.where(held).loc["2010-01-01":]
cnt = hr.notna().sum().sum()
md.append(f"\nHolding-days of single stocks in base case: {cnt:,}. Daily close-to-close drops while held: < -10%: {int((hr< -.10).sum().sum())} ({(hr< -.10).sum().sum()/cnt*100:.2f}% of holding-days), "
          f"< -15%: {int((hr< -.15).sum().sum())}, < -20%: {int((hr< -.20).sum().sum())}; worst single-stock day {f(np.nanmin(hr.values))}.")
# when stop is flagged, does exec price differ from level compared with nominal 30%?
# Does the stop cut tails: compare trades
def tailstats(r):
    tr = [t for t in r["trades"] if t["entry"]]; rets = np.array([t["exit"]/t["entry"]-1 for t in tr]); return rets
rs_stop, rs_none = tailstats(runs[(0.30, True)]), tailstats(runs[(None, True)])
md.append(f"\nTrade-return tails, regime on: with 30% stop: worst {f(rs_stop.min())}, 1st pct {f(np.percentile(rs_stop,1))}, 5th pct {f(np.percentile(rs_stop,5))}, mean {f(rs_stop.mean())}, n={len(rs_stop)}; "
          f"no stop: worst {f(rs_none.min())}, 1st pct {f(np.percentile(rs_none,1))}, 5th pct {f(np.percentile(rs_none,5))}, mean {f(rs_none.mean())}, n={len(rs_none)}.")

# ---------- 5. single-stock ruin ----------
md.append("\n## 5. Single-stock ruin\n")
rows = []
for n in (10, 15, 25):
    r = base if n == 15 else R.run(P, top_n=n)
    e = R.rs_curve(r["eq"]); mw = r["maxw"].loc["2010-01-01":]
    # Rs of largest position on each date, = maxw * NAV(Rs)
    pos_rs = mw * e
    i = pos_rs.idxmax()
    rows.append(dict(top_n=n, nominal_weight=f(1/n), Rs_at_start=R.inr(config.START_CAPITAL_INR/n),
        Rs_at_peak_NAV=R.inr(e.max()/n), max_drifted_weight=f(mw.max()), max_drifted_date=d(mw.idxmax()),
        largest_position_Rs_ever=R.inr(pos_rs.max()), on=d(i), pct_of_NAV_then=f(mw.loc[i]),
        Rs_loss_if_zero_at_trough=R.inr(sb['mdd_trough_val']/n if n==15 else e.loc[R.risk_stats(e)['mdd_trough']]/n)))
md.append(pd.DataFrame(rows).to_markdown(index=False))
# combined: MDD trough + simultaneous zero of largest drifted position
trough_nav = sb["mdd_trough_val"]; mwt = base["maxw"].loc[sb["mdd_trough"]]
md.append(f"\nCombined stress (base): at the MDD trough NAV {R.inr(trough_nav)} the largest position is {f(mwt)} of NAV = {R.inr(trough_nav*mwt)}; "
          f"zero on top of the observed drawdown would leave about {R.inr(trough_nav*(1-mwt))} ({f((trough_nav*(1-mwt)/sb['mdd_peak_val'])-1)} from the Rs {sb['mdd_peak_val']:,.0f} peak).")
# empirical: how many positions ended with -50% / -70% from entry; and survivors-only caveat
tr = [t for t in base["trades"] if t["entry"]]
rets = np.array([t["exit"]/t["entry"]-1 for t in tr])
md.append(f"Empirical (survivors only): worst realised single-position trade {f(rets.min())}; trades below -50%: {(rets<-.5).sum()}; below -30%: {(rets<-.3).sum()} of {len(rets)}.")
# wipeout drag illustration
rows = []
for p in (0.01, 0.02, 0.03):
    rows.append(dict(annual_prob_a_held_name_goes_to_zero=f(p), approx_CAGR_drag_pp=f"{p*100:.1f} pp (each name held ~1y; loss = 100% of that 1/15 slot) -> CAGR about {f(sb['CAGR']-p)}"))
md.append("\nIllustrative (assumed, NOT measured) wipeout drag: " + "; ".join(f"{r['annual_prob_a_held_name_goes_to_zero']}/name/yr -> -{r['approx_CAGR_drag_pp'].split(' ')[0]} pp CAGR" for r in rows) + ". A 1% annual per-name wipeout probability on 15 names means one wipeout every ~6.7 years, i.e. about Rs 66,667 per Rs 10,00,000 invested.")

# ---------- 6. max-loss budget ----------
md.append("\n## 6. Loss budget inputs\n")
ee = eb
dd = ee / ee.cummax() - 1
md.append(f"Peak Rs {sb['mdd_peak_val']:,.0f} -> trough Rs {sb['mdd_trough_val']:,.0f}. Base MDD {f(sb['mdd'])}; Nifty (price) MDD {f(sn['mdd'])}; ratio {sb['mdd']/sn['mdd']:.2f}x.")
# Worst peak-to-trough on the Rs 10L initial (from start, how far below initial capital did it get)
md.append(f"Lowest Rs value ever vs initial Rs 10,00,000: {R.inr(ee.min())} on {d(ee.idxmin())} ({f(ee.min()/ee.iloc[0]-1)} from start).")
# Rolling-entry drawdown: for every entry date, worst loss from that entry
ent = []
v = ee.values
runmin = np.minimum.accumulate(v[::-1])[::-1]  # min of future values incl. today
ent = runmin / v - 1
md.append(f"Rolling-entry view (someone who starts on any day in 2010-2018): median worst subsequent loss from entry {f(np.median(ent))}, 90th-percentile worst {f(np.percentile(ent,10))}, worst {f(ent.min())}; "
          f"share of entry days that at some point were >20% below entry value: {f((ent<-0.20).mean())}, >30%: {f((ent<-0.30).mean())}.")
nm = (en/en.cummax()-1).min()
md.append(f"Same for Nifty: median {f(np.median(np.minimum.accumulate(en.values[::-1])[::-1]/en.values-1))}.")
(OUT / "tables.md").write_text("\n".join(md))
print("\n".join(md))
