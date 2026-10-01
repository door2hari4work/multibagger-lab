# Agent 1 - Backtester report (tune window 2010-2018 only)

## READ THIS FIRST: every number below is an UPPER BOUND, not an estimate
- Universe = TODAY's Nifty 500 survivors (Yahoo adjusted closes). 272 names have prices on 2010-01-04 (361 by 2018-12-31); every name
  that was delisted, merged or dropped from the index between 2010 and 2018 is absent. No name in the data ever goes to zero
  (`apply_end_policy` had nothing to act on: 0 series end early). The universe is selected on having done well to 2026.
- Benchmark = ^NSEI **price** index (no dividends). "Approx TRI" = ^NSEI x 1.013^years (+1.3%/yr, my assumption, not data).
- No point-in-time fundamentals, no PIT membership. Price-only engine (trend + stops + regime); no fundamental gate was tested.
- Tune window only: `data_loader.load_tune()`; no 2019+ file was opened. Trading starts 2010-01-01 (`start="2010-01-01"`; 2009 is warm-up),
  equity via `data_loader.window()` from Rs 10,00,000.
- Costs are the flat 25 bps/side placeholder from config; no ADV/liquidity or slippage-tier logic exists in backtest.py (so "illiquid slippage" was not modelled separately; the cost sweep to 400 bps covers it as a blunt stress).
- Random runs: **200 seeds per mode, not the 1000 in config.RANDOM_BASELINE_RUNS**, because of the CPU budget (4 cores shared with 4 other agents,
  max 2 workers, ~5-6 s per backtest => 400 runs took 18 min). With 200 seeds, 0/200 is an upper 95% bound of about 1.5% on the tail probability; percentiles are good to about +/-3 points.

## Headline (base case: top_n=15, stop=30%, regime=ON, lookback=252, ma=200, 25 bps/side)
| Question | Answer |
|---|---|
| Strategy result | CAGR 24.5%, MaxDD -34.4%, Sharpe 1.29, Rs 10,00,000 -> **Rs 71,78,036**, worst peak-to-trough loss **Rs 36,42,242** |
| Beats Nifty on return? | Yes: Nifty price 8.5% (Rs 20,76,096), approx TRI 9.9% (Rs 23,31,670) |
| **Beats Nifty on max drawdown?** | **NO. -34.4% vs -27.9% (price) / -26.8% (approx TRI).** In rupees the strategy's worst fall (Rs 36.4 lakh) is about 9x Nifty's (Rs 3.9 lakh) because it holds 3.5x more money by then. 2018 alone: strategy -34.4% vs Nifty -14.6% |
| Beats random_all on return? | Yes: 200/200 seeds below it (random_all median 7.4%, p95 11.5%) |
| **Beats random_all on max drawdown?** | **Only vs the median.** random_all median MaxDD -37.4%; 50/200 seeds (25%) had a SHALLOWER drawdown than the strategy. So it is not clearly better on drawdown, and no seed beat it on return AND drawdown simultaneously (0/200), but that is because no seed beats it on return |
| Beats random (same filters) on return / drawdown? | Return yes (0/200 seeds above; median 12.2%). **Drawdown NO: 182/200 seeds (91%) had a shallower MaxDD than the strategy** (median -28.4%) |
| Beats equal-weight buy&hold of the survivors? | Barely on return (24.5% vs 22.9%, +1.6%/yr), **worse on drawdown (-34.4% vs -31.1%)**; break-even cost vs it is only 44 bps/side |
| Is the base case a good cell of the grid? | **No.** It ranks 125th of 144 on CAGR and 126th of 144 on MaxDD. The headline is not a cherry-pick: it is roughly the 13th percentile |
| Protocol pass criteria (tune-window analogue) | CAGR > Nifty: pass. CAGR > random median: pass. **MaxDD better than Nifty: FAIL. MaxDD better than random median: FAIL vs "random" (same filters), pass vs "random_all".** Not a pass overall |

