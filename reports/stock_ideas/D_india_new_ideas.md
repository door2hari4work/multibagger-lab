# D. India: new stock ideas for a 1-2 year horizon (as of 2026-10-14)

Research, not advice. Nothing was executed. The investor decides. No personal portfolio numbers are in this file; fit with existing holdings is left to the private overlay.
Tags: FACT (primary source or dated data), INFERENCE (my reasoning), SPECULATION. Probabilities are labelled model estimates. "Unverified" means I could not confirm it.

## 0. Bottom line
Six ideas, none of them a multibagger candidate (model estimate P(5x in 24m) below 1% for each; the lab found 5x outcomes rare in large and mid caps). They are "reasonable business at a reasonable price" ideas, entered in stages because the India regime filter is OFF (Nifty 500 22,090 vs its 200d MA 22,901 on 2026-10-13, 3.5% below).

| Tier | Name | Why in one line | Cap (% of net worth) | Status |
|---|---|---|---|---|
| 1 core | Bajaj Auto (BAJAJ-AUTO) | Best momentum rank of the finalists (84th pct), strong standalone cash conversion, export growth plus weak rupee tailwind | 2.5% | Starter allowed now, scale after 27-Oct results |
| 1 core | HCLTech (HCLTECH) | Q2 FY27 net income +21% y/y, bookings +27%, guidance raised, ~20x earnings vs 22x own 5-year median, net cash | 2.0% | Starter allowed now (just above 200d MA) |
| 2 staged | Hero MotoCorp (HEROMOTOCO) | ~18x clean earnings, 3.7% yield, cash conversion above 100%; but margin squeeze and tougher comps | 1.5% | Wait for 28-Oct results |
| 2 staged | State Bank of India (SBIN) | ~10x earnings, ~1.4x book, loans +18.6%; but earnings growth is only +10% and funding gap is widening | 1.5% | Wait for Q2 print, below 200d MA |
| 3 watch | Sun Pharma (SUNPHARMA) | Quality franchise, but a US$11.75bn debt-funded Organon deal changes the balance sheet | 1.5% if triggers met | No position yet |
| 3 watch | HAL (HAL) | Huge order book but ~35x earnings for ~12% guided growth; 31% of pre-tax profit is other income | 1.5% if triggers met | No position yet |

Researched but not selected: M&M (core auto margin falling), TCS (cheapest in 5 years but weakest momentum; interchangeable with HCLTech, see 4.7). Sleeve cap if everything triggers: 8% of net worth (INFERENCE, see section 5). Two of the picks are two-wheeler makers, so treat them as one cluster capped at 3.5%.

## 1. Market backdrop (FACT unless stated; sources in section 9)
- Indices on 2026-10-13: Nifty 50 22,722 (13.7% below 52-week high), Nifty 500 22,090, Midcap 150 21,829 (7.3% below high), Nifty IT 29,830 (24.5% below high). India VIX 14.6.
- USDINR 95.0 on 2026-10-14 (88.7 a year earlier, 7% weaker). Brent $106 (63 a year earlier; 52-week high 118). US 10-year yield 5.22%. S&P 500 at a record 7,805.
- RBI raised the repo rate 25 bp to 5.50% on 2026-10-07, stance "calibrated tightening" (several secondary sources; the RBI document itself was not opened). FPIs sold about Rs 45,500 cr in September and Rs 26,000 cr in 1-7 October (secondary source, unverified).
- INFERENCE: oil and rupee shocks hurt domestic cost-sensitive names (autos, consumer, NBFCs) and help dollar earners (IT, pharma exporters, export-heavy two-wheelers). This drove the picks. If crude and the rupee reverse, the same tailwind reverses.

## 2. How the shortlist was built
1. Ran `research/screen_IN_ideas.py` (Nifty 500, Yahoo data to 2026-10-12, fundamentals refreshed 2026-10-13/14 after a rate-limited first download). 499 names scored; 404 eligible after excluding negative earnings, short history, illiquid (<Rs 5 cr/day), metals, realty, and the 15 names already in theses/IN. I switched the screen's "avoid healthcare" sector flag off because the task asked for pharma coverage; treat pharma as a lower-confidence area for that reason.
2. Of the eligible, 356 trade above Rs 15 cr a day and 158 sit above their own 200d MA. Composite = declared, unvalidated weights (price 30%, value 20%, growth 20%, quality 20%, balance sheet 10%). Only the 12-1 momentum rank has lab evidence; everything else is a flag.
3. Already downgraded in theses/IN and excluded: Sterlite Tech, HFCL, TD Power, Kirloskar Oil Engines. No evidence of a material change was found, so they stay out. The other IN theses (MTAR, Laurus, Sansera, etc.) are Level-1 snapshots and were not re-run.
4. Picked 26 across the requested sectors, then ran primary-source checks (NSE filings, shareholding XBRL) on the best eight.

