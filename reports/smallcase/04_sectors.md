# India sector map for a 1-2+ year view (as of 8-9 Oct 2026)

Prepared 2026-10-09. Research only, not personal advice. Every number below is either (a) computed by me from NSE files I downloaded, (b) read from an NSE/Nifty Indices document, or (c) taken from a named web source listed at the end. Where I could not verify something, it is listed in section 9 and not filled from memory.

## 1. Bottom line

The market is in a stress regime, so almost everything large-cap looks "cheap against its own history". What matters is which sectors are cheap AND have earnings that are rising AND are not already crowded.

- Regime: Nifty 50 closed 8 Oct 2026 at 22,232, down 14.3% year to date. Its trailing P/E is 19.0 against a 10-year monthly median of 23.2 (decade low in my sample: 18.7). A US/Israel-Iran war from 28 Feb pushed Brent from about $60 (31 Dec) to a $118 peak (31 Mar) and $103 now; the rupee is 96.6 per dollar (89.8 at end-2025); the RBI hiked the repo rate 25 bp to 5.50% on 7 Oct and said cuts are "off the table" (sources in section 8). Foreign investors sold about $24.6 bn of Indian equities in calendar 2026 through August (Finnovate).
- Earnings are not collapsing: NSE's Q1 FY27 review shows Nifty 500 PAT +11.1% year on year, but +22.6% excluding Energy, and Financials +24% do most of the work. Consensus FY27/FY28 earnings growth for the top 200 companies is 9.2% / 17.2% (NSE, LSEG data, 11 Sep), after FY27 was cut 4.1% since March.
- Cheap is not the same as a bargain. Four traps show up in the data: Realty (P/E at the 10th percentile of its history while index earnings per share are 3.0x their 10-year median), Metals (earnings per share up 46% in a year, near cycle highs), PSU banks (P/E 7.2 only because earnings are at a record) and Oil and Gas (P/B at the 2nd percentile because Q1 earnings collapsed). Details in section 5.

### Ranking (1-2+ year view)

| Rank | Sector | Verdict | One-line evidence |
|---|---|---|---|
| 1 | Private banks and large lenders | Cheap and improving | P/B 1.93 vs decade low 1.91 (2nd percentile); P/E 16.6 (18th pct); Q1 FY27 gross NPAs low and falling (Axis 1.28%, ICICI 1.38%) |
| 2 | Autos and auto components | Fair, leaning cheap and improving | P/B 3.83 (14th pct) with implied ROE 13.4% vs 16.1% median; Sept 2026 PV wholesales +21% YoY; margins squeezed |
| 3 | Power and grid (utilities, T&D) | Fair, improving (valuation history unverifiable) | Record 271 GW peak demand; BHEL order book Rs 2.60 lakh cr (+27%); Power Grid FY27 capex target Rs 370 bn; sector uncrowded |
| 4 | FMCG | Fair (de-rated, defensive) | P/E 30.4 and P/B 7.3 are decade lows; HUL volume growth 5%, best in 13 quarters; earnings growth only about 6% a year |
| 5 | NBFCs and other financials ex-banks | Fair, leaning cheap and improving | P/E 19.5 (23rd pct), P/B 3.56 (32nd pct); implied EPS +15.8% in a year; rate-hike funding cost is the risk |

Next in line (not ranked): Telecom (strong Q1, tariff-hike catalyst unconfirmed, no valuation history) and IT services (cheapest vs history, but "cheap for a reason").

### Three to avoid for new money

| Sector | Verdict | Why |
|---|---|---|
| Pharma (and healthcare) | Avoid | Highest relative valuation in the table (P/E 40.0, 78th pct own history; 99th pct vs Nifty 500) while index earnings per share are flat (-0.4%) and Nifty 50 healthcare PAT fell 18.7% in Q1; up 14.6% this year in a down market |
| Metals | Avoid for new lump sums | Cyclical near peak earnings: implied EPS +46% in 1 year, implied ROE 16.2% vs 11.3% median, P/B at the 78th percentile; price spike driven by West Asia disruption and China capacity cap |
| Realty | Avoid | Low P/E is an earnings-peak artefact; Anarock Q2 sales -6% YoY; unsold premium homes +43%; DLF bookings Rs 657 cr vs Rs 11,425 cr; RBI now hiking |

Also "expensive but strong, do not chase": Defence and Capital goods.

### Sectors that add something different to an AI/tech, US and broad-index portfolio

- Genuinely different: Power and grid, FMCG, Autos (domestic consumption cyclical), Telecom, upstream oil and gas (a hedge against an oil spike, because India imports oil).
- Mostly more of what you already hold: Private banks and NBFCs. The Nifty 50 factsheet (30 Sep 2026) shows HDFC Bank 10.38%, ICICI Bank 9.05%, SBI 3.79%, Axis 3.37% and Kotak 2.93%, which is 29.5% in five banks, before Bajaj Finance and others outside the top ten. A broad Indian index fund already owns this trade, so rank 1 is the best-value sector but not a diversifier.
- IT services overlap with your technology theme by label, but their risk is different: the market fears AI substitutes for IT-services labour. That is my reasoning, not a sourced fact; treat it as a hypothesis that Indian IT could behave like a partial hedge to your AI holdings, not as a proven one.

## 2. Method and what the numbers mean

- Valuation data: NSE's daily file `ind_close_all_DDMMYYYY.csv` (archives.nseindia.com) gives closing level, P/E, P/B and dividend yield for every NSE index. I downloaded 133 dates (one near each month-end from Sep 2016 to Sep 2026, plus anchor dates for 1/3/5 year returns, plus 7-8 Oct 2026). The 9 Oct 2026 file was not yet published (404), so "now" is the 8 Oct close. Yahoo shows the Nifty up about 1.1% on 9 Oct (22,486 intraday/last).
- "10-year percentile" = share of the monthly observations since Sep 2016 at or below today's value. "Cheap" = both P/E and P/B at or below the 33rd percentile; "expensive" = at or above the 67th; otherwise fair or mixed. Where the index has less than 60 observations I say "limited history" and do not label it.
- Returns are price returns on the sector index (no dividends); 3 and 5 year are annualised.
- Implied EPS = index level / index P/E; implied ROE = P/B divided by P/E. These are my derived measures. They move when the index constituents change (for example the Tata Motors split inside Nifty Auto), and I have not verified NSE's P/E methodology, so treat them as indicators of direction and cycle position, not exact earnings.
- Because the whole market has de-rated, I also report each sector's P/E and P/B relative to the Nifty 500, against its own 10-year relative history.
- Breadth: I downloaded Yahoo daily closes for 490 of the Nifty 500 stocks (list in `data/raw/nifty500_current.csv`, Aug 2025 to 9 Oct 2026) and computed, by NSE industry group, the share above the 200-day average and the share 30% or more below the 52-week high. The sample is too short to be rigorous (about 14 months) and prices are Yahoo's.
- The lab's own `data/raw` price files end in 2018 and were not needed; I did not open any SEALED file or anything under `private/`. Of the Yahoo sector tickers, only ^CNXIT, ^NSEBANK, ^CNXPHARMA, ^NSEI, ^NSEMDCP50 and ^CRSLDX returned history; ^CNXAUTO, ^CNXFMCG, ^CNXMETAL, ^CNXENERGY, ^CNXINFRA, ^CNXREALTY and ^CNXPSUBANK returned a single row, so those histories come from the NSE archive instead.

