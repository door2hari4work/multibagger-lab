"""Diagnostic: random baselines WITHOUT regime filter / stops (20 seeds each) to see how much of the random gap is rule drag."""
from multiprocessing import Pool
from common import *
def j(a):
    m, s, rg, st = a; e, t = run(mode=m, seed=s, regime=rg, stop=st); r = summ(e); return dict(mode=m, seed=s, regime=rg, stop=st, CAGR=r["CAGR"], MaxDD=r["MaxDD"], FinalRs=r["FinalRs"])
if __name__ == "__main__":
    specs = [(m, s, rg, st) for m in ["random", "random_all"] for (rg, st) in [(False, NOSTOP), (False, 0.30)] for s in range(20)]
    with Pool(2) as p: rows = p.map(j, specs, chunksize=1)
    d = pd.DataFrame(rows); d.to_csv(ROOT/"results/tune/random_diag_20seeds.csv", index=False)
    print(d.groupby(["mode","regime","stop"])[["CAGR","MaxDD","FinalRs"]].median().round(3))
