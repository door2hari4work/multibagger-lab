# D. The fund / ETF route to data-centre exposure (India resident, IndMoney/Drivewealth + Zerodha)
Date: 2026-10-19. Prices are 2026-10-16 closes unless stated. Research, not advice; nothing is executed. Model estimates are labelled.
Tags: FACT (source named), INFERENCE (my arithmetic or reading), SPECULATION, "unverified" (could not confirm).
No personal portfolio numbers are in this file. "Overlap" below means overlap with the investor's existing large-cap AI/semis and India infrastructure/Nasdaq-100 fund holdings, judged high / medium / low from a private brief.

## 1. Bottom line
1. FACT: there is no clean "data-centre" fund. The US-listed ones are about 55% REITs (towers plus data-centre landlords) with the rest a mix of Asian operators, AI-server makers and "neoclouds". In India I found no fund or ETF with a data-centre mandate (IndMoney catalogue lookup plus web search, 2026-10-19; not exhaustive).
2. INFERENCE: the two things the investor wants pull against each other.
   - The data-centre REITs (EQIX, DLR, AMT, CCI, SBAC) have the best valuation anchors (about 15-23x P/AFFO, 2-5% yields) and low correlation to the AI mega-caps.
   - Everything tied to AI capex (equipment, power equipment, servers, optical, memory) has about 0.7 correlation to QQQ and to the investor's AI basket, and valuation is full.
   - The ETFs that mix both (DTCR, IDGT) end up at about 0.65-0.70 correlation to the AI basket, because the non-REIT 40-45% drives the daily moves.
3. Verdicts (no fund is START-SMALL today):
   - DTCR: WATCH-WITH-TRIGGER (the best pure-theme US ETF).
   - SRVR: WATCH-WITH-TRIGGER (the lowest correlation, but the least "data-centre").
   - POWR: WATCH-WITH-TRIGGER (a power diversifier whose data-centre link is indirect).
   - IDGT: WATCH.
   - TCAI, GRID, PAVE, AIQ, SMH: AVOID as additions.
   - Indian funds: all AVOID for this purpose (data-centre content is small and diluted).
4. FACT: all of the US data-centre / power ETFs below are under their 200-day average on 2026-10-16 (DTCR -5.5% vs 200d MA, SRVR -9.8%, TCAI -8.7%). The lab's US regime filter is ON, but these are not in an uptrend themselves. Lab evidence says trend filters protect and do not find winners, so waiting for the reclaim is a drawdown-control choice and not a return edge.
5. Stock-picking vs ETF (section 7): an ETF is the lower-risk route for the "AI-equipment" half of the chain. A 3-5 stock basket is only defensible if it is mostly REITs, where single-stock risk is moderate and there is a real diversification gain.

## 2. US-listed ETF screen (FACT unless marked; yfinance + issuer pages, fetched 2026-10-19)
| ETF | Theme | Exp. ratio | Net assets | Holdings | Top-10 weight | Inception / note | 30d SEC or TTM yield |
|---|---|---|---|---|---|---|---|
| DTCR (Global X) | Data-centre REITs + digital infra | 0.50% | $1.95bn (issuer, 2026-10-16) | 25 | about 66% for top 8 (issuer); yfinance top-10 68% (older snapshot) | 2020-10-27 | 1.50% SEC (issuer, 10-16); TTM about 1.0% |
| SRVR (Pacer) | Data and infrastructure real estate | 0.49% | about $0.32bn (yfinance, unverified at issuer) | about 75 (press) | about 71% (yfinance, undated) | 2018-05 | TTM about 4.9%, includes distributions I could not decompose: unverified |
| IDGT (iShares) | US digital infra and real estate | 0.37% (some sources 0.39%) | about $0.51bn (yfinance, unverified at issuer) | about 25 | about 61% (yfinance, undated) | name/strategy dates from a 2001 fund: history before the re-index is not comparable | TTM about 0.9% |
| TCAI (Tortoise, active) | "AI infrastructure": power, cooling, networking, memory | 0.65% | $93m at 2026-03-31 (issuer fact sheet); about $240m now (yfinance) | about 40+ | 41.7% (yfinance) | 2025-08-04, only 14 months of history | about 0% |
| POWR (iShares) | US power infrastructure (utilities 49%, industrials 32%) | 0.40% | about $0.42bn (yfinance); $74m-$422m across sources, so treat as unverified | 75-77 | about 48% | renamed and re-indexed 2025-10-29; earlier history is a different strategy | TTM 6.4% looks distorted by old distributions; unverified |
| GRID (First Trust) | Smart-grid / electrification, global | 0.56% | $11.9bn | about 100 | about 58% | 2009 | about 0.9% |
| PAVE (Global X) | US infrastructure (industrials) | 0.47% | $13.4bn | about 100 | about 33% | 2017 | about 0.8% |
| AIQ (Global X) | AI and tech, broad | 0.68% | $10.3bn | about 85 | about 33% | 2018 | about 0.1% |
| SMH (VanEck) | Semiconductors | 0.35% | $74.9bn | 25 | about 67% | 2011 | about 0.2% |
Others seen but not analysed: AIPO (Defiance AI & Power Infrastructure, 0.69%, sponsor says over $500m by May 2026: sponsor claim), IVEP (Wedbush AI Power & Infrastructure, launched April 2026, too new). Hypothetical index back-tests from sponsors are not evidence.
Existence checks: all ten tickers returned a live quote from IndMoney's US-stocks lookup on 2026-10-19 (AIPO too). This confirms catalogue listing and a live price, not that a given Indian account can buy it (see section 6).

