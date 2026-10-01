from common import *
import indep
px, b = load()
dates = px.index
# ---- (1) coverage vs 500 slots
rows=[]
for y in range(2010, 2019):
    d = px.loc[f"{y}-01-01":].index[0]
    hist = px.ffill().loc[:d]      # same ffill the engine applies
    listed = int(px.loc[:d].iloc[-1].notna().sum())
    elig = int((hist.iloc[-252:].notna().all()).sum())          # >=252 clean bars, i.e. signal-eligible
    rows.append(dict(year_start=d.date(), with_price=listed, signal_eligible=elig, slots=500,
                     pct_slots_covered=round(100*listed/500,1)))
cov = pd.DataFrame(rows); print(cov.to_string(index=False)); cov.to_csv("out_surv_coverage.csv", index=False)
print("cols in file", px.shape[1], "| with ANY tune-window data", int(px.notna().any().sum()), "| missing from Yahoo (fetch_missing)", 2)

# ---- (2) end_policy zero vs last on the raw tune file
e0,_ = run(px, b, end_policy="zero"); e1,_ = run(px, b, end_policy="last")
print("zero", met(e0)); print("last", met(e1), "identical:", bool((e0-e1).abs().max() < 1e-12))
last_valid = px.apply(lambda s: s.last_valid_index())
print("names ending before 2018-12-21:", int((last_valid < dates[-1]-pd.Timedelta(days=10)).sum()))

# ---- (3) synthetic wipe-outs
pxf0 = None
def inject(px, rate, seed, variant):
    rng = np.random.default_rng(seed); p = px.copy(); dead = {}
    for y in range(2010, 2019):
        yidx = np.where(dates.year == y)[0]
        d0 = yidx[0]
        alive = [c for c in p.columns if (not np.isnan(p.iloc[d0][c])) and c not in dead]
        for c in alive:
            if rng.random() < rate:
                T = int(rng.choice(yidx[5:]))     # death bar uniform within year
                dead[c] = T
    for c, T in dead.items():
        if variant == "decay":      # glide to 15% over the 120 bars before the end, then dead
            a = max(T-120, 0); n = T - a
            f = np.exp(np.linspace(0, np.log(0.15), n+1))
            p.iloc[a:T+1, p.columns.get_loc(c)] = p.iloc[a:T+1, p.columns.get_loc(c)].values * f
        p.iloc[T+1:, p.columns.get_loc(c)] = np.nan
    return p, dead
def go(p, policy):
    q = bt.apply_end_policy(p, policy)
    eq, tr = indep.sim(indep.prep(q), b)
    e = eq.loc[START:]; e = e/e.iloc[0]; return met(e)
res = []
for rate in (0.01, 0.02, 0.03):
    for variant in ("gap", "decay"):
        for seed in range(30):
            p, dead = inject(px, rate, seed, variant)
            mz = go(p, "zero"); ml = go(p, "last")
            res.append(dict(rate=rate, variant=variant, seed=seed, ndead=len(dead), zero_CAGR=mz["CAGR"], zero_DD=mz["MaxDD"],
                            last_CAGR=ml["CAGR"], last_DD=ml["MaxDD"]))
R = pd.DataFrame(res); R.to_csv("out_surv_inject.csv", index=False)
g = R.groupby(["rate","variant"]).agg(ndead=("ndead","mean"), zero_CAGR=("zero_CAGR","mean"), zero_CAGR_sd=("zero_CAGR","std"),
        zero_DD=("zero_DD","mean"), last_CAGR=("last_CAGR","mean"), last_DD=("last_DD","mean"))
g["wipe_cost_CAGR"] = g.zero_CAGR - g.last_CAGR
g["vs_base_CAGR"] = g.zero_CAGR - 0.24519
print(g.round(4).to_string())
# cross-check one case with the official engine
p, dead = inject(px, 0.02, 0, "gap")
e,_ = bt.backtest(p, b, start=START, end_policy="zero", **BASE); e = e.loc[START:]; e/=e.iloc[0]
print("bt.backtest cross-check rate2% seed0 gap:", met(e), "vs indep", go(p,"zero"))

# ---- (4) held-name hazard (annual probability a HELD name is wiped out by a gap to ~0)
def sim_hazard(h, seed):
    rng = np.random.default_rng(seed); q = indep.prep(px); P = q.copy()
    sig = indep.signals(q, b)
    # day-by-day wipe: we need path-dependence -> use a wrapper by pre-running and re-running with injected events
    events = {}
    for it in range(6):         # iterate: events depend on holdings, which depend on events
        Pm = q.copy()
        for c, T in events.items(): Pm.iloc[T:, Pm.columns.get_loc(c)] *= 1e-4
        eq, tr = indep.sim(Pm, b, sig=sig)
        td = indep.trades_df(tr, dates)
        # draw wipe events for holdings (per held-day hazard)
        ev = {}
        for _, r in td.iterrows():
            nd = int(r.xi - r.ei)
            if nd <= 0: continue
            if rng.random() < 1-(1-h/252)**nd:
                ev.setdefault(r["name"], int(r.ei + rng.integers(1, nd+1)))
        if ev == events: break
        events = ev
    eq2, tr2 = indep.sim(Pm, b, sig=sig)
    e = eq2.loc[START:]; e = e/e.iloc[0]; return met(e), len(events)
hz = []
for h in (0.01, 0.02, 0.03, 0.05):
    ms = [sim_hazard(h, s) for s in range(15)]
    hz.append(dict(h=h, CAGR=np.mean([m[0]["CAGR"] for m in ms]), sd=np.std([m[0]["CAGR"] for m in ms]), MaxDD=np.mean([m[0]["MaxDD"] for m in ms]), events=np.mean([m[1] for m in ms])))
H = pd.DataFrame(hz); print(H.round(4).to_string(index=False)); H.to_csv("out_surv_hazard.csv", index=False)

# ---- (5) membership look-ahead proxies
fv = px.apply(lambda s: s.first_valid_index())
old = fv[fv <= pd.Timestamp("2009-03-01")].index       # listed before 2009-03 => has data at 2010 start
pxo = px[old]; pxn = px[[c for c in px.columns if c not in set(old)]]
eo,tro = run(pxo, b); print("only names listed by Mar-2009 (%d)" % len(old), met(eo,tro))
eq, tr = indep.sim(indep.prep(px), b); td = indep.trades_df(tr, dates); td = td[td.edate>=pd.Timestamp(START)]
td["ipo_after_2010"] = td["name"].isin(set(pxn.columns))
tot = td.pnl_frac.sum()
print("trades in post-Mar-2009-listed names: %.1f%% of trades, %.1f%% of sum pnl" % (100*td.ipo_after_2010.mean(), 100*td[td.ipo_after_2010].pnl_frac.sum()/tot))
