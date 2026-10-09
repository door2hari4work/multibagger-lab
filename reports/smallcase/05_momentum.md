# Momentum smallcases vs momentum index funds/ETFs: what the evidence supports (as of 2026-10-09)

Research note, not personal advice. Every number carries a source and date. Where I could not verify something it says so in section 7. Nothing here was filled from memory.

## 0. Bottom line

1. **A low-cost direct index momentum fund is likelier to deliver than a paid-manager momentum smallcase.** The reason is structural, not a claim that the smallcase manager is worse. At Rs 1,00,000 or Rs 10,000/month, a subscription of the size smallcase pages currently show (Rs 4,500 per 6 months for Wright, Rs 5,100 per 3 months for Windmill) is several percent of capital every year. Add short-term capital gains tax on churn, which a fund wrapper avoids. The smallcase manager would need roughly 5 to 10 percentage points more gross return a year than the index to break even (section 5).
2. **The momentum edge itself is thin in live data.** Since 2022, India Nifty 200 Momentum 30 index funds have matched the Nifty 500 (not beaten it) and beaten the Nifty 50 by 2 to 3 points a year. They carried roughly twice the drawdown: about -31.5% against -18.6% for a Nifty 500 index fund. They have still not recovered (section 3). That fits the lab's own findings: the rank adds return in large/mid caps and does not add protection (ENGINE_FINDINGS.md section 2).
3. **No currently live momentum smallcase I found publishes a verifiable live return or drawdown without a login.** Two of the five I sampled are closed ("played out", ended 30 Sep 2025). I cannot rank paid smallcases on evidence. What I can say is that the cost and tax arithmetic is hostile and that the one manager who explained the gap said smallcase NAVs are "an ideal theoretical return" (Capitalmind, 2021).
4. **Timing:** India's Nifty 500 was below its 200-day average at the lab's 2026-09-30 screen (22,072 vs 22,966, regime OFF; FINAL.md update). Momentum index funds have no regime filter. They are fully invested into that weakness. Momentum index funds are about 24% below their 27 Sep 2024 peak today (section 3).

## 1. Momentum smallcases found (sample, not the full category)

The smallcase discover page is JavaScript-rendered and returned no listings to my fetcher. I reached individual smallcase pages by ID, manager pages and Tickertape snippets. Returns on every active smallcase page I opened were locked behind a login/"request to view" gate. Tickertape direct fetches returned 404, so Tickertape figures come only from search-result snippets and are stale snapshots (flagged "snapshot").