### Data quality flags
- IndMoney quote for IDGT showed an extended-hours price about 11% above the close. I treat this as a data glitch: unverified.
- IndMoney's "dividend_yield" field is inconsistent in units across tickers (POWR 6.34, SRVR 4.9, DTCR 0.94). I used dividend histories from yfinance and issuer SEC yields instead.
- yfinance holdings are undated. DTCR top holdings and assets are from the issuer page dated 2026-10-16; the others are secondary and should be re-pulled from the iShares, Pacer and Tortoise sites before any order.

## 3. Top holdings and concentration (weights in %, source as marked)
- DTCR (issuer, 2026-10-16): AMT 14.4, DLR 13.1, EQIX about 12.7, CCI 10.2, SBAC 4.9, Keppel DC REIT 4.4, GDS 3.4, NEXTDC 3.3, then APLD about 3.1 and SMCI about 2.6.
  - The five US REITs are about 55% of the fund. China 8.3%, Singapore 4.3%, Australia 3.6% (country weights at 2026-09-30).
  - INFERENCE: concentration is high (top 3 about 40%), but these are the biggest names in the niche.
- SRVR (yfinance, undated): EQIX 15.9, DLR 15.2, AMT 15.0, IRM 4.7, CCI 4.3, SBAC 4.2, Cellnex 4.2, NEXTDC 2.6, China Tower 2.4, Iridium 2.0. About 55% is the five US REITs; the rest is towers, storage and telecom real estate.
- IDGT (yfinance, undated): EQIX 8.9, AMT 8.5, FSLY 8.1, SBAC 6.5, UNIT 5.3, CCI 5.0, NTAP 4.9, SMCI 4.7, ANET 4.7, EXTR 4.5. Fastly, Uniti and Extreme are small, low-quality names.
- TCAI (yfinance): DELL 5.2, VRT 5.0, MU 4.9, SNDK 4.5, PWR 4.1, STX 4.1, CIEN 4.0, WDC 3.4, GEV 3.3, MTZ 3.0. Memory and storage (MU, SNDK, STX, WDC) is about 17% of the fund.
- POWR (yfinance): ETN 6.6, PWR 6.5, GEV 6.3, NEE 5.8, EQT 4.5, SO 4.0, NVT 3.8, DUK 3.7, CEG 3.5, HUBB 3.5.
- GRID (yfinance): ETN 8.6, PWR 8.5, JCI 8.3, ABB 7.8, Schneider 7.7, Prysmian 4.0, National Grid 3.8, E.ON 3.7, NVT 2.9, HUBB 2.5.
- PAVE: no position above 3.7% (DE, FAST, EMR, ETN, PWR lead). AIQ: PLTR 4.1, MSFT 3.6, META 3.2, TSM 3.0, NVDA 2.9 in the top 10. SMH: NVDA 19.3, TSM 9.3, MU 4.9, plus AVGO and AMD.

