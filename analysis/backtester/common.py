"""Shared helpers for Agent 1. TUNE WINDOW ONLY (data_loader.load_tune). Does not modify backtest.py."""
import os, sys
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np, pandas as pd
import config, data_loader, backtest as bt

START = "2010-01-01"
PX, BENCH = data_loader.load_tune()
BASE = dict(top_n=15, stop=0.30, cost_bps=25, regime=True)
NOSTOP = 10.0   # stop >= 1 can never trigger (px < peak*(1-stop) is never true)

def run(**kw):
    """One backtest; returns (equity in Rs from 2010-01-01, trades)."""
    a = dict(BASE); a.update(kw)
    eq, tr = bt.backtest(PX, BENCH, start=START, **a)
    return data_loader.window(eq, START), tr

def summ(eq_rs, trades=None):
    m = bt.metrics(eq_rs / eq_rs.iloc[0], trades)
    pk = eq_rs.cummax(); dd_rs = (eq_rs - pk).min()
    m.update(FinalRs=float(eq_rs.iloc[-1]), MaxDD_Rs=float(dd_rs))
    return m

def inr(x):
    """Indian digit grouping."""
    x = int(round(x)); s = str(abs(x))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        s = ",".join(parts + [tail])
    return ("-" if x < 0 else "") + "Rs " + s
