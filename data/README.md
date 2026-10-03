# Data layout (not committed; you supply it)

data/raw/
  prices/            daily OHLCV, split/bonus-adjusted, ONE file per symbol incl. delisted names
  index/             Nifty 50 TRI, Nifty 500 daily levels
  constituents.csv   point-in-time Nifty 500 membership: symbol, from_date, to_date
  delistings.csv     symbol, delist_date, reason, final_price (0 if wiped out)
  corp_actions.csv   splits, bonuses, demergers, mergers (symbol mapping across renames/mergers)
data/pit/
  fundamentals.parquet   symbol, period_end, filed_date, revenue, ebitda, ocf, capex, ...
                         `filed_date` is REQUIRED; if absent, period_end + lag from config.py

Known data hazards to resolve before trusting any result:
- Delisted names missing from free sources (the main survivorship risk).
- Renames/mergers breaking symbol continuity (e.g. HDFC -> HDFC Bank).
- Adjusted vs unadjusted prices mixed.
- Restated fundamentals overwriting originally reported values.

## STATUS (as built by fetch_data.py)
- Universe = TODAY's Nifty 500 (nifty500_current.csv), Yahoo adjusted closes. SURVIVORSHIP-BIASED: only 272 names have
  data on 2010-01-04; every delisted/dropped name (e.g. DHFL, Satyam) is absent. Treat all results as an UPPER BOUND.
- Benchmark = ^NSEI price index (no dividends). Nifty 50 TRI not available from Yahoo.
- No point-in-time fundamentals and no point-in-time membership exist yet.
- prices_tune.parquet / bench_tune.parquet: 2009-2018 (agents may read). *_SEALED.parquet: 2019+ (do not read).

## US set (fetch_us.py)
us_prices_tune/test_SEALED.parquet, us_extra_*: CURRENT S&P 500 members (data/raw/sp500_current.csv), Yahoo adjusted closes; ^GSPC and SPY
(dividend-adjusted TRI proxy). Survivor-biased like India (418 of 503 alive on 2010-01-04). US test (2019+) is sealed and unused.
