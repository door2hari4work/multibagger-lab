# 06 - Named, SEBI-registered managers on Zerodha (Kite): who can you actually buy, and is any worth it?

Prepared 2026-10-09 for an investor using Zerodha/Kite, about Rs 1 lakh staged over 4 to 6 months, loss tolerance about 25% of money invested, wanting a named and checkable SEBI-registered manager and exposure to autos, power/grid/energy, capital goods/manufacturing, consumption, banks/financials, infrastructure or a diversified mix. Builds on `02_landscape.md` and `03_managers.md`. All smallcase numbers below were pulled from smallcase's public JSON API and pages on 2026-10-09 (series to 2026-10-08). Nothing was filled from memory; where I could not establish something it says so.

## Verdict

**There is not a named-manager basket I would consider on Zerodha for this brief.** Reasons, in order of weight:

1. **Almost nothing from named managers is on Kite.** Of 544 reachable baskets, 73 show `brokerMeta.status = PUBLISHED` for kite. 55 are Windmill (excluded by your rule, and the platform's own affiliate with no named analysts) and 9 are Zerodha Fund House ETF-of-ETF baskets (1.0 to 1.5 years old, not stock baskets). That leaves **9 baskets from 4 named managers** (Wright 2, Green Portfolio 2, WeekendInvesting 4, Estee 1). 77 of the 83 publishers have no basket on Kite at all.
2. **None of those 9 is a sector basket** in your list (autos, power, capital goods, consumption, banks, infra). They are momentum, multi-factor, quality/value or MNC baskets.
3. **The one basket that fits your sector brief, Wright New India Manufacturing, is not buyable on Kite on every test I could run** (section 4): kite status UNPUBLISHED since launch day, absent from smallcase's search when the request is made in the Kite context, and Zerodha's own smallcase web app (smallcase.zerodha.com) is coded to show "Request Invite" instead of "Invest" for a fee-based basket that has no `kite` distributor entry, which is Wright New India's case. I could not test a live purchase from a Zerodha account.
4. **Fees swamp a Rs 1 lakh ticket.** The viable baskets charge Rs 7,200 to Rs 8,100 a year, 7.2% to 8.1% of Rs 1 lakh, so you need roughly 8% to 12% a year of excess return over a Nifty 500 holding just to break even after fee, trading cost and short-term tax (section 5). At Rs 2 lakh that falls to roughly 4% to 8%.
5. **A repeat of the worst drawdown plus one year of fee breaks your 25% limit** for all three best candidates at Rs 1 lakh (Rs 28,200 to Rs 30,800 lost against Rs 25,000 allowed). The fee alone uses 29% to 32% of the loss budget before the market moves.

**What would change my answer:** (a) Wright publishes New India on Kite, or you accept opening an account at one of the four brokers where it is PUBLISHED, and you can put in about Rs 2 lakh or more; (b) you treat the loss limit as market drawdown only and exclude fees; (c) you want a diversified quality/value satellite rather than a sector tilt, in which case the only one I would look at is Green Portfolio High Quality Right Price (`GPRMO_0003`), at Rs 2 lakh or more and sized as a satellite (section 3). Even then I would first check the registration on SEBI's own register, which I could not do (see 03_managers.md).

## 1. What was done

- **Enumeration.** `www.smallcase.com/smallcases-sitemap.xml` lists 603 smallcase URLs (43 are `MF_` baskets). I called `api.smallcase.com/smallcases/smallcase?scid=<id>` for the other 560, one request at a time with a 0.35 second pause (about 1.3 requests a second, roughly 7 minutes in total). **544 returned data**; 16 US baskets (`SCUS*`, `SKUPAUSMX_0001`, `LTDUSFAM_0001`) return "Request to SME service failed" and are excluded. 
- **Per-basket fields** (all in the CSV): scid, name, publisher, SEBI number from the publisher's `smallcase.com/manager/<id>` page (all 83 publisher pages fetched; the number is as shown there and is not checked against SEBI), theme (inferred from name and strategy tags, so approximate), launch date (`publishedOnDate`), series start (`uploaded`), kite status, whether a `kite` entry exists in `distributorMeta`, minimum investment, subscription plans, fee as % of Rs 1 lakh and Rs 2 lakh (1-year plan), rebalance frequency, stocks, cap mix, PE, platform CAGR and 1y/2y/3y CAGR, performance-verified flag. Full table: **`reports/smallcase/06_all_baskets.csv`** (544 rows, Windmill first).
- **Series.** For the shortlisted baskets I pulled `smallcases/historical?scid=<id>&duration=max&benchmarkId=.NIFTY500` and `smallcases/rebalances?scid=<id>`. Sampling is every 18 to 38 days (5 to 7 days for the Zerodha baskets), so drawdowns are understated. Returns are price-only and before trading cost and tax.
- **Not done:** SEBI's register could not be queried (blocked in the earlier work; I did not retry). I did not log in to Zerodha or smallcase, so holdings, weights and a live "Invest" click were not available.

### 1a. What the 544 look like

| Fact | Count |
|---|---|
| Baskets reachable | 544 (83 publishers) |
| kite `PUBLISHED` | 73 (13.4%) |
| kite `UNPUBLISHED` | 471 |
| Windmill (publisher id `smallcaseHQ`) baskets | 60, of which 55 PUBLISHED on kite |
| Non-Windmill baskets | 484, of which 18 PUBLISHED on kite (3.7%) |
| Non-Windmill, kite PUBLISHED, live at least 3 years | 9 |
| Non-Windmill baskets with a fee plan ("private") | 463 of 484; only 9 of them are on Kite |
| Publishers with at least one kite PUBLISHED basket | 6 of 83: Windmill, Zerodha Fund House, WeekendInvesting, Green Portfolio, Wright Research, Estee |

Largest publishers (basket count, kite PUBLISHED): Windmill 60 (55); Quantace 38 (0); Ethical Advisers 23 (0); Compounding Wealth Advisors 20 (0); Growth Investing 15 (0); Omniscience 14 (0); Green Portfolio 13 (2); Bullcapital 11 (0); WeekendInvesting 11 (4); Wright Research 9 (2). Every Quantace, Niveshaay, CWA, Ethical Advisers and Omniscience basket on the earlier shortlist is UNPUBLISHED on kite, which also removes most of the sector baskets in `02_landscape.md` for a Zerodha investor.

## 2. The 18 non-Windmill baskets that are PUBLISHED on kite

### 2a. Structure and cost

| scid | Basket | Publisher (SEBI no. per manager page) | Theme | Launched | Series yrs | Min invest Rs | Plans Rs (6m / 1y) | Fee 1y as % of Rs 1L / 2L | Rebalance | Stocks | Cap mix L/M/S % | PE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ESTMO_0001 | Gulaq Gear 6 Quant | Estee (INH000019503, RA) | Quant multi-factor, BSE 500 | 2020-05-11 | 6.4 | 24,000 | 3500 / 5900 | 5.9% / 3.0% | monthly | 15 | 27/23/50 | 12 |
| GPRMO_0003 | High Quality Right Price Theme | Green Portfolio (INH100008513, RA) | Value/quality; Atmanirbhar-PLI universe, pharma/chem tilt | 2020-03-20 | 6.5 | 32,041 | 5450 / 8100 | 8.1% / 4.0% | quarterly | 17 | 8/18/70 | 32 |
| GPRNM_0001 | Emerging Global Giants - Global Companies Theme | Green Portfolio (INH100008513, RA) | Indian-listed MNCs | 2021-02-18 | 5.6 | 111,378 | - / 3540 | 3.5% / 1.8% | quarterly | 14 | 0/13/68 | 36 |
| WKIMO_0009 | MI NNF10 Momentum Model | Weekend Investing (INH100008717, RA) | Momentum, Nifty Next 50 | 2020-11-12 | 5.9 | 90,117 | - / 9999 (3m 3334) | 10.0% / 5.0% | monthly | 10 | 100/0/0 | 24 |
| WKIMO_0017 | Mi 20 Momentum Model | Weekend Investing (INH100008717, RA) | Momentum, mid/small | 2021-07-15 | 5.2 | 160,962 | - / 14999 (3m 4999) | 15.0% / 7.5% | weekly | 20 | 5/25/70 | 61 |
| WKIMO_0019 | Mi EverGreen Momentum Model | Weekend Investing (INH100008717, RA) | Momentum + 25% gold | 2021-12-26 | 4.8 | 246,596 | - / 14999 (3m 4999) | 15.0% / 7.5% | monthly | 21 | 34/41/0 | 50 |
| WKIMO_0020 | Mi INDIA Top10 Momentum Model | Weekend Investing (INH100008717, RA) | Momentum, Nifty 50 top 10 | 2022-08-04 | 4.2 | 95,523 | - / 6999 (3m 2333) | 7.0% / 3.5% | monthly | 10 | 100/0/0 | 32 |
| WRTMO_0003 | Balanced Multi Factor Model | Wright Research (INH000017295, RA) | Multi-factor, multi-asset | 2019-08-20 | 7.1 | 48,656 | 4500 / 7200 | 7.2% / 3.6% | monthly | 19 | 3/32/54 | 30 |
| WRTMO_0018 | Alpha Prime Momentum Model | Wright Research (INH000017295, RA) | Momentum, 10 stocks | 2023-06-23 | 3.3 | 28,876 | 6600 / 10000 | 10.0% / 5.0% | weekly | 10 | 24/20/56 | 47 |
| ZEFHAA_0001 | 3-in-1 Multi Asset Allocation | Zerodha Fund House (MF/080/23/06; AMC, page labels it RA) | Asset-Allocation | 2025-04-17 | 1.5 | 201 | free | 0 | quarterly | 4 | n/a | n/a |
| ZEFHAA_0002 | Gold & Debt Asset Allocation | Zerodha Fund House (MF/080/23/06; AMC, page labels it RA) | Asset-Allocation | 2025-04-17 | 1.5 | 100 | free | 0 | quarterly | 2 | n/a | n/a |
| ZEFHAA_0003 | Midcaps & Gold Asset Allocation | Zerodha Fund House (MF/080/23/06; AMC, page labels it RA) | Asset-Allocation | 2025-04-17 | 1.5 | 56 | free | 0 | quarterly | 2 | n/a | n/a |
| ZEFHAA_0004 | Equity & Precious Metals Asset Allocation | Zerodha Fund House (MF/080/23/06; AMC, page labels it RA) | Asset-Allocation | 2025-09-12 | 1.1 | 224 | free | 0 | quarterly | 4 | n/a | n/a |
| ZEFHAA_0005 | Equity & Debt 70/30 Asset Allocation | Zerodha Fund House (MF/080/23/06; AMC, page labels it RA) | Asset-Allocation | 2025-09-12 | 1.1 | 102 | free | 0 | quarterly | 3 | n/a | n/a |
| ZEFHTR_0001 | Large & Midcap Tracker | Zerodha Fund House (MF/080/23/06; AMC, page labels it RA) | Sector-Trackers | 2025-04-17 | 1.5 | 31 | free | 0 | quarterly | 2 | n/a | n/a |
| ZEFHTR_0002 | Precious Metals Tracker | Zerodha Fund House (MF/080/23/06; AMC, page labels it RA) | Sector-Trackers | 2025-04-17 | 1.5 | 46 | free | 0 | quarterly | 2 | n/a | n/a |
| ZEFHTR_0003 | Equity Multicap Tracker | Zerodha Fund House (MF/080/23/06; AMC, page labels it RA) | Sector-Trackers | 2025-09-12 | 1.1 | 32 | free | 0 | quarterly | 3 | n/a | n/a |
| ZEFHTR_0004 | Mid & Smallcap Tracker | Zerodha Fund House (MF/080/23/06; AMC, page labels it RA) | Sector-Trackers | 2025-09-30 | 1.0 | 22 | free | 0 | quarterly | 2 | n/a | n/a |

Notes: "Series yrs" is the age of the displayed series (it starts at or just after `publishedOnDate`, so I treat it as live since publication, as in 02_landscape.md; the API does not label live versus backtested). Fee % is the 1-year plan listed by the API divided by Rs 1 lakh (Rs 2 lakh). Whether GST is added to the listed subscription price is not established: smallcase's fee pages say GST applies to the platform fee, and I found nothing saying whether subscription prices include it (if GST is extra, add 18%). Green Portfolio Global Giants' cap mix sums to about 80% (rest unclassified by smallcase). The Zerodha Fund House baskets hold 2 to 4 Zerodha AMC ETFs each (minimum Rs 22 to Rs 224); the manager page lists a mutual fund registration (MF/080/23/06) under an "RA" label.

### 2b. Live record (computed by me from the smallcase series; % a year; Nifty 500 price in brackets)

| scid | Basket | CAGR since series start (Nifty 500, same window) | 3y | 2y | 1y | Max drawdown on series (N500) | Worst rolling 12m | Now vs own peak |
|---|---|---|---|---|---|---|---|---|
| ESTMO_0001 | Gulaq Gear 6 Quant | 32.3 (17.9) from 2020-05-12 | 6.2 (7.0) | -10.5 (-5.8) | -9.8 (-4.9) | -26.8 (-16.9) 2024-08 to 2026-03 | -13.9 | -20.5 |
| GPRMO_0003 | High Quality Right Price Theme | 40.8 (20.9) from 2020-03-23 | 23.5 (8.1) | 12.2 (-4.2) | 36.3 (-8.1) | -20.4 (-14.1) 2024-09 to 2025-02 | -11.1 | -1.0 |
| GPRNM_0001 | Emerging Global Giants - Global Companies Theme | 19.4 (10.3) from 2021-02-19 | 12.7 (7.8) | 0.3 (-5.0) | 2.9 (-6.7) | -16.8 (-15.3) 2024-09 to 2025-03 | -5.6 | -3.2 |
| WKIMO_0009 | MI NNF10 Momentum Model | 20.4 (13.2) from 2020-11-13 | 16.5 (7.7) | -7.9 (-5.0) | -1.1 (-7.6) | -26.1 (-13.9) 2024-07 to 2025-02 | -21.1 | -19.1 |
| WKIMO_0017 | Mi 20 Momentum Model | 17.2 (9.0) from 2021-07-16 | 4.5 (7.0) | -16.3 (-5.0) | -2.5 (-6.8) | -39.8 (-16.7) 2024-07 to 2026-03 | -30.4 | -30.1 |
| WKIMO_0019 | Mi EverGreen Momentum Model | 22.2 (8.4) from 2021-12-27 | 23.8 (7.2) | 3.2 (-6.1) | 4.4 (-6.9) | -16.2 (-16.4) 2022-04 to 2022-06 | 0.1 | -10.7 |
| WKIMO_0020 | Mi INDIA Top10 Momentum Model | 7.9 (9.3) from 2022-08-05 | 8.4 (8.1) | -13.4 (-5.8) | -12.4 (-6.9) | -25.0 (-16.2) 2024-09 to 2026-10 | -14.5 | -25.0 |
| WRTMO_0003 | Balanced Multi Factor Model | 23.2 (13.3) from 2019-08-21 | 12.7 (8.0) | -0.0 (-4.9) | 6.1 (-4.9) | -21.0 (-27.2) 2024-10 to 2025-03 | -8.1 | -5.9 |
| WRTMO_0018 | Alpha Prime Momentum Model | 23.4 (9.4) from 2023-06-26 | 16.7 (7.7) | -3.2 (-5.6) | 6.7 (-6.5) | -24.7 (-15.8) 2024-12 to 2025-02 | -14.8 | -10.1 |
| ZEFHAA_0001 | 3-in-1 Multi Asset Allocation | 9.3 (-1.2) from 2025-04-21 | n/a (n/a) | n/a (n/a) | 4.4 (-6.1) | -11.0 (-13.7) 2026-02 to 2026-03 | 4.4 | -8.0 |
| ZEFHAA_0002 | Gold & Debt Asset Allocation | 22.7 (-1.2) from 2025-04-21 | n/a (n/a) | n/a (n/a) | 18.0 (-6.1) | -12.0 (-13.7) 2026-02 to 2026-03 | 18.0 | -7.1 |
| ZEFHAA_0003 | Midcaps & Gold Asset Allocation | 17.3 (-1.2) from 2025-04-21 | n/a (n/a) | n/a (n/a) | 11.7 (-6.1) | -13.3 (-13.7) 2026-02 to 2026-03 | 11.7 | -9.2 |
| ZEFHAA_0004 | Equity & Precious Metals Asset Allocation | 9.2 (-6.5) from 2025-09-15 | n/a (n/a) | n/a (n/a) | 6.0 (-6.9) | -14.5 (-14.7) 2026-01 to 2026-03 | 6.0 | -11.2 |
| ZEFHAA_0005 | Equity & Debt 70/30 Asset Allocation | -2.5 (-6.5) from 2025-09-15 | n/a (n/a) | n/a (n/a) | -2.7 (-6.9) | -10.2 (-14.7) 2026-01 to 2026-03 | -2.7 | -6.9 |
| ZEFHTR_0001 | Large & Midcap Tracker | 1.0 (-1.2) from 2025-04-21 | n/a (n/a) | n/a (n/a) | -4.5 (-6.1) | -13.3 (-13.7) 2025-11 to 2026-03 | -4.5 | -9.0 |
| ZEFHTR_0002 | Precious Metals Tracker | 48.5 (-1.2) from 2025-04-21 | n/a (n/a) | n/a (n/a) | 35.3 (-6.1) | -22.6 (-13.7) 2026-01 to 2026-03 | 35.3 | -16.2 |
| ZEFHTR_0003 | Equity Multicap Tracker | -1.4 (-6.5) from 2025-09-15 | n/a (n/a) | n/a (n/a) | -1.2 (-6.9) | -14.4 (-14.7) 2026-01 to 2026-03 | -1.2 | -7.6 |
| ZEFHTR_0004 | Mid & Smallcap Tracker | 4.2 (-5.6) from 2025-10-01 | n/a (n/a) | n/a (n/a) | 2.5 (-6.9) | -14.1 (-14.7) 2026-01 to 2026-03 | 2.5 | -7.7 |

Window effects to keep in mind: GPRMO_0003's series starts 2020-03-23, the Covid low; Estee's on 2020-05-12; Wright Balanced on 2019-08-21. Since-start CAGRs are inflated by that start (Nifty 500 shows 21% a year over the HQRP window for the same reason). The Weekend Investing and Estee baskets trail or match the index over 2 and 3 years even before fees.

## 3. Ranking of the eligible baskets

Gates: kite PUBLISHED, non-Windmill, at least 3 years live, and minimum investment of Rs 50,000 or less so that a Rs 1 lakh budget can be staged (a Rs 90,000 minimum is one tranche). Scores 0 to 2 per criterion, rubric below the table. Rows marked "-" fail a gate but are scored for reference.

| Rank | scid | Basket | Gate: live >= 3y | Gate: min invest <= Rs 50k (can stage) | Live yrs | Method transparency (0-2) | Fee at Rs 1L (0-2) | Sector fit (0-2) | Drawdown + fee <= 25% (0-2) | Manager DD (0-2) | Net-of-fee 3y excess vs N500 at Rs 1L (0-2) | Min-invest score (0-2) | Total /16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | GPRMO_0003 | High Quality Right Price Theme | pass | pass | 6.5 | 1 | 0 | 1 | 1 (28.5% incl. fee) | 2 | 2 (+6.0 pts) | 2 | 11 |
| 2 | WRTMO_0003 | Balanced Multi Factor Model | pass | pass | 7.1 | 1 | 1 | 1 | 1 (28.2% incl. fee) | 2 | 0 (-4.0 pts) | 2 | 10 |
| 3 | ESTMO_0001 | Gulaq Gear 6 Quant | pass | pass | 6.4 | 1 | 1 | 1 | 0 (32.7% incl. fee) | 1 | 0 (-8.2 pts) | 2 | 8 |
| 4 | WRTMO_0018 | Alpha Prime Momentum Model | pass | pass | 3.3 | 1 | 0 | 1 | 0 (34.7% incl. fee) | 2 | 0 (-2.7 pts) | 2 | 7 |
| - | GPRNM_0001 | Emerging Global Giants - Global Companies Theme | pass | FAIL (Rs 111,378) | 5.6 | 1 | 2 | 1 | 2 (20.3% incl. fee) | 2 | 1 (+0.6 pts) | 0 | 11 |
| - | WKIMO_0009 | MI NNF10 Momentum Model | pass | FAIL (Rs 90,117) | 5.9 | 2 | 0 | 1 | 0 (36.1% incl. fee) | 1 | 0 (-2.9 pts) | 1 | 7 |
| - | WKIMO_0020 | Mi INDIA Top10 Momentum Model | pass | FAIL (Rs 95,523) | 4.2 | 2 | 1 | 1 | 0 (32.0% incl. fee) | 1 | 0 (-8.2 pts) | 1 | 7 |
| - | WKIMO_0019 | Mi EverGreen Momentum Model | pass | FAIL (Rs 246,596) | 4.8 | 1 | 0 | 1 | 0 (31.2% incl. fee) | 1 | 0 (-0.1 pts) | 0 | 4 |
| - | WKIMO_0017 | Mi 20 Momentum Model | pass | FAIL (Rs 160,962) | 5.2 | 1 | 0 | 1 | 0 (54.8% incl. fee) | 1 | 0 (-20.3 pts) | 0 | 5 |
| - | ZEFHAA_0001-0005, ZEFHTR_0001-0004 | Zerodha Fund House (9 ETF-of-Zerodha-funds baskets) | FAIL (1.0 to 1.5 yrs) | pass | 1.0-1.5 | - | free | 0-1 | - | n/a (AMC, not an RA) | n/a | - | not scored |
| (not buyable) | WRTNM_0003 | Wright New India Manufacturing (hypothetical) | pass (4.4) | pass (Rs 48,184) | 4.4 | 1 | 1 | 2 | 1 (27.7% incl. fee) | 2 | 1 (+4.9 pts) | 2 | 11 |

Rubric: live >= 5y 2, 3 to 5y 1; transparency: 2 = fixed published rule (equal-weight top 10 of a named index), 1 = rules described only in general terms (every other basket: "proprietary", "AI/ML", "valuation filters"), holdings are login-gated for all; fee at Rs 1 lakh: <= 4% 2, <= 7.5% 1, else 0; sector fit against your list: 2 = built for it, 1 = diversified or partial, 0 = none; drawdown: worst series drawdown plus first-year fee as % of Rs 1 lakh, <= 25% 2, <= 30% 1, else 0; manager DD from `03_managers.md`: 2 = registration cross-checked with no adverse found (Wright, Green Portfolio), 1 = could not verify (Estee was not in that file; I only found the smallcase page plus an aggregator showing INH000019503 "Jan 31, 2025 to perpetual" and a PMS number INP000003146 on another aggregator; WeekendInvesting "could not verify"); net-of-fee 3y excess: 3-year net-of-fee return at Rs 1 lakh (section 5) minus Nifty 500: >= 5 points 2, 0 to 5 points 1, negative 0; minimum investment <= Rs 50k 2, <= Rs 1 lakh 1, else 0.

What each eligible basket is, in one line:

- **GPRMO_0003 High Quality Right Price (Green Portfolio), rank 1.** Valuation-filtered multi-cap, universe "government schemes like Aatmanirbhar Bharat, import substitution, PLI", and the basket's own text says it leans to pharma and chemicals. 17 stocks, 70% small-cap, PE 32, quarterly rebalance (last done today, 2026-10-09; next 2027-01-11), only 1 stock in and 1 out per quarter in the last four rebalances, so it is the low-turnover option. Best net-of-fee record of the group, but the method is a team judgement and a sector tilt you did not ask for. Green Portfolio is also a PMS manager (INP000006022 per the firm's investor charter). Note a CIN discrepancy on its own documents (a Delhi CIN on some, a Gurgaon CIN on a 2024 grievance matrix) that 03_managers.md did not flag.
- **WRTMO_0003 Balanced Multi Factor (Wright), rank 2.** Multi-factor, multi-asset (stocks, bonds, gold, international ETFs per its method text), 19 stocks, monthly rebalance with 2 to 5 names swapped each month. Volatility 18.5% a year on the series, but after a Rs 7,200 fee its 3-year return trails the Nifty 500 (net 4.0% vs 8.0% at Rs 1 lakh).
- **ESTMO_0001 Gulaq Gear 6 (Estee), rank 3.** Rule-based, BSE 500, monthly. 3-year return 6.2% against 7.0% for the index before any fee; 20% below its own August 2024 peak; worst drawdown on the series -26.8%.
- **WRTMO_0018 Alpha Prime (Wright), rank 4.** 10-stock weekly momentum book, 3.3 years, fee Rs 10,000 (10% of Rs 1 lakh), 9 of the last 33 updates skipped.
- **Blocked by minimum investment:** Green Global Giants Rs 1.11 lakh (and its next rebalance was scheduled for 2026-03-25 but the last one logged is 2025-12-08); WeekendInvesting Mi NNF10 Rs 90k and Mi India Top10 Rs 95k (both 10 large-caps, both well behind the index over 2 years), EverGreen Rs 2.47 lakh, Mi 20 Rs 1.61 lakh (worst: -39.8% drawdown, 2y -16.3%/yr).
- **Excluded for age:** the nine Zerodha Fund House baskets are free and cheap to hold but are 1.0 to 1.5 years old and are ETF baskets, not named-analyst stock selection. For plain index exposure they are a different product to compare against.

