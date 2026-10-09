# 07 - Sector and thematic funds/ETFs vs the free Windmill trackers (as of 2026-10-09)

Research support, not personal advice. Investor profile from the earlier files: about Rs 1 lakh staged over 4-6 months, optional Rs 5,000-15,000 a month, Zerodha (Kite and Coin), strict loss tolerance (the decision memo records a 20-25% fall as the limit). Sector view comes from `04_sectors.md`; smallcase facts from `01_mechanics.md` and `02_landscape.md`.

## 1. Bottom line

- **Private banks: ICICI Prudential Nifty Private Bank ETF (PVTBANIETF), bought through a Kite SIP.** Base expense ratio 0.13%, AUM Rs 4,287 cr, tracking difference about -0.18% a year, tracking error 0.02% (all AMC, 31 Aug 2026). The sister index funds cost 0.23-0.43% and lag the index by 0.55-0.65 points a year.
- **Autos: ICICI Prudential Nifty Auto Index Fund (Direct) on Coin**, or Nippon India Nifty Auto ETF (AUTOBEES) if you prefer the exchange. The ETF is about 0.1-0.2 points a year cheaper; the index fund is simpler to stage.
- **Power/grid: no clean fund exists.** I found no fund on Nifty Power or Nifty Capital Goods in the 18,000-line AMFI NAV file of 8 Oct 2026. The nearest are the Groww BSE Power ETF (an index of about 63% generation/distribution and 37% electrical equipment, aggregator-only figures) and the Nifty Energy products (about 37% oil, gas and coal). Treat as a small, optional slice.
- **Capital goods/manufacturing/infrastructure: skip, or accept the mismatch.** Manufacturing funds hold pharma and metals, which `04_sectors.md` says to avoid. Infrastructure ETFs cost 0.42-0.50%.
- **FMCG: ICICI Prudential Nifty FMCG ETF** (0.17%, Rs 735 cr). The sector is still falling: the fund closed 1 Oct 2026 at a new low, 32% below its Sept 2024 peak. Stage slowly.
- **Free Windmill trackers do not beat the fund route on cost, tax, transparency or staging for Rs 1 lakh.** Their one real edge is a different stock mix (tilt). Their holdings are login-gated, so I cannot tell what that tilt is. The Auto Tracker's Rs 86,227 minimum rules out staging.
- **Markets fell hard after the 31 Aug factsheets.** Between 31 Aug and 8 Oct 2026 Nifty 50 fell 7.7%, Nifty Auto 15.0%, Nifty India Manufacturing 10.5%, Nifty Bank 6.0%, Nifty Private Bank 4.1%. AMC 1-year returns dated 31 Aug are stale (Nifty Auto TRI was +16.7% then; the Nifty Auto price index is -7.6% over 1 year now).
- **A strict loss limit and sector funds are in tension.** Worst falls in the fund histories were -49% (banks), -43% (infrastructure), -38% (Nifty 50), all in Feb-Mar 2020. See section 8 for the rupee arithmetic.

## 2. Method, sources and how far to trust each number

Source tags used in every table:

| Tag | Source | Date | Trust |
|---|---|---|---|
| [F] | AMC factsheet or product note: ICICI Prudential (Aug 2026 passive factsheets), Nippon India (Sept 2026 factsheet, data as on 31 Aug; Aug product notes), Kotak (Aug 2026 web factsheet), Axis (Energy fund one-pager) | 31 Aug 2026 | Primary |
| [C] | Zerodha Coin fund page (server-rendered text) | 8 Oct 2026 | Broker display of vendor data. Cross-check below |
| [N] | AMFI NAV: today's file `portal.amfiindia.com/spages/NAVAll.txt` (latest NAV, 08-Oct-2026) plus daily NAV history from the free `api.mfapi.in` mirror of AMFI data. Returns are my calculation on Direct Growth NAV, split-adjusted | 8 Oct 2026 | Primary data, my arithmetic. Reproduces AMC 1/3/5-year figures within 0.05 points where both exist |
| [X] | NSE `ind_close_all_DDMMYYYY.csv` (index close, P/E, P/B, yield) and NSE `/api/etf` (ETF last price, volume) | 8-9 Oct 2026 | Primary. Index returns are **price** returns, so they exclude dividends |
| [Y] | Yahoo Finance daily closes and volumes via yfinance, 6 months | to 9 Oct 2026 | Aggregator. Used for traded value only |
| [E] | My estimate: fund NAV return minus the TRI return printed in AMC factsheets at 31 Aug 2026 | 31 Aug 2026 | Runs 0.05-0.09 points less negative than AMC-reported at 1 year (checked on about 10 funds) |
| [A] | Aggregator or search summary | various | **Do not rely.** Marked wherever used |

What I checked:
- **Coin vs AMC.** Coin expense ratio and AUM matched the ICICI factsheets for all 6 ICICI index funds I tested (Auto 0.25%/Rs 253 cr, Bank 0.13%/Rs 794 cr, Private Bank 0.30%/Rs 54 cr, Next 50 0.26%/Rs 10,117 cr, Midcap 150 0.22%/Rs 1,328 cr, Nifty 500 0.25%/Rs 105 cr). Kotak Nifty 50 Index Fund: Coin 0.06% against the AMC's Direct 0.07%. Nippon's index-fund factsheets show a "FY 25-26" Direct figure 0.03-0.05 points higher than Coin (for example Auto 0.35% against 0.30%); I show Coin and note the difference. Coin "launch date 2013-01-01" is a placeholder for older funds and is not used.
- **Expense ratios are now "Base Expense Ratio" (BER).** Kotak and Nippon factsheets say the figure excludes brokerage, transaction costs and statutory levies under SEBI (Mutual Funds) Regulations 2026. Tracking difference is the better cost measure because it includes everything.
- **TRI benchmark returns come from AMC tables at 31 Aug 2026.** niftyindices.com returned an error for TRI history, so I could not get TRI to 8 Oct.
- **Bid-ask spreads were not measured.** NSE's quote API returned "Access Denied" and I did not try to bypass it. Liquidity is shown as average daily traded value (Rs crore) over about 3 months.
- **Not gathered:** factsheets for Navi, Edelweiss, UTI, SBI, Tata, HDFC, Motilal, DSP, Groww, Mirae, Bandhan and Axis (except the Energy one-pager). For those funds, expense ratio, AUM and launch date come from Coin [C], and tracking difference is my estimate [E]. Tracking error is "n/r" (not retrieved).

## 3. How each route works on Zerodha, with costs and tax

