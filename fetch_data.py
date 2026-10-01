"""Fetch Yahoo prices for the CURRENT Nifty 500 list. SURVIVORSHIP-BIASED by construction (today's members only).
Writes tune and test files separately so tuning code never touches 2019+ data.
Warm-up: tune file starts 2009-01-01 so 252d momentum/200d MA are valid by 2010-01-01; no trading before TUNE_START."""
import pandas as pd, yfinance as yf, config
from pathlib import Path

raw = config.ROOT / "data" / "raw"
syms = pd.read_csv(raw / "nifty500_current.csv")["Symbol"].str.strip().tolist()
tick = [s + ".NS" for s in syms]
frames = []
for i in range(0, len(tick), 50):
    df = yf.download(tick[i:i+50], start="2009-01-01", end="2026-10-01", auto_adjust=True, progress=False, threads=True)
    frames.append(df["Close"])
px = pd.concat(frames, axis=1).dropna(how="all")
px = px.loc[:, px.notna().sum() > 60]
bench = yf.download("^NSEI", start="2009-01-01", end="2026-10-01", auto_adjust=True, progress=False)["Close"].iloc[:, 0].rename("^NSEI")
cut = pd.Timestamp(config.TUNE_END)
px[px.index <= cut].to_parquet(raw / "prices_tune.parquet"); bench[bench.index <= cut].to_frame().to_parquet(raw / "bench_tune.parquet")
px[px.index > cut].to_parquet(raw / "prices_test_SEALED.parquet"); bench[bench.index > cut].to_frame().to_parquet(raw / "bench_test_SEALED.parquet")
missing = sorted(set(tick) - set(px.columns))
pd.Series(missing).to_csv(raw / "fetch_missing.csv", index=False, header=["missing"])
print("fetched", px.shape[1], "of", len(tick), "| missing", len(missing), "| tune rows", (px.index <= cut).sum())