## 4. Overlap with what the investor already holds
Look-through (INFERENCE from the holdings above); this compares to MSFT, GOOGL, AMZN, NVDA, TSM, MU, META, APH.
| ETF | Holds any of the eight? | Overlap with existing holdings | Why |
|---|---|---|---|
| DTCR | None in top holdings | LOW by weight, MEDIUM by factor | Adds REITs the investor lacks. But the non-REIT 40-45% (APLD, SMCI, GDS, NEXTDC) trades with the AI basket |
| SRVR | None | LOW | Real-estate and tower heavy; the lowest correlation of the group |
| IDGT | None (ANET, NTAP, SMCI are adjacent) | LOW-MEDIUM | Networking and storage hardware has the same capex driver |
| TCAI | MU about 4.9%; memory/storage 17% | MEDIUM-HIGH | Adds more memory-cycle risk on top of an existing MU position; also the investor's semis exposure is already large |
| POWR | None | LOW | Utilities and electrical equipment; the least overlapping |
| GRID | None directly | LOW-MEDIUM | Electrical equipment (ETN, PWR) that is also the AI power trade |
| PAVE | None | LOW | Not really data-centre |
| AIQ | MSFT, META, TSM, NVDA in top 10 | HIGH | Duplicates mega-cap AI exposure and the Nasdaq-100 fund |
| SMH | NVDA, TSM, MU about 33% | VERY HIGH | Duplicate of the semis exposure |
| India infra funds | Mixed | MEDIUM with the infrastructure fund already held | See section 5 |
APH (Amphenol) is not in any top-10 above: unverified below the top 10.

## 5. Correlation, risk and trend (FACT: computed from yfinance adjusted closes to 2026-10-16)
The AI basket is the equal-weight daily average of MSFT, GOOGL, AMZN, NVDA, TSM, MU. 3y window starts 2023-10-16.
| ETF | Corr to QQQ (daily) | Corr to AI basket | Corr to QQQ (weekly) | Beta to QQQ | Ann. vol | 3y total return | 3y max drawdown | Worst in 2021-11..2022-12 | vs 200d MA |
|---|---|---|---|---|---|---|---|---|---|
| DTCR | 0.70 | 0.65 | 0.62 | 0.77 | 23% | +108% | -25% | -39% | below |
| SRVR | 0.48 | 0.38 | 0.42 | 0.43 | 18% | +17% | -20% | -39% | below |
| IDGT | 0.71 | 0.63 | 0.65 | 0.77 | 22% | +87% | -23% | n/a | below |
| TCAI (since 2025-08-05) | 0.76 | 0.75 | 0.66 | 1.69 | 42% | +58% | -32% | n/a | below |
| POWR (post-rename, since 2025-10-29) | 0.56 | 0.52 | n/a | 0.51 | n/a | +5% | n/a | n/a | below |
| GRID | 0.81 | 0.75 | 0.79 | 0.84 | 21% | +88% | -21% | -30% | below |
| PAVE | 0.71 | 0.62 | 0.62 | 0.71 | 21% | +77% | -26% | -23% | below |
| AIQ | 0.95 | 0.88 | 0.95 | 1.16 | 25% | +127% | -26% | n/a | above |
| SMH | 0.90 | 0.90 | 0.90 | 1.63 | 37% | +265% | -36% | n/a | above |
| QQQ (reference) | 1.00 | 0.91 | 1.00 | 1.00 | 20% | +95% | -23% | -35% | above |
Correlation of DTCR with single holdings (daily, 3y): TSM 0.60, MU 0.59, APH 0.53, NVDA 0.51, MSFT 0.29, META 0.30. TCAI: MU 0.75, TSM 0.72, APH 0.58, NVDA 0.54.
Notes:
- Survivorship caveat: DTCR's 3y return rode the neocloud/AI-server names that are now 5-10% of the fund. Do not extrapolate it.
- The 2021-11..2022-12 window is the rate shock. FACT: the data-centre REIT ETFs fell about 39%, more than QQQ (-35%). So REITs diversify AI-capex risk, not interest-rate risk. EQIX -39%, DLR -48%, AMT -36% in the same window.
- INFERENCE: planning drawdown for DTCR/SRVR about 40%, TCAI/SMH about 50-60% (lab drawdown file: SMH worst -64% since 2005; QQQ -53%).
- Last month (to 10-16): DTCR -7.5%, SRVR -5.6%, TCAI -13.8%. There was a de-rating of the AI-infrastructure complex.

