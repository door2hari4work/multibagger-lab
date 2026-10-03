"""Live month-end signal from the FROZEN India rule. Research output, not advice. Reads existing price files (through 2026-09-30)."""
import sys, pandas as pd, numpy as np
sys.path.insert(0, "/home/user/multibagger-lab/analysis/improve"); sys.path.insert(0, "/home/user/multibagger-lab")
from common import scores, RAW
px = pd.concat([pd.read_parquet(RAW/"prices_tune.parquet"), pd.read_parquet(RAW/"prices_test_SEALED.parquet")]).sort_index().ffill(limit=5)
ex = pd.concat([pd.read_parquet(RAW/"extra_tune.parquet"), pd.read_parquet(RAW/"extra_test_SEALED.parquet")]).sort_index()
n5 = ex["^CRSLDX"].dropna(); d = px.index[-1]
regime = bool(n5.iloc[-1] > n5.rolling(200).mean().iloc[-1])
print("as of", d.date(), "| Nifty 500", round(n5.iloc[-1]), "vs 200dMA", round(n5.rolling(200).mean().iloc[-1]), "-> regime", "ON (invest)" if regime else "OFF (cash)")
ma = px.rolling(200).mean(); hi = px.rolling(252).max(); mom = px.shift(21)/px.shift(252)-1; sc = scores(px)["S_mom_vol"]
elig = ((px.loc[d] > ma.loc[d]) & (mom.loc[d] > 0) & (px.loc[d] >= 0.75*hi.loc[d])).fillna(False)
stale = px.index[-1] - px.apply(lambda s: s.last_valid_index()); elig &= stale < pd.Timedelta(days=5)
c = sc.loc[d, elig[elig].index].sort_values(ascending=False)
print("eligible names:", len(c)); top = c.head(25)
meta = pd.read_csv(RAW/"nifty500_current.csv").set_index("Symbol")
out = pd.DataFrame({"company": [meta.loc[t[:-3], "Company Name"] for t in top.index], "industry": [meta.loc[t[:-3], "Industry"] for t in top.index],
                    "mom_12_1": mom.loc[d, top.index].round(2).values, "score": top.round(2).values, "px": px.loc[d, top.index].round(1).values}, index=top.index)
out["rs_if_equal_wt_of_10L"] = round(1_000_000/25) if regime else 0
print(out.to_string()); out.to_csv("/home/user/multibagger-lab/results/live_india_picks.csv")