| Item | Open-ended index fund (Coin, Direct) | ETF (Kite) | Windmill smallcase (Kite) |
|---|---|---|---|
| Buy mechanics | Order at end-of-day NAV, any amount from Rs 100 for most funds | Exchange order at market price, minimum 1 unit | Basket of 9-14 stocks bought into your demat, first buy at least the basket minimum |
| Staging / SIP | Coin SIPs: flexible, pausable, step-up (Zerodha support page). Coin shows no SIP floor; AMC factsheets I read say Rs 100 (Nippon, Kotak, Axis). ICICI factsheets do not state it (n/v) | Kite SIP supports ETFs, amount-based, daily/weekly/monthly, UPI Autopay for amount-based (Zerodha support pages, via search, not opened directly). Each run is an exchange order | AutoSIP at Zerodha only. Minimum SIP equals basket minimum (01_mechanics) |
| Per-order platform fee | Rs 0 | Rs 0 brokerage (Zerodha charges page) | Rs 100 + GST per lump-sum order (cap 1.5%); Rs 10 + GST per AutoSIP run |
| Stamp duty on buy | 0.005% (Coin charges page) | 0.015% (Zerodha charges page, equity delivery) | 0.015% |
| STT | 0.001% on redemption (Coin charges page) | 0.001% on sale of equity-oriented units is the standard rate in tax guides; **Zerodha's charges page does not separate ETFs** (n/v) | 0.1% on buy and on sell |
| Sell-side extras | None. No DP charge on Coin | DP Rs 15.34 per ETF sold per day | DP Rs 15.34 per stock sold, so about Rs 150-215 for a full exit of 10-14 stocks |
| Exit load | ICICI, Kotak, Nippon index funds: Nil [F]. Axis Energy Index Fund: 0.25% if redeemed within 15 days [F]. Others not shown on Coin | Not applicable on the exchange | None from smallcase |
| Internal churn and tax | Index reconstitution inside the fund; no tax to you until you redeem | Same | Every rebalance you apply sells stocks: taxable on those lots |
| Tax (all three) | Domestic-equity index funds and ETFs hold about 99-100% Indian equity, so they are equity-oriented: short-term gain (12 months or less) 20%, long-term 12.5% above Rs 1.25 lakh a year across all equity gains, no indexation. Rates as in the CBDT FAQ via `01_mechanics.md`. Tax guides for FY 2026-27 say Budget 2026 changed nothing; I could not read the Income-tax Act 2025 or Finance Act 2026 text. Each tranche has its own 12-month clock | Same | Same rates, but realised more often (quarterly rebalances) |

Per Rs 1 lakh, explicit costs, my arithmetic from the charges above (excludes spread, tracking difference, tax):

| Route | Entry | Exit | Running cost |
|---|---|---|---|
| Coin index fund | Rs 5 stamp | about Rs 1 STT | tracking difference |
| ETF | about Rs 19 (stamp Rs 15, exchange fees about Rs 4) | about Rs 20 (DP Rs 15.34, fees, STT) | tracking difference plus half-spread |
| Windmill smallcase, one lump sum | about Rs 237 (platform Rs 118, STT Rs 100, stamp Rs 15, fees about Rs 4) | about Rs 257 for 10 stocks (STT Rs 100, DP Rs 153, fees about Rs 4) | each applied rebalance repeats STT, DP and stamp on the shares traded, plus possible 20% tax. `01_mechanics.md` worked example for a 15-stock free basket held 24 months: about Rs 1,576 (1.6%), of which Rs 800 is assumed STCG; about Rs 595 with no rebalances |
| Windmill smallcase, 5 AutoSIP runs of Rs 20,000 | platform fee Rs 59 in total, plus STT, stamp | as above | as above |

## 4. The indexes: valuation and returns

NSE price indexes at 8 Oct 2026 [X]; TRI returns as printed by AMC factsheets at 31 Aug 2026 [F]. "n/a" = no TRI figure found.

| Index (fund benchmark) | P/E / P/B / yield | Price return 1y / 3y / 5y (8 Oct 2026) | TRI return 1y / 3y / 5y (31 Aug 2026) | Move 31 Aug to 8 Oct |
|---|---|---|---|---|
| Nifty 50 | 19.0 / 2.73 / 1.24 | -11.2 / 4.2 / 4.4 | -0.35 / 8.99 / 8.32 | -7.7% |
| Nifty Next 50 | 17.7 / 3.25 / 1.08 | -0.8 / 14.6 / 9.3 | 13.13 / 19.40 / 13.12 | -8.3% |
| Nifty 500 | 21.3 / 3.03 / 1.04 | -6.5 / 7.7 / 7.1 | 5.31 / n/a / n/a | -7.8% |
| Nifty Midcap 150 | 27.7 / 3.73 / 0.74 | -0.8 / 12.3 / 12.6 | 14.05 / 17.67 / 17.82 | -9.5% |
| Nifty Bank | 12.9 / 1.64 / 0.73 | -2.7 / 7.1 / 7.6 | 8.80 / 10.52 / 10.63 | -6.0% |
| Nifty Private Bank | 16.6 / 1.93 / 0.67 | -2.0 / 5.4 / 6.3 | 8.08 / 7.59 / 8.98 | -4.1% |
| Nifty Financial Services Ex-Bank | 19.5 / 3.56 / 0.81 | -3.2 / 12.0 / n/a | n/a | -10.5% |
| Nifty Auto | 28.5 / 3.83 / 1.19 | -7.6 / 15.3 / 17.2 | 16.68 / 23.64 / n/a | -15.0% |
| Nifty FMCG | 30.4 / 7.29 / 1.08 | -19.4 / -5.2 / 1.9 | -17.17 / -1.85 / 4.81 | -4.6% |
| Nifty India Consumption | 36.0 / 6.44 / 0.86 | -11.8 / 8.2 / 8.1 | -1.35 / 13.50 / 12.43 | -9.0% |
| Nifty Infrastructure | 21.3 / 2.53 / 1.02 | -6.5 / 10.9 / 10.7 | 4.29 / 16.51 / 15.43 | -7.4% |
| Nifty Energy | 14.1 / 1.96 / 1.94 | 1.6 / 10.1 / 8.3 | n/a (30 Jun: 10.1 / 18.8 / 16.7, Axis one-pager) | -6.1% |
| Nifty India Manufacturing | 26.2 / 3.76 / 0.93 | -0.2 / 15.4 / n/a | 17.30 / n/a / n/a | -10.5% |
| Nifty Power (no fund tracks it) | 18.1 / 2.20 / 1.67 | no history (listed 30 Jun 2026) | n/a | -5.6% |
| Nifty Capital Goods (no fund tracks it) | 43.4 / 8.79 / 0.61 | no history | n/a | -8.2% |

Reading it:
- Over 1 and 3 years the broad Next 50 and Midcap 150 indexes beat Nifty 50 and most sector indexes.
- Over 3 years only Nifty Auto (15.3%) beat Nifty Next 50 (14.6%).
- The difference between TRI and price in 1-year figures is the dividend yield plus the 31 Aug versus 8 Oct dates.

## 5. Fund-by-fund comparison

Columns: type (IF = open-ended index fund, Direct Growth, buy on Coin; ETF = exchange traded, buy on Kite); BER = base expense ratio; AUM in Rs crore; TD = tracking difference vs TRI, 1y / 3y (negative means the fund lags); TE = tracking error 1y (annualised daily, as printed by the AMC); returns = Direct Growth NAV return to 8 Oct 2026 [N], 1y simple, 3y and 5y annualised, "-" = not available; liquidity = average daily traded value over about 63 sessions to 9 Oct 2026 [Y], median in brackets where the two differ a lot. ETFs have a single plan, so "Direct" does not apply.

### 5.1 Autos (benchmark Nifty Auto TRI)