## 6. Valuation of the baskets (dated 2026-10-16 prices; guidance from Q2 2026 releases)
### 6a. Data-centre / tower REIT core (these are what DTCR and SRVR mostly are)
| REIT | Price | 2026 AFFO or core-FFO/sh (guidance) | P/AFFO | AFFO yield | Div. yield now vs own 5y median trailing yield | Net debt/EBITDA | Source |
|---|---|---|---|---|---|---|---|
| EQIX | $986 | $42.69-43.29 (mid 42.99; raised in Q2; 9-12% AFFO/sh CAGR to 2029 is company outlook) | 22.9x | 4.4% | 2.05% vs 1.86% (slightly higher yield than median = a bit cheaper) | 4.9x (yfinance) | Equinix Q2 release, via search summary |
| DLR | $176 | $8.15-8.20 core FFO ex promote (mid 8.175) | 21.5x | 4.6% | 2.77% vs 3.22% (lower yield than median = richer) | 5.7x (yfinance) | DLR 8-K 2026-07-23 |
| AMT | $185 | $11.00-11.17 (Benzinga range, mid 11.085; company says midpoint raised $0.09) | 16.7x | 6.0% | 3.82% vs 3.15% (cheaper) | 4.9x net leverage (company) | AMT 8-K 2026-07-28; range from a secondary source |
| CCI | $82 | $4.53-4.65 (mid 4.59) | 17.9x | 5.6% | 5.17% vs 5.46% (about median) | 8.3x (yfinance) | CCI Q2 release 2026-07-22 |
| SBAC | $187 | $11.91-12.36 (mid 12.135) | 15.4x | 6.5% | 2.60% vs 1.63% (cheaper) | 6.4x (company, 2026-06-30) | SBAC 8-K 2026-08-03 |
- INFERENCE (arithmetic): harmonic-weighted P/AFFO of the five REITs at DTCR weights is about 19.0x (they are 55% of DTCR). At SRVR weights it is about 19.4x (55% of SRVR).
- Own-history context: I could not obtain a 5-year median P/AFFO from a free source: unverified. The dividend-yield-vs-5y-median column is a weak proxy, because payout ratios changed.
- Reverse-DCF, deliberately simple (INFERENCE): a Gordon model on AFFO with an 8.5% required return implies perpetual AFFO growth of about 4.1% for EQIX, 3.9% for DLR, 2.5% for AMT, 2.9% for CCI and 2.0% for SBAC. For EQIX and DLR that sits below the 9-12% (EQIX) growth management guides. But AFFO excludes growth capex (EQIX capex $5-6bn against about $4.2bn of AFFO), so the model flatters. A 8.5% required return is my assumption; moving it ±1 pt shifts the implied growth by 1 pt.
- Caveats on EQIX/DLR Q2: EQIX's Q2 beat included one-off xScale fees; DLR's reported Q2 core FFO $2.65 included $188m of net promote, so I used the ex-promote guide.
- Valuation read: REITs are not cheap vs their own yield history (DLR richer, EQIX and AMT a little cheaper) but are the only part of the chain priced on cash earnings at under 25x.
### 6b. Non-REIT sleeves
| Basket | Forward P/E (harmonic, top-10 weights) | EV/EBITDA | Comment |
|---|---|---|---|
| DTCR as a whole | Issuer P/E 23.0 (2025) and 20.0 (2026 estimate); P/B 8.1-9.3 | n/a | P/E is not meaningful for a REIT-heavy fund. APLD has negative forward EPS, GDS forward P/E meaningless (data-quality), SMCI about 6x |
| IDGT (top ~48% by weight) | about 19x | about 20x | Mix of REITs and hardware |
| POWR (top 10, 48%) | about 21.6x | about 17.3x | Utilities 14-18x, GEV 36x, PWR 32x |
| GRID (US names only, 31%) | about 24.9x | about 25.5x | Non-US 40% not computed |
| TCAI (top 10, 42%) | about 10.6x | about 20x | MU 4.2x, SNDK 4.9x, WDC 10x on peak memory earnings: low P/E reflects expected cyclical normalisation, not safety |
| Mega-cap AI names the investor holds (forward P/E, yfinance) | MSFT 22, GOOGL 22, AMZN 24, NVDA 13, META 20, APH 24 | | For scale |
Data from yfinance on 2026-10-19: forward P/Es from aggregator consensus, not audited. Peak-cycle earnings in memory and AI hardware make low forward P/Es unreliable.
Peer comparison: DTCR/SRVR REIT sleeve at about 19x P/AFFO vs the general US REIT index (VNQ) yield and growth: not retrieved, unverified.

