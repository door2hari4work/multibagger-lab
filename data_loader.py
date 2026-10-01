"""Tune-window loader. Agents use ONLY this. Test files (*_SEALED) are read solely by final_test.py via holdout.py."""
import pandas as pd, config

RAW = config.ROOT / "data" / "raw"

def load_tune():
    """Returns (prices, bench_price_index) up to 2018-12-31 incl. warm-up from 2009. Trade only from config.TUNE_START."""
    px = pd.read_parquet(RAW / "prices_tune.parquet")
    b = pd.read_parquet(RAW / "bench_tune.parquet").iloc[:, 0]
    assert px.index.max() <= pd.Timestamp(config.TUNE_END)
    return px, b

def window(eq, start=None):
    """Slice an equity curve to the evaluation window and rebase to Rs START_CAPITAL_INR."""
    eq = eq.loc[pd.Timestamp(start or config.TUNE_START):]
    return eq / eq.iloc[0] * config.START_CAPITAL_INR
