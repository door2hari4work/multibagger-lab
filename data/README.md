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