| Product | Type | AMC | BER % | AUM (date) | Launch | TD 1y / 3y | TE | NAV return 1y / 3y / 5y | Min lump / SIP | Exit load | Liquidity |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ICICI Prudential Nifty Auto Index Fund | IF | ICICI Pru | 0.25 [F][C] | 253.24 (31 Aug) [F] | 11 Oct 2022 [F] | -0.47 / -0.56 [F] | 0.08 [F] | -6.9 / 15.8 / - | Rs 1,000; SIP n/v | Nil [F] | - |
| Tata Nifty Auto Index Fund | IF | Tata | 0.40 [C] | 109 (8 Oct) [C] | 8 Apr 2024 [C] | -0.66 / - [E] | n/r | -7.1 / - / - | Rs 5,000 / SIP n/v | n/v | - |
| Nippon India Nifty Auto Index Fund | IF | Nippon | 0.30 [C] (0.35 in FY25-26 table [F]) | 50.51 (31 Aug) [F] | 4 Dec 2024 [F] | -0.21 [E] (AMC prints -0.94, which is the Regular plan) | 0.19 [F] | -6.7 / - / - | Rs 1,000 / Rs 100 [F] | Nil [F] | - |
| HDFC Nifty Auto Index Fund | IF | HDFC | 0.25 [C] | 163 (8 Oct) [C] | allotted 7 Jul 2026 [N] | none yet | n/r | no history | Rs 100 / SIP n/v | n/v | - |
| Nippon India Nifty Auto ETF (AUTOBEES) | ETF | Nippon | 0.22 [F] | 496.71 (31 Aug) [F] | 20 Jan 2022 [F] | -0.37 / -0.35 [F] | 0.05 [F] | -6.9 / 16.0 / - | 1 unit | n/a | Rs 6.6 cr (5.3) |
| ICICI Prudential Nifty Auto ETF (AUTOIETF) | ETF | ICICI Pru | 0.17 [F] | 227.30 (31 Aug) [F] | 12 Jan 2022 [F] | -0.28 / -0.26 [F] | 0.06 [F] | -6.8 / 16.1 / - | 1 unit | n/a | Rs 2.1 cr (1.7) |

- Index: M&M 22.8%, Maruti 13.7%, Bajaj Auto 10.4%, Eicher 8.5%, TVS 7.9% [F, ICICI 31 Aug]. Four of the top holdings (M&M, Maruti, Bajaj Auto, Eicher) are also in Nifty 50, together 55.4% of the auto fund and 6.5% of Nifty 50.
- Worst fall in NAV history (starts Jan 2022 only): -28.3% (Sept 2024 to Apr 2025); the fund is now 17.3% below its peak. The Windmill Auto Tracker series shows -53% (coarse), which suggests the shorter fund history understates the risk.
- AUTOBEES tracking difference is about 0.1 point worse than the ICICI ETF, consistent with its higher BER; ICICI's ETF trades only about Rs 2 cr a day. With Rs 20,000 orders both are fine on size, but use limit orders.

### 5.2 Banks and financial services

Nifty Bank (benchmark Nifty Bank TRI, 14 stocks: HDFC Bank 17.0%, ICICI 14.9%, SBI 10.3%, Kotak 9.9%, Axis 9.2%, about 24% PSU banks) [F].

| Product | Type | AMC | BER % | AUM (date) | Launch | TD 1y / 3y / 5y | TE | NAV return 1y / 3y / 5y | Min lump / SIP | Exit load | Liquidity |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ICICI Prudential Nifty Bank Index Fund | IF | ICICI Pru | 0.13 [F][C] | 793.57 (31 Aug) [F] | 2 Mar 2022 [F] | -0.26 / -0.29 / - [F] | 0.06 [F] | -2.3 / 7.7 / - | Rs 1,000; SIP n/v | Nil [F] | - |
| Navi Nifty Bank Index Fund | IF | Navi | 0.15 [C] | 649 (8 Oct) [C] | 17 Jan 2022 [C] | -0.29 / -0.27 [E] | n/r | -2.3 / 7.7 / - | Rs 100 / n/v | n/v | - |
| Axis Nifty Bank Index Fund | IF | Axis | 0.14 [C] | 184 [C] | 3 May 2024 [C] | -0.25 [E] | n/r | -2.3 / - / - | Rs 500 / n/v | n/v | - |
| Nippon India Nifty Bank Index Fund | IF | Nippon | 0.17 [C] (0.20 FY25-26 [F]) | 232.22 (31 Aug) [F] | 22 Feb 2024 [F] | -0.32 [E] | 0.07 [F] | -2.4 / - / - | Rs 1,000 / Rs 100 [F] | Nil [F] | - |
| Motilal Oswal Nifty Bank Index Fund | IF | Motilal | 0.23 [C] | 676 [C] | 19 Aug 2019 [C] | -0.31 / -0.30 / -0.28 [E] | n/r | -2.4 / 7.6 / 8.2 | Rs 500 / n/v | n/v | - |
| Nippon India ETF Nifty Bank BeES (BANKBEES) | ETF | Nippon | 0.19 [F] | 8,397.01 (31 Aug) [F] | 27 May 2004 [F] | -0.29 / -0.25 / -0.24 [F] | 0.04 [F] | -2.3 / 7.7 / 8.2 | 1 unit | n/a | Rs 37 cr (32) |
| ICICI Prudential Nifty Bank ETF (BANKIETF) | ETF | ICICI Pru | 0.13 [F] | 3,058.38 (31 Aug) [F] | 10 Jul 2019 [F] | -0.24 / -0.19 / -0.19 [F] | 0.03 [F] | -2.3 / 7.8 / 8.3 | 1 unit | n/a | Rs 3.5 cr (2.0) |
| Kotak Nifty Bank ETF (BANKNIFTY1) | ETF | Kotak | 0.15 [F] | 4,465.73 (31 Aug) [F] | 4 Dec 2014 [F] | -0.18 / -0.21 / -0.24 [E] | 0.04 [F] | -2.3 / 7.7 / 8.2 | 1 unit | Nil [F] | Rs 7.4 cr (1.9) |

Nifty Private Bank (benchmark Nifty Private Bank TRI, 10 stocks: ICICI 22.1%, Kotak 20.8%, Axis 19.0%, HDFC Bank 18.7%, Federal 5.9%, IndusInd 4.5% [F]; no PSU banks). The top four are 25.5% of Nifty 50, so this adds to what a broad index already holds.

| Product | Type | AMC | BER % | AUM (date) | Launch | TD 1y / 3y / 5y | TE | NAV return 1y / 3y / 5y | Min lump / SIP | Exit load | Liquidity |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ICICI Prudential Nifty Private Bank ETF (PVTBANIETF) | ETF | ICICI Pru | 0.13 [F] | 4,286.58 (31 Aug) [F] | 9 Aug 2019 [F] | -0.18 / -0.19 / -0.18 [F] | 0.02 [F] | -1.5 / 5.9 / 6.9 | 1 unit | n/a | Rs 8.4 cr (5.8) |
| HDFC Nifty Private Bank ETF (HDFCPVTBAN) | ETF | HDFC | n/r | n/r | 16 Nov 2022 (first NAV) [N] | -0.14 / -0.19 [E] | n/r | -1.6 / 5.9 / - | 1 unit | n/a | Rs 0.8 cr (0.5) |
| DSP Nifty Private Bank Index Fund | IF | DSP | 0.23 [C] | 110 (8 Oct) [C] | 14 Feb 2025 [C] | -0.57 [E] | n/r | -1.8 / - / - | Rs 100 / n/v | n/v | - |
| ICICI Prudential Nifty Private Bank Index Fund | IF | ICICI Pru | 0.30 [F][C] | 54.00 (31 Aug) [F] | 17 Jul 2025 [F] | -0.61 [F] | n/r | -1.9 / - / - | Rs 1,000; SIP n/v | Nil (assumed; not read for this fund) | - |
| UTI Nifty Private Bank Index Fund | IF | UTI | 0.43 [C] | 239 [C] | 2 Sep 2024 [C] | -0.64 [E] | n/r | -2.0 / - / - | Rs 5,000 / n/v | n/v | - |

