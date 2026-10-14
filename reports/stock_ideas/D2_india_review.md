# D2. Independent adversarial review of D (India ideas), as of 2026-10-14

Reviewer stance: try to kill each idea. Research, not advice; nothing executed. Public file, no personal portfolio numbers. Tags: FACT (primary filing or dated market data I pulled myself), INFERENCE, SPECULATION, unverified. Probabilities are labelled model estimates.
Method: NSE filings downloaded and read (HCLTech investor release, Hero/Bajaj/SBI/Sun/HAL filings, Sun's CRISIL rating rationale of 13-Oct, NSE board-meeting and corporate-action feeds), live yfinance prices to the 2026-10-14 close, lab screen data (`scratchpad/w/scored.pkl`, 417 Nifty 500 names with turnover of Rs 15 cr/day or more), 3-year return regressions for the macro-fit test.

## 0. Verdicts

| Idea | D's tier | Verdict | One-line reason |
|---|---|---|---|
| Bajaj Auto | 1, start now | **CONFIRM (best of six), start moved to after the 27-Oct print** | Only name with upper-quintile momentum (80th pct); D omitted the Rs 5,633 cr buyback at Rs 12,000 and the KTM kill trigger is mis-specified |
| HCLTech | 1, start now | **DOWNGRADE to Tier 3 / small** | 34th-pct momentum, entry zone is after a 14% four-day bounce, 2.6% constant-currency growth at the bottom of its own guide, no price-level rupee hedge in 3 years of data |
| Hero MotoCorp | 2 | **KILL as a start candidate (monitor)** | 43rd-pct momentum, fails the lab's trend filter, P/E above its own median, D missed about Rs 2,700 cr committed to loss-making associate Ather in six weeks |
| SBI | 2 | **CONFIRM as Tier 2 with a corrected gate** | Cheapest, 67th-pct momentum; but Q2 profit will carry a one-off SBI Funds gain and a bank strike is noticed from 26-Oct, so the "buy after the Q2 print" rule would trigger on a distorted number |
| Sun Pharma | 3 | **DOWNGRADE (park, no entry plan)** | Operating profit grew 2.7% (not the headline 27% PAT); US formulations -10%; 34.8x; lab says avoid the sector. Leverage worry is overstated: CRISIL/ICRA AAA, 1.5-2.0x |
| HAL | 3 | **CONFIRM as watch only** | Passes the lab's trend filter (+10.7% over 200d) but 34x trailing, beta 1.7, 51st-pct momentum; wait for a pullback and Q2 |

Start first: **Bajaj Auto only**, after the 27-Oct result and the 30-Oct month-end check, one third of a reduced cap. Everything else waits for regime ON or a stock-specific trigger (section 5).

## 1. Facts I re-verified, and what D missed

### 1.1 Bajaj Auto
| Item | D says | Primary-source check | Status |
|---|---|---|---|
| Q1 FY27 standalone revenue / PAT | Rs 17,244 cr / Rs 2,983 cr (+42%) | Filing: Rs 17,243.72 cr / Rs 2,982.84 cr vs Rs 2,095.98 cr | FACT, confirmed |
| Standalone EBITDA margin | 20.9% | PBT 3,985 less other income 512 plus finance 4 plus depreciation 118 = Rs 3,595 cr = 20.8% | FACT, confirmed (rounding) |
| Sep-26 sales | domestic 2W -12%, exports +34% | Company sheet: domestic 2W -12%, exports 2W +34%, total +5%; H1: exports +47%, domestic 2W +6% | FACT, confirmed |
| KTM | EBIT +EUR 1.3 mn in Q2 2026, FCF -22 mn H1, equity ratio 21.5% | Ad hoc release: confirmed. Note H1 EBIT is still EUR -24.8 mn and EBITDA margin 5.4% | FACT, confirmed |
| Q2 date | 27-Oct | NSE board-meeting feed: 27-Oct-2026 | FACT, confirmed |
| Buyback | **not mentioned** | Board approved 6-May-2026: up to 46.94 lakh shares (1.68%) at **Rs 12,000**, Rs 5,633 cr; closed and extinguished 24-Jul-2026 (NSE) | FACT, **missed by D** |
| Price | Rs 10,370 | Rs 10,336 (14-Oct); 200d MA 10,242; 50d 11,349 | FACT |
| P/E | 27x standalone | 26.5x standalone on Rs 390 TTM; 23.9x consolidated (Yahoo EPS 432) | confirmed with both bases |

What the buyback changes (INFERENCE): the stock traded above Rs 12,000 in June-September (peak close 12,361 on 1-Sep) and is now 16% below that peak and 14% below the buyback price. About 2% of market value was returned in cash in July, so part of the free-cash-flow "support" in D's thesis is already spent. The share count is 1.68% lower, which lifts standalone per-share figures slightly.
Price path: 12,361 (1-Sep) to 9,637 (8-Oct) is -22%; the 1-Oct and 5-Oct sessions alone took off about 8% after the September sales print (domestic -12%). The 12-1 momentum rank ignores the last month, so the 80th percentile does not show this fall.

### 1.2 HCLTech
| Item | D says | Check | Status |
|---|---|---|---|
| Revenue / net income | Rs 35,620 cr (+11.5%) / Rs 5,132 cr (+21%) | Release: +11.5% y/y, Rs 5,132 cr, +21.2% y/y, +11.0% q/q | confirmed |
| Dollar growth | +2.2%; CC +2.6% y/y | Release: $3,724 mn, +2.2% y/y, CC +2.6% y/y, +2.3% q/q CC | confirmed |
| Guidance | raised to 2.5-4.0% | Release: company CC growth 2.5-4.0%, services 3.0-4.0%, **EBIT margin 17.5-18.5%** | confirmed. Q2 y/y CC 2.6% sits at the **bottom** of the guide |
| Restructuring | 55, 81, 122, 62, 84 bp | Footnotes match exactly; Q3 FY26 also had a separate Rs 956 cr EBIT labour-code charge | confirmed |
| Bookings | $3.26 bn, +27% | confirmed | |
| Net cash | Rs 24,503 cr vs 33,288 in March | confirmed (Gross cash 25,457, borrowings 954) | |
| Dividend | Rs 12 interim, record 16-Oct | NSE: record date and ex-date both 16-Oct-2026 | confirmed |
| Not mentioned | | HCLSoftware revenue **-11.2% y/y CC**, Engineering & R&D EBIT 15.2% (down 231 bp y/y), Europe -0.3% CC; Yahoo mean analyst target Rs 1,270 (below the price; may predate the results) | missed |
| P/E | "~20x" | 1,342 / 70.2 company LTM EPS = 19.1x; about 18.4x if the one-off labour-code hit (Rs 719 cr, INFERENCE) is added back. D's own entry grid mislabels multiples (section 3) | corrected |

Price path: 1,177 (8-Oct) to 1,339 (14-Oct) is +14% in four sessions, of which +8.4% on 13-Oct alone. D's table (-27% from high, -7% vs 200d, 38th pct) uses the pre-result close; today HCLTech is -22% from its high and +0.3% over its 200d, momentum percentile 34.

### 1.3 Hero MotoCorp
| Item | D says | Check | Status |
|---|---|---|---|
| Q1 standalone | revenue Rs 12,999 cr (+36%), PAT Rs 1,454 cr (+29%), EBITDA 13.3% vs 14.4% | confirmed from the press release (EBITDA 1,727 / 12,999) | confirmed |
| Consolidated -17% | base effect of Rs 722 cr one-off | confirmed (PAT 1,418 vs 1,706; one-time gain on associate dilution) | confirmed |
| Sep dispatches | 766,348 (+12%), VAHAN +31% | confirmed, release says VAHAN data exclude Telangana | confirmed |
| Q2 date | 28-Oct | NSE feed: 28-Oct-2026 (Yahoo's calendar shows 12-Nov, which is an estimate) | confirmed |
| Ather | **not mentioned** | 14/15-Jul: up to Rs 1,000 cr via warrants (76.2 lakh at Rs 1,260, Rs 960 cr); 27/28-Aug: bought 1.188 crore Ather shares for about **Rs 1,758 cr**, stake now about 32.8% | **missed** |
| Management | not mentioned | New Chief Strategy Officer 17-Aug, new Chief Digital and Information Officer 31-Aug, CTO change in May; ESIC lien Rs 4.8 cr (trivial) | minor |

About Rs 2,700 cr committed to a listed, loss-making EV associate within six weeks is roughly 2.7% of Hero's market value (INFERENCE: mcap about Rs 1.0 lakh cr). The "cash returns" thesis competes with this use of cash. Ather's own results are equity-accounted into Hero's consolidated profit, and the Rs 722 cr "one-off" in the base came from the same associate. Ather's loss size was not verified.
Valuation: Yahoo trailing EPS 272, 18.5x; D's own 5-year median 16.8x, so it trades about 10% above its history, not "roughly fair".

### 1.4 SBI
| Item | Check | Status |
|---|---|---|
| Q1 FY27 PAT Rs 21,121 cr (+10.23%), NII +14.88%, advances +18.63%, deposits +9.73%, GNPA 1.47%, NNPA 0.38%, credit cost 0.27%, CRAR 15.67%, ROA 1.11%, ROE 17.87%, domestic NIM 3.00% | all confirmed in the 7-Aug press release | FACT |
| Provisions -31.9% y/y | confirmed (3,359 vs 4,934). Without that, operating profit grew only 9.8% | FACT |
| Q2 result date | not announced in the NSE feed; last year 4-Nov; Yahoo shows 4-Nov as an estimate | unverified |
| **SBI Funds Management** | IPO 14-16 Jul, listed 21-Jul (SBI press release). SBI sold about 6.3% (61.76% to 55.46%); press estimates a pre-tax gain of about **Rs 7,363 cr** plus Rs 1,655 cr from a pre-IPO placement (secondary sources, unverified). It falls in **Q2**, so the Q2 headline profit may be inflated by roughly a quarter's profit | **missed by D**; amount unverified |
| **Strike** | UFBU notices served 7-Sep: strikes 11-Sep, 28-30 Sep, and "continuous strike from 26 October 2026". SBI says it has made arrangements. Whether the 26-Oct strike is still on was not verified | FACT (notice), outcome unknown |
| Management | CFO and Chief Credit Officer superannuated 31-Jul; new CFO from 1-Aug | FACT |

### 1.5 Sun Pharma
| Item | D says | Check | Status |
|---|---|---|---|
| NCD up to Rs 10,000 cr, independent director resigned 12-Oct | | confirmed (Gautam Doshi, personal reasons) | confirmed |
| Funding mix and pro-forma leverage "unverified" | | **CRISIL rating rationale of 13-Oct (and ICRA) is public**: Organon EV $11.75 bn, funded by $2.0-2.5 bn cash and **$9.5-10.0 bn debt** (including taking over Organon's ~$8.5 bn debt); net debt/EBITDA **1.5-2.0x in FY28**; completion late 2026 to early 2027; NCDs rated **AAA/Stable** by both | FACT, D's trigger (1) is effectively answered |
| Q1 FY27 | revenue +10.5%, profit +27%, EBITDA margin 29% | CRISIL: operating income Rs 15,300 cr (+10%), **operating profit +2.7% to Rs 4,418 cr**, margin 29.0% vs 31.1%, **US formulations -10%**, India formulations +16%, innovative medicines +13%. CRISIL expects margin of 26-27% over the medium term | the +27% PAT is not an operating number (base-effect reason unverified) |
| Other | | 17-Aug "Update on Lipitor Antitrust Litigation" filing; promoter-group reclassification approved 26-Sep; agreement with the US administration gives two years of tariff mitigation (CRISIL) | not covered by D |

### 1.6 HAL
| Item | Check | Status |
|---|---|---|
| Q1 revenue Rs 5,515 cr, PAT Rs 1,590 cr | confirmed (5,51,528 lakh; 1,58,061 lakh standalone) | FACT |
| Other income Rs 903 cr in Q1 vs total income Rs 6,418 cr | confirmed | FACT |
| FY27 guide 10-12% revenue, EBITDA 30-31%, order book about Rs 2.54 lakh cr | several secondary sources agree; Q1 EBITDA margin about 27.7% (Citi via press) so the guide is back-end loaded | secondary |
| Tejas Mk1A | no formal delivery as of May; engine counts conflict across sources; first squadron targeted March 2027 | secondary, unverified |
| Management | Executive Director (Finance) retired 30-Sep; government nominee director replaced 7-Oct; new CMD (Ravi K); new statutory auditors appointed 8-Sep | FACT (filings), D covered only the CMD |
| Price | Rs 4,903; +10.7% over 200d; 3.8% below 52w high; 6m +15.7% | FACT |

## 2. Arithmetic and consistency errors in D
1. **Caps do not add up.** Tier caps are 2.5 + 2.0 + 1.5 + 1.5 + 1.5 + 1.5 = 10.5% of net worth, but the stated sleeve cap is 8% and "two-wheeler cluster capped at 3.5%" while Bajaj 2.5 + Hero 1.5 = 4.0%. Tier 1+2 alone is 7.5%.
2. **HCLTech multiples are mislabelled.** On D's own EPS of Rs 72: Rs 1,250-1,360 is 17.4-18.9x (not "17-18.5x"), Rs 1,150-1,250 is 16.0-17.4x (not "17-18.5x"), Rs 1,500 is 20.8x (not 22x).
3. **SBI "8x / 1.2x book" at Rs 880 is wrong.** Yahoo consolidated EPS 94.9 and book 673.8: Rs 880 is 9.3x and 1.31x book. 8x would be about Rs 760.
4. **HCLTech "Q2 YoY +21%" is quarterly.** Company LTM EPS growth is +12.2% (release). Dollar revenue growth is 2.2%.
5. **P(+30% in 12m) of 8-12% contradicts D's own base case.** With D's base returns (+8% to +15%) and realised volatility (1y: Bajaj 24%, HCL 30%, Hero 26%, SBI 24%, Sun 19%, HAL 28%), a lognormal gives roughly 15-25%. My model estimates (with a haircut for regime OFF): Bajaj 18%, HCL 16%, Hero 14%, SBI 15%, Sun 11%, HAL 16%. History since 2015 (survivor-inflated, current index members) is 22-31% for these names, and HAL 54%. D's dip odds are in line with history and realised volatility (my check: Bajaj 16-20%, HCL 21-24%, Hero 24-29%, SBI 22-31%, HAL 34%), but HAL's 3-year volatility of 35% implies about 40%.
6. **Brent is quoted on one instrument.** D uses futures ($106); F uses FRED dated Brent ($125.4 on 6-Oct, with $135.5 on 2-Oct). Futures were $100-107 over the same days. The $20-30 gap (extreme backwardation, INFERENCE: physical tightness) means D understates the import-price shock for India. State both.
7. Stale table: D's 2.1 shortlist uses 12-Oct closes; HCLTech and TCS gapped up 13-Oct.

## 3. Momentum, the lab's only validated selector
My ranking among 417 Nifty 500 names with at least Rs 15 cr/day turnover (12-1 return in brackets): Bajaj 80th (+38%), SBI 67th (+17%), Sun 66th (+15%), HAL 51st (+4%), Hero 43rd (-3%), HCLTech 34th (-8%). D's percentiles (84/71/70/56/48/38) use a different base but the order is the same.
- D says three of six (HCL, Hero, SBI) rank mid or low. Correct set: **HCLTech and Hero are below the median, HAL is at the median**; SBI and Sun are upper-middle. Nobody is top decile (the lab's edge is the **top decile**, which needs roughly +60% 12-1 return in this universe). Bajaj is top quintile only.
- So the sleeve as a whole is a valuation/earnings-revision sleeve, which the lab has not validated, inside a lab whose only edge is momentum. Demotion rule I would apply: **no start while below the 50th percentile unless the stock passes the lab's trend filters (above own 200d and within 25% of the 52-week high) at a month-end close.** That demotes HCLTech and Hero, leaves HAL as watch, and leaves Bajaj and SBI eligible.
- Lab filters today (14-Oct): Bajaj passes by 0.9%, HCLTech by 0.3%, HAL passes comfortably; Hero (-5.3%), SBI (-8.5%), Sun (-3.0%) fail. A 1% move flips Bajaj and HCL, and the index regime flipped 17 times this year (F section 7.1), so a month-end close is the right test, not an intraday one.

## 4. Does a dollar-earner plus domestic-cyclical bundle fit this backdrop?
Backdrop (FACT, dated): Nifty 500 22,041 vs 200d 22,894 (-3.7%), regime OFF; USDINR 95.06; Brent futures 105.7, dated Brent 125 (6-Oct); RBI repo 5.50% (hike 7-Oct; RBI page lists the 5-7 Oct MPC resolution, rate and stance from several secondary sources); FPI selling.
Test (weekly returns, Oct 2023 to Oct 2026, regressed on Nifty 500, USDINR and Brent; INFERENCE, n about 156 weeks):

| | Beta to Nifty 500 | Beta to USDINR (rupee weaker) after market | Avg weekly return in the 14 weeks the rupee fell over 1% | 2026 YTD | Since 1-Sep |
|---|---|---|---|---|---|
| Bajaj Auto | 1.07 | -0.3 | -0.7% | +10.1% | -16.5% |
| HCLTech | 0.67 | **-1.2** | **-2.0%** | -15.5% | -1.1% |
| Hero | 1.06 | -0.6 | -1.8% | -12.4% | -9.5% |
| SBI | 0.92 | 0.0 | -1.6% | -2.7% | -7.7% |
| Sun | 0.53 | -0.1 | -1.0% | +2.1% | -9.4% |
| HAL | 1.68 | -0.4 | -2.0% | +12.0% | +1.9% |
| Nifty 500 / Nifty IT | 1 / | | -1.1% / -2.2% | -8.5% / -21.6% | -5.6% / -4.6% |

Reading:
1. **The "dollar earner hedges the rupee" idea is an earnings story, not a price story.** HCLTech fell more than the market in rupee-slump weeks, Nifty IT is -21.6% YTD while the rupee is 5.6% weaker, and D's own numbers show only 2% dollar growth. The rupee boosts reported profit with a lag; the share price has been driven by AI-disruption fears and FPI selling. If the rupee reverses to 88-89, profit support fades while the price has not been rewarded for it.
2. **Daily correlations are low** (HCL vs the other five 0.15-0.21; Hero-Bajaj 0.53; SBI-HAL 0.45), so there is real diversification in day-to-day noise. But over three years the equal-weight six had annualised volatility of 16.2% vs 14.5% for Nifty 500 and a worst drawdown of -25% vs -19% (survivor-selected names, so a floor on the true risk). In a stress regime correlations rise; the bear scenario in F (33% model estimate: Nifty 500 -10% to -20%, mid caps -20% to -35%) would take most of these down together. The bundle is roughly index-beta (average about 1.0), not a hedge.
3. **Domestic cyclicals are on the wrong side of two of four stressors:** oil (Hero commuter demand and input costs; Bajaj domestic -12% in September) and rate hikes (SBI treasury mark-to-market, funding gap of 8.9 pp between loan and deposit growth). Bajaj's export half is the only genuine rupee-positive earnings leg: exports +47% in H1 FY27.
4. **A quick-pace rule consistent with F:** F allows at most one third of the intended slice before an ON month-end, only for names that pass the lab's filters. By that rule only Bajaj (and HAL at a better price) qualifies; HCLTech passes by 0.3% after a 14% bounce, which is not a signal.

Verdict on the bundle: it does not fit as a regime-OFF "barbell". Hold the dollar-earner leg to a small, late-staged position. The macro-consistent core is Bajaj's export franchise.

## 5. Per-idea review, corrected numbers and entry plan

### 5.1 Bajaj Auto: CONFIRM, but start after 27-Oct; cap 2.5% (keep), tranches 1/3 each
- Bull case holds: standalone PAT +42%, margin 20.8%, H1 exports +47%, record export base, 23.9x consolidated vs own 25.7x median. Bear case D under-weighted: price -16% in six weeks on weak domestic demand and the buyback support is gone; the Q2 comparison base is easy (INFERENCE: the GST cut took effect 22-Sep-2025 per D's secondary source), so the 27-Oct print is a weaker test than D assumes; the hard test is Q3 (Oct-Dec) against the festive base.
- **KTM kill trigger is mis-specified.** "KTM EBIT negative again in the Q3 2026 print" would probably fire for seasonal reasons (Q2 EBIT was +EUR 1.3 mn; H1 EBIT -24.8 mn). Replace with: Bajaj Mobility quarterly EBITDA margin below 3% for two quarters, or any new parent funding, guarantee or loan above EUR 100 mn (parent funding history: loans signed Feb-Mar 2026, see NSE filings; amount of any further support unverified). The other three kill criteria are observable and sensible (standalone EBITDA below 19% for two quarters, exports under +10% y/y for two months, domestic 2W under -10% for three post-festive months).
- **Entry plan (changed):** nothing before 27-Oct. Tranche 1 (one third of cap) on the first close after the 27-Oct print, or on the 30-Oct month-end, if standalone EBITDA margin is 20% or more, exports are up 25% or more in the quarter, and the price is above the 200d MA (about 10,250) at that close. If it fails only the MA test, half-size tranche. Tranche 2 on the first ON month-end or after Q3 results (late January, date unannounced) with the checks green, at least 6 weeks later. Tranche 3 on a pullback to Rs 9,300-9,800 (24-25.6x on Rs 383) with checks green, or after Q3. Do not chase above Rs 11,500 (30x).
- Odds (model estimates): P(+30% in 12m) 18%; P(22.5% dip) 20%; base +8% to +15%.
- Stress: at 2.5% and a covid-type fall of 35%, -0.9 pp of net worth (D's figure; checks).

### 5.2 HCLTech: DOWNGRADE to Tier 3; cap 1.0%
- Hard numbers hold, so this is not a kill. Reasons to downgrade: (a) momentum 34th pct and the whole IT group is the weakest in the universe (Infosys 11th, TCS 16th); (b) the entry zone starts after a 14% bounce in four sessions, with the 200d MA at the price; (c) y/y CC growth of 2.6% is at the floor of 2.5-4.0% guidance, HCLSoftware is shrinking 11%, Engineering and R&D margin fell 231 bp; (d) restructuring in five straight quarters means the 18.2% margin is not clean; (e) the price already exceeds the Yahoo mean target (stale risk noted); (f) no price-level rupee hedge in the data (section 4); (g) at 19x and 3% growth it is not cheap against TCS at 15x. Cash yield is real (Rs 60 DPS in the last four payouts, about 4.5%; part is a special).
- **Buy after the ex-date.** Ex-dividend is 16-Oct; buying before it means receiving a Rs 12 (0.9%) dividend taxed at slab rate (INFERENCE; verify with a CA) and an equal price drop.
- **Revised plan:** no purchase now. A starter (one third of a 1.0% cap) only if (i) price is at or below about Rs 1,290 with the lab filters passing at a month-end, or (ii) after the Q3 FY27 print (Yahoo estimates 11-Jan-2027; not announced) with y/y CC growth at least 3.0% and EBIT margin at least 17.5% including restructuring. Add only on ON.
- **Kill criteria changed:** replace "CC growth negative q/q for two quarters" (Q3 has seasonal furlough noise) with y/y CC growth below 2.0% for two quarters, or EBIT margin including restructuring below 17.0% in any quarter (Q1 FY27 was 16.9%), or net cash below Rs 15,000 cr without a disclosed deal.
- Odds: P(+30%) 16%; P(22.5% dip) 25%.

### 5.3 Hero MotoCorp: KILL as a start candidate (keep on monitor)
- No part of D's Q1 data is wrong. The reasons to kill: momentum 43rd pct and fails the trend filter (-5.3% under the 200d); P/E 18.5x vs 16.8x median; capital allocation drifted to Ather (about Rs 2,700 cr in six weeks); EBITDA margin 13.3% vs its 14-16% target; Q2 (28-Oct, confirmed) compares against a weak, GST-pause base so a strong print says little; Q3-Q4 is the hard comparison; it adds a second two-wheeler exposure to Bajaj and breaks D's own 3.5% cluster cap.
- Re-open only if: price closes above its 200d (about Rs 5,310) at a month-end and Q2/Q3 standalone EBITDA margin is 13.5% or more and Ather funding is capped (no further commitment beyond about Rs 3,000 cr). Then at most a 1.0% cap.
- Odds if started anyway: P(+30%) 14%; P(22.5% dip) 25%.

### 5.4 SBI: CONFIRM Tier 2, but replace the gate; cap 1.5%
- Keeps: 10.0x trailing, 1.41x book, 1.8% yield, loans +18.6%, GNPA 1.47%, Yahoo mean target Rs 1,255 (+32%, 39 analysts). Momentum 67th. Cheapest of the six against its own history.
- **Gate changed.** D buys after the Q2 print if kill checks pass. That print will include the SBI Funds sale gain (est. Rs 7,000 cr pre-tax, unverified) and likely Rs 1,655 cr from the placement; strip both before judging. Revised pass test: Q2 PAT excluding the one-off up at least 8% y/y; domestic NIM at least 2.9%; credit cost at most 0.45%; GNPA at most 1.6%; deposit growth at least 9% against loan growth.
- Kill thresholds in D are loose (credit cost 0.6% vs 0.27% now, GNPA 2.0% vs 1.47%). Tighten to 0.5% and 1.8%; keep domestic NIM 2.8% and ROA 0.9%.
- Event risk: UFBU strike notice from 26-Oct (unknown if it stands); results date not announced (4-Nov is Yahoo's estimate, last year's date); the Rs 60,000 cr bond approval is debt only.
- **Entry plan:** no purchase before the result. Tranche 1 (one third, 0.5%) only if the gain-adjusted checks pass and the price has reclaimed its 200d (about Rs 1,040, +9% from here) or Nifty 500 is ON; otherwise wait. A price near Rs 900-1,000 is 9.5-10.5x; Rs 880 is 9.3x (not 8x).
- Odds: P(+30%) 15%; P(22.5% dip) 28% (full-history 31%, since 2015 22%, model 18-21%).

### 5.5 Sun Pharma: DOWNGRADE (park)
- The quality franchise and AAA balance sheet are real (AAA/Stable from CRISIL and ICRA on 13-Oct; leverage 1.5-2.0x in FY28). But 34.8x trailing for operating profit +2.7%, a falling margin (29.0% vs 31.1%; CRISIL expects 26-27%), US formulations -10%, an $11.75 bn integration with $3.5 bn of Organon debt due in 2028, MFN/tariff drug-pricing policy risk, and the lab's own sector note ("avoid healthcare, flat EPS") argue for no entry plan now.
- Replace D's trigger (1) (leverage 2.5x or less, already met on CRISIL numbers) with: Q2 operating profit growth at least 8% y/y and EBITDA margin at least 28%; trigger (2) price at or below Rs 1,560 stays. Kill: leverage guidance above 2.5x or an Organon deal re-cut.
- Odds: P(+30%) 11%; P(22.5% dip) 15%.

### 5.6 HAL: CONFIRM watch only
- Passes the trend filter, but 34.4x trailing (28.4x Yahoo forward, unverified), Q1 EBITDA margin about 27.7% against a 30-31% guide, 31% of pre-tax profit from other income (D), beta 1.7, 3-year volatility 35%, dip frequency 34%, and leadership turnover (CMD, finance director, government nominee, auditors).
- D's trigger of Rs 4,200 (29.5x on EPS 142.6; D used Rs 139) is 14% below the price and below the 200d (about 4,430). Practical trigger: Rs 4,430-4,600 after Q2 (Yahoo estimate 11-Nov; not announced) shows EBITDA margin at least 28% and at least four Mk1A deliveries disclosed. Cap 1.0%.
- Kill criteria in D ("engine supply slips beyond FY28") are not observable soon. Replace with: no Mk1A delivery disclosed by the Q3 print (about February 2027), or FY27 revenue guidance cut below 8%.
- Odds: P(+30%) 16%; P(22.5% dip) 35%.

## 6. What I would start first and the pace
**One name now-ish: Bajaj Auto. Everything else waits.** A second name only on a stock-specific trigger, SBI first.
| Step | When | Action |
|---|---|---|
| 0 | to 30-Oct | Nothing. Watch: Bajaj Q2 27-Oct, Hero Q2 28-Oct, FOMC 27-28 Oct, SBI strike notice from 26-Oct, SBI/Sun/HAL dates when announced |
| 1 | 28-Oct to 30-Oct | Bajaj tranche 1 (one third of 2.5% cap, about 0.8% of net worth) if the Q2 checks and 200d test pass |
| 2 | at least 6-8 weeks later; first ON month-end (P about 20% on 30-Oct, about 55% by Dec, F) or Q3 results | Bajaj tranche 2; SBI tranche 1 if its gain-adjusted checks pass and trend is repaired |
| 3 | Q3 prints (January, dates unannounced) | Bajaj tranche 3 or pullback buy; HCLTech starter only if its conditions are met |
| Never before ON | | Hero, Sun, HAL (unless their triggers fire) |
Sleeve cap I would use: 5% of net worth in aggregate for the active names (Bajaj 2.5, SBI 1.5, HCL 1.0), with at most 7% if every watch trigger also fires. Pace per F's slow lane: half-size or one-third tranches, at least 6-8 weeks apart, none while a kill criterion is amber. Averaging-down and exit rules in D (review at -20%, exit at -25% unless all checks are re-verified) are consistent with the stated loss limit; keep them.

## 7. Additional items for the calendar
| Date | Event | Status |
|---|---|---|
| 16-Oct | HCLTech ex-dividend Rs 12 | NSE confirmed |
| 26-Oct | Bank unions' continuous strike notice (SBI affected) | notice only; outcome unknown |
| 27-Oct | Bajaj Auto Q2 | NSE confirmed |
| 27-28 Oct | FOMC | F |
| 28-Oct | Hero Q2 | NSE confirmed |
| 30-Oct | Month-end regime and stock filter check | lab rule |
| 4 to 12-Nov | SBI (4), Sun (5), HAL (11), M&M (5) | **Yahoo estimates, not announced**; Hero's Yahoo date (12-Nov) was wrong, so treat as unverified |
| 2-4 Dec | RBI MPC | secondary sources |
| Mid-Nov | Bajaj Mobility (KTM) Q3 | date not verified |

## 8. What I could not verify
- SBI Funds gain size (press estimate only), whether the 26-Oct strike goes ahead, Ather's loss size, any consensus estimates or call transcripts (not opened), HAL guidance and Tejas delivery counts (secondary), RBI statement text (page lists the resolution; figures from secondary sources), HCLTech's analyst target date, the Q2/Q3 result dates for SBI/Sun/HAL/HCLTech.
- Regression and correlation numbers are my own computation from Yahoo adjusted prices (about 156 weekly observations); coefficients are noisy and not a forecast.
- All base rates are survivor-inflated (current index members); the lab's momentum edge was tested on India large/mid caps, price-only.
- Tax and employer rules from D stand unverified: verify with a CA and with HR/compliance (restricted-list screening for an IT-services name).
