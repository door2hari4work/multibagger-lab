# Agent 2 - Bias audit (adversarial). Tune window only.

## Data caveat (read first)
- Data: `data_loader.load_tune()` only (Yahoo adjusted closes, 2009-01 to 2018-12-31, 499 columns, 361 with any tune data).
  Universe = TODAY's Nifty 500 survivors. Benchmark = `^NSEI` PRICE index. Trading starts 2010-01-01. No SEALED file, no post-2018 data was read.
- Everything below is a stress test of a survivor-only, price-only backtest. Headline under audit (backtest.backtest, top_n 15, stop 30%, 25 bps, regime on):
  **CAGR 24.5%, MaxDD -34.4%, Sharpe 1.29, 446 trades.** Nifty price index same window: CAGR 8.5%, MaxDD -27.9%.
- Scripts: `analysis/bias/NN_*.py` (run from that directory, 1 process). Raw outputs: `analysis/bias/out_*.txt|csv`.
  `analysis/bias/indep.py` is an independent re-implementation of the strategy (Rs-based, numpy), used for the fast sweeps.
  It reproduces backtest.py to a max relative equity difference of 7e-5 (CAGR 24.520% vs 24.519%, 446 vs 446 trades), and a random-kill case was cross-checked against backtest.backtest (21.529% vs 21.529%).
- Not modified: backtest.py, config.py. Nothing committed.