Financial services ex-bank (NBFC-style; benchmark Nifty Financial Services Ex-Bank TRI, TRI return not retrieved).

| Product | Type | AMC | BER % | AUM (date) | Launch | TD | TE | NAV return 1y / 3y | Min lump / SIP | Exit load | Liquidity |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kotak Nifty Financial Services Ex-Bank Index Fund | IF | Kotak | 0.18 [C] | 99 [C] | 24 Jul 2023 [C] | not retrieved. 3y NAV return 12.0% equals the index price return (12.0%) while the sister ETF below shows 12.6%, so the fund lags the ETF by about 0.6 points a year [N] | n/r | -3.0 / 12.0 | Rs 100 / n/v | n/v | - |
| ICICI Prudential Nifty FS Ex-Bank ETF (FINIETF) | ETF | ICICI Pru | n/r | n/r | 28 Nov 2022 (first NAV) [N] | n/r | n/r | -2.6 / 12.6 | 1 unit | n/a | Rs 1.2 cr (0.9) |

### 5.3 Power, energy, capital goods, manufacturing, infrastructure

No fund on Nifty Power or Nifty Capital Goods was found by name in the AMFI NAV file. This is the thinnest part of the market and several figures below are aggregator-only.

| Product | Type | AMC | BER % | AUM | Launch | Benchmark | TD / TE | NAV return 1y / 3y | Min lump / SIP | Exit load | Liquidity |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Groww BSE Power ETF (GROWWPOWER) | ETF | Groww | 0.40-0.48 [A] | about Rs 273 cr [A] | 5 Aug 2025 [A] | BSE Power TRI | n/r | 4.3 / - | 1 unit | n/a | Rs 2.8 cr (2.1) |
| Groww BSE Power ETF FoF (Direct) | FoF on Coin | Groww | 0.14 [C] **plus** the ETF's own cost | Rs 37 cr [C] | 18 Jul 2025 [C] | BSE Power TRI | n/r | 5.15 (Coin) | Rs 500 / Rs 100 [A] | Nil [A] | - |
| Axis Nifty Energy Index Fund | IF | Axis | 0.20 [C] (Axis one-pager says "to be announced") | Rs 100 cr [C] | allotted 2 Sep 2026 [N] | Nifty Energy TRI | none yet | no history | Rs 100 / Rs 100 [F] | 0.25% if redeemed within 15 days [F] | - |
| Mirae Asset Nifty Energy ETF (ENERGY) | ETF | Mirae | 0.11-0.57, aggregators disagree [A] | Rs 290-322 cr [A] | 10 Nov 2025 (first NAV) [N] | Nifty Energy TRI | TE 0.10-0.17 [A] | no 1y history | 1 unit | n/a | Rs 1.4 cr (1.0) |
| Motilal Oswal Nifty Energy ETF (MOENERGY) | ETF | Motilal | n/r | n/r | 16 Oct 2025 (first NAV) [N] | Nifty Energy TRI | n/r | no 1y history | 1 unit | n/a | Rs 0.7 cr (0.4) |
| Axis Nifty Energy ETF (ENERGYAXIS) | ETF | Axis | n/r | n/r | 2 Sep 2026 [N] | Nifty Energy TRI | n/r | none | 1 unit | n/a | Rs 0.04 cr; 2 zero-volume days in 26; one day 6.2% from NAV. **Avoid** |
| ICICI Prudential Nifty Infrastructure ETF (INFRAIETF) | ETF | ICICI Pru | 0.42 [F] | 283.56 (31 Aug) [F] | 17 Aug 2022 [F] | Nifty Infrastructure TRI | -0.54 / -0.62 [F]; TE 0.03 [F] | -6.2 / 11.3 | 1 unit | n/a | Rs 3.8 cr (1.1) |
| Nippon India ETF Nifty Infrastructure BeES (INFRABEES) | ETF | Nippon | 0.50 [F] | 184.68 (31 Aug) [F] | 29 Sep 2010 [F] | Nifty Infrastructure TRI | -0.72 / -1.13 [F]; TE 0.05 [F] | -6.3 / 10.8 | 1 unit | n/a | Rs 0.9 cr (0.7) |
| Nippon India Nifty India Manufacturing Index Fund | IF | Nippon | 0.21 [C] (0.25 FY25-26 [F]) | 42.71 (31 Aug) [F] | 26 Aug 2025 [F] | Nifty India Manufacturing TRI | -0.31 [E]; TE 0.09 [F] | 0.3 / - | Rs 1,000 / Rs 100 [F] | Nil [F] | - |
| Navi Nifty India Manufacturing Index Fund | IF | Navi | 0.40 [C] | 87 [C] | 12 Aug 2022 [C] | Nifty India Manufacturing TRI | -0.37 [E] | 0.2 / 15.7 | Rs 100 / n/v | n/v | - |
| Nippon India Nifty India Manufacturing ETF (MANUFGBEES) | ETF | Nippon | 0.25 [F] | **11.72** (31 Aug) [F] | 26 Aug 2025 [F] | Nifty India Manufacturing TRI | -0.38 [F]; TE 0.05 [F] | 0.4 / - | 1 unit | n/a | Rs 0.17 cr. **Avoid** (tiny) |
| Mirae Asset Nifty India Manufacturing ETF (MAKEINDIA) | ETF | Mirae | about 0.42 [A] | Rs 227-247 cr [A] | 2022 (first NAV 28 Jan) [N] | Nifty India Manufacturing TRI | n/r | 0.1 / 15.6 | 1 unit | n/a | Rs 0.7 cr (0.6) |

What is in the indexes (why "energy" and "manufacturing" are not "power and grid" or "capital goods"):
- **Nifty Energy** (Axis one-pager, index weights 30 Jun 2026) [F]: Heavy Electrical Equipment 26%, Refineries and Marketing 15%, Oil Exploration and Production 12%, Power Generation 12%, Coal 10%. Top ten: Coal India 10.0%, Reliance 9.9%, ONGC 9.5%, NTPC 5.9%, GAIL 4.9%, Power Grid 4.6%, Suzlon 4.2%, CG Power 3.9%, GE Vernova T&D 3.6%, BHEL 3.6%. So refineries and oil exploration are 27% and coal another 10% (37% together, before gas utilities such as GAIL), which `04_sectors.md` calls cheap for a reason. About 26% is equipment, which that file calls expensive. The utility core (NTPC, Power Grid) is about 10.5%.
- **BSE Power** [A]: about 62.6% power generation/distribution and 37.4% electrical capital goods (Anand Rathi, July 2026), NTPC about 17%. This is closer to the power/grid view but rests on aggregator pages only, and the ETF has 14 months of history; it is 18.2% below its 27 May 2026 peak.
- **Nifty India Manufacturing** (Nippon factsheet top ten, Aug 2026) [F]: M&M 5.1%, Sun Pharma 4.9%, Reliance 4.7%, BEL 3.4%, Hindalco 3.4%, Bajaj Auto 3.1%, JSW Steel 2.8%, Divi's 2.8%. At least 13.9% of the fund sits in pharma and metals in the top ten alone, both on the avoid list.
- **Nifty Infrastructure** (ICICI ETF, Aug 2026) [F]: Reliance 20.0% (Nippon factsheet), L&T 12.6%, plus Bharti, UltraTech, Grasim, power and hospitals. Not a capex-purity play, and costs 0.42-0.50%.

