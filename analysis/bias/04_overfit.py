from common import *
import indep, itertools
from scipy.stats import norm, skew, kurtosis, spearmanr
px, b = load(); pxf = indep.prep(px); dates = pxf.index
def ev(eq, a=START, z=None):
    e = eq.loc[a:z]; e = e/e.iloc[0]; return e
# ---------- trial grid: (A) backtest.py's own 18-point grid  (B) signal-parameter variants (lookback, skip, ma)
sigcache = {}
def S(lb, sk, ma):
    key=(lb,sk,ma)
    if key not in sigcache: sigcache[key] = indep.signals(pxf, b, lookback=lb, skip=sk, ma=ma)
    return sigcache[key]
trials = []
for n, s, rg in itertools.product([10,15,25],[0.2,0.3,0.4],[True,False]):
    trials.append(dict(grp="A", top_n=n, stop=s, regime=rg, lb=252, sk=21, ma=200))
for lb, sk, ma in itertools.product([126,189,252],[0,21],[100,150,200]):
    if (lb,sk,ma)==(252,21,200): continue
    trials.append(dict(grp="B", top_n=15, stop=0.3, regime=True, lb=lb, sk=sk, ma=ma))
curves = {}
rows=[]
for i, t in enumerate(trials):
    sg = S(t["lb"], t["sk"], t["ma"])
    eq, tr = indep.sim(pxf, b, sig=sg, top_n=t["top_n"], stop=t["stop"], regime=t["regime"])
    curves[i] = eq
    e = ev(eq); m = met(e)
    ei = ev(eq, "2010-01-01", "2014-12-31"); eo = ev(eq, "2015-01-01", "2018-12-31")
    rows.append(dict(**t, CAGR=m["CAGR"], MaxDD=m["MaxDD"], Sharpe=m["Sharpe"],
                     IS_CAGR=met(ei)["CAGR"], IS_Sharpe=met(ei)["Sharpe"], OOS_CAGR=met(eo)["CAGR"], OOS_Sharpe=met(eo)["Sharpe"], OOS_MaxDD=met(eo)["MaxDD"]))
T = pd.DataFrame(rows); T.to_csv("out_overfit_grid.csv", index=False)
pd.set_option("display.width", 250)
print(T.round(3).to_string())
# the headline config is (A: 15, .3, True)
base_i = int(T[(T.grp=="A")&(T.top_n==15)&(T.stop==.3)&(T.regime)].index[0])
print("\nSharpe across 36 trials: mean %.3f sd %.3f min %.3f max %.3f; CAGR min %.3f max %.3f; frac with CAGR>bench 8.5%%: %.2f" % (
    T.Sharpe.mean(), T.Sharpe.std(), T.Sharpe.min(), T.Sharpe.max(), T.CAGR.min(), T.CAGR.max(), (T.CAGR>0.0847).mean()))

# ---------- Deflated Sharpe (Bailey & Lopez de Prado 2014)
r = eq_r = curves[base_i].loc[START:].pct_change().dropna()
T_ = len(r); sr = r.mean()/r.std(); g3 = skew(r); g4 = kurtosis(r, fisher=False)
var_sr_ann = T.Sharpe.var(); var_sr = var_sr_ann/252              # cross-trial variance of daily SR
gam = 0.5772156649
def sr0(N, v=var_sr): return np.sqrt(v)*((1-gam)*norm.ppf(1-1/N) + gam*norm.ppf(1-1/(N*np.e)))
def psr(sr, ref): return norm.cdf((sr-ref)*np.sqrt(T_-1)/np.sqrt(1-g3*sr+(g4-1)/4*sr**2))
print(f"\nheadline daily SR {sr:.4f} (ann {sr*np.sqrt(252):.3f}) T={T_} skew {g3:.2f} kurt {g4:.1f}; cross-trial sd of ann SR {np.sqrt(var_sr_ann):.3f}")
dsr=[]
for N in (1, 18, 36, 100, 500, 1000):
    s0 = 0 if N==1 else sr0(N); dsr.append(dict(N=N, SR0_ann=s0*np.sqrt(252), DSR_prob=psr(sr, s0), haircut_SR_ann=(sr-s0)*np.sqrt(252)))
D = pd.DataFrame(dsr); print(D.round(3).to_string(index=False)); D.to_csv("out_overfit_dsr.csv", index=False)
# also with a pessimistic cross-trial variance equal to the *whole* range seen in tests (sd ann SR 0.25)
print("N=1000 with sd(ann SR)=0.3:", round(sr0(1000,(0.3**2)/252)*np.sqrt(252),3))

# ---------- walk-forward inside 2010-2018: choose on 2010-14, evaluate 2015-18 (and reverse)
for name, (isa, isb), (osa, osb) in [("fwd", ("IS", "OOS"), ("", "")), ]: pass
iS = T.IS_Sharpe; oS = T.OOS_Sharpe
best = int(iS.idxmax()); print("\nWALK-FORWARD fwd: best IS-Sharpe trial", T.loc[best, ["grp","top_n","stop","regime","lb","sk","ma"]].to_dict())
print(" IS  CAGR %.3f Sharpe %.2f | OOS CAGR %.3f Sharpe %.2f MaxDD %.3f | OOS rank %d/%d | OOS median CAGR %.3f" % (T.IS_CAGR[best], T.IS_Sharpe[best], T.OOS_CAGR[best], T.OOS_Sharpe[best], T.OOS_MaxDD[best], int((oS>oS[best]).sum()+1), len(T), T.OOS_CAGR.median()))
print(" Spearman(IS Sharpe, OOS Sharpe) over 36 trials: %.2f" % spearmanr(iS, oS)[0])
# reverse direction
rows2=[]
for i in curves:
    ea = ev(curves[i], "2015-01-01", "2018-12-31"); eb = ev(curves[i], "2010-01-01", "2014-12-31")
    rows2.append((met(ea)["Sharpe"], met(eb)["Sharpe"], met(eb)["CAGR"]))
R2 = pd.DataFrame(rows2, columns=["S15_18","S10_14","C10_14"]); bb = int(R2.S15_18.idxmax())
print("WALK-FORWARD rev (tune 2015-18 -> test 2010-14): best trial", T.loc[bb,["grp","top_n","stop","regime","lb","sk","ma"]].to_dict(), "test CAGR %.3f; rank %d/36; spearman %.2f" % (R2.C10_14[bb], int((R2.S10_14>R2.S10_14[bb]).sum()+1), spearmanr(R2.S15_18, R2.S10_14)[0]))
# benchmark in the same windows
for a,z in (("2010-01-01","2014-12-31"),("2015-01-01","2018-12-31")):
    bb_ = b.loc[a:z]; print("bench",a,z, met(bb_/bb_.iloc[0]), "EW buyhold", met(bt.buy_hold(px.loc[a:z])))
