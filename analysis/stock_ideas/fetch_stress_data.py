"""Download daily adjusted closes for the stress-test instruments (yfinance) into a local cache.
Weights/personal data are NOT used here. Output: analysis/stock_ideas/out/prices.csv (derived market data only)."""
import os, sys
import pandas as pd, yfinance as yf

TICKERS = ["MSFT","GOOGL","TSM","AMZN","NVDA","MU","META","APH","BNY",   # BNY = BNY Mellon (Yahoo symbol today; history back to 2005 as served by Yahoo)
           "QQQ","SPY","RSP","SMH","SOXX","XLF","GLD","^GSPC","^NDX","INR=X",
           "^NSEI","NIFTYBEES.NS","JUNIORBEES.NS","MID150BEES.NS","GOLDBEES.NS","^CRSLDX","^NSMIDCP","^CNXIT","^NSEBANK"]
OUT = os.path.join(os.path.dirname(__file__), "out"); os.makedirs(OUT, exist_ok=True)
frames = {}
for t in TICKERS:
    try:
        d = yf.download(t, start="2005-01-01", end="2026-10-14", auto_adjust=True, progress=False, threads=False)
        if d is None or d.empty:
            print("EMPTY", t); continue
        s = d["Close"]; s = s.iloc[:,0] if isinstance(s, pd.DataFrame) else s
        frames[t] = s.dropna(); print(t, s.dropna().index[0].date(), s.dropna().index[-1].date(), len(s.dropna()))
    except Exception as e:
        print("FAIL", t, repr(e)[:100])
pd.DataFrame(frames).to_csv(os.path.join(OUT, "prices.csv"))