### 2.1 Shortlist of 26 (prices are 2026-10-12 closes from Yahoo; P/E is trailing from Screener; Q = latest quarter y/y; Mom pct = 12-1 momentum percentile among 404 eligible)
| Sector | Name | Mcap Rs 000 cr | P/E (own 5-FY median) | ROE % | Q sales / profit y/y % | Mom pct | vs 200d MA % | vs 52w high % | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| Bank/NBFC | SBIN | 869 | 10.5 (9.3) | 15 | 8 / 14 | 71 | -9 | -22 | Deep dive, Tier 2 |
| | AXISBANK | 390 | 14.2 (13.0) | 13 | 10 / 22 | 58 | -2 | -11 | Pass: ROE 13%, Q2 result due 17-Oct, revisit after |
| | FEDERALBNK | 81 | 17.4 (10.7) | 12 | 10 / 37 | 98 | +8 | -11 | Pass: 63% above own-history multiple |
| | M&MFIN | 45 | 13.5 (15.4) | 12 | 15 / 75 | 82 | -5 | -22 | Pass: rate-hike and funding-cost risk, ROE 12% |
| | CHOLAFIN | 135 | 24.1 (26.5) | 19 | 22 / 46 | 71 | -6 | -19 | Pass: P/B 4.4x with a rate hike under way |
| Capital goods / defence | HAL | 318 | 35.0 (27.0) | 24 | 14 / 15 | 56 | +8 | -7 | Deep dive, Tier 3 |
| | BEL | 273 | 45.2 (38.7) | 27 | 25 / 9 | 50 | -10 | -20 | Pass: 45x earnings, profit +9% |
| | MAZDOCK | 82 | 29.9 (25.6) | 29 | 12 / 22 | 24 | -16 | -29 | Pass: weak trend, 81% government |
| | SIEMENS | 130 | 88.6 (45.7) | 19 | 15 / base effect | 77 | +4 | -11 | Pass: 89x |
| Healthcare | SUNPHARMA | 422 | 33.6 (37.1) | 16 | 10 / 27 | 70 | -2 | -12 | Deep dive, Tier 3 |
| | ZYDUSLIFE | 114 | 23.2 (22.0) | 21 | 22 / -35 | 69 | +12 | -7 | Pass: profit -35%, margin 32% to 24%, FY26 CFO/OP 44% |
| | AJANTPHARM | 42 | 36.6 (33.0) | 27 | 25 / 31 | 89 | +9 | -9 | Pass: small cap (Rs 34 cr/day), 37x |
| | APOLLOHOSP | 112 | 53.8 (70.3) | 21 | 21 / 38 | 74 | -3 | -14 | Pass: 54x |
| Consumer | ASIANPAINT | 223 | 46.7 (54.2) | 22 | 18 / 40 | 60 | -8 | -21 | Pass for now: 47x, revisit below ~Rs 2,000 |
| | TITAN | 390 | 68.3 (74.9) | 38 | 29 / 63 | 88 | 0 | -15 | Pass: 68x |
| | HINDUNILVR | 428 | 40.0 (48.9) | 31 | 10 / -3 | 17 | -16 | -29 | Pass: weakest momentum, flat profit |
| Autos | BAJAJ-AUTO | 280 | 24.0 (25.7) | 29 | 65 (incl. KTM) / 44 | 84 | -1 | -19 | Deep dive, Tier 1 |
| | HEROMOTOCO | 99 | 18.1 (16.8) | 28 | 35 / -17 (one-off base) | 48 | -6 | -20 | Deep dive, Tier 2 |
| | M&M | 338 | 18.6 (20.2) | 20 | 28 / 37 | 37 | -13 | -25 | Deep dive, not selected |
| | EICHERMOT | 195 | 33.8 (28.4) | 24 | 32 / 21 | 66 | -3 | -12 | Pass: 34x, above own history |
| Power | NTPC | 301 | 10.9 (13.7) | 15 | 8 / 13 | 52 | -12 | -24 | Pass: already in the infrastructure fund; regulated returns, little upside beyond yield |
| | POWERGRID | 232 | 14.7 (16.1) | 15 | 3 / -1 | 43 | -12 | -22 | Pass: no growth, same reason |
| IT services | HCLTECH | 331 | 18.9 (22.2) | 24 | 12 / 21 | 38 | -7 | -27 | Deep dive, Tier 1 |
| | TCS | 769 | 15.0 (25.2) | 52 | 11 / 15 | 19 | -13 | -34 | Deep dive, alternate to HCLTech |
| | COFORGE | 62 | 44.6 (40.1) | 21 | 49 / 49 | 69 | +21 | -8 | Pass: 45x, acquisition-driven growth |
| | PERSISTENT | 90 | 47.5 (48.4) | 27 | 29 / 14 | 61 | +8 | -11 | Pass: 48x |
Caveats: "own 5-FY median" is a rough Yahoo-based figure (current share count, dividend-adjusted prices, at most 5 points). Banks' ROCE is not meaningful and is omitted. Survivor bias: universe is today's index members.

