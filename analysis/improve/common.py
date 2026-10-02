import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/multibagger-lab")
import backtest as bt, config
from data_loader import load_tune, RAW

START = "2010-01-01"
CASH = 0.06  # assumed liquid-fund yield on idle cash (India avg 2010-18 was ~7-8%); stated assumption

def load():
    px, b = load_tune()
    ex = pd.read_parquet(RAW / "extra_tune.parquet")
    return px, b, ex["^CRSLDX"].dropna(), ex["NIFTYBEES.NS"].dropna()

def regimes(px, b, n500, ma=200):
    breadth = (px > px.rolling(ma).mean()).where(px.notna() & px.rolling(ma).mean().notna()).mean(axis=1)
    r = {
        "R0_nifty50_ma200": (b > b.rolling(ma).mean()),
        "R1_nifty500_ma200": (n500 > n500.rolling(ma).mean()),
        "R2_breadth_gt40": breadth > 0.40,
        "R3_breadth_gt50": breadth > 0.50,
        "R5_none": pd.Series(True, index=px.index),
    }
    r["R4_n500_and_breadth40"] = r["R1_nifty500_ma200"].reindex(px.index).ffill().fillna(False) & r["R2_breadth_gt40"]
    return r

def scores(px, lookback=252, skip=21):
    mom = px.shift(skip) / px.shift(lookback) - 1
    vol = px.pct_change(fill_method=None).rolling(lookback).std() * np.sqrt(252)
    return {"S_mom": mom, "S_mom_vol": mom / vol}

def stats(eq, a=START, b_=None):
    e = eq.loc[a:b_] if b_ else eq.loc[a:]
    e = e / e.iloc[0]
    m = bt.metrics(e)
    return m["CAGR"], m["MaxDD"]