## 3. Valuation table: sector index vs its own history (8 Oct 2026)

P/E and P/B: now / 10-year median / percentile. DY = dividend yield now / 10-year median. "n" = monthly observations available.

| Index | P/E | P/B | DY % | Own-history read | Relative to Nifty 500 (P/E pct, P/B pct) | n |
|---|---|---|---|---|---|---|
| Nifty 50 | 19.0 / 23.2 / 1.5 | 2.73 / 3.58 / 2.3 | 1.24 / 1.25 | Cheap | 41, 5 | 132 |
| Nifty 500 | 21.3 / 26.4 / 5.3 | 3.03 / 3.56 / 9.9 | 1.04 / 1.16 | Cheap | n/a | 132 |
| Nifty Private Bank | 16.6 / 22.5 / 18 | 1.93 / 2.76 / 2 | 0.67 / 0.56 | Cheap | 35, 27 | 132 |
| Nifty Bank | 12.9 / 22.3 / 1.5 | 1.64 / 2.69 / 0.8 | 0.73 / 0.63 | Cheap (see note) | 14, 6 | 132 |
| Nifty PSU Bank | 7.2 / 8.5 / 13 | 1.11 / 1.04 / 63 | 0.80 / 0.77 | Mixed | 22, 91 | 132 (P/E 87) |
| Nifty Fin Services ex-Bank | 19.5 / 21.5 / 23 | 3.56 / 3.92 / 32 | 0.81 / 0.87 | Cheap-ish, limited history | 58, 81 | 62 |
| Nifty IT | 17.4 / 25.4 / 13 | 4.86 / 6.88 / 20 | 2.89 / 2.04 | Cheap | 47, 27 | 132 |
| Nifty Auto | 28.5 / 30.6 / 43 | 3.83 / 4.72 / 14 | 1.19 / 1.06 | Fair to cheap | 61, 46 | 132 |
| Nifty FMCG | 30.4 / 41.9 / 1.5 | 7.29 / 10.7 / 0.8 | 1.08 / 1.67 | Cheap vs history, not cheap in absolute terms | 36, 14 | 132 |
| Nifty Pharma | 40.0 / 35.0 / 78 | 4.86 / 4.72 / 58 | 0.54 / 0.65 | Expensive | 99, 92 | 132 |
| Nifty Healthcare | 40.8 / 37.6 / 82 | 5.18 / 5.39 / 34 | 0.49 / 0.59 | Expensive | 96, 99 | 79 |
| Nifty Metal | 15.6 / 16.4 / 45 | 2.52 / 1.92 / 78 | 1.58 / 3.30 | Fair on P/E, rich on P/B | 61, 95 | 132 |
| Nifty Energy | 14.1 / 13.9 / 53 | 1.96 / 2.00 / 48 | 1.94 / 2.40 | Fair | 94, 91 | 132 |
| Nifty Oil and Gas | 10.3 / 11.5 / 34 | 1.28 / 1.71 / 2 | 1.90 / 2.78 | Mixed (cheap on P/B) | 66, 10 | 90 |
| Nifty Infrastructure | 21.3 / 22.9 / 32 | 2.53 / 2.64 / 46 | 1.02 / 1.30 | Fair | 64, 90 | 132 |
| Nifty Realty | 33.7 / 48.7 / 10 | 3.48 / 3.08 / 58 | 0.52 / 0.37 | Mixed (trap, see 5.12) | 26, 77 | 131 |
| Nifty India Defence | 55.8 / 47.5 / 83 | 10.5 / 10.5 / 49 | 0.52 / 0.57 | Expensive | 98, 83 | 63 |
| Nifty Consumer Durables | 57.2 / 68.2 / 17 | 9.17 / 11.9 / 8 | 0.42 / 0.42 | Cheap vs own history, 57x in absolute terms | 42, 34 | 90 |
| Nifty Chemicals | 41.7 / 44.0 / 36 | 3.66 / 4.22 / 5 | 0.58 / 0.66 | Limited history | n/a | 22 |
| Nifty Power | 18.1 | 2.20 | 1.67 | No history (listed in NSE files from 30 Jun 2026) | n/a | 5 |
| Nifty Capital Goods | 43.4 | 8.79 | 0.61 | No history | n/a | 5 |
| Nifty Telecommunications | 15.0 | 8.03 | 0.47 | No history | n/a | 5 |
| Nifty Cement | 24.8 | 1.90 | 0.43 | Only since 27 Feb 2026 | n/a | 9 |
| Nifty Construction | 18.0 | 2.23 | 0.98 | No history | n/a | 5 |
| Nifty NBFC / Insurance / Hospitals | 20.0 / 24.6 / 61.5 | 3.11 / 7.44 / 8.17 | 0.62 / 0.26 / 0.18 | No history | n/a | 5 |
| Nifty Midcap 100 | 27.3 / 32.3 / 35 | 3.68 / 3.22 / 67 | 0.67 / 0.98 | Fair | 50, 83 | 109 |
| Nifty Smallcap 250 | 33.9 / 32.2 / 57 | 3.36 / 3.06 / 61 | 0.62 / 0.88 | Fair, but P/B is the richest vs Nifty 500 in its history (100th pct) | 72, 100 | 124 |

Note on Nifty Bank and PSU banks: the bank P/E history includes years when bad loans depressed earnings (Nifty Bank P/E peaked at 67 and PSU Bank at 179 in the window), which inflates the median. Using P/B and implied ROE gives a cleaner picture: Nifty Bank implied ROE is 12.7% today against a 12.4% median, so the P/B discount is real rather than a result of peak earnings. For PSU banks the implied ROE is 15.4% against a 14.7% median and an 18.4% maximum, so their earnings are good rather than trough.

## 4. Returns, earnings growth, cycle position and breadth

Price returns to 8 Oct 2026 (NSE file); implied EPS growth as defined in section 2. "EPS vs 10y max" near 1.00 means implied earnings are at their decade high.