## 3. Evidence table for the eight deep dives
Sources: NSE-hosted company filings for results, Screener.in (aggregator, used for ratios only), NSE shareholding XBRL for promoter and pledge. Dates are filing dates.

| | Bajaj Auto | HCLTech | Hero | SBI | Sun Pharma | HAL | M&M | TCS |
|---|---|---|---|---|---|---|---|---|
| Latest quarter | Q1 FY27 (21-Jul) | Q2 FY27 (12-Oct) | Q1 FY27 (6-Aug) | Q1 FY27 (7-Aug) | Q1 FY27 (31-Jul) | Q1 FY27 (12-Aug) | Q1 FY27 (30-Jul) | Q2 FY27 (8-Oct) |
| Revenue y/y | +37% standalone Rs 17,244 cr; +65% consolidated Rs 21,689 cr (KTM now consolidated) | +11.5% INR Rs 35,620 cr; +2.6% constant currency | +36% standalone Rs 12,999 cr; volumes +23% | NII +14.9%; advances +18.6% | Rs 15,300 cr, +10.5% (Screener) | +14.4% Rs 5,515 cr | +28% Rs 58,188 cr | +11.2% INR Rs 73,188 cr; +0.5% q/q constant currency |
| Profit y/y | Standalone PAT Rs 2,983 cr, +42% | Net income Rs 5,132 cr, +21% | Standalone PAT Rs 1,454 cr, +29%; consolidated -17% only because last year had a Rs 722 cr one-off | Rs 21,121 cr, +10.2% (provisions -32%) | Rs 2,901 cr, +27% (Screener) | Rs 1,590 cr, +14.9% | Rs 5,455 cr, +34%; core auto PBIT flat | Rs 13,884 cr (company), margin 24.0% |
| Valuation (trailing P/E) | 27x standalone | ~20x | ~18x | ~10x; ~1.4x book | ~34x | ~35x | 18.6x consol / 21.7x standalone | ~15x |
| Cash conversion | Standalone CFO/OP 99-112% over 5 years; FY26 free cash flow Rs 8,470 cr | LTM free cash flow / net income 87%; FY26 CFO/OP 90% | CFO/OP 85-134%; FY26 free cash flow Rs 7,227 cr | n/a (bank) | FY26 CFO/OP 89% | FY26 CFO/OP 142% but inventory days 859 and working-capital days 301 vs 153 | Standalone CFO/OP 108-123% (consolidated is distorted by the finance arm) | Q2 operating cash flow 102% of net income |
| Balance sheet | Net cash at standalone level (FY26 borrowings small, Screener) | Net cash Rs 24,503 cr (Sep-26), down from Rs 33,288 cr in March after acquisitions and dividends | Almost debt free | CRAR 15.67%, GNPA 1.47%, NNPA 0.38% | Net cash until the Organon deal (see 4.5) | Almost debt free; Rs 3,897 cr other income a year | Standalone almost debt free | Borrowings Rs 11,808 cr vs large investments |
| Promoter / holding (30-Jun-26) | 55.0% | 60.9% | 34.7% | Government 55.5% | 54.5% | Government 71.6% | 18.4% | 71.8% |
| Pledge (NSE XBRL) | Immaterial (13,822 shares, 0.002% of the category) | None | None | None | Immaterial: 85,000 shares plus ~2% of one promoter-group category (my reading of the XBRL; unverified) | None | Immaterial (40,000 shares) | None |
| Liquidity (20d median, Rs cr/day) | 255 | 341 | 206 | 742 | 256 | 258 | 711 | 717 |
Hero, HCLTech and SBI figures are from the company press releases and presentations on NSE; Bajaj Auto from the results filing; HAL from the results filing (consolidated Rs 5,515 cr revenue, Rs 1,590 cr profit).