For context only (out of scope by your rule): Windmill's free sector trackers (autos, banks, energy, infra, pharma, IT, rural) are the only sector baskets with a long series that are PUBLISHED on kite; they have no named analyst and, per 02_landscape.md, most tracked the index or lagged it over the last 2 years.

## 4. Wright New India Manufacturing (`WRTNM_0003`), in depth

### 4a. What Wright's own factsheet contains

Downloaded `wrightresearch.in/portfolio/newindia/download` (4-page PDF, created 2026-09-08 per file metadata). Contents: objective, investment mechanism ("data-driven quantitative smart beta strategy ... position sizing techniques and market regime modelling using machine learning"), minimum investment Rs 63,975, monthly rebalance, a return table, a "10 Years Expected Performance" block, a performance chart, a month-by-month return table (May 2022 to Aug 2026), team bios and a disclosure/registration block.

**What it does not contain, which you asked for:** holdings, sector split, valuation (PE/PB), portfolio turnover, rebalance dates, fees. None of these is in the PDF. Wright's web page for the basket shows "No record found" for holdings and "Login to unlock all metrics"; smallcase's constituents page returns an empty list (login-gated). So **no source I could read exposes the holdings or sector split**, and "manufacturing" cannot be confirmed from the portfolio itself. The only descriptive text (smallcase and Wright pages) says 20-25 stocks across infrastructure, pharma, fintech, renewables and electric mobility, aligned to Make in India, PLI and China+1, with dynamic sector weights; one page note says exposure to the Adani group was being reduced, banking cut, and metals and IT added (undated). That is a broad "India growth" mix, not a pure capital-goods, auto or power basket.