| Index | YTD | Since 27 Feb (war start) | 1y | 3y CAGR | 5y CAGR | Implied EPS 1y | Implied EPS 3y CAGR | EPS vs 10y max | Implied ROE now / median |
|---|---|---|---|---|---|---|---|---|---|
| Nifty 50 | -14.3% | -11.7% | -11.2% | 4.2% | 4.4% | +3.4% | 9.8% | 0.99 | 14.4 / 15.2 |
| Nifty 500 | -8.7% | -6.7% | -6.5% | 7.7% | 7.1% | +6.1% | 11.2% | 0.99 | 14.2 / 14.7 |
| Private Bank | -5.5% | -6.1% | -2.0% | 5.4% | 6.3% | +8.7% | 8.8% | 0.95 | 11.6 / 11.5 |
| Bank | -7.9% | -9.9% | -2.7% | 7.1% | 7.6% | +16.5% | 15.8% | 1.00 | 12.7 / 12.4 |
| PSU Bank | -5.2% | -18.6% | +6.3% | 15.3% | 25.7% | +15.3% | 19.2% | 1.00 | 15.4 / 14.7 |
| Fin Services ex-Bank | -8.0% | -7.2% | -3.2% | 12.0% | n/a | +15.8% | 13.7% | 1.00 | 18.2 / 18.2 |
| IT | -27.0% | -9.4% | -21.3% | -5.0% | -5.3% | +14.7% | 10.2% | 1.00 | 27.9 / 26.1 |
| Auto | -12.1% | -12.9% | -7.6% | 15.3% | 17.2% | -10.8% | 10.8% | 0.83 | 13.4 / 16.1 |
| FMCG | -20.2% | -14.2% | -19.4% | -5.2% | 1.9% | +6.6% | 6.0% | 0.99 | 23.9 / 25.3 |
| Pharma | +14.6% | +12.5% | +19.0% | 19.5% | 12.2% | -0.4% | 10.9% | 0.92 | 12.2 / 13.5 |
| Metal | +7.8% | -3.0% | +17.1% | 20.7% | 15.9% | +45.8% | 40.5% | 0.81 | 16.2 / 11.3 |
| Energy | +2.4% | -3.8% | +1.6% | 10.1% | 8.3% | +10.6% | 1.4% | 0.85 | 13.9 / 14.6 |
| Oil and Gas | -13.1% | -15.6% | -9.3% | 9.9% | 5.1% | +7.1% | 4.2% | 0.80 | 12.4 / 14.8 |
| Infrastructure | -10.5% | -10.8% | -6.5% | 10.9% | 10.7% | -3.7% | 7.7% | 0.90 | 11.9 / 12.3 |
| Realty | -8.4% | +2.0% | -9.0% | 10.7% | 8.9% | +15.7% | 25.1% | 0.99 | 10.3 / 6.6 |
| Defence | +17.2% | +10.3% | +12.2% | 39.4% (since Jan 2022 base) | n/a | +11.0% | 21.9% | 0.97 | 18.8 / 22.0 |
| Consumer Durables | -1.6% | -5.2% | -6.9% | 6.7% | 4.4% | +13.3% | 10.8% | 0.99 | 16.0 / 18.2 |
| Smallcap 250 | +6.0% | +10.1% | +3.1% | 12.4% | 12.5% | -7.3% | 1.2% | 0.85 | n/a |
| Midcap 100 | -3.4% | -2.1% | 0.0% | 12.8% | 13.0% | n/a | n/a | n/a | n/a |

Note: the Auto implied EPS fall is probably affected by the Tata Motors demerger inside the index, which I could not verify; treat the -10.8% with caution.

Breadth by NSE industry group (my calculation from Yahoo prices, 490 Nifty 500 stocks, 9 Oct 2026). The overall market: 37.8% of stocks above their 200-day average, 28.0% are 30% or more below their 52-week high, and 17.3% are within 10% of it.

| Industry group | Stocks | % above 200-day | % 30%+ below high | Median 12m return | Median since 27 Feb |
|---|---|---|---|---|---|
| Financial Services | 97 | 31 | 20 | -6% | -6% |
| Capital Goods | 69 | 49 | 25 | +6% | +7% |
| Healthcare | 44 | 61 | 7 | +7% | +12% |
| Auto and Auto Components | 40 | 35 | 25 | -6% | -7% |
| FMCG | 28 | 25 | 36 | -16% | -13% |
| Chemicals | 26 | 42 | 35 | -11% | +3% |
| Information Technology | 24 | 42 | 50 | -14% | +4% |
| Metals and Mining | 18 | 17 | 22 | +1% | -9% |
| Oil, Gas and Fuels | 17 | 41 | 24 | -1% | -9% |
| Power | 17 | 18 | 35 | -11% | -6% |
| Consumer Durables | 16 | 31 | 50 | -17% | -6% |
| Construction | 13 | 23 | 62 | -28% | -16% |
| Realty | 13 | 31 | 31 | -17% | +6% |
| Construction Materials | 11 | 0 | 64 | -25% | -16% |
| Telecommunication | 11 | 27 | 27 | -2% | -3% |

Reading the breadth: only Healthcare, Services (not tabled) and, near half, Capital Goods have a majority or near-majority of stocks above their 200-day average; Construction Materials has none. That fits the goodreturns report that 252 of the Nifty 500 are 30%+ below their highs (my figure for the 490 I could price is 28%, about 137 stocks; the gap is probably the different measurement window, I did not reconcile it).

## 5. Sector by sector

For each: valuation, cycle position, 1-2 year drivers and risks, crowding, verdict. Company figures come from secondary sources (broker notes, news, aggregator sites) except where marked NSE, because exchange filings were not reachable; where sources disagreed I say so.

### 5.1 Private banks and large lenders (Nifty Private Bank, Nifty Bank): cheap and improving

- Valuation: Private bank P/B 1.93 is within 0.02 of its decade low (1.91) and at the 2nd percentile; P/E 16.6 at the 18th. Nifty Bank P/B 1.64 is the decade low. Against the Nifty 500, Nifty Bank's P/B is at the 6th percentile of its relative history. Implied ROE is about median (11.6% private, 12.7% Nifty Bank), so this is a discount on normal profitability, not on peak profitability.
- Earnings: implied EPS +16.5% (Nifty Bank) and +8.7% (private) over 1 year. NSE's Q1 FY27 review: Financials PAT +19.2% (Nifty 50) and +23.7% (Nifty 500), and Financials plus Materials gave about 95% of Nifty 50 earnings growth. Axis Bank said Q1 may be the trough of its margin cycle (target 3.8% over time) with gross NPA 1.28% and credit cost 0.63%; ICICI Bank gross NPA fell to 1.38% from 1.67% while advances grew 19.6% (Swastika; Arihant). A pre-season broker preview expected about 16.8% credit growth.
- Cycle position: credit-quality cycle is near its best; margin cycle near a trough after the 2025-26 rate cuts; policy rates now turning up. The risk is that asset quality only has one direction from here.
- Risks: deposit growth lagging credit growth (NSE review notes this), CASA slipping (ICICI 38.1% from 41.2%), margin effect of the hike is genuinely ambiguous (faster repricing of loans vs slower deposits; I found no sourced 2026 analysis), bond mark-to-market losses with US 10-year at 5.2-5.3%, and rising credit costs later if growth slows.
- Crowding: not crowded. Financial services was the sector where foreigners sold most in 2026 per PL Quant (persistent selling January-August), though they bought about $1.1 bn in August. Only 31% of financial stocks are above their 200-day average.
- Portfolio fit: weak diversifier (see section 1).
- Verdict: cheap and improving. I would rather own the large private lenders than PSU banks (next).

### 5.2 PSU banks: fair (low P/E is a peak-earnings signal)

