# Agent 5 - Skeptic: why the trend + quality framework fails live in India

## DATA WARNING (read first)
- Universe = TODAY's Nifty 500 survivors (499 columns, 272 priced on 2010-01-04), Yahoo adjusted closes, no delisted names. Benchmark = ^NSEI price index (no dividends). No PIT fundamentals, no volume, no PIT membership.
- Tune window only (2010-01-01 to 2018-12-31, warm-up from 2009). Loaded only via `data_loader.load_tune()`. No SEALED file and no post-2018 data was read. Where I mention 2019+ events (2020 crash, SEBI actions) it is general market history, flagged as "not tested here".
- Every in-sample number below is an UPPER BOUND. Nothing here proves the rule works; most of it shows how little the data can prove.
- Other reports: `3_risk_manager.md` and `4_fundamentals_tester.md` exist and are attacked in section 9. `1_backtester.md` and `2_bias_auditor.md` did NOT exist when I finished; I did not rely on them. I did not use the partial CSVs in `analysis/bias/`.

## What I ran
All in `analysis/skeptic/` (1 process, ~6 s per backtest, `backtest.py` untouched).
- `sk_common.py`: instrumented COPY of `backtest.backtest` (momentum, end_policy zero). Check: equity identical to `backtest.backtest` (max abs diff 0.0; matches Agent 3's numbers exactly: 24.52% CAGR, -34.42% MaxDD, 446 trades, 33 stops).
- `s1_core.py` (ablations, random baselines, leave-top-k-out, cost stress), `s2_diag.py` (drawdowns, regime, stops, turnover), `s3_5x_glitch.py` / `s4_base_rates.py` (concentration, 5x base rates, data glitches), `s5_regime_tax.py`, `s6_fix_breadth.py` (breadth, EW baselines; supersedes the breadth numbers in s2/s5 which had an NaN bug), `s7_tax_cost.py` (tax, cost, capacity). Outputs in `analysis/skeptic/out/*.txt`. Run: `cd analysis/skeptic && python s1_core.py && python s2_diag.py && ...`.

## 1. Bottom line
1. In-sample (survivor data) the rule shows 24.5% CAGR, but **its max drawdown (-34.4%) is deeper than Nifty's (-27.9%) and deeper than a naive hold of the same survivors (-31.2%)**. Protocol drawdown criterion fails on the tune window already.
2. The headline edge is mostly the universe. A plain equal-weight hold of the 272 survivors returned 22.9% CAGR (monthly-rebalanced 19.0%) vs the strategy's 24.5%. After tax the strategy (20.6%) is BELOW the buy-and-hold survivors (21.3%).
3. Profit is two years and about ten names. 2014 (+119%) and 2017 (+115%) produce 107% of net P&L; the other seven years net to -0.4x start capital. Top-10 names = 72% of net P&L.
4. It is not a multi-bagger finder. Of 446 trades, ONE reached 5x; median hold is 60 days; 99% of trades are held under a year. It is a short-horizon momentum rotation, taxed as such.
5. The two risk overlays (Nifty 200d regime filter, 30% stop) did not reduce drawdown and cost 6.0 and 1.1 pp CAGR (Rs 37,47,968 and Rs 5,73,951 of terminal wealth on Rs 10,00,000).
6. The "quality" half is untested (Agent 4: no PIT fundamentals exist). Everything is price momentum.

## 2. Where it loses money (explicit conditions)
The rule loses money, or underperforms Nifty, when one or more of these hold. Evidence tag: [T] = measured in tune window, [A] = argued/untested.

| # | Condition | Evidence |
|---|---|---|
| C1 | Narrow / rotating market: Nifty 50 above its 200d MA while breadth collapses and mid/small caps fall. The regime filter only watches Nifty 50, so it stays ON. | [T] Jan-Oct 2018: strategy -34.4% (Rs 36,42,242 from a Rs 1.06 cr peak; Rs 3,44,000 per Rs 10,00,000), Nifty -4.1%. Filter ON ~89% of days, 100% invested at peak and trough. Breadth (% of names above own 200d MA) went 87% to 13%. Sep-2018 alone: strategy -15.8% vs Nifty -6.4%. |
| C2 | Low breadth generally. | [T] Month-end breadth tercile 14-48%: next-month strategy -0.40% vs Nifty +0.86% (36% of months negative). High breadth 75-97%: +4.79%/month vs Nifty +1.30%. The edge exists only when everything is rising. |
| C3 | Sharp macro/policy shock that hits momentum favourites harder than the index (demonetisation Nov-2016, NBFC-heavy winners). | [T] Oct-Dec 2016: strategy -23.5% (Rs 12,91,743 of paper loss on the compounded account), Nifty -9.0%. Worst names: Sardaen, Escorts, Cholafin, Bajfinance, Muthoot. |
| C4 | Momentum crash / reversal month: yesterday's winners dump together. | [T] All 8 worst months had the filter ON; in 6 of 8 the strategy lost at least 1.5x the Nifty move (Nov-2016 -14.2% vs -4.8%; Sep-2018 -15.8% vs -6.4%; Jun-2018 -7.2% vs -0.2%; Dec-2016 -7.5% vs -0.5%). |
| C5 | A year without a mania/crowded theme. Alpha is two years. | [T] 2011 -10.3%, 2012 +21.8% (Nifty +27.7%), 2013 +4.2%, 2016 -5.7%, 2018 -22.9%. Strategy trailed Nifty in 28% of rolling 12m windows and was negative in 18%. |
| C6 | Stops cannot fill (circuit locks, suspension, gap-down on bad news). | [T] 33 "30%" stops filled on average 32.0% below the peak, worst -47.0% (PGEL 2013: -24.3% beyond trigger). 64% of fills were below the stop level. Close-only data hides intraday/circuit behaviour. [A] Fraud/insolvency names (Satyam-type, DHFL-type, Jet-type, Yes-Bank-moratorium-type) fall from a trend-OK state with no exit. None are in the data. |
| C7 | Costs/tax regime worse than assumed, or the account is treated as trading business income. | [T] 7.1x one-way turnover per year; see section 6. At 100 bps/side CAGR 18.0%; add 20% STCG and it is 15.1%. At a 30% slab (business income) after-tax is 18.7% from 24.5% pre. |
| C8 | Universe is point-in-time rather than hindsight: losers and not-yet-famous names are present. | [A] Unmeasurable here; Section 5. |
| C9 | Flat/choppy Nifty with 200d-MA flip-flops. | [T] Filter flipped state 19 times in 120 month-ends; when OFF, Nifty's next-month return was +1.64% (vs +0.57% when ON); 14 of 28 OFF months were followed by Nifty gains above +3% (avg +6.5%). The filter was anti-predictive in sample. |
| C10 | Gap crashes where the monthly-rebalance + next-close execution is too slow [A, not tested]: e.g. a Mar-2020-style 35-40% index fall in 5 weeks leaves the strategy invested through the fall and out near the low. Not in the tune window and not looked at. |

## 3. Worst stretches and what they had in common (tune window)
| Peak -> trough | Strategy | Nifty | Filter ON | Breadth peak -> trough | Common thread |
|---|---|---|---|---|---|
| 2018-01-15 -> 2018-10-09 (not recovered by 2018-12-31) | -34.4% | -4.1% | ~89% | 87% -> 13% | Crowded mid/small-cap winners (PCBL -0.54, GPIL -0.35, AVANTIFEED -0.26, GRAVITA -0.24, RADICO -0.23 in start-capital units) |
| 2016-10-25 -> 2016-12-26 (recovered 2017-05-11) | -23.5% | -9.0% | 100% | 82% -> 47% | Concentrated in NBFC/consumer-finance and autos |
| 2010-11-10 -> 2011-04-01 (recovered 2012-11-06, 727 days) | -23.2% | -7.2% | 60% | 85% -> 40% | Post-run-up fade; small contributors, 107 eligible names |
| 2013-01-29 -> 2013-04-12 | -14.5% | -8.6% | 100% | 69% -> 31% | Small-cap fade |

Common features: (a) the strategy fell 2.6-8x as far as Nifty in the same window; (b) the filter was mostly ON; (c) breadth was falling hard from 70-87%; (d) the holdings were last-12m winners bunched in one factor/theme; (e) 45% of all days were >10% below the prior peak, 9% of days >20% below; longest underwater stretch 493 trading days (727 calendar days from the 2010-11 peak, per Agent 3), and the 2018 stretch was still open on 2018-12-31.

## 4. Whipsaw cost of the regime filter and stops
- Regime filter: ON 69% of months, 19 flips, 28 OFF months. Strategy return in months after an ON signal +2.75%/month vs after OFF +0.09%, but Nifty itself did +1.64% in OFF months, so OFF months were not defensive in this sample. Terminal Rs 10,00,000 -> Rs 71,78,036 with filter vs Rs 1,09,26,003 without. MaxDD barely changes (-34.4% vs -33.9%). Equal weight cash earned 0% in the model (fully in cash 26.9% of days); real cash earns ~6-7%, worth ~1.5-2 pp/yr; fair to the filter, but not enough to change the verdict.
- 30% stop: 33 stops (3.7/yr). After exit, price was higher after 63 / 126 / 252 trading days in 53% / 54% / 56% of cases (mean +6.8% / +19.6% / +42.9%, median +2.7% / +7.5% / +25.0%). 50% regained the old peak within a year. 45% were re-selected by the rule within about 3 months (sold low, rebought). Stop variants: none 25.6% CAGR / -32.9% DD; 20% 22.5% / -34.6%; 30% 24.5% / -34.4%; 40% 25.7% / -32.9%. Tighter is monotonically worse; the stop never improves MaxDD.
- Turnover: 7.1x NAV one-way traded per year, 446 closed trades in 9 years (413 rebalance exits + 33 stops), median holding 60 days.

## 5. Multi-bagger base rates and concentration
- 5x capture: one trade of 446 reached 5x (0.2%); 3.1% reached 2x; hit rate 55%, median trade +1.4%, mean +10.6%. 99% of trades closed under 365 days. A rule that exits in ~2 months cannot capture 5x runs.
- Names that did 5x: in the data, 90 of the 272 names alive at 2010-01-04 rose 5x or more from 2010 to 2018 (140 rose 3x or more, 53 lost money). That is a hindsight artifact of survivor selection: today's Nifty 500 members are, by construction, the winners. A hindsight "any trough to later peak 5x" count is 206 of 346 names, which is meaningless. Better base rate (entry at each month-end through 2015, 3-year forward max within the survivor data): P(5x) = 9.1% unconditional, 15.4% for the rule's top-15 picks (n=765); P(2x) 48.5% vs 61.4%; 23.4% of picks fell 30% or more below entry within 12 months (before any stop). So even in a flattering universe about 85% of picks do NOT 5x and nearly a quarter draw down 30%+.
- Of the 206 names with a hindsight 5x run, the rule held 145 at some point during the run (70%) but held a given name on average only 7% of its run days; held 50% or more of the run for 1 name. "Held while it ran" is rare.
- Concentration (NAV units, 1.0 = start capital; total net P&L 6.77): top-1 = 18%, top-3 = 36%, top-5 = 49%, top-10 = 72%, top-20 = 101% of net P&L. Top contributors: HEGAM 1.20, GRAPHITE 0.72, UNOMINDA 0.54, HSCL 0.43, KEI 0.39, WELSPUNLIV 0.35, JBMA 0.35, GRAVITA 0.30, AVANTIFEED 0.30, PCBL 0.28. These names are in the universe because they are Nifty 500 members today, i.e. after they rose; with no PIT membership the true 2010-18 candidate list is unknown (adjusted price levels do not show 2010 size).
- Leave-winners-out (universe re-run without them): drop top-3 -> 21.1% CAGR, MaxDD -41.1%; drop top-5 -> 20.3% / -38.2%; drop top-10 -> 17.4% / -36.4%. A random 75% sub-universe stayed at 25-31% (not fragile to which names are present, fragile to the specific winners).
- Years: P&L in start-capital units by year 2010 +0.57, 2011 -0.14, 2012 +0.33, 2013 +0.10, 2014 +2.14, 2015 +0.80, 2016 -0.18, 2017 +5.09, 2018 -1.93. 2017 alone is 75% of the net total.
- Data fragility: 38 single-day moves beyond +/-25% in the tune data; the strategy held a name on 2 of them. KIRLOSENG sat at a stale Rs 126.29 for days, jumped +146% on 2010-06-24 (contributing +0.111 of start capital, about 11% of starting NAV) and fell -39% on 2010-12-24 (-0.043). Stale/illiquid prints and unadjusted corporate actions in Yahoo data can manufacture "momentum". Several other known glitch days (WHIRLPOOL +570% and NESTLEIND -76% on 2010-01-08) were harmless only because the strategy had not started trading.

## 6. Tax, costs, drift, capacity
Rules ASSUMED (check with a CA; I am not a tax adviser): equity delivery sold within 12 months = short-term, taxed at 20% (post 23-Jul-2024; 15% for 2019 to Jul-2024) plus 4% cess; held more than 12 months: LTCG 12.5% above Rs 1,25,000 per FY (10% above Rs 1,00,000 before Jul-2024). Losses offset gains, carried forward. Tax paid at each FY end out of the portfolio. Holding age uses the oldest lot (slightly kind to the strategy). Unrealised gains at the end of the window are not taxed (kind to the strategy). The 20% rule is applied to ALL tune years for illustration (the 2010-18 rules were different).
| Scenario (Rs 10,00,000 start, 2010-18 path) | Pre-tax CAGR / final | After-tax CAGR / final | Tax paid |
|---|---|---|---|
| 25 bps/side, STCG 20% | 24.5% / Rs 71,78,036 | 20.6% / Rs 53,82,324 | Rs 10,56,606 |
| 25 bps/side, STCG 15% (2019-Jul-2024 rule) | 24.5% | 21.6% / Rs 57,83,060 | Rs 8,32,419 |
| 25 bps/side, taxed as business income at ~30% | 24.5% | 18.7% / Rs 46,53,620 | Rs 14,44,999 |
| 50 bps/side, STCG 20% | 22.3% / Rs 61,16,704 | 18.7% / Rs 46,81,345 | Rs 8,98,213 |
| 100 bps/side, STCG 20% | 18.0% / Rs 44,37,530 | 15.1% / Rs 35,44,835 | Rs 6,38,873 |
| Nifty price buy-and-hold, one LTCG exit | 8.5% / Rs 20,76,096 | 7.7% | about Rs 1,24,000 |
| EW 272 survivors buy-and-hold, one LTCG exit | 22.9% | 21.3% | small |
94% of realised gross gains were short-term. Tax drag 3.0-5.9 pp/yr depending on assumption.
- Cost drift: the model uses a flat 25 bps/side. Fixed statutory cost (STT 0.1% each side on delivery, stamp 0.015% on buy, exchange/SEBI/GST, DP charge per scrip per sell) is about 11-12 bps/side before spread and impact. For the small, locked-circuit-prone names momentum picks, 25 bps total is optimistic (the config itself puts illiquid names at 50 bps). Each +25 bps/side costs about 2 pp/yr at 7.1x turnover. CAGR at 25 / 50 / 100 / 200 bps per side: 24.5% / 22.3% / 18.0% / 9.9% (200 bps is Nifty-price territory). The tune data has no volume, so slippage on these names is unmeasured. Statutory rates are policy variables, not constants; STT/stamp/tax changes in the 2019-2026 period are untested here.
- Capacity (no ADV data; arithmetic only): at 15 positions and a Rs 1,00,00,000 account, a position is Rs 6,66,667; at 10% participation that needs Rs 66,66,667 average daily traded value per name, and the config floor is Rs 1,00,00,000. At the floor name, the ceiling is about Rs 1.5 cr total (Rs 10 L/position at 10% ADV). Annual traded value is 7.1x the account (Rs 7.1 cr per Rs 1 cr). Momentum winners at selection time are the names with the largest recent volume spike, so entry (and the stop exit) trades against crowded liquidity. Above Rs 5 cr, a 30% stop is not executable in one session for small caps.
- Cash drag: the model's 0% on cash is conservative by ~1.5-2 pp/yr (26.9% days in cash). Netted against the above, it does not change the conclusion.

## 7. Behavioural failure: what the user must hold through
Same % at different account sizes (Rs loss from peak):
| Account | -34% (tune worst) | -50% (planning, Agent 3) | -60% (2008-type, untested) | One bad year (-22.9%) | Worst month (-15.8%) |
|---|---|---|---|---|---|
| Rs 10,00,000 | Rs 3,44,000 | Rs 5,00,000 | Rs 6,00,000 | Rs 2,29,000 | Rs 1,58,000 |
| Rs 25,00,000 | Rs 8,60,000 | Rs 12,50,000 | Rs 15,00,000 | Rs 5,72,500 | Rs 3,95,000 |
| Rs 50,00,000 | Rs 17,20,000 | Rs 25,00,000 | Rs 30,00,000 | Rs 11,45,000 | Rs 7,90,000 |
| Rs 1,00,00,000 | Rs 34,40,000 | Rs 50,00,000 | Rs 60,00,000 | Rs 22,90,000 | Rs 15,80,000 |
- The window contains neither 2008 nor 2020 nor 2022, and its worst case is still open at the end. A -34% in 9 years with all the favourable biases means -50% is an honest planning figure (Agent 3 agrees) and -60% is not unreasonable for a concentrated momentum book in a crowded-theme unwind.
- Time: the user must hold through 493-727 days underwater in-sample, with 45% of days more than 10% below peak. After 2017's +115% year the account gave back Rs 36,42,242 on the Rs 1.06 cr peak in nine months. This is the standard behavioural failure: peak euphoria, sizing up, then selling near the lows (the 2018 drawdown was still open at the end of the data).
- The strategy does well only by taking the 25-30% of months the user will want to skip (the regime-filter's OFF months produced +1.6% for Nifty). It requires monthly discipline over 120+ rebalances, 7x turnover and acting on stops mechanically.

## 8. Survivorship, the real attack
- EW baseline correction: "EW buy-and-hold of survivors" in Agent 3's report (12.1% CAGR / -20.4% MaxDD) is `backtest.buy_hold` over all 499 columns with `fillna(0)` returns, which counts not-yet-listed names as zero returns. The correct baselines on the 272 names alive at 2010-01-04: buy-and-hold 22.9% / -31.2%; monthly rebalanced 19.0% / -34.1%; daily rebalanced 19.5% / -33.3%. Versus those, the strategy's 24.5% / -34.4% is a +1.6 to +5.5 pp CAGR edge with equal or worse drawdown, before 7.1x turnover, tax and slippage. After 20% STCG and 25 bps, the strategy's 20.6% < buy-and-hold survivors' 21.3%.
- Same-engine baselines (8 seeds each; protocol wants 1000 runs and Agent 3 used 10 unfiltered with regime/stop on): random picks with the same filters (trend, 52w-high, regime, stops) 12.8% CAGR (range 3.8% to 19.4%), MaxDD -29.1%; random picks with no filters 8.2% (4.2% to 13.5%), MaxDD -38.6%. So the ranking by 12-month momentum contributes about 11.7 pp over random-from-the-filtered-set and the trend/52w filters about 4.6 pp over random picks. The ranking edge is the part most exposed to hindsight: among today's index members, the highest 12-month-momentum stocks of 2013-2017 are disproportionately names that kept compounding into index membership. 92% of P&L came from names already priced at the start of 2010. Several top contributors (HEGAM, JBMA, UNOMINDA, WELSPUNLIV, KEI) are not names a 2010 screen would obviously have owned; their 2010 market caps are unknown here (no data), so membership-by-hindsight cannot be sized.
- Not representable: delisted names whose price went to Rs 0 with no exit (suspensions, frauds, insolvencies). Agent 3's survivor-only worst trade is -47.0% and 0 trades below -50%, which is exactly what survivorship produces. Wipeout cost per Agent 3: 1% per name-year costs about 1 pp, 3% about 3 pp. I add that real wipeouts are not random: they strike names with a good trend and no exit, which a trailing stop cannot address.
- How much would a true universe cost? Unknown; the premium of survivors over Nifty alone is +11 to +14 pp CAGR (EW survivors 19-23% vs Nifty price 8.5%). Even a 1.2 pp dividend adjustment to Nifty leaves that premium far above the after-tax, after-cost edge (15.1% at 100 bps/side after tax vs roughly 9% for Nifty after tax). The edge disappears if survivorship and hindsight membership explain more than roughly 6 of those 11-14 pp.

## 9. Attacks on other agents' claims
**Agent 3 (risk manager), exists:**
1. EW baseline is wrong (section 8). Consequence: their statement that the strategy is "much deeper than a naive equal-weight hold (-20.4%)" is right in direction but the correct comparator is -31.2% (B&H) and -33.3% (daily-rebalanced), and the correct CAGR comparator is 22.9% not 12.1%. The strategy's return advantage over a survivor hold is +1.6 pp, not +12.4 pp. The same bug exists in `backtest.report()` ("Equal-weight buy&hold of universe").
2. "Planning budget -50%" is stated as 1.5x observed MDD, "judgement, not a model". With the observed worst starting 2018-01 and still open, plus no 2008/2020/2022 and concentrated 15 names, I would plan for -55% to -60% and 3+ years underwater, and treat -50% as a floor.
3. Recommending top_n >= 25 (Calmar 0.85 vs 0.71) rests on one path where CAGR is non-monotone in n (10: 30.7%, 15: 24.5%, 25: 26.7%). They acknowledge that but still recommend it. It changes the freeze after seeing the tune result; at best it needs to be pre-registered and tested as a robustness range, not picked.
4. "Rolling-entry view: median worst loss -4.7%": based only on entries inside 2010-2018, where two years carry >100% of the profit. It is a statement about this path, not entry-timing risk. The 2018-01 entrant lost -34.4% and was still underwater.
5. Agreed and reinforced: stop/regime do not help MaxDD; stop fill gap is real (my numbers match theirs: 33 stops, average shortfall -2.9% beyond trigger, worst trade -47.0%). I add: the stop cost 1.1 pp CAGR and 45% of stopped names were re-bought within about 3 months, so the stop is roughly a paid rotation, not protection.
6. Their reproduction matches mine to the paisa (both from the same engine); the independent check does not test engine bugs, only transcription.

**Agent 4 (fundamentals), exists:**
1. The "quality" leg has zero empirical content. Coverage of symbol-quarters in the tune window is 0%. Every number in this repo is price-momentum. Do not describe the result as "trend + quality".
2. Their gate thresholds (10% revenue/EBITDA growth, OCF/EBITDA >= 0.5, 8 contiguous quarters, fail closed on missing data) are untuned placeholders and fail closed, so on real data they would remove most banks/NBFCs (sector exclusion) and any recent-listing candidate, concentrating the strategy further and removing exactly the financial names (Bajaj Fin, Cholafin, Muthoot) that drove part of the 2016 loss and 2014-17 gains. Effect untested.
3. Even when PIT data arrive, a fundamentals gate multiplies the same hindsight problem: the surviving names' fundamentals are survivor-biased too (restated, delisted missing). A gate that "adds" 2 pp on survivors proves little.

**Agents 1 and 2:** not available at time of writing. If their reports claim (i) robustness of parameters, check against my ablations (regime off = +6 pp, stop off = +1 pp, parameters move CAGR by 4+ pp with no consistent direction), (ii) no look-ahead, check against the fact that the universe itself is a look-ahead (members chosen by future survival), which a bar-shift test cannot detect.

## 10. Loses-money summary for the frozen rule set
The framework should be expected to lose money or underperform Nifty TRI after tax when any of these hold:
1. Market breadth is falling from above 70% to below 40% while Nifty 50 holds above its 200d MA (2018 pattern). Trigger is invisible to the regime filter.
2. Two or more consecutive quarters with no top-10 name delivering +50%: the profits historically come from a few runners (top-10 = 72% of net P&L).
3. Realised round-trip cost (spread + impact + statutory) above 100 bps (50/side), or realised turnover above ~8x per year with 20%+ STCG and no tax-loss offset. Net edge over Nifty TRI after tax goes to roughly zero near ~11% pre-tax CAGR (rough: after-tax is about 0.8x pre-tax vs about 9% for Nifty TRI after tax).
4. The account is treated as business income (slab ~30%+): after-tax CAGR 18.7% from 24.5% pre-tax in-sample.
5. A held name is suspended, locked at lower circuit for 3+ days, put under a surveillance-measure stage that restricts trading, or goes into insolvency: the stop does not execute.
6. A true point-in-time universe (with delisted names and not-yet-listed names removed) lowers the strategy by more than ~8 pp. Not measurable now.
7. Position sizing above the liquidity floor: account above about Rs 1.5 cr with the config's Rs 1 cr ADV floor.
8. A 12-month momentum reversal (winners dumping together, as in Sep-2018 -15.8% and Nov-2016 -14.2%).

## 11. Kill-switch / stop-using-it criteria (numeric)
Pre-register these before the single test run; do not tune them afterwards. Rs figures assume the illustrative Rs 10,00,000 account; scale linearly or use the % column.
| Trigger | Threshold | Action |
|---|---|---|
| Account drawdown from high-water mark (HWM), warning | -25% (Rs 2,50,000 per Rs 10,00,000 of HWM) | Halve exposure; no new entries until 3 consecutive month-ends above the 200d MA of the strategy's own equity |
| Account drawdown from HWM, hard stop | -35% (Rs 3,50,000 per Rs 10,00,000 of HWM; tune max was -34.4%, so anything worse is outside the evidence) | Stop using the framework; move to index fund; written review before any restart |
| Time underwater | More than 30 months (tune longest 24 months, 2018 episode still open) | Stop |
| Rolling underperformance after tax and cost | Trailing 24 months after-tax return trails Nifty 50 TRI by more than 10 pp cumulative, OR trailing 36 months after-tax CAGR below Nifty 50 TRI | Stop |
| Realised slippage | Median measured slippage vs signal close above 60 bps/side over any 50 consecutive trades, OR all-in cost above 100 bps round trip per trade | Stop or cut size by half until fixed |
| Turnover | Annual one-way turnover above 8.5x NAV (tune 7.1x), or realised STCG tax drag above 5 pp/yr | Review; stop if after-tax return minus Nifty TRI is below +3 pp |
| Stop execution | Any stop filled more than 20% below its trigger, or two stops in one year more than 10% below trigger, or any exit blocked 3+ sessions by circuits | Impose a liquidity floor and a position cap of 5% of ADV; if repeated within 12 months, stop |
| Single-name loss | Any position down more than 50% from entry (tune worst -47%) or any halted/suspended name | Exit what is possible; review whole book; if it is the second such event in 24 months, stop |
| Concentration of profit | Trailing 24-month P&L excluding the top 3 positions is below Rs 0 | No sizing-up; do not add capital |
| Out-of-sample criteria | Any of the four `config.CRITERIA` fails in the single test run (CAGR vs Nifty TRI, CAGR vs random median, MaxDD vs Nifty TRI, MaxDD vs random median) | Do not deploy; the result is the negative finding |
| Cost stress | Test CAGR at 2x cost (50 bps/side) not beating Nifty TRI | Do not deploy |
| Capital cap | Account above about Rs 1.5 cr with the Rs 1 cr ADV floor | Do not scale beyond the cap |
| Breadth overlay (hypothesis only, NOT validated) | Nifty above its 200d MA but breadth (% of Nifty 500 above own 200d MA) below 35-45% | At most a monitoring flag. Only 5 to 12 months in the sample; mean strategy return was not clearly negative, so do not trade it without a pre-registered test. |

## 12. Caveats about my own evidence
- Single 9-year survivor path; no statistical power. Two years drive the result, so differences of 1-2 pp (stop effect, top_n) are noise.
- Random baselines are 8 seeds, not 1000.
- Tax simulation approximates lot age by position age and ignores unrealised gains at the end; tax paid each FY end out of the portfolio (the real path would also have exemptions and carry-forward subtleties).
- Breadth is computed from ffilled prices on the 499-name survivor universe; the first draft (s2/s5) had an NaN bug and was superseded by `s6_fix_breadth.py`. The EW baseline in section 8 includes only names alive on 2010-01-04.
- No volume, no circuit data, no intraday; stop and liquidity risk are understated. 2019+ behaviour is unseen by design.