## Verdict table
| # | Bias | Verdict | One-line evidence |
|---|------|---------|-------------------|
| a1 | Survivorship: dead names missing | **FAIL** (structural) | 0 of 499 series end before 2018-12-31; only 272 of 500 slots have data in Jan-2010 (54%). `end_policy` zero vs last is byte-identical, i.e. the delisting fix is inert on this data. |
| a1q | Cost of missing wipe-outs (synthetic) | **FAIL (modest)** | Injecting 1-3%/yr wipe-outs costs 0.8-3.0 CAGR pts (same kill set, zero vs last); held-name hazard 1-5%/yr costs 0.4-3.7 pts. |
| a2 | Index-membership look-ahead (today's members) | **UNTESTABLE** (FAIL by construction) | No PIT membership. Bound: if the best 20% of names were late joiners, CAGR 18.7%; best 33% -> 10.4%. |
| a3 | Post-2010 IPOs only enter once listed | **PASS (mild)** | 95 names listed after Mar-2009; 14.8% of trades but 6.0% of P&L; dropping them RAISES CAGR to 29.4%. |
| b1 | Signal-close to fill timing (look-ahead) | **PASS** | Shift +1/+2/+5 bars: CAGR 24.9/23.8/25.2% (no collapse). Same-bar fill (cheat, -1): 26.3%. Independent re-implementation matches; 4 trades re-derived by hand. |
| b2 | 52w-high / MA include current bar | **PASS** | Computed at close t, filled at close t+1 (checked by shifting and by hand). |
| b3 | Adjusted-price leakage | **UNTESTABLE (minor)** | Needs unadjusted prices. Splits are ratio-invariant for the signals. Dividend adjustment tilts old prices ~1-2%/yr, too small to reorder 12m-momentum ranks. Dividends ARE in strategy returns but NOT in the ^NSEI benchmark (see "benchmark" below). |
| b4 | Data glitches (stale / phantom prices) | **FAIL (small)** | Stale-forward-filled series and unadjusted corporate-action jumps found in 17 names. Cleaned re-run: 24.1% vs 24.5%. |
| c1 | Parameter-search haircut (deflated Sharpe) | **PASS (not binding)** | Sharpe 1.29 vs cross-trial sd 0.10; DSR prob >= 0.997 even at N=1000 trials. Multiple testing of parameters is not the problem. |
| c2 | Walk-forward 2010-14 -> 2015-18 | **FAIL** | Best IS config: 42.9% IS -> 17.6% OOS (rank 26/35); IS-vs-OOS Sharpe rank correlation -0.52. Headline config: 31.1% (2010-14) -> 16.5% (2015-18). |
| c3 | Drop top-3 winners | **FAIL** | Top-3 names (HEG, Graphite India, PCBL) = 41% of total P&L; dropping them: CAGR 21.3%, MaxDD -37.1%. Dropping 3 random traded names: 25.1% +/- 0.65%. |
| c4 | Placebo / random baselines | **MIXED** | Beats 1000 random-same-filter draws (median 12.3%) and 1000 unfiltered (median 7.3%) on CAGR. But only the 89th percentile of a permuted-month placebo (median 18.9%). |
| c5 | Concentration in time | **FAIL** | Ex-2014 and ex-2017, geometric mean falls to 6.2%/yr. 2017 is the HEG/Graphite electrode boom. |
| d1 | ADV / volume capacity of Rs 66,000 per position | **UNTESTABLE** | No volume loaded. Conceptually small; see below. |
| d2 | Whole shares, circuit locks, zero-return proxy | **PASS** (proxies only) | Whole-share CAGR 24.52% = fractional. Circuit-lock stress (4.8/9.5/19%) -> 24.6/25.4/24.5%. Only 1.6% of trades in zero-return-heavy names. |
| d3 | Cost realism | **FAIL (sensitive)** | Each +25 bps/side costs ~2.2 CAGR pts: 50 bps 22.3%, 75 bps 20.2%, 100 bps 18.0%, 150 bps 13.9%. |
| e | Protocol criteria even in-sample | **FAIL 2 of 4** | MaxDD -34.4% is WORSE than ^NSEI (-27.9%) and than the random-same-filter median (-28.2%). |

## (a) Survivorship
**Coverage (`03_survivorship.py`).** Names with a price at each year-start vs the 500 index slots (signal-eligible = 252 clean bars):

| year-start | with price | signal-eligible | % of 500 slots |
|---|---|---|---|
| 2010-01-04 | 272 | 266 | 54.4 |
| 2011-01-03 | 288 | 272 | 57.6 |
| 2012-01-02 | 296 | 288 | 59.2 |
| 2013-01-01 | 303 | 296 | 60.6 |
| 2014-01-01 | 304 | 302 | 60.8 |
| 2015-01-01 | 306 | 304 | 61.2 |
| 2016-01-01 | 315 | 306 | 63.0 |
| 2017-01-02 | 329 | 315 | 65.8 |
| 2018-01-01 | 346 | 329 | 69.2 |

The missing 154-228 slots per date are IPOs not yet listed plus every name that was dropped, delisted or wiped out and is not in today's list. Zero names end early. The coverage trend (54% -> 69%) also means the look-ahead is largest in the early years, consistent with the edge decaying in c2.

**end_policy zero vs last:** identical (CAGR 24.519%, MaxDD -34.42% both) because no series ends before the sample. The pre-flight "delisting hides losses" fix therefore cannot act here; the bias is that dead names are not in the file at all.

**Synthetic wipe-outs (assumptions stated).** Rates are assumptions, not measured: my recollection of Indian wipe-outs/near-wipe-outs 2010-18 (Unitech, Jaiprakash Assoc., Lanco, Educomp, Gitanjali, Videocon, Reliance Communications/Capital, DHFL, Jet, Amtek, IL&FS group, Era Infra, IVRCL, Punj Lloyd, ...) is roughly 30-50 names against ~500 slots over 9 years, i.e. about 1%/yr; I bracket 1/2/3%/yr of listed names (about 25/50/73 names killed over 2010-18). Death date uniform within each year, then `backtest.apply_end_policy(policy="zero")` collapses the price to 1e-4 the next day (gap = worst case for a stop). "decay" glides the price to 15% over the prior 120 bars first. The control re-runs the same kill set with policy "last" so that the pure wipe-out loss is separated from the incidental removal of a random winner's later path. 30 seeds each (`out_surv_inject.csv`):

| rate/yr | variant | CAGR (zero) | MaxDD | wipe cost = zero - last | vs base 24.52% |
|---|---|---|---|---|---|
| 1% | gap | 24.5% | -33.7% | -0.8 pt | +0.0 |
| 2% | gap | 24.2% | -33.4% | -1.7 pt | -0.3 |
| 3% | gap | 22.8% | -34.4% | -3.0 pt | -1.7 |
| 1-3% | decay | 25.3-25.6% | -32 to -33% | 0.0 (stop exits before death) | +0.8 to +1.1 |

(The positive "vs base" in the removal-only control is sampling noise in which winners got randomly removed; sd across seeds is 1.1-2.0 pts, so use the wipe-cost column.) Alternative hazard model (`out_surv_hazard.csv`, 15 seeds): a held position is wiped by a gap to ~0 with annual probability h: h=1% -> 24.1% (-0.4), 2% -> 23.5% (-1.0), 3% -> 22.2% (-2.3), 5% -> 20.8% (-3.7), MaxDD -34.4% to -36.1%. Because the strategy is invested only about 3 of every 10 position-years (regime filter, cash), direct wipe-out risk is a modest haircut: **about 1-2 pts central, 3-4 pts stressed.** MaxDD barely moves because the 30% stop usually exits first except on gaps.

**Index-membership look-ahead (UNTESTABLE).** Today's membership is knowable only after the 2010-18 outcomes. Names that rose into the index are over-represented, and the strategy buys exactly the names that rose. No PIT constituents or market cap exist, so I can only bound it (`09_lateentrant.py`): delete the best X% of names by 2010-18 return as if they were not yet members (an extreme, outcome-selected bound):

| best X% removed | n names | strategy CAGR | strategy MaxDD | EW buy&hold CAGR (same names) |
|---|---|---|---|---|
| 0 | 0 | 24.5% | -34.4% | 20.0% |
| 5% | 13 | 23.6% | -35.5% | 18.3% |
| 10% | 27 | 23.2% | -35.5% | 17.0% |
| 20% | 54 | 18.7% | -36.9% | 15.0% |
| 33% | 89 | 10.4% | -38.2% | 12.7% |

Also telling: the equal-weight buy&hold of the survivor universe alone returns **20.0% CAGR (MaxDD -32.9%)** over the same window (cleaned data: 19.6%), vs the Nifty price index 8.5%. Roughly 11.5 of the 16 headline points over the index come from simply owning today's survivors, not from the rule. In 2015-18 the rule equals EW survivors (16.5% vs 16.4%) with a worse MaxDD (-34.4% vs -24.8%).

**IPO-after-2010 names (a3).** 95 of 361 names listed after Mar-2009. Restricting to names that already existed (266 names): CAGR 29.4%, MaxDD -33.0%; trades in late-listed names are 14.8% of trades but only 6.0% of P&L. Not the main look-ahead channel.

## (b) Look-ahead
1. **Timing shifts** (`02_lookahead.py`, `indep.sim(k=...)`; k bars of extra delay between signal close and fill close, k=0 is the base design):

| k | meaning | CAGR | MaxDD | Sharpe |
|---|---|---|---|---|
| -1 | fill at SAME close as signal (cheat) | 26.3% | -37.2% | 1.36 |
| 0 | base (signal close t, fill close t+1) | 24.5% | -34.4% | 1.29 |
| 1 | one bar later | 24.9% | -32.4% | 1.30 |
| 2 | two bars later | 23.8% | -33.9% | 1.25 |
| 5 | five bars later | 25.2% | -30.6% | 1.30 |

   Result does not depend on a 1-day edge; the same-bar cheat would add only 1.7 pts, so the base is not secretly benefiting from it. The signal is slow (monthly, 12m momentum).
2. **Independent re-derivation of 4 trades** (ECLERX Feb-2010, NATCOPHARM Jan-2011, POLYMED Mar-2013, RKFORGE Mar-2015), from raw un-ffilled prices with fresh code: signal bar is the last trading day of its month, fill bar is the next bar, the recorded entry price equals the raw close of the fill bar, all three conditions (close > 200d MA, 12-1m momentum > 0, close >= 75% of the 252-bar high) hold at the signal bar, rank is 3-15 of 118-238 eligible, regime filter on. Output in `out_02.txt`.
3. **52w-high includes the current bar**: by construction (close_t <= max over window incl. t). It is a signal on the close of t that is only acted on at t+1, so no leak. PASS.
4. **Sensitivity to deliberate future info** (`06_placebo.py`, candidate list taken from the month-end m months later): +1 month -> CAGR 50.0%, +2 -> 116%, +3 -> 122%. Any hidden look-ahead of even a month would produce a result far above 24.5%, so the base is well clear of that.
5. **Stale-signal check**: using the list from 1/2/3 months earlier: 22.7/18.5/21.8%; 6/12 months earlier: 12.4/11.3% (MaxDD about -41%). The edge decays within about 3-6 months, as expected of momentum.
6. **Adjusted prices**: UNTESTABLE without unadjusted closes (see table). Separate but real: Yahoo's early history is corrupted for some names (b4).
7. **Fundamentals before filed_date**: not applicable, no fundamentals in this engine (price only).
8. **Benchmark mismatch (FAIL, flatters)**: `^NSEI` is a price index; strategy returns are total-return adjusted closes. Assuming ~1.3%/yr dividend yield (an assumption, not measured), the fair benchmark CAGR is about 9.8%, not 8.5%.

**b4 data glitches** (`05_robust.py`): Yahoo series with long exactly-flat runs (WHIRLPOOL, NESTLEIND, ABBOTINDIA flat for ~1 year to 2010-01-07 then jump +570%/-76%/+188% on 2010-01-08; FSL flat 527 bars; J&KBANK flat ~600 bars; GVT&D, TECHNOE, MINDACORP, KIRLOSENG, ...). 4 of 446 trades overlap a stale run or a >40% one-day move, but they carry 5.3% of P&L (AVANTIFEED +313%, KIRLOSENG +127%). Masking all names before the end of any stale run >= 20 bars or before a one-day drop worse than -45%: CAGR 24.1% (-0.4 pt), MaxDD unchanged. Small but it is data the strategy ranks on.

## (c) Overfitting
- **Configs tried** (`04_overfit.py`, `results/tune/grid.csv`): backtest.py's own report grid = 18 + 3 cost + 10 random; agent 1 grid.csv = 144 rows (+9 cost); my sensitivity grid = 35 distinct configs (18 + 17 signal variants over lookback 126/189/252, skip 0/21, MA 100/150/200). Across the 35: CAGR 22.5-39.0%, Sharpe 1.25-1.64, every config beats the Nifty price CAGR. Sharpe sd is 0.10; parameters are not a knife-edge.
- **Deflated Sharpe** (Bailey & Lopez de Prado, skew -0.70, kurtosis 12.0, T=2222 daily obs, cross-trial sd of annual Sharpe 0.099): expected max Sharpe under the null SR0 = 0.18 / 0.25 / 0.32 for N = 18 / 100 / 1000; DSR probability 0.997+ in every case. This passes, but only means the Sharpe is not a parameter-picking artefact within this single price dataset. All trials are near-copies of one idea on one survivor-biased sample, so it says nothing about the data problem.
- **Walk-forward (2010-14 -> 2015-18, diagnostic only):** picking the best 2010-14 Sharpe over the 35 configs gives IS 42.9% / Sharpe 2.27, OOS 17.6% / Sharpe 0.89, OOS MaxDD -33.6%, OOS rank 26 of 35 (OOS median across configs 20.2%). Spearman correlation IS vs OOS Sharpe -0.52 (best IS configs are worst OOS). Reverse direction (tune 2015-18 -> test 2010-14): picked config ranks 34 of 36. Headline config by sub-period vs EW survivors vs ^NSEI price:

| window | strategy CAGR / MaxDD | EW survivors CAGR / MaxDD | ^NSEI price CAGR / MaxDD |
|---|---|---|---|
| 2010-14 | 31.1% / -23.2% | 22.8% / -32.9% | 9.6% / -27.9% |
| 2015-18 | 16.5% / -34.4% | 16.4% / -24.8% | 6.7% / -22.5% |

- **Year concentration:** annual returns 2010 +54.6%, 2011 -10.3%, 2012 +21.8%, 2013 +4.2%, 2014 +119.3%, 2015 +18.7%, 2016 -5.7%, 2017 +115.5%, 2018 -22.9%. Geometric mean excluding 2014: 16.0%; excluding 2017: 16.2%; excluding both: 6.2%.
- **Drop top winners** (re-selected, universe re-ranked): top P&L names HEGAM (HEG) 22.2% of total P&L from 2 trades, GRAPHITE 12.0% (2 trades), PCBL 6.8%, JBMA 6.7% (one trade, +455%), ... Top-3 = 41%, top-5 = 54%, top-10 = 77% of P&L (176 names traded). Dropping top 1 / 3 / 5 / 10: CAGR 22.6 / 21.3 / 19.3 / 17.4%, MaxDD -37.6 / -37.1 / -38.0 / -36.4%. Dropping 3 random traded names: 25.1% +/- 0.65% (min 22.3%). Even after dropping the top 10 the CAGR (17.4%) stays well above the Nifty price index (8.5%), but falls below the full-universe EW buy&hold (20.0%). The HEG/Graphite pair is one 2017-18 theme.
- **Placebos** (`06_placebo.py`): (i) random picks among filtered names, 1000 runs: CAGR median 12.3% (p5 8.4%, p95 16.3%), MaxDD median -28.2%; base CAGR is above all 1000, base MaxDD is better than only 4.7% of them. (ii) Unfiltered random_all, 1000 runs: CAGR median 7.3%, MaxDD median -37.9%; base MaxDD is better than 75.9% of them. (iii) Permuted-month placebo (the month-end candidate lists shuffled across months, regime and stops on, 1000 runs): CAGR median 18.9% (p5 11.8%, p95 26.9%); base sits at the 88.8th percentile, so **month-specific ranking explains only about 5-6 pts; most of the return comes from buying trending survivors at all.** The permuted lists include future and past lists, so this placebo is generous, but the point stands that the base is not separable from it at 95%.
- Hit rate 55%; median trade +1.4%, mean +10.6%; top decile of trades carries 126% of P&L; only 1 trade in 446 reached 5x (the "multi-bagger" capture is anecdotal).

## (d) Liquidity (Rs 10,00,000, about Rs 66,000 per position at the start)
- **ADV / volume: UNTESTABLE** (no volume data; config.MIN_ADV_INR is not enforced by backtest.py). Conceptual: Rs 66,000 is 0.1-1% of the 20-day ADV of a typical name at the Rs 5-70 lakh/day level, so entry size is not the problem at day one. Sim NAV reaches about Rs 71.8 lakh by end-2018 (Rs 4.8 lakh per slot, 15 slots), still small against an ADV floor of Rs 1 crore but the Rs 5-20 lakh/day small caps of 2010-14 become capacity-limited well before that. Impact for illiquid names is the 25 bps cost line, which is optimistic (below).
- **Whole shares** (`07_liquidity.py`): rounding to whole shares at Rs 10 lakh start gives CAGR 24.517% vs 24.520% fractional. Only 0.2% of entries have one share > 10% of the position. Caveat: Yahoo prices are adjusted to today's splits/dividends, so as-traded price levels differ; the true minimum position is Rs 66,667 (max adjusted price held Rs 30,295), so very high-priced names (MRF, Page, Bosch) are the only practical issue.
- **Circuit-lock proxies:** treating any entry-day close-to-close move >= 4.8% / 9.5% / 19% as a locked circuit (buy skipped) and any exit-day move <= -4.8% / ... as a lower-circuit lock (sale retried next bar): CAGR 24.6 / 25.4 / 24.5%; 46 / 5 / 1 buys blocked and 18 / 3 / 0 sells delayed. No damage on this data. Caveat: a locked sell on a wipe-out name is the real danger (a1q gap scenario), which this proxy cannot see.
- **Zero-return-day illiquidity proxy** (share of unchanged closes in the 60 bars before entry): only 1.6% of trades have >= 10% zero-return days (1.7% of P&L); excluding the 5 flagged names changes CAGR to 25.4%. 8.1% of trades (19.9% of P&L) are in names with adjusted price < Rs 20, where tick size and spread matter more.
- **Cost stress (FAIL-sensitive)**: 25 bps/side is a placeholder. With STT (0.1% each side on delivery), brokerage, stamp duty and impact for small/mid caps, 50-75 bps per side is more realistic: CAGR 22.3% / 20.2%; at 100 bps 18.0% (MaxDD -37.9%); at 150 bps 13.9%; 200 bps 9.9%. Capital-gains tax (not modelled; most trades are short-term) is a further drag.
- **Stop fills:** the 33 stop exits have median trade return -18.8%, worst -47.0%, and 9.1% worse than -35% (fills at the next close, not at the stop level); gaps through the stop are real in small caps.

## Bottom line: how much to haircut the headline
Headline: **CAGR 24.5%, MaxDD -34.4%, Sharpe 1.29** (Nifty price 8.5%, about 9.8% with assumed dividends).

Quantified deductions (CAGR points, not strictly additive; some are scenarios, not measurements):

| item | pts | basis |
|---|---|---|
| Missing wipe-outs (1-2%/yr central; stress 3-5%) | -1 to -2 (stress -3 to -4) | synthetic, assumed rates |
| Realistic costs (50-75 bps per side instead of 25) | -2 to -4 | cost sweep |
| Data glitches | -0.4 | cleaned rerun |
| Winner luck / single-theme concentration | -3 (drop top-3) | drop-top-N |
| Membership look-ahead (not measurable) | -2 to -6 (bound up to -14) | outcome-selection bound |
| Taxes | not modelled | |

That sums to about -8 to -15 pts, so **plan on roughly 10-16% CAGR before tax, a haircut of about 40-60% of the headline**, versus a fair Nifty benchmark of about 9.8%. On the evidence of the 2015-18 window (strategy = EW survivors at 16.5%, before the extra costs and wipe-outs) the expected edge over simply holding the same universe is roughly zero. Treat the 24.5% as an upper bound and the 2015-18 figure (16.5%, Sharpe 0.84) as the more honest mid-point before the deductions above.

Drawdown: do not accept -34.4% as the number. It is already worse than the index (-27.9%) and than the random-same-filter median (-28.2%), the window excludes 2008 and 2020, the regime filter was never tested in a real crash, and the cost/wipe-out/concentration stresses push it to -36% to -43%. Assume **-35% to -45%** or worse on live money, and note it fails the protocol's drawdown criteria even in-sample (2 of 4 criteria fail on tune data).

What would change these verdicts: point-in-time Nifty 500 membership with delisted names and final prices (a1, a2), unadjusted closes (b3), volume/ADV data (d1), and a Nifty 50/500 TRI series (benchmark).

## Reproduce
```
cd analysis/bias
python 01_replicate.py   # engine equivalence
python 02_lookahead.py   # shifts + hand-checked trades
python 03_survivorship.py  # coverage, zero vs last, kills, hazard (about 4 min)
python 04_overfit.py; python 05_robust.py; python 06_placebo.py  # 06 about 8 min
python 07_liquidity.py; python 08_misc.py; python 09_lateentrant.py
```
