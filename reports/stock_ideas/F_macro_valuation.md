# F. Macro and market-valuation context for decisions through mid-2027

As of 2026-10-14 (market data to the 2026-10-13 close unless dated otherwise). Research for one investor's staging decisions, not advice; nothing is executed. All probabilities are labelled model estimates. Public file: no personal numbers, only percentages of generic amounts.
Tags: **FACT** (source named), **INFERENCE** (my reasoning from facts), **SPECULATION**, **unverified** (secondary or single-source, or could not be checked). Method files are in the session scratchpad (yfinance, FRED CSVs, NSE archive, multpl, lab engine on tune data only).

## 0. Bottom line

1. **US: a strong tape on a narrow base and an expensive price-based valuation.** S&P 500 7,805 (0.2% below its 6 Oct record, 7.5% above its 200d MA). FactSet forward P/E 19.0-19.1 looks average (5y 19.8, 10y 19.1) but Shiller CAPE is 41.8 (record 44.2, Dec 1999; mean 17.4). Forward earnings yield (~5.25%) is about equal to the 10y Treasury (5.22%). Only 51.8% of S&P stocks are above their own 200d (67.5% in mid-July). FACT, computed.
2. **The rate regime changed:** the Fed hiked on 16 Sep (3.75-4.00%), the dots point to one more, the 10y touched 5.31% (5 Oct), Brent is ~$125 (FRED, 6 Oct). INFERENCE: this, not earnings, is the main risk to multiples through mid-2027.
3. **India is the cheap, stressed market, and the regime filter is verified OFF:** Nifty 500 22,090 vs 200d MA 22,901 (-3.5%); needs +3.7% (+3.2% by the 30 Oct month-end if flat) to flip. Nifty 50 trailing P/E 19.4 is at the 2nd percentile of 133 sampled dates since Oct 2016 (10y median 23.1; sample low 18.7). Smallcaps are not cheap (SC250 P/E 34.4 vs 10y median 32.2).
4. **"Should new money wait for India regime ON?" Not as an absolute gate.** The lab's own results say the filter is a drawdown overlay that costs return (3-7 pp CAGR), does not find winners, and failed in the one narrow-market stress (2018). My new tests: after OFF month-ends, entering immediately beat waiting in about 70-75% of cases but with deeper interim dips (Section 6). Recommendation: treat OFF as a **slow lane** (smaller tranches, individually filtered names), not a stop. Details in Section 6.
5. Probabilities (model estimates, to end-June 2027): US S&P 500 closes at least 10% below today's level at some point ~45%; at least 20% ~18%; higher than today on 30 Jun 2027 ~60%. India Nifty 500 breaks its 30 Mar 2026 low (20,528) ~33%; at least one ON month-end by Dec 2026 ~55%.

## 1. US valuation (dated)

| Metric | Value | Reference | Tag |
|---|---|---|---|
| S&P 500 close | 7,805.45 (2026-10-13); record 7,818.9 (10-06) | 12m +19.1%, YTD +14.0% | FACT yfinance |
| Nasdaq-100 | 30,569 (10-13); record 31,224 (10-06), -2.1% | 12m +26.2%; 200d MA 27,676 (+10.5%) | FACT yfinance |
| SOX (semis) | 12,209, **-16.6% from 22 Jun record**; +15.9% above 200d | 12m +90.5% | FACT yfinance |
| Equal-weight (RSP) | 213.3, -4.3% from 14 Aug record | 12m +15.2% vs cap-weight +19.1% | FACT yfinance |
| Forward 12m P/E (S&P) | 19.0 (FactSet, 2 Oct) / 19.1 (9 Oct); 20.4 on 30 Jun | 5y avg 19.8, 10y avg 19.1 | FACT FactSet |
| Shiller CAPE | 41.84 (2026-10-13) | mean 17.4, median 16.1, max 44.19 (Dec 1999) | FACT multpl |
| Trailing P/E | SPY 24.7, QQQ 28.5 (yfinance, 10-13) | provider definition | unverified |
| Nasdaq-100 forward P/E | not obtained | | unverified |
| Forward earnings yield vs 10y | 1/19.05 = 5.25% vs 10y 5.22% (FRED 10-08; 5.217% on 10-13) | spread ~ +0.03 pp; CAPE yield 2.4% vs 10y TIPS 2.87% (FRED 10-08) | INFERENCE |
| Earnings growth | Q3-26 est. +29.6% (FactSet 9 Oct); CY26 +32.4%, CY27 +15.8% (FactSet 2 Oct, via Forbes) | revisions +1.4% in the quarter vs usual -2.2% | FACT FactSet |

