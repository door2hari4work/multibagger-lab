# AB2. Independent adversarial review of the US data-centre START-SMALL list (A, B, D) - as of 2026-10-19

Research, not advice; nothing executed. Public file: no personal portfolio numbers. Prices = yfinance close 2026-10-16 (latest close; 10-year yield 5.10%, ^TNX; it was 5.24% on 10-09). Tags: FACT (source), INFERENCE (my arithmetic), unverified. Odds are labelled model estimates.
Method: primary data from SEC XBRL (data.sec.gov companyfacts, 10-Q/10-K/8-K text via fetch) and company releases; prices, 3y correlations, drawdowns and EPS history from yfinance; recomputed every ratio below. Limits: SEC_CONTACT was not set, so www.sec.gov scripted download was blocked; filings were read through a fetch tool that returns the first ~100k characters, so some notes (customer-concentration notes in EQIX/EME/HPE 10-Qs, legal notes) were not reachable. Where a fact is missing I say so. Consensus EPS (FY1) is Yahoo, taken from B.

## 1. Verdicts

| Name | A/B verdict | My verdict | One-line reason |
|---|---|---|---|
| **EQIX** | START-SMALL | **CONFIRM, with corrected claims** | Only name that diversifies the AI load (corr 0.29). But valuation is fair, not cheap; its debt-cost "strength" is wrong; FCF is negative. |
| **EME** | START-SMALL (T1 now) | **DOWNGRADE to WATCH-WITH-TRIGGER** | One-third of revenue and 84% of Q2 growth is data-centre-led "network and communications"; trailing P/E 31% above own median; B's T1 "now" contradicts its own "wait for the print". |
| **VRT** | START-SMALL gated on Q3 | **DOWNGRADE to WATCH-WITH-TRIGGER** | Highest AI co-movement (0.68) and it amplifies AI sell-offs; guidance needs ~+50% y/y in Q4; new $1.45B + $1.15B-earnout acquisition not in B; FCF flattered by prepayments. |
| **HPE** | START-SMALL (smallest) | **KILL for this sleeve** | Stock tripled in a year, trailing P/E 17.4x vs 8.0x own median (B's 22x was stale); EPS jump = Juniper + memory pass-through; data-centre networking is 3% of revenue; CEO sold ~$32M in 4 weeks; -25% in one week is a downgrade-led de-rating, not a bargain signal. |
| **NRG** | START-SMALL (smallest) | **DOWNGRADE to WATCH-WITH-TRIGGER** | Gross debt $23.3B vs cash $0.16B; H2 must deliver +29% to +55% EPS vs H2 2025 to hit guide; hyperscaler deal still not final; Texas data-centre interconnection pause (Aug 3). |
| DTCR / SRVR | WATCH-WITH-TRIGGER | **CONFIRM WATCH; redundant if EQIX is bought** | DTCR is 12.7% EQIX, 13.1% DLR, 29.5% towers, 5.6% APLD+SMCI; direct EQIX is cleaner. |
| POWR | WATCH-WITH-TRIGGER | **DOWNGRADE to WATCH (low priority)** | Top holdings include PWR/GEV/ETN that B itself rates AVOID/WATCH at today's prices; new index since 2025-10-29 (12 months of history); data-centre link indirect. |
| DLR, IRM, ORCL | WATCH | **CONFIRM WATCH** | Not re-underwritten in depth (see section 9). |

**What I would start first: EQIX only, and not before its Q3 print (Wed 2026-10-28 by pattern, unconfirmed).** Second: none now. If the investor wants a second name, EME after its 2026-10-29 print under the stricter conditions in 3.2. VRT, NRG, HPE: do not start.
**Recommended total sleeve cap: 2.25% of net worth (EQIX 1.5% + EME 0.75%), hard ceiling 2.5% even if a conditional NRG/VRT slot is later used. A, B and D together implied 5.0% for the five names (3.5% B-basket + 1.5% EQIX) plus fund add-ons.**
Why smaller: the original five-name sleeve has 0.71 correlation to the AI basket (0.66 to a holdings-weighted version), 0.71 in the basket's worst 10% days, and a 3y max drawdown of -37% for the sleeve. My two-name sleeve: 0.51, 0.53, -26%. A sleeve that mostly adds AI beta is not "diversification" of the existing AI exposure.

## 2. Corrections to the source reports (what I could not reproduce)

| # | Report claim | What I found | Impact |
|---|---|---|---|
| 1 | A: EQIX debt cost "new paper at 4.4-4.7% below the 10y... a strength" | FACT (8-K 2026-08-06): USD notes sold 2026-08-06 at **5.000% 2029, 5.500% 2033, 5.800% 2036**; a EUR-swapped 2031 tranche at 5.25% USD (~3.95% after swap). New $5.5B unsecured revolver 2026-07-27. The March 4.4-4.7% notes I could not verify. | Marginal USD debt cost is at or above the 10y and **above the 4.36% AFFO yield**: debt-funded growth is negative-carry on day one. |
| 2 | A: EQIX H1 FCF -$560M | FACT (XBRL 10-Q): operating cash flow $1,784M minus PP&E purchases $2,834M = **-$1,050M** (-$702M after $348M asset-sale proceeds), plus $1,029M dividends paid. | Funding gap is bigger; ~$3B/yr of new debt (capex $5.5B + dividends $2.04B - AFFO $4.27B at guide midpoints, INFERENCE). |
| 3 | A: EQIX "~9% cheaper than own median (22.9x vs ~25x)" | Own history (see 4): 22.9x vs median 23.0-23.4x. **In line, not cheap.** | "Good valuation" claim fails; it is fair value. |
| 4 | B: HPE trailing P/E 22.1x vs own 7.1x; T1 buy at <=$56 | Yahoo TTM lacked FQ3 ($1.11). TTM adj EPS = 0.62+0.65+0.79+1.11 = $3.17 -> **17.4x**; own median 8.0x. T1 ($56) is already triggered at $55.13 (stock -25% Oct 9-15). | Mechanical plan says buy into a falling knife. |
| 5 | B: EME data-centre share "unverified"; T1 "now to $740" | FACT (10-Q): see 3.2. T1 "now" is before the Oct 29 print; B's own text says "wait for the print, not a dip". | Internal contradiction; I removed it. |
| 6 | B: VRT print date conflict (21 vs 28 Oct) | FACT (company release 2026-10-14): **Wed 2026-10-28, before market open**. EME: **Thu 2026-10-29 BMO** (release 2026-10-15). | Resolved. |
| 7 | B: VRT acquisitions | Missed: 8-K 2026-09-02 merger for UtilityInnovation Group, **$1.45B cash + up to $1.15B earnout** (EBITDA-based; ~13x 2027 EBITDA per company); 8-K 2026-09-24 King Environmental Services. Both close Q4 2026. | Net cash disappears; earnout and goodwill risk. |
| 8 | B: NRG ND/EBITDA 7.2x (Yahoo) | Debt+leases $23.26B, cash $0.16B vs 2026 EBITDA guide $5.325-5.825B = **4.1x** (gross of recourse split; includes $2.3B receivables facility). 7.2x overstated; but not "safe". | Corrects up and down. |
| 9 | B: NRG "tracking below midpoint" | The Q2 release (8-K 2026-08-04) **reaffirms** guidance and does not say that; the phrase came from a call summary. I show the H2 arithmetic instead (4.4). | Unverified claim removed. |
| 10 | B/D correlation headline 0.26-0.47 | That is the average of six pairwise numbers. Against the equal-weight AI basket (the right test for an AI-loaded investor): EQIX 0.29, EME 0.58, VRT 0.68, HPE 0.47, NRG 0.49. | Four of five names are AI-correlated. |
| 11 | A: no mention of AFFO-metric history | EQIX was the target of a March 2024 short report on its AFFO accounting; SEC closed its probe without action; a securities class action (Chan v. Equinix) was reportedly settled for $41.5M (year unverified). | P/AFFO rests on a metric once challenged. Not a 2026 event. |
| 12 | D: EQIX ND/EBITDA 4.9x (yfinance) vs A 3.8x | 3.6x on Q2 annualised EBITDA, 3.8x on FY26 guide, ~4.2x on FY25 (revenue x 51%, my estimate). Use 3.8x forward / 4.2x trailing. | Reports disagreed. |

## 3. Per-name re-verification

### 3.1 EQIX (price $985.98, mkt cap ~$97.3B on 98.67M shares, 10-Q cover 2026-07-28)
Facts re-verified (FACT unless marked):
1. Q2 2026 (8-K 2026-07-29): revenue $2,625M (+16%), adj EBITDA $1,396M (53%), AFFO $1,168M (+20%), AFFO/sh $11.78 (+19%), annualised gross bookings $424M. Matches A. Release says one-time xScale fees helped but does not quantify them.
2. FY26 guide: revenue $10,205-10,285M, adj EBITDA $5,210-5,270M, AFFO $4,240-4,300M, AFFO/sh $42.69-43.29 (mid $42.99, +12.2% vs FY25 $38.33), capex $5.0-6.0B, dividends ~$2,039M.
3. Net debt: debt principal $22,153M (incl. $2,280M finance leases) less cash $979M and ST investments $1,245M = $19.9B: 3.6x Q2-annualised EBITDA, 3.8x FY26E. EV ~$117B -> EV/EBITDA 22.4x.
4. Financing: Aug 2026 USD notes 5.0-5.8%; $5.5B revolver (see table 2).
5. Concentration (10-K FY25): "No one customer made up 10% or more of revenues"; >10,500 customers; ~61% of revenue outside the US (so a USD-translation exposure). RPO ~$15.0B, ~65% recognised within two years (10-Q).
6. xScale JV: equity-method $735M, max VIE exposure $1,620M (10-Q) - matches A.
7. Events: CBO Jon Lin left (8-K 2026-07-14, effective Jul 18); routine Form 4/144 sales; short interest 1.8% of float; no new litigation or short report in 2026 found. Q3 date unconfirmed: Yahoo 10-28, AJ Bell 10-29; company pattern is the last Wednesday (07-29, 04-29) = Oct 28.
8. Power: 10-K risk factors state "power, not space, is a limiting factor in many of our IBX data centers" (supports pricing power, caps growth).

Valuation, recomputed:
| Metric | Now | Own history | Peers | Read |
|---|---|---|---|---|
| P/AFFO FY26 | 22.9x | Year-end price / next-year actual AFFO/sh: 2021 28.6x, 2022 20.4x, 2023 23.0x, 2024 24.6x, 2025 17.8x (on guide); 2021-25 median 23.0x. Oct-16 price / same-year AFFO median 23.4x. (2021-22 AFFO/sh from a secondary table: $27.11, $29.55; 2023-25 company: $32.11, $35.02, $38.33) | DLR 21.5x, IRM 19.1x, AMT 16.7x (A's guides, my division) | Fair vs itself, most expensive of the four peers |
| AFFO yield vs 10y | 4.36% vs 5.10% (-74bp) | | DLR 4.65% (-45bp), IRM 5.24% (+14bp) | Negative spread to the risk-free rate |
| EV/EBITDA FY26E | 22.4x | | DLR ~22.7x (A) | Premium |
| FCF yield | about -1% (OCF - capex negative) | | | AFFO excludes growth capex |
| Dividend yield | 2.05%, payout ~48% of AFFO | | | |
Reverse arithmetic (INFERENCE): 5-year AFFO/sh growth of 8/10/12% with exit at 18/20/22.9x gives annual price return of 2.9-6.7% / 4.8-9.0% / 8.0-12.0% before the 2% dividend. Guidance-level growth (10%) with a 3-turn de-rating (20x) = ~7% price + 2% dividend = ~9%. 12-month: AFFO/sh ~$47.3 (+10%) x 18/20/22.9/25/28x = -12%/-2%/+12%/+22%/+36% (+2% dividend). +30% needs ~27x: P(+30%) ~5%.

**Verdict: CONFIRM, as a diversifier rather than a value pick.** A's plan stands with changes: label valuation "fair"; tighten debt gates (net debt/EBITDA will drift towards 4.0x within ~12 months at ~$3B/yr of debt funding); add kill (f) below.

### 3.2 EME (price $721.66, mkt cap $31.8B, 44.11M shares)
Facts re-verified (10-Q 06-30 and release 07-30):
1. Q2 revenue $5,155M (+19.8%), operating income $547M (10.6% margin), diluted EPS $9.06 (+34.8%). FY26 guide raised: revenue $20.0-20.5B, op margin 9.5-9.8%, EPS $32.00-33.25. RPO $17,143M (+43.9% y/y; $13.0B within one year). Matches B.
2. **Data-centre share (the open question):** the 10-K defines "network and communications" as "including data centers, data and fiber projects, and cabling" and attributes the segment growth to "greater demand for data center construction projects". Q2 N&C revenue = $973M (Electrical) + $799M (Mechanical) = **$1,772M = 34.4% of revenue (H1: $3,143M = 32.1%)**, +67% y/y, and **84% of the Q2 y/y revenue increase** (77% for H1; 67% excluding the sold UK business). Revenue excluding N&C grew ~4% reported / ~9% ex-UK. (INFERENCE: N&C is a ceiling on pure data-centre revenue; it also holds telecom.) High-tech manufacturing is shrinking (-19% Q2 in Mechanical).
3. Segment margins Q2: Electrical 13.9%, Mechanical 12.5%, Building services 7.6%, Industrial 2.7%.
4. Balance sheet: cash $924M, no revolver borrowings in H1, no term debt to speak of: net cash. H1 buybacks $268M, dividends $0.40/quarter.
5. Cash conversion: H1 OCF $290M vs net income $709M. TTM FCF $1,171M (OCF $1,290M - capex $119M) = **3.7% yield** (B had 3.1%); TTM FCF/net income 81%.
6. Concentration: "largest projects ~58% of electrical and mechanical construction revenue" (10-K); no customer share disclosed in text I could read - project concentration is real even though no named customer is.
7. Events: MSHA "imminent danger" order at a subsidiary mine site (8-K Item 1.04, 2026-07-31; no injuries; immaterial in size, INFERENCE). Directors sold $0.8-2.2M each at $844-$926 in May-June. Short interest 1.7%. Last year the stock fell ~17% on a Q3 beat-and-raise (Oct 2025, search).
8. Date: **Thu 2026-10-29 before open** (company release 10-15).

Valuation: FY26 guide midpoint EPS $32.63 = 22.1x; FY27E consensus $37.4 = 19.3x; trailing 24.3x vs own median 18.6x (+31%; B said +24%); EV/EBITDA FY26E ~15x (EBITDA ~ $2.08B, my estimate); peers FIX 23.9x and PWR 31.8x FY1 (B). Cheapest of the contractors, but the whole group has re-rated. 12m scenarios: EPS27 $37.4 x 16/19.3/22/24x = -17%/0%/+14%/+25%; if growth stalls at +3% ($33.5) x 16/19.3x = -26%/-10%.
Rate sensitivity: ~0 (net cash). Correlation to AI basket 0.58 (0.61 in worst days; QQQ beta 1.09; 3y max drawdown -36%).

**Verdict: DOWNGRADE.** Quality business at a fair-to-full multiple whose growth is mostly data-centre construction. New entry: nothing before the Oct 29 print. After it, a single starter of 0.25% of net worth only if RPO >= $17.1B and book-to-bill > 1, FY26 EPS guide >= $32.00, op margin >= 10%, and price <= $740. Add 0.25% each at <= $650 (~17.4x FY27E, ~20x guide) or after two further clean prints. Cap 0.75% (B: 1.0%). Kill: RPO down q/q twice; op margin < 9.5%; N&C revenue growth < +25% y/y; a close < $540 (-25% from $721).

### 3.3 VRT (price $206.42, mkt cap $79.5B on 384.99M shares)
Facts re-verified (release 07-29, 10-Q, 10-K FY25):
1. Q2: sales $3,274M (+24%, organic +17.8%), adj op margin 22.6%, adj EPS $1.52 (+60%), adj FCF $925M, net cash, liquidity $5.6B. FACT quote: revenue timing "minor timing shifts, primarily due to temporary supply chain congestion and multi-phased project execution". The release gave no orders, book-to-bill or backlog.
2. FY26 guide: sales $13.8-14.2B (organic +30-32%), adj EPS $6.65-6.75, adj FCF $2.4-2.6B. Q3 guide: sales $3.65-3.85B (organic +34-36%), adj EPS $1.77-1.83.
3. **What the guide implies (INFERENCE):** H1 sales $5.92B + Q3 $3.75B leaves **Q4 ~$4.33B = +50% y/y and +15% q/q** (FY25 Q4 $2.88B). Implied Q4 adj EPS ~$2.21 (+62%).
4. Cash flow quality: current deferred revenue rose from $1,815M (Dec) to $3,634M (Jun): **+$1.82B of customer prepayments in six months**; H1 OCF $1,867M vs net income $888M. TTM FCF $2.93B (3.7% yield) is flattered; guide $2.5B = 3.1%. Prepayments reverse as units ship.
5. Backlog $15.0B at 2025-12-31 vs $7.2B (+108%), majority firm for 12-18 months (10-K). 2025 sales by region: Americas 62%. Customer concentration: no customer percentage disclosed (INFERENCE: none >=10%); 10-K says large customers are "a material portion" and warns of "less leverage with large customer contract terms".
6. Balance sheet: debt $2.94B, cash $2.81B (net debt ~$0.1B). After UtilityInnovation ($1.45B cash at close, up to $1.15B more on 12/24-month EBITDA targets) and King: net debt ~$1.5B+ (0.4x), goodwill already $2.28B and a PurgeRite earnout liability of $206M with $62M of H1 losses.
7. Legal/events: securities class action (S.D.N.Y. 22-cv-3572, 10(b) claims still pending); SEC concluded its investigation without action (2025-12-30). Director Monser sold $3.9M at ~$250 (2026-09-01). Short interest 3.7% of float. Stock -15% in the last 5 sessions, -46% from the $379.93 high, 3y max drawdown -61% (5y -70%), vol 63%.
8. Date: **Wed 2026-10-28 before open**.

Valuation: 30.8x FY26 adj EPS ($6.70), 22.5x FY27E ($9.17, +36%), 35x on GAAP guide ($5.87); EV/EBITDA FY26E ~22x (adj op profit $3.3B + ~$0.25B depreciation, my estimate); trailing 39.0x vs own median 41.0x (a hypergrowth sample); peers (B) ETN 24.0x, JCI 23.7x, NVT 21.1x, Schneider 19.9x FY1: roughly in line with peers for faster growth. 12m scenarios on EPS27 $9.17 x 16/20/22.5/26/30x = -29%/-11%/0%/+16%/+33%; on $7.50 (+12%) x 20/22.5x = -27%/-18%.
Correlation to AI basket 0.68 (0.65 in worst days; avg -5.2% when the basket loses -3.2%; QQQ beta 2.0).

**Verdict: DOWNGRADE.** It is the best business of the four, but for this investor it is the most expensive way to add AI beta. Start only if (a) Q3 (Oct 28) delivers sales >= $3.65B and holds the FY guide, with orders/backlog disclosed growing faster than sales, (b) price <= $190 (~20.7x FY27E), and (c) it is funded by trimming existing AI weight (it is a swap, not an addition). Cap 0.5% of net worth (B: 1.0%). Kill: Q3 sales < $3.65B or FY cut; backlog flat/down; adj op margin < 22%; a named hyperscaler cuts 2027 capex; close < $155.

### 3.4 HPE (price $55.13, mkt cap $73.2B, 1.327B shares)
Facts re-verified (8-K/exhibit 2026-09-02, 10-Q 07-31):
1. FQ3 revenue $12.2B (+34%), non-GAAP EPS $1.11, non-GAAP op margin 16.2%, non-GAAP gross margin 40.4% (29.9% a year earlier). Server $6.8B (+35%), Networking $2.9B (+75%; routing $788M vs $213M, **Data Center Networking $382M vs $180M = 3.1% of group revenue**), Storage $1.3B, Financial Services $0.9B.
2. Guide: FY26 revenue +34-37%, non-GAAP EPS $3.75-3.85, FCF >= $3.75B; Q4 revenue $13.9-14.8B (+44% to +53% y/y vs $9.68B), EPS $1.20-1.30. FY27 framework: revenue +13-17%, non-GAAP EPS +16-20% (= $4.41-4.56), FCF >= $5.0B.
3. Quality: networking comparisons include Juniper (closed July 2025; first fully clean comparison is FQ1 FY27); inventory $11.8B vs $6.4B at Oct 2025, payables $13.7B vs $7.7B (10-Q) - working capital doubled. Barclays (2026-10-14, Equal Weight, PT $77 from $83, forecasts unchanged) argued enterprise revenue strength reflects memory-price pass-through more than enterprise AI.
4. Price path: 1y ago $22.96, high $73.56 (Oct 9), -25% since. HPE fell 8.3% on Oct 14 and 7.1% on Oct 15 (Trefis); Dell -11% same day.
5. Insiders (Form 4, yfinance): CEO sold 250,000 shares at $60.44 (Sep 11, $15.1M) and 250,000 at $68.31 (Oct 5, $17.1M); another officer exercised 1.12M options ($46M) in July and sold; a director sold at $56.91. Plan status (10b5-1) unverified.
6. Net debt ~$14.0B incl. financing arm ($20.2B debt - $6.2B cash); ex-financing unverified. 9M FCF $2.58B (company).
7. Short interest 4.3% of float; no company-specific litigation or short report found. Next print early December (date unconfirmed). Dividend $0.1425/quarter (1.0%).

Valuation: FY26 14.5x ($3.80), FY27E 11.7x on consensus $4.71 but **12.2x on the company's own framework ($4.5)** - consensus sits above the top of management's range; trailing 17.4x vs own median 8.0x (realised-forward median 7.7x); FCF yield 5.1% (FY26 guide) / 6.8% (FY27 floor); peers DELL 16.9x, NTAP 18.3x FY1. Cheap only against AI-server peers; **2.2-2.4x its own history**. 12m scenarios on EPS $4.5 x 8/10/12.2/14/16x = -34%/-17%/+1%/+15%/+32%; on flat $3.80 x 10/12x = -30%/-16%.
Correlation to AI basket 0.47 (QQQ beta 1.26), 3y max drawdown -48%.

**Verdict: KILL for the data-centre sleeve.** No evidence that its profits are data-centre-driven (3% of revenue in DC networking; AI-server share undisclosed), margins at a peak inflated by acquisition and memory pricing, own-history multiple doubled, insider selling at higher prices, and the stock is in a violent de-rating with the catalyst six weeks away. It can re-enter the general watchlist at <= $45 (10x FY27 framework EPS) or after FQ1 FY27 shows organic networking growth and gross margin holding. Do not use the "T1 <= $56" rule.

### 3.5 NRG (price $103.75, mkt cap $21.8B on 210.2M shares)
Facts re-verified (8-K 2026-08-04, 10-Q 06-30, 8-K 2026-07-15):
1. Q2 adj EBITDA $1,217M (vs $909M), adj EPS $1.49 (vs $1.73), adj net income $315M, GAAP net income $506M. FY26 guide reaffirmed: adj EBITDA $5,325-5,825M, adj EPS $7.90-9.90, FCFbG $2.8-3.3B.
2. Balance sheet: cash $162M (vs $4,708M in December); debt + finance leases $23.26B (current $1.5B); liquidity $5.3B; $650M 10.25% perpetual preferred; shares issued rose to 225M (LS Power closed ~2026-01-30, stock partly used); 210.2M outstanding after buybacks ($932M of ~$1.0B plan done by Jul 31).
3. Leverage (INFERENCE): $23.1B net / $5.575B = 4.1x; EV ~$45.6B -> 8.2x guide EBITDA (B: 14.1x on TTM). The release gives no net-debt ratio or target; B's "3x pushed to 2029" is from a call summary, unverified.
4. **H2 arithmetic:** reported adj EPS H1 = $2.98. Guide midpoint needs H2 = $5.92 (+55% vs H2 2025's $3.82); low end needs $4.92 (+29%). Texas EBITDA fell $131M in Q2 (weather -30% heating degree days, higher supply costs); East rose $370M on LS Power/CPower.
5. Company FCFbG ($2.8-3.3B, = 13-15% of market cap) is a non-GAAP measure. GAAP TTM OCF $1,555M - capex $1,207M = **$348M (1.6% yield)**; interest expense ran $595M in H1.
6. Hyperscaler: "aligned on principal commercial terms" for 1.2 GW combined-cycle in Texas, subject to documentation and approvals (release); secondary: 15-year minimum, parent guarantee, >95% capacity payments, late-2029 delivery. **Not final ten weeks after announcement.** Texas Governor's 2026-08-03 directive to audit data-centre projects and pause interconnections (law-firm alerts, no end date) is a direct risk; B only listed it under Vistra.
7. PJM 2028/29 auction: NRG cleared 6,839 MW at $325/MW-day (8-K 2026-07-15) - a real positive. Director/officer activity: one officer sold $0.19M (Sep 8). Short interest 3.9%.
8. Date: unconfirmed, Nov 5 (TipRanks, pattern) or Nov 9 (Earnings Whispers); Q3 consensus ~$3.5 vs $2.78 last year.

Valuation: 11.7x FY26 guide mid, 9.3x FY27E ($11.16); trailing 15.3x vs own median 13.0x; peers VST 14.7x, CEG 20.4x, TLN 11.4x (B). 12m scenarios on EPS27 $11.16 x 7/8/9.3/11/13x = -23%/-12%/+2%/+20%/+42%; if EPS27 only equals the 2026 midpoint ($8.90) x 8/9.3x = -30%/-18%.
Correlation to AI basket 0.49 (worst days 0.56), rate beta ~0, 3y max drawdown -48%.

**Verdict: DOWNGRADE.** Cheap on forward earnings that include a $7B debt-funded acquisition and an unsigned deal; its profits are mostly retail/generation, not data-centre. Start condition: Q3 print reaffirms guide with YTD adj EPS on a path to >= low end, hyperscaler agreement signed (terms as described), and no Texas rule that blocks the site; price <= $105. Cap 0.5%. Kill: guide cut below $5.325B; deal abandoned; Texas/PJM rule voiding co-location; corporate leverage target pushed beyond 2029.

## 4. "Good valuation" check, side by side (prices 2026-10-16)
| | Fwd P/E or P/AFFO | Own 5y history | vs peers | EV/EBITDA FY26E | FCF yield | ND/EBITDA | Is it good value? |
|---|---|---|---|---|---|---|---|
| EQIX | 22.9x AFFO | median 23.0-23.4x | dearest REIT (DLR 21.5, IRM 19.1, AMT 16.7) | 22.4x | ~-1% | 3.8x (4.2x TTM) | Fair. Yield 74bp below 10y. |
| EME | 22.1x guide / 19.3x FY27E | trailing 24.3x vs 18.6x | cheapest contractor, group re-rated | ~15x | 3.7% | net cash | Fair-to-full |
| VRT | 30.8x / 22.5x | trailing 39.0x vs 41.0x | in line with ETN/JCI/NVT | ~22x | 3.7% TTM, 3.1% guide | ~0.1x (0.4x pro forma) | Fair for growth; growth must hit |
| HPE | 14.5x / 12.2x (framework) | trailing 17.4x vs 8.0x | cheap vs DELL/NTAP only | n/c | 5.1% FY26, 6.8% FY27 | ~2x incl. financing arm (unverified) | **No: 2.2x own median** |
| NRG | 11.7x / 9.3x | trailing 15.3x vs 13.0x | cheapest vs VST/CEG | 8.2x | 1.6% GAAP; 13-15% non-GAAP | 4.1x | Cheap, with leverage and execution risk |
Own-history method: price on each earnings date divided by trailing four reported (adjusted) EPS from yfinance, 20 reports since Oct 2021; realised-forward = price over the next four reports (hindsight). EQIX uses AFFO/sh as in 3.1. These are yardsticks, not forward-multiple histories.

## 5. Rate sensitivity at a 5.1-5.2% 10-year
- FACT: 10y 5.10% (Oct 16), 5.24% (Oct 9). This week's sell-off came with yields falling 14bp: it was a credit/AI-hardware de-rating (Barclays downgrade of Dell/HPE Oct 14, AI-financing worries Oct 16), not a rates move.
- Weekly return vs weekly change in the 10y, 3y/5y OLS: EQIX -7.3%/-7.9% per +100bp, DLR -6.2%/-7.3%, IRM -8.8%/-7.3%, DTCR -7.0%/-7.3%, SRVR -8.9%/-8.7% (R2 low, 0.04-0.18). EME, VRT, HPE, NRG: not significant (AI factor dominates).
- Constant-spread arithmetic (INFERENCE): EQIX AFFO yield 4.36%. If the spread to the 10y stays and yields +100bp, the multiple goes to ~18.7x (-18%); with half pass-through ~20.6x (-10%). In the 2021-11 to 2022-12 shock (10y 1.3% -> 4.2%) EQIX fell 39%, DLR 48%, DTCR 39%.
- Kill/pause: 10y > 5.5% pauses any REIT tranche; > 5.75% = stop (A's trigger). FOMC 2026-10-27/28 (lab report F) lands the same week as VRT, EQIX, EME and DLR prints.

## 6. Does the sleeve diversify the existing AI exposure? (3y daily, to 2026-10-16)
| | Corr to AI-6 (equal-wt MSFT, GOOGL, AMZN, NVDA, TSM, MU) | Corr, basket's worst 10% days | Avg return those days (basket -3.2%) | QQQ beta | 3y max DD |
|---|---|---|---|---|---|
| EQIX | 0.29 | 0.32 | -1.1% | 0.47 | -25% (5y -39%) |
| EME | 0.58 | 0.61 | -2.5% | 1.09 | -36% |
| VRT | 0.68 | 0.65 | -5.2% | 1.99 | -61% |
| HPE | 0.47 | 0.52 | -2.7% | 1.26 | -48% |
| NRG | 0.49 | 0.56 | -2.7% | 1.05 | -48% |
| DTCR / SRVR / POWR | 0.65 / 0.38 / 0.41 | 0.39 / 0.22 / 0.43 | -1.9 / -1.0 / -1.1% | 0.77 / 0.43 / 0.43 | -25 / -20 / -23% |
| Sleeve: original (EQIX 1.5, EME 1, VRT 1, HPE .75, NRG .75) | 0.71 | 0.71 | -2.7% | | -37% |
| Sleeve: proposed (EQIX 1.5, EME .75) | 0.51 | 0.53 | -1.6% | | -26% |
| EQIX alone | 0.29 | 0.32 | -1.1% | | |
Reading: only EQIX (and REITs generally) diversifies. Everything else is the same AI-capex trade at 1-2x volatility. POWR's 3y numbers are for the pre-October-2025 index; the new index has 12 months of history. Funding rule: EME/VRT/NRG should be funded from trims of existing AI positions or accepted as AI-theme additions.

## 7. Missed events and calendar (next 2 weeks and beyond)
| Date | Event | Status |
|---|---|---|
| Mon Oct 19 | No new filings found for the five names since Oct 16 | checked EDGAR submissions |
| Oct 27-28 | FOMC | per lab report F |
| **Wed Oct 28** | **VRT Q3 (BMO, 11am ET call)**; EQIX Q3 after close (pattern; Yahoo agrees; unconfirmed) | VRT FACT |
| **Thu Oct 29** | **EME Q3 (BMO, 10:30 ET)**; DLR Q3 after close (A) | EME FACT |
| ~Nov 5 or 9 | NRG Q3 | unconfirmed |
| Nov 19 | Nvidia (B) | |
| early Dec | HPE FQ4 and FY27 detail | unconfirmed |
| Q4 2026 | VRT closes UtilityInnovation and King; EQIX and DLR financings | |
Other searched, none found: guidance cuts at the five names, short-seller reports in 2026, new litigation (EQIX, EME, HPE, NRG: none new; VRT: pending 2022 class action). Insider/financing items are in section 3. Not verified: whether the HPE CEO sales are under a 10b5-1 plan; EQIX/EME/HPE/NRG legal-proceedings notes (not reachable in the fetched text).

## 8. Plan changes (replace the A/B entry plans)
**EQIX (cap 1.5% of net worth, 3 tranches of 0.5%)**
- No purchase before the print. T1 (0.5%): the first session after Q3 results if FY26 AFFO/sh guide midpoint is held or raised, organic AFFO/sh growth guide >= 8%, and price <= $1,020 (23.7x). If it gaps above $1,020, wait; do not chase.
- T2 (0.5%): at least 4 weeks after T1 and only at <= $940 (21.9x, AFFO yield 4.6%) or after the Q4 print (mid-Feb 2027) with guide intact.
- T3 (0.5%): after Q1 2027 print (late April), only if net debt/EBITDA <= 4.2x, 10y <= 5.5%, and price <= $1,050.
- Accumulate only if guide holds and new unsecured USD issuance prices <= 6.0%. Trim above 27x FY26 AFFO (~$1,160) or if > 2.0% of net worth.
- Kill (any one): FY26 AFFO/sh midpoint cut or organic growth guided < 8%; adj EBITDA margin guide < 51%; net debt/EBITDA > 4.5x; two quarters of falling net interconnection adds; a new AFFO-accounting inquiry or restatement; a close below ~$760 (-23%) = mandatory exit/review.
- Worst-case loss: 1.5% x 39% (5y max) = **0.59pp of net worth**; if the -25% exit rule is honoured, 0.38pp.
- Odds (model estimates, 12m): P(+30% price) ~5%; P(total return >= +10%) ~45%; P(ends <= -25%) ~3-5%; P(touches -25%) ~15-25% (empirical 16% of 12m windows in 5 years; zero-drift volatility model 27%).

**EME (cap 0.75%)**: as in 3.2; first tranche no earlier than the first session after Oct 29. Odds: P(+30%) ~20%; P(touch -25%) 30-45% (volatility model 47%; the empirical 7% comes from a bull sample and is not usable).
**VRT (cap 0.5%), NRG (cap 0.5%)**: only the conditional starters above, never both together with EME unless total stays <= 2.5%. Odds: VRT P(+30%) ~25%, P(touch -25%) ~60%; NRG P(+30%) ~25%, P(touch -25%) ~45%.
**HPE**: removed.
**Staging pace**: about one tranche every 4-8 weeks, aligned to quarterly prints (late Oct/early Nov, mid-Feb, late Apr). Timing states carry no return edge in the lab; staging here is for event risk and for the leverage/rates gates, not alpha.
**Sleeve cap**: 2.25% of net worth normal, 2.5% hard. Loss arithmetic at historical drawdowns: EQIX 0.59pp + EME 0.75% x 36% = 0.27pp = **0.86pp**; with a conditional 0.5% in VRT at -61% add 0.31pp. Money-invested limit (20-25%): none of these names has stayed inside it historically without an exit rule, so the -25% exit trigger must be a hard order discipline, and gap risk around prints remains.

## 9. Funds and watch names
- **DTCR** (Global X, FACT 2026-10-16): AUM $1.95B, ER 0.50%, 25 holdings, 30-day SEC yield 1.50%, semi-annual distributions, -21% from 52w high, 5.8% below its 200d MA, NAV discount 0.3%. Weights: AMT 14.4, DLR 13.1, EQIX 12.65, CCI 10.2, SBAC 4.9, Keppel DC REIT 4.4, GDS 3.4, NEXTDC 3.3, APLD 3.1, SMCI 2.6. Towers 29.5%, DLR+EQIX 25.8%, AI-hardware/neocloud (APLD+SMCI) 5.6%. Corr to AI basket 0.65 overall but 0.39 on worst days. If EQIX is bought, DTCR duplicates 12.7% of itself; count both inside one 1.5% REIT cap. Verdict WATCH-WITH-TRIGGER stands (D's 200d-MA trigger or <= 18x REIT-core P/AFFO).
- **SRVR**: AUM ~$320M, -21% from high, 11.7% below 200d MA, yield TTM 4.9% includes a $0.64 Sep distribution (return of capital split unverified). Lowest worst-day correlation (0.22). WATCH.
- **POWR**: AUM ~$425M, ER 0.39% (yfinance; D said 0.40%), top holdings ETN 6.6, PWR 6.5, GEV 6.3, NEE 5.8, EQT 4.5, SO 4.0, NVT 3.8, DUK 3.7, CEG 3.5, HUBB 3.5; B rates PWR and GEV AVOID at current prices. TTM yield 6.4% is distorted by a $1.35 Dec-2025 distribution (current quarterly ~$0.08 = 1.3%). Downgrade to WATCH, low priority.
- **DLR / IRM / ORCL (not re-underwritten)**: price-based checks only. DLR 21.5x core FFO mid (A's guide), AFFO yield 4.65% (-45bp vs 10y), print Oct 29 after close; IRM 19.1x, yield 5.24% (+14bp), Q2 call reported a $1.5B 6.25% 2035 bond (search, unverified) and Groupe ATF closing 2026-08-01, so its marginal debt costs 6%+; ORCL $128.23, no new primary data. Keep A's triggers.

## 10. Remaining uncertainties
1. EQIX 2021-22 AFFO/sh come from a secondary table; Q3 date unconfirmed. 2. EME N&C is a ceiling on data-centre revenue (includes telecom/fibre). 3. VRT orders/backlog since December not seen in the fetched release. 4. HPE net debt excluding financing arm, FY27 consensus and insider-plan status unverified. 5. NRG corporate vs non-recourse debt not split in the text I could read; 3x-by-2029 target is second-hand. 6. Tax: US withholding on REIT dividends for an Indian resident, Indian slab/LTCG treatment (12.5% after 24 months per D), LRS/TCS, US estate-tax exposure on US-listed holdings: not verified; verify with a CA. Employer pre-clearance: verify with HR. 7. All odds are model estimates; backtests and the 5-year samples are survivor- and bull-market-inflated; 5x outcomes are not expected from any name here.