- Valuation: P/E 7.2 (13th pct) but P/B 1.11 (63rd pct); implied ROE 15.4% vs 14.7% median, and implied EPS at its decade high (1.00 of max) after +19% a year for three years and +39% a year over five (my calculation). This is the "cheap because earnings are at the top" case.
- Evidence of fading momentum: PNB Q1 FY27 profit about Rs 5,253 cr from a low base, but net interest income only +2%, provisions doubled to Rs 792 cr, domestic margin 2.64% vs 2.84% a year earlier (Swastika). The sector index fell 18.6% since 27 Feb, the biggest drop of any bank group. A Budget write-up found no disinvestment signal for PSU banks (Prime Investor).
- Crowding: not crowded now. Verdict: fair; not a bargain. Sell-side enthusiasm after a 26% annual price gain over five years is already in the price.

### 5.3 NBFCs and other financials ex-banks: fair, leaning cheap and improving

- Valuation (since Feb 2022 only, 62 observations): P/E 19.5 (23rd pct), P/B 3.56 (32nd pct), implied ROE 18.2% equal to its median. Relative to the Nifty 500 it is not cheap (P/B at the 81st percentile) because the whole market has de-rated.
- Earnings: implied EPS +15.8%. Bajaj Finance Q1 PAT about +28% with AUM +24% and credit cost about 1.5%; Shriram Finance PAT about +60%, AUM +15%, guided credit cost 2% (secondary sources, figures varied between outlets).
- Risk: the hike cycle just began (RBI said "calibrated tightening"; Goldman Sachs expected hikes in October and December per ETV Bharat). A Business Standard piece on the 2022 cycle said some NBFC stocks fell 30-50% from highs. I found no October 2026 market reaction. Also the Budget raised securities transaction tax on F&O, which is a negative for broking and exchange-type names in this index.
- Verdict: fair, leaning cheap and improving, but rate-sensitive; size it as part of the same financials bucket as 5.1.

### 5.4 IT services: cheap for a reason

- Valuation: P/E 17.4 (13th pct; 5-year percentile 4%), P/B 4.86 (20th pct), dividend yield 2.89% (89th percentile of its history, my calculation). Relative to the Nifty 500 the P/E is average (47th pct), so about half the cheapness is the market-wide de-rating.
- Price: -27.0% YTD, -21.3% over one year, -5.3% a year for five years. Implied EPS is at its decade high (+14.7% in a year), so the index has de-rated on fear, not on earnings so far. NSE: IT PAT +11.7% (Nifty 50) and +16.4% (Nifty 500) in Q1.
- What worries the market: AI substituting for coding, testing and support work; Accenture's weak outlook; Infosys's guide cut (reports differ between 1.5-3% and a trimmed upper end; verify against the filing) with flat organic growth; TCS dollar revenue growth only about 3% year on year; Wipro guided to -1% to +1% next quarter; HCLTech held 2-4%. Emkay cut sector estimates 1% for FY27 and 2% for FY28 (search summary). Offsets: a rupee near 96.6 helps margins, Budget 2026 improved data-centre and GCC tax treatment, Coforge jumped 10% on its Q1.
- Crowding: foreigners bought about $434 m in August after heavy YTD selling. Half of IT stocks in the Nifty 500 are 30%+ below their highs.
- Portfolio fit: you already hold AI/technology. This is a different risk (AI as a threat to Indian IT labour arbitrage), but it is the same label and I cannot show it hedges anything. 
- Verdict: cheap for a reason. A value-trap test is whether organic growth turns positive, which is not visible yet.

### 5.5 Autos and auto components: fair, leaning cheap and improving

- Valuation: P/E 28.5 (43rd pct, distorted by past low-earnings years), P/B 3.83 (14th pct), implied ROE 13.4% vs 16.1% median, so profitability is below normal and has room to recover.
- Volume cycle: strong. India PV wholesale dispatches +20.9% YoY in September 2026 to 457,604 units, and retail registrations +32.1% (Vahan) according to trade-press summaries; Maruti Q1 volume +29.3%, Bajaj Auto Q1 profit +42%, TVS +51% (secondary sources). The September 2025 base was depressed by buyers waiting for the GST cut that took effect 22 Sep 2025, so growth rates flatter from here; this base effect will fade from Q3 FY27.
- Margin cycle: weak. Maruti's Q1 EBITDA margin was 8.2%, down 380 bp as material cost jumped 600 bp to 80.5% of sales; profit fell about 9-11% despite revenue +36%. Two-wheelers held margins better.
- Other drivers: BofA turned positive on autos (July); Budget 2026 cut duties on battery minerals and kept EV production incentives. Risks: crude at $103 and a Rs 7.5 per litre petrol hike in May, higher auto-loan rates, and the Middle East cost shock.
- Crowding: not crowded. Foreigners bought about $329 m in August after a weak 2026, but only 35% of auto stocks are above their 200-day average and the sector is down 12% YTD.
- Verdict: fair, leaning cheap and improving. The evidence for improvement is volumes; margins have not yet turned.

### 5.6 FMCG: fair (de-rated, defensive diversifier)

- Valuation: P/E 30.4 and P/B 7.29 are the lowest in the 10-year sample (P/E 1.5th pct, P/B 0.8th pct). But 30 times earnings that are growing about 6% a year (3-year CAGR 6.0%, 5-year price CAGR 1.9%) is not cheap in absolute terms; the 10-year median of 42x belonged to a period of scarcity pricing. Relative to the Nifty 500, P/B is at the 14th percentile, P/E the 36th.
- Earnings: NSE Q1: Consumer Staples PAT -10.5% in the Nifty 50 (a drag), but +27.7% outside the Nifty 50. HUL turnover +10% with underlying volume growth 5% (best in 13 quarters) and operating margin 23.0%, down 40 bp sequentially; Nestle India sales +25.4%, profit +48%. I could not find ITC's Q1 numbers.
- Risks: crude-linked packaging and edible-oil input costs, a consumer squeezed by fuel and rate rises, and the decade-long de-rating continuing. CRISIL (pre-season) expected only 2-3% volume growth for FY27, which Q1 beat.
- Crowding: the least crowded of the quality sectors: foreigners were the persistent sellers (August -$203 m), a third of FMCG stocks are 30%+ below highs, and the sector fell 20% YTD.
- Portfolio fit: the most different from AI/tech and US holdings.
- Verdict: fair; valuation support is relative, not absolute. It needs earnings growth to move from 6% toward 10% to work.

### 5.7 Pharma and healthcare: avoid