**Why the forward P/E flatters (INFERENCE):** forward EPS jumped on a few AI-hardware names. Macrovisor (8 Oct, paywalled, unverified) says ten companies supply over two-thirds of index EPS growth and Micron plus Nvidia more than one-third; Micron's fiscal Q4 net income was $37.7B vs $3.2B (same source, unverified). yfinance forward P/Es: MU 4.6, NVDA 14.4, AVGO 18.4 (10-13). A low multiple on peak-cycle memory earnings is not the same as a low multiple on normal earnings; the lab's own OPPORTUNITIES note found the same pattern in smaller names (peak-cycle numbers at peak-cycle multiples).

## 2. Fed path and rates (FRED, dated)

| Series | Latest | ~1m ago | ~12m ago |
|---|---|---|---|
| Fed funds effective (DFF) | 3.88% (10-08) | 3.63% | 4.10% |
| 2y / 10y Treasury | 4.75% / 5.22% (10-08) | 4.39% / 4.80% | 3.58% / 4.13% |
| 10y real (TIPS) | 2.87% | 2.43% | 1.78% |
| 10y breakeven | 2.33% | 2.37% | 2.34% |
| HY option-adjusted spread | 3.11% (10-12) | 2.65% | 3.18% |
| VIX | 15.2 (10-12) | 15.8 | 21.7 |
| Brent | $125.4 (10-06); 2026 high $138.2 (7 Apr); low ~$70 late Jun | $102 | $67 |
| CPI all-items YoY (my calc, SA index, Aug) | 3.7% (core 2.8%; core PCE 3.0%) | | |
| Unemployment (Sep) | 4.2%; payrolls 3m avg ~+51k (noisy) | | |

- FACT (secondary: Chase, JPM, Advisor Perspectives, 16 Sep): the FOMC raised 25 bp to 3.75-4.00%, 12-0, the first hike since 2023 (Chair Warsh). The median dot shows one more 25 bp hike in 2026; four participants see two; 2027 views are dispersed (cuts to more hikes). Markets price one more hike in December (sources differ on exact range 4.00-4.25% vs 4.1-4.4%).
- A discrepancy: an aggregator quotes Aug CPI at 3.4% YoY; my calculation from the FRED SA index gives 3.7%. Treat the level as **unverified** to ±0.3 pp; the direction (energy-led, core ~2.8%) is not in doubt.
- Fed calendar (federalreserve.gov): **27-28 Oct** (no projections), **8-9 Dec** (projections), 2027: 26-27 Jan, 16-17 Mar, 27-28 Apr, 8-9 Jun (tentative).
- INFERENCE: with the 10y real yield up ~110 bp in a year, long-duration equity (CAPE 41.8) is the sensitive part. A hiking Fed with oil at $125 is the opposite of the 2024-25 "cuts ahead" backdrop that carried multiples.

## 3. AI-capex cycle: evidence and risk

| For the cycle (FACT unless noted) | Against / fragility |
|---|---|
| 2026 hyperscaler capex ~$690B cash, +80% YoY (FactSet 23 Jul); FT tally ~$725B for four; ~$800B incl. leases and prepayments | FCF "close to zero or negative" in FY26 for all but Alphabet and Microsoft (FactSet 23 Jul) |
| Alphabet guide $180-190B, Meta $125-145B (raised in Q1); Alphabet flagged higher 2027 | Debt funded 9% of capex in FY24, 32% LTM; ~$700B debt; ~$820B off-balance lease commitments (FactSet) |
| Record 72 companies guided Q3 EPS positively, 44 in tech (Macrovisor, unverified); 62% of guiders positive (FactSet 2 Oct) | Alphabet raised $84.75B equity (Jun); S&P cut Oracle to BBB- (9 Jul); Oracle capex ~86% of sales (CreditSights, secondary) |
| Micron blow-out (reported 30 Sep); Nvidia reports 19 Nov | PP&E bought $434B vs ~$149B depreciation, LTM Mar-26 (secondary): depreciation wall; GPU useful-life 5-6y vs 3-4y scenario |
| >65% of S&P Q2 calls cited "AI" (FactSet 18 Sep) | Customer concentration (OpenAI, Anthropic); hyperscaler shares lagged the S&P over 12m while chips and power rose (FactSet) |

INFERENCE: demand evidence is strong and visible in supplier earnings; the fragility is financing (debt, equity, leases) and the rate level. SOX is 16.6% below its June high despite the earnings surge: the market may already be discounting a peak in the growth rate (SPECULATION). **What breaks the cycle fastest** is not a demand miss but a funding event: an Oracle downgrade to junk, a failed large AI-lab financing, a capex cut by one hyperscaler with a punishing share reaction, or the 10y holding above 5.5%.

