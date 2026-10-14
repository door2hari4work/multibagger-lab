# C. New US stock ideas that diversify an AI/tech-heavy book (as of 2026-10-14)

Research, not advice. Nothing is executed. All figures are dated; prices are 2026-10-13 closes (Yahoo adjusted closes via yfinance) unless stated.
Tags: **FACT** (source named), **INFERENCE**, **SPECULATION**; "unverified" = not confirmed in a primary source this session. All probabilities are labelled model estimates.
Public repo: no personal portfolio numbers appear here. Position sizes are suggested weights as % of total net worth (new-money amount is unknown).

## 0. Bottom line

| Tier | Name | Role in a tech-heavy book | Verdict (one line) |
|---|---|---|---|
| 1 core accumulate | **LLY** Eli Lilly | Healthcare growth; near-zero tech link | Best earnings growth of the set; 32x 2026E is full, so build in thirds, not at once |
| 1 core accumulate | **CB** Chubb | P&C insurance; negative link to Nasdaq | Cheapest quality name (12x), rate beneficiary; pricing cycle is turning, so size modestly |
| 2 starter + wait | **MA** Mastercard | Payments (quality compounder) | At an all-time high, +10% in 2 weeks, 14% above 200d MA; starter only |
| 2 starter + wait | **CVX** Chevron | Oil-shock insurance | Peak-war-premium earnings; starter-sized hedge only, not a return play |
| 3 watchlist | **GD** General Dynamics | Defence/aerospace | Below 200d MA (lab rule: not yet); defined triggers below |
| 3 watchlist | **KRYS** Krystal Biotech | Higher-risk growth (profitable gene-therapy) | Binary readouts before year-end; wait for the events or a lower price |

Honest framing (INFERENCE): none of these is a bargain. The S&P 500 sits at a record (~7,800 on 2026-10-07, source: cryptodaily.co.uk market wrap) and the 10-yr Treasury touched 5.36% intraday that day (same source; unverified elsewhere). The case for these six is **diversification and quality**, not mispricing. The lab's own evidence: trend filters protect but do not find multi-baggers, the quality gate showed no value, timing states carry no return edge, 5x outcomes are rare. Expect index-like to modestly better outcomes, not 3x.

## 1. How the shortlist was built

