# 02 - Thematic / sectoral smallcase landscape (longlist, critique, shortlist)

Prepared 2026-10-09 for a retail investor wanting 1-2 smallcases that capture undervalued or high-potential sectors over 1-2+ years. Momentum baskets are out of scope (another agent covers them). Sector valuation is out of scope here; section 6 maps sectors to baskets so the valuation work can plug in.

## 1. How the data was obtained (and what it is worth)

All smallcase numbers below were pulled on 2026-10-09 from smallcase.com's own public JSON endpoints, not from memory:

- `api.smallcase.com/smallcases/discover` returns only 75 smallcases (the platform-owned and a few partner baskets). Not the full catalogue.
- `www.smallcase.com/smallcases-sitemap.xml` lists 603 smallcase URLs (43 are `MF_` mutual-fund baskets that the API refuses). `api.smallcase.com/smallcases/smallcase?scid=<id>` returned detail for the other 544 (all flagged active, none blocked). Of these 184 are typed Thematic or Sector-Tracker.
- Time series: `api.smallcase.com/smallcases/historical?scid=<id>&duration=max&benchmarkId=.NIFTY500` (basket index plus a rebased Nifty 500 price series). Series are sampled every 4 to 41 days (Windmill's older trackers about every 41 days), so my drawdown and volatility figures are coarse and understate true daily drawdowns.
- Fee plans, cap-mix, basket PE and constituent counts come from the `__NEXT_DATA__` block of each smallcase.com page. Manager SEBI numbers come from each `smallcase.com/manager/<id>` page ("per smallcase manager page"; I did not cross-check them on sebi.gov.in).
- Wright's own factsheet PDF (`wrightresearch.in/portfolio/newindia/download`, generated 2026-09-08) was read as an independent cross-check. Fee mechanics from smallcase's fee page via search (not opened directly). SEBI advertising and PaRRVA context from news search.

Limits that matter:

1. **Live versus backtested is not labelled by the API.** The displayed index starts on the `uploaded` date; `created` is earlier (a backtest/construction start that is not shown) and `publishedOnDate` is the public launch. For every basket in the tables the series starts on or after `publishedOnDate`, so I treat the series as live-since-publication. That is an inference. Every basket is flagged `VERIFIED` (provider type `CPPL_ASSIGNED`) but the certificate and CSV are not publicly downloadable, and I could not confirm this is SEBI's PaRRVA scheme. Wright's disclosure warns charts "might include backtested/simulated results", and its factsheet carries a "10 Years Expected Performance" block that is model output, not track record.
2. **Holdings are hidden.** The API returns an empty constituent list; smallcase pages and Tickertape gate holdings behind login. So top holdings and true overlap are not visible for any basket. Concentration is judged from stock count and cap mix only.
3. **Returns are price-only.** Basket index and Nifty 500 series are both price series (dividends are reported separately by smallcase), so the comparison is like-for-like but excludes dividends and all trading costs, taxes and impact cost.
4. Investor counts appear only for the 9 baskets that are in the public `discover` list; the rest are "not shown".
5. Benchmark used in tables is Nifty 500 (price) for every basket. Each basket's own smallcase-assigned benchmark differs (Nifty 100, Midcap 150, Smallcap 100), see the section 2 note.

## 2. Landscape facts

- 544 live smallcases are reachable, of which 184 are thematic or sector trackers from about 60 publishers. 
- Breadth gaps: **no live chemicals, pure capital-goods, textiles, cement or hospital basket**. The only manufacturing/engineering baskets are broad "Make in India"-style themes (Wright, Niveshaay, Quantace, CWA, GVSR Smart Engineering with 6 stocks). Electronics manufacturing exists only as Growth Investing's tracker (published 2026-01-21, under 9 months). Chemicals history exists only as closed baskets: GVSR Specialty Chemicals and Agrochemicals (both played out July 2026), Agility "YJ Chemistry" (played out July 2023), Marcellus Chemicals & Pharma (hidden June 2025).
- Windmill Capital (publisher id `smallcaseHQ`, so platform-affiliated per the API) owns 60 of the 544; 50 of them (28 of its 31 thematic/sector baskets) carry no subscription plan (shown as free). Every third-party basket in the longlist is paid.
- The `brokerMeta` field shows PUBLISHED status per broker. Windmill's sector trackers are published on 13 to 15 brokers each, including Kite, Groww and Upstox (Windmill Defence Picks only on Kite and Axis). Wright New India Manufacturing is published only on Edelweiss, Dhan, SMC and Stoxkart. Niveshaay, Quantace (mostly), Ethical Advisers and Omniscience baskets show UNPUBLISHED on all 23 listed brokers (Quantace Defence Stars: Dhan only). I do not know exactly what UNPUBLISHED implies for purchasing; verify in your broker app before relying on any non-Windmill basket.

## 3. Longlist (25 candidates)

Source for every row: smallcase API/page data fetched 2026-10-09 (series to 2026-10-08, performance verification date shown by smallcase 2026-09-30). Fee drag = 1-year subscription fee divided by an illustrative Rs 5 lakh investment (scales inversely with your amount; at Rs 1 lakh it is 5 times larger). Platform transaction fee is separate: smallcase's fee page (via search, 2026) lists Rs 100 + GST per lump-sum order, capped at 1.5%, plus broker statutory charges on every rebalance trade; sources disagree on whether it is per order or per basket, so check your broker.

### 3a. Structure, cost, size

| # | Basket (scid) | Manager, SEBI reg. per smallcase mgr page | Sector | Published / series start | Series yrs | Min invest Rs | Stocks | Rebalance (updates logged last 12m) | Fee Rs/yr (1y plan) | Fee drag at Rs5L | Cap mix L/M/S % | Basket PE | Investors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [Wright New India Manufacturing Theme](https://www.smallcase.com/smallcase/wright-new-india-WRTNM_0003) `WRTNM_0003` | Wright Research, INH000017295 (RA) | Manufacturing / capital goods | 2022-05-01 / 2022-05-02 | 4.4 | 48,377 | 19 | monthly (12) | 7,200 | 1.44% | 32/30/38 | 37 | not shown |
| 2 | [Make in India Theme](https://www.smallcase.com/smallcase/make-in-india-NIVNM_0001) `NIVNM_0001` | Niveshaay, INH000027830 (RA) | Manufacturing / capital goods | 2021-08-15 / 2021-08-16 | 5.1 | 83,807 | 20 | none (7) | 9,600 | 1.92% | 0/5/95 | 106 | not shown |
| 3 | [Made in India Theme](https://www.smallcase.com/smallcase/quantace-india-manufacturing-QURENM_0003) `QURENM_0003` | Quantace Research, INH000018258 (RA) | Manufacturing / capital goods | 2023-04-08 / 2023-04-10 | 3.5 | 76,387 | 9 | weekly (52) | 8,100 | 1.62% | 22/33/44 | 55 | not shown |
| 4 | [CWA Manufacturing - China Plus One Theme](https://www.smallcase.com/smallcase/cwa-manufacturing-%28china-plus-one%29-COWANM_0001) `COWANM_0001` | Compounding Wealth Advisors, INH000019983 (RA) | Manufacturing / capital goods | 2024-05-30 / 2024-05-31 | 2.4 | 364,843 | 20 | weekly (51) | 11,800 | 2.36% | 6/34/60 | 45 | not shown |
| 5 | [Banking Tracker](https://www.smallcase.com/smallcase/banking-tracker-SCTR_0002) `SCTR_0002` | Windmill Capital, INH200007645 (RA) | Banks / financials | 2016-04-04 / 2019-01-02 | 7.8 | 12,553 | 10 | quarterly (4) | Free (no plan) | 0 | 60/31/9 | 7 | 9,767 |
| 6 | [Financial Services Powerpack Theme](https://www.smallcase.com/smallcase/financial-services-powerpack-EHAMO_0001) `EHAMO_0001` | Ethical Advisers, INA000007818 (RIA) | Banks / financials | 2020-06-05 / 2020-06-08 | 6.3 | 99,491 | 24 | quarterly (3) | 3,999/6m only (about 7,998/yr if renewed; derived) | 1.60% | 44/28/28 | 12 | not shown |
| 7 | [Pharma Tracker](https://www.smallcase.com/smallcase/pharma-tracker-SCTR_0009) `SCTR_0009` | Windmill Capital, INH200007645 (RA) | Pharma / healthcare | 2016-04-04 / 2019-01-02 | 7.8 | 40,529 | 12 | quarterly (4) | Free (no plan) | 0 | 30/65/5 | 34 | 11,877 |
| 8 | [Pharma Stars Tracker](https://www.smallcase.com/smallcase/pharma-ace-stars-QURETR_0006) `QURETR_0006` | Quantace Research, INH000018258 (RA) | Pharma / healthcare | 2021-12-16 / 2021-12-17 | 4.8 | 16,378 | 9 | weekly (52) | 8,100 | 1.62% | 0/22/78 | 54 | not shown |
| 9 | [Health is Wealth Theme](https://www.smallcase.com/smallcase/health-is-wealth-EHANM_0018) `EHANM_0018` | Ethical Advisers, INA000007818 (RIA) | Pharma / healthcare | 2022-10-03 / 2022-10-04 | 4.0 | 182,128 | 22 | quarterly (3) | 8,501 | 1.70% | 30/36/35 | 34 | not shown |
| 10 | [Pharma Select Tracker](https://www.smallcase.com/smallcase/pharma-select-GPRNM_0012) `GPRNM_0012` | Green Portfolio, INH100008513 (RA) | Pharma / healthcare | 2024-08-29 / 2024-08-30 | 2.1 | 25,436 | 11 | quarterly (5) | 7,080 | 1.42% | 8/0/92 | 34 | not shown |
| 11 | [Bringing the Bling Theme](https://www.smallcase.com/smallcase/bringing-the-bling-SCNM_0015) `SCNM_0015` | Windmill Capital, INH200007645 (RA) | Consumer (incl. jewellery) | 2016-04-04 / 2019-01-02 | 7.8 | 47,181 | 9 | quarterly (4) | Free (no plan) | 0 | 35/42/24 | 57 | 2,401 |
| 12 | [Niveshaay Consumer Trends Portfolio Theme](https://www.smallcase.com/smallcase/amrit-kaal-of-consumption-NIVNM_0002) `NIVNM_0002` | Niveshaay, INH000027830 (RA) | Consumer (incl. jewellery) | 2023-11-10 / 2023-11-13 | 2.9 | 101,371 | 20 | none (13) | 9,600 | 1.92% | 4/5/91 | 91 | not shown |
| 13 | [Bharat Consumption Theme](https://www.smallcase.com/smallcase/quantace-bharat-consumption-QURENM_0008) `QURENM_0008` | Quantace Research, INH000018258 (RA) | Consumer (incl. jewellery) | 2024-04-27 / 2024-04-29 | 2.4 | 73,325 | 9 | weekly (52) | 8,100 | 1.62% | 56/33/11 | 24 | not shown |
| 14 | [Auto Tracker](https://www.smallcase.com/smallcase/auto-tracker-SCTR_0001) `SCTR_0001` | Windmill Capital, INH200007645 (RA) | Autos | 2016-04-04 / 2019-01-02 | 7.8 | 86,227 | 14 | quarterly (4) | Free (no plan) | 0 | 47/18/35 | 33 | 1,967 |
| 15 | [Auto Pack - Stepping Up the Gear Theme](https://www.smallcase.com/smallcase/auto-pack%3A-stepping-up-the-gear-EHAMO_0002) `EHAMO_0002` | Ethical Advisers, INA000007818 (RIA) | Autos | 2020-06-06 / 2020-06-08 | 6.3 | 224,362 | 23 | quarterly (3) | 8,500 | 1.70% | 39/18/43 | 19 | not shown |
| 16 | [Auto Stars Tracker](https://www.smallcase.com/smallcase/auto-ace-stars-QUREMO_0023) `QUREMO_0023` | Quantace Research, INH000018258 (RA) | Autos | 2021-12-16 / 2021-12-17 | 4.8 | 88,726 | 9 | weekly (52) | 8,100 | 1.62% | 0/11/89 | 43 | not shown |
| 17 | [Energy Tracker](https://www.smallcase.com/smallcase/energy-tracker-SCTR_0003) `SCTR_0003` | Windmill Capital, INH200007645 (RA) | Energy / power | 2016-04-04 / 2019-01-02 | 7.8 | 12,309 | 11 | quarterly (4) | Free (no plan) | 0 | 75/25/0 | 11 | 15,665 |
| 18 | [Green Energy Theme](https://www.smallcase.com/smallcase/green-energy-portfolio-NIVTR_0001) `NIVTR_0001` | Niveshaay, INH000027830 (RA) | Energy / power | 2021-03-22 / 2021-03-23 | 5.5 | 150,216 | 23 | none (12) | 12,900 | 2.58% | 7/14/79 | 49 | not shown |
| 19 | [Infra Tracker](https://www.smallcase.com/smallcase/infra-tracker-SCTR_0005) `SCTR_0005` | Windmill Capital, INH200007645 (RA) | Infra | 2016-04-04 / 2019-01-02 | 7.8 | 195,815 | 15 | quarterly (4) | Free (no plan) | 0 | 60/22/18 | 28 | 3,815 |
| 20 | [CWA Infrastructure Theme](https://www.smallcase.com/smallcase/cwa-infrastructure-COWANM_0002) `COWANM_0002` | Compounding Wealth Advisors, INH000019983 (RA) | Infra | 2024-05-30 / 2024-05-31 | 2.4 | 97,161 | 10 | weekly (51) | 11,800 | 2.36% | 11/32/57 | 31 | not shown |
| 21 | [Defence Picks Theme](https://www.smallcase.com/smallcase/defence-picks-ai-model-SCMX_0002) `SCMX_0002` | Windmill Capital, INH200007645 (RA) | Defence | 2025-11-18 / 2025-11-19 | 0.9 | 33,173 | 8 | monthly (10) | 6,550 | 1.31% | 23/0/77 | 60 | 190 |
| 22 | [Omni Bharat Defence Theme](https://www.smallcase.com/smallcase/omni-bharat-defence-OMNNM_0012) `OMNNM_0012` | Omniscience Capital, INH000020077 (RA) | Defence | 2021-01-07 / 2021-01-08 | 5.7 | 85,470 | 17 | none (2) | 12,900 | 2.58% | 38/18/44 | 20 | not shown |
| 23 | [Defence Stars Theme](https://www.smallcase.com/smallcase/quantace-defence-stars-QURENM_0001) `QURENM_0001` | Quantace Research, INH000018258 (RA) | Defence | 2023-04-08 / 2023-04-10 | 3.5 | 134,103 | 10 | weekly (52) | 8,100 | 1.62% | 0/10/90 | 71 | not shown |
| 24 | [IT Tracker](https://www.smallcase.com/smallcase/it-tracker-SCTR_0006) `SCTR_0006` | Windmill Capital, INH200007645 (RA) | IT | 2016-04-04 / 2019-01-02 | 7.8 | 106,621 | 9 | quarterly (4) | Free (no plan) | 0 | 59/41/0 | 23 | 17,498 |
| 25 | [Rising Rural Demand Theme](https://www.smallcase.com/smallcase/rising-rural-demand-SCNM_0012) `SCNM_0012` | Windmill Capital, INH200007645 (RA) | Rural demand | 2016-04-04 / 2019-01-02 | 7.8 | 36,307 | 15 | quarterly (4) | Free (no plan) | 0 | 50/18/32 | 27 | 7,687 |

Notes: "Series yrs" is length of displayed history; Windmill trackers were published in April 2016 per `publishedOnDate` but their displayed series starts 2019-01-02, so the 7.8 years is a floor on live length. "Updates logged" counts rebalance versions in the last 12 months; for weekly managers many are flagged `skipped` by smallcase (Quantace Made in India 24 of 52, CWA China+1 38 of 51, CWA Infrastructure 42 of 51), so the true trade count is lower than the log suggests. Subscription fee is the 1-year plan from the page; Rs figures are as shown on 2026-10-09 and plans can change. Basket PE and cap mix are smallcase-computed and not audited by me (Banking Tracker PE of 7 looks low for a bank basket; treat with caution). Top holdings: not visible for any basket (login-gated).

### 3b. Performance (computed by me from the smallcase series; percent per year unless stated)

| # | CAGR since series start (vs N500) | 3y CAGR (vs N500) | 2y CAGR (vs N500) | 1y (vs N500) | Max drawdown on series (vs N500) | Ann. vol (series) | Now vs own peak (peak month) | 2y excess vs N500 after fee at Rs5L | 3y excess after fee at Rs5L |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 27.7 (9.0) | 24.0 (9.5) | -1.4 (-3.9) | 4.7 (-8.8) | -20 (-16) | 21 | -6 (2024-07) | +1.0 pts | +13.1 pts |
| 2 | 32.1 (8.7) | 34.0 (8.7) | 18.0 (-2.5) | 39.8 (-7.2) | -24 (-14) | 24 | -1 (2026-09) | +18.5 pts | +23.4 pts |
| 3 | 37.9 (11.5) | 24.6 (7.8) | 24.0 (-4.3) | 57.2 (-8.4) | -36 (-18) | 23 | -4 (2026-09) | +26.7 pts | +15.2 pts |
| 4 | 10.6 (1.0) | n/a (n/a) | 6.7 (-4.1) | 40.8 (-6.5) | -33 (-16) | 20 | -0 (2026-09) | +8.4 pts | n/a |
| 5 | 8.1 (11.8) | 11.8 (8.1) | 9.2 (-3.9) | 1.3 (-9.3) | -51 (-29) | 25 | -10 (2026-02) | +13.1 pts | +3.7 pts |
| 6 | 20.7 (16.3) | 10.6 (8.1) | 1.0 (-4.0) | -5.8 (-9.8) | -24 (-17) | 22 | -10 (2026-01) | +3.4 pts | +0.9 pts |
| 7 | 16.7 (11.8) | 11.0 (8.1) | -2.9 (-3.9) | 2.6 (-9.3) | -20 (-29) | 16 | -8 (2024-09) | +1.0 pts | +3.0 pts |
| 8 | 21.4 (8.4) | 33.3 (9.5) | 18.3 (-4.6) | 25.4 (-9.2) | -20 (-15) | 18 | -4 (2026-09) | +21.3 pts | +22.2 pts |
| 9 | 18.2 (9.6) | 15.9 (7.5) | 2.4 (-2.7) | 10.3 (-6.5) | -18 (-17) | 14 | -6 (2026-09) | +3.4 pts | +6.7 pts |
| 10 | 12.6 (-4.3) | n/a (n/a) | 12.8 (-4.3) | 29.5 (-8.3) | -24 (-18) | 21 | -6 (2026-09) | +15.7 pts | n/a |
| 11 | 16.1 (11.8) | 13.8 (8.1) | 4.4 (-3.9) | 4.1 (-9.3) | -46 (-29) | 26 | -7 (2026-08) | +8.3 pts | +5.8 pts |
| 12 | 26.2 (7.9) | n/a (n/a) | 15.0 (-3.7) | 21.8 (-7.0) | -25 (-18) | 21 | -2 (2026-09) | +16.8 pts | n/a |
| 13 | 16.8 (1.2) | n/a (n/a) | 4.3 (-4.3) | 9.4 (-7.4) | -16 (-17) | 20 | -8 (2026-08) | +6.9 pts | n/a |
| 14 | 12.0 (11.8) | 14.5 (8.1) | -1.8 (-3.9) | -1.9 (-9.3) | -53 (-29) | 27 | -14 (2026-08) | +2.1 pts | +6.4 pts |
| 15 | 27.1 (16.3) | 19.5 (8.1) | 4.3 (-4.0) | -7.0 (-9.8) | -21 (-17) | 20 | -12 (2026-08) | +6.6 pts | +9.7 pts |
| 16 | 24.2 (8.4) | 25.4 (9.5) | 8.1 (-4.6) | 25.9 (-9.2) | -30 (-15) | 20 | -10 (2026-09) | +11.1 pts | +14.3 pts |
| 17 | 11.1 (11.8) | 9.2 (8.1) | -12.5 (-3.9) | -10.9 (-9.3) | -27 (-29) | 19 | -27 (2024-07) | -8.6 pts | +1.2 pts |
| 18 | 47.6 (10.5) | 30.2 (9.5) | 6.2 (-3.9) | 20.9 (-8.1) | -31 (-15) | 25 | -3 (2026-09) | +7.5 pts | +18.2 pts |
| 19 | 15.8 (11.8) | 11.3 (8.1) | -2.0 (-3.9) | 0.7 (-9.3) | -39 (-29) | 25 | -8 (2026-08) | +1.9 pts | +3.2 pts |
| 20 | 14.9 (1.0) | n/a (n/a) | 10.5 (-4.1) | 63.7 (-6.5) | -40 (-16) | 26 | 0 (2026-10) | +12.2 pts | n/a |
| 21 | 14.0 (-10.8) | n/a (n/a) | n/a (n/a) | n/a (n/a) | -13 (-13) | 31 | -12 (2026-08) | n/a | n/a |
| 22 | 44.4 (10.9) | 27.1 (7.5) | 4.2 (-2.5) | -5.8 (-9.0) | -35 (-14) | 31 | -18 (2024-07) | +4.1 pts | +17.0 pts |
| 23 | 54.3 (11.5) | 39.0 (7.8) | 18.8 (-4.3) | 22.0 (-8.4) | -36 (-18) | 36 | -3 (2026-09) | +21.5 pts | +29.6 pts |
| 24 | 17.5 (11.8) | 4.7 (8.1) | -15.4 (-3.9) | -16.0 (-9.3) | -31 (-29) | 27 | -28 (2024-10) | -11.5 pts | -3.3 pts |
| 25 | 7.2 (11.8) | -1.5 (8.1) | -12.9 (-3.9) | -19.8 (-9.3) | -28 (-29) | 17 | -28 (2024-07) | -9.1 pts | -9.5 pts |

Reading guide: "N500" is the Nifty 500 price series from the same endpoint over the same window. Excess columns are basket CAGR minus Nifty 500 CAGR minus fee drag at Rs 5 lakh; they ignore transaction cost and tax. Platform-reported CAGR for comparison: Wright New India 28.3% (4Y), Quantace Made in India 38.8% (3Y), Niveshaay Make in India 32.9% (5Y); these match my since-start figures to within rounding or date effects. Wright's own sheet (2026-09-08) shows inception 31.0%, 3Y 26.9%, 1Y 7.7%, 2Y -3.6%, versus smallcase's 3Y 24.0%, 2Y -1.4% at 2026-10-08: same shape, different dates and methods.

## 4. Critique

**Recency regime.** Most 3-year and since-start numbers are carried by the 2023 to mid-2024 rally. Over the last 2 years the free Windmill sector trackers were roughly flat to negative (Pharma -2.9%, Infra -2.0%, Auto -1.8%, Energy -12.5%, IT -15.4%, Rural -12.9%) against Nifty 500 at -3.9%; Wright New India is flat since its July 2024 peak (2Y -1.4%, 6% below peak). A 3-year CAGR of 24% to 39% should not be read as a forward rate. Several baskets sit 12% to 28% below their own peak right now (IT, Rural, Energy, Omni Bharat Defence, Auto), which is where a valuation-led entry would matter.

**Concentration.** Quantace baskets hold 9 to 10 stocks (Made in India 9, Pharma Stars 9, Auto Stars 9, Defence Stars 10); Windmill Defence Picks 8; Windmill Bling 9; IT Tracker 9. With so few names one or two stocks drive the outcome, and weights are not visible. The 17 to 24-stock baskets (Wright 19, Niveshaay 20 to 23, Ethical Advisers 22 to 24, Omni 17) are better diversified.

**Small-cap liquidity and valuation.** Niveshaay Make in India is 95% small-cap with basket PE 106; Niveshaay Consumer Trends 91% small-cap, PE 91; Quantace Auto Stars 89%, Pharma Stars 78%, Defence Stars 90% (PE 71); Windmill Defence Picks 77% (PE 60); Green Portfolio Pharma Select 92%; Niveshaay Green Energy 79%. A retail order is small, but exits in a sell-off through weekly or discretionary rebalancing in thin stocks can cost far more than the index shows, and none of the series include impact cost. By contrast Windmill Banking (60% large-cap), Energy (75% large) and Infra (60% large) are liquid but track sectors that have been lagging.

**Overlap.** Holdings are not visible, so overlap is inferred from theme: Wright, Niveshaay, Quantace and CWA manufacturing baskets are all "Make in India/PLI/China+1" and will share capital-goods, EMS and defence-adjacent names; Windmill Defence Picks, Quantace Defence Stars and Omni Bharat Defence will share the same listed defence universe; Windmill Infra overlaps with large-cap capital goods and power names in Wright and the Energy Tracker; Banking Tracker overlaps with any financial basket. Pick one basket per theme.

**Does the headline return survive costs?** For the free Windmill trackers the 3-year excess over Nifty 500 is small and in several cases the 2-year excess is roughly the index (Pharma +1.0 pts, Infra +1.9, Auto +2.1), while Energy (-8.6 pts), IT (-11.5) and Rural (-9.1) lose to the index over 2 years and since 2019 the Banking and Rural trackers lag Nifty 500 (CAGR 8.1% and 7.2% versus 11.8%). They are cheap sector exposure, not alpha. For paid baskets the after-fee excess is large on the surface (Niveshaay Make in India +18.5 pts over 2 years, Quantace baskets +21 to +27) but those figures come from a rising small-cap regime, 9-stock books and weekly or discretionary trading; the fee also rises with smaller tickets (Quantace's Rs 8,100 is 10.6% of a Rs 76,387 minimum investment). Wright New India clears its fee at 3 years (+13 pts) but only about +1 pt at 2 years. Net of tax and trading cost on weekly baskets, the real excess will be lower; I could not measure it.

**Survivorship.** Beyond the 544 live baskets I probed neighbouring scids of every live publisher prefix and found 738 more in non-live states (played out, blocked or hidden). For thematic and sector-tracker types: 184 live versus 154 found non-live, so at least 46% of the baskets I could find were no longer live (a lower bound on the failure rate because totally closed publishers are not probed, and because some blocked rows are AUM-priced duplicates such as "Wright New India [AUM Based]" rather than failures). Of 94 played-out thematic/sector baskets with dates, median lifetime was 2.0 years, 29% lasted under a year and 49% under two. Closures cluster (147 state changes dated April 2026, 100 in July 2026, across all types); the API gives no reason beyond "will no longer be actively tracked". Heavy casualties: Omniscience Capital (9 thematic live, 21 non-live), Paterson (4 live, 20 non-live), Green Portfolio (9 live, 9 non-live), Quantace (21 live, 8 non-live incl. IT Tracker, Media, Spacetech, Green Stars). Marcellus's three sector funds were hidden in June 2025. Median platform "since inception" return was 43% for closed baskets versus 78% for live ones (inception includes pre-publication history, so this is indicative of survivor bias, not a clean comparison). Survivors like Omni Bharat Defence (44% CAGR) therefore overstate what a random pick at publication would have earned.

**Manager and regulatory notes.** All managers above are listed on smallcase with a SEBI RA or RIA number (shown in the table, unverified by me on SEBI's site). Ethical Advisers' RIA registration is held in an individual's name (`Mr Dick Hosy Mody` on the manager page); Wright's footer also lists a PMS registration. SEBI's advertising code restricts past-performance claims by RAs/IAs, and an interim arrangement from 2025-10-30 allows one-to-one performance sharing only with a chartered-accountant certificate; verified-only disclosure is expected within two years (news search, not primary SEBI text). Treat manager marketing numbers with that in mind.

## 5. Recommended shortlist (8)

Ranked by suitability for "sector exposure at sensible cost with a track record you can check", not by raw return.

| Rank | Basket | Sector | Why | Main caveat |
|---|---|---|---|---|
| 1 | Wright New India Manufacturing (`WRTNM_0003`) | Manufacturing / capital goods | 4.4 years from May 2022; 19 stocks across large/mid/small (32/30/38); monthly rebalance; Rs 7,200/yr (1.44% at Rs 5L); 3y 24.0% vs 9.5%; max drawdown on series -20% versus -16% for N500; own factsheet corroborates; the only diversified manufacturing basket from a manager with PMS and RA registrations | Flat since July 2024 (2Y -1.4%); PE 37; only listed on Edelweiss/Dhan/SMC/Stoxkart, so check access; factsheet "10-year expected" block is a model |
| 2 | Windmill Pharma Tracker (`SCTR_0009`) | Pharma / healthcare | Free; 12 stocks, 65% mid-cap; lowest volatility (16%) and shallowest drawdown (-20% vs -29% N500) of the free trackers; since 2019 CAGR 16.7% vs 11.8%; listed on Kite, Groww, Upstox and others; 11,877 investors | 2Y excess only about +1 pt; PE 34; mid-cap heavy; holdings hidden |
| 3 | Windmill Banking Tracker (`SCTR_0002`) | Banks / financials | Free; 10 stocks, 60% large-cap; Rs 12,553 minimum; 2Y +9.2% vs -3.9%; 9,767 investors | Since-2019 CAGR 8.1% trails N500 (11.8%); drawdown -51% on a coarse series; one sector, high bank overlap |
| 4 | Windmill Infra Tracker (`SCTR_0005`) | Infra | Free; 15 stocks, 60% large-cap; 3Y 11.3% vs 8.1%; since 2019 15.8% vs 11.8% | Rs 1.96 lakh minimum is the highest of the free set; 2Y -2.0%; drawdown -39% |
| 5 | Windmill Auto Tracker (`SCTR_0001`) | Autos | Free; 14 stocks (47/18/35); 3Y 14.5% vs 8.1% | 2Y -1.8%, 14% below peak, drawdown -53% (coarse); only 1,967 investors |
| 6 | Windmill Energy Tracker (`SCTR_0003`) | Energy / power | Free; Rs 12,309 minimum; 75% large-cap; basket PE 11; 15,665 investors; among the lowest basket PEs in the set on smallcase's own figures (Banking shows 7 but looks unreliable) | 2Y -12.5% and 27% below its July 2024 peak; a valuation call, not a momentum one |
| 7 | Windmill IT Tracker (`SCTR_0006`) | IT | Free; 9 stocks, 59% large / 41% mid; 17,498 investors; 28% below its October 2024 peak, so the natural contrarian vehicle if sector valuation says IT is cheap | 3Y 4.7% vs 8.1% and 2Y -15.4%; Rs 1.07 lakh minimum; 9 stocks |
| 8 (conditional) | Niveshaay Make in India (`NIVNM_0001`) | Manufacturing (aggressive) | 5.1 years of history; 20 stocks; 3y 34.0% vs 8.7%, 2Y +18.0% vs -2.5%; Rs 9,600/yr; 1% from its peak | 95% small-cap, PE 106, not "undervalued"; no scheduled rebalance; UNPUBLISHED on all listed brokers; include only if the valuation work favours manufacturing and you accept small-cap risk. Otherwise take Wright instead and skip this |

Practical combination for a 1 to 2 basket plan: pair one tactical sector basket chosen by the valuation analysis (from ranks 2 to 7, all free) with Wright as the manufacturing/capex leg. Because Windmill's trackers are free and cheap to enter and exit, they suit a valuation-timed view you may change in 12 to 24 months; the paid thematic baskets carry a fixed fee whether or not you hold through weak patches.

Considered and not shortlisted: Quantace baskets (Made in India, Defence Stars, Pharma Stars, Auto Stars: strongest numbers but 9 to 10 stocks, 78 to 90% small-cap, weekly churn, Rs 8,100/yr, mostly UNPUBLISHED on brokers); CWA baskets (2.4 years, weekly with most updates skipped, Rs 11,800/yr, CWA China+1 minimum Rs 3.65 lakh); Omni Bharat Defence (5.7 years, 44% CAGR but 1Y -5.8%, 18% below peak, Rs 12,900/yr, same manager lost 21 thematic baskets); Windmill Defence Picks (under 1 year of history, PE 60, 77% small-cap, 190 investors, only on Kite and Axis; watch list); Ethical Advisers Health is Wealth and Auto Pack (good diversification and low volatility, but Rs 1.8 to 2.2 lakh minimums and all brokers UNPUBLISHED); Windmill Rising Rural Demand (3Y -1.5%/yr, 28% below peak; a pure valuation-contingent contrarian pick, free); Bringing the Bling (narrow jewellery theme, 9 stocks).

## 6. Sector to basket map for the valuation analysis

| Sector | Best live vehicle | Alternative | Gap / warning |
|---|---|---|---|
| Capital goods / manufacturing | Wright New India Manufacturing | Niveshaay Make in India; Quantace Made in India | No pure capital-goods basket; baskets are broad "Make in India" |
| Banks / financials | Windmill Banking Tracker | Ethical Financial Services Powerpack (UNPUBLISHED on brokers); Quantace Banking Stars (5 stocks, not in table) | Banking Tracker trails N500 since 2019 |
| Pharma / healthcare | Windmill Pharma Tracker | Ethical Health is Wealth; Green Pharma Select (2.1 yrs, 92% small-cap); Windmill Healthcare Tracker (published 2025-08, about 1 year) | Pharma Tracker flat for 2 years |
| Consumer | Windmill Bringing the Bling (narrow) | Quantace Bharat Consumption (2.4 yrs, 9 stocks); Niveshaay Consumer Trends (2.9 yrs, 91% small-cap) | No broad, long, diversified consumer basket; Windmill FMCG, Middle Class and Brand Value trackers lag the index |
| Autos | Windmill Auto Tracker | Ethical Auto Pack (min Rs 2.24L); Quantace Auto Stars | Coarse drawdown -53% |
| Energy / power | Windmill Energy Tracker | Niveshaay Green Energy (79% small-cap, Rs 12,900/yr); Omni Power | Energy Tracker down 27% from peak |
| Infra | Windmill Infra Tracker | CWA Infrastructure (2.4 yrs) | Min Rs 1.96 lakh |
| Defence | Omni Bharat Defence (record) / Windmill Defence Picks (new) | Quantace Defence Stars; CWA Defence; Lamron defense | Defence baskets carry PE 20 to 71 and high small-cap share; Windmill's is under 1 year old |
| IT | Windmill IT Tracker | Ethical India Tech Titans (3Y 5%) | 2Y -15% |
| Chemicals | none live | | Closed: GVSR Specialty Chemicals, Agrochemicals; Marcellus Chemicals & Pharma hidden |
| Rural demand | Windmill Rising Rural Demand | Quantace Rural Theme (published 2025-03, about 1.5 years) | Windmill rural basket 3Y -1.5% per year |
| Metals / realty (outside the brief) | Windmill Metal Tracker (3Y CAGR 24%, 1Y +19%), Realty Tracker | Quantace Metal Stars | not analysed in detail |

## 7. Biggest data gaps

1. **Top holdings and weights** for every basket (login-gated); overlap and true concentration cannot be measured.
2. **Live versus backtested split** is not exposed; I rely on `publishedOnDate` versus series start. Verification certificates and CSVs are not public.
3. **Investor counts** for 16 of the 25 longlist baskets (only the public-list baskets show them); **AUM** not shown for any.
4. **Net returns after trading costs, impact cost and tax** are not available; series are price-only and exclude dividends and fees.
5. **Broker availability** for non-Windmill baskets is unclear (UNPUBLISHED statuses); which broker the investor uses was not given.
6. **Sector valuations** are not in this file; basket PEs are smallcase-computed and unaudited.
7. **No chemicals or pure capital-goods basket** exists live; independent third-party reviews of these managers were not found, so manager quality rests on SEBI registration, track length and survivorship only.
