"""Step 2: ~2y adjusted daily prices for the universe via mblab.data.prices (cached, reliability-checked) -> price signals.
Usage: python step2_prices.py <universe_csv> <signals_csv_out>"""
import sys, os
import pandas as pd, numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from mblab.data import prices as P
from mblab import discovery as D

uni = pd.read_csv(sys.argv[1])
tk = uni["ticker"].tolist() + ["^GSPC"]
pdta = P.get_ohlcv(tk, refresh=True)
print("panel", pdta.close.shape, "last", pdta.close.index.max().date(), flush=True)
sig = D.price_signals(pdta)
liq = P.liquidity_table(pdta.close, pdta.volume, min_adv=5e6)
rel = P.reliability_check(pdta.close.tail(P.MIN_HISTORY + 7), tickers=uni["ticker"].tolist(), min_history=P.MIN_HISTORY,
                          as_of=pdta.close.index.max(), volume=pdta.volume.reindex_like(pdta.close.tail(P.MIN_HISTORY + 7)))
sig = sig.join(liq[["adv", "passes_liquidity"]]).join(rel[["flags", "max_abs_move", "max_move_date"]])
sig["flags"] = sig["flags"].map(lambda x: ";".join(x) if isinstance(x, list) else "no_data")
# extra: 6m / 3m returns and 1y return
c = pdta.close
def ret(n): return c.apply(lambda s: (s.dropna().iloc[-1] / s.dropna().iloc[-1 - n] - 1) if s.dropna().shape[0] > n + 1 else np.nan)
sig["ret_1y"] = ret(252); sig["ret_6m"] = ret(126); sig["ret_3m"] = ret(63); sig["ret_1m"] = ret(21)
sig.to_csv(sys.argv[2])
g = sig.loc["^GSPC"]; print("S&P500", g["price"], "ma200", g["ma200"], "regime_on", g["price"] > g["ma200"], "ret_1y", g["ret_1y"])
print(sig.loc[uni["ticker"]].passes_liquidity.value_counts(dropna=False).to_dict())