## 7. ETF vs "pick 3-5 stocks"
Window for the stock baskets: 2024-03-28 to 2026-10-16 (GEV listing date limits it), equal weight, daily rebalanced approximation.
| Option | Corr to QQQ | Corr to AI basket | Beta | Vol | Return | Max DD | Worst month |
|---|---|---|---|---|---|---|---|
| DLR+EQIX+AMT (3 REITs) | 0.29 | 0.21 | 0.28 | 21% | +25% | -19% | -10% |
| VRT+PWR+GEV+ETN (equipment/power) | 0.70 | 0.72 | 1.43 | 43% | +197% | -42% | -13% |
| DLR+EQIX+VRT+PWR+GEV (mixed 5) | 0.70 | 0.70 | 1.11 | 34% | +165% | -36% | -11% |
| DTCR | 0.70 | 0.67 | 0.77 | 23% | +71% | -25% | -10% |
| POWR / GRID | 0.49 / 0.82 | 0.44 / 0.77 | 0.45 / 0.85 | 19% / 22% | +7% / +52% | -23% / -21% | |
| Single names: VRT | 0.64 | 0.68 | 1.99 | 66% | +156% | -61% | -28% |
| Single names: GEV | 0.57 | 0.58 | 1.43 | 53% | +605% | -38% | -16% |
(VRT and GEV are past winners: do not extrapolate. They sit well below their 52-week highs now, VRT -45%.)
- Cost, FACT: ETF expense ratios 0.37-0.65% a year. A stock basket has no fund fee. IndMoney/Drivewealth account charges, forex mark-up and brokerage on US trades: unverified, check the IndMoney fee page. On a small ticket in dollars the fixed per-trade costs can exceed the annual ETF fee, which favours the ETF for tranches.
- Tax, FACT/INFERENCE: stocks and ETFs are taxed the same in India (section 9), so tax does not decide this.
- Risk, INFERENCE: a REIT-only 3-stock basket looks like the best risk-adjusted way to get "data-centre" with low AI-basket correlation, and it holds the very names that dominate DTCR. The equipment basket carries 1.4x beta and a 40%+ drawdown. DTCR and a REIT basket are not the same: DTCR's non-REIT 45% adds the correlation. Stocks give control (skip APLD, SMCI) but need monitoring and cost concentration; at 3 names a 40% single-stock fall is a 13-pp hit to that sleeve.
- Practical split: for the REIT leg, 2-3 stocks (EQIX, DLR, one tower) or SRVR is defensible. For power/equipment, prefer an ETF (POWR) over picking, unless the investor wants GEV/VRT/PWR specifically (all lab-adjacent AI beta).