Calibration: on survivorship-free data the real CAGR would be materially lower (unknown by how much); the return gap vs Nifty (+15 points/yr) is
far larger than any plausible fee/dividend adjustment and should be read mostly as survivorship + small/mid-cap beta, not as proven skill.
The part that is robust to survivorship in direction: the drawdown failure (survivors only make drawdowns look shallower than reality).

## 1. Commands
```
cd /home/user/multibagger-lab/analysis/backtester
python base_regimes.py                  # base case, regimes, baselines -> results/tune/base_curves.csv
python run_all.py grid                  # 144 cells  -> results/tune/grid.csv        (2 workers, ~7 min)
python run_all.py cost                  # 9 costs    -> results/tune/cost_stress.csv
python run_all.py random                # 2x200 seeds -> results/tune/random_baselines.csv  (~18 min)
python summarize.py                     # percentiles, break-even, plateau analysis
python diag_random_nodrag.py            # 20-seed diagnostic: random baselines without regime/stops -> results/tune/random_diag_20seeds.csv
```
backtest.py was not modified. `common.py` wraps `backtest.backtest(..., start="2010-01-01")` + `data_loader.window()`.

## 2. Full window 2010-01-04 to 2018-12-31 (Rs 10,00,000 start)
| Series | CAGR | MaxDD | MaxDD Rs | Sharpe | Final value |
|---|---|---|---|---|---|
| Strategy (base) | 24.5% | -34.4% | -Rs 36,42,242 | 1.29 | Rs 71,78,036 |
| Nifty 50 price (^NSEI) | 8.5% | -27.9% | -Rs 3,87,151 | 0.61 | Rs 20,76,096 |
| Nifty approx TRI (+1.3%/yr) | 9.9% | -26.8% | -Rs 3,95,629 | 0.70 | Rs 23,31,670 |
| EW buy&hold, the 272 names live on 2010-01-04 | 22.9% | -31.1% | -Rs 13,75,090 | 1.47 | Rs 63,65,569 |
| EW daily-rebalanced, all names with data (272 -> 361) | 19.8% | -32.9% | -Rs 15,17,099 | 1.21 | Rs 51,45,592 |

Trade stats (446 trades, ~50/yr): hit rate 54.9%, avg win +28.3%, avg loss -10.9%, worst trade -47.0%, trades >=2x: 3.1%, >=5x: 0.2% (1 trade).
So this is a trend-following P&L from many small wins, not a multibagger-capture engine. 26.4% of days have exactly zero return (all cash).

Note on the survivor bias in the strategy's own results: the 272-name equal-weight buy&hold of survivors earned 22.9%, i.e. ~13 points/yr above Nifty
with zero skill. Most of the "alpha" vs Nifty is already present in the universe itself.

## 3. Regimes (each segment rebased to Rs 10,00,000 at its start; strategy runs continuously through them)
Hit rate: per-trade hit rate by regime is not available (backtest.py trades carry no dates and I cannot modify it), so the table shows the share of months with a positive return (Months up). Whole-window trade hit rate is 54.9%.

| Regime | Strategy return (CAGR) | Strat MaxDD | End value | Months up | Nifty price return | Nifty MaxDD | EW b&h survivors return | EW MaxDD |
|---|---|---|---|---|---|---|---|---|
| 2010-11 (weak) | +38.7% (17.9%) | -23.2% | Rs 13,86,718 | 39% | -11.6% | -27.9% | +1.9% | -31.1% |
| 2012-13 (sideways) | +26.9% (12.7%) | -14.5% | Rs 12,68,835 | 48% | +32.3% | -14.6% | +70.6% | -17.3% |
| 2014-15 (bull) | +158.6% (61.0%) | -13.7% | Rs 25,86,485 | 74% | +27.7% | -16.0% | +134.6% | -11.2% |
| 2016 | **-5.7%** | **-23.5%** | Rs 9,43,176 | 45% | +5.1% | -11.7% | +11.2% | -14.9% |
| 2017 (bull) | +111.4% | -9.3% | Rs 21,13,844 | 91% | +28.7% | -4.1% | +50.4% | -5.8% |
| 2018 (mid/small drawdown) | **-23.3%** | **-34.4%** | Rs 7,67,270 | 27% | +4.0% | -14.6% | -8.3% | -19.4% |

