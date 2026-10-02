"""One-shot evaluation of the FROZEN rules (reports/FROZEN_RULES.md). `--dry` uses tune data only (no lock);
`--final` loads the sealed 2019-2026 files via holdout.load_range(final_run=True) exactly once."""
import sys, json, numpy as np, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, "analysis/improve")
import backtest as bt, config, holdout
from common import CASH, scores, RAW

MODE = sys.argv[1] if len(sys.argv) > 1 else "--dry"
if MODE == "--final":
    holdout.load_range(config.TEST_START, config.TEST_END, purpose="frozen-candidate one-shot test", final_run=True)
    px = pd.concat([pd.read_parquet(RAW / "prices_tune.parquet"), pd.read_parquet(RAW / "prices_test_SEALED.parquet")]).sort_index()
    ex = pd.concat([pd.read_parquet(RAW / "extra_tune.parquet"), pd.read_parquet(RAW / "extra_test_SEALED.parquet")]).sort_index()
    b = pd.concat([pd.read_parquet(RAW / "bench_tune.parquet"), pd.read_parquet(RAW / "bench_test_SEALED.parquet")]).iloc[:, 0].sort_index()
    EV0, EV1 = "2019-01-01", "2026-09-30"; OUT = "results/test/"
else:
    px = pd.read_parquet(RAW / "prices_tune.parquet"); ex = pd.read_parquet(RAW / "extra_tune.parquet")
    b = pd.read_parquet(RAW / "bench_tune.parquet").iloc[:, 0]; EV0, EV1 = "2017-01-01", "2018-12-31"; OUT = "/tmp/claude-0/-home-user-multibagger-lab/cfc67b4e-fdd4-507f-8bec-b536e5867c2e/scratchpad/dry_"
n500 = ex["^CRSLDX"].dropna(); tri = ex["NIFTYBEES.NS"].dropna()
reg = (n500 > n500.rolling(200).mean()); SC = scores(px)["S_mom_vol"]
CAND = dict(top_n=25, stop=0.30, cost_bps=25, regime=True, regime_series=reg, score=SC, cash_rate=CASH, start=EV0)

def curve(eq):
    e = eq.loc[EV0:EV1]; return e / e.iloc[0]
def detail(e):
    m = bt.metrics(e); dd = e / e.cummax() - 1; tr_ = dd.idxmin(); pk = e.loc[:tr_].idxmax()
    rec = e.loc[tr_:][e.loc[tr_:] >= e.loc[pk]]
    yr = e.resample("YE").last().pct_change(); yr.iloc[0] = e.resample("YE").last().iloc[0] / e.iloc[0] - 1
    mo = e.resample("ME").last().pct_change().dropna()
    return dict(CAGR=m["CAGR"], MaxDD=m["MaxDD"], final_rs=config.START_CAPITAL_INR * e.iloc[-1], peak=str(pk.date()), trough=str(tr_.date()),
                recovery_days=(int((rec.index[0] - tr_).days) if len(rec) else None), worst_year=(str(yr.idxmin().year), float(yr.min())),
                worst_month=(str(mo.idxmin().date()), float(mo.min())), years={str(k.year): round(float(v), 3) for k, v in yr.items()})
def rnd(a):
    mode, seed = a; eq, _ = bt.backtest(px, b, mode=mode, seed=seed, **CAND); e = curve(eq); m = bt.metrics(e); return mode, m["CAGR"], m["MaxDD"]
def cst(c):
    k = dict(CAND); k["cost_bps"] = c; eq, _ = bt.backtest(px, b, **k); m = bt.metrics(curve(eq)); return c, m["CAGR"], m["MaxDD"]

if __name__ == "__main__":
    NS = 150 if MODE == "--final" else 4
    eq, tr = bt.backtest(px, b, **CAND); e = curve(eq); res = {"strategy": detail(e)}
    t = pd.DataFrame(tr, columns=["t", "e", "x", "why"]).dropna(); t["r"] = t.x / t.e - 1
    res["trades"] = dict(n=len(t), hit=float((t.r > 0).mean()), over5x=int((t.r >= 4).sum()), worst=float(t.r.min()))
    top = t.groupby("t").r.sum().sort_values(ascending=False).head(3).index.tolist(); eq2, _ = bt.backtest(px.drop(columns=top), b, **CAND)
    res["drop_top3"] = dict(names=top, **{k: v for k, v in bt.metrics(curve(eq2)).items() if k in ("CAGR", "MaxDD")})
    res["bench_BeES_TRI_proxy"] = detail(tri.loc[EV0:EV1] / tri.loc[EV0:EV1].iloc[0]); res["bench_nifty500_price"] = detail(n500.loc[EV0:EV1] / n500.loc[EV0:EV1].iloc[0])
    res["bench_nifty50_price"] = detail(b.loc[EV0:EV1] / b.loc[EV0:EV1].iloc[0])
    sv = px.loc[EV0:EV1]; sv = sv.loc[:, sv.iloc[0].notna()]; r_ = sv.pct_change(fill_method=None).mean(axis=1).fillna(0)
    res["survivor_equal_weight_hold"] = detail((1 + r_).cumprod())
    with Pool(4) as p:
        rr = p.map(rnd, [(m, s) for m in ("random", "random_all") for s in range(NS)]); cc = p.map(cst, [50, 100, 150])
    rd = pd.DataFrame(rr, columns=["mode", "CAGR", "MaxDD"]); rd.to_csv(OUT + "random.csv", index=False)
    s = res["strategy"]; res["random"] = {m: dict(CAGR_median=float(x.CAGR.median()), MaxDD_median=float(x.MaxDD.median()),
        share_cagr_below_strategy=float((x.CAGR < s["CAGR"]).mean()), share_maxdd_worse_than_strategy=float((x.MaxDD < s["MaxDD"]).mean())) for m, x in rd.groupby("mode")}
    res["costs_bps_per_side"] = {str(c): dict(CAGR=a, MaxDD=d) for c, a, d in cc}
    json.dump(res, open(OUT + "result.json", "w"), indent=1, default=str); pd.DataFrame({"strategy": e}).to_csv(OUT + "curve.csv")
    print(json.dumps(res, indent=1, default=str))