1. Universe: current S&P 500 + S&P 400 members (903 names, survivor-biased) with the lab's screen fields (12-1 momentum, 200d MA, 52w high, vol, liquidity), computed on prices to **2026-10-13**. I reused the scratchpad `signals.csv` produced with the lab's `mblab/discovery.py` definitions; I did not re-run `discovery.py` end-to-end. Yahoo data is unaudited.
2. Excluded: the 8 held names, the 16 names already in `theses/US`, employer-correlated custody banks (BNY, STT, NTRS), and IT / Real Estate sectors (this task is diversification).
3. Filters (lab's): liquid, close > 200d MA, 12-1 momentum > 0, within 25% of 52w high -> 281 names. Then a quality screen (ROE > 12%, operating margin > 10%, FCF > 0, market cap > $8B, vol < 45%, not > 35% above 200d MA) -> 113 names. I added ~15 quality names that fail the trend filter (defence, medtech, staples) so they can be Tier 3 with triggers.
4. Shortlist of 26 (below), then primary-source research (company 8-K press releases on SEC EDGAR, via WebFetch; SEC_CONTACT was not set so no direct EDGAR API calls) on 8: LLY, CB, MA, CVX, GD, KRYS, plus JNJ, MRK/REGN checked and rejected.

| Ticker | Px | 12-1 mom | Mom pct (903) | Vol | From 52w high | vs 200d | Trend ok | Fwd P/E | ROE | Op margin | Rev gr | FCF yld |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LLY | 1162 | +37% | 77 | 34% | -9% | +8% | Y | 24.5 | n/m | 54% | 48% | 1.1% |
| JNJ | 249 | +43% | 81 | 20% | -10% | +3% | Y | 20.8 | 26% | 29% | 7% | 2.8% |
| MRK | 142 | +72% | 91 | 29% | -9% | +15% | Y | 15.3 | 7% | ~0% (charge) | 5% | 4.3% |
| ABBV | 274 | +17% | 57 | 25% | -2% | +19% | Y | 16.9 | n/m | 40% | 10% | 3.5% |
| REGN | 755 | +41% | 80 | 33% | -11% | +3% | Y | 12.2 | 14% | 33% | 17% | 4.0% |
| TMO | 661 | +17% | 57 | 29% | -3% | +21% | Y | 24.0 | 14% | 19% | 11% | 2.5% |
| HCA | 461 | +3% | 37 | 31% | -15% | +4% | Y | 14.4 | n/m | 15% | 9% | 3.7% |
| KRYS | 324 | +87% | 94 | 38% | -14% | +7% | Y | 34.7 | 20% | 49% | 24% | 1.6% |
| MA | 603 | +4% | 38 | 23% | 0% | +14% | Y | 26.2 | n/m | 61% | 14% | 3.2% |
| V | 394 | +10% | 47 | 22% | 0% | +17% | Y | 26.4 | 61% | 66% | 14% | 2.7% |
| CB | 347 | +22% | 63 | 20% | -4% | +5% | Y | 11.8 | 15% | 24% | 6% | 7.9% |
| TRV | 373 | +42% | 80 | 21% | -6% | +16% | Y | 12.2 | 27% | 24% | 0% | 19% (cat-light yr) |
| CPAY | 399 | +47% | 83 | 37% | -6% | +14% | Y | 12.7 | 29% | 47% | 22% | 7.4% |
| JPM | 334 | +18% | 58 | 22% | -8% | +5% | Y | 13.2 | 18% | 50% | 30% | n/m |
| GD | 334 | +9% | 45 | 22% | -15% | **-5%** | **N** | 17.8 | 18% | 10% | 8% | 4.9% |
| RTX | 184 | +26% | 66 | 26% | -19% | **-5%** | **N** | 23.3 | 12% | 13% | 15% | 4.0% |
| PH | 959 | +31% | 72 | 26% | -11% | +1% | Y | 24.0 | 25% | 23% | 10% | 2.5% |
| EMR | 164 | +20% | 60 | 32% | 0% | +13% | Y | 22.5 | 13% | 27% | 7% | 4.1% |
| KO | 90 | +36% | 76 | 19% | -1% | +13% | Y | 25.6 | 42% | 35% | 7% | 1.3% |
| PG | 153 | 0% | 32 | 20% | -7% | +5% | Y | 20.7 | 30% | 22% | 2% | 3.7% |
| COST | 956 | -1% | 31 | 20% | -13% | -1% | N | 38.2 | 28% | 4% | 11% | 1.6% |
| ROST | 225 | +57% | 88 | 26% | -12% | +3% | Y | 25.2 | 43% | 14% | 13% | 2.8% |
| CVX | 218 | +48% | 84 | 24% | 0% | +17% | Y | 14.5 | 12% | 22% | 54% | 5.1% |
| XOM | 174 | +53% | 87 | 26% | 0% | +16% | Y | 15.2 | 13% | 16% | 44% | 2.9% |
| WMB | 75 | +18% | 59 | 24% | -5% | +5% | Y | 28.2 | 22% | 40% | 8% | negative |
| DUK | 118 | -3% | 28 | 16% | -10% | -3% | N | 16.5 | 10% | 28% | 1% | negative |

Source: lab screen fields and Yahoo `info` (aggregator, unaudited), 2026-10-13/14. Fwd P/E uses Yahoo's forward EPS (next fiscal year).

**Why these six and not the rest** (one line each): JNJ (adj. EPS -7.5% in Q3, 2026 EPS growth ~3%, 22x current-year; yield 2%, rich versus its own 4-yr FYE P/E of 10-24x, talc charge); MRK (2026 EPS wiped by Terns charge, Keytruda dependence; ~$8.4B of $16.6B Q2 sales; 15x is fair, not cheap); REGN (Eylea franchise falling 45% y/y; aggregator 2027E EPS below 2026E); V (same as MA, slightly lower growth; pick one); TRV (2027E EPS -12% as cats normalise, same cycle risk as CB); PG/KO/COST (growth 2-7% at 21-38x with 10-yr near 5%); PH/EMR (24x/22x, automation exposure partly AI-capex linked); ROST (best momentum but tariff-sensitive, 25x); XOM (duplicate of CVX); WMB (28x, negative FCF); DUK (below 200d, negative FCF, rate-sensitive); RTX (below 200d, 23x).

## 2. Portfolio-fit evidence (computed 2026-10-14; Yahoo adj. closes)

| | LLY | CB | MA | CVX | GD | KRYS |
|---|---|---|---|---|---|---|
| Beta to QQQ (3y daily) | 0.34 | -0.06 | 0.34 | 0.10 | 0.23 | 0.64 |
| Corr with an equal-weight basket of the 8 held AI/mega-cap names (daily, 2018+) | 0.26 | 0.26 | 0.59 | 0.33 | 0.35 | 0.29 |
| Mean daily return on QQQ's worst-10% days (QQQ avg -2.28%) | -0.43% | +0.46% | -0.53% | -0.23% | -0.34% | -1.37% |
| Max drawdown since listing (2005 or IPO) | -51% | -51% | -63% | -56% | -61% | -53% |
| Feb-Mar 2020 drawdown | -15% | -42% | -41% | -51% | -43% | -44% |
| 2022 (Jan-Oct) drawdown | -13% | -8% | -23% | 0% | -1% | -32% |
| Apr 2025 (Feb 19-Apr 8) drawdown | -17% | 0% | -16% | -13% | 0% | -10% |

INFERENCE: real diversification versus the AI basket, but partial (equal-weight basket of LLY/MA/CB/CVX/GD has 0.50 correlation with the AI-8 basket; MA at 0.59 is the weakest diversifier). In a 2020-style liquidity crash everything falls; the diversifiers do not protect there. They protected in 2022-type (rate/tech) and Apr-2025-type (tariff) stress.

Basket stats (equal weight, monthly rebalanced, LLY/MA/CB/CVX/GD since 2012-06): max drawdown -38.7% (2020-03-23); share of 12-month windows with a dip beyond -22.5% from entry: 7.3%; p5 worst 12m dip -30%. These names were chosen today, so the sample is survivor-selected and understates risk; the 25.8% CAGR including KRYS is not an expected return.

## 3. Sizing and risk budget (suggested caps, % of total net worth)

| Name | Cap | First tranche (now) | Stress drawdown used | Loss at cap (pp of net worth) |
|---|---|---|---|---|
| LLY | 3.5% | 1.2% | -35% (own 2020 -15%, GLP-1 de-rating assumed) | 1.2 |
| CB | 2.5% | 0.8% | -42% (Mar 2020) | 1.1 |
| MA | 3.0% | 0.75% | -41% (Mar 2020) | 1.2 |
| CVX | 1.0% | 0.25% | -50% (Mar 2020 -51%; oil to $60) | 0.5 |
| GD | 2.0% | 0 (trigger) | -43% | 0.9 |
| KRYS | 1.0% | 0 (trigger) | -55% | 0.55 |
| **All six** | **13.0%** | **~3.0%** | | **~5.4 pp** |

- A fully built sleeve (13%) falls ~41% in a Mar-2020-type crash, beyond the stated 20-25% limit on money invested. Mitigation: build in thirds (an unfilled tranche is cash), apply the per-name review rules below, and treat the cap table as maximums, not targets. Starting at ~3% of net worth, a Mar-2020 replay costs ~1.2 pp.
- Lab evidence on stops (ENGINE_FINDINGS section 3): stop level 30-50% barely changed results; exit on a 200d-MA break helped in India, weaker in the US. So the rules below use a **review at -20% from average cost** and **sell at -25% only if the thesis is also impaired or the 200d is broken**; mechanical stops are a risk-limit choice, not an edge. Gaps through a stop are possible.
- Sleeve rule: no single new name above 3.5%; Tier 3 names stay at or below 2%; the whole sleeve stays below ~13% until the first four quarters of results confirm theses.

## 4. Idea sheets

### 4.1 LLY, Eli Lilly (Tier 1)

**Business.** Diabetes/obesity (tirzepatide: Mounjaro, Zepbound), oncology (Verzenio), immunology, pipeline of oral GLP-1 (orforglipron, brand Foundayo) and retatrutide.
**Thesis (1-2 yrs).** Volume-led growth: Q2 2026 revenue $22.97B, +48% (volume +60%, price -13%); Mounjaro $9.94B (+91%), Zepbound $4.93B (+46%). FY26 revenue guidance raised to $85-87B; non-GAAP EPS $35.50-36.50 (after $3.03 of Q2 IPR&D). Performance margin guide raised to 49.0-50.5%. Retatrutide full obesity data package; BLA planned Q1 2027. FACT (Lilly 8-K Ex.99.1, 2026-08-05, sec.gov/Archives/edgar/data/0000059478/000005947826000077).
**What is priced in.** 32.4x 2026E (guide midpoint $36) and 24.5x consensus 2027E EPS ($47.6, aggregator, unverified); EV/EBITDA 26x. Own FYE trailing P/E: 54x (2022), 99x (2023), 65x (2024), 47x (2025), so the multiple has been compressing as earnings catch up. Street mean target $1,330 (range $930-1,600, 29 analysts, aggregator). INFERENCE: market already pays for roughly +35% EPS in 2027; it needs that plus the oral/retatrutide follow-through.
**Three strongest bear points.**
1. Price erosion: realised price -13% in Q2 (US -3%, ex-rebate-adjustments about -9%; ex-US -36% on China NRDL). Further US price pressure from government pricing agreements is plausible (INFERENCE).
2. Oral launch is behind Novo: Foundayo $98M in Q2; early IQVIA data showed Novo's Wegovy pill ~67k weekly scripts at week 7 vs ~11.7k for Foundayo (Fierce Pharma, ~2026-06-01); RBC cut 2026 Foundayo sales expectations from ~$4B to ~$1.6B. IQVIA may undercount telehealth (Citi). Newer data not found: unverified.
3. Concentration + rates: tirzepatide is most of growth; the stock fell from ~$1,208 (07-29) to $1,166 and sits 9% below its high with the 10-yr near 5%; a 22x multiple on a $38 EPS gives $836 (-28%).
**Kill criteria (observable).** (a) FY26 revenue guide cut below $85B; (b) combined Mounjaro+Zepbound US revenue falls sequentially in a quarter; (c) Foundayo Q3 revenue below Q2's $98M; (d) retatrutide BLA slips beyond 1H 2027; (e) close below the 200d MA (~$1,075) with a guide cut.
**Entry.** Thirds. T1 now (up to ~$1,190, i.e. <=25x 2027E). T2 after the Q3 print (aggregator date 2026-10-29; Lilly had not announced a date, unverified) if guidance holds or rises and price <= ~$1,250. T3 on a pullback to <= $1,075 (200d MA; 30x 2026E guide) or, if none occurs, after the Q4 print (early Feb 2027) provided thesis intact. Do not chase above $1,300 (new high; ~36x 2026E).
**Accumulate on.** US Mounjaro+Zepbound volume still growing and guide raised; dips to the 200d MA with no kill trigger.
**Trim / sell.** Trim one-third of the position if price >= $1,430 (30x consensus 2027E) or if weight exceeds the 3.5% cap. Sell if any kill criterion hits, or close < $1,000 (about -14% from entry zone) with a negative estimate revision. Review at -20% from average cost.
**Cap.** 3.5% of net worth. **Catalysts.** Q3 results ~late Oct (unverified), Foundayo scripts weekly (IQVIA), retatrutide filings, US pricing policy news.
**Model-estimate odds (12m).** P(+30%) 15%; P(>= +10%) 45%; P(touches -25% from entry) 14%; P(ends <= -25%) 8%. Own 21-year history shows P(+30% in 12m)=34% but that is survivor-selected; discounted.

### 4.2 CB, Chubb (Tier 1)

**Business.** Global P&C (commercial, personal, reinsurance-adjacent specialty) plus life/accident & health. Underwriting-profit and float-income model.
**Thesis.** Q2 2026 core operating EPS $7.26, +18.2%; P&C combined ratio 83.8% (85.4% a year earlier); record net investment income $1.76B (+12.3%); P&C premiums +3.0% (+6.3% excluding large-account/E&S property that Chubb is deliberately shedding); catastrophe losses $475M vs $630M. FACT (Chubb Q2 release, 2026-07-21, sec.gov/Archives/edgar/data/0000896159/000119312526310312; summarised by Insurance Business). Higher yields lift investment income, which is the reverse of the tech book's rate sensitivity (INFERENCE).
**What is priced in.** 12.3x 2026E ($28.1) and 11.8x 2027E ($29.3), aggregator; year-end trailing P/E 10.1-16.8x over 2022-25 (computed from Yahoo EPS), so the multiple sits in the middle. Dividend yield 1.2%; FCF yield ~8%. Price $346 vs mean target $367 (23 analysts).
**Three strongest bear points.**
1. Pricing cycle turning: commercial property rates fell for a fifth straight quarter (Baldwin -8.1% in Q2; WTW -14.5% for large risks); Chubb's North America Commercial premiums -2.3%. Earnings are at a cyclical high.
2. Consensus Q3 EPS $6.80 is -9% y/y (vs $7.49) and 2027E growth is only ~4% (aggregator); no earnings tailwind to re-rate on.
3. Tail risks: hurricane season runs to Nov 30 (forecast below-normal, but one major landfall tightens everything), and long-tail casualty reserve adequacy is flagged by Fitch as the structural risk.
**Kill criteria.** P&C combined ratio above 92% (ex-major-cat) for two quarters; adverse prior-year reserve development above ~$500M in a quarter (my threshold); P&C premiums negative ex-FX for two quarters; close below 200d MA (~$329) with 2027E EPS cut > 10%.
**Entry.** Thirds. T1 now (<= ~$355, 12.6x 2026E). T2 after the Q3 print (aggregator 2026-10-20, unverified) if combined ratio < 90%. T3 at <= $330 (200d MA, 11.7x) or after the Q4 print (late Jan/Feb 2027) if thesis intact.
**Accumulate on.** Dips to $330-340 without reserve charges; a major hurricane that hits the group less than peers (opportunity), after reading the loss estimate.
**Trim / sell.** Trim one-third at >= $400 (14.2x 2026E; upper part of the 4-yr range) or above the 2.5% cap. Sell on any kill criterion. Review at -20% from average cost.
**Cap.** 2.5%. **Catalysts.** Q3 ~Oct 20 (unverified); hurricane/cat events to Nov 30; Jan 1 reinsurance renewals; Q4 late Jan.
**Odds (12m).** P(+30%) 6%; P(>= +10% incl. dividend) 42%; P(touches -25%) 8%; P(ends <= -25%) 4%.

### 4.3 MA, Mastercard (Tier 2: starter and wait)

**Business.** Global card network; revenue from volume-linked assessments, cross-border, and value-added services.
**Thesis.** Q2 2026 net revenue $9.3B, +14% (+12% currency-neutral); adjusted operating margin 61.1%; adjusted EPS $5.04, +21%; Q2 buybacks $4.9B. FY guide: currency-neutral growth at the high end of low double digits; opex low double digits. FACT (Mastercard 8-K Ex.99.1, 2026-07-30, sec.gov/Archives/edgar/data/0001141391/000114139126000081; guidance from call summary, webull). Agent-pay/stablecoin plans (BVNK acquisition expected to close Q3).
**What is priced in.** 30.3x 2026E ($19.94) and 26.2x 2027E ($23.06), aggregator. FYE trailing P/E 33-37x in 2022-25, so today (33x trailing) is in line with its own history, not cheap. Price $605 equals the 52w high; target $670 (mean).
**Three strongest bear points.**
1. Entry price: +10% since 2026-09-30 ($551 -> $605), 14% above 200d MA, 12-1 momentum rank only 38th percentile (lab: momentum rank is the selector with edge, and this is not top-ranked).
2. Regulation/legal: revised Visa/Mastercard merchant settlement (interchange cut ~0.1pp for five years, preliminary approval, reports conflict on size, Walmart seeking opt-out); the Credit Card Competition Act was publicly backed by the President in Jan 2026 (Constantine Cannon summary). Current status unverified.
3. Growth quality: Q2 cross-border helped by Venezuela card-not-present spending and promotion timing; Europe growth slowing as it laps 2024 wins; Middle East conflict "dynamic". Highest correlation with the AI basket of the six (0.59): not a strong diversifier.
**Kill criteria.** Currency-neutral net revenue growth below 9% for two quarters; CCCA or equivalent enacted; cross-border volume growth below 8% for two quarters; adjusted operating margin below 58%.
**Entry.** Starter only: T1 = one quarter of target size now. T2 at <= $575 (50d MA ~$572; 28.8x 2026E) after the Q3 print (aggregator 2026-10-29, unverified). T3 at <= $540 (27x). If it only rises, do not chase above $650; add after Q4 results instead.
**Accumulate on.** Pullbacks into $530-575 (200d MA ~$531), or a result showing revenue growth held at 12%+ with margin >= 60%.
**Trim / sell.** Trim one-third at >= $720 (31x 2027E) or above 3.0%. Sell on kill criteria; close < 200d MA with downgrade of 2027E EPS. Review at -20%.
**Cap.** 3.0%. **Catalysts.** Q3 ~Oct 29 (unverified; Visa ~Oct 27), settlement approval hearings (dates unverified), BVNK close, CCCA moves.
**Odds (12m).** P(+30%) 8%; P(>= +10%) 40%; P(touches -25%) 12%; P(ends <= -25%) 6%. Scenario arithmetic (model): bear 22x x $21.5 = $473 (-22%); base 28x x $23.0 = $645 (+7%); bull 31x x $24 = $744 (+23%).

### 4.4 CVX, Chevron (Tier 2: hedge-sized starter)

**Business.** Integrated oil major (Hess assets since 2025), refining and chemicals.
**Thesis (as a hedge, not a growth idea).** An Iran war/Hormuz disruption has kept Brent around $100 (Brent $100.20 on 2026-10-07; range $97-108 in early Oct; cryptodaily, moneymagpie). Q2 2026: production 4,070 MBOE/d (+~20% y/y with Hess), adjusted FCF $15.4B (vs $4.9B), debt cut by a record $8.4B, $1.5B Hess synergies achieved (Chevron 8-K and press, 2026-07-31; buyback figure conflicts between sources). An oil shock is the scenario that hurts the rest of the investor's book most (stress case "India rate/oil, Nifty -20" in the lab's stress file), so a small oil position pays when other things lose (INFERENCE).
**What is priced in.** 12.8x 2026E ($17.0) but 14.6x 2027E ($14.9): consensus already expects earnings to fall 12% next year, i.e. a Brent glide-down; the EIA (2026-08-11) forecasts Brent averaging $69 in 2027; Goldman's earlier base $70. Yield 3.3%. Price $218 = 52w high, 17% above 200d MA, up 21% in 3 months.
**Three strongest bear points.**
1. Peak-earnings entry: shares at a high with Brent ~$100 while the base case from EIA/Goldman is ~$70 in 2027 (a ~30% lower oil price).
2. A Hormuz settlement could reprice oil quickly: the scenario that helps the rest of the book hurts CVX (hedge works in one direction only).
3. Capex up (Q2 $4.5B vs $3.7B) and buybacks at the low end of the range while debt is repaid.
**Kill criteria.** Brent 3-month average below $70 together with 2027E EPS below $12.5; close below the 200d MA (~$186) for a week; dividend cover break. Hedge purpose ends if the investor's book has no oil-shock sensitivity (unknown).
**Entry.** Quarter-size starter now. T2 at <= $200 (50d MA ~$205; 13.4x 2027E). T3 at <= $186 (200d MA). If Brent falls below $80 and CVX is still above $210, skip T2/T3.
**Accumulate on.** Pullbacks to $186-200 with Brent >= $80. **Trim / sell.** Trim half at >= $240 (16x 2027E) or if weight > 1.5% from price rise; sell if close < 200d MA and Brent < $75. **Cap.** 1.0% (hedge size; 1.5% only on price drift).
**Catalysts.** Q3 results ~Oct 30 (aggregator, unverified), OPEC+ decisions, Hormuz/ceasefire news.
**Odds (12m).** P(+30%) 7%; P(touches -25%) 20%; P(ends <= -25%) 10%. Scenario (model): Brent $60 -> EPS $11 x 12.5 = $138 (-37%); base ($70) EPS $14.9 x 13.5 = $201 (-8%, +3% dividend); war persists ($100) EPS $20 x 12 = $240 (+10%). Skewed down as a stand-alone investment; the case is only insurance.

