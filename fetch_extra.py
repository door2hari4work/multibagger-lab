"""Extra series: Nifty 500 index (^CRSLDX, price) and Nifty BeES (NIFTYBEES.NS, dividend-adjusted TRI proxy).
Tune (<=2018) and SEALED (2019+) written separately, like fetch_data.py."""
import pandas as pd, yfinance as yf, config
raw = config.ROOT / "data" / "raw"
d = yf.download(["^CRSLDX", "NIFTYBEES.NS"], start="2009-01-01", end="2026-10-01", auto_adjust=True, progress=False)["Close"]
cut = pd.Timestamp(config.TUNE_END)
d[d.index <= cut].to_parquet(raw / "extra_tune.parquet"); d[d.index > cut].to_parquet(raw / "extra_test_SEALED.parquet")
print(d.notna().sum().to_dict())
