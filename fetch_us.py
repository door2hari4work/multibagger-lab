"""US universe: CURRENT S&P 500 members (Wikipedia list), Yahoo adjusted closes. SURVIVOR-BIASED like the India set.
Tune (<=2018) and SEALED (2019+) saved separately. Benchmarks: ^GSPC (price), SPY (dividend-adjusted TRI proxy)."""
import pandas as pd, yfinance as yf, config
raw = config.ROOT / "data" / "raw"
syms = pd.read_csv(raw / "sp500_current.csv")["Symbol"].tolist()
fr = []
for i in range(0, len(syms), 50):
    fr.append(yf.download(syms[i:i+50], start="2009-01-01", end="2026-10-03", auto_adjust=True, progress=False, threads=True)["Close"])
px = pd.concat(fr, axis=1).dropna(how="all"); px = px.loc[:, px.notna().sum() > 60]
ex = yf.download(["^GSPC", "SPY"], start="2009-01-01", end="2026-10-03", auto_adjust=True, progress=False)["Close"]
cut = pd.Timestamp(config.TUNE_END)
px[px.index <= cut].to_parquet(raw / "us_prices_tune.parquet"); px[px.index > cut].to_parquet(raw / "us_prices_test_SEALED.parquet")
ex[ex.index <= cut].to_parquet(raw / "us_extra_tune.parquet"); ex[ex.index > cut].to_parquet(raw / "us_extra_test_SEALED.parquet")
first = px.apply(lambda s: s.first_valid_index())
print("fetched", px.shape[1], "of", len(syms), "| alive on 2010-01-04:", int(px.loc["2010-01-04"].notna().sum()), "| last", px.index.max().date())