### 5.4 Consumption and FMCG

| Product | Type | AMC | BER % | AUM (date) | Launch | Benchmark | TD 1y / 3y | TE | NAV return 1y / 3y / 5y | Min lump / SIP | Exit load | Liquidity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ICICI Prudential Nifty FMCG ETF (FMCGIETF) | ETF | ICICI Pru | 0.17 [F] | 735.18 (31 Aug) [F] | 5 Aug 2021 [F] | Nifty FMCG TRI | -0.13 / -0.19 [F] | 0.06 [F] | -18.8 / -3.9 / 3.4 | 1 unit | n/a | Rs 7.2 cr (5.9) |
| DSP Nifty FMCG ETF | ETF | DSP | n/r | n/r | 19 May 2026 (first NAV) [N] | Nifty FMCG TRI | n/r | n/r | no history | 1 unit | n/a | about Rs 0.01 cr. **Avoid** |
| Nippon India ETF Nifty India Consumption (CONSUMBEES) | ETF | Nippon | 0.31 [F] | 191.66 (31 Aug) [F] | 3 Apr 2014 [F] | Nifty India Consumption TRI | -0.33 / -0.41 [F] | 0.03 [F] | -11.4 / 8.8 / 8.8 | 1 unit | n/a | Rs 1.2 cr (0.9) |
| ICICI Prudential Nifty India Consumption ETF (CONSUMIETF) | ETF | ICICI Pru | 0.17 [F] | 51.42 (31 Aug) [F] | 28 Oct 2021 [F] | Nifty India Consumption TRI | -0.23 / -0.28 (scheme vs TRI table) [F] | 0.03 [F] | -11.3 / 8.9 / - | 1 unit | n/a | Rs 0.3 cr (0.1) |
| SBI Nifty India Consumption Index Fund | IF | SBI | 0.34 [C] | 259 [C] | 16 Oct 2024 [C] | Nifty India Consumption TRI | -0.48 [E] | n/r | -11.6 / - / - | Rs 5,000 / n/v | n/v | - |
| HDFC Nifty India Consumption Index Fund | IF | HDFC | 0.30 [C] | 115 [C] | first NAV 18 Feb 2026 [N] | Nifty India Consumption TRI | none yet | n/r | no 1y history | Rs 100 / n/v | n/v | - |

- Nifty FMCG: ITC 26.0%, HUL 18.4%, Nestle 11.3%, Britannia 6.5%, Tata Consumer 7.1%, Varun Beverages 5.8% (ICICI ETF, Aug 2026). Top three are 55.7%. ITC, HUL and Nestle are also in Nifty 50 (2.2%, 1.6%, 1.0% of it).
- Nifty India Consumption: Bharti Airtel 9.4%, Maruti 5.2%, HUL 5.1%, TVS 3.0%, Interglobe 3.5% (Nippon/ICICI factsheets, Aug 2026). It overlaps with autos and telecom, so it is not a clean FMCG vehicle.
- I found no Nifty FMCG open-ended index fund among the Coin-listed Direct funds I scanned (only the two ETFs above). A Nifty FMCG position therefore has to be bought on the exchange.
- Drawdown: ICICI FMCG ETF NAV is 32.1% below its 23 Sept 2024 peak and made its low on 1 Oct 2026, so there is no base yet.

### 5.5 Broad comparison funds (Nifty 50, Next 50, Nifty 500, Midcap 150)

| Product | Type | AMC | BER % | AUM (date) | Launch | TD 1y / 3y [source] | TE | NAV return 1y / 3y / 5y | Min lump / SIP |
|---|---|---|---|---|---|---|---|---|---|
| Nippon India ETF Nifty 50 BeES (NIFTYBEES) | ETF | Nippon | 0.04 [F] | 67,095.32 [F] | 28 Dec 2001 [F] | -0.03 / -0.06 [F] | 0.02 [F] | -10.3 / 5.4 / 5.6 | 1 unit; liquidity Rs 160 cr a day [Y] |
| Kotak Nifty 50 Index Fund | IF | Kotak | 0.07 [F] (Coin 0.06) | 1,156.66 [F] | 21 Jun 2021 [F] | -0.10 / -0.29 [E] | 0.06 [F] | -10.3 / 5.1 / 5.4 | Rs 100 / Rs 100 [F]; exit Nil [F] |
| Navi Nifty 50 Index Fund | IF | Navi | 0.06 [C] | 4,130 [C] | 3 Jul 2021 [C] | -0.13 / -0.19 [E] | n/r | -10.3 / 5.2 / 5.5 | Rs 100 |
| Edelweiss Nifty 50 Index Fund | IF | Edelweiss | 0.04 [C] | 287 [C] | 7 Oct 2021 [C] | -0.09 / -0.21 [E] | n/r | -10.2 / 5.2 / 5.4 | Rs 100 |
| UTI Nifty 50 Index Fund | IF | UTI | 0.18 [C] | 29,485 [C] | (placeholder) | -0.19 / -0.23 [E] | n/r | -10.4 / 5.2 / 5.4 | Rs 1,000 |
| Nippon India ETF Nifty Next 50 Junior BeES (JUNIORBEES) | ETF | Nippon | 0.17 [F] | 8,969.10 [F] | 21 Feb 2003 [F] | -0.11 / -0.20 [F] | 0.05 [F] | 0.0 / 15.3 / 10.1 | 1 unit; Rs 28 cr a day [Y] |
| Kotak Nifty Next 50 Index Fund | IF | Kotak | 0.08 [C] | 1,295 [C] | 17 Feb 2021 [C] | -0.21 / -0.35 [E] | n/r | -0.1 / 15.2 / 10.1 | Rs 100 |
| Edelweiss Nifty Next 50 Index Fund | IF | Edelweiss | 0.07 [C] | 303 [C] | 10 Nov 2022 [C] | -0.25 / -0.39 [E] | n/r | 0.0 / 15.2 / - | Rs 100 |
| ICICI Prudential Nifty Next 50 Index Fund | IF | ICICI Pru | 0.26 [F][C] | 10,116.69 [F] | 25 Jun 2010 [F] | -0.59 / -0.63 [F] | 0.16 [F] | -0.4 / 14.9 / 9.8 | Rs 100 |
| Motilal Oswal Nifty 500 Index Fund | IF | Motilal | 0.13 [C] | 3,195 [C] | 19 Aug 2019 [C] | -0.09 [E] | n/r | -5.7 / 8.5 / 7.8 | Rs 500 |
| Axis Nifty 500 Index Fund | IF | Axis | 0.09 [C] | 322 [C] | 26 Jun 2024 [C] | -0.30 [E] | n/r | -5.9 / - / - | Rs 100 |
| Motilal Oswal Nifty Midcap 150 Index Fund | IF | Motilal | 0.22 [C] | 4,151 [C] | 19 Aug 2019 [C] | -0.15 / -0.20 [E] | n/r | -0.3 / 12.7 / 13.1 | Rs 500 |
| Nippon India ETF Nifty Midcap 150 (MID150BEES) | ETF | Nippon | 0.21 [F] | 4,062.74 [F] | 31 Jan 2019 [F] | -0.17 / -0.24 [F] | 0.15 [F] | -0.3 / 12.7 / 13.1 | 1 unit; Rs 18 cr a day [Y] |
| ICICI Prudential Nifty Midcap 150 Index Fund | IF | ICICI Pru | 0.22 [F][C] | 1,328.47 [F] | 22 Dec 2021 [F] | -0.34 / -0.52 [F] | 0.06 [F] | -0.4 / 12.4 / - | Rs 100 |
| Tata Nifty Midcap 150 Index Fund | IF | Tata | 0.11 [C] | 332 [C] | 2 Jun 2025 [C] | -0.38 [E] | n/r | -0.5 / - / - | Rs 5,000 / Rs 1,000 |