- Valuation: Pharma P/E 40.0 (78th pct; 96th pct over 5 years), Healthcare P/E 40.8 (82nd pct). Relative to the Nifty 500, pharma P/E is at the 99th percentile of its history (1.87x vs median 1.39x). It is the only large sector that is expensive on both measures while the market is cheap.
- Earnings are not supporting it: implied EPS -0.4% in one year; NSE Q1: Health Care PAT -18.7% (Nifty 50) and -0.4% (Nifty 500), blamed on weaker North American performance. Sun Pharma: US formulations -9.7% to $427 m (specialty +12.8%), EBITDA margin 28.9% vs 31.1%; Dr Reddy's profit down about 69% on a semaglutide API quality charge; Cipla profit down about 39% (verify, the table was hard to read). The domestic market is healthy (IPM +13.5% in Q1) and Budget 2026 gave Rs 10,000 cr for biologics.
- Policy risk: a 100% US tariff on patented drugs from April 2026; generics exempt for two years from 1 Aug 2026, with reports of tariffs of 100-200% afterwards (sources differ). This is a 2028 cliff, but it sits inside a "several years" holding period.
- Crowding: it was the best-performing large sector this year (+14.6% YTD while Nifty -14.3%), foreigners bought about $628 m in August, and 61% of healthcare stocks are above their 200-day average, among the highest of any group (Services is 62%).
- Verdict: avoid for new money. Rich price, flat earnings, crowded safe-haven. A fall in the multiple would be the only entry signal.

### 5.8 Metals: avoid for new lump sums (cheap at peak earnings is the trap)

- Valuation: P/E 15.6 looks middling (45th pct), but P/B 2.52 is at the 78th percentile (95th relative to the Nifty 500) and the dividend yield is 1.58% against a 3.30% median.
- Cycle position: implied EPS +46% in a year and +41% a year for three; implied ROE 16.2% vs 11.3% median. NSE: Materials PAT +68.6% (Nifty 50, Q1), the biggest contributor to earnings growth together with financials. Prices doing the work: aluminium about $3,616/t and copper +40% year on year in the quarter, driven by West Asia disruption and a China capacity cap (ICRA via search summary); steel realisations +11% (JSW) behind a 12% safeguard duty. Hindalco posted a record quarter (profit Rs 7,013 cr, +75%).
- Risks: a commodity price reversal (a Goldman view from late 2025 expected aluminium -18% by end-2026, flagged as stale), coking coal cost, Chinese steel exports, and the safeguard duty tapering in April 2027. The sector index is up 17% in a year but only 17% of metal stocks are above their 200-day average, which suggests momentum has already faded under the surface.
- Crowding: foreigners called metals and capital goods the year's main beneficiaries of inflows (PL Quant, Jan-Aug).
- Verdict: avoid for new money; a long-term holder with a falling-price entry plan could revisit. 

### 5.9 Energy, oil and gas: cheap for a reason (binary on crude and policy)

- Valuation: Oil and Gas P/E 10.3 (34th pct), P/B 1.28 (2nd pct), dividend yield 1.9% vs 2.8% median. Nifty Energy P/E 14.1 (53rd pct).
- Earnings: NSE Q1: Energy EBITDA -37.4% and PAT -9.2% (Nifty 50) / -53.3% (Nifty 500); operating margin 15.5% to 7.4%. Brent averaged about $96.9 in the quarter; state oil marketers lost money (IOC loss about Rs 2,662 cr standalone, BPCL about Rs 1,873 cr, HPCL about Rs 11,526 cr standalone); the oil ministry put under-recoveries at Rs 74,781 cr in the quarter and Rs 2.18 lakh cr cumulatively.
- What flips it: if crude falls, marketing margins recover sharply (positive for OMCs, negative for upstream); if crude stays near $100, losses and subsidy bills persist and windfall taxes remain a risk for upstream. I did not find Reliance or ONGC Q1 numbers.
- Crowding: foreigners sold Oil and Gas in August (-$186 m). Verdict: cheap for a reason. Its portfolio role is a hedge: ONGC/Oil India-type upstream exposure would help if oil spikes again, which hurts the rest of an India-heavy portfolio. This is a hedging idea, not a growth call.

### 5.10 Power and grid (utilities, transmission and equipment): fair, improving