## 8. India: mutual funds and ETFs that actually hold data-centre names
Source: IndMoney fund data (2026-10-19), Nippon product note (2026-08-31), Sharpely (Mirae, 2026-09-30). IndMoney's holdings API returned only 20 lines per fund, covering 20-37% of the book, so its lists are partial. Weights in % of fund.
| Fund | Type / ER | AUM | Data-centre-linked names seen | Look-through read | Valuation | Verdict |
|---|---|---|---|---|---|---|
| Nippon India ETF Nifty Infrastructure BeES (INFRABEES) | Index ETF, listed on NSE/BSE (instrument found in Zerodha master; ER unverified) | unverified | Reliance 20.0, Bharti Airtel 14.7 (Nxtra data centres), L&T 12.6, Indus Towers 1.3, CG Power 1.7, Cummins 1.8, Tata Power 1.5 (2026-08-31) | Data-centre is a small part of each business: INFERENCE under 10% of the fund by revenue exposure | P/E 22.65, P/B 2.65, dividend yield 0.98% (Nifty Infrastructure, 2026-08-31, NSE via Nippon); 3y return 15.4% a year | AVOID for this purpose |
| Mirae Asset Infrastructure Fund (already held by the investor in some size; no numbers here) | Active, ER 0.82% direct | Rs 484 cr | Bharti Airtel 2.8, TD Power 2.9, Kirloskar Oil Engines 2.2 (IndMoney list), ABB India, Voltamp, CG Power, BHEL, Indus 0.5; top 10 = 36.8%, 48 stocks (30 Sep 2026) | MEDIUM-HIGH: includes the two India names the lab already downgraded (TD Power, Kirloskar Oil). It is a young fund (NAV about 11): no 3y record | Not available: unverified | Do not add; the fund already carries the India data-centre-power trade |
| Nippon India Power & Infra Fund | Active, ER 1.13% | Rs 7,867 cr | Reliance, L&T, NTPC, BHEL, Kaynes, Cyient DLM, Tata Power; Techno Electric, Hitachi Energy etc. not confirmed | LOW-MEDIUM data-centre content | 3y 16.1%, 5y 18.2% a year (IndMoney) | AVOID/WATCH; holdings sources disagree |
| ICICI Prudential Infrastructure Fund | Active, ER 1.30% | Rs 8,227 cr | Techno Electric listed at about 0% in the partial list | LOW | 1y -4.1%, 3y 15.0% | AVOID |
| Quant Infrastructure Fund | Active, ER 1.09% | Rs 3,076 cr | Indus Towers 4.9, Adani Power, BHEL; concentrated (top 20 = 68% of book in the partial list), 8.5% in debt/cash | LOW; high concentration | n/a | AVOID |
| HDFC Infrastructure Fund | Active, ER 1.35% | Rs 2,251 cr | Voltamp, Powerica; mostly banks and infra | LOW | 3y 11.5% | AVOID |
| Tata Digital India Fund | Active IT fund, ER 0.67% (already held in small size) | Rs 9,276 cr | Bharti Airtel 5.1, Tata Comm 0.9, Netweb 0.9, ABB India 0.3, Adani Enterprises 1.2 | Mostly IT services, e-commerce: data-centre content under 10% | 1y -9.0%, 3y 6.3% | AVOID for this purpose |
| Tata Nifty India Digital ETF FoF | Index FoF, ER 0.14% | Rs 108 cr | Same names, small weights | LOW | 1y -7.2%, 3y 9.4% | AVOID |
| Groww BSE Power ETF FoF | Index FoF, ER 0.26% | Rs 37 cr | Power utilities (NTPC about 21%, Power Grid about 17%, Adani Power about 11% at Dec 2025 snapshot) | Power generation, not data-centre | Index P/E about 32 (aggregators, Jul-Aug 2026) | AVOID: tiny, new, high P/E |
- INFERENCE: Indian exposure to data centres comes through three routes: telecom (Airtel/Nxtra, Tata Comm, Indus), power and electrical equipment (TD Power, Voltamp, CG Power, ABB), and gensets/cooling (Kirloskar, Cummins, Blue Star). The earlier lab work shows that the direct names are expensive and were downgraded. A diversified fund dilutes the theme to a rounding error.
- India regime filter is OFF, so no India fund is a start candidate under the lab rules regardless.
- Verification gaps: factsheets with exact September 2026 weights for Nippon Power & Infra and ICICI/HDFC Infra were not retrieved. The Mirae top-10 list differs between IndMoney's partial list (BHEL, Lodha, JSW Energy) and Sharpely (Adani Ports, L&T, NTPC), likely because of different dates; use the AMC factsheet.
- Zerodha: INFRABEES is a listed instrument in Zerodha's master (found 2026-10-19). Zerodha/Coin availability of the direct plans of the active funds above: unverified.

## 9. Availability and tax
### 9a. IndMoney availability
- FACT: DTCR, SRVR, IDGT, TCAI, POWR, GRID, PAVE, AIQ, SMH and AIPO all appear in IndMoney's US-stock catalogue with live quotes (2026-10-19).
- Not verified: whether each is tradable for the investor's Drivewealth account (fractional shares, restrictions on new or small funds, minimum order), the IndMoney fee schedule, and whether the Ireland-domiciled UCITS versions seen as "LSE~..." keys are open to Indian retail. Test with a small order or ask IndMoney support before planning around one.
- Indian-side: the funds in section 8 are all in IndMoney's MF catalogue; INFRABEES is listed on NSE/BSE.
### 9b. Indian tax (verify with a CA; I did not read the Finance Act text)
| Instrument | Short-term | Long-term | Source / status |
|---|---|---|---|
| US-listed ETFs and US stocks | slab rate if held up to 24 months | 12.5%, no indexation, no Rs 1.25 lakh exemption, after 24 months | Investor's stated rule; consistent with Angel One and Tata Capital articles; FY26-27 rules reported unchanged (Bajaj Finserv). Not confirmed against the Act |
| Indian international fund-of-funds | slab rate | 12.5% after 24 months, no exemption (units bought after April 2023) | Consistent with the above; classification under section 50AA not confirmed |
| Indian equity-oriented funds and ETFs (infra, power, tech, Nifty Infra BeES) | 20% if under 12 months | 12.5% over Rs 1.25 lakh a year, after 12 months | From general knowledge; rates not re-verified for FY26-27 |
Other items to check with a CA or HR:
- Dividends on US ETFs: US withholding on payments to India residents is commonly cited as 25% (treaty), then taxed again at slab in India with a foreign-tax credit through Form 67. Unverified.
- LRS TCS: 20% above Rs 10 lakh per financial year for investment remittances. Budget 2026 cut TCS on tours, education and medical remittances to 2% but reportedly left investments unchanged. One aggregator disagreed (an error, I think). Unverified against the Finance Act; TCS is creditable against tax.
- Foreign-asset disclosure (Schedule FA) is required for US holdings.
- US estate tax exposure: non-US persons holding US-situs assets, including US-domiciled ETFs, face US estate tax above a low threshold (commonly cited about $60,000) with no India treaty relief. Check with a CA. It matters more as US-listed holdings grow; Indian FoFs avoid it.
- Employer rules: the investor's employer stock has blackout and vesting rules, which are not relevant to these funds. Verify with HR whether outside investing in listed data-centre or tech names needs pre-clearance.

