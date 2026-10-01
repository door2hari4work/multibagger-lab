# Pre-flight review of backtest.py (static read + synthetic smoke test; NO real data run)

Status: BLOCKED on data. Yahoo (query1/query2.finance.yahoo.com) and NSE (nsearchives.nseindia.com) are denied by the
environment network policy, and data/ is empty. No agent has run. Nothing here says anything about Indian markets.

## Runs
Synthetic random-walk prices: code executes end to end, no crashes. Proves plumbing only.

## Defects vs PROTOCOL.md (must fix before agents run)
1. Test-set leak: report() runs 2010 to 2026 in one pass (regime table includes 2019-2026). Not gated by holdout.py.
2. Delisting hides losses (demonstrated on synthetic data): px.ffill() keeps a dead name at its last price.
   Synthetic case: stock wiped out -> measured MaxDD -16.9%, WorstTrade -31.5%; truth MaxDD -35.5%, WorstTrade -100%.
   Delisted/suspended names need an explicit terminal price (final_price in delistings.csv, 0 if wiped out).
3. Universe is a static ticker list = survivorship bias; no point-in-time Nifty 500 membership.
4. Benchmark ^NSEI is a price index (excludes dividends); protocol says Nifty 50 TRI. Bias flatters the strategy.
5. Random baseline is 10 seeds drawn from the SAME trend/52w-high filters; protocol wants 1000 runs and an unfiltered
   random-pick variant. Current version cannot show the filters themselves add value.
6. Equity normalised to 1.0, no Rs 10,00,000 / whole-share / liquidity handling; no ADV or circuit-limit check.
7. "Multi-bagger" never measured (Over2x only); need >=5x capture rate and share of total P&L from top-3 winners.
8. `block` set is built but never used; `tot` unused. Harmless, but dead code.
9. Fundamentals gate (EBITDA/growth/cash flow) is not implemented; agent 4 needs PIT data + new code.
10. Cash earns 0% (conservative), cost model flat 25 bps (placeholder; no STT/stamp split, no slippage tiers).

## What looks right
Signals at close t executed at close t+1; stops likewise; momentum uses shift(skip) so no same-bar peek.

## Needed from user
Network access to a price source, OR uploaded files per data/README.md (esp. delisted names + PIT constituents).
