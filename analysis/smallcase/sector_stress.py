"""Sector-index stress test and staged-entry simulation. Yahoo price indices (no dividends), 2009-2026. Illustration of history, not a forecast.
Question: for a Rs 1,00,000 stake, how often did it fall >=25% below the money invested within 24 months, lump sum vs 5 monthly tranches?"""
import numpy as np, pandas as pd, yfinance as yf
T = {"Nifty 50": "^NSEI", "Nifty 500": "^CRSLDX", "Auto": "^CNXAUTO", "Energy": "^CNXENERGY", "Bank": "^NSEBANK", "Infra": "^CNXINFRA", "FMCG": "^CNXFMCG", "Pharma": "^CNXPHARMA", "IT": "^CNXIT", "Midcap 100": "^CRSMID", "Smallcap 100": "^CNXSC"}
px = yf.download(list(T.values()), start="2008-01-01", auto_adjust=True, progress=False)["Close"]
px = px.rename(columns={v: k for k, v in T.items()}).dropna(how="all")
print("data from", px.index.min().date(), "to", px.index.max().date(), "| first valid by series:", {c: str(px[c].first_valid_index().date()) for c in px.columns if px[c].notna().any()})
m = px.resample("ME").last()           # month-end series
ref = m["Nifty 500"].fillna(m["Nifty 50"]); hi52 = ref.rolling(12).max(); weak = (ref / hi52 - 1) <= -0.10   # market >=10% below its 12m high at the start month
rows = []
for c in [x for x in px.columns]:
    s = m[c].dropna()
    if len(s) < 60: continue
    dd = s / s.cummax() - 1; yrs = (s.index[-1] - s.index[0]).days / 365.25
    # time under water from worst trough
    tr = dd.idxmin(); pk = s.loc[:tr].idxmax(); rec = s.loc[tr:][s.loc[tr:] >= s.loc[pk]]
    # staged vs lump sum: for each start month, 24 months horizon
    lump_b, stg_b, lump_r, stg_r = [], [], [], []; w_l, w_s = [], []
    idx = s.index
    for i in range(len(idx) - 24):
        path = s.iloc[i:i + 25].values
        # lump: invest 1 at path[0]
        v = path / path[0]; worst_l = v.min() - 1
        # staged: 1/5 at months 0..4 (units bought at price)
        units = np.zeros(25); cash_in = np.zeros(25)
        for k in range(5): units[k:] += 0.2 / path[k]; cash_in[k:] += 0.2
        val = units * path; inv = cash_in; ratio = val / inv; worst_s = ratio.min() - 1
        lump_b.append(worst_l <= -0.25); stg_b.append(worst_s <= -0.25); lump_r.append(v[-1] - 1); stg_r.append(val[-1] / 1.0 - 1)
        if weak.reindex([idx[i]]).iloc[0] if idx[i] in weak.index else False: w_l.append(worst_l <= -0.25); w_s.append(worst_s <= -0.25)
    rows.append(dict(index=c, since=str(s.index[0].date()), CAGR=(s.iloc[-1] / s.iloc[0]) ** (1 / yrs) - 1, worst_dd=dd.min(), worst_dd_date=str(tr.date()),
                     months_to_recover=(None if len(rec) == 0 else int((rec.index[0].to_period("M") - tr.to_period("M")).n)), now_vs_peak=dd.iloc[-1],
                     breach25_lump=np.mean(lump_b), breach25_staged=np.mean(stg_b), med24m_lump=np.median(lump_r), p10_24m_lump=np.percentile(lump_r, 10),
                     breach25_lump_weakstart=(np.mean(w_l) if w_l else np.nan), breach25_staged_weakstart=(np.mean(w_s) if w_s else np.nan), n_weak=len(w_l)))
df = pd.DataFrame(rows)
pd.set_option("display.width", 250, "display.float_format", lambda v: f"{v:,.2f}")
print(df.to_string(index=False)); df.to_csv("/home/user/multibagger-lab/results/smallcase_sector_stress.csv", index=False)
