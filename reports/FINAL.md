# Final synthesis: trend + quality framework on Indian stocks

## Verdict
- Original rule (momentum rank, Nifty-50 regime filter, 15 names): FAILED the drawdown test in tuning (see FINAL_phase1_tune_only.md).
- Revised rule (frozen at 6bc9ac6, tested once on sealed 2019-2026): beats the Nifty clearly on return AND drawdown, beats random
  picks on return, but FAILS the "drawdown better than random-picks median" criterion (-25.3% vs -22.1%). 4 of 5 pass criteria hold.
- The QUALITY (EBITDA/growth/cash-flow) leg was never tested (no point-in-time data). All numbers are survivor-biased UPPER BOUNDS.
- Not proven; not ready for real money without the data fixes below.

## What changed between phase 1 and phase 2 (tuned on 2010-2018 only; 72 cells, plateau not spike: 34/72 beat Nifty drawdown)
Regime filter on the Nifty 500 index (not Nifty 50; it saw the 2018 mid/small-cap fall), momentum/volatility ranking (not raw momentum),
25 names (not 15), idle cash earns 6%. Rules in reports/FROZEN_RULES.md.

## Sealed test, 2019-01-01 to 2026-09-30, Rs 10,00,000 start (one shot; results/test/result.json)
| | Final value (Rs) | CAGR | Max drawdown | Worst year | Worst month |
|---|---|---|---|---|---|
| Frozen strategy | 98,09,090 | 34.3% | -25.3% (17 Jan 2022 to 12 May 2022; recovered 403 days after trough) | 2022: -0.7% | Jan 2025: -17.1% |
| Nifty BeES (TRI proxy, split artifact corrected) | ~22.7 lakh | 11.0% | -36.3% | 2026 YTD -12.5% | Mar 2020: -22.9% |
| Nifty 50 price index | 20,95,942 | 10.0% | -38.4% | | |
| Nifty 500 price index | 23,99,692 | 12.0% | -38.3% | | |
| Equal-weight hold of survivors | 62,71,504 | 26.8% | -40.9% | | |
| Random picks, same filters/regime (150) | n/a | median 19.3% | median -22.1% | | |
| Random picks, no stock filters, same regime (150) | n/a | median 15.5% | median -22.3% | | |

Pass criteria: CAGR > Nifty PASS; CAGR > random median PASS (beat 100% of 300 runs); MaxDD better than Nifty PASS (-25.3% vs -36 to -38%);
MaxDD better than random median FAIL (88% / 84% of random runs had a shallower drawdown); survives 2x costs PASS (50 bps: 31.8% / -25.9%).
Cost stress: 100 bps -> 27.0% / -27.1%; 150 bps -> 22.3% / -28.3%.
Robustness: without its top-3 names (TTML, GVT&D, CGPOWER) 30.6% / -24.9%; without 9 names with suspect data 33.7% / -25.3%.
Years: 2019 +1.7%, 2020 +40.9%, 2021 +134.8%, 2022 -0.7%, 2023 +79.3%, 2024 +52.8%, 2025 0.0%, 2026 YTD +7.2% (2021 and 2023 dominate).
Tune window (2010-2018): 25.8% / -19.7%, Rs 78,78,526; 2018: -10.1% vs Nifty +3-5%.

## Reading it honestly
- The drawdown protection comes mostly from the regime filter and cash, which the random baselines share. The momentum/vol ranking adds return
  (+15 pts CAGR over random, +24 pts over unfiltered random) but slightly MORE drawdown than random. That is why criterion 4 fails.
- The 34.3% is inflated. Survivors-only universe and today's Nifty 500 membership: the survivor hold gets 26.8% vs 12.0% for the actual index.
  Stocks that entered the index after 2019 because they rose are in the universe (look-ahead selection). Earlier audit haircut: 40-60%,
  i.e. realistic 14-20% before tax, then ~3-4 pts of short-term tax drag at this turnover. Closer to Nifty+ some, with a drawdown not clearly better than random.
- It is not a multi-bagger finder: 0 of 668 trades reached 5x (1 of 624 in tune); median holding is weeks. It is a momentum/regime strategy.
- Concentrated years: 2021 (+135%) and 2023 (+79%). Without such years returns are far lower.

## Honest worst case (Rs, per Rs 10,00,000 invested)
Observed: -19.7% (tune), -25.3% (test), worst month -17.1%. Because the data flatters, plan for -35% to -45%
(Rs 3,50,000-4,50,000 at a peak), plus one-name ruin of about Rs 40,000 (25 equal weights) and a 1-2 year recovery. Unfiltered Nifty did -38% in 2020.
The regime filter avoided the 2020 crash here, but it can whipsaw (2025 flat, Jan 2025 -17%).

## Still unproven
1. Quality gate (EBITDA-margin trend + growth + cash flow): untested; gate code and 32 leak tests exist, need point-in-time data.
2. Survivorship: delisted names and point-in-time Nifty 500 membership absent in both windows; true effect unknown.
3. Whether the ranking adds risk-adjusted value versus the regime filter alone (criterion 4 failed).
4. Liquidity/volume, circuit-limit fills, real STT/stamp/impact costs and taxes.
5. Data quality: Yahoo has unadjusted corporate actions; results were insensitive to the 9 flagged names but not audited for all 499.
6. Only ONE out-of-sample period; the design was shaped after seeing the 2018 fall. The test set is now used.

## Next steps
Supply PIT constituents, delisted prices, PIT fundamentals; test regime-only vs regime+ranking; add the quality gate; paper trade
with kill-switches (-25% warning, -35% stop, >30 months underwater) before real money.
