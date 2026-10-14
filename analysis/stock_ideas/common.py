"""Shared helpers: price loading with the known Yahoo split artifact fixed (NIFTYBEES.NS and GOLDBEES.NS, 2019-12-19/23)."""
import os, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
def load_prices():
    P = pd.read_csv(os.path.join(OUT, "prices.csv"), index_col=0, parse_dates=True)
    for t in ("NIFTYBEES.NS", "GOLDBEES.NS"):          # unadjusted 10:1 split days: -89.9% / +896.9% (and -99%/+9900%); combine the two days
        s = P[t].dropna(); r = s.pct_change()
        d1, d2 = pd.Timestamp("2019-12-19"), pd.Timestamp("2019-12-23")
        r.loc[d1] = (1 + r.loc[d1]) * (1 + r.loc[d2]) - 1; r.loc[d2] = 0.0
        P[t] = (1 + r.fillna(0)).cumprod() * s.iloc[0]; P.loc[~P.index.isin(s.index), t] = np.nan
    return P.ffill(limit=5)
