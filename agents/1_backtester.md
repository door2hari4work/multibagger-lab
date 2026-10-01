# Agent 1 - Backtester
Run `backtest.py` (uploaded by user) on real data.
1. Regimes: split tune window into bull / bear / sideways / crash (e.g. 2011-13, 2014-17 bull, 2018 mid/small-cap drawdown,
   2010-11 and 2008-style stress if data allows). Report per-regime CAGR, MDD, hit rate.
2. Parameter grid: trend lookback, rebalance freq, N positions, stop rule, quality-gate thresholds. Report the FULL grid
   (heatmap/table), not the best cell. Flag whether the optimum is a plateau or a spike.
3. Cost stress: 1x, 2x, 3x costs plus illiquid-name slippage. Report break-even cost.
4. Baselines: Nifty TRI, 1000 random-pick runs (same N, dates, costs). Report percentile of the strategy.
Output: `reports/1_backtester.md`, `results/tune/grid.csv`. TUNE WINDOW ONLY.
