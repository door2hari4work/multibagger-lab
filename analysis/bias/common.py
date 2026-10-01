import sys, time, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np, pandas as pd
import backtest as bt, data_loader as dl, config

START = "2010-01-01"
BASE = dict(top_n=15, stop=0.30, cost_bps=25, regime=True)

def load():
    return dl.load_tune()

def run(px, bench, start=START, win=None, **kw):
    a = dict(BASE); a.update(kw)
    eq, tr = bt.backtest(px, bench, start=start, **a)
    e = eq.loc[pd.Timestamp(win or start):]
    e = e / e.iloc[0]
    return e, tr

def met(e, tr=None):
    m = bt.metrics(e, tr)
    return {k: (float(v) if not isinstance(v, (int,)) else v) for k, v in m.items()}
