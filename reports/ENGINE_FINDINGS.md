# Multi-bagger engine: what the tune-window evidence says (India + US, 2010-2018, survivors-only; 2019+ India test used, US test sealed)

## 1. Forensic: do trend signals find multi-baggers? (analysis/forensic/lift.py; 3y/5y forward outcomes, starts 2010-2015)
Base rates are survivor-inflated, so read LIFT only.
| Signal | India: 3x in 3y | India: loss >30% in 3y | US: 3x in 3y | US: loss >30% in 3y |
|---|---|---|---|---|
| All stocks (base) | 17.6% | 11.9% | 3.5% | 2.0% |
| Strategy trend filters only (>200d MA, mom>0, within 25% of high) | 16.3% (lift 0.93) | 10.1% | 2.6% (0.76) | 1.7% |
| Top decile 12-1 momentum | 30.3% (1.72x) | 8.7% | 7.0% (1.99x) | 3.2% (1.58x worse) |
| Top decile momentum/volatility | 26.8% (1.52x) | 7.0% | 4.0% (1.14x) | 2.1% |
| Low-volatility third + filters | 10.5% (0.59x) | 5.3% | 0.3% | 0.6% |
- The trend FILTERS protect against loss (India loss 11.9% -> 10.1%, and far lower in the lowest-vol group) but give NO multi-bagger lift.
- The SELECTION edge sits in the momentum RANK: strong and fairly consistent in India (2011-2014 start years), weak and unstable in US
  (lift below 1 in 2012, 2013, 2015) and the raw-momentum top decile in the US had 1.6x more big losses.
- Safe vs. winner trade-off: low volatility removes both losses and winners.

## 2. Decomposition: where do return and drawdown protection come from? (analysis/improve/decompose.py, tune only)
| India | CAGR | Max DD | | US | CAGR | Max DD |
|---|---|---|---|---|---|---|
| Regime + random 200 of all names | 11.3% | -28.6% | | | 12.1% | -20.1% |
| No regime + random 25 of all names | 12.2% | -39.1% | | | 14.4% | -22.7% |
| No regime + filters + random 25 | 18.0% | -27.1% | | | 13.9% | -20.5% |
| Regime + filters + random 25 | 15.0% | -23.6% | | | 11.4% | -20.0% |
| Regime + filters + momentum rank | 29.4% | -26.3% | | | 21.7% | -22.0% |
| Regime + filters + mom/vol rank (candidate) | 25.8% | -19.7% | | | 16.2% | -20.8% |
| No regime + filters + mom/vol rank | 29.5% | -24.3% | | | 18.7% | -28.4% |
(benchmarks: India Nifty TRI proxy 9.0% / -27.3%; US SPY 11.4% / -19.3%)
- Trend filters cut drawdown most (India random picks -39% -> -27%). The index regime filter cuts a few more points at a cost of about 3-4 pts of CAGR.
- Everything above index-like (roughly 11-15% with filters+regime on random picks) comes from the momentum RANK.
- Honest reading: the earlier test-window drawdown miss vs random (-25.3% vs -22.1%) is consistent with this: the rank adds return, not protection.

## 3. "Hold winners" engine (backtest.py keep_winners; 36 declared configs per market, tune only)
Positions held until trailing stop (30/40/50%) or a close below the 200d MA, new names only fill free slots (no rank-slip selling).
- India: median 23.8% CAGR, -24.7% DD; best drawdown cell 23.9% / -18.8% (N=40, mom/vol, stop 40-50%, exit on 200d break). 24 of 36 cells beat Nifty drawdown.
- US: median 16.5%, -21.2%; only 10 of 36 beat SPY drawdown. Best drawdown cell 14.0-14.8% / -17%.
- Versus the rebalanced candidate (India 25.8% / -19.7%; US 16.2% / -20.8%) holding winners does NOT improve risk-adjusted results. It changes trade
  shape: average win +45-55% (was +28%), trades >= 3x rise from about 3% to 11-17 per run, but trades >= 5x are still 0-1 in nine years.
- Exiting on a 200d-MA break beats not exiting in India (25.4% vs 22.4% CAGR); stop level (30-50%) barely matters.

## 4. Live screen, 2026-09-30/10-02 (information only, not backtested; results/live_quality_screen.csv, results/live_india_picks.csv)
- India: regime OFF (Nifty 500 22,072 < 200d MA 22,966), rule says cash. 165 stocks pass filters. Of the top 25 by mom/vol, 10 pass the quality
  gate (e.g. Sterlite Tech, MTAR, Sansera, Laurus Labs, Acutaas, MCX, Divi's, Navin Fluorine, BHEL, Granules); Cupid, HFCL, Aether, Anand Rathi fail on weak cash conversion.
- US: regime ON (S&P 500 7,723 > 200d MA 7,226). Of the top 25, 4 pass the gate (MU, DELL, STX, AMD); many top names fail on growth or margin (VLO, PSX, MPC, XOM).
- The US backtest says the gate does not improve results, so treat "fails gate" as risk information, not an exclusion rule.
- Yahoo gives only about 4 fiscal years, so this quality check can be used going forward but never backtested.

## What this means for a multi-bagger engine
1. Today's universes (Nifty 500, S&P 500) are large/mid caps. Over 9 years the rule produced 0-1 trades of 5x. It is a momentum strategy with a 3x occasional winner, not a multi-bagger finder.
2. The only component with demonstrated selection power is top-decile momentum (India strong, US weak). Trend filters and the regime filter provide protection, not selection.
3. The quality gate did not help in the US, the only market we could test it on.
4. Real multi-bagger odds live in small/micro caps, where survivorship, delisting and liquidity problems are far larger. Not testable without delisted data.