| Smallcase (manager) | Launch | LIVE vs BACKTESTED returns I could verify | CAGR / drawdown / vol | Rebalance (turnover, tax) | Min invest | Subscription | Stocks / cap mix | Regime/risk-off rule |
|---|---|---|---|---|---|---|---|---|
| **Wright Momentum Model** (Wright Research; Sonam Srivastava) | Not on smallcase page. Dec 2020 per Wright blog; "25 Nov 2020" per a Tickertape snippet | Page returns locked ([smallcase page](https://www.smallcase.com/smallcase/WRTNM_0001)). Wright's own claims, not verified: "322% in last 4 years" (Dec 2023 blog, no dates, live/backtest unstated); own table Oct 2022: 2Y CAGR 55.2% vs Nifty 14.6%; 2024 "33.77%" (year-end review, via search summary); Tickertape snapshot (last rebalance 1 May 2024): 3Y CAGR 48.02% | CAGR: see claims. Drawdown: none published. Vol: labelled "High" only | Monthly, 0 to 4 stock changes (Wright blog). Holding "1 to 6 months", so mostly short-term gains. Wright's 2021 cost note: trading costs cut profit "~3% per year" (ambiguous wording) | Rs 49,091 (smallcase page, undated); Rs 48,915 (manager page); Rs 61,743 (May 2024 snapshot) | Rs 4,500 per 6 months (smallcase page, read by fetch tool); Rs 2,000 per 3 months (May 2024 snapshot); Rs 200 + GST/month (2021 blog) | 20 to 25 stocks. Universe "top 300" (Wright) or "top 500" (smallcase page). Cap mix not stated; "small-cap bias when small caps are in favour" | **Partial.** Moves toward liquid bees in equity drawdowns, no trigger on current pages. Smallcase blog (3 Oct 2022) states a **10% portfolio-drawdown trigger** for gradual shift to cash. It is a portfolio rule, not an index-below-200DMA rule. Not confirmed as current |
| **Alpha Prime Momentum Model** (Wright) | Not stated | Locked (3Y CAGR label only) | None public | Not stated | Rs 29,293 | Not shown | Few, concentrated (per tagline) | Not stated |
| **Capitalmind Momentum Model** (Capitalmind) | Live since Jan 2019 ([Capitalmind update](https://pages.capitalmind.in/posts/capitalmind-momentum-smallcase-update-what-sell-in-may-and-go-away)) | Smallcase NAV CAGR "~60%" (May 2021), Capitalmind says most investors' real return "closer to ~46%" because smallcase NAV is "an ideal theoretical return". Page now: no returns shown | Drawdown: monthly factsheets of 6 to 7% in 2021; no all-period figure found. Vol: "High" | Weekly review; monthly rebalance (Capitalmind, Apr 2024). Capitalmind's Aug 2025 post: high-churn momentum "mostly short-term gains" hit by 2024 STCG rise 15% to 20%, a mutual-fund wrapper is better | Rs 1,81,843 | Not shown | 15 to 25 stocks, all caps | "If there aren't enough opportunities, stay in cash" (smallcase page). **Service ended 30 Sep 2025.** Capitalmind said momentum-only had done poorly for 12 to 24 months ([Aug 2025](https://premium.capitalmind.in/2025/08/whats-next-for-capitalmind-momentum-the-flexi-cap-path/)) |
| **Stockstar Momentum Superstars** (Stockstar) | Feb 2022 (snapshot only) | Snapshot: 2Y CAGR 74.81%, now "played out", not tracked ([page](https://www.smallcase.com/smallcase/STCKMO_0001)) | None current | "No defined timeline"; can be frequent | Rs 62,730 | Not shown | Not stated; mid and small cap | None stated. **Marked "played out"** |
| **Value & Momentum Asset Allocation** (Windmill Capital) | Oct 2021 (snapshot only) | Locked on [page](https://www.smallcase.com/smallcase/SCMO_0044). Snapshot: 3Y CAGR 21.59% | None public. Gold and debt added "to reduce risk" | Not stated | Rs 40,316 | Rs 5,100 per 3 months | Not stated | Static gold/debt sleeve, not a switch |

How to read this: the only entries with usable numbers are manager self-reports with no dates, stale snapshots, or numbers the manager itself later qualified. Smallcase's own disclosure page says its displayed returns are "for informational purposes only". Wright's pages say performance "is not verified by SEBI".

## 2. Momentum mutual funds and ETFs

Sources: AMC factsheets (Kotak, 31 Jul 2026) for what is marked "factsheet"; AMFI NAV data (portal.amfiindia.com, NAVAll.txt dated 8 Oct 2026) for fund names/NAVs; NAV histories via the mfapi.in mirror of AMFI data. I spot-checked three Kotak NAVs on 31 Jul 2026 against the factsheet and they matched exactly. Drawdowns and CAGR below are my own calculations from daily Direct-Growth NAVs, in 5.6 years at most. Only Kotak factsheets were obtained; other AMCs' TER/AUM come from aggregator pages (marked "agg.", unverified).

### 2a. Index funds / ETFs

| Fund | AMC | Launch (first NAV) | TER (Regular / Direct) | AUM | Tracking | Return vs benchmark | Max drawdown (Direct, own calc) |
|---|---|---|---|---|---|---|---|
| Nifty 200 Momentum 30 Index Fund | **UTI** | 12 Mar 2021 | n/v | n/v | n/v | NAV CAGR 13.4% to 8 Oct 2026, vs Nifty 500 index fund 10.9% and Nifty 50 index fund 8.3% (same start) | -31.5% (27 Sep 2024 to 7 Apr 2025); now -23.8% below peak |
| Nifty 200 Momentum 30 Index Fund | **Motilal Oswal** | 16 Feb 2022 | agg.: 0.9 to 1.08% / 0.28 to 0.33% (sources conflict) | agg.: Rs 840 to 972 cr | n/v | 8.8% vs Nifty 500 9.3%, Nifty 50 6.6% | -31.6%; now -24.4% |
| Nifty 200 Momentum 30 Index Fund | **Kotak** (factsheet, 31 Jul 2026) | Allotted 15 Jun 2023 | **0.68% / 0.20%** (Base ER, excludes brokerage) | **Rs 587.73 cr** | TE **0.20%**, turnover **170.75%** | Regular: SI 12.34% vs index 13.69% (alpha -1.35); 1Y 0.77% vs 1.85%; 3Y 10.88% vs 12.06%; Nifty 50 TRI 3Y 8.56% | -31.6%; now -23.8% |
| Nifty 200 Momentum 30 Index Fund | **HDFC** | 28 Feb 2024 (NFO 9 Feb 2024) | agg.: 0.85 to 0.87% regular | agg.: Rs 610 to 618 cr | n/v | NAV 9.67 vs Rs 10 issue price: **-1.3% a year since launch** | -31.8%; now -24.5%; 1Y -6.2% |
| Nifty 200 Momentum 30 Index Fund | ICICI Pru, Bandhan, Baroda BNP | Aug 2022, Sep 2022, Oct 2024 | agg.: ICICI 1.01% (regular); Baroda 1.06% (agg.) | agg.: ICICI Rs 546 cr; Baroda Rs 22 cr | n/v | ICICI 11.2% a yr; Bandhan 9.8%; **Baroda NAV 7.62 (-12.6% a yr)** | -30.4% to -31.8% |
| Nifty 200 Momentum 30 ETFs | HDFC (Oct 2022), ABSL | HDFC ETF: Oct 2022 | agg.: HDFC ETF 0.30%; ABSL 0.29% (AMC page text, tracking error 0.17%, May 2025 data) | agg.: HDFC ETF Rs 101.7 cr | ABSL 0.17% (May 2025) | not computed | not computed |
| Nifty Midcap 150 Momentum 50 Index Fund | **Kotak** (factsheet) | Allotted 8 Oct 2024 | **0.93% / 0.28%** | **Rs 442.9 cr** (31 Jul 2026); Rs 473.9 cr (31 Aug 2026) | TE 0.12%, turnover 131.5% | Regular: SI -3.36% vs index -1.93% (alpha -1.43); 1Y 2.07% vs 3.27%. Regular NAV 9.40 vs Rs 10 | -25.5% (Direct) vs Midcap 150 index fund -19.7% over the same window |
| Nifty Midcap 150 Momentum 50 Index Fund | Edelweiss (Regular plan series) | 2 Dec 2022 | n/v | n/v | n/v | 14.7% a yr (Regular plan NAV) | -26.0%; now -13.8% |
| Nifty 500 Momentum 50 Index Fund | Nippon, Motilal Oswal, Bandhan, Axis; **Kotak** (Dec 2025) | Sep 2024 to Feb 2025 (Kotak 11 Dec 2025) | Nippon agg. 1.59% regular; Kotak direct **0.19%** (factsheet; regular figure blank) | Nippon agg. Rs 1,326 cr; **Kotak only Rs 24.5 cr** | Kotak TE **0.34%** | Nippon -9.7% a yr, Motilal -9.9%, Bandhan -6.8% vs Nifty 500 fund -4.8% (same window); Axis +6.7% (started Feb 2025); Kotak SI 0.63% vs index 1.90% | -29% to -32% (Axis -17.0%, short history) |

n/v = not verified.

### 2b. Actively managed momentum funds (all new, short history)

AMFI lists funds from ICICI Pru, Kotak, Motilal Oswal, quant, Union, Axis, Nippon India, Samco and NJ (Aug 2026). I verified TER and AUM only for Kotak.

| Fund | Launch | TER (Regular / Direct) | AUM | Return (Direct NAV CAGR/abs to 8 Oct 2026) | Max drawdown (own calc) | Note |
|---|---|---|---|---|---|---|
| Kotak Active Momentum Fund | 20 Aug 2025 | **2.13% / 0.84%** (July 2026 factsheet; June sheet said 2.15%) | **Rs 1,624.76 cr** | Regular SI 11.87% vs Nifty 500 TRI 2.34%, Nifty 50 TRI -1.80% to 31 Jul 2026 (under 1 year, not annualised). Direct +3.3% to 8 Oct 2026 | -13.6% | Holds 5.8% debt/money market (6.4% TREP); turnover **188%**; cap mix 43% large, 48% mid, 3.5% small. No stated cash rule; no hedging rule |
| Nippon India Active Momentum | 3 Mar 2025 | n/v | n/v | 13.8% a yr | -12.6% | Multi-factor |
| Motilal Oswal Active Momentum | 21 Mar 2025 | n/v | n/v | 26.9% a yr | -16.6% | About 30 stocks, equal weight, monthly (news snippet). Started near the April 2025 trough, flatters result |
| quant Momentum | 21 Nov 2023 | n/v | n/v | 14.7% a yr | -22.7% | |
| Samco Active Momentum | 12 Jul 2023 | n/v | n/v | 15.7% a yr | -25.0% | |
| Axis Momentum | 18 Dec 2024 | n/v | n/v | -6.8% a yr | -21.5% | |
| Union Active, ICICI Pru Active, NJ Momentum | Dec 2024, Jul 2025, 3 Aug 2026 | n/v | n/v | Union +0.7% a yr; ICICI +4.3%; NJ -3.5% in 2 months | -26.6%, -11%, -6% | Too young to judge |

The live record of these active funds is under 3.3 years and starts after the 2024 to 2025 fall for many. It is no evidence of persistent skill. The wide spread (+27% to -7%) shows how far implementation choices matter.

## 3. What the live (not backtested) index record shows

All Direct-plan NAV CAGR/XIRR, pre-tax, to 8 Oct 2026, against Motilal Oswal Nifty 500 Index Fund and UTI Nifty 50 Index Fund (also Direct, so these are investable comparisons).

| Window | Momentum fund | Nifty 500 index fund | Nifty 50 index fund |
|---|---|---|---|
| UTI N200 Mom30 from 12 Mar 2021 (5.6 yrs) | 13.4% | 10.9% | 8.3% |
| Motilal N200 Mom30 from 16 Feb 2022 (4.6 yrs) | 8.8% | 9.3% | 6.6% |
| Kotak N200 Mom30 from 20 Jun 2023 (3.3 yrs) | 9.8% | 9.9% | 6.2% |
| Kotak Mid150 Mom50 from 11 Oct 2024 (2.0 yrs) | -5.5% (vs Midcap 150 index fund -1.3%) | -3.5% | n/a |
| Nippon N500 Mom50 from 1 Oct 2024 (2.0 yrs) | -9.7% | -4.8% | -6.2% |

Drawdown from the 27 Sep 2024 peak: UTI N200 Mom30 -31.5% max, -23.8% now; Nifty 500 index fund -18.6% max, -10.2% now; Nifty 50 index fund -15.4% max, -13.4% now; Nippon Midcap 150 index fund -20.6% max, -4.2% now. One lakh in UTI's fund at the peak was worth about Rs 68,500 at the trough and about Rs 76,200 today, against about Rs 89,800 for the Nifty 500 fund.

Real SIP of Rs 10,000/month (dated the 5th, XIRR, pre-tax, Direct, from each fund's launch): UTI Mom30 7.4% (Rs 6.8 lakh invested, Rs 8.35 lakh value) vs Nifty 500 7.7% (Rs 8.42 lakh) and Nifty 50 4.6% (Rs 7.73 lakh). Motilal Mom30 5.7% vs 6.6% vs 3.3%. Kotak Mom30 -0.5% vs 2.1% vs -1.1%.

**Backtest caveat for the index headline.** Aggregator pages quote "19.2% a year vs 15.1% for Nifty 200 since April 2005" for the Nifty 200 Momentum 30 (dealplexus, citing NSE, to 27 Feb 2026) and HDFC's leaflet "18.8% vs 13.9%" (to 29 May 2026). FreeFinCal said in 2020 the index's "entire history is based on backtested data". Dealplexus says it launched in Aug 2020, so about 15 of the 21 years are backtest. I could not download the NSE factsheet (niftyindices.com timed out on every attempt), so these index figures are unverified. FreeFinCal also noted in 2021 that nearly all outperformance came from 2012 to 2018 and that momentum lagged for 3.5 years after 2008. The live history (about 6 years) shows a smaller edge than the quoted history, and weaker in the last four years.

## 4. How this fits the lab's own evidence

| Lab finding (reports/) | Implication for products |
|---|---|
| Momentum rank is the only component with selection power; India lift is strongest in large/mid (mid top-decile 3x rate 29.8%, lift 1.81x), fading toward 1.11x in micro caps (SMALL_CAPS.md) | Nifty 200 / Midcap 150 / Nifty 500 momentum indices sit in the zone where the edge exists. Smallcase products with "small-cap bias" (Wright, Stockstar) move into the zone where it fades and survivorship is worst |
| Rank adds return but **not** drawdown protection (-25.3% vs random -22.1% in the sealed test; ENGINE_FINDINGS section 2) | Matches the live index record: about -31.5% against -18.6% for Nifty 500. An index fund has no regime filter, so this drawdown is expected, not a defect |
| Trend filters and an index regime filter cut drawdown at about 3 to 4 points of CAGR | Only some smallcases claim a risk-off rule (Wright's 10% portfolio trigger, Capitalmind's cash when thin). None of it is verifiable from public data. The index funds have none |
| Lab backtests are survivor-inflated (34.3% sealed test; survivor equal-weight hold 26.8% vs Nifty 500 12.0%); realistic 14 to 20% pre-tax, 3 to 4 points of short-term tax drag at lab turnover | Treat any smallcase backtest or early-years live CAGR (48%, 75%) as a ceiling. Smallcase live NAVs are idealised, per Capitalmind's own 46% vs 60% disclosure |
| 50 bps costs trimmed the lab strategy from 34.3% to 31.8% CAGR, 100 bps to 27.0% (FINAL.md) | Each extra half-point of friction costs 2.5 to 4.7 points of CAGR at high turnover. Subscription plus short-term tax are larger than that |
| 0 of 668 trades reached 5x; not a multi-bagger finder | Don't buy a momentum product expecting multi-baggers |
| Regime OFF for India on 2026-09-30 | The lab's rule is cash. No product above applies that rule at index level |

## 5. Net-of-fees, after-tax, drawdown-aware comparison

**This is a scenario model, not a forecast.** Inputs are my assumptions, labelled below. The model is in the session scratchpad, not in the repo.

Assumptions:
- Market return 11% a year, the lab's sealed-window Nifty TRI proxy. 5-year horizon.
- Momentum gross edge over market of 0, +2 or +4 points. Zero is the live Nifty 500 comparison since 2022. +2 is about the live UTI edge. +4 is the NSE index backtest edge, so optimistic.
- Index fund drag: Direct 0.8% (the Kotak factsheet's 0.20% TER plus implementation cost, calibrated to the observed 1.08 to 1.43 point regular-plan gap on a 0.68% to 0.93% TER); Regular 1.3%. Nifty 500 index fund drag 0.25%.
- Smallcase: subscription Rs 9,000 a year (Wright's Rs 4,500 per 6 months) or Rs 2,832 a year (Wright's 2021 Rs 200 + GST a month); trading and impact cost 1% or 2% a year of portfolio (assumption; Wright's own 2021 estimate was about 3%); 60% or 100% of each year's gain realised short-term at 20% plus 4% cess; remaining gains taxed at 12.5% plus cess above the Rs 1.25 lakh exemption at exit.
- Index fund tax: 12.5% plus cess on long-term gains above Rs 1.25 lakh, 20% plus cess on units held 12 months or less, one redemption in one financial year. Rates per FY 2026-27 commentary (unchanged from FY 2025-26). I could not confirm the section numbers under the Income-tax Act, 2025.
- IRR includes subscription as an extra cash outflow each year.

### Rs 1,00,000 lump sum, 5 years (after-tax ending value, Rs / IRR)

| Product | Edge 0 (gross 11%) | Edge +2 (13%) | Edge +4 (15%) |
|---|---|---|---|
| Nifty 500 index fund, Direct (reference, no momentum) | 1,66,617 / 10.7% | same | same |
| Momentum index fund, Direct | 1,62,520 / 10.2% | 1,77,813 / 12.2% | 1,94,236 / 14.2% |
| Momentum index fund, Regular | 1,58,867 / 9.7% | 1,73,886 / 11.7% | 1,90,021 / 13.7% |
| Smallcase, Rs 9,000/yr sub, 1% cost, 60% realised | 1,52,120 / **1.1%** | 1,64,763 / **2.9%** | 1,78,232 / **4.8%** |
| Smallcase, Rs 2,832/yr sub, 1% cost, 60% realised | 1,52,120 / 6.2% | 1,64,763 / 8.0% | 1,78,232 / 9.8% |
| Smallcase, Rs 2,832/yr sub, 2% cost, 100% realised | 1,41,096 / 4.5% | 1,51,840 / 6.2% | 1,63,230 / 7.8% |

The smallcase ending values exclude the subscription paid; with Rs 9,000 a year that is Rs 45,000 on top, which is what drives the IRR down. Gains of Rs 62,000 to 94,000 sit under the Rs 1.25 lakh exemption, so the index fund pays no tax if sold in one year.

### Rs 10,000/month SIP, 5 years (Rs 6,00,000 invested; after-tax ending value / IRR)

| Product | Edge 0 | Edge +2 | Edge +4 |
|---|---|---|---|
| Nifty 500 index fund, Direct | 7,71,093 / 10.0% | same | same |
| Momentum index fund, Direct | 7,62,234 / 9.5% | 7,94,969 / 11.2% | 8,29,167 / 12.9% |
| Momentum index fund, Regular | 7,54,274 / 9.1% | 7,86,650 / 10.8% | 8,20,478 / 12.5% |
| Smallcase, Rs 9,000 sub, 1% cost, 60% realised | 7,42,798 / 5.5% | 7,74,865 / 7.2% | 8,08,190 / 8.8% |
| Smallcase, Rs 2,832 sub, 1% cost, 60% realised | 7,42,798 / 7.5% | 7,74,865 / 9.2% | 8,08,190 / 10.9% |
| Smallcase, Rs 2,832 sub, 2% cost, 100% realised | 7,14,105 / 5.9% | 7,42,031 / 7.5% | 7,70,951 / 9.0% |

**Break-even.** To match a Direct momentum index fund's net IRR (index gross 11% to 13%), a smallcase with 1% trading cost and 60% of gains realised short-term needs gross returns of about:
- Lump sum, Rs 9,000 subscription: 21% to 23% a year.
- SIP, Rs 9,000 subscription: 16% to 18%.
- With the cheap Rs 2,832 subscription: 13% to 15% (SIP), 16% to 18% (lump sum).

The break-even is higher for a small lump sum because the fee is a larger share of Rs 1 lakh. Capitalmind's own rule of thumb (a fee of no more than 3% to 5% of the amount invested) gives the same answer: Rs 9,000 on Rs 1 lakh is 9%.

### Drawdown-aware reading (observed, then planning)

| | Observed | Per Rs 1,00,000 at the peak |
|---|---|---|
| N200 Mom30 index funds, 27 Sep 2024 to 7 Apr 2025 | -30.4% to -31.8%, still -23% to -25% in Oct 2026 (about 2 years) | Rs 68,500 at trough |
| Nifty 500 Momentum 50 index funds | -29% to -32% | about Rs 69,000 |
| Nifty 500 index fund (same dates) | -18.6% | Rs 81,400 |
| Lab strategy with regime filter | -19.7% (tune), -25.3% (sealed) | Rs 75,000 to 80,000 |
| Lab planning range (data flatters) | -35% to -45% | Rs 55,000 to 65,000 |

An investor who needs a high probability of not selling in a -30% fall should size the momentum sleeve so that a -35% to -45% hit is survivable. I found no verifiable smallcase drawdown figure, so I cannot say a smallcase's risk-off rule would have done better.

**Outcome ranges the model cannot capture:** manager selection skill; a regime where momentum underperforms for 3.5 years (FreeFinCal's 2008 to 2010 case); fund-level operational risk (tiny AUM funds can close or merge); tax law changes; behaviour. A fund wrapper also avoids paying tax on internal churn, which is the main reason Capitalmind said it was moving its momentum idea into a mutual fund.

## 6. What I would and would not consider

**Would consider (only if the investor wants momentum exposure at all):**
- A **Direct-plan Nifty 200 Momentum 30 or Nifty Midcap 150 Momentum 50 index fund** as a **satellite of limited size** next to a plain Nifty 50/500 index core. Choose the cheapest with real size: Kotak's Mom30 (Rs 588 cr, 0.20% Direct, TE 0.20%) and Mid150 Mom50 (Rs 474 cr, 0.28% Direct, TE 0.12%) are the ones I could verify. UTI, Motilal and HDFC are plausible but I did not verify their Direct TER.
- **Staged entry:** SIP over 12 to 24 months, since the lab's rule is cash while the index is below its 200-day average (it is, today), and a lump sum at a prior peak lost 31% within 6 months.
- **Rolling comparison against a Nifty 500 index fund** and a pre-set exit review (for example, if it trails the Nifty 500 for 3 years), since the live edge over the Nifty 500 since 2022 has been about zero.
- Direct plans only. In the Kotak factsheets, Regular plans trail the index by 1.1 to 1.4 points.
- The **ETF route** (about 0.3% TER, agg., unverified), for investors with a demat account who can tolerate bid/ask spreads on a thinly traded ETF.

**Would not consider:**
- **Paid momentum smallcases at Rs 1 lakh or Rs 10,000/month** unless: (a) the subscription is below about 1 to 2% of the money, (b) the manager publishes live, time-weighted, post-cost returns and a drawdown on a public page, (c) there are at least 5 live years including the 2024 to 2025 fall, and (d) the investor is happy to pay short-term tax on churn. I found none that meet this in public data.
- **Any smallcase whose pages show only a lock icon, a multi-year "CAGR" without dates, or marketing claims of 48%, 75%, 322%.** Treat these as ceilings.
- **Small-cap-tilted momentum products,** where the lab edge fades (lift 1.11x in micro caps) and survivorship is worst.
- **Regular-plan momentum index funds at 0.68% to 1.6% TER** and **tiny momentum index funds** (Kotak Nifty 500 Momentum 50 at Rs 24.5 cr, TE 0.34%; Baroda BNP Mom30 about Rs 22 cr agg.) with closure or tracking risk.
- **Active momentum funds as a core holding.** The oldest of the 9 AMCs' funds is about 3.3 years old, the spread of results is -7% to +27%, and Kotak's Regular plan costs 2.13%. Watch rather than buy. Revisit at 3 to 5 years, after a full drawdown.
- **Treating any momentum product as a multi-bagger finder,** or buying at the point of a recent winning streak (the best young funds started near the April 2025 trough).
- **Buying a lump sum now** on the assumption that the 2005 to 2026 "19% a year" index headline will repeat.

## 7. What I could not verify

- **Live returns, CAGR, drawdown and launch dates for current smallcases:** locked or absent on every smallcase page I opened. Tickertape snapshot numbers (Wright 3Y 48.02%, Stockstar 2Y 74.81%, Windmill 3Y 21.59%/32.41%) come only from search snippets of pages that returned 404 on direct fetch, dated to roughly 2024.
- **Complete list of momentum smallcases:** smallcase's discover page did not render. I reviewed 5 (Wright's two, Capitalmind, Stockstar, Windmill). I did not check Flameback, SMWANM, SYVMO, PREMO or others.
- **Current subscription prices and minimums** vary by page and date (Wright: Rs 200/month 2021; Rs 2,000/quarter May 2024 snapshot; Rs 4,500/6 months now). I used the current-page reading with a cheaper alternative.
- **The Capitalmind-cited "whitepaper" on 36 smallcases:** I could not find it, and its source is a seller. I do not rely on it.
- **NSE index factsheets (niftyindices.com):** all fetches timed out or returned an empty reply, so index volatility/beta/index drawdown figures come from third-party pages (dealplexus, FreeFinCal, CEIC via aggregator). The index launch date (Aug 2020) is third-party.
- **TER, AUM and tracking for all funds other than Kotak's:** from aggregators with conflicting values (e.g., Motilal Mom30 TER quoted as 0.90%, 1.01%, 1.06% and 1.08%). AMC factsheets for UTI, Motilal, HDFC, ICICI, Nippon and the active funds were not obtained.
- **ETF returns, tracking and drawdowns:** not computed. ETF TERs are from aggregator pages.
- **Drawdown numbers:** my calculation from daily NAVs through a mirror of AMFI data (spot-checked on three dates against Kotak factsheets), at most 5.6 years of history. A different definition (month-end, TRI index) can change them.
- **Tax law under the Income-tax Act, 2025:** rates for FY 2026-27 from commentary only. Section numbers unconfirmed.
- **Smallcase platform fee:** smallcase's own page (15 Jan 2026) says Rs 100 + GST on lump-sum buys (capped at 1.5%), Rs 10 + GST per SIP run, Rs 0 on rebalance/exit. Kotak Neo describes a different one-time fee. Broker charges are separate.
- **Kotak Active Momentum SIP statistics** (XIRR 17.89% vs Nifty 500 5.58%) are fund-reported, under 1 year.
- **Backtests used by managers:** I could not find any manager document that separates their live and backtested numbers with dates. This is a gap in their disclosure, not necessarily proof of wrongdoing.

## Sources

- Kotak factsheets, July 2026: [Midcap 150 Momentum 50 (one-pager)](https://www.kotakmf.com/factsheet/July_2026/kotak/Download_pdf/Kotak%20Nifty%20Midcap%20150%20Momentum%2050%20Index%20Fund_Factsheet%20One%20Pager.pdf), [Nifty 200 Momentum 30](https://www.kotakmf.com/factsheet/July_2026/kotak/Download_pdf/Kotak%20Nifty%20200%20Momentum%2030%20Index%20Fund_Factsheet%20One%20Pager.pdf), [Nifty500 Momentum 50](https://www.kotakmf.com/factsheet/July_2026/kotak/Download_pdf/Kotak%20Nifty500%20Momentum%2050%20Index%20Fund_Factsheet%20One%20Pager.pdf), [Active Momentum](https://www.kotakmf.com/factsheet/July_2026/kotak/Download_pdf/Kotak%20Active%20Momentum%20Fund_Factsheet%20One%20Pager.pdf); [August 2026 Midcap page](https://www.kotakmf.com/factsheet/August_2026/kotak/Kotak-Nifty-Midcap-150-Momentum-50-Index-Fund.html).
- AMFI NAV file and history (portal.amfiindia.com NAVAll.txt, 8 Oct 2026; NAV series via api.mfapi.in).
- smallcase pages: [Wright Momentum Model](https://www.smallcase.com/smallcase/WRTNM_0001), [Wright manager page](https://smallcase.com/manager/wright-research/smallcases/), [Capitalmind Momentum](https://www.smallcase.com/smallcase/CMMO_0001), [Stockstar](https://www.smallcase.com/smallcase/STCKMO_0001), [Windmill AA](https://www.smallcase.com/smallcase/SCMO_0044), [fees and charges (15 Jan 2026)](https://www.smallcase.com/learn/smallcase-fees-and-charges/), [Wright rebalance, 3 Oct 2022](https://www.smallcase.com/blog/rebalance-update-wright-momentum/).
- Manager commentary: Wright ([momentum](https://www.wrightresearch.in/blog/wrightmomentum), [costs, May 2021](https://www.wrightresearch.in/blog/costs/), [four years, Dec 2023](https://www.wrightresearch.in/blog/four-years-wright-momentum-successful-strategy/), [July 2026 index month](https://www.wrightresearch.in/blog/how-did-the-nifty200-momentum-30-perform-in-july-2026/)); Capitalmind ([2021 update](https://pages.capitalmind.in/posts/capitalmind-momentum-smallcase-update-what-sell-in-may-and-go-away), [sunsetting notice](https://pages.capitalmind.in/posts/important-update-sunsetting-capitalmind-smallcases), [Aug 2025](https://premium.capitalmind.in/2025/08/whats-next-for-capitalmind-momentum-the-flexi-cap-path/), [Apr 2024 smallcase guide](https://premium.capitalmind.in/2024/04/investing-best-smallcase-2024/)).
- Independent commentary: [FreeFinCal on the index](https://freefincal.com/nifty200-momentum-30-index-a-new-strategy-index-from-the-nse/), [FreeFinCal on the UTI fund](https://freefincal.com/?p=55563), [dealplexus momentum funds, 28 Sep 2026](https://www.dealplexus.com/blog/momentum-funds-india/raw), [arthgyaan HDFC page](https://arthgyaan.com/fund/hdfc-nifty200-momentum-30-index-fund-direct-growth/152430).
- Lab evidence: reports/ENGINE_FINDINGS.md, reports/FINAL.md, reports/SMALL_CAPS.md.