## 4. Breadth and concentration

| Measure (S&P 500, computed 2026-10-13 from 500 constituents, current membership) | Value |
|---|---|
| % of stocks above own 200d MA | **51.8%** (59.8% on 14 Sep; 67.5% on 15 Jul; 59.0% a year ago) |
| % above 50d MA | 39.6% |
| % within 5% of their 52w high / more than 20% below it | 15.4% / 33.0% |
| Median stock 12m return vs index | +10.9% vs +19.1%; only 38% of stocks beat the index |
| Top-10 weight | ~39% (Slickcharts via search, 10 Oct, secondary); record ~40.7% end-2025; ~37% SPY on 11 Jun; dot-com peak ~26% (Morgan Stanley via Walnut). Top 10 earn ~32% of earnings (end-2025 estimate, secondary) |

INFERENCE: new highs with half the stocks under their 200d is the same shape the lab's skeptic report flagged for India in 2018 (index above its MA, breadth collapsing, filter blind). The lab's US regime filter watches only the index, so US "ON" today is weaker information than it looks. Macrovisor's claim of "weakest breadth since the dot-com bubble" is unverified.

## 5. Drawdown base rates from this valuation level (computed; S&P 500 price index 1927-2026 via yfinance, CAPE monthly 1871-2026 via multpl)

Price returns exclude dividends (~1.1%/yr). "Worst close vs entry" is the lowest close in the window relative to the entry level (what a buyer actually experiences).

| Entry condition | n months | P(worst close <= -10%) 12m | P(<= -20%) 12m | P(<= -20%) 24m | 12m return mean / median |
|---|---|---|---|---|---|
| All months since 1928 | 1,186 | 37% | 17% | 25% | +8.2% / +9.9% |
| Within 2% of all-time high | 275 | 25% | 11% | 18% | +8.4% / +8.8% |
| Within 2% of ATH, since 1990 | 158 | 22% | 7% | 12% | +10.2% / +11.5% |
| CAPE 25-30 | 146 | 29% | 17% | 26% | +8.9% / +10.1% |
| CAPE 30-35 | 65 | 51% | 25% | 32% | +8.6% / +11.7% |
| **CAPE >= 35** (today 41.8) | 72 (61 with 12m data) | 52% | 25% | 45% | +3.8% / +10.7% |
| CAPE >= 38 | 39 | 48% | 34% | 63% | -0.9% / +4.5% |

- **Reading (INFERENCE):** high CAPE does not predict the next 12 months well (median still +10.7%), but it widens the left tail: at CAPE >= 35 roughly 1 in 4 entries sat 20% under water at some point within a year and nearly half within two years.
- **Honest limit:** CAPE >= 35 consists of only ~3 independent episodes (1998-2001, 2021-22, 2024-26); the dot-com run dominates the 24-36m figures. The 2024-26 months so far were positive (12m +15.7% mean for 2024 entries). Treat the CAPE rows as a warning on tail width, not as a forecast.
- Intra-year peak-to-trough in the S&P was at least 10% in 61 of 100 calendar years (19 of 37 since 1990); 2025 saw -18.9% and 2026 so far -9.1%. Ordinary pullbacks of 10% are common and should not by themselves break a staging plan.
- Recent episode depths (close-to-close, yfinance): S&P -53% (2008), -34% (2020), -25% (2022), -19% (2025); Nasdaq-100 -50/-28/-36/-23%; SOX -59/-35/-47/-35%.

## 6. Earnings and event calendar

| Date | Event | Source / status |
|---|---|---|
| 14 Oct | US Sept CPI; ASML Q3 | BLS date via aggregators; ASML via aggregator (verify) |
| 15 Oct | TSMC Q3 call (14:00 Taiwan) | TSMC IR (FACT) |
| wk of 12 Oct, 26-30 Oct | ~7% of S&P market cap reports wk of 12 Oct; ~44% wk of 26-30 Oct; ~70% by end-Oct | Macrovisor (unverified) |
| **27-28 Oct** | FOMC | federalreserve.gov (FACT) |
| 28 Oct | Alphabet, Microsoft (confirmed per Signalstack citing IR); Meta ~28 Oct and Amazon ~29 Oct are **estimates** | verify on IR pages |
| 2 Nov | Apple FQ4 | Signalstack citing IR |
| **3 Nov** | US midterm elections (policy-change risk named by Macrovisor) | calendar fact |
| ~6 Nov | October jobs report | typical BLS timing, unverified |
| **19 Nov** | Nvidia | Macrovisor (verify) |
| 8-9 Dec | FOMC with new dots | federalreserve.gov |
| Jan-Feb 2027 | Q4 prints; hyperscaler 2027 capex guides | SPECULATION on timing |