## 4. The ideas
Common rules (apply to every idea):
- Regime OFF: no more than one third of a position's cap is deployed before one of (a) Nifty 500 closes above its 200d MA (about 22,900), (b) the next results print confirms the thesis. No position reaches full cap while the regime is OFF unless the stock has also reclaimed its own 200d MA.
- Averaging down only while the thesis checks (the kill criteria below) are intact and the loss on average cost is under 15%. At -20% on average cost: review; at -25%: exit unless every thesis check has just been re-verified (investor's stated loss limit is 20-25%).
- Trim when: price is above 1.35x the average cost and the trailing P/E is above the higher of 30x or 1.3x its 5-year median; or the position exceeds 1.5x its cap; or a kill criterion fires. Exits: sell the earliest lots only after 12 months where possible (tax, section 6).
- Odds shown are model estimates blending lab-computed base rates (2007-2026 Yahoo history, survivor-inflated, flagged) with my haircut for the OFF regime. "Dip" = price falling at least 22.5% below the entry price at some point in the next 12 months.

### 4.1 TIER 1: Bajaj Auto (BAJAJ-AUTO), cap 2.5% of net worth
- **Business (FACT):** world's most valuable two- and three-wheeler maker by its own description; Pulsar, Chetak EV, three-wheelers and commercial vehicles; premium KTM/Husqvarna/GASGAS via Bajaj Mobility AG (restructured after Austrian insolvency proceedings; now a subsidiary).
- **Thesis (INFERENCE):** (1) exports reached a record 732,173 units in Q1 FY27 (+54%) and Sep-26 exports were +34%, helped by a rupee 7% weaker than a year ago; (2) KTM turned EBIT-positive in Q2 2026 (EUR +1.3 mn, from -164.7 mn a year earlier, ad hoc release 27-Aug), so the drag on consolidated profit is shrinking; (3) standalone profit is growing 40%+ at a stable 21% EBITDA margin with free cash flow of about 3% of market value.
- **Priced in:** about 27x standalone trailing EPS (Rs 383) at Rs 10,370, versus a Yahoo-based 5-FY median near 25.7x. Not cheap; the case relies on earnings growth, not re-rating.
- **Three strongest bear points:** (1) Domestic is weakening: Sep-26 domestic 2-wheelers -12% y/y and domestic total -9% (company, 1-Oct; part timing of Navratri, INFERENCE) while exports carry the quarter; (2) Consolidated numbers include KTM, whose free cash flow was still EUR -22 mn in H1 2026 on equity of EUR 340 mn (21.5% equity ratio); relapse would hit consolidated profit; (3) export strength leans on the rupee and on a handful of emerging markets (Africa, Latin America, per press); a rupee recovery or a local currency crisis would cut it.
- **Kill criteria:** standalone EBITDA margin below 19% for two quarters (Q1 FY27 20.9%); exports growth below 10% y/y for two consecutive months; KTM EBIT negative again in the Q3 2026 print; domestic 2W down more than 10% y/y for three months after the festive season.
- **Entry plan:** starter 1/3 of cap (0.8% of net worth) in the zone Rs 10,000-10,600 (price is 1% above its 200d MA of Rs 10,242 but below the 50d MA of Rs 11,349). Second third after the 27-Oct Q2 results if standalone margin is at least 20% and exports at least +25%. Final third on regime ON, or a pullback to Rs 9,300-9,800 (24-25.5x) with all kill checks green. Do not chase above Rs 11,500 (30x).
- **Accumulate on:** earnings confirmation or regime flip, not on price alone. Max one add after a fall.
- **Trim/sell:** above Rs 13,500 (about 31x on Rs 430 EPS) trim a third; close below Rs 8,700 (52-week low area) with a kill criterion firing: exit; thesis break: exit.
- **Next catalysts:** Q2 FY27 results 27-Oct-2026 (NSE board-meeting feed); October sales around 1-Nov; Q3 around late January (date not announced).
- **Model odds (12m):** P(+30%) 12%; P(dip of 22.5%+) 20%; base-case total return +8 to +15% (EPS +10-14%, multiple flat, 1.4% dividend). Historical (2007-2026, survivor-inflated): dip 20%, +30% in 12m 26%.
- **Stress:** covid-window fall -35%; at the cap that is -0.9 pp of net worth.

### 4.2 TIER 1: HCLTech (HCLTECH), cap 2.0% of net worth
- **Business (FACT):** IT services (75% of revenue), engineering and R&D (17%), software (8%); 56% of services revenue from the USA.
- **Thesis:** Q2 FY27 (12-Oct): revenue Rs 35,620 cr (+11.5% y/y; +2.2% in dollars; +2.6% constant currency), EBIT margin 18.2% including 84 bp restructuring cost (+131 bp q/q), net income Rs 5,132 cr (+21%, a record), bookings US$3.26 bn (+27%), advanced AI revenue US$219 mn (+78% constant currency), FY27 constant-currency guidance raised to 2.5-4.0% (from 1-4% after Q1; secondary report for the earlier range). LTM free cash flow / net income 87%, ROIC 41%. INFERENCE: at a 95 rupee the earnings are being lifted by currency; the dollar growth is only about 2%.
- **Priced in:** trailing P/E about 20x vs 22x 5-FY median (low 17x, high 24x); free cash flow yield about 5%; dividend yield about 4% (Rs 12 interim declared; Screener); net cash about 7% of market value. The stock is 22% below its 52-week high; Nifty IT is 24.5% below its.
- **Three strongest bear points:** (1) Dollar growth of 2% means the +21% profit leans on the weak rupee (7% depreciation) and margin recovery; a rupee reversal to 88-89 would remove a large part of it (INFERENCE); (2) restructuring charges have appeared in five consecutive quarters (55, 81, 122, 62, 84 bp), so "one-off" costs are recurring; (3) AI could deflate services revenue pools: the sector derated 24% even as company AI revenue grows. Momentum is also poor (38th percentile), and the lab found momentum rank the only selector with edge.
- **Kill criteria:** constant-currency growth negative q/q for two quarters; EBIT margin (excluding restructuring) below 17%; bookings below US$2.0 bn for two quarters (Q2 3.26 bn; Q1 record 2.4 bn per secondary report); net cash falling below Rs 15,000 cr without a large announced deal.
- **Entry plan:** starter 1/3 of cap (0.7% of net worth) between Rs 1,250 and Rs 1,360 (the 200d MA is Rs 1,338; the price is just above it). Second third on the earlier of: Q3 FY27 results (January 2027, date unannounced) with guidance held or raised, or regime ON. Final third at Rs 1,150-1,250 (17-18.5x) only if the kill checks are green. Avoid above Rs 1,500 (22x).
- **Trim/sell:** a close above Rs 1,800 (about 25x on Rs 72 EPS) trims a third; below Rs 1,000 with a kill criterion: exit.
- **Catalysts:** US tariff and AI-policy news; rupee and US 10-year yield; Q3 results in January; ex-dividend 16-Oct record date.
- **Model odds (12m):** P(+30%) 10%; P(dip of 22.5%+) 25%; base case +8 to +14% including the dividend. Historical: dip 25%, +30% in 12m 39% (2007-2026 secular rise, discount heavily).
- **Stress:** covid window -32%, 2022 -24%; at the cap -0.6 pp of net worth.
- **Portfolio-fit note (INFERENCE):** the investor already has large AI-capex exposure in US names; Indian IT services is hurt, not helped, by AI disruption, so it may partly offset that theme. Not verified with correlation data.

### 4.3 TIER 2: Hero MotoCorp (HEROMOTOCO), cap 1.5%
- **Business:** world's largest two-wheeler maker by volume; commuter bikes, scooters, VIDA EVs, Harley-Davidson distribution, parts.
- **Thesis:** Q1 FY27 standalone volume 16.77 lakh (+23%), revenue +36%, PAT Rs 1,454 cr (+29%); VIDA +151%, global +63% (all company, 6-Aug). Sep-26 dispatches 766,348 (+12%) with company-reported VAHAN retail +31% ahead of the festive season. Consolidated profit -17% is a base effect: last year included a Rs 722 cr one-time associate dilution gain; excluding it, Q1 consolidated profit rose about 44% (INFERENCE from company figures). Trailing consolidated profit Rs 5,488 cr gives about 18x, a 3.7% yield and FY26 free cash flow of Rs 7,227 cr (about 7% of market value).
- **Priced in:** P/E 18x vs 16.8x median: roughly fair, so the case is cash returns plus modest growth.
- **Bear points:** (1) EBITDA margin fell to 13.3% from 14.4% on commodity costs, below management's 14-16% target; (2) comps harden: the GST cut took effect on 2025-09-22, so Q3-Q4 FY27 compare against a boosted base (INFERENCE; GST date from a secondary article); (3) history of share loss in motorcycles and EV losses at VIDA; momentum percentile only 48.
- **Kill criteria:** standalone EBITDA margin below 12.5% for two quarters; domestic retail growth negative y/y for two straight months after the festive season; VAHAN market share (company-reported) down more than 1 pp y/y.
- **Entry plan:** nothing before the 28-Oct results. Then starter 1/2 of cap (0.75%) at Rs 4,800-5,200 if margin is at least 13.3% and retail growth holds. Second half on regime ON or reclaim of the 200d MA (Rs 5,311), or at Rs 4,500-4,700 (16.5-17x) with checks green.
- **Trim/sell:** above Rs 6,500 (24x) trim half; thesis break exit.
- **Catalysts:** Q2 results 28-Oct-2026 (NSE feed); Oct and Nov sales prints; festive retail data.
- **Model odds:** P(+30%) 10%; P(dip 22.5%+) 25%; base +6 to +13% including 3.7% yield.
- **Stress:** covid window -28%; at the cap -0.4 pp.

### 4.4 TIER 2: State Bank of India (SBIN), cap 1.5%
- **Thesis:** Q1 FY27 net profit Rs 21,121 cr (+10.2%), advances +18.6% (agri +25%, SME +22%), whole-bank NIM 2.86% (+5 bp q/q), GNPA 1.47%, NNPA 0.38%, credit cost 0.27%, CRAR 15.67%, ROE 17.9% (8-Aug press release). The October rate hike may help asset yields faster than deposit costs for a bank with a large repo-linked book (INFERENCE). A fund-raise of up to Rs 60,000 cr was approved on 18-Jun but only via debt instruments, so no equity dilution (board outcome). SBI Funds Management listed on 21-Jul.
- **Priced in:** about 10.5x consolidated earnings, 1.4x consolidated book, 1.8% yield; roughly in line with own 5-FY median.
- **Bear points:** (1) deposits grew only 9.7% against loans at 18.6%, a funding gap that can raise costs; (2) profit growth of 10% is helped by provisions down 32% y/y and credit cost has limited room to fall further (INFERENCE); (3) rate hikes cause treasury mark-to-market losses on the bond book and the stock is a government-linked, FPI-sensitive large bank, with the highest historical dip frequency of the finalists (32% of 12m windows breached 22.5%). Banking weight in index funds is high already, so this adds to a crowded exposure (overlap unverified).
- **Kill criteria:** GNPA above 2.0%; credit cost above 0.6%; domestic NIM below 2.8% (Q1 3.00%); ROA below 0.9% (Q1 1.11%).
- **Entry plan:** no purchase before the Q2 print (date not yet announced in the NSE feed). Then 1/3 of cap (0.5%) if kill checks pass and the price is Rs 900-1,000; next third on regime ON or a close above the 200d MA (about Rs 1,040); the last third below Rs 880 (8x/1.2x book) with checks green.
- **Trim/sell:** above Rs 1,250 (about 13x); thesis break exit.
- **Model odds:** P(+30%) 12%; P(dip 22.5%+) 32%; base +6 to +12%.
- **Stress:** covid window -43%; at the cap -0.65 pp.

### 4.5 TIER 3 watch: Sun Pharma (SUNPHARMA), up to 1.5% only if triggers are met
- **What changed (FACT):** Sun agreed in April 2026 to buy Organon & Co for US$14 a share in cash, enterprise value US$11.75 bn; Organon shareholders approved it in July; closing is subject to regulatory approvals and is hoped for early 2027 (secondary reports of company statements). On 12-Oct the board approved listed NCDs of up to Rs 10,000 cr (NSE filing), and an independent director resigned the same day citing personal reasons (the filing; a director resignation on its own is not a thesis break). The funding mix and pro-forma leverage are not in the documents I read: unverified.
- **Underlying business:** Q1 FY27 revenue Rs 15,300 cr (+10.5%), profit +27%, EBITDA margin 29%, free cash flow about 2% of market value (Screener), 34x trailing earnings.
- **Bear points:** a first leveraged mega-deal for a historically net-cash company; US generic/women's-health pricing risk in the target (unverified); 34x for 10% sales growth.
- **Triggers to start (all must hold):** (1) regulatory clearances received or a disclosed financing structure with pro-forma net debt/EBITDA of 2.5x or less (my threshold, INFERENCE); (2) price at or below Rs 1,560 (about 31x trailing EPS, near the 52-week low of Rs 1,589) OR a close above the 200d MA (Rs 1,808) with the 50d MA rising.
- **Kill:** Organon deal terms re-cut or leverage above 3.5x; US specialty sales (Ilumya, Leqselvi) growth below 10% y/y (unverified baseline).
- **Odds:** P(+30% in 12m) 8%; P(dip 22.5%+) 21%. **Catalysts:** Q2 results (date unannounced); regulatory decisions; NCD pricing.

### 4.6 TIER 3 watch: HAL (HAL), up to 1.5% only if triggers are met
- **Facts:** Q1 FY27 revenue Rs 5,515 cr (+14.4%), profit Rs 1,590 cr (+14.9%) (results filing); other income Rs 3,897 cr over the trailing year versus pre-tax profit of Rs 12,432 cr (31%) (Screener); working-capital days 301 vs 153; promoter (Government) 71.64%, no pledge; trailing P/E 35x vs 27x 5-FY median. Order book about Rs 2.54 lakh cr and FY27 guidance of 10-12% revenue growth and 30-31% EBITDA margin come only from secondary reports (unverified). Tejas Mk1A delivery depends on GE F404 engine supply; reports conflict on rates (unverified). Signed 26-Aug: Aravalli helicopter engine contract with Safran; Ravi K appointed CMD (AGM material-event filing, 31-Aug).
- **Bear points:** 35x earnings for about 12% growth; engine and software delays push revenue to later years; a government customer and government seller (OFS risk).
- **Triggers:** price at or below Rs 4,200 (about 30x trailing EPS Rs 139); or evidence of at least four Tejas Mk1A deliveries plus new order inflows with the price at or below Rs 4,600. **Kill:** engine supply slips beyond FY28; margin guidance cut below 28%.
- **Odds:** P(+30% in 12m) 8%; P(dip 22.5%+) 30%. **Catalysts:** Q2 results (date unannounced); GE delivery news; defence procurement approvals.

### 4.7 Researched, not selected
- **M&M:** consolidated profit +34% to Rs 5,455 cr, but the profit growth came from Mahindra Finance (+78%) and Tech Mahindra (+28%). Core auto PBIT was flat at Rs 2,212 cr with margin 8.3% excluding eSUV contract manufacturing (down 170 bp); standalone EBITDA margin fell to 12% from 14%; management cited "significant commodity inflation" (30-Jul press release). Price is 13% below its 200d MA. Re-open if standalone EBITDA margin holds above 13% at the 5-Nov results. It also sold 51% of Novavayu Aerospace to Embraer on 9-Oct (NSE).
- **TCS:** Q2 FY27 revenue Rs 73,188 cr (+1.3% q/q, +0.5% constant currency), operating margin 24.0%, net profit Rs 13,884 cr, operating cash flow 102% of net income, annualised AI revenue US$3.1 bn, deal value US$9.6 bn (8-Oct release). Trades at 15x, below its 5-year low of 17x, with a 2.8% yield, but growth is slowest and momentum percentile is 19. Treat as an alternate to HCLTech; do not hold both at full cap (same drivers).

## 5. Position sizing and worst-case arithmetic (% of net worth; new-money amount unknown)
Loss in pp of net worth = position weight x drawdown. Drawdowns come from each stock's own history (adjusted closes from Yahoo, 2007 start; the 2008 figures for Bajaj Auto look distorted by restructuring and are not used).
| Name | Cap | Covid window (Feb-Mar 2020) | 2021-11 to 2022-12 | Loss at cap in covid-type fall | At -45% |
|---|---|---|---|---|---|
| Bajaj Auto | 2.5% | -34.6% | -16.7% | -0.87 pp | -1.13 pp |
| HCLTech | 2.0% | -31.7% | -23.9% | -0.63 pp | -0.90 pp |
| Hero | 1.5% | -28.2% | -16.2% | -0.42 pp | -0.68 pp |
| SBI | 1.5% | -43.3% | -14.6% | -0.65 pp | -0.68 pp |
| Tier 1+2 total | 7.5% | | | -2.6 pp | -3.4 pp |
| Sun / HAL if triggered | +1.5% each | -19.6% / -28.5% | -9.2% / -8.0% | -0.3 / -0.4 pp | |
- Sleeve cap 8% of net worth in total (INFERENCE): even a covid-type fall costs about 2.6-3 pp, and these stocks are correlated with the investor's existing India fund exposure (beta near 1 to the Nifty), so the loss adds to, not diversifies, any India fund drawdown.
- Tiers if new money is small: do Tier 1 first (Bajaj, then HCLTech), Tier 2 only after the 28-Oct/Q2 prints; Tier 3 stays empty until triggers fire.
- Historical share of 12-month windows with a 22.5%+ dip from entry (2007-2026, survivor-inflated): Nifty 12%, Midcap 150 15%, Bajaj 20%, Sun 21%, HCL 25%, Hero 24%, SBI 32%, HAL 35% (2018+). Single stocks breach the investor's stated loss limit about twice as often as the index; staged entry and the -20% review rule are the mitigation.
- Funding option (INFERENCE): money for this sleeve could come from consolidating overlapping index funds rather than adding India risk; check fund exit loads and tax first.

## 6. Liquidity, tax, compliance
- **Liquidity (FACT, Yahoo 20-day median value):** all eight finalists trade Rs 200-740 cr a day; a retail-sized order is negligible against that. Use limit orders in the first and last 15 minutes' noise; avoid results-day open.
- **Tax (verified in secondary sources, not the Act; verify with a CA):** listed equity held under 12 months: STCG 20%. Over 12 months: LTCG 12.5% on gains above Rs 1.25 lakh per financial year (shared with equity mutual fund gains), no indexation; sources agree the Budget 2026-27 left these unchanged. Plus surcharge and 4% cess as applicable. Dividends are taxed at slab rate with TDS (rate and threshold unverified). Securities transaction tax applies on delivery trades. Each tranche has its own holding period; sell the oldest lot first. STCG loss offsets STCG and LTCG; LTCG loss offsets LTCG only; carry-forward of 8 years (verify).
- **Employer rules (UNKNOWN):** check with HR/compliance whether personal trades in Indian listed stocks need pre-clearance, a holding period, or restricted-list screening (an IT services name could be a client or vendor of an employer). Do this before the first trade.

## 7. Catalyst calendar (dates from the NSE board-meeting feed on 2026-10-14 unless stated)
| Date | Event |
|---|---|
| 16-Oct | HCLTech dividend record date (company) |
| 17-Oct | Axis Bank Q2 results: read-across for banks |
| 27-Oct | Bajaj Auto Q2 |
| 28-Oct | Hero Q2 |
| ~1-Nov | October auto sales (Bajaj, Hero, M&M) |
| 5-Nov | M&M Q2 |
| Not announced | SBI, Sun Pharma, HAL Q2 (Q1 dates were 7-Aug, 31-Jul, 12-Aug) |
| Not verified | Next RBI MPC meeting; Organon closing; HCLTech Q3 (January) |

## 8. What I could not verify, and lab caveats
- Consensus estimates, management transcripts and Q2 guidance calls were not obtained (IR sites blocked or not searched); management remarks beyond press releases are therefore INFERENCE. HAL order book and guidance, HCLTech's earlier guidance range, rupee and FPI numbers and the RBI decision are from secondary sources.
- Screener ratios are an aggregator and were used to locate numbers, not as sole evidence; Yahoo "own history" valuation is rough (n at most 5).
- Fund look-through overlap with the investor's index funds is unverified (no holdings data fetched). Zerodha and INDmoney tools were not used.
- The lab's only validated selector is the momentum rank. Three of six picks (HCLTech, Hero, SBI) rank mid or low on it, so their case rests on valuation and earnings evidence that the lab has not validated. Trend filters protect but do not find winners; the regime filter is OFF, so every entry above is staged; quality gate had no demonstrated value.
- Probabilities are model estimates, not forecasts. Backtest-style base rates are survivor-inflated.

## 9. Sources (retrieved 2026-10-13/14)
- NSE announcements (nsearchives.nseindia.com/corporate/): HCLTech `HCLTECH_12102026170757_InvestorRelease_5.pdf`; TCS `TCS_CORPCS_08102026154325_PressReleaseletter.pdf`; Hero `HEROMOTO_06082026225253_OutcomeBM06082026pressrelease.pdf`, `HEROMOTO_07082026083605_Stxintimationpresentation07082026.pdf`, `HEROMOTO_01102026154242_StxintimationPR01102026.pdf`; Bajaj Auto `lkwalimbe_bajajauto_co_in_21072026124211_SE_FR.pdf`, `..._01102026085327_Sales_Report_Sep26.pdf`, `..._27082026121722_SE_BMAG_H1_Results_2026.pdf`; SBI `SBIN_07082026135523_PressRelease.pdf`, `SBIN_18062026132315_BSE_NSE_Outcome_18062026.pdf`; Sun `SUNSEC_12102026195625_BMOutcome12October2026.pdf`, `SUNSEC_31072026142955_BMOutcomewithannexures31072026.pdf`; HAL `HAL_12082026140538_FR_30062026.pdf`, `HAL_26082026111035_Mediarelease_26082026.pdf`; M&M `ferozebaria_30072026130242_IntimationPressRelease30072026.pdf`, `AmitDodani_09102026232007_Novavayu_SE_Intimation_Investment_Agreement_Revised.pdf`. Shareholding patterns and pledge flags: NSE shareholding XBRL (SHP_*.xml) for each name; board meeting dates: NSE board-meetings API.
- Screener.in company pages (ratios, 5-quarter and annual tables, cash flow).
- Yahoo Finance via yfinance (prices, indices, USDINR, Brent, US 10-year, drawdown statistics).
- Secondary news: TCS/HCL/M&M/Hero/Bajaj Q results coverage (businesstoday.in, autocarpro.in, freepressjournal.in, kotakneo.com, sahi.com); RBI decision (motilaloswal.com/learning-centre/2026/10/rbi-raises-rate-by-0-25-percent-what-it-means-for-the-economy, adda247); market move (outlookmoney.com, moneylife.in, dailypioneer.com); Sun-Organon (medicaldialogues.in, outlookbusiness.com, upstox.com); tax (sahi.com, bajajfinserv.in, taxguru.in).
- Repo: research/screen_IN_ideas.py, mblab/discovery.py, research/candidates_IN.csv, theses/IN/*, reports/ENGINE_FINDINGS.md, reports/OPPORTUNITIES_2026-10-05.md, analysis/stock_ideas/out/*.csv.