What I could get from other places: PE 36.8, PB 3.6, dividend yield 0.39% (smallcase API; Wright's page shows PE 36.8 too), against Nifty 500 PE 22.2 and PB 3.2 in the same API response; cap mix 32% large / 30% mid / 38% small; 19 stocks. Rebalance counts from smallcase (last four): 2026-10-01 (4 added, 3 removed, 22 weights changed), 2026-09-01 (no change; the update logged on 2026-08-31 is flagged skipped), 2026-08-04 (5 added, 5 removed, 23 weights), 2026-07-01 (3 added, 5 removed, 23 weights). 56 rebalances logged since 2022-07-01; next due 2026-11-02. So roughly 3 of 19 names are replaced in a typical month, and nearly every weight is nudged each time. Turnover itself is not published; my floor estimate is about 200% a year one-way from replaced names alone.

### 4b. Reconciling the factsheet with smallcase's series

| Item | Wright factsheet (2026-09-08) | smallcase / my calculation | Reading |
|---|---|---|---|
| Start of record | Monthly table is 0.00 for Jan to Apr 2022, first return May 2022 | `publishedOnDate` 2022-05-01, series starts 2022-05-02 (a `created` date of 2022-04-01 also exists) | Consistent: live from May 2022, no pre-launch backtest in the displayed record |
| Index level, end Aug 2026 | Compounding the monthly table from 100 gives 311.8 | smallcase index 310.5 on 2026-09-03, 302.5 on 2026-08-12 | Agrees within about 0.5% |
| YTD | 11.3% | Compounding Jan to Aug gives 11.3% | Matches |
| Inception | 31.0% a year | Platform since-launch CAGR 28.3% (to 2026-10-08), my 27.7%; table-compounded to Aug 2026 gives 30.0% | Difference is the date: the index fell about 5% from early September to 8 October |
| 3 years | 26.9% a year | Table-compounded 25.9%; platform 22.8% and mine 21.1% at 2026-10-08 | Same date effect |
| 1 year / 2 years / 3M / 6M | 7.7% / -3.6% / 7.8% / 5.4% | Table-compounded to Aug 2026: 22.0% / +3.5% cumulative / 15.1% / 10.1%. smallcase at 2026-10-08: 1y +8.4% to +8.7%, 2y -1.3% a year | **Do not reconcile with the factsheet's own monthly table.** They look like a later date than the stated one. I cannot explain it. "MTD 7.9" equals the August monthly figure and "1M 4.5" equals July's, so those column labels are also off by a month |
| "10 Years Expected Performance" | Return 31.0, risk 21.3, Sharpe 145.7, max drawdown -25.3 | Return equals the inception figure; risk 21.3 equals series volatility (21%); Sharpe 145.7 is 1.457 scaled by 100 | This block restates history. It is not a forecast and should not be read as one |
| Max drawdown | -25.3 | Monthly table gives -23.6% (Dec 2024 to Feb 2025) and -22.8% (Mar 2026); smallcase's coarse series shows -20.5% | Daily drawdown is likely deeper than any of these |
| Minimum investment | Rs 63,975 | Rs 48,184 on 2026-10-09 | Moves with share prices; the factsheet figure is older |
| Registrations | Disclosure text says SEBI Investment Adviser INA100015717; footer says PMS INP000007979 (valid from 3 Apr 2023) and RA INH000017295 (valid from 3 Jul 2024) | smallcase manager page: RA INH000017295 | Three registrations quoted. The basket has been published since May 2022, before the stated RA and PMS validity dates. This may be a renewal or category change; I could not check the SEBI register |

Calendar returns from the factsheet table: 2022 (May to Dec) +9.7%, 2023 +87.5%, 2024 +50.6%, 2025 -9.5%, 2026 to August +11.3%. 17 of 52 months were negative; the worst were -15.2% (Mar 2026), -14.6% (Jan 2025), -10.1% (Feb 2025). Nearly all of the gain came in 2023 and 2024. Performance verification: smallcase flags it verified (provider type CPPL_ASSIGNED, PaRRVA registration triggered 2026-07-22, last verified index date 2026-09-30, index 304.67); the certificate itself is not public. Factsheet disclosure still says charts "might include backtested/simulated results".

### 4c. Does "UNPUBLISHED on kite" mean Zerodha clients cannot buy it?

**Established (with the evidence):**

| # | Evidence | Source and date | Weight |
|---|---|---|---|
| 1 | `brokerMeta` for kite is UNPUBLISHED with a date of 2022-05-01, the launch day, so it was never published on Kite. The page's full broker list shows PUBLISHED only on edelweiss, dhan, smc and stoxkart, and UNPUBLISHED on the other 19 of 23 listed brokers (kite among them; also Groww, Upstox, HDFC, ICICI, Angel One) | smallcase API and page, 2026-10-09 | Platform data |
| 2 | smallcase's search endpoint (`/smallcases/search?text=...`), which the Zerodha-branded site calls, returns **only two Wright baskets for "wright" in the Kite context** (`WRTMO_0003`, `WRTMO_0018`) and nothing for "new india". Sending `X-SC-Broker: edelweiss` instead returns six Wright baskets including `WRTNM_0003`. The Zerodha site's own code sends `X-SC-Broker: kite`; with no header the result is the same as Kite | Run by me, 2026-10-09 | Direct test. Shows the basket is not discoverable for Zerodha users |
| 3 | The JavaScript of `smallcase.zerodha.com` ("Invest in ideas \| smallcases on Zerodha") classifies every fee-based smallcase the user has not already subscribed to by calling a function with `"kite"`: if `distributorMeta` has no entry whose `distributor` is `kite`, the access type is NOT_SUBSCRIBABLE. The UI then shows the message "Sorry, you can't subscribe to this smallcase from here just yet. You can request an invite from <manager> to continue" with a "Request Invite" button (mailto invite@smallcase.com), and watchlist cards hide the Invest button. `WRTNM_0003` is fee-based (`flags.private = true`) and its 55 `distributorMeta` entries contain no `kite` entry | Bundle files downloaded from smallcase.zerodha.com by me, 2026-10-09 | Client code, not documentation, but it is the site Zerodha users are sent to |
| 4 | Pattern check across all 544: every fee-based basket that is PUBLISHED on kite has a `kite` distributor entry (0 exceptions). Wright publishes two other baskets on Kite, so it does use Kite selectively | My calculation | Supports the reading of 1 to 3 |

**Not established:**

- **Zerodha's own pages say nothing.** Zerodha support has two smallcase articles (how to buy and what the charges are; why Kite and smallcase holdings differ). Neither mentions published or unpublished baskets, which baskets Zerodha clients can buy, or "Request Invite". Web searches of Zerodha support, Z-Connect (I read "Presenting smallcase 2.0") and the Kite Connect docs and forum found nothing that defines UNPUBLISHED, and smallcase's developer docs (Gateway transaction errors and distribution module) list no error for an unpublished basket. I did not read the whole Kite Connect documentation. A forum thread (TradingQ&A, Apr 2024) offers "the manager made it inactive" as a guess from another user; it is not an answer from Zerodha.
- **I did not test a purchase** from a Zerodha account. So "cannot be bought by Zerodha clients" is supported by three independent signs but is not confirmed by a live attempt or by Zerodha or smallcase in writing. The "Request Invite" route might let a client obtain access; I found nothing on what Wright or smallcase does with such a request.
- **Why** Wright left it off Kite, and what UNPUBLISHED means for someone already subscribed, are unknown.
- Wright's help centre lists Zerodha among 16 supported brokers and offers a "manual execution plan" for unsupported brokers (article gives no detail or price). That is a general statement about Wright's portfolios, and it conflicts with this basket's per-broker status. A manual plan would mean placing roughly 3 to 5 trades a month yourself on Kite for stocks worth about Rs 5,000 each, with Rs 15.34 DP charges each sell; I have not checked whether Wright offers that for this basket.
- Consistency with `02_landscape.md`: it said the basket is published on Edelweiss, Dhan, SMC and Stoxkart (true per the page's broker list; note the API's separate `distributorMeta` list shows those four as UNPUBLISHED, so the two fields disagree for them but both exclude kite) and that it did not know what UNPUBLISHED implies. It is still not documented, but see rows 2 and 3.

**Practical check before you rely on any of this:** open `smallcase.zerodha.com/smallcase/wright-new-india-WRTNM_0003` signed in, and email smallcase support with the scid and your Kite client ID. If you see "Invest" and a price, my reading is wrong.

## 5. Investor-level economics for the top candidates

Charges used (all read from the sources named):

- Subscription fee, 1-year plan, from the API: Wright Rs 7,200, Green Portfolio HQRP Rs 8,100. 6-month plans are Rs 4,500 and Rs 5,450 (9.0% and 10.9% a year equivalent), so the yearly plan is the cheaper one.
- smallcase platform fee (smallcase fees page, 15 Jan 2026): Rs 100 + GST per lump-sum Buy or Invest More order (capped at 1.5% of the order), Rs 10 + GST per SIP run, nothing on rebalances or exit; the page says the fee depends on the connected broker. A blog titled "transaction charges for smallcases on Zerodha have been revised" exists but its text had no Zerodha figures, so I could not confirm the Zerodha amount. Staging over 5 orders costs Rs 59 to Rs 590.
- Zerodha equity delivery (zerodha.com/charges): zero brokerage, STT 0.1% on buy and on sell, NSE transaction charge 0.00307%, SEBI Rs 10 a crore, stamp duty 0.015% on buy, **DP charge Rs 15.34 per scrip sold per day**. For a Rs 1 lakh basket of about 19 stocks each position is about Rs 5,000, so each full exit costs 0.3% of that stock in DP charges alone.
- Tax (listed equity, FY 2026-27): short-term gains (held under 12 months) 20%, long-term 12.5% above Rs 1.25 lakh of gains a year, plus 4% cess. These rates date from July 2024 and were reported unchanged by Budget 2026 (secondary sources: financial-education sites and a TaxGuru summary; I did not read the Finance Act text). Wright's own blog quotes the older 15%/10%/Rs 1 lakh rates and is out of date.

### 5a. Fee drag, break-even excess return, costs and tax

Cost floor counts only the names the manager replaced (adds and removes in the last four logged rebalances); trims and impact cost are extra, so true costs are higher. The tax line is an illustration, not a forecast: it assumes the basket earns a 15% gross return, 50% to 100% of that is realised as short-term gain in the two monthly-rotating baskets (names rotate monthly, so most sales are likely under 12 months; holdings are hidden, so this is my inference), and 0% to 0.8% in the quarterly basket.

| Item | Wright New India (hypothetical, not buyable on Kite) | Wright Balanced Multi Factor | Green Portfolio HQRP |
|---|---|---|---|
| Subscription fee, 1y plan (Rs) | 7,200 | 7,200 | 8,100 |
| Names replaced per rebalance (avg of last 4 logged) / rebalances per year | 3.25 of 19 / 12 | 2.75 of 19 / 12 | 1.00 of 17 / 4 |
| One-way turnover floor (replaced names only, equal weight assumed) | 205% a year | 174% a year | 24% a year |
| **Rs 1 lakh**: subscription fee % of money | 7.20% | 7.20% | 8.10% |
| Rs 1 lakh: platform fee, 5 staged orders (Rs 11.8 SIP run to Rs 118 lump sum each) % | 0.06% to 0.59% | 0.06% to 0.59% | 0.06% to 0.59% |
| Rs 1 lakh: statutory + DP cost floor (Rs / %) | Rs 1,053 / 1.05% | Rs 891 / 0.89% | Rs 113 / 0.11% |
| Rs 1 lakh: tax drag if gross return is 15% (STCG 20% + 4% cess) | 1.6% to 3.1% | 1.6% to 3.1% | 0.0% to 0.8% |
| Rs 1 lakh: break-even excess return a year over a Nifty 500 index holding | **9.9% to 12.0%** | **9.7% to 11.8%** | **8.3% to 9.6%** |
| **Rs 2 lakh**: subscription fee % of money | 3.60% | 3.60% | 4.05% |
| Rs 2 lakh: platform fee, 5 staged orders (Rs 11.8 SIP run to Rs 118 lump sum each) % | 0.03% to 0.29% | 0.03% to 0.29% | 0.03% to 0.29% |
| Rs 2 lakh: statutory + DP cost floor (Rs / %) | Rs 1,507 / 0.75% | Rs 1,275 / 0.64% | Rs 166 / 0.08% |
| Rs 2 lakh: tax drag if gross return is 15% (STCG 20% + 4% cess) | 1.6% to 3.1% | 1.6% to 3.1% | 0.0% to 0.8% |
| Rs 2 lakh: break-even excess return a year over a Nifty 500 index holding | **5.9% to 7.8%** | **5.8% to 7.7%** | **4.2% to 5.2%** |

Reading: **at Rs 1 lakh the manager must beat a plain Nifty 500 holding by roughly 8% to 12% a year before you are ahead**; at Rs 2 lakh roughly 4% to 8%. A buy-and-hold index holding also defers tax, and while gains stay under Rs 1.25 lakh a year it pays none on long-term gains. The monthly-rotation baskets cannot use that exemption because they realise short-term gains as they trade; the quarterly HQRP can, partly. With staged entry the first year's drag is higher than shown: if the money builds up over 5 months you pay a full year's fee on about 80% of the average capital in year one.

### 5b. What the live record says net of fee

Investor-level IRR: you put in the amount, pay the listed 1-year fee up front each year, and receive the smallcase index growth on the amount. Price-only, so before dividends (about 0.4% a year for Wright New India), trading cost and tax. Format: gross CAGR / net of fee / Nifty 500 price CAGR over the same dates. Windows end 2026-10-08.

| Basket | Money | Since series start: gross / net of fee / Nifty 500 | 3y | 2y | 1y |
|---|---|---|---|---|---|
| Wright New India Manufacturing Theme (WRTNM_0003) | Rs 1 lakh | 27.7 / **21.3** / 9.0 | 21.1 / **12.7** / 7.8 | -2.5 / **-9.2** / -5.9 | 8.4 / **1.1** / -6.9 |
| Wright New India Manufacturing Theme (WRTNM_0003) | Rs 2 lakh | 27.7 / **24.4** / 9.0 | 21.1 / **16.8** / 7.8 | -2.5 / **-6.0** / -5.9 | 8.4 / **4.7** / -6.9 |
| Balanced Multi Factor Model (WRTMO_0003) | Rs 1 lakh | 23.2 / **18.2** / 13.3 | 12.6 / **4.0** / 8.0 | -0.0 / **-6.7** / -4.9 | 6.1 / **-1.0** / -4.9 |
| Balanced Multi Factor Model (WRTMO_0003) | Rs 2 lakh | 23.2 / **20.6** / 13.3 | 12.6 / **8.2** / 8.0 | -0.0 / **-3.5** / -4.9 | 6.1 / **2.4** / -4.9 |
| High Quality Right Price Theme (GPRMO_0003) | Rs 1 lakh | 40.8 / **35.8** / 20.9 | 23.5 / **14.1** / 8.1 | 12.2 / **4.2** / -4.2 | 36.3 / **26.1** / -8.1 |
| High Quality Right Price Theme (GPRMO_0003) | Rs 2 lakh | 40.8 / **38.2** / 20.9 | 23.5 / **18.7** / 8.1 | 12.2 / **8.0** / -4.2 | 36.3 / **31.0** / -8.1 |

- **Wright New India (not buyable on Kite):** since launch it clears the fee comfortably (21% net at Rs 1 lakh against 9% for the index), over 3 years it is 12.7% against 7.8%, but over the last 2 years it is below zero and behind the index once the fee is paid at Rs 1 lakh (-9.2% against -5.9%). After a further 1% of trading cost and roughly 2% to 3% of short-term tax at Rs 1 lakh, the 3-year edge over the index is close to nothing.
- **Wright Balanced Multi Factor:** after the Rs 7,200 fee at Rs 1 lakh it has trailed the Nifty 500 over 3 years (4.0% against 8.0%) and 2 years (-6.7% against -4.9%), and led only over the last year (-1.0% against -4.9%). The 7-year since-start figure (18.2% against 13.3%) starts in August 2019 and is carried by 2020 to 2024.
- **Green Portfolio HQRP:** the only candidate that has beaten the index after fee over every window (3y 14.1% against 8.1%, 2y 4.2% against -4.2%, 1y 26.1% against -8.1% at Rs 1 lakh). That record is concentrated in a small-cap-heavy (70%) book during a small-cap-friendly period and a pharma and chemicals tilt; After a 36% year its basket PE is 32 (Nifty 500 PE 22.2 in the Wright API response), so you would not be entering at a low valuation, though the basket was rebalanced today.

### 5c. Loss budget: your 25% limit against the worst drawdown plus a year of fee

| Basket | Fee Rs | Worst peak-to-trough on series | Rs lost at Rs 1L from that drawdown + 1st-year fee | Within Rs 25,000? | Same at Rs 2L (budget Rs 50,000) |
|---|---|---|---|---|---|
| Wright New India Manufacturing Theme | 7,200 | -23.6% (factsheet monthly table, Feb 2025) | Rs 30,800 (30.8%) | No | Rs 54,400 (27.2%) - No |
| Balanced Multi Factor Model | 7,200 | -21.0% (smallcase series) | Rs 28,200 (28.2%) | No | Rs 49,200 (24.6%) - Yes |
| High Quality Right Price Theme | 8,100 | -20.4% (smallcase series) | Rs 28,500 (28.5%) | No | Rs 48,900 (24.4%) - Yes |

At Rs 1 lakh the Rs 7,200 to Rs 8,100 fee is 29% to 32% of your Rs 25,000 budget before any market move, leaving room for only about a 17% to 18% market fall. At Rs 2 lakh the two diversified baskets just fit if the drawdown does not exceed what the coarse series shows; with weekly or daily data it would probably be deeper, and New India's monthly-table drawdown does not fit even at Rs 2 lakh. Drawdown inputs for Wright Balanced and HQRP use smallcase's series sampled every 34 to 38 days, which understate the true daily peak-to-trough.

## 6. Open items for the investor

1. Check each firm's registration number on SEBI's Recognised Intermediaries page (Wright INH000017295, INP000007979 and the IA INA100015717; Green Portfolio INH100008513 and INP000006022; Estee INH000019503; WeekendInvesting INH100008717). I could not query it.
2. Ask Wright which registration the smallcase operated under between May 2022 and July 2024, and why its factsheet's 1-year and 2-year returns do not match its own monthly table.
3. Ask Green Portfolio which CIN is current (Delhi U67190DL2014PTC268647 or Gurgaon U67190HR2014PTC124368).
4. smallcase's complaint API returns the monthly tables for Wright but they are blank and stop in August 2024, so I treated complaint data as unavailable. Ask each manager for its current monthly SCORES table.
5. If you want to test the Zerodha question directly, see the check at the end of 4c.

## Sources and files

- Data: `reports/smallcase/06_all_baskets.csv` (544 rows). Scratch data in the session scratchpad (`w6/`).
- smallcase API: `smallcases/smallcase`, `smallcases/historical`, `smallcases/rebalances`, `smallcases/search`, `smallcases/publishers`; `smallcase.com/manager/<id>` pages; `smallcase.zerodha.com` bundle files (main and 50 lazy chunks) read for the access logic.
- Wright: `wrightresearch.in/portfolio/newindia` and `/download` (factsheet), `help.wrightresearch.in` article 82000900517 (supported brokers) and 82000900186 (portfolio types).
- Zerodha: `support.zerodha.com` articles buy-smallcase and smallcase-and-kite-values-mismatch, `zerodha.com/charges`, Z-Connect "Presenting smallcase 2.0".
- smallcase: `smallcase.com/learn/smallcase-fees-and-charges/` (15 Jan 2026), `smallcase.com/blog/buying-smallcases-with-zerodha-kite/` (2016), Gateway docs `developers.gateway.smallcase.com` (transaction errors, module).
- Tax: secondary sources only (search results from Business Today, Sahi, TaxGuru, Bajaj Finserv, StockCalc).
- Green Portfolio documents at `admin.greenportfolio.co` (investor charter, disclosures), Estee at `esi.in` and `pmsbazaar.com` (aggregators, not SEBI).