### 4.5 GD, General Dynamics (Tier 3: watchlist, wait for trigger)

**Business.** Gulfstream business jets, nuclear submarines/ships (Marine Systems), combat vehicles, IT services.
**Thesis.** Q2 2026 (quarter ended 2026-07-05): revenue $14.1B (+8.1%), EPS $4.24 (+13.4%), operating margin 10.4% (+40bp), backlog a record $136.5B (+32% y/y), orders $20B (book-to-bill ~1.4), operating cash flow $1.9B (162% of earnings). FY26 EPS guide $16.80-16.90, revenue ~$55.7B. FACT (GD 8-K Ex.99.1, 2026-07-29, sec.gov/Archives/edgar/data/0000040533; govconwire, marketbeat). A 44% increase in FY27 defence spending was requested (Daily Upside, date not given).
**What is priced in.** 19.7x 2026E guide mid ($16.85), 17.8x 2027E ($18.65); FYE trailing P/E range 18.6-21.4x in 2022-25. Price $332 is 15% below the 52w high ($400), 5% below the 200d MA ($351); it fell from $379 on 07-29 despite a beat. The cause of the Sept-Oct decline was not found: unverified. INFERENCE: higher yields and "peak defence spending" worries.
**Why Tier 3.** Fails the lab's trend filter (below 200d MA). Trend filters protect rather than find winners, but the rule is clear and I follow it.
**Three bear points.** (1) Second-half cash flow guided lighter (capex, ~$500M pension, >$500M cash taxes); (2) aerospace (Gulfstream) cyclicality and a sell-side downgrade ("has run its course", Seeking Alpha; reasoning not retrieved); (3) lowest operating margin (10%) of the set, so earnings are sensitive to shipyard execution; the stock lacks a catalyst until the Q3 print.
**Kill criteria.** Backlog falls sequentially with book-to-bill < 0.9 for two quarters; FY EPS guide cut below $16.0; major submarine/ship charge; Gulfstream delivery guide cut.
**Trigger to start (either).** (A) trend: 5 closes above the 200d MA (~$351) with backlog >= $136B at the Q3 print; (B) value: <= $300 (17.8x 2026E guide), a level below its 4-yr low multiple, with book-to-bill >= 1.0. Start at one-third of position.
**Accumulate on.** A second tranche after two consecutive prints with margin >= 10.4%. **Trim / sell.** Trim at >= $400 (21x 2026E; 52w high) ; sell on kill criteria or a close below the 200d MA after entering via trigger B. **Cap.** 2.0%.
**Catalysts.** Q3 result late Oct (aggregator 2026-10-30, unverified), FY27 defence appropriations, Gulfstream certification milestones.
**Odds (12m, if bought at $332).** P(+30%) 12%; P(touches -25%) 14%; P(ends <= -25%) 6%.