- Valuation: Nifty Power P/E 18.1, P/B 2.20, DY 1.67%; NSE only started publishing history for it on 30 Jun 2026, so I cannot show where that sits against its past. Nifty Energy (which holds NTPC, Power Grid, Coal India, ONGC and others) trades at the median.
- Demand: record 271 GW peak on 21 May 2026; all-India electricity demand +9.4% in April-July (ICRA); Fitch expects 4-5% growth for FY27, Crisil up to 7%, ICRA 6.5%. Thermal capacity additions lag plans (9.4 GW achieved vs 12.8 GW target in FY26; 21 GW of projects stuck), so the new-build pipeline supports orders.
- Earnings and orders: NTPC group PAT +13% (Rs 6,896 cr); Power Grid profit flat at Rs 3,598 cr (about +6% excluding a one-off) with capex run-rate toward a Rs 370 bn target; BHEL order inflow Rs 26,745 cr (nearly double a year earlier), order book Rs 2.60 lakh cr (+27%), first June-quarter profit since FY19. NSE: Utilities PAT +20.7% (Nifty 500). Budget 2026 kept duties low on solar and storage inputs and nuclear equipment. BofA turned positive on regulated power utilities.
- Risks: weather-driven demand, coal availability, PSU capital allocation, and rich multiples in power-equipment small caps (TD Power at about 94x trailing earnings per the lab's 5 Oct report). Thermal PLF is only 66-68%.
- Crowding: low. Foreigners sold Power (-$164 m in August), 82% of power stocks are below their 200-day average and 35% are 30%+ below their highs.
- Portfolio fit: genuinely different (regulated, domestic, low AI/US correlation).
- Verdict: fair, improving, with the caveat that I cannot place its valuation in history. Prefer regulated utilities and grid over rich equipment names.

### 5.11 Capital goods and industrials (including construction): expensive but strong

- Valuation: Capital Goods P/E 43.4 and P/B 8.79 (no history). Nifty Infrastructure P/E 21.3, 32nd percentile, with implied EPS -3.7% in one year, so it is cheaper but not growing. Construction stocks are the weakest group in the breadth table (62% are 30%+ below their highs; median -28% over 12 months).
- Orders: L&T order book Rs 7.79 lakh cr (+27%), Q1 inflow Rs 1.08 lakh cr (+14%), but revenue +7% against 10-12% guidance and EBITDA margin 9.0% from 9.9%; ABB India orders +50% and backlog Rs 11,898 cr (+22%) but PAT +8%. Budget 2026 central capex Rs 12.2 lakh cr (+11.5%, described as steady rather than expansive; FY26 capex undershot budget).
- Crowding: foreigners called this a 2026 inflow beneficiary but sold in August (-Rs 15.6 bn per PL; +$63 m per Finnovate; the sources disagree on the sign). Verdict: expensive but strong; wait for a pullback or buy via power/grid instead.

### 5.12 Realty: avoid

- Valuation trap: P/E 33.7 is at the 10th percentile of its history (median 48.7), but implied EPS is 3.0x its decade median and at 0.99 of the decade maximum, and implied ROE is 10.3% vs 6.6% median. The history is dominated by lumpy or depressed earnings.
- Demand evidence conflicts: PropEquity says top-9-city sales +19% YoY in Q2 2026, Anarock says top-7-city sales -6% (slowest since early 2023). Listed developers: Godrej Properties bookings Rs 8,651 cr (up from Rs 7,082 cr), Lodha Rs 4,630 cr, DLF Rs 657 cr vs Rs 11,425 cr with no launches. Knight Frank: unsold inventory +4% to 525,695 units, with the Rs 2-5 crore band +43%.
- Rate hike is a headwind for affordability; the "rate pause" article I found pre-dates 7 Oct. Foreigners sold Realty in August (-$63 m).
- Verdict: avoid. The index is +2% since 27 Feb, i.e. it has held up while rate and demand risks grew.

### 5.13 Defence: expensive but strong (do not chase)

- Valuation: P/E 55.8 (83rd pct since Jan 2022), 98th percentile relative to the Nifty 500; implied EPS +22% a year for three years; price +17% YTD while the market fell.
- Orders: HAL order book about Rs 2.5 lakh cr (one source with a conflicting Rs 94,000 cr figure, which I discarded); BEL Q1 order inflow about Rs 3,750 cr (-49%), order book Rs 723 bn (-3.5%), revenue +25%, EBITDA margin about 25% vs 28% target, but FY27 inflow guidance above Rs 55,000 cr hinges on QRSAM approval expected in Q2; Mazagon Dock order book fell to Rs 18,218 cr from Rs 20,535 cr with two mega-submarine contracts pending. Budget 2026 defence capital outlay about Rs 2.31 lakh cr (+17%; Prime Investor also printed Rs 2.19 lakh cr, so check).
- Verdict: the earnings are real but the price already pays for them and near-term order inflow is soft. Entry only on a de-rating or after large contracts are signed.

### 5.14 Cement and construction materials: fair, wait (no valuation history)

- NSE has published a Cement index only since 27 Feb 2026 (P/E 24.8, P/B 1.90). Sector volumes +7-8% in Q1 (UltraTech +12% volume, profit +17%), but fuel and freight costs from the West Asia conflict are expected to peak in Q2, which is seasonally weak. India Ratings expects mid-single-digit demand growth in FY27. Mixed brokers (BofA positive; ICICI Securities Hold on UltraTech).
- Crowding/breadth: 0 of 11 cement stocks are above their 200-day average and 64% are 30%+ below highs; the index is down 17.6% since 27 Feb. A contrarian case may form in H2 FY27 if margins recover (JM Financial's view), but I cannot show it is cheap against history. Verdict: fair, wait.

### 5.15 Telecom: fair, improving (no valuation history; next in line)

- Valuation: Nifty Telecommunications P/E 15.0, P/B 8.03, DY 0.47% (history since 30 Jun 2026 only). It is the sector index with the smallest drawdown (near highs).
- Earnings: Airtel Q1 profit about Rs 8,167 cr (+37%), ARPU Rs 264 (from Rs 250); Jio Platforms profit +9.2%, ARPU Rs 215.6. NSE: Communication Services PAT +39.7% (Nifty 50) and +127% (Nifty 500, small base).
- Catalysts and risks: Morgan Stanley expects 16-20% tariff rises (a forecast; I found no announced headline hike), and Jio's roughly Rs 37,700 cr IPO (SEBI observation received, listing expected by end-2026) could either trigger a tariff increase or add a large supply of telecom stock. Foreigners sold Telecom most of all sectors in August (-$527 m, -Rs 33.2 bn).
- Portfolio fit: domestic subscription revenue, but the index is dominated by a single company (Bharti is already 5.1% of the Nifty 50). Verdict: fair, improving; limited ability to judge valuation.

### 5.16 Consumer durables: fair (cheap vs own history, 57x in absolute terms)

- P/E 57.2 (17th pct of 90 observations since 2020), P/B 9.17 (8th pct). Implied EPS +13.3%. But cumulative price increases of 16-18% since January and a further 5-8% (Voltas, LG, Daikin) from 1 October are meant to pass on copper (+34%), steel (+24%), aluminium (+16%) and resin (+17%) cost increases, and analysts flagged festive-demand risk. Voltas Q1 revenue +18.7%, RAC volumes +45%. Budget 2026 raised the EMS scheme outlay from Rs 22,000 cr to Rs 40,000 cr. Foreigners bought about $413 m in August. Verdict: fair; the margin and demand test comes in the festive quarter.

### 5.17 Chemicals: not enough history to rate

- NSE history starts 28 Mar 2025 (P/E 41.7, P/B 3.66 against an average of 4.22). ICRA (31 Aug) described healthy domestic volumes but Chinese overcapacity limiting pricing and rising raw-material costs squeezing margins; crude-linked inputs are about a third of costs (CRISIL). No company-level Q1 numbers found. Verdict: not rated.

## 6. Crowding summary

| Sector | Recent price action | Foreign flows (Aug 2026, NSDL via Finnovate / PL) | Read |
|---|---|---|---|
| Pharma / Healthcare | +14.6% YTD | +$628 m | Crowded safe haven |
| Defence | +17.2% YTD | n/a | Crowded |
| Metals | +7.8% YTD | +$189 m; YTD key beneficiary | Crowded among foreigners |
| Capital goods | median stock +6% 12m | -Rs 15.6 bn per PL; +$63 m per Finnovate; YTD beneficiary | Moderately crowded |
| Smallcaps | Smallcap 250 +6.0% YTD, richest vs Nifty 500 in its history | AMFI Aug: small-cap funds Rs 7,973 cr, the largest equity category inflow; mid-cap Rs 6,989 cr; large-cap -Rs 1,147 cr | Domestic money chasing smaller companies |
| Private banks / Financials | -5.5% / -8.0% YTD | +$1.11 bn (YTD persistent selling) | Uncrowded |
| Autos | -12.1% YTD | +$329 m | Uncrowded, turning |
| IT | -27.0% YTD | +$434 m | Uncrowded, turning |
| FMCG | -20.2% YTD | -$203 m | Uncrowded |
| Power | 18% of stocks above 200-day | -$164 m | Uncrowded |
| Telecom | near highs | -$527 m | Foreigners selling |
| Realty | +2% since 27 Feb | -$63 m | Neutral |

Fund-flow facts I could source: AMFI August 2026 equity inflows of about Rs 29,329 cr; SIP inflows record Rs 32,297 cr; sectoral funds -Rs 53 cr and thematic funds +Rs 1,766 cr. I could not find September 2026 AMFI or NSDL sector data (not yet published or not indexed).

## 7. Cycle position at a glance

| Sector | Cycle position |
|---|---|
| Banks | Credit-quality peak, margin trough, policy now tightening |
| NBFCs | Growth strong, funding-cost upcycle starting |
| IT | Demand soft, guidance being cut, structural AI question |
| Autos | Volume upcycle (flattered by a low Sept 2025 base), margin trough |
| FMCG | Valuation trough, volume recovery early, input costs rising |
| Pharma | Domestic upcycle, US generics downcycle, tariff cliff 2028 |
| Metals | Late-ish price-led upcycle, near peak earnings |
| Oil and gas | OMC earnings trough, upstream earnings elevated; depends on crude |
| Power and grid | Early-to-mid capex and demand upcycle |
| Capital goods | Mid upcycle in orders; margins lagging |
| Realty | Post-peak volumes, rates now rising |
| Defence | Long order cycle, inflow lumpy |
| Telecom | Early tariff upcycle |
| Cement | Demand mid-cycle, margin trough in Q2 FY27 |

## 8. Policy and macro drivers (sourced)

- RBI: repo rate raised 25 bp to 5.50% on 7 Oct 2026, unanimous, stance "calibrated tightening", cuts "off the table" near term; FY27 GDP 7.1%, CPI 5.2% (ETV Bharat; Business Standard headline; Upstox live blog). First hike since February 2023. Goldman Sachs and Nomura expected a second hike in December (pre-decision forecasts).
- Union Budget 2026-27 (1 Feb 2026): central capex about Rs 12.2 lakh cr (+11.5%); defence capex +17%; railways +10%; F&O securities transaction tax raised (options sale 0.10% to 0.15%, futures 0.02% to 0.05%); EMS scheme Rs 22,000 cr to Rs 40,000 cr; battery-mineral duty cuts; data-centre tax exemption for foreign cloud customers; fiscal deficit target 4.3% of GDP (Prime Investor, IANS, Outlook Business). Budget analysts called it "no fireworks" for equities.
- PLI: recalibrated, with increases for autos/EVs, ACC batteries, IT hardware, white goods, APIs, medical devices and specialty steel (Prime Investor).
- War and oil: Feb 28 US-Israel strikes on Iran, Hormuz shipping collapse, ceasefire 8 Apr, truce broke 8 Jul (goodreturns; single article). Market data I pulled from Yahoo corroborate the shock: Brent $60.85 (31 Dec) to $118.35 (31 Mar) to $103.2 (9 Oct), India VIX 27.9 on 30 Mar vs 14.8 now, US 10-year yield 5.23% vs 4.16% at end-2025, USD/INR 96.6 vs 89.8.
- Q1 FY27 earnings (NSE review, primary): Nifty 50 PAT +11.8%, Nifty 500 +11.1%; revenue +18.4% / +18.9%; Nifty 500 operating margin down 244 bp to 16.8%; Energy EBITDA -37.4%; Nifty 500 smallcap PAT +33.9%. Estimates: FY27 -4.1% since March; growth now 9.2% (FY27) and 17.2% (FY28); the revision indicator is near zero (no upgrade cycle yet). Broker figures differ (Motilal Nifty EPS Rs 1,232 FY27 and Rs 1,425 FY28; BofA FY27 growth 10%).
- Index targets cited: Nomura 25,900 by Mar 2027; Citi 26,000; BofA base 26,200 by Dec 2026 and bear case 22,000 (the Nifty is at 22,232).

## 9. What I could not verify (not filled from memory)

- Valuation history for Capital Goods, Power, Telecom, Construction, Hospitals, Insurance, NBFC, Cement and Chemicals: the niftyindices.com historical P/E API returned an HTML page instead of data and the NSE archive files list those indices only from 2025-2026. Their "fair/cheap" labels therefore rely on peers, not on their own past.
- Sector-level consensus earnings estimates (only the aggregate NSE figure was available), a current Nifty forward P/E (the last sourced multiples were from Dec 2025-Jan 2026), India 10-year bond yield (so no equity risk premium comparison).
- The primary RBI statement and the primary Budget documents: I used news and research-site summaries. The Business Standard RBI page returned 403; the PRS India expenditure PDF appeared in search but I did not open it. The Prime Investor Budget page printed two different defence capex figures (Rs 2.19 and 2.31 lakh crore).
- Market reaction to the 7 Oct hike (no article found) and whether banks' margins benefit or lose from this specific hike.
- Sept 2026 AMFI and NSDL sector flows (not published or not indexed). The "FPI outflows Jan-Sep Rs 3.05 lakh crore" figure came from an aggregator citing social-media posts and I did not use it; the Finnovate figure ($24.6 bn through August) and The Wire headline (Rs 2.6 lakh cr in 2026, no body text retrieved) are consistent in order of magnitude but not identical.
- Company results: HAL Q1, M&M, Hero, ITC, ONGC, Reliance, Siemens India, Havells and Dixon numbers were not found. No management call transcripts were read, so "management commentary" is limited to what the cited articles quote. Company figures come from aggregator and broker pages (Sahi, Swastika, Finology, DSIJ, Kotak Neo, etc.) and different outlets gave different numbers for the same item (Infosys guidance, IOC loss, Hindalco and Dr Reddy's profit, Maruti profit); where they conflicted I stated a range or flagged it.
- The Tata Motors split and other index changes may distort implied EPS and ROE for Auto and other indices; I did not adjust for them.
- The Iran-war timeline rests on one article (goodreturns) plus corroborating price moves; I did not find a second written source.
- Breadth numbers rely on Yahoo prices for 490 stocks over about 14 months (BAGMANE had no data; a few listings are recent), and they exclude NSE's own breadth statistics.

## 10. Sources

NSE and Nifty Indices (primary):
- Daily index files (P/E, P/B, dividend yield, close): https://archives.nseindia.com/content/indices/ind_close_all_08102026.csv and the same pattern for other dates (133 files)
- Factsheets dated 30 Sep 2026: https://www.niftyindices.com/Factsheet/ind_Nifty_IT.pdf, ind_nifty_bank.pdf, ind_Nifty_Auto.pdf, ind_Nifty_FMCG.pdf, ind_Nifty_Pharma.pdf, ind_Nifty_Metal.pdf, ind_Nifty_Energy.pdf, ind_Nifty_Realty.pdf, ind_Nifty_PSU_Bank.pdf, ind_Nifty_Private_Bank.pdf, ind_Nifty_Financial_Services.pdf, ind_Nifty_Infra.pdf, ind_nifty50.pdf, ind_niftymidcap100.pdf, ind_Nifty_Smallcap_250.pdf
- NSE Q1 FY27 Corporate Earnings Review (Sept 2026): https://nsearchives.nseindia.com/web/mediaattachment/2026-09/Q1FY27_Corporate_Earnings_Review_v1.0_20260911_20260916121318.pdf
- Market prices (Brent, USD/INR, US 10-year, India VIX, sector stocks): Yahoo Finance via yfinance, pulled 9 Oct 2026

Macro, policy and flows:
- Nifty and Sensex in 2026: https://www.goodreturns.in/common/static_html/nifty-and-sensex-in-2026--down-about-15--1790886452.html
- RBI 7 Oct 2026: https://www.etvbharat.com/en/business/rbi-mpc-meeting-october-2026-sanjay-malhotra-25-basis-points-repo-rate-hike-inflation-india-gdp-enn26100701116 ; https://upstox.com/news/market-news/economy/rbi-mpc-meeting-october-7-2026-live-updates-governor-sanjay-malhotra-speech-repo-rate-hike-key-highlights/liveblog-201398/ ; https://www.business-standard.com/finance/news/rbi-mpc-october-2026-repo-rate-hike-inflation-growth-gdp-sanjay-malhotra-126100700222_1.html (search summary only)
- Budget 2026-27: https://primeinvestor.in/reports/union-budget-2026/ ; https://ianslive.in/pragmatic-budget-with-capex-focus-zero-fireworks-report--20260202130717 ; https://www.outlookbusiness.com/budget/budget-2026-fm-sitharaman-raises-capex-for-fy27-to-122-lakh-crore ; https://prsindia.org/files/budget/budget_parliament/2026/Analysis_of_Expenditure_2026-27.pdf (not opened)
- FPI flows: https://www.finnovate.in/learn/blog/fpi-inflows-august-2026-sectoral-flows ; https://www.plindia.com/pl-research/quant-the-outlanders-monthly-sector-wise-fpi-fii-flows-aug26/
- AMFI August 2026: https://www.bajajbroking.in/share-market-news/amfi-august-2026-equity-mutual-funds-inflows-up-19-percent-mom
- Earnings estimates and targets: https://www.outlookbusiness.com/markets/bofa-raises-fy27-earnings-estimates-turns-positive-on-autos-cement-and-power ; https://www.businesstoday.in/markets/stocks/story/nifty-at-25900-by-march-2027-nomura-keeps-index-target-shares-key-themes-to-watch-549936-2026-08-19 ; https://businesstoday.in/markets/stocks/story/citi-cuts-nifty-target-to-26000-from-27000-earlier-heres-why-536236-2026-06-11

Sector and company reporting (secondary):
- IT: https://ticker.finology.in/discover/market-update/infosys-q1-fy27-results-analysis ; https://www.bajajbroking.in/share-market-news/infosys-q1-results-peer-comparison-and-it-sector-review ; https://www.outlookmoney.com/invest/nifty-it-stocks-has-lost-10-percent-in-a-week-what-the-market-is-worried-about
- Banks and NBFCs: https://arihantresearch.arihantcapital.com/Mumbai_Research/Axis%20Bank_Q1FY27_Result%20Update.pdf ; https://www.swastika.co.in/blog/icici-bank-share-price-momentum-a-deep-dive-into-q1-fy27-results ; https://www.swastika.co.in/blog/punjab-national-bank-results-q1-fy27-profit-surge-nii-growth-and-asset-quality-t ; https://barodaetrade.com/Reports/Banking-Q1FY27Preview9Jul26-Research.pdf ; https://www.multibagg.ai/market-pulse/articles/shriram-finance-q1fy27-results-cmsj5j16l06jn0zqzqi9fy5if
- Autos: https://www.autopunditz.com/post/india-car-sales-september-2026-oem-wise-dispatches ; https://www.businesstoday.in/markets/stocks/story/maruti-suzuki-q1-results-profit-slips-9-yoy-to-rs-3447-crore-revenue-climbs-36-546565-2026-07-31 ; https://www.sahi.com/blogs/bajaj-auto-vs-tvs-motor-q1-fy27-comparison
- FMCG: https://www.republicworld.com/business/hul-hindustan-unilever-q1-fy27-results-net-profit-revenue-sales-growth-2026-07-28-133609 ; https://www.indmoney.com/blog/stocks/fmcg-results-q1-fy27-growth-vs-margins-analysis
- Pharma: https://www.angelone.in/news/stocks/sun-pharma-q1-fy27-results-net-profit-rises-27-us-formulation-sales-weigh-on-revenue ; https://www.sahi.com/blogs/dr-reddys-q1-fy27-results ; https://www.latestly.com/agency-news/business-news-india-pharma-market-enters-us-tariff-transition-with-strong-domestic-growth-report-7528287.html
- Metals: https://www.kotakneo.com/news/stocks/jsw-q1fy27-results-profit-jumps-beats-estimates/ ; https://www.multibagg.ai/market-pulse/articles/hindalco-q1-fy27-record-profit-cmsisq6s100p70zlmilatkd9c ; https://www.barodaetrade.com/Reports/MetalsMining-Q1FY27Preview3Jul26-Research.pdf
- Oil and gas: https://www.zeebiz.com/economy-infra/news-fuel-under-recoveries-at-rs-218-lakh-crore-omcs-lost-rs-74781-crore-in-q1-hardeep-singh-puri-398305 ; https://www.plindia.com/news/omc-stocks-in-focus-crude-prices-lpg-costs-and-q1fy27-trends-pl-capital/ ; https://ticker.finology.in/discover/market-update/bpcl-q1-fy27-results
- Power: https://solarquarter.com/2026/07/30/ntpc-reports-13-rise-in-consolidated-q1-fy27-profit-on-operational-gains/amp/ ; https://www.plindia.com/pl-research/power-grid-corporation-of-india-pwgr-in-q1fy27-result-update-healthy-capex-and-order-win-buy/ ; https://www.tribuneindia.com/news/business/indias-power-demand-to-grow-up-to-5-yoy-in-fy27-on-sustained-economic-momentum-fitch-ratings/
- Capital goods and defence: https://www.kotakneo.com/news/stocks/lt-q1-fy27-results-pat-rises-14-order-inflow-rs-1-08-lakh-crore/ ; https://indianpsu.com/bhel-q1-fy27-results-profit-rs377-crore-revenue-up-40-percent/ ; https://www.angelone.in/news/stocks/abb-india-q2-cy2026-results-orders-jump-50-percent-revenue-rises-21-percent-and-announces-rs-90-special-dividend ; https://www.sahi.com/news/bel-projects-55-000-crore-order-inflow-with-ebitda-margins-surpassing-28-in-fy27-928-PE1_CORP ; https://mailcontent.icicidirect.com/mailcontent/idirect_mazagondock_q1fy27.pdf ; https://www.kalkine.co.in/article/general/hindustan-aeronautics-rides-record-rs-254-lakh-crore-order-book-into-fy27
- Realty: https://www.businesstoday.in/real-estate/story/housing-sales-in-indias-top-9-cities-rise-19-in-q2-2026-supply-jumps-43-reports-539248-2026-06-26 ; https://therealtytoday.com/news/market-insights/housing-sales-drop-6-in-q2-2026-amid-west-asia-conflict-new-launches-rise-7-says-anarock ; https://www.freepressjournal.in/business/realty-firms-sales-bookings-fall-21-to-40000-crore-godrej-properties-tops-june-quarter-chart
- Telecom: https://india.entrepreneur.com/business-news/jio-and-airtel-kick-off-fy27-with-robust-q1-gains ; https://telecomtalk.info/?p=1002675
- Consumer durables, cement, chemicals: https://arihantresearch.arihantcapital.com/Mumbai_Research/Voltas_Q1FY27_Result_update.pdf ; https://www.sahi.com/news/voltas-and-appliance-makers-set-to-hike-prices-by-5-8-from-october-1 ; https://www.indmoney.com/blog/stocks/ultratech-cement-q1-results-management-guidance ; https://www.devdiscourse.com/article/business/3949568-chinas-restraint-boosts-indian-specialty-chemical-sector-amid-pricing-fluctuations