Q3 season expectation: FactSet est. +29.6% growth on revenue +12.3%; FactSet says the final figure "likely above 35%" because beats usually lift the number. INFERENCE: with a Fed hiking, the stock reaction to beats may matter more than the beats (Meta fell ~9% after Q1 despite growth).

## 7. India

### 7.1 Is the regime filter really OFF, and why? (verified)

- FACT (yfinance ^CRSLDX, my calc): Nifty 500 **22,090 vs 200d MA 22,900.9 (-3.5%)** on 13 Oct. The lab's 30 Sep figures reproduce exactly (22,072 vs MA 22,966). Daily state flipped OFF on **9 Sep**; at month-ends: OFF 31 Jan-30 Jun, ON 31 Jul-31 Aug, OFF 30 Sep. There were **17 daily flips since 20 Jan**, i.e. the filter whipsawed this year.
- To flip ON: +3.7% now; if the index is flat on 30 Oct the MA drifts to ~22,797 (+3.2% needed). Model estimate from a block-bootstrap of Nifty 500 returns (no skill, 20,000 paths): P(ON on 30 Oct) ~20%; P(at least one ON month-end by Dec 2026) ~52-63%; by Mar 2027 ~69-81%; by Jun 2027 ~82-92% (range = zero vs historical drift).
- Why it fell (FACT from news, secondary: Stockedge/TradingView/Trading Economics, 7-13 Oct): oil shock (Brent crossed $100 on 9 Sep; import bill $63.4B Apr-Jul vs $40.5B), rupee ~95-97, FPIs selling 11 straight sessions to 9 Oct, global yields up, RBI hike. Nifty 50 closed 22,232 on 8 Oct, lowest close in ~18 months; September: IT -11.2%, autos -8.8%, Midcap-100 -7.6%.
- Price context (yfinance): Nifty 50 22,722, **-13.7% from 2 Jan record**, YTD -13.0% vs S&P +14.0%; Nifty 500 -8.3% from its 2 Jan high; Midcap-150 -7.3% from 13 Aug, 1.7% under its 200d; Smallcap-250 +5.2% above its 200d and 4.3% under its 2024 peak (so smallcaps held up better, helped by domestic inflows). Nifty 50 in USD terms: -15.5% over 12m. India VIX 14.1 (calm for a -14% market).
- Breadth (my calc, 9 Oct, only 318 of 500 names have 200d history): 34.3% above their 200d (55.7% on 8 Sep), 17.3% above 50d, 5.0% within 5% of 52w high, 53.5% more than 20% below it. Few individual stocks pass the lab's entry filters at present.

### 7.2 Valuations vs own history (NSE index P/E archive, 135 sampled dates Sep 2016-13 Oct 2026; medians because 2020 earnings collapse inflates means)

| Index | P/E now | 10y median | vs median | P/B now vs median | Div yield |
|---|---|---|---|---|---|
| Nifty 50 | 19.4 | 23.1 | **-16%** (2nd percentile; low of 18.7) | 2.79 vs 3.56 | 1.5% |
| Nifty 500 | 21.8 | 26.2 | -17% | 3.10 vs 3.56 | 1.3% |
| Nifty Next 50 | 18.1 | 26.2 | -31% | 3.31 vs 3.83 | 1.5% |
| Midcap-150 | 28.3 | 33.5 | -15% | 3.82 vs 3.56 (+7%) | 1.0% |
| Smallcap-250 | 34.4 | 32.2 (since Apr-17) | **+7%** | 3.43 vs 3.12 | 0.75% |
| Smallcap-100 | 37.9 | 30.8 (since Apr-18) | **+23%** | 3.77 vs 3.48 | 0.6% |

- INFERENCE: large caps are cheap on trailing earnings against their own decade, mid caps are around fair on P/E (but above median on P/B), small caps are the expensive segment: SC250/Nifty-50 P/E ratio 1.77x vs a 1.29x median. The 8-Oct-2026 NSE file shows Midcap-150 27.7 and Smallcap-250 33.9 (the 13-Oct values are in the table).
- Forward: Nifty 50 FY27 EPS Rs 1,227, FY28 Rs 1,398 (Kotak, quoted by Business Standard 8 Oct, secondary) imply ~18.5x and ~16.3x at 22,722. Most brokerages see FY27 Nifty profit growth 14-15%; Elara 11%; BofA cut to 8.5% (older, crude-driven) (secondary).
- Earnings yield (trailing 5.2%, FY27E 5.4%) is ~1.8 pp **below** the 10y G-sec at ~7.23% (Trading Economics, 7 Oct): equities are not cheap against bonds, only against their own history.