Takeaways for the comparison: a sector index fund costs 0.13-0.25% at best against 0.04-0.08% for Nifty 50 and Next 50, so the sector call has to earn its extra cost and its extra concentration. Index funds lag their TRI by about 0.2-0.6 points a year; ETFs by 0.03-0.4 (Nippon Infrastructure BeES is the outlier at 0.7-1.2).

## 6. Smallcase vs funds: Windmill Auto (SCTR_0001), Energy (SCTR_0003), Banking (SCTR_0002)

Windmill facts are from `02_landscape.md` (smallcase API, 9 Oct 2026). Basket returns are smallcase price series, so I compare them with NSE **price** indexes from section 4. Series are sampled every 4-41 days, so windows are not exactly aligned.

### 6.1 Performance on the same basis (annualised price returns to 8 Oct 2026)

| Basket | Basket 1y / 2y / 3y | Matching index price 1y / 2y / 3y | Since 2019 vs Nifty 500 (11.8%) | Now vs own peak |
|---|---|---|---|---|
| Banking Tracker | 1.3 / 9.2 / 11.8 | Nifty Bank -2.7 / 3.4 / 7.1; Nifty Private Bank -2.0 / 2.9 / 5.4 | 8.1% (trails) | -10% (Feb 2026) |
| Auto Tracker | -1.9 / -1.8 / 14.5 | Nifty Auto -7.6 / -3.3 / 15.3 | 12.0% | -14% (Aug 2026) |
| Energy Tracker | -10.9 / -12.5 / 9.2 | Nifty Energy 1.6 / -7.6 / 10.1 | 11.1% (trails) | -27% (Jul 2024) |

The Banking tracker beat both bank indexes by roughly 4-6 points a year over 1-3 years; the Energy Tracker lagged Nifty Energy by 12.5 points over 1 year. Holdings are hidden, so I cannot say why.

### 6.2 Criteria

| Criterion | Windmill trackers | Index funds / ETFs |
|---|---|---|
| Cost per year | Subscription Rs 0. Running cost is rebalance trades only: STT 0.1% each way, DP Rs 15.34 per scrip sold, stamp 0.015% on buys, plus 20% tax on short-term gains realised. Quarterly updates (4 logged in 12 months) | Tracking difference 0.13-0.6% depending on product; no trading cost inside your account |
| Entry and exit charges | Entry about Rs 237 per Rs 1 lakh as one lump sum (Rs 118 platform fee); Rs 11.80 per AutoSIP run. Exit about Rs 257 for 10 stocks | Coin: stamp Rs 5, STT about Rs 1. ETF: about Rs 19 in, Rs 20 out, plus half-spread |
| Tax events from rebalances | Each rebalance you apply sells stocks: STCG 20% on lots under 12 months, 12.5% above Rs 1.25 lakh on older lots. smallcase's own blog lists "potential capital gains" as a cost | None inside the fund. Index reshuffles do not create a tax bill for you |
| Transparency of holdings | Login-gated; the API returns an empty constituent list. You see them after buying. Weights and the rule are not public. Basket P/E shown by smallcase is unaudited (Banking Tracker shows 7, which looks wrong for a bank basket) | Full portfolio in the AMC factsheet monthly and on AMC websites; index methodology public |
| SIP convenience on Zerodha | AutoSIP at Zerodha only when SIP is at least the basket minimum: Banking Rs 12,553 and Energy Rs 12,309 (only the Rs 15,000 SIP fits); Auto Rs 86,227 (no SIP at the stated amounts, and staging 4-6 tranches is not possible on the first buy). Whether later top-ups can be smaller than the first-buy minimum is unverified | Coin SIP from about Rs 100 for most funds; Kite ETF SIP, amount-based |
| Concentration | 10 stocks (Banking, cap mix 60/31/9), 14 (Auto, 47/18/35), 11 (Energy, 75/25/0). Weights unknown | Nifty Bank: 14 stocks, top five 61.4%. Nifty Private Bank: 10 stocks, top four 80.5%. Nifty Auto: top three 46.9%, M&M 22.8%. Nifty FMCG: top three 55.7% |
| Overlap with Nifty indexes | Not measurable. A tracker with 9% small-cap (Banking) or 35% small-cap (Auto) must hold names outside the large-cap indexes, but I cannot say which | Exact. Nifty Bank's top five banks are 29.5% of Nifty 50; the auto fund's top four are 6.5% of Nifty 50. Adding either duplicates what a broad index holds |
| Survivorship | `02_landscape.md`: at least 46% of thematic baskets found are no longer live. Windmill's own sector trackers have lasted since 2016 | Funds do close or merge, but passive large-AUM funds rarely vanish |

### 6.3 Where a smallcase gives something a fund cannot, and where it does not