## 10. Ranked table (fund/ETF level)
| Rank | Name | Role in the chain | Valuation snapshot | Growth | Balance-sheet risk | Key bear point | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | DTCR | Landlords (about 55% US REITs) plus Asian operators and AI-server names | REIT core about 19x P/AFFO; issuer P/E about 20x (2026e); 30d SEC yield 1.5% | REIT AFFO/sh growth 3-12% (EQIX guide 9-12% to 2029; AMT calls 2026 a trough) | REIT leverage 4.9-8.3x net debt/EBITDA | Rate shock took REIT ETFs down 39% in 2022; 45% of fund is higher-beta; below 200d MA | WATCH-WITH-TRIGGER |
| 2 | SRVR | Same REITs plus towers, storage, telecom real estate | REIT core about 19.4x P/AFFO; TTM yield about 4.9% (unverified) | 2-6% | Same | Least data-centre; trailing 3y +17% and near 52-week low; rate-sensitive | WATCH-WITH-TRIGGER |
| 3 | POWR | Power generation, grid, electrical equipment | about 21.6x forward P/E | 8-15% | Utilities 5x+ leverage | Data-centre demand is a small slice of utility earnings; track record only 12 months | WATCH-WITH-TRIGGER |
| 4 | IDGT | Mixed REIT, networking, storage | about 19x forward P/E | mixed | Fastly/Uniti are weak credits | Fastly 8% and Uniti 5% are not quality names | WATCH |
| 5 | GRID | Electrification equipment | about 25x forward P/E (US names) | 10-20% | Moderate | 0.8 corr to QQQ; no valuation cushion | AVOID |
| 6 | TCAI | AI infra, power, memory, networking | about 10.6x forward P/E, memory on peak EPS | high | Moderate | Beta 1.7; MU overlap; 14 months old; active fee 0.65% | AVOID |
| 7 | PAVE, AIQ, SMH | Broad infrastructure / AI / semis | 25-29x trailing | | | Not data-centre, or pure duplicates | AVOID |
| 8 | India funds (section 8) | Diluted | P/E 22.7 for Nifty Infra | | | Data-centre exposure is incidental | AVOID |

