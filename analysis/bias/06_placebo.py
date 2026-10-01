from common import *
import indep
px, b = load(); pxf = indep.prep(px); dates = pxf.index
def cagr(eq):
    e = eq.loc[START:]; e = e/e.iloc[0]; return met(e)
sig = indep.signals(pxf, b)
sig_all = indep.signals(pxf, b, filt=False)
keys = sorted(k for k in sig if dates[k] >= pd.Timestamp(START))
base = cagr(indep.sim(pxf, b, sig=sig)[0]); print("base", base)
# (1) fixed lag placebo: use the candidate list from m month-ends away (m<0 = FUTURE list = deliberate look-ahead)
rows = []
for m in (-3, -2, -1, 0, 1, 2, 3, 6, 12):
    perm = {}
    for j, k in enumerate(keys):
        jj = min(max(j + m, 0), len(keys)-1); perm[k] = keys[jj]
    mm = cagr(indep.sim(pxf, b, sig=sig, perm=perm)[0]); rows.append(dict(month_shift=m, **mm))
L = pd.DataFrame(rows); print(L.round(4).to_string(index=False)); L.to_csv("out_placebo_lag.csv", index=False)
# (2) random permutation of month->list assignment (1000 draws)
rng = np.random.default_rng(42); pc = []; pdd = []
for it in range(1000):
    p = rng.permutation(len(keys)); perm = {k: keys[p[j]] for j, k in enumerate(keys)}
    m = cagr(indep.sim(pxf, b, sig=sig, perm=perm)[0]); pc.append(m["CAGR"]); pdd.append(m["MaxDD"])
pc = np.array(pc); pdd = np.array(pdd)
print("PLACEBO permuted-month lists (1000): CAGR median %.4f p5 %.4f p95 %.4f max %.4f | MaxDD median %.3f | base percentile %.1f%%" % (
    np.median(pc), np.percentile(pc,5), np.percentile(pc,95), pc.max(), np.median(pdd), 100*(pc < base["CAGR"]).mean()))
# (3) random baselines per protocol: same filters / no filters, 1000 draws each
def rnd(sg, seed):
    r = np.random.default_rng(seed); s2 = {}
    for k, (c, rg) in sg.items():
        c = list(c); r.shuffle(c); s2[k] = (c, rg)
    return s2
for name, sg in (("random (same filters)", sig), ("random_all (no filters)", sig_all)):
    cs = []; ds = []
    for seed in range(1000):
        m = cagr(indep.sim(pxf, b, sig=rnd(sg, seed))[0]); cs.append(m["CAGR"]); ds.append(m["MaxDD"])
    cs = np.array(cs); ds = np.array(ds)
    print("%s x1000: CAGR median %.4f p5 %.4f p95 %.4f | MaxDD median %.3f p5 %.3f | base CAGR percentile %.1f%% | base MaxDD better than %.1f%% of draws" % (
        name, np.median(cs), np.percentile(cs,5), np.percentile(cs,95), np.median(ds), np.percentile(ds,5), 100*(cs < base["CAGR"]).mean(), 100*(ds < base["MaxDD"]).mean()))
# EW buy&hold and regime-only
print("EW buyhold", met(bt.buy_hold(px.loc[START:])))