Gives something a fund cannot:
- **A different stock mix.** The index funds are capped by their index rule (Nifty Auto's 15 names include 22.8% M&M). A tracker can include small and mid caps the index excludes (Auto Tracker is 35% small-cap; the Banking Tracker beat both bank indexes in 1-3 years). That is the only real argument for them. It cuts both ways: the Energy Tracker lagged its index by 12.5 points over 1 year.
- **A rule that avoids a bad sub-sector.** Nifty Energy has no way to exclude oil and gas. A basket could. But I cannot see whether Windmill's Energy Tracker does; `00_decision_memo.md` records that it "mixes oil and gas".
- **Full ownership of shares in your demat** (dividends paid directly, you can sell single stocks). This is a convenience, not a return advantage.

Does not give:
- **No cost advantage at Rs 1 lakh.** Entry plus exit alone is about 0.5% (Rs 237 + Rs 257). The `01_mechanics.md` 24-month example reached 1.6% with rebalances and an assumed 20% tax on Rs 4,000 of gains. A fund costs 0.03-0.05% explicit plus 0.2-0.6% a year of tracking difference.
- **No tax advantage.** Rebalances create tax events a fund does not.
- **No transparency advantage.** Holdings are hidden until purchase.
- **No staging advantage.** Auto cannot be staged; Banking and Energy need Rs 12,000-12,600 a tranche.
- **No lower concentration.** 10-14 stocks against the funds' 10-15 names; weights unknown.
- **Overlap with Nifty 50 cannot be measured**, so the diversification claim cannot be tested.

## 7. Verdicts: best instrument for a Rs 1 lakh staged entry

The sector views come from `04_sectors.md`. Sizes are arithmetic on the loss limit (section 8), not advice.

| Sector (view) | Best instrument | Why | Runner-up / when to use a smallcase | Main caveat |
|---|---|---|---|---|
| **Private banks and large lenders** (cheap, improving) | **ICICI Prudential Nifty Private Bank ETF (PVTBANIETF)** through a Kite SIP, 4-6 weekly or monthly runs | BER 0.13%, AUM Rs 4,287 cr, tracking difference -0.18/-0.19/-0.18 and tracking error 0.02-0.04% (ICICI, 31 Aug); Rs 8.4 cr a day traded; exactly the "private" half of the view, no PSU banks | DSP Nifty Private Bank Index Fund on Coin if you want no exchange orders: 0.23%, but my estimate of tracking difference is -0.57 against -0.18 for the ETF (about Rs 400 a year more per Rs 1 lakh), Rs 110 cr, from Feb 2025. For Nifty Bank, ICICI Pru Nifty Bank Index Fund (0.13%, Rs 794 cr, -0.26) is fine but 24% PSU banks. Windmill Banking Tracker (free, Rs 12,553 minimum, 9% small cap) only if you want its tilt and accept hidden holdings and about Rs 237 entry cost | Holds ICICI, Kotak, Axis and HDFC Bank = 80.5%, the same four that are 25.5% of Nifty 50. The investor already holds about a fifth in financials via index funds. Worst fall in the series: -50.6% (Mar 2020) |
| **Autos** (fair, leaning cheap) | **ICICI Prudential Nifty Auto Index Fund (Direct), Coin SIP** | BER 0.25%, AUM Rs 253 cr, tracking difference -0.47/-0.56 (Direct, ICICI), 3-year record from Oct 2022, any amount, Nil exit load, priced at NAV | **AUTOBEES** (BER 0.22%, Rs 497 cr, -0.37/-0.35) or ICICI Auto ETF (0.17%, -0.28/-0.26) via Kite SIP: about 0.1-0.2 points a year cheaper but you carry spread. Windmill Auto Tracker is not viable: Rs 86,227 minimum | Index is down 15.0% since 31 Aug; margins have not turned (`04_sectors.md`). 55% of the fund is M&M, Maruti, Bajaj Auto and Eicher, already in Nifty 50 |
| **Power and grid** (fair, improving) | **Groww BSE Power ETF (GROWWPOWER) via Kite SIP, small slice**, with eyes open | Closest listed match to a power/grid view (about 63% generation/distribution, 37% equipment per an aggregator). NTPC about 17%. Rs 2.8 cr a day | Axis Nifty Energy Index Fund (Direct, Coin, 0.20% per Coin, Rs 100 cr, 0.25% exit load within 15 days) if you want a Coin SIP, accepting 27% refining/exploration and 10% coal. Windmill Energy Tracker: 1y -10.9% against Nifty Energy +1.6%, holdings hidden; not recommended | Aggregator-only numbers for the Groww ETF (BER, AUM, composition). 14 months of history and already 18.2% below its May peak. Cost of the Coin FoF route is 0.14% plus the ETF's own cost, so it is dearer than the ETF |
| **Capital goods / manufacturing / infrastructure** (capital goods expensive but strong; infrastructure fair, EPS falling) | **Do not build a dedicated position.** The energy/power slice above already holds 26-37% heavy electrical equipment (Suzlon, CG Power, GE Vernova T&D, BHEL) | No fund tracks Nifty Capital Goods. Manufacturing funds hold at least 13.9% pharma and metals in their top ten. Infrastructure ETFs cost 0.42-0.50% and are 20% Reliance | If you still want one: Nippon India Nifty India Manufacturing Index Fund (0.21%, Direct) but Rs 43 cr, 12 months old, estimated tracking difference -0.31; avoid the tiny ETFs (Rs 11.7 cr and Rs 0.17 cr a day) | Cheap versions of these products exist, but they hold the wrong sectors for this view |
| **FMCG** (fair, de-rated) | **ICICI Prudential Nifty FMCG ETF (FMCGIETF)** via Kite SIP, in smaller, slower tranches | BER 0.17%, AUM Rs 735 cr, tracking difference -0.13/-0.19/-0.22, TE 0.06, Rs 7.2 cr a day; the only pure FMCG product with scale | Consumption index funds (SBI 0.34%; HDFC 0.30%) mix in Bharti, Maruti, Interglobe and are 36x earnings; skip | The fund is still making new lows (1 Oct) and 32% below peak; earnings growth is only about 6% (`04_sectors.md`). ITC 26%, HUL 18%, Nestle 11% |
| **Financials ex-bank / NBFCs** (fair, leaning cheap) | Kotak Nifty Financial Services Ex-Bank Index Fund (Coin, 0.18%, Rs 99 cr) or ICICI Pru FS Ex-Bank ETF | Only dedicated vehicles | Optional | Kotak fund lagged its sister ETF by about 0.6 points a year over 3 years (my calc). Rate hike risk per `04_sectors.md` |
| **Broad comparison** | Nifty 50: **NIFTYBEES** (BER 0.04%, Rs 67,095 cr, -0.03) or Kotak/Navi/Edelweiss index fund (0.04-0.07%). Next 50: Kotak Nifty Next 50 Index Fund (0.08%) or JUNIORBEES. Nifty 500: Motilal Oswal (0.13%). Midcap 150: Motilal or Nippon ETF | Cheapest ways to hold the market the sectors must beat | - | 3-year price return: Next 50 14.6%, Midcap 150 12.3%, Nifty 50 4.2%; sector indexes ranged -5.2% to 15.3% |

## 8. Loss-limit arithmetic (my calculation)

The memo records a 20-25% fall as the limit. Taking 25% of Rs 1,00,000 = Rs 25,000.

| Fund history (NAV, split-adjusted) | Worst peak-to-trough | Date | Now vs peak (8 Oct 2026) | 1-year volatility |
|---|---|---|---|---|
| Nifty Bank (BANKBEES, from Nov 2016) | -48.6% | 2 Jan to 23 Mar 2020 | -11.0% | 16.9% |
| Nifty Private Bank (ICICI ETF, from Aug 2019) | -50.6% | same | -7.5% | 16.6% |
| Nifty Auto (AUTOBEES, from Jan 2022) | -28.3% | 27 Sep 2024 to 7 Apr 2025 | -17.3% | 21.0% |
| Nifty India Consumption (CONSUMBEES) | -31.3% | 2018-2020 | -16.7% | 15.0% |
| Nifty FMCG (ICICI ETF, from Aug 2021) | -32.2% | 23 Sep 2024 to 1 Oct 2026 | -32.1% | 14.9% |
| Nifty Infrastructure (INFRABEES) | -42.5% | 5 Jan 2018 to 23 Mar 2020 | -12.6% | 15.5% |
| Nifty 50 (NIFTYBEES) | -38.4% | 14 Jan to 23 Mar 2020 | -14.8% | 13.6% |
| Nifty Next 50 (JUNIORBEES) | -40.5% | 2018-2020 | -11.7% | 17.3% |
| Nifty Midcap 150 (MID150BEES, from Feb 2019) | -38.3% | 2020 | -9.5% | 16.4% |
| BSE Power (GROWWPOWER, 14 months) | -18.2% | 27 May to 8 Oct 2026 | -18.2% | 19.3% |

- A repeat of the 2020 fall (Nifty 50 -38%) on Rs 1 lakh fully in sector funds loses roughly Rs 38,000-50,000, above the Rs 25,000 limit. Keeping the loss inside Rs 25,000 at a -40% fall means no more than about Rs 62,000 in equity funds of this kind; the rest would have to be cash, liquid funds or another low-risk asset.
- The auto fund's short history (since Jan 2022) probably understates its worst case; the Windmill Auto Tracker series shows -53% (coarse).
- Illustrative stakes that respect that cap, using the worst falls above: private banks Rs 20,000-25,000 (worst case about Rs 10,000-12,500), autos Rs 12,000-15,000, power slice Rs 8,000-10,000, FMCG Rs 8,000-10,000. This is arithmetic, not advice; the monthly Rs 5,000-15,000 would follow the same weights.
- Staging: the market is in a sharp fall (Nifty 50 -7.7% in five weeks; RBI hiked on 7 Oct). Equal tranches over 4-6 months reduce timing risk but cannot cap a fall.

## 9. What I could not verify (not filled from memory)

- **Tracking error and TD from the AMC** for Navi, Edelweiss, UTI, SBI, Tata, HDFC, Motilal, DSP, Groww, Mirae, Bandhan, Axis (except Energy one-pager) funds. TD for these is my estimate; TE is n/r.
- **Expense ratio and AUM** for the Mirae, Motilal and Axis energy/manufacturing ETFs and the Groww BSE Power ETF: aggregator pages disagreed (BER 0.11-0.57%, AUM Rs 18-322 cr), so I did not pick one.
- **BSE Power index composition**: Anand Rathi and PersonalFN pages only.
- **Bid-ask spread**: not measured (NSE quote API refused). Liquidity is average traded value from Yahoo, an aggregator.
- **ETF premium to NAV**: NSE intraday prices on 9 Oct are not comparable with the 8 Oct NAV. From Yahoo closes against AMFI NAV, the median daily gap over about 60 sessions was 0.11-0.27% (single-day maximum 0.4-6.2%), mixing timing, spread and premium. Treat as an upper bound on spread-plus-premium, not a measurement.
- **SIP minimums** for ICICI, Tata, SBI, UTI, Motilal, HDFC, DSP, Navi, Edelweiss index funds: not in the factsheets I read, and Coin does not show them. Confirm in the Coin SIP screen.
- **Exit loads** for funds other than ICICI, Kotak, Nippon (read in AMC documents) and Axis Energy (AMC one-pager).
- **STT on ETF sales at Zerodha**: Zerodha's charges page does not separate ETFs.
- **Tax law text**: Income-tax Act 2025 and Finance Act 2026 not read; rates rest on the CBDT FAQ and secondary guides. FoF funds qualify as equity-oriented only if at least 90% is in equity-oriented funds (secondary source); the Groww Power and Mirae Manufacturing FoFs should but I did not confirm.
- **Windmill holdings and weights**: gated. Everything about tilt and overlap is inferred from cap mix.
- **TRI returns beyond 31 Aug 2026**: niftyindices TRI download failed; 8 Oct comparisons use price indexes.
- **Date mismatch**: AMC returns (31 Aug) and my NAV returns (8 Oct) differ by a fall of 4-15% in the indexes. Both are shown and labelled.
- **Coin placeholders**: launch date 2013-01-01 on older funds; Mirae Manufacturing FoF shows an exit load of "0.05" without units.

## 10. Sources

Primary and near-primary:
- AMFI NAV file (latest NAV and ISIN list), 8 Oct 2026: https://portal.amfiindia.com/spages/NAVAll.txt
- NAV history mirror of AMFI data: https://api.mfapi.in/mf/<scheme code> (codes in table; e.g. https://api.mfapi.in/mf/147483)
- NSE index daily files (P/E, P/B, yield, closes): https://archives.nseindia.com/content/indices/ind_close_all_08102026.csv (and 31082026, 08102025, 08102024, 06102023, 08102021)
- NSE ETF list with prices/volumes (9 Oct 2026, 12:25): https://www.nseindia.com/api/etf
- ICICI Prudential passive factsheets, Aug 2026: https://www.icicipruamc.com/blob/knowledgecentre/factsheet-schemes/Passive%20Schemes/ETFs%20Schemes/ICICI%20Prudential%20Nifty%20Bank%20ETF.pdf (same folder for Auto, Private Bank, FMCG, India Consumption, Infrastructure, Nifty 50, Next 50 ETFs); index funds under `.../Passive%20Schemes/Index%20Schemes/ICICI%20Prudential%20Nifty%20Auto%20Index%20Fund.pdf` (also Bank, Private Bank, Next 50, Midcap 150, Nifty 500, Nifty 50)
- Nippon India September 2026 factsheet (data as on 31 Aug 2026): https://mf.nipponindiaim.com/InvestorServices/FactSheetsDocuments/Nippon-FS-September-2026.pdf ; August product notes under https://mf.nipponindiaim.com/FundsAndPerformance/ProductNotes/NipponIndia-ETF-Nifty-Bank-BeES-Aug-2026.pdf (also Nifty-Auto-ETF, Nifty-Auto-Index-Fund, Nifty-Bank-Index-Fund, ETF-Nifty-50-BeES, ETF-Nifty-Next-50-Junior-BeES, ETF-Nifty-India-Consumption, ETF-Nifty-Infrastructure-BeES, Nifty-India-Manufacturing-ETF, Nifty-India-Manufacturing-Index-Fund, ETF-Nifty-Midcap-150, Nifty-Midcap-150-Index-Fund)
- Kotak factsheets, Aug 2026: https://www.kotakmf.com/factsheet/August_2026/kotak/NIFTY-BANK-ETF.html ; https://www.kotakmf.com/factsheet/August_2026/kotak/NIFTY-50-INDEX.html
- Axis Nifty Energy Index Fund one-pager (NFO 7-21 Aug 2026): https://www.axismf.com/1/5/85/93/4551/4553/One_pager_Axis_Nifty_Energy_Index_Fund.pdf
- Zerodha charges: https://zerodha.com/charges ; Coin charges: https://support.zerodha.com/category/mutual-funds/about-coin/articles/what-are-the-charges-for-using-coin
- Zerodha Coin fund pages by ISIN, 8 Oct 2026: https://coin.zerodha.com/mf/fund/INF109KC16J4 (pattern `/mf/fund/<ISIN>`; ETFs have no Coin page)

Secondary / aggregator (flagged [A] or used for context only):
- Kite ETF SIP: https://zerodha.com/z-connect/business-updates/introducing-updated-stock-sip-experience-on-kite-web ; https://support.zerodha.com/category/trading-and-markets/charts-and-orders/stock-sip/articles/setup-stock-sip (via search summary)
- Tax summary for FY 2026-27: https://www.sahi.com/blogs/ltcg-tax-mutual-funds-stocks-budget-2026 ; HSBC reckoner https://www.assetmanagement.hsbc.co.in/assets/documents/mutual-funds/en/da5d1d18-343c-41d2-aaf9-e6967d009ee8/tax-reckoner-fy-2026-2027.pdf
- Groww BSE Power ETF: https://anandrathi.com/mutual-funds/schemes/groww-bse-power-etf ; https://www.valueresearchonline.com/funds/45370/groww-bse-power-etf/
- Mirae Asset Nifty Energy ETF: https://sharpely.in/etfs/mirae-asset-nifty-energy-etfgrowth/45587 ; https://www.tickertape.in/etfs/mirae-asset-nifty-energy-etf-ENE
- Mirae Asset Nifty India Manufacturing ETF: https://www.5paisa.com/mutual-funds/mirae-asset-nifty-india-manufacturing-etf
- Yahoo Finance daily prices via yfinance (traded value)
- Local reports: `reports/smallcase/00_decision_memo.md`, `01_mechanics.md`, `02_landscape.md`, `04_sectors.md`
