# 08 - What the free Windmill sector trackers really are

Prepared 2026-10-09. Baskets: Auto Tracker `SCTR_0001`, Energy Tracker `SCTR_0003`, Banking Tracker `SCTR_0002`, Infra Tracker `SCTR_0005`, Rising Rural Demand Theme `SCNM_0012`. Follows `02_landscape.md` (same smallcase endpoints, same date).

## 0. Bottom line

1. **They are not index trackers.** The word "Tracker" is a product label. Methodology text on smallcase says the stocks are hand-picked ("quantamental", analyst research, then liquidity/pledge/ASM-GSM screens) and weighted so "risk contribution of each stock ... is equal". Holdings are 10 to 15 stocks versus 14 to 40 in the matching NSE sector indices, and 0 to 78% of the basket weight sits in names the NSE index does not hold. Rural Demand is a theme basket and has almost nothing to do with the Nifty FMCG index.
2. **The constituent list is public after all.** smallcase publishes a "Model portfolio report" PDF for each basket (URL is in the API field `portfolioReport`, downloadable with no login). It lists every stock, cap bucket and target weight, and the latest rebalance's adds, removals and weight changes. I did not need to reconstruct anything. Section 3 has the listed holdings (dated 16 to 22 Sep 2026) and a check that they reproduce the basket's own daily series since the last rebalance (daily correlation 0.988 to 0.999).
3. **Weights are not strictly equal-risk.** Disclosed weights range from 3% to 12% and look hand-set. Against my own equal-risk-contribution calculation (trailing 1-year volatility and covariance) Auto and Energy are roughly consistent, Banking is loose, Infra and Rural are far off (section 3.3).
4. **Behaviour versus the plain sector index:** correlation of 0.87 to 0.97 on sampled returns with the matched index, beta 0.74 to 1.20 against the matched index depending on basket and window, annualised tracking error 5% to 13%, and annual return gaps of roughly -10 to +11 percentage points in 1-year windows. They resemble the sector, they do not replicate it. Rural Demand is a different animal (correlation 0.70 to 0.75 with Nifty FMCG).
5. **Cost of owning one for a year, Rs 1 lakh, using your charge schedule:** roughly Rs 700 to 1,100 (0.7% to 1.1%) including entry and a year-end exit; add Rs 118 per active rebalance if smallcase charges its Rs 100 + GST on rebalances (smallcase's own page says it does not). Capital-gains tax comes on top and depends on how much you made. See section 5.
6. **Minimum investment is mechanical:** it is about the highest (share price / target weight) in the basket, so it moves daily with one stock's price and jumps at rebalances. Infra needs about Rs 1.9 lakh today, so Rs 1 lakh cannot buy it properly.

## 1. Sources and method

| Item | Source | Notes |
|---|---|---|
| Basket detail, methodology, rationale, updates, stats | `api.smallcase.com/smallcases/smallcase?scid=<id>` pulled twice on 2026-10-09 | `constituents` is empty, as expected. `plans` key is absent (free; same conclusion as 02). |
| Basket series | `.../smallcases/historical?scid=<id>&duration={max,5y,3y,1y,1m}&benchmarkId=.NIFTY500` | Sampling is coarser for longer windows: max ~41 days (70 points from 2019-01-02), 5y ~27 days, 3y ~15 days, 1y ~5 days (82 points), 1m daily. I used all four windows so the investor can see how conclusions change with sampling. |
| Holdings and latest rebalance | smallcase "Model portfolio report" PDFs, URLs from API field `portfolioReport`, e.g. `portfolio-report.smallcase.com/user/SCTR_0001/2026-09-16/42_...pdf` | Public, no login (HTTP 200). This is smallcase's own publication, not a reconstruction. Report dates: Auto/Energy/Banking 16 Sep, Infra 17 Sep, Rural 22 Sep 2026. |
| Sector index closes | **NSE archives `archives.nseindia.com/content/indices/ind_close_all_DDMMYYYY.csv`**, one file per basket sample date (279 dates, all returned HTTP 200) | Price-return index closes. **Deviation from your brief:** Yahoo (yfinance 1.7.0) returned only one row (today) for `^CNXAUTO`, `^CNXENERGY`, `^CNXINFRA`, `^CNXFMCG`, `^CNXPSUBANK`, `^CNXMETAL` and several others, so it cannot give history. `^NSEBANK`, `^CRSLDX`, `^CNX100`, `^NSEI` do work on Yahoo. I checked the NSE-archive series against Yahoo `^NSEBANK` on 278 shared dates: maximum difference 0.000%. So the archive series is the same data. |
| Index constituents and weights | `archives.nseindia.com/content/indices/ind_nifty{auto,energy,bank,infra,fmcg}list.csv`; NSE factsheets `niftyindices.com/Factsheet/ind_Nifty_{Auto,Energy,Bank,FMCG,Infra}.pdf` (dated 30 Sep 2026; top-10 weights only) | Index weights beyond the top 10 are not public in these files. |
| Stock prices | Yahoo `.NS` tickers via yfinance (close, not dividend-adjusted) | Used for the drift, turnover, minimum-investment and risk-contribution checks only. |
| Fees | smallcase `smallcase.com/learn/smallcase-fees-and-charges/` and a smallcase blog post on transaction charges, both fetched; a web search of Zerodha's pages | Your charge list (Rs 100 + GST, DP Rs 15.34, STT 0.1%, STCG 20%, LTCG 12.5% above Rs 1.25 lakh) is used as given. I did not verify the tax rates or DP figure on a primary source. |

All basket and index series are **price-only** (the NSE factsheets show total return runs about 0.9 to 1.7 points a year above price return for these indices). Rural Demand's NSE counterpart `Nifty Rural` exists in the archive only from mid-2024, so comparisons with it are short.

## 2. What smallcase says they are (every descriptive field)

Fields identical across all five (read from the API): publisher "Windmill Capital" (`smallcaseHQ`), SEBI RA INH200007645, `type` Sector-Trackers (Rural: Thematic), `investmentStrategy` "Sector Tracker" + "Quantamental" (Rural: "Thematic" + "Fundamental"), `investmentHorizon` Long Term, `assetClass` ETI (stocks and ETFs), `universeSubset` FULL, `weighting.noWeights` false, `customized` false, `segments` empty, `stateChangeHistory` empty, `parrva` registered 2026-07-30, performance verification state VERIFIED, rebalance schedule quarterly, published 2016-04-04, displayed series from 2019-01-02, first update version dated 2016-09-01.

**Methodology blocks (identical wording in all five unless noted):**

- *Universe:* "All publicly traded companies on NSE ... covering 90% market capitalization" (Infra: "approximately 90%"; Rural: "more than 90%"; **Energy: "top 750 companies by market cap"**).
- *Research:* analyst process: investor presentations, calls, sector reports, "fundamental factors, market share within the sector, and recent financial performance" to select stocks/ETFs "that best represent the industry". Nothing about an index.
- *Constituent screening:* proprietary liquidity filters; removal of stocks with significant promoter pledge; removal for ASM/GSM presence, "deep negative news or sentiment etc".
- *Weighting:* "weighted such that the risk contribution of each stock in the smallcase is equal ... instead of marketcap or value".
- *Rebalance:* quarterly; "research team reviews ... and realign the weights".
- *Asset allocation:* block exists but is hidden and empty.

| Basket | Declared benchmark | Rationale scope (from the text) | Stocks | Cap mix L/M/S % (API) | Style flags |
|---|---|---|---|---|---|
| Auto | Nifty 500 | automobiles, auto parts, batteries, tyres | 14 | 46.8 / 18.3 / 34.9 | PE 32.9, PB 4.5, "High Volatility" |
| Energy | Nifty 100 | coal, power T&D, power trading, gas distribution, power generation, oil & gas | 11 | 75.3 / 24.7 / 0 | PE 11.3, PB 1.4, div yield 2.95 |
| Banking | Nifty 100 | private and public sector banks | 10 | 59.8 / 31.3 / 8.9 | PE 7.4 (looks too low, per 02), PB 0.94 |
| Infra | Nifty 100 | construction & engineering, water, renewables, cables, ports, cement | 15 | 59.8 / 22.4 / 17.8 | PE 27.8, PB 3.4 |
| Rural Demand | Nifty 100 | firms with rural revenue: tractors, fertilisers, FMCG etc. | 15 | 50.5 / 18.0 / 31.6 | PE 27.4; "Medium Volatility" |

The declared benchmark is a broad market index, not the sector index. Nothing in any field names a Nifty sector index.

**Rationale text** is a sector essay with dated macro facts (for example Infra cites Interim Budget 2024-25 capex; Auto cites a projection "to 2026"). It was not refreshed to 2026 data. It says nothing about selection beyond the methodology above.

**Update history (API `updates`).** Each basket has 41 versions. Versions 2 to 12 (2016-09-01 to 2019-03-15) show `appliedToUsers: false`; 30 versions from 2019-06-14 to September 2026 were applied to users. Every version has an empty `label` and empty `rationale`, so **the API says nothing about what changed**. Cadence is strictly quarterly (gaps 86 to 109 days, median 91). `skipped` is `true` on some versions.

| Basket | Live updates since 2019-06 | Skipped | Skipped, last 3y (12) | Last 2y (8), skipped | Last 12m (4), skipped | Latest version (date) |
|---|---|---|---|---|---|---|
| Auto | 30 | 15 (50%) | 5 | 2 | 1 (Mar-26) | v42, 2026-09-16, not skipped |
| Energy | 30 | 13 (43%) | 5 | 5 | 2 (Mar-26, Sep-26) | v42, 2026-09-16, **skipped** |
| Banking | 30 | 11 (37%) | 6 | 4 | 2 (Mar-26, Sep-26) | v42, 2026-09-16, **skipped** |
| Infra | 30 | 3 (10%) | 1 | 1 | 0 | v42, 2026-09-17, not skipped |
| Rural | 30 | 6 (20%) | 2 | 1 | 0 | v42, 2026-09-22, not skipped |

What "skipped" means is **my inference, 5 out of 5 consistent**: the two baskets whose Sep-2026 version is skipped (Energy, Banking) have a factsheet that says "the current portfolio composition continues to hold good until next rebalance", and the three not skipped (Auto, Infra, Rural) each show adds/removals/weight changes. So skipped = reviewed, no change, no trades.

## 3. Holdings (published by smallcase, not reconstructed)

Weights are **target weights** from the Model portfolio report issued on the dates above. They sum to 100.0% for each basket (I checked). Your actual share counts differ by rounding.

### 3.1 Listings

**Auto Tracker, 16 Sep 2026 (14 stocks).** Bajaj Auto 11.80 (+3.90 vs prior), Hyundai Motor India 9.13 (+0.71), Eicher 8.00 (+1.10), CIE Automotive 7.28 (-0.37), Endurance Tech 7.26 (+1.02), Suprajit Engg 7.23 (+0.22), Exide 6.75 (+0.14), TVS Motor 6.42 (+0.11), Belrise 6.42 (+0.58), Sona BLW 6.40 (-0.27), Balkrishna Ind 6.32 (-1.02), M&M 6.29 (-0.12), UNO Minda 5.53 (+0.10), Samvardhana Motherson 5.17 (+0.30). **Removed: Hero MotoCorp (was 6.41).** Not held: Maruti, Tata Motors PV, Ashok Leyland, Bosch, Bharat Forge, Tube Investments.

**Energy Tracker, 16 Sep 2026 (11 stocks, unchanged).** Power Grid 10.53, ONGC 10.48, Coal India 10.18, Reliance 10.00, NTPC 9.53, Oil India 9.64, Tata Power 8.47, BPCL 8.22, NHPC 7.94, GAIL 7.89, JSW Energy 7.11. All 11 are in the Nifty Energy index (40 stocks).

**Banking Tracker, 16 Sep 2026 (10 stocks, unchanged).** ICICI Bank 12.00, Federal Bank 12.00, SBI 11.80, Kotak 11.00, AU Small Finance Bank 9.82, Axis 9.50, Bank of Baroda 9.24, Karur Vysya 8.85 (smallcap, not in Nifty Bank), Canara 8.79, HDFC Bank 7.00. Not held: IndusInd, IDFC First, PNB, Union Bank, Yes Bank.

**Infra Tracker, 17 Sep 2026 (15 stocks).** Power Grid 11.55 (+3.55), Apar Industries 9.50 (+1.00), UltraTech 8.92 (+1.17), L&T 7.60 (+0.86), NTPC 7.00 (-3.51), JSW Infrastructure 6.93 (+0.47), Adani Ports 6.61 (+0.78), NCC 6.54 (+0.67), Polycab 6.46 (+0.61), KEI 5.99 (+0.04), Techno Electric 5.93 (+0.78), CG Power 5.65 (+0.23), IndiGrid InvIT 5.32 (+0.06), Siemens Energy India 3.00, Siemens 3.00. **Removed: J K Cement (was 6.72).** Not held: Reliance, Bharti Airtel, Grasim, hospitals, airlines, telecom towers (all in Nifty Infrastructure).

**Rising Rural Demand, 22 Sep 2026 (15 stocks).** SBI Life 10.00 (+1.00), Pidilite 9.76 (+1.66), Varun Beverages 8.45 (+0.10), M&M 7.85 (-0.27), CreditAccess Grameen 7.38 (-0.62), Sumitomo Chemical 7.00 (+1.19), Muthoot Finance 7.00 (-0.99), Five-Star Business Finance 6.56 (+1.32), Cholamandalam 6.39 (-0.08), **Marico 6.00 (new, +6.00)**, Crompton Greaves Consumer 5.61 (-2.69), Dhanuka Agritech 5.00 (-1.58), Coromandel 5.00 (-1.06), Hindustan Unilever 5.00 (-1.00), ITC 3.00 (-3.00).

### 3.2 Does the rule match an NSE index? No.

| Basket | Matching NSE index | Index size | Basket names in index | Basket weight in index names | Largest index weights vs basket (index % / basket %) |
|---|---|---|---|---|---|
| Auto | Nifty Auto | 15 | 8 of 14 | 58.7% | M&M 22.26 / 6.29; Maruti 13.15 / 0; Bajaj 10.02 / 11.80; Eicher 8.33 / 8.00; TVS 8.15 / 6.42; Hero 5.75 / 0 (removed); Tata Motors PV 5.01 / 0 |
| Energy | Nifty Energy | 40 | 11 of 11 | 100% | Coal India 10.19 / 10.18; Reliance 9.89 / 10.00; ONGC 9.27 / 10.48; NTPC 6.10 / 9.53; GAIL 4.86 / 7.89; Power Grid 4.69 / 10.53; BHEL 3.84 / 0 |
| Banking | Nifty Bank | 14 | 9 of 10 | 91.2% | HDFC Bank 18.61 / 7.00; ICICI 14.18 / 12.00; Kotak 10.20 / 11.00; Axis 10.06 / 9.50; SBI 9.93 / 11.80; Federal 6.56 / 12.00; IndusInd 4.97 / 0 |
| Infra | Nifty Infrastructure | 30 | 6 of 15 | 47.3% | Reliance 19.86 / 0; Bharti Airtel 14.50 / 0; L&T 11.94 / 7.60; NTPC 4.16 / 7.00; Adani Ports 3.82 / 6.61; UltraTech 3.52 / 8.92; Power Grid 3.20 / 11.55 |
| Rural | Nifty FMCG (a stand-in; no NSE rural-theme file in the archive) | 15 | 4 of 15 | 22.4% | ITC 27.65 / 3.00; HUL 18.20 / 5.00; Nestle 10.25 / 0; Varun 6.45 / 8.45; Marico 4.55 / 6.00 |

NSE index weights are free-float cap weights with caps (33% for Auto and FMCG, 10% per stock for Energy, 20% for Infra), semi-annual rebalance, per the NSE factsheets dated 30 Sep 2026. So the baskets are **sector-flavoured portfolios, not rule-based index copies**. Energy and Banking are the closest (Energy is essentially a de-concentrated, roughly equal-weight subset of the Nifty Energy large names). Auto, Infra and Rural differ by selection as well as weight. Because the rule does not match an index, I made no index-based reconstruction of holdings; the published list replaces it.

### 3.3 Is "equal risk contribution" really what they do?

I tested the published weights against equal risk contribution (ERC) computed from each stock's trailing 1-year daily returns to the rebalance date (about 245 observations; full covariance). This is **my estimate with my risk model, not Windmill's**; a different lookback would shift the answer.

| Basket | Weight range | Largest/smallest risk contribution under the published weights | Mean gap to my ERC weights | Reading |
|---|---|---|---|---|
| Auto | 5.2% to 11.8% | 1.4x | 0.5 pp | Roughly consistent with ERC |
| Energy | 7.1% to 10.5% | 1.5x | 0.5 pp | Roughly consistent |
| Banking | 7.0% to 12.0% | 2.1x | 1.6 pp | Loose: HDFC Bank, a low-volatility name, carries the smallest weight (7%) and 5.7% of risk |
| Infra | 3.0% to 11.6% | 35x | 3.8 pp | Not ERC: IndiGrid InvIT (annualised volatility 8.8%) has 5.3% weight and 0.5% of risk, Apar (46% volatility) has 16% of risk |
| Rural | 3.0% to 10.0% | 6.0x | 2.5 pp | Not ERC: ITC held at 3% (1.5% of risk); weights uncorrelated with inverse volatility (-0.04) |

Round numbers (12%, 11%, 9.5%, 7%, 5%, 3%) and a floor of 3% and cap near 12% suggest an analyst overlay on top of whatever the weighting model produces. Nothing in the data says which.

### 3.4 Check that the published list is the real thing

I held the published weights from the factsheet date to 8 Oct 2026 (buy and hold, Yahoo closes) and compared with the basket's daily series from the API. If the factsheet were stale or wrong, these would diverge.

| Basket | From | Hold return | Basket return | Gap | Daily correlation |
|---|---|---|---|---|---|
| Auto | 2026-09-16 | -5.90% | -6.57% | 0.67 pp | 0.988 |
| Energy | 2026-09-16 | -5.72% | -5.75% | 0.03 pp | 0.999 |
| Banking | 2026-09-16 | -2.31% | -2.32% | 0.02 pp | 0.999 |
| Infra | 2026-09-17 | -2.78% | -3.38% | 0.60 pp | 0.996 |
| Rural | 2026-09-22 | -6.83% | -7.02% | 0.19 pp | 0.999 |

The listed weights reproduce the basket within 0.7 pp over three weeks (price data and last-day timing explain the small gaps; for example Yahoo's 8 Oct closes may be provisional). I treat the lists as correct. They are a single dated snapshot: smallcase publishes no earlier lists I could reach, so holdings history is not available.

## 4. Do they behave like the plain index?

Method: log returns between consecutive basket sample dates versus the same-date NSE index closes. Correlation, beta (basket on index), tracking error (annualised standard deviation of basket minus index return), CAGR difference over the window, and maximum drawdown measured on the sampled dates for both series. n is 69 to 82 returns per window. **All series are price-only. Maximum drawdowns are on sample dates (every 41, 27, 15 or 5 days) and understate true daily drawdowns for both basket and index.**

### 4.1 Matched sector index

| Basket vs index | Window (sampling) | Corr | Beta | Tracking error | CAGR basket / index | Diff | Max DD basket / index |
|---|---|---|---|---|---|---|---|
| Auto vs Nifty Auto | 2019-01 to 2026-10 (41d) | 0.95 | 1.04 | 9.0% | 12.0 / 13.9 | -1.9 | -53 / -44 |
| | 5y (27d) | 0.89 | 0.82 | 9.4% | 14.4 / 17.2 | -2.8 | -25 / -22 |
| | 3y (15d) | 0.92 | 0.86 | 8.7% | 14.5 / 15.7 | -1.2 | -29 / -25 |
| | 1y (5d) | 0.93 | 0.86 | 7.4% | -0.9 / -7.6 | +6.7 | -14 / -17 |
| Energy vs Nifty Energy | max | 0.89 | 0.74 | 10.5% | 11.1 / 12.6 | -1.5 | -27 / -29 |
| | 5y | 0.86 | 0.79 | 10.3% | 9.6 / 8.3 | +1.3 | -27 / -29 |
| | 3y | 0.93 | 0.98 | 7.9% | 9.2 / 10.4 | -1.2 | -29 / -29 |
| | 1y | 0.92 | 0.81 | 6.6% | -8.7 / +1.6 | -10.3 | -17 / -13 |
| Banking vs Nifty Bank | max | 0.97 | 1.08 | 6.6% | 8.1 / 9.4 | -1.3 | -51 / -44 |
| | 5y | 0.96 | 1.02 | 5.4% | 10.6 / 7.6 | +3.0 | -17 / -16 |
| | 3y | 0.96 | 0.98 | 5.0% | 11.8 / 7.5 | +4.3 | -14 / -15 |
| | 1y | 0.96 | 0.99 | 4.8% | +8.0 / -2.7 | +10.7 | -15 / -16 |
| Infra vs Nifty Infrastructure | max | 0.88 | 1.20 | 13.0% | 15.8 / 13.7 | +2.2 | -39 / -27 |
| | 5y | 0.83 | 1.01 | 10.9% | 11.9 / 10.7 | +1.2 | -26 / -14 |
| | 3y | 0.87 | 1.14 | 11.4% | 11.3 / 11.3 | 0.0 | -27 / -17 |
| | 1y | 0.87 | 1.13 | 9.6% | +1.4 / -6.5 | +7.9 | -13 / -13 |
| Rural vs Nifty FMCG | max | 0.74 | 0.87 | 11.7% | 7.2 / 4.9 | +2.2 | -28 / -31 |
| | 5y | 0.84 | 0.90 | 8.8% | 2.8 / 1.9 | +0.9 | -27 / -32 |
| | 3y | 0.70 | 0.86 | 12.3% | -1.5 / -5.2 | +3.7 | -28 / -33 |
| | 1y | 0.75 | 0.90 | 10.9% | -17.5 / -19.4 | +2.0 | -20 / -23 |

Other comparators from the same run (max window / 3y / 1y unless noted): Banking vs Nifty Private Bank corr 0.97 / 0.93 / 0.90, beta 1.06 / 0.97 / 0.90; Banking vs Nifty PSU Bank corr 0.83 / 0.81 / 0.82, beta 0.63 / 0.57 / 0.64 (so the basket behaves like private banks). Infra vs Nifty500 Multicap Infrastructure 50:30:20 (available only from 2024-03): corr 0.89 / 0.91 / 0.91, beta 1.14 to 1.24, basket ahead by 3.6 to 6.0 pp a year. Rural vs Nifty India Consumption: corr 0.90 / 0.87 / 0.87, beta 1.01 / 0.98 / 1.02, but the basket lags it by 3.5 / 9.9 / 5.6 pp a year. Rural vs Nifty Rural (from Aug 2024, 54 points on the 3y grid): corr 0.89, basket behind by 8.7 pp a year.

### 4.2 Versus the basket's own declared benchmark and Nifty 100/500

On the 3y grid the basket-versus-Nifty 500 correlations are 0.84 (Auto), 0.76 (Energy), 0.85 (Banking), 0.87 (Infra), 0.85 (Rural), with betas 1.13, 1.07, 0.96, 1.28, 0.95. Basket CAGR minus Nifty 500 (3y): Auto +6.4, Energy +1.2, Banking +3.7, Infra +3.2, Rural -9.6 pp. Over the full window (41-day sampling) the CAGR gaps to Nifty 500 are +0.2, -0.6, -3.7, +4.1 and -4.6 pp. These agree in sign and rough size with `02_landscape.md` (small differences come from sampling and end dates).

### 4.3 What this says

- **Same direction, not same path.** Sampled correlations of 0.87 to 0.97 (Auto, Energy, Banking, Infra) mean the sector call is what you buy; tracking error of 5% to 13% a year means the basket can lag or lead the index by a lot in any year. A plain index fund's tracking difference is a fraction of a percent. Annual gaps in 1-year windows run from -10.3 (Energy) to +10.7 pp (Banking).
- **Tracking is best for Banking (corr 0.96 to 0.97, error 5% to 7%)** and Energy on the 3y grid; worst for Infra (error 10% to 13%, 15 hand-picked names plus a large non-index share) and Rural.
- **Infra has higher beta (1.1 to 1.2) and deeper drawdowns than its index** (-39% vs -27% since 2019, -27% vs -17% over 3 years), consistent with its mid/small-cap tilt (cap mix 60/22/18) and with only 47% of its weight in Nifty Infrastructure names.
- **Energy has beta below 1 against Nifty Energy** (0.74 to 0.98) and under-performed it in the last year (-8.7% vs +1.6%). The basket holds none of the index's capital-goods names (BHEL, CG Power, GE Vernova T&D, ABB and others; Capital Goods is 24.9% of the index per the NSE factsheet) nor Adani Power; I did not test whether that explains the gap.
- **Rural Demand is not a sector tracker.** Against Nifty FMCG correlation is 0.70 to 0.84 and against Nifty 500 about 0.85; it is better described as a diversified consumer/financials/agri basket. It has lost money over 1y and 3y (-17.5% and -1.5% a year) and sits 28% below its peak per 02.
- Basket-versus-index gaps in either direction are mostly stock selection and weighting, not costs, because there is no fee on these baskets. With 5 to 15 stocks, a few names drive it.
- The backtest/live split is not labelled by the API (see 02). I treat the displayed series as live from 2019-01-02. Different caveat: windows ending in 2026 are dominated by one sell-off (all five baskets are down 2% to 7% in the three weeks after the last rebalance).

## 5. Rebalance frequency, turnover and the cost of owning them (Rs 1 lakh)

### 5.1 How often, how big

Rebalance reviews happen every quarter (mid-Mar, Jun, Sep, Dec). Actual trade rounds per year, from the non-skipped share of the last 8 quarterly updates: **Auto 3.0, Energy 1.5, Banking 2.0, Infra 3.5, Rural 3.5.** Over the longer record (30 live updates) Infra was active 90% of quarters, Rural 80%, Auto 50%, Energy 57%, Banking 63%.

Turnover for the latest rebalance is the only one I can measure (the API gives no content for past updates and the factsheet shows only the latest). Two ways to count it:

| Latest rebalance | Headline weight change, one-way | One-way trade after letting weights drift from the 16 Jun 2026 rebalance (my estimate) | Scrips sold / bought | Realised gain on the sold lots if bought at the June rebalance |
|---|---|---|---|---|
| Auto (16 Sep) | 8.2% | 9.2% | 5 / 9 | Rs +760 on Rs 9,685 sold (per Rs 1 lakh invested) |
| Energy (16 Sep) | 0 (skipped) | 0 | 0 | 0 |
| Banking (16 Sep) | 0 (skipped) | 0 | 0 | 0 |
| Infra (17 Sep) | 10.2% | 11.4% | 6 / 10 | Rs -506 on Rs 10,858 sold |
| Rural (22 Sep) | 11.3% | 10.3% | 9 / 6 | Rs -933 on Rs 9,713 sold |

Assumption behind the "after drift" column: the prior target weight equals the new weight minus the published delta, and the previous rebalance executed at the 16 Jun 2026 close. Smallcase may not rebalance to exact targets, so this is an estimate. Per active rebalance, **about 9% to 11% of the portfolio is sold and the same bought**. For Energy and Banking I have no active-quarter data; below I use the mean of the three (10.3%, 6.7 scrips) as an **assumption**.

### 5.2 Per-year cost, Rs 1,00,000 held for one year

Your schedule: smallcase fee Rs 100 + 18% GST on a buy; DP Rs 15.34 per scrip sold; STT 0.1% on each buy and each sell. I assumed zero brokerage (Zerodha delivery; not verified here) and ignored exchange fees, stamp duty and SEBI fees, which are not in your list, and impact cost (unmeasured; the Auto and Infra names include small caps). Position value held at Rs 1 lakh for simplicity.

| Item | Auto | Energy | Banking | Infra | Rural |
|---|---|---|---|---|---|
| Entry: smallcase fee Rs 118 + STT Rs 100 | 218 | 218 | 218 | 218 | 218 |
| Per active rebalance: STT (0.1% x buys + sells) | 18 | 21 | 21 | 23 | 21 |
| Per active rebalance: DP Rs 15.34 x scrips sold | 77 (5) | 103 (6.7, assumed) | 103 (6.7, assumed) | 92 (6) | 138 (9) |
| Active rebalances per year (last 2 years) | 3.0 | 1.5 | 2.0 | 3.5 | 3.5 |
| **Entry + rebalances, no exit, no smallcase fee on rebalances** | **504** | **403** | **465** | **620** | **774** |
| Same, if Rs 118 is charged on every active rebalance | 858 | 580 | 701 | 1,033 | 1,187 |
| Exit at 12 months: STT Rs 100 + DP Rs 15.34 x all scrips | 315 (14) | 269 (11) | 253 (10) | 330 (15) | 330 (15) |
| **Year-one total incl. exit: no fee on rebalances** | **818 (0.82%)** | **672 (0.67%)** | **718 (0.72%)** | **950 (0.95%)** | **1,104 (1.10%)** |
| **Year-one total incl. exit: Rs 118 per active rebalance** | 1,172 (1.17%) | 849 (0.85%) | 954 (0.95%) | 1,363 (1.36%) | 1,517 (1.52%) |
| Share of capital sold in rebalances per year | 28% | 15% | 21% | 40% | 36% |

Fee-policy point: smallcase's fee page and its transaction-charges blog post both say the Rs 100 + GST applies to buy, invest-more and (Rs 10 + GST) SIP orders and that "the platform does not levy any smallcase rebalance charges". Zerodha's page (as relayed by search) agrees: Rs 100 on buying a smallcase, none on rebalance or exit. Kotak and Groww pages describe the rules somewhat differently. So the first row of totals (no per-rebalance fee) is what the sources suggest and the second row is your "per buy" assumption. Check your own contract note after the first rebalance. Free-to-hold: these baskets have no subscription fee; the brokerage-free assumption is the largest unverified piece.

### 5.3 Tax on top (user-specified rates: STCG 20% under 12 months, LTCG 12.5% above Rs 1.25 lakh a year)

- **Rebalance sells realise gains at STCG rates if the lots are under 12 months old**, and every lot bought at a rebalance is. Tax per year = 20% x (amount sold in rebalances) x (average gain on what is sold). The amount sold is Rs 15,000 to 40,000 a year per Rs 1 lakh (table above). If the stocks sold had gained 0%, 10%, 20% or 40% since you bought them, tax is Rs 0 / 310 to 800 / 620 to 1,600 / 1,240 to 3,200 (Energy lowest, Infra highest). In the one real example above (Sep 2026) the sold lots were net losers (Auto +Rs 760, Infra -Rs 506, Rural -Rs 933), so the tax bill would have been about zero, because stocks are sold when weights fall, often after weakness.
- **Exit inside 12 months:** 20% of the gain on the whole position. On the basket's trailing-12-month price move (+8.0% Banking, +1.4% Infra, -0.9% Auto, -8.7% Energy, -17.5% Rural) that is Rs 1,600 for Banking, Rs 280 for Infra and zero (a loss) for the rest. Dividends are not in these series and are taxed separately at slab rate (not computed here).
- **Exit after 12 months:** lots from the original purchase qualify as long-term, and 12.5% applies only above Rs 1.25 lakh of long-term gains across all your holdings in the year, so on a Rs 1 lakh position the long-term bill is likely zero. Lots added at later rebalances are younger and still short-term.
- A loss on rebalance sells can be set off against other gains in the same year (rules not re-verified).

Net result for a Rs 1 lakh holder: charges of about 0.7% to 1.5% in year one including exit, and 0.2% to 0.5% a year thereafter if you never exit (0.4% to 1.0% if Rs 118 is charged per active rebalance), plus tax that is zero to about 3% of capital depending on gains. Because there is no subscription fee, cost is small next to tracking differences of several percentage points either way.

## 6. Minimum investment and how it drifts

| Basket | API `minInvestAmount` (now) | In 02 (earlier pull today) | Binding stock (my calc) | Hypothetical MIA with today's weights, past 52 weeks (min to max) | Rs 1 lakh feasible? |
|---|---|---|---|---|---|
| Auto | Rs 85,865 | 86,227 | Eicher (Rs 7,004 / 8.0%) | 82,325 to 104,754 | Yes, but only just; max weight error 2.1 pp |
| Energy | Rs 12,296 | 12,309 | Reliance (Rs 1,173 / 10%) | 11,677 to 15,923 | Yes; max error 0.6 pp |
| Banking | Rs 12,562 | 12,553 | Axis Bank (Rs 1,259 / 9.5%) | 12,224 to 14,768 | Yes; max error 0.6 pp |
| Infra | Rs 1,88,784 | 1,95,815 | Apar Industries (Rs 17,860 / 9.5%) | 1,16,166 to 1,99,421 | **No**: two stocks (Siemens Energy, Polycab) cannot be bought at all and weights are off by up to 8.4 pp |
| Rural | Rs 36,165 | 36,307 | Muthoot Finance (Rs 2,610 / 7%) | 36,890 to 58,453 | Yes; max error 0.9 pp |

How the number works (my inference, fitted to the API values): **MIA ~ the highest value of (share price / target weight) across the holdings**, i.e. the cash needed to buy one whole share of the most expensive-per-weight stock. My calculation gives 87,550 / 11,728 / 13,251 / 188,000 / 37,290 against the API's 85,865 / 12,296 / 12,562 / 188,784 / 36,165 (within 0.4% to 5%; the gap is timing, since I used the last Yahoo close).

Drift:
- **Daily:** it follows the binding stock's price. Infra's figure was 3.6% lower in my pull than in 02's earlier pull the same day (195,815 to 188,784), consistent with a move in the binding stock's price (I did not check intraday prices).
- **At each rebalance:** weight changes reset it. At the 16 Sep Auto rebalance, raising Bajaj Auto from 7.9% to 11.8% lowered the minimum by about 33% for unchanged prices (my estimate: 146,747 to 98,246); Infra's NTPC cut and J K Cement removal lowered it about 10%; Rural's Marico addition and ITC cut raised it about 8%.
- **Why it matters:** a minimum under your cash is not enough; whole-share rounding can add several percentage points of weight error near the minimum (Infra at Rs 1 lakh), and a rebalance can push a basket you can afford today out of reach later (Auto) or into reach. Add-on investments (SIP minimum Rs 5,000 on the API, adjusted amounts shown by smallcase Rs 20,000 Auto, 36,000 Infra, 6,000 Rural) are subject to the same rounding.

## 7. What I could not establish

1. **Past holdings and turnover.** Only the latest rebalance is documented. Annual turnover (and therefore tax and DP cost) beyond that rests on the assumption that earlier active rebalances were similar in size (9% to 11% one-way).
2. **What "skipped" officially means** is inferred (section 2). The API provides no labels or rationale for any of 41 versions per basket.
3. **Windmill's actual weighting model.** The ERC test (3.3) uses my own risk estimates; Windmill's lookback and constraints are unknown.
4. **Live versus back-tested history** is not labelled (see 02); the published `publishedOnDate` is 2016-04-04 but the series starts 2019-01-02. The performance-verification CSV is not public (HTTP 403).
5. **Dividends.** All comparisons are price-only. The API's `divReturns` field (Auto 0.15, Energy 0.92, Banking 0.17, Infra 0.44, Rural 0.09) appears to be cumulative dividends in index points, but I could not confirm its definition, so I did not use it.
6. **Impact cost and brokerage assumptions**, plus Zerodha's own current smallcase policy (read via search only).
7. **Tax and charge rates** are yours; not checked against primary sources.
8. Sector-index factsheets give weights for the top 10 only, so "active share" versus the index was not calculated.

## 8. Practical reading for the investor

- Treat each as a **10 to 15 stock sector portfolio run by one research team**, free to hold, rebalanced roughly 2 to 3.5 times a year with about 10% of the portfolio traded each time.
- If you want exposure to **the sector index itself**, none of these is a substitute (tracking error 5% to 13%); for Banking and Energy the difference is smaller.
- Banking is the closest to its index (private-bank-like); Infra is the one most unlike its index (47% overlap, higher beta, deeper drawdowns) and not buyable at Rs 1 lakh; Rural is a different thing from FMCG and should be judged as a standalone thematic.
- Past gaps to the index (for example Banking +10.7 pp in the last year, Energy -10.3 pp) come from stock choices and cannot be projected.
