# Final synthesis (tune window 2010-2018 only; 2019-2026 test set NOT run, still sealed)

## Verdict: FAIL on the tune window. Not ready for live money. The test set was deliberately not spent.
The trend (momentum/52w-high/200d MA/30% trailing stop/Nifty regime filter) rule fails your own drawdown requirement
even on survivor-flattered data. The quality (EBITDA/growth/cash-flow) half could not be tested at all (no data).

## Rule set tested (nothing passed, so nothing frozen)
Monthly rebalance; hold up to 15 equal-weight names with price > 200d MA, 12-1m momentum > 0, within 25% of 52w high;
rank by momentum; 30% trailing stop; go to cash if Nifty < 200d MA; signals executed at next close; 25 bps per side.
No FROZEN_RULES.md was written because no variant meets the criteria.

## Results vs baselines (Rs 10,00,000 start, 2010-2018, survivors-only universe, price-index Nifty = UPPER BOUNDS)
| | Final value (Rs) | CAGR | Max DD | Worst year |
|---|---|---|---|---|
| Strategy | 71,78,036 | 24.5% | -34.4% | 2018: -22.9% |
| Nifty 50 price index | 20,76,096 | 8.5% | -27.9% | |
| Nifty approx TRI (+1.3%/yr assumed) | n/a | 9.9% | -26.8% | |
| Equal-weight hold of the 272 survivors | n/a | 22.9% | -31.1% | |
| Random picks, same filters (200 runs) | n/a | median 12.2% | 91% of runs shallower than -34.4% | |
| Random picks, no filters (200 runs) | n/a | median 7.4% | median -37.4% | |

Pass criteria: beats Nifty CAGR PASS (before bias haircut); beats random median CAGR PASS; drawdown better than Nifty FAIL;
drawdown better than random median FAIL (vs filtered random; only ties unfiltered). 2 of 4 fail even in-sample.

## What failed
- Drawdown: -34.4% (Rs 36,42,242 from a Rs 1,05,81,457 peak, Jan-Oct 2018), not recovered by end of 2018. The regime filter
  stayed invested while breadth fell 87% -> 13%. Best of 144 grid cells has MaxDD -21.2%; base case ranks 125th of 144.
- Most of the excess return is the universe: holding the survivors returns 22.9%. Over 2015-18 strategy 16.5% vs survivors 16.4%.
- Regime filter costs ~6-7 pts CAGR, stops ~1 pt; neither cut drawdown. 64% of stops filled below the stop; worst -47% trade.
- Walk-forward: 2010-14 CAGR 31% -> 16.5% in 2015-18. Top 3 names = 41% of P&L; excluding 2014 and 2017, 6.2% a year.
- Not a multibagger finder: 1 of 446 trades reached 5x; median hold 60 days.
- Costs/tax: 100 bps/side -> 18.0%; 20% short-term tax -> 20.6%, below the survivor hold (21.3%); both -> ~15%. Turnover 7.1x/yr.

## Biases (bias auditor)
Survivorship FAIL (only 54% of index slots have data in 2010; no delisted names). Timing look-ahead PASS. Overfitting FAIL
(walk-forward, concentration). Index-membership look-ahead UNTESTABLE (best 20% later joiners -> 18.7%; 33% -> 10.4%).
Volume liquidity UNTESTABLE. Auditor's haircut: 40-60% -> roughly 10-16% CAGR pre-tax, i.e. about Nifty with dividends.

## Honest worst case
Observed: -34.4% in the tune window on a flattered universe. Plan for -45% to -50% and 2-3 years underwater
(that range is judgement, ~1.5x observed, not a model): Rs 4,50,000-5,00,000 lost per Rs 10,00,000 invested at a peak,
plus ~Rs 67,000 per Rs 10 lakh if one equal-weight name goes to zero. Realistic live return after haircut and tax: ~Nifty-like at a worse drawdown.

## Still unproven
- The quality gate (EBITDA-margin trend + growth + cash flow): zero point-in-time data 2010-2018 (0% coverage). Gate code and
  32 leak-tests exist (analysis/fundamentals/pit_gate.py); thresholds are untuned placeholders. Data needed: reports/4_fundamentals_tester.md.
- Anything on 2019-2026 (sealed test files untouched).
- Delisted/dropped names and point-in-time Nifty 500 membership; true Nifty 50 TRI.
- Volume-based liquidity for Rs 10 lakh positions and circuit-lock days.
- 1000 random runs (200 used); rebalance frequency (hard-coded monthly).
- Whether quality screening would have avoided the 2018 mid/small-cap drawdown: plausible, unproven.

## Recommended next steps
1. Supply point-in-time constituents, delisted prices and PIT fundamentals; re-run the tune phase.
2. Only a variant that beats Nifty and random on drawdown in tune gets frozen and tested once on 2019-2026.
3. Kill-switch if ever run live (skeptic): -25% warning, -35% hard stop, >30 months underwater.
