"""Live signals + quality screen (INFORMATION, not backtested). Frozen India rule + same rule on US. Quality = latest annual statements from Yahoo
(revenue growth, EBITDA margin trend, OCF/EBITDA). Yahoo has ~4 fiscal years only, so this can only be used going forward, never to backtest."""
import sys, time, numpy as np, pandas as pd, yfinance as yf
sys.path.insert(0, "/home/user/multibagger-lab/analysis/improve"); sys.path.insert(0, "/home/user/multibagger-lab")
from common import scores, RAW
def live(px, idx, label, n=25):
    d = px.index[-1]; reg = bool(idx.iloc[-1] > idx.rolling(200).mean().iloc[-1])
    ma = px.rolling(200).mean(); hi = px.rolling(252).max(); mom = px.shift(21) / px.shift(252) - 1; sc = scores(px)["S_mom_vol"]
    el = ((px.loc[d] > ma.loc[d]) & (mom.loc[d] > 0) & (px.loc[d] >= 0.75 * hi.loc[d])).fillna(False)
    el &= (px.index[-1] - px.apply(lambda s: s.last_valid_index())) < pd.Timedelta(days=5)
    top = sc.loc[d, el[el].index].sort_values(ascending=False).head(n)
    print(f"{label}: as of {d.date()} | index {idx.iloc[-1]:,.0f} vs 200dMA {idx.rolling(200).mean().iloc[-1]:,.0f} -> regime {'ON' if reg else 'OFF (rule says cash)'} | eligible {int(el.sum())}")
    return reg, top, mom.loc[d]
def quality(t):
    try:
        k = yf.Ticker(t); f = k.financials; c = k.cashflow
        rev = f.loc["Total Revenue"].dropna(); eb = f.loc["EBITDA"].dropna() if "EBITDA" in f.index else None
        ocf = c.loc["Operating Cash Flow"].dropna() if "Operating Cash Flow" in c.index else None
        if len(rev) < 2 or eb is None or len(eb) < 2: return dict(ticker=t, note="insufficient data")
        rg = rev.iloc[0] / rev.iloc[1] - 1; m0, m1 = eb.iloc[0] / rev.iloc[0], eb.iloc[1] / rev.iloc[1]
        return dict(ticker=t, fy=str(rev.index[0].date()), rev_growth=rg, ebitda_margin=m0, margin_chg=m0 - m1, ocf_ebitda=(ocf.iloc[0] / eb.iloc[0]) if ocf is not None and eb.iloc[0] > 0 else np.nan)
    except Exception as e: return dict(ticker=t, note="error")
def gate(r):
    if "note" in r and isinstance(r.get("note"), str): return "NO DATA"
    return "PASS" if (r["margin_chg"] > 0 and r["rev_growth"] >= 0.10 and r["ocf_ebitda"] >= 0.5) else "fails: " + ",".join([n for n, ok in [("margin", r["margin_chg"] > 0), ("growth", r["rev_growth"] >= 0.10), ("cash", r["ocf_ebitda"] >= 0.5)] if not ok])
out = []
pi = pd.concat([pd.read_parquet(RAW/"prices_tune.parquet"), pd.read_parquet(RAW/"prices_test_SEALED.parquet")]).sort_index().ffill(limit=5)
ei = pd.concat([pd.read_parquet(RAW/"extra_tune.parquet"), pd.read_parquet(RAW/"extra_test_SEALED.parquet")]).sort_index()["^CRSLDX"].dropna()
pu = pd.concat([pd.read_parquet(RAW/"us_prices_tune.parquet"), pd.read_parquet(RAW/"us_prices_test_SEALED.parquet")]).sort_index().ffill(limit=5)
eu = pd.concat([pd.read_parquet(RAW/"us_extra_tune.parquet"), pd.read_parquet(RAW/"us_extra_test_SEALED.parquet")]).sort_index()["^GSPC"].dropna()
for label, px, idx in [("INDIA", pi, ei), ("US", pu, eu)]:
    reg, top, mom = live(px, idx, label)
    for t in top.index[:25]:
        r = quality(t); r.update(market=label, mom_12_1=mom[t], score=top[t], regime_on=reg); out.append(r); time.sleep(0.4)
df = pd.DataFrame(out); df["gate"] = df.apply(lambda r: gate(r.to_dict()), axis=1)
df.to_csv("/home/user/multibagger-lab/results/live_quality_screen.csv", index=False)
pd.set_option("display.width", 250, "display.float_format", lambda v: f"{v:,.2f}")
print(df[["market", "ticker", "mom_12_1", "rev_growth", "ebitda_margin", "margin_chg", "ocf_ebitda", "gate"]].to_string(index=False))
print(df.groupby("market").gate.apply(lambda s: (s == "PASS").sum()).to_dict(), "pass of 25 each")
