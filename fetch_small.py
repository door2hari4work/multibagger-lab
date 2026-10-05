"""Small/micro-cap universes (CURRENT members, survivor-biased and WORSE than large caps): NSE Microcap 250 (.NS) and S&P 600 (US).
Tune (<=2018) / SEALED (2019+) split like fetch_data.py. Nifty Smallcap 250 is a subset of the Nifty 500 data already fetched."""
import pandas as pd, yfinance as yf, config
raw = config.ROOT / "data" / "raw"; cut = pd.Timestamp(config.TUNE_END)
jobs = {"micro": [s.strip() + ".NS" for s in pd.read_csv(raw / "ind_niftymicrocap250_list.csv")["Symbol"]],
        "sp600": pd.read_csv(raw / "sp600_current.csv")["Symbol"].tolist()}
for k, syms in jobs.items():
    fr = []
    for i in range(0, len(syms), 50):
        fr.append(yf.download(syms[i:i+50], start="2009-01-01", end="2026-10-06", auto_adjust=True, progress=False, threads=True)["Close"])
    px = pd.concat(fr, axis=1).dropna(how="all"); px = px.loc[:, px.notna().sum() > 60]
    px[px.index <= cut].to_parquet(raw / f"{k}_prices_tune.parquet"); px[px.index > cut].to_parquet(raw / f"{k}_prices_test_SEALED.parquet")
    print(k, "fetched", px.shape[1], "of", len(syms), "| alive on first 2010 trading day:", int(px.loc["2010-01-04":"2010-01-08"].iloc[0].notna().sum()))