## 11. Plans for the WATCH names (the framework needs these before any START-SMALL)
Lab evidence respected: trend filters protect but do not find winners; momentum rank is the only selector with edge; timing states carry no return edge; backtests are survivor-inflated.
- Sizing (INFERENCE). Cap one data-centre REIT ETF (DTCR or SRVR, not both) at 1.5-2% of net worth in total. A 40% stress fall on 2% of net worth is 0.8 pp of net worth. The investor's stated limit is 20-25% on money invested, so the data-centre sleeve alone should not exceed about 55% of its intended size in a 40% scenario unless the rest is in cash. POWR: cap 1-1.5%. Combined with existing AI exposure the whole theme should stay below 3-3.5% of net worth.
- Trigger to start (observable): the ETF closes above its 200-day average for 5 days and the 200d average stops falling. Currently DTCR 25.78 vs about 27.3 MA; SRVR 28.15 vs about 31.2. As a valuation alternative, start only if the REIT core is at or below about 18x P/AFFO after the Q3 prints (about the end of October to early November; dates unverified, check each IR calendar).
- Tranches: three equal purchases, spaced at least a month apart (INFERENCE: spreads timing and fee impact), skipping a tranche if the ETF is below its 200d average again.
- Accumulate rule: add only if the thesis metrics hold at the Q3 and Q4 prints (AFFO guidance not cut, leasing backlog growing) and the position remains under the cap.
- Kill / trim triggers (numeric):
  - DLR or EQIX cuts AFFO/core-FFO guidance for 2026 or 2027.
  - Fund weight in any single hyperscaler-dependent name rises above 15% (issuer holdings page).
  - 10-year Treasury yield rises 100 bp or more from the entry level (the 2022 mechanism): reduce by half.
  - ETF closes more than 25% below the average entry price: exit (the investor's limit).
  - Expense ratio or index changes; DTCR assets fall below $500m (closure risk).
- Catalysts: Q3 2026 earnings from EQIX, DLR, AMT, CCI, SBAC (late October to early November: unverified dates); hyperscaler Q3 capex guidance; FOMC; any DLR/EQIX equity raise.
- Odds (model estimates, labelled): for DTCR over 12 months, P(+30%) about 10%, P(-25%) about 15%. For SRVR, P(+30%) about 5%, P(-25%) about 12%. For POWR, P(+30%) about 8%, P(-25%) about 10%. These are judgmental, not computed.

## 12. Data-centre-specific risks (as they apply to funds)
- Power-grid constraints and interconnect delays can postpone capacity and revenue recognition at the landlords and favour the power-equipment names.
- Customer concentration: a few hyperscalers lease most new capacity. The fund diversifies across landlords but not across this customer group.
- Financing and debt: REITs run 5-8x net debt/EBITDA and need frequent capital. A rate rise cuts valuation directly (2022 evidence above).
- Lease cancellations and overbuild: DLR's record backlog and +25% renewal spreads in Q2 are the bull evidence. A hyperscaler pause would hit the neocloud and server names in these ETFs (APLD, SMCI, GDS) first.
- Obsolescence: higher rack densities and liquid cooling can strand older capacity.
- Tower REITs in the same funds are not data-centre exposure and carry DISH churn and rate risk.
- Currency: US ETFs are in USD, so a falling rupee helps and a rising one hurts. The lab's stress file includes INR scenarios.

## 13. What would make this thesis wrong
- Hyperscaler capex guidance is cut for the next year, and leasing at EQIX/DLR slows, which moves the REITs and the AI hardware names together.
- Interest rates rise again so REIT multiples compress even with stable AFFO.
- AFFO growth is mostly one-off fees (EQIX xScale, DLR promote) and the base is lower than it looks.
- Correlation rises to above 0.8 in a sell-off: then the diversification case fails, and the ETF is only a smaller AI position.
- The investor's real AI exposure is already high enough that the marginal benefit is small: INFERENCE: adding any of these is justified only by its low overlap, not by return expectations.

## 14. Sources (accessed 2026-10-19)
- Global X DTCR page (globalxetfs.com/funds/dtcr, data 2026-10-16). Yahoo Finance via yfinance 1.7.0 (prices, holdings, ratios; computed in scratchpad).
- IndMoney MCP: US-stock lookups and quotes, MF detail data (Mirae, Nippon, ICICI Pru, Quant, HDFC, Tata, Groww funds).
- Nippon India ETF Nifty Infrastructure BeES product note, August 2026 (nipponindiaim.com PDF).
- Sharpely Mirae Asset Infrastructure holdings page (30 Sep 2026); Tickertape and Trendlyne via search for BSE Power data.
- DLR 8-K ex 99.1 (sec.gov, 2026-07-23); SBAC 8-K (2026-08-03); Equinix Q2 2026 release (via search summary); American Tower Q2 2026 (via 8-K search summary and Benzinga range); Crown Castle Q2 2026 (via barchart/mfn summary).
- Tortoise TCAI 1Q2026 fact sheet (via search summary); search results on POWR, AIPO, IVEP.
- Tax: Angel One, Tata Capital, Bajaj Finserv, Vested, 1 Finance and Samco articles (secondary). Not checked against statute.
- Lab files: reports/ENGINE_FINDINGS.md, reports/OPPORTUNITIES_2026-10-05.md, analysis/stock_ideas/out/drawdowns.csv.
- Not read: issuer pages for SRVR, IDGT (iShares fetch returned the wrong fund; Pacer returned 403), TCAI current holdings, AMT and CCI full releases (403).