### 4.6 KRYS, Krystal Biotech (Tier 3: higher-risk growth, wait)

**Business.** Commercial-stage gene-therapy company; VYJUVEK (topical gene therapy for dystrophic epidermolysis bullosa) is the only marketed product; inhaled and eye programmes in development.
**Thesis.** Q2 2026 VYJUVEK revenue $119.2M (+24%), gross margin 95%, US $91.6M; net income $54.8M ($1.79/share; Nasdaq summary, secondary); cash and investments over $1.1B (about 11% of market cap) and no debt; 2026 R&D+SG&A guided $175-195M. Launches in Germany, France, Japan; Spain and Italy expected before year-end; UK approved May 2026. FACT (Krystal 8-K Ex.99.1, 2026-08-03, sec.gov/Archives/edgar/data/0001711279/000171127926000058; call summary).
**What is priced in.** 41.5x 2026E ($7.74) and 34.7x 2027E ($9.27) at $321; EV/EBITDA 43x; mean target $392 (aggregator). Momentum rank 94th percentile (the lab's only selector) but vol 38-49%.
**Bear points.** (1) Single product: all profit is VYJUVEK; US sequential growth +4.7% (Q1 $87.5M to $91.6M) suggests the US patient pool is maturing; (2) binary readouts: KB407 (cystic fibrosis, ~5 patients, safety/expression only) interim before year-end, other registrational readouts reported by a secondary source for Q4 (unverified); (3) European reimbursement slow (Germany/France talks into 2027); a 35x multiple leaves little room.
**Kill criteria.** US VYJUVEK revenue declines sequentially for two quarters; Q3 global VYJUVEK below ~$115M; failed registrational readout; new competing DEB therapy approved; close below $250 after entry.
**Trigger to start.** Either (A) Q3 print (aggregator 2026-11-02, unverified) shows global revenue >= $125M and price stays > 200d MA (~$304) -> start at one-half of target; or (B) price <= $290 (about 37x 2026E) with no negative news; do not buy ahead of year-end readouts at full size.
**Accumulate on.** Positive KB407/other data after which the price holds above the pre-event level. **Trim / sell.** Trim half on a +50% gain from entry (a single-product name; take risk off); sell on any kill criterion. **Cap.** 1.0% (stress -55%).
**Catalysts.** Q3 ~Nov 2, KB407 interim and registrational readouts by year-end, Spain/Italy launches.
**Odds (12m).** P(+30%) 25%; P(touches -25%) 35%; P(ends <= -25%) 20%. Own history shows 37% of 12m windows with a >22.5% dip (nine years of data).

## 5. Taxes, employer rules and mechanics (state what was verified)

- Sources (blog summaries, not official; verified only that sources agree, 2026-10-14): gains on foreign shares are long-term only after 24 months (12.5%, no indexation); short-term is at slab rate. Both are computed in INR using SBI TTBR dates. **Implication:** with a 1-2 year horizon, trimming within 24 months realises slab-rate gains; trim rules here are therefore partial and size-driven. Verify with a CA.
- US dividends: 25% withholding for Indian individuals under the DTAA with W-8BEN (sources agree); Foreign Tax Credit through Form 67 on time. Affects LLY, MA, CB, CVX, GD (all pay dividends); KRYS pays none.
- LRS limit USD 250,000 per financial year (sources); TCS 20% above Rs 10 lakh (sources conflict between Rs 7 lakh and Rs 10 lakh): **unverified; verify with CA/bank**.
- US estate-tax exposure for non-US persons holding US-listed shares directly (threshold around USD 60,000; there is no India-US estate treaty): from memory, **not verified this session; verify with CA**.
- Employer rule (BNY): the investor works at a financial firm; **verify with HR/compliance** whether pre-clearance, holding periods or a restricted list cover payments/insurers (MA, CB) or any of these names. I deliberately avoided custody banks.
- Schedule FA reporting of foreign assets applies (standard practice; verify).

## 6. Calendar (all dates from Yahoo's calendar unless stated; treat as unverified until the company confirms)

| Date | Event |
|---|---|
| ~Oct 20 | CB Q3 |
| ~Oct 27 | Visa Q3 (read-through for MA) |
| ~Oct 29 | LLY Q3 (Lilly had not announced), MA Q3, Merck/Gilead (peer read) |
| ~Oct 30 | CVX Q3, GD Q3 (GD date unverified) |
| ~Nov 2 | KRYS Q3 |
| to Nov 30 | Atlantic hurricane season (CB) |
| by Dec 31 | KB407 interim, other KRYS readouts; Foundayo/Wegovy pill script trends (weekly) |
| Q1 2027 | LLY retatrutide BLA |

## 7. What would change this report

- Add: a 10-day pullback of the S&P 500 by 8-10% would improve entry prices (start T2/T3 earlier); a US regime flip (S&P 500 below its 200d MA, last read 7,723 vs 7,226 on 2026-09-30 from ENGINE_FINDINGS) means pause all new tranches per the lab's rule.
- Drop: any kill criterion; a new filing contradicting the cited numbers.
- Data gaps (honest): no transcripts read in full; prices/consensus from Yahoo (aggregator); several event dates unverified; GD's September decline unexplained; KRYS net income is from a secondary source; LLY oral-GLP-1 script data is from June 2026 and may be stale; 10-yr yield and Brent levels come from news summaries.

## 8. Sources (accessed 2026-10-14)

- Lilly Q2 2026 8-K: https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000077/q226lillysalesandearningsp.htm
- Fierce Pharma oral GLP-1 tracker: https://www.fiercepharma.com/pharma/oral-glp-1-tracker-launch-trajectories-lilly-foundayo-novo-wegovy-pill
- Chubb Q2 2026 8-K: https://www.sec.gov/Archives/edgar/data/0000896159/000119312526310312/d78544dex991.htm ; Insurance Business Q2 summary; Risk & Insurance property-rate report (Q2 2026)
- Mastercard Q2 2026 8-K: https://www.sec.gov/Archives/edgar/data/0001141391/000114139126000081/ma06302026-exx991xearnings.htm ; call summary https://www.webull.com/news/15364638758544384 ; PaymentsJournal settlement; Constantine Cannon CCCA note
- Chevron Q2 2026 8-K: https://www.sec.gov/Archives/edgar/data/0000093410/000009341026000162/a06302026ex9918-k.htm ; Goldman/EIA/Morgan Stanley oil forecasts via hellenicshippingnews, yahoo finance
- General Dynamics Q2 2026 8-K: https://www.sec.gov/Archives/edgar/data/0000040533/000004053326000029/gd-20260705exhibit991.htm ; marketbeat guidance page
- Krystal Q2 2026 8-K: https://www.sec.gov/Archives/edgar/data/0001711279/000171127926000058/a2q26-ex991xpressrelease.htm
- J&J Q3 2026 8-K (rejected name): https://www.sec.gov/Archives/edgar/data/0000200406/000020040626000189/a2026q3exhibit991.htm ; Merck, Regeneron Q2 2026 releases (rejected names); P&G FY26 Q4 8-K
- Market context: cryptodaily.co.uk (2026-10-07 wrap), lanacion.com.ar (2026-10-05); tax blogs: winvesta.in, angelone.in, vestedfinance.com (2026)
- Internal: reports/ENGINE_FINDINGS.md, reports/OPPORTUNITIES_2026-10-05.md, analysis/stock_ideas/out/*.csv, analysis/stock_ideas/sizing_arithmetic.py