### 7.3 Flows, rates, rupee

| Item | Reading | Tag |
|---|---|---|
| FPI equity, 13 Oct provisional | FII net -Rs 1,305 cr; DII +Rs 2,439 cr (NSE API, fetched 13 Oct) | FACT |
| FPI equity fortnightly net (NSDL, parsed by a scratchpad script; June fortnights missing) | Jan-May about -Rs 2.25 lakh cr (peak outflow Mar -52,704 / -65,071 per fortnight); Jul-Aug about +Rs 0.50 lakh cr; Sep about -Rs 0.36 lakh cr; FPI equity AUC ~$803bn (15 Jan) to ~$689bn (30 Sep) | unverified parse |
| Domestic | SIP record Rs 32,490 cr (Sep); equity-fund inflows Rs 38,307 cr, small-cap funds Rs 9,039 cr (AMFI via Statesman/Upstox); DII bought Rs 4,597 cr on 7 Oct | FACT (secondary) |
| RBI | Repo **raised 25 bp to 5.50% on 7 Oct** (first hike since Feb 2023), stance to "calibrated tightening", cuts "off the table near term"; FY27 GDP 7.1%, CPI 5.2%; Aug CPI 4.8% | secondary (Business Standard, SCC Online, Trading Economics); verify on rbi.org.in |
| Next MPC | **2-4 Dec 2026**, then 3-5 Feb 2027 | 5paisa schedule (verify) |
| USD/INR | ~95.0-96.3 (95.0 on 14 Oct; FRED 96.31 on 2 Oct; 2026 FRED high 96.82 on 20 May; press says >97 on 8 Oct, unverified) | FACT |
| INR trend | 12m depreciation ~7.9%; 5y ~4.9%/yr; 10y ~3.7%/yr (yfinance). RBI curbed OMC dollar demand and tightened FX-derivative norms (press, 12 Oct) | FACT/secondary |

INFERENCE: the four India stressors (oil, INR, FPI selling, higher global and domestic yields) feed each other. A durable bottom more likely needs oil to ease or INR to stabilise than a cheap P/E. For a rupee investor, a weaker INR cushions US holdings, but it also makes new US purchases dearer in rupees (neutral in expectation; not a timing tool).

### 7.4 Q2 FY27 results season (Oct to mid-Nov)

- TCS reported 8 Oct: revenue Rs 73,188 cr (+1.3% QoQ, +11.2% YoY), profit ~Rs 13,884 cr, margin ~24% (secondary; sources differ); stock +5% on 9 Oct. Season runs to the SEBI 45-day deadline, **about 14 Nov** (INFERENCE from the listing rule; verify). Individual dates for Infosys, banks, Reliance not verified.
- Preview: Nifty-50 profit +27% YoY (Motilal Oswal; highest in 17 quarters), Kotak +21%, "about 23%" in another review. Drivers: low crude in Jul-Aug, metals, banks, export autos, **a low base** (Sep-2025 quarter). Risks named: crude hits Q3 P&L fully, margin squeeze in FMCG, passenger vehicles, cement, chemicals; weak rural demand (rainfall); momentum expected to moderate in H2 (all secondary).
- INFERENCE: a strong headline Q2 growth number is largely base effect and is unlikely to be the market catalyst; the guidance on H2 margins and crude pass-through is.

### 7.5 Upcoming India events

