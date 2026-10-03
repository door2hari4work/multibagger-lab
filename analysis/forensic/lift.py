"""Multibagger forensic (TUNE WINDOW ONLY). For every (month-end t, stock) with 252d history, past-only features and forward outcomes.
Outcomes use adjusted prices: 3y fwd return (>=3x 'mb3', <=-30% 'loss3'), 5y fwd (>=5x 'mb5'). Only starts whose forward window ends <= 2018-12-31.
Universe is survivors-only: base rates of winners are INFLATED and losers DEFLATED; read LIFT relative to the same universe, not absolutes."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/multibagger-lab")
MK = sys.argv[1] if len(sys.argv) > 1 else "india"
RAW = "/home/user/multibagger-lab/data/raw/"
px = pd.read_parquet(RAW + ("prices_tune.parquet" if MK == "india" else "us_prices_tune.parquet"))
px = px.ffill(limit=5)
mom = px.shift(21) / px.shift(252) - 1; m6 = px.shift(21) / px.shift(126) - 1
hi = px.rolling(252).max(); ma = px.rolling(200).mean()
vol = px.pct_change(fill_method=None).rolling(252).std() * np.sqrt(252)
feat = {"mom12_1": mom, "mom_over_vol": mom / vol, "dist_high": px / hi, "above200": (px > ma).astype(float).where(px.notna() & ma.notna()),
        "mom6": m6, "vol": vol}
idx = px.index; me = px.groupby([idx.year, idx.month]).tail(1).index
pos = {d: i for i, d in enumerate(idx)}
rows = []
for d in me:
    i = pos[d]
    if i + 756 >= len(idx) or i < 252: continue
    p0 = px.iloc[i]; r3 = px.iloc[i + 756] / p0 - 1; r5 = px.iloc[i + 1260] / p0 - 1 if i + 1260 < len(idx) else pd.Series(np.nan, index=px.columns)
    f = pd.DataFrame({k: v.loc[d] for k, v in feat.items()}); f["r3"] = r3; f["r5"] = r5; f["date"] = d
    f = f.dropna(subset=["r3", "mom12_1"]); rows.append(f)
df = pd.concat(rows).reset_index().rename(columns={"index": "sym", "Ticker": "sym"}); df["year"] = df.date.dt.year
df["mb3"] = df.r3 >= 2; df["loss3"] = df.r3 <= -0.30; df["mb5"] = df.r5 >= 4
df["rank_mv"] = df.groupby("date").mom_over_vol.rank(pct=True); df["rank_m"] = df.groupby("date").mom12_1.rank(pct=True)
S = {
 "ALL (base rate)": pd.Series(True, index=df.index),
 "strategy filters (>200d, mom>0, within 25% of high)": (df.above200 == 1) & (df.mom12_1 > 0) & (df.dist_high >= 0.75),
 "filters + top decile mom/vol": (df.above200 == 1) & (df.mom12_1 > 0) & (df.dist_high >= 0.75) & (df.rank_mv >= 0.9),
 "top decile mom12-1 only": df.rank_m >= 0.9,
 "top decile mom/vol only": df.rank_mv >= 0.9,
 "within 5% of 52w high": df.dist_high >= 0.95,
 "bottom half mom (losers)": df.rank_m < 0.5,
 "low vol third + filters": (df.above200 == 1) & (df.mom12_1 > 0) & (df.vol <= df.groupby("date").vol.transform(lambda s: s.quantile(1/3))),
}
base = S["ALL (base rate)"]; out = []
for k, m in S.items():
    x = df[m]; y5 = x.dropna(subset=["r5"])
    out.append(dict(signal=k, n=len(x), mb3=x.mb3.mean(), loss3=x.loss3.mean(), med_r3=x.r3.median(), p10_r3=x.r3.quantile(0.1),
                    mb5=y5.mb5.mean() if len(y5) else np.nan, lift_mb3=x.mb3.mean() / df.mb3.mean(), lift_loss3=x.loss3.mean() / df.loss3.mean()))
res = pd.DataFrame(out); pd.set_option("display.width", 250, "display.float_format", lambda v: f"{v:,.3f}")
print(f"== {MK.upper()} | start months {df.date.min().date()}..{df.date.max().date()} | stocks {df.sym.nunique()} | observations {len(df)}")
print(res.to_string(index=False))
yrs = df.assign(sig=S["filters + top decile mom/vol"]).groupby("year").apply(lambda g: pd.Series(dict(n_sig=int(g.sig.sum()), mb3_sig=g[g.sig].mb3.mean(), mb3_all=g.mb3.mean(), loss_sig=g[g.sig].loss3.mean(), loss_all=g.loss3.mean())))
print("\nby start year (filters + top decile mom/vol vs all):"); print(yrs.to_string())
res.to_csv(f"/home/user/multibagger-lab/results/tune/lift_{MK}.csv", index=False)