Calendar years (strategy / Nifty price / approx TRI; strat MDD / Nifty MDD): 2010 +54.6 / +17.2 / +18.8 (-15.6 / -10.7); 2011 -10.3 / -24.6 / -23.6 (-15.0 / -26.2);
2012 +21.8 / +27.7 / +29.4 (-6.2 / -13.8); 2013 +4.2 / +6.8 / +8.1 (-14.5 / -14.6); 2014 +119.3 / +31.4 / +33.1 (-9.9 / -6.5); 2015 +18.7 / -4.1 / -2.8 (-13.7 / -16.0);
2016 -5.7 / +3.0 / +4.4 (-23.5 / -11.7); 2017 +115.5 / +28.6 / +30.3 (-9.3 / -4.1); 2018 -22.9 / +3.2 / +4.5 (-34.4 / -14.6).

Reading: the strategy lags or ties in the sideways years (2012-13: below Nifty AND below the survivors' buy&hold), loses money in 2016 and 2018 while Nifty is flat/up,
and the entire excess return comes from 2010, 2014 and 2017 (three years, +55%, +119%, +115%). The max drawdown of the whole run (-34.4%) is the 2018 mid/small-cap
break: the regime filter keys off Nifty 50 (above its 200-day average through most of 2018), so it did not de-risk. Two of the nine years (2016, 2018) are clear failures.
(Regime-table returns rebase at the first trading day of the segment; calendar-year figures use the prior year-end close, so they differ slightly for 2012-13.)

## 4. Parameter grid (144 cells, FULL table in results/tune/grid.csv)
Grid: top_n {10,15,25} x stop {20%,30%,40%,none} x regime {on,off} x lookback {126,189,252} x ma {100,200}. In grid.csv `stop=10.0` means NO stop (a stop >= 1 can never trigger).
Columns: CAGR, MaxDD, Sharpe, Trades, HitRate, Over2x, Over5x, WorstTrade, AvgWin, AvgLoss, FinalRs, MaxDD_Rs. Cost 25 bps, start 2010-01-01.
Not varied: rebalance frequency (monthly is hard-coded via `last_of_month` in backtest.py; no argument exists and I was told not to edit it), `skip` (left at 21), quality-gate thresholds (no fundamentals).

Distribution over the grid: CAGR min 19.6%, p25 25.9%, median 29.4%, p75 33.0%, max 39.5%. MaxDD best -21.2%, median -28.7%, worst -39.4%.
All 144 cells beat Nifty price CAGR (8.5%); 93% beat survivors' EW buy&hold (22.9%). MaxDD shallower than Nifty (-27.9%): 60/144 cells (regime ON: 38/72; regime OFF: 22/72). No cell has MaxDD better than -21.2%.
CAGR and MaxDD are negatively correlated across cells (-0.38): higher CAGR cells tend to have deeper drawdowns (a risk-return trade, not free lunch).

Mean over the other parameters (CAGR / MaxDD):
| top_n | regime OFF | regime ON | | stop | regime OFF | regime ON |
|---|---|---|---|---|---|---|
| 10 | 34.5% / -34.7% | 27.7% / -29.4% | | 20% | 29.2% / -33.6% | 23.9% / -28.8% |
| 15 | 33.1% / -30.8% | 25.8% / -26.5% | | 30% | 32.8% / -30.9% | 26.0% / -27.8% |
| 25 | 31.1% / -27.7% | 24.6% / -25.9% | | 40% | 34.7% / -30.0% | 27.1% / -26.2% |
| | | | | none | 34.8% / -29.8% | 27.0% / -26.2% |

| lookback | regime OFF | regime ON | | ma | regime OFF | regime ON |
|---|---|---|---|---|---|---|
| 126 | 34.1% / -29.0% | 26.6% / -25.2% | | 100 | 32.4% / -31.3% | 24.6% / -24.6% |
| 189 | 31.7% / -31.2% | 25.2% / -27.2% | | 200 | 33.3% / -30.9% | 27.4% / -30.0% |
| 252 | 32.8% / -33.0% | 26.3% / -29.3% | | | | |

Findings from the grid:
- **The regime filter costs ~7 points of CAGR/yr** (mean 26.0% ON vs 32.9% OFF) and buys only ~4 points of MaxDD (-27.3% vs -31.1%). The base case has it ON.
- **Stops do not help.** Tight stops (20%) are the worst on both CAGR and MaxDD; 40% and "no stop" are indistinguishable (mean 30.9% each) and slightly better than 30%. Whipsaw, not protection.
- Concentration: top_n=10 gives most CAGR and deepest drawdown; top_n=25 the reverse; Sharpe rises slightly with N (1.38 / 1.43 / 1.49).
- Lookback matters little (126 slightly best on both). ma=100 vs 200 is mixed.
- **Plateau vs spike: it is a broad plateau, not a spike, on CAGR.** 93% of cells beat survivors' buy&hold; the grid CAGR std is only 4.5 points; the best cell (top_n=10, no stop, regime OFF, 252, 200; 39.5%, MaxDD -36.2%, Rs 1,98,94,808)
  exceeds the average of its one-step neighbours by 4.4 points (about 1 std), the top 14 cells by a median 2.9 points. A mild optimum, no isolated lucky cell. Direction is consistent: higher N-concentration, no/loose stop, regime OFF = more return AND more drawdown.
- **But the plateau is on the wrong dimension for the goal:** the MaxDD surface has no cell better than -21.2% and the median is worse than Nifty. Nothing in the grid reaches "large losses avoided" except at the cost of lower return, and all of it rides on survivorship.
- The base case (15, 30%, ON, 252, 200) is NOT the optimum: rank 125/144 on CAGR and 126/144 on MaxDD; its one-step neighbours average 27.0%. The base is a poor choice among grid cells; I did not pick parameters from the grid (tuning on this window would be fitting to survivors anyway).
- Best-drawdown cells (-21.2%): top_n=25, regime ON, ma=100, lookback 126/252, stop 40%/none, with CAGR 24.5-26.1%. That is the only corner that beats Nifty on drawdown by a margin (-21.2% vs -27.9%), still on survivor data.

## 5. Cost stress (base params; cost per side in bps; results/tune/cost_stress.csv)
| cost bps/side | CAGR | MaxDD | Sharpe | Final value |
|---|---|---|---|---|
| 0 | 26.8% | -33.3% | 1.38 | Rs 84,20,952 |
| 25 (base) | 24.5% | -34.4% | 1.29 | Rs 71,78,036 |
| 50 | 22.3% | -35.6% | 1.19 | Rs 61,16,704 |
| 75 | 20.2% | -36.7% | 1.10 | Rs 52,10,702 |
| 100 | 18.0% | -37.9% | 1.00 | Rs 44,37,530 |
| 150 | 13.9% | -40.6% | 0.80 | Rs 32,15,350 |
| 200 (extra) | 9.9% | -43.3% | 0.60 | Rs 23,26,878 |
| 300 (extra) | 2.2% | -48.3% | 0.21 | Rs 12,14,008 |
| 400 (extra) | -5.0% | -56.0% | -0.16 | Rs 6,30,155 |

Each +25 bps/side costs ~2.2 points of CAGR (about 50 trades/yr plus monthly rotation). Break-even cost (linear interpolation of CAGR vs cost, rivals fixed at their 25 bps results):
| vs | their CAGR | break-even bps/side |
|---|---|---|
| Nifty price | 8.5% | ~218 |
| Nifty approx TRI | 9.9% | ~200 |
| Random picks, same filters (median) | 12.2% | ~171 |
| random_all (median) | 7.4% | ~232 |
| EW daily-rebalanced universe | 19.8% | ~79 |
| EW buy&hold of survivors | 22.9% | ~44 |
It survives 2x (50 bps) and 3x (75 bps) cost stress against Nifty and random with large margin; vs buying-and-holding the survivors it stops adding value at ~44 bps/side, which
is realistic for small/mid-caps (impact + STT + stamp). MaxDD worsens with cost (-33.3% -> -37.9% at 100 bps). Rivals' costs were not re-stressed (random baselines also pay costs and would fall too, which would push their break-even higher, not lower).

## 6. Baselines
Benchmark and EW rows are in section 2. Random picks (base params top_n=15, stop=30%, regime ON, 25 bps, seeds 0-199, **200 not 1000**):
| Mode | CAGR mean / median | CAGR p5 - p95 | MaxDD median | MaxDD worst-5% - best-5% | Final value (median) | Sharpe (median) |
|---|---|---|---|---|---|---|
| random (same trend/52w-high filters) | 12.3% / 12.2% | 8.1% - 16.4% | -28.4% | -36.0% - -22.5% | Rs 28,05,162 | 0.88 |
| random_all (no filters) | 7.4% / 7.4% | 3.6% - 11.5% | -37.4% | -47.3% - -31.0% | Rs 18,98,319 | 0.55 |
| Strategy | 24.5% | | -34.4% | | Rs 71,78,036 | 1.29 |

Strategy percentile: above 100% of seeds on CAGR in both modes (0/200 seeds >= 24.5%; best random seed is far below). On MaxDD, 91% of "random" seeds and 25% of random_all seeds were shallower than the strategy.
17/200 "random" and 141/200 random_all seeds do not even beat Nifty price (8.5%).

Diagnostic (20 seeds, results/tune/random_diag_20seeds.csv) - the random baselines carry the regime filter, which costs ~6 points/yr, so they are handicapped:
| Random median CAGR / MaxDD | regime ON (200 seeds) | regime OFF, no stop (20) | regime OFF, 30% stop (20) |
|---|---|---|---|
| random (filters) | 12.2% / -28.4% | 18.8% / -27.7% | 18.4% / -27.7% |
| random_all | 7.4% / -37.4% | 11.5% / -37.7% | 11.6% / -37.9% |
Matched comparison: strategy with regime OFF (15, 30%, 252, 200) = 30.5% CAGR, MaxDD -33.9%: still ahead of random (18.4%) by ~12 points and random_all (11.6%) by ~19 points on return, but still has a deeper drawdown than "random" (-27.7%) and similar to random_all (-37.9%).
Interpretation: (a) the trend/52w-high filters add ~7 points/yr over unfiltered picks; (b) momentum ranking adds another ~12 points over random picks among filtered names; (c) NONE of this reduces drawdown versus random picks that
pass the same filters; (d) the survivorship bias is not removed by any baseline since every baseline draws from the same survivor list, so "beats random" shows ranking skill relative to survivors, not that the absolute level is real.
The dominant caveat stays: beating random among survivors does not mean beating the market among all names that existed in 2010.

## 7. Failures and caveats, plainly
1. Max drawdown is worse than Nifty (-34.4% vs -27.9%) in the base case, worse in 2016 and 2018 and worse than 91% of same-filter random runs. The pass criterion on drawdown is FAILED on the tune window, even with survivor-flattered data.
2. 2012-13 (sideways): strategy +26.9% vs Nifty +32.3% vs survivors' buy&hold +70.6%. 2016: -5.7% vs Nifty +5.1%. 2018: -23.3% vs Nifty +4.0%.
3. The regime filter (Nifty 50 above its 200-day) did not protect in 2018 because the damage was in mid/small caps; it also costs ~7 points/yr elsewhere.
4. Edge over the survivors' own buy&hold is small (+1.6%/yr) and vanishes at ~44 bps/side.
5. Excess return is concentrated in 2010, 2014, 2017; only 1 of 446 trades was a 5x.
6. Rebalance frequency and quality-gate thresholds were not testable (hard-coded monthly; no fundamentals). Illiquid-name slippage not modelled (no ADV data); cost sweep to 400 bps is a blunt proxy.
7. Random baselines are 200 seeds, not 1000. The grid was run only on the strategy (random baselines only at base parameters).
8. Equity is a fractional-weight index, not whole shares; Rs values scale linearly from Rs 10,00,000 and ignore circuit limits and ADV.
