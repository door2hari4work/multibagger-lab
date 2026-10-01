"""Parallel (2 workers) jobs: grid, cost stress, random baselines. Usage: python run_all.py grid|cost|random"""
import sys, itertools, time
from multiprocessing import Pool
from common import *

def job(spec):
    kind, kw = spec
    eq, tr = run(**kw)
    m = summ(eq, tr)
    # per-calendar-year returns for the equity curve (kept for random baselines / reuse)
    return dict(kind=kind, **kw, **{k: (float(v) if v is not None else None) for k, v in m.items()})

def main(which):
    if which == "grid":
        specs = [("grid", dict(top_n=n, stop=s, regime=rg, lookback=lb, ma=ma))
                 for n, s, rg, lb, ma in itertools.product([10, 15, 25], [0.20, 0.30, 0.40, NOSTOP],
                                                          [True, False], [126, 189, 252], [100, 200])]
        out = ROOT / "results/tune/grid.csv"
    elif which == "cost":
        specs = [("cost", dict(cost_bps=c)) for c in [0, 25, 50, 75, 100, 150, 200, 300, 400]]
        out = ROOT / "results/tune/cost_stress.csv"
    elif which == "random":
        specs = [("random", dict(mode=m, seed=s)) for m in ["random", "random_all"] for s in range(200)]
        out = ROOT / "results/tune/random_baselines.csv"
    t = time.time()
    with Pool(2) as p:
        rows = []
        for i, r in enumerate(p.imap(job, specs, chunksize=1)):
            rows.append(r)
            if i % 10 == 0: print(which, i + 1, "/", len(specs), f"{time.time()-t:.0f}s", flush=True)
    pd.DataFrame(rows).to_csv(out, index=False); print("wrote", out, f"{time.time()-t:.0f}s")

if __name__ == "__main__":
    main(sys.argv[1])