30 Oct (month-end regime check; the lab's paper books take their first signal on 30 Oct), Q2 results to ~14 Nov, RBI 2-4 Dec, US FOMC 28 Oct and 9 Dec, Union Budget around 1 Feb 2027 (customary date, unverified), RBI 3-5 Feb 2027, Q3 results Jan-Feb 2027.

## 8. "Should new money wait for India regime ON?" using the lab's own results

### 8.1 What the lab's reports say (all survivor-inflated, price-only, 2010-2018 tune unless noted)

| Source | Finding on the regime filter (Nifty 500 > 200d MA, month-end) |
|---|---|
| ENGINE_FINDINGS section 2 (India) | Regime + filters + mom/vol rank: 25.8% CAGR / -19.7% max DD; **without regime 29.5% / -24.3%**. Random 25 with filters: 15.0% / -23.6% (regime) vs 18.0% / -27.1% (none). "Index regime filter cuts a few more points of drawdown at a cost of about 3-4 pts of CAGR." |
| ENGINE_FINDINGS (US) | Regime on 16.2% / -20.8% vs off 18.7% / -28.4% |
| 1_backtester (144-cell grid, Nifty 50 filter) | Regime costs ~7 pts CAGR (26.0% vs 32.9%) and buys ~4 pts of max DD (-27.3% vs -31.1%) |
| 3_risk_manager | Regime does not cut the tail that mattered: 2018 the book was 100% invested at peak and trough (Nifty stayed above its MA while mid/small caps fell 34%); MDD -34.4% on vs -33.9% off |
| 5_skeptic | Filter ON 69% of months, 19 flips; Nifty itself returned +1.64%/month in OFF months, so OFF was not defensive; costs 6 pp CAGR; breadth collapsing while index above MA is the invisible failure |
| FINAL (sealed 2019-2026, filter on, Nifty 500) | 34.3% CAGR / -25.3% DD, 2025 flat, Jan-2025 -17.1%: "drawdown protection comes mostly from the regime filter and cash" (note the tension with the risk manager's earlier Nifty-50 version) |
| Lab verdicts | Filters protect but do not find multi-baggers; momentum rank is the only selector with edge; timing states carry no return edge; never tested in a prolonged bear market (2008 outside window) |

### 8.2 New tests run for this report

**(a) Index level, Nifty 500 price, month-end rule, 2006-2026 (includes 2008 and 2020; overlapping 12m windows, about 17 OFF spells, so effective sample is small).**

| Start state | n | 12m fwd mean / median | P(<0) | P(worst close vs entry <= -20%) |
|---|---|---|---|---|
| OFF | 65 | +21.5% / +11.3% | 17% | 22% |
| ON | 164 | +9.9% / +7.3% | 29% | 12% |
| OFF and within 6% of MA (like today, 3.9%) | 39 | +11.1% / +7.7% | 23% | 20% |
| ...of which 2006-2012 (incl. 2008) | 10 | **-4.8% / -7.8%** | 70% | 57% |
| ...of which 2013-2018 | 16 | +17.3% / +11.1% | 0% | 0% |

Waiting for the next ON month-end (cash at 6% meanwhile) vs investing at an OFF month-end: wait mean 19.7% vs invest 21.5%; waiting won 32% of the time. For OFF-near-MA starts: wait 11.3% vs now 11.1% (no edge either way). Waiting won 56% of the time in 2006-2012 (80% for the near-MA starts, which is only about three episodes incl. 2008) and only 25% and 6% in 2013-2018 and 2019-2026.
Analogues (hand-picked, illustrative): OFF month-ends Sep-2013 (+46% 12m), Oct-2018 (+11%), Jun-2022 (+23%), Aug-2015 (+12%); but Jun-2008 and Aug-2011 started 38.6% and 12.2% under water within 12 months before recovering.
For comparison, the **S&P 500** regime (2000-2026): OFF months had P(<= -20% from entry within 12m) = 39% vs 8% for ON; 12m mean 5.4% vs 10.1%. The US filter separates the crash tail much better than the India one did.

**(b) The lab's own engine** (frozen rule: top 25 by mom/vol, 30% stop, 25 bp costs, 6% cash; tune data only, starts at each month-end Jan 2010-Dec 2017; 12-month outcomes; survivor-inflated upper bounds, read the differences):

| Start at an OFF month-end (n=28; ~6 episodes) | 12m return mean / median | P(<0) | Max DD inside the 12m: mean / worst | P(DD worse than -20%) |
|---|---|---|---|---|
| Enter now, regime ignored | +35.1% / +21.8% | 4% | -15.1% / -24.0% | **18%** |
| Wait for ON (cash at 6% until then) | +28.1% / +16.1% | 0% | -7.1% / -18.6% | 0% |
| Nifty 500 index from same date | +14.4% / +12.8% | 21% | -15.3% / -25.1% | 25% |

"Enter now" beat "wait" in 75% of OFF starts by 7.1 pp on average, but with about 8 pp deeper interim drawdown and an 18% chance of breaching the investor's 20-25% loss limit. Waiting won mainly for the Aug-Dec 2015 starts. From ON starts, "enter now" 34.8% vs wait 31.1%, with P(DD worse than -20%) 22% vs 0%: the filter buys drawdown limits mostly by sitting in cash, not by entry timing.
Caveats: 2018 starts (the failure year) cannot be shown (12m window beyond tune); six overlapping episodes; survivor-biased universe; the sealed 2019+ window was not touched.

### 8.3 Answer

- **INFERENCE:** the regime filter is a risk-budget tool, not an alpha tool. It reduced interim drawdown in the lab's tests and cost return. It is therefore consistent with the investor's 20-25% loss limit if used to **slow** deployment, and not justified as a rule that new money must sit idle. Waiting for ON forgoes about 7 pp (mean) in the lab's engine and ~2 pp at index level; it protects mainly in crash-type OFF episodes (2008) that the lab never tested.
- **What differs today:** OFF is shallow (-3.5%), valuations are at a 10-year low for large caps, but the macro triggers (oil, INR, Fed and RBI hiking, FPI selling) resemble stress regimes, breadth is weak (34% above 200d), and the filter's 2026 record is mixed (it held cash at 7 of the 9 month-ends of 2026 while Nifty 500 fell 7.5% YTD, so it has helped this year, yet the daily state flipped 17 times).
- **Practical stance (staging, not advice):** (1) keep the lab's frozen India rule as the benchmark: cash until a month-end ON. (2) If the investor chooses to start before ON, cap the pre-ON slice at about one third of the intended India direct-stock allocation, in at most two tranches, only names that individually pass the lab's filters (above own 200d, within 25% of 52w high; 165 passed on 30 Sep) and are not already among the AI-hardware names dominating existing exposure. (3) Release the remaining tranches only on a month-end ON or on the pause-clear triggers below. (4) Do not hold back diversified index or fund contributions on this filter; the lab's evidence concerns a concentrated stock-picking sleeve.
- **Model estimate:** P(entering one third now ends with a drawdown beyond -20% on that slice within 12 months) ~20-25% (lab OFF-start 18%, index 25%, uplifted for survivor bias and the stressed macro); P(waiting costs more than 5 pp of 12m return vs entering now) ~40% (lab engine: 54% of OFF starts, waiting gained more than 5 pp in 18%; discounted for survivor bias).

## 9. Scenario map through end-June 2027 (model estimates; they sum to 100% per market)

### 9.1 US

| Scenario | P | Shape | Confirming observations | Staging action |
|---|---|---|---|---|
| **Base: choppy grind** | 50% | S&P between -12% and +10% of today; one or two 5-10% pullbacks; one more Fed hike then hold; Q3 beats absorbed | 10y 4.8-5.4%, HY OAS < 4%, VIX 14-24, S&P above 200d at most month-ends, breadth 45-60% | Normal pace: equal tranches at calendar anchors (30 Oct, 20 Nov, 10 Dec), skip none; add on 8-10% pullbacks while above 200d |
| **Bull: broadening** | 22% | S&P +10 to +20%; oil falls, yields back under 4.8%, Fed pauses, breadth recovers | 10y < 4.8%, % above 200d > 65%, RSP outperforming, Q3 growth > 30% with positive reaction | Speed up: compress remaining tranches to two-week spacing, but keep the sizing caps in Section 10 |
| **Bear: rates or AI-funding shock** | 28% | S&P closes at least 15% below today's level at some point (≥20% ~18%, ≥30% ~5%); semis -35 to -50%; Nasdaq-100 -25 to -35% | 10y > 5.5% sustained; HY OAS > 4.0%; S&P month-end close below 200d (7,260 today, rising); a hyperscaler capex cut or FCF/credit event; Nvidia 19 Nov guide shortfall; Fed signals > 4.5% end-2026 | Pause: freeze new tranches; resume only after S&P regains 200d at a month-end, or after a -20% drawdown with HY OAS stable (not widening) and 10y falling |

### 9.2 India

| Scenario | P | Shape | Confirming observations | Staging action |
|---|---|---|---|---|
| **Base: range and basing** | 45% | Nifty 500 within 20,500-23,500; regime flips ON for at least one month-end by Dec-Feb; Q2 prints fine, H2 guidance cautious | Brent $95-125, USD/INR 94-97, FPI flows mixed, RBI holds on 4 Dec | Slow lane: at most one third of the intended slice before an ON month-end, then the rest in two tranches after ON |
| **Bull: relief** | 22% | Nifty 500 +12-25% (25,000-27,000) by mid-2027; large caps re-rate toward 22x | Brent < $90, USD/INR < 94, 3+ days of FPI net buying then positive weeks, breadth > 50%, Nifty 500 month-end > 200d | Speed up: ON month-end releases remaining tranches monthly; add to leaders on 5-8% dips above own 200d |
| **Bear: stress deepens** | 33% | Nifty 500 breaks the 20,528 low (30 Mar 2026), -10 to -20% from here; mid/small caps -20 to -35%; FY27 EPS cuts | Brent > $130, USD/INR > 98-100, second RBI hike on 4 Dec, 10y G-sec > 7.5%, FY27 EPS cuts > 5%, FPI selling > 15 straight sessions | Pause stock tranches; hold cash; reassess only on (a) a month-end ON or (b) a washed-out signal: Nifty 500 down > 15% from today with FPI selling reversing and oil falling |

Note: India's bear weight (33%) is judgement: it starts from the 22% frequency of a -20% worst close after OFF index starts (8.2a) and adds weight for the oil, INR and hiking-cycle mix; it is not computed. Probability the Nifty 500 trades below its 2026 low before end-June 2027: ~33% (model estimate).

### 9.3 Trigger dashboard (current reading, so the distance is visible)

| Trigger | Now | Pause if | Speed up if |
|---|---|---|---|
| S&P 500 vs 200d MA (month-end) | +7.5% (7,805 vs 7,260) | month-end close under 200d | pullback of 8-12% that holds the 200d |
| US 10y yield | 5.22% (5.31% on 5 Oct) | > 5.5% for a week | < 4.9% |
| HY OAS | 3.11% (2.65% a month ago) | > 4.0% | stays < 3.5% while 10y falls |
| S&P breadth (% above 200d) | 51.8% | < 40% with index near highs | > 65% |
| SOX vs 200d | +15.9% (-16.6% from high) | closes under 200d (10,533) | reclaims high |
| Fed | hiked 16 Sep; 28 Oct and 9 Dec | dots imply > 4.5% end-26 or hikes in 2027 | dots flat for 2027 |
| AI financing | Oracle BBB-; FCF ~0 | downgrade to junk or failed raise or capex cut | Q3 capex guides intact with FCF stabilising |
| Nifty 500 vs 200d (month-end) | -3.5% | stays OFF (no stock tranches beyond the slow-lane slice) | ON at a month-end |
| Brent (FRED) / USD-INR | $125 / ~95-96 | > $130 / > 98 | < $95 / < 94 |
| FPI flow (daily provisional) | 11-session selling streak to 9 Oct; 13 Oct -Rs 1,305 cr | > 15 sessions | 3+ net-buy sessions in a row |
| Nifty 500 breadth (% above 200d) | 34% (9 Oct, n=318) | < 25% | > 50% |
| RBI / India 10y | repo 5.50%; 10y ~7.23% | second hike or 10y > 7.5% | pause plus 10y < 7.0% |
| Q2 FY27 results | preview +21-27% Nifty-50 | actual < 15% or FY27 EPS cuts > 5% | in line plus stable H2 margin guides |

Pace ladder used above: **fast** = tranche every 2 weeks; **normal** = monthly; **slow lane** = half-size tranche every 6-8 weeks; **pause** = none. Lab evidence tempers these rules: trend and regime filters protect but do not select winners; timing states carry no return edge; none of the thresholds above was validated by backtest (they are judgement anchored to the data shown).

## 10. Sizing guardrails tied to the investor's 20-25% loss limit

Share of a new-money sleeve that can sit in an asset with stress drawdown d if the sleeve may lose L = 22.5% (rest in cash at 0%): share = L / d. FACT arithmetic (analysis/stock_ideas/sizing_arithmetic.py logic).

| Stress drawdown d | 25% | 30% | 40% | 50% | 60% | 70% |
|---|---|---|---|---|---|---|
| Max share of sleeve | 90% | 75% | 56% | 45% | 38% | 32% |

Loss in percentage points of net worth = weight (% of net worth) x drawdown. Examples per 1% of net worth: S&P-like (-34%, 2020) 0.34 pp; Nasdaq-100 bear (-36%) 0.36 pp; semiconductor name (-65%) 0.65 pp; Nifty 50 (-38% in 2020) 0.38 pp; Midcap (-37% to -72% in 2020 / 2008) 0.37-0.72 pp. A 5% position in a semis-type name at -65% costs 3.3 pp; a 10% position in Indian mid/small stocks at -40% costs 4 pp.

## 11. What I could not verify, and tax or rule flags

- Not obtained: Nasdaq-100 forward P/E, an official S&P top-10 weight (S&P DJI), US consensus for 2027 EPS beyond FactSet's CY27 +15.8% (via Forbes), official dates for Amazon, Meta, Nvidia, Infosys and bank results, the India 10y yield after 7 Oct, Nifty Smallcap-250 history before Apr 2017, and India Q2 GDP / Union Budget dates.
- Secondary sources (news summaries, aggregators) carry the RBI details, FOMC dots, hyperscaler capex trackers and Macrovisor claims; verify on rbi.org.in, federalreserve.gov, company IR pages before acting.
- The lab's results are survivor-inflated and price-only; the engine test in 8.2b uses tune data (2010-2018) only and cannot show the 2018 stress or any crash.
- Taxes (not verified here, verify with a CA): India-resident gains on US shares versus Indian shares are taxed differently, remittance rules (LRS and TCS) and employer-stock blackout rules may constrain timing; none of the staging dates above account for them.
- Never read from private/; no personal data used.
