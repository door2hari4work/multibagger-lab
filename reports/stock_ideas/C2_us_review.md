# C2. Adversarial review of "C. New US stock ideas" (LLY, CB, MA, CVX, GD, KRYS), as of 2026-10-14

Research, not advice. Nothing is executed. Public repo: no personal portfolio numbers; sizes are % of total net worth.
Reviewer mandate: re-verify, check arithmetic, challenge odds, look for missed bear cases, and decide what survives.
Tags: **FACT** (source named), **INFERENCE**, **SPECULATION**, "unverified" = not confirmed in a primary source this session.
Prices: 2026-10-13 closes via yfinance (unadjusted Close for MAs; consensus EPS from Yahoo's analyst tables, aggregator). Direct EDGAR API was not used (SEC_CONTACT unset); company 8-K exhibits on sec.gov/Archives were read through WebFetch.

## 0. Verdicts

| Name | Report verdict | My verdict | One-line reason |
|---|---|---|---|
| LLY | Tier 1 core | **CONFIRM, smaller and staged** | Primary-source numbers hold. Price is fair, not cheap; EPS path leans on IPR&D normalising; tails in the report's odds are too thin |
| CB | Tier 1 core | **CONFIRM, start after the Oct 20 print** | Best diversifier and cheapest. Report missed Hurricane Isaias (Cat 2, Destin FL, Oct 9-10) and understates the pricing downturn; its kill triggers are too loose to protect |
| MA | Tier 2 starter | **DOWNGRADE to watchlist (no starter)** | The report's own scenarios give about +4% expected 12m return, below a 5.2% Treasury; at an all-time high; weakest diversifier |
| CVX | Tier 2 hedge starter | **KILL as a hedge, do not start** | At 1% size the hedge offsets about 0.1pp of an oil-shock loss. Base-case price is too generous (CVX was $164 at Brent $73 in June). Zero expected return with wide dispersion |
| GD | Tier 3 watchlist | **CONFIRM watchlist only** | Correctly gated. Missed CEO succession (Oct 7). Trigger B compares a forward to a trailing multiple. Not a candidate under the lab's rank rule (45th percentile momentum) |
| KRYS | Tier 3 wait | **DOWNGRADE (remove from the diversifier basket)** | Not a diversifier (acts like tech in sell-offs, most rate-sensitive of the six). Q3 consensus needs +8% q/q after +2.4% in Q2; Germany price outcome due in Q3; US pool near saturation |

**Start first (if anything): CB and LLY**, in that order of fit, each as a first tranche only, and neither needs to be bought before the prints (CB Oct 20, LLY Oct 29, both dates from Yahoo, unconfirmed). Concrete plan in section 9. If the investor wants zero event risk, "none before Oct 29, then CB and LLY thirds" is equally defensible; I found no evidence that buying 2 weeks earlier has an edge (lab: timing states carry no return edge).

## 1. Macro and basket-level checks

| Item | Report | My check (2026-10-13) | Result |
|---|---|---|---|
| S&P 500 | ~7,800 (10-07) | 7,805 close; 200d MA 7,260; 52w high 7,819 | Confirmed. US regime filter ON |
| 10-yr yield | touched 5.36% on 10-07 | ^TNX high since 09-20 = 5.36% (intraday), closes 5.22-5.31 since 09-30; was 4.42 on 06-30 | Confirmed; +80bp in 3.5 months, which the report under-weights |
| Brent | $100.20 on 10-07 | Front future 106.4 on 10-13. EIA (Oct STEO, secondary reports): Sep spot avg $114, Q4 $105, 2027 ~$84 | Report's oil context is stale (its EIA $69 for 2027 is the August forecast) |
| Earnings yield vs 10-yr | not discussed | Forward earnings yields (1/PE on 2027E): LLY 4.1%, MA 3.8%, KRYS 2.9%, GD 5.6%, CVX 6.9%, CB 8.5% vs 10-yr 5.2% | INFERENCE: four of six offer less forward earnings yield than a Treasury; growth must carry them |
| Report's correlation table | 0.26/0.26/0.59/0.33/0.35/0.29 vs AI-8 basket | Reproduced exactly (daily, 2018+). Equal-weight 5-name sleeve vs AI-8: 0.50 | Confirmed |
| "Mean return on QQQ worst-10% days" | LLY -0.43, CB +0.46, MA -0.53, CVX -0.23, GD -0.34, KRYS -1.37 | Window-dependent. Since 2018 (QQQ avg -2.74%): LLY -0.88, CB -0.76, MA -1.90, CVX -1.21, GD -1.06, KRYS -2.42. Last 12m (QQQ -2.07%): LLY +0.68, CB +1.23, MA +0.29, CVX +0.93, GD -0.07, KRYS -0.96 | Direction holds (sleeve loses 25-60% of QQQ on bad days; MA and KRYS the most), but "CB positive" is a recent-regime result, not a law. The 2020 crash makes all negative |
| Drawdown table | 2022: CB -8, CVX 0, GD -1; Apr 2025: CB 0, GD 0 | My peak-to-trough in the same windows: 2022: CB -19, CVX -25, GD -15, MA -28, LLY -13, KRYS -33. Apr 2025: CB -9, GD -10, CVX -19, LLY -22, MA -17, KRYS -18 | **Report measures decline from the window start, which flatters names that rose first.** Peak-to-trough is what a buyer experiences. Stress inputs for sizing (-35% to -55%) are still adequate; the "protected in 2022/Apr 2025" narrative is true only relative to the AI basket |
| Sleeve vs AI basket in stress (my calc) | "diversifier partly" | Equal-weight LLY/MA/CB/CVX/GD vs equal-weight AI-8, peak-to-trough: Mar 2020 -39% vs -31%; 2022 -13% vs -43%; Apr 2025 -12% vs -25%; last 12m -8% vs -18% | **Diversification claim confirmed for rate/AI/tariff stress, fails in a liquidity crash.** The report states this correctly |
| Last-12m reality check | not in report | Within the past 12 months LLY fell 23% peak-to-trough (low 2026-04-29), CVX 21%, MA 18%, GD 18%, KRYS 17%, CB 10% | These are not low-vol assets. A 20-25% loss limit can be hit by ordinary variation in LLY, CVX and MA alone |

Gaps in the diversification claim that the report does not state:
- The test basket is the 8 held single stocks. A Nasdaq-100 index fund and a large India/financial-services block sit on top of those. MA and CB are financial-sector names with 0.5 daily correlation to the employer's stock (BNY) and 0.7 to the financial sector ETF (XLF); CVX and GD are also 0.5 with BNY. **INFERENCE: for an investor whose income and employer stock already depend on financial services, MA and CB add to that factor, not away from it.**
- FX is ignored. USD/INR moved 89.8 to 95.0 this year (about +5.8%), a tailwind to USD assets in rupee terms; a peace/oil-down scenario would likely reverse part of it at the same time CVX falls.
- Survivor bias: the universe is today's S&P 500/400 members; the screen picked names after large moves (KRYS 12-1 momentum +87%, LLY +37%). The report says so; the basket CAGR of 25.8% must not be read as expected return.

## 2. Arithmetic audit (all recomputed)

| Check | Result |
|---|---|
| P/E table (price / consensus EPS): LLY 32.4x guide mid or 33.1x consensus ($35.19) / 24.5x 2027E; CB 12.3/11.8; MA 30.3/26.2; CVX 12.8/14.6; GD 19.7/17.8; KRYS 41.5/34.6 | All correct |
| Entry/trim levels: LLY $1,190 = 25x 2027E; $1,075 = 29.9x guide; $1,430 = 30x; CB $355 = 12.6x, $400 = 14.2x; MA $575 = 28.8x, $540 = 27.1x, $720 = 31.2x; CVX $200 = 13.4x 2027E; $240 = 16.1x; KRYS $290 = 37.5x | Correct |
| **GD trim at $400 "21x 2026E"** | **Wrong label: $400 / $16.85 = 23.7x. It is 21.4x on 2027E.** GD 52w closing high is $396 |
| GD trigger B "$300 ... below its 4-yr low multiple" | $300 / $16.85 = 17.8x is a **forward** multiple compared with a **trailing** FYE range of 18.6-21.4x. On TTM EPS ($16.24) $300 is 18.5x, inside the range, not below it |
| Sizing table: caps sum 13.0%; first tranches 3.0%; loss at cap 1.2+1.1+1.2+0.5+0.9+0.55 = 5.4pp | Correct; 5.4/13 = 41% |
| MA scenario table (bear $473 / base $645 / bull $744) | Arithmetic right. With the report's own odds shape (25/50/25) expected 12m price change is about +3.8% (+0.6% dividend) vs 5.2% on a Treasury. Not a buy on its own numbers |
| CVX scenario table | Arithmetic right, but base case ($70 Brent -> $201) is contradicted by CVX's own June trading: $164 on 2026-06-30 with Brent $73 (-25% from today) |
| Report: "Chubb P&C combined ratio 83.8% (85.4% a year earlier)" | Primary source says **85.6%** a year earlier. Minor |
| Report: LLY "-28% at 22x on $38 EPS" | Correct arithmetic ($836) but compares a multiple with 2026 EPS; use 2027 EPS ($44-48 -> $970-1,050 at 22x, i.e. -10% to -17%). The bear case in the report is slightly overstated; mine is below |

## 3. LLY (Eli Lilly): CONFIRM, smaller and staged

**Re-verified (FACT, Lilly Q2 8-K Ex.99.1, 2026-08-05):** revenue $22,974M, +48% (volume +60%, price -13%); Mounjaro $9,943M (+91%); Zepbound $4,928M (+46%); Foundayo $98M; US +33% to $14.4B on 37% volume, price -3% (about -9% before rebate adjustments); ex-US +80% to $8.6B with price -36% (China NRDL); Q2 IPR&D $2,776M = $3.03/share; FY26 revenue guide $85-87B (from $82-85B); non-GAAP EPS $35.50-36.50 (**the top end was cut from $37.00**, and the report's "raised" applies to revenue and margin only); performance margin 49.0-50.5%; retatrutide BLA submission planned Q1 2027. Yahoo: price $1,166.51, 200d MA $1,077.5, 52w high $1,280 (2026-08-19), mean target $1,330 (29), forward EPS $47.57, trailing P/E 39x. All match.

**New or corrected facts**
1. Foundayo data in the report is stale (June). Newer secondary data: about 34,000 weekly US scripts in early August (+16% w/w, via Citi/IQVIA) and about 44,000 in early September (blog citing Fierce Pharma, unverified), versus about 172,000-181,000 for Novo's Wegovy pill. The gap is still 4x but narrowing, so the report's June ratio (11.7k vs 67k) overstates the lag. **Kill trigger (c) "Foundayo Q3 revenue below Q2's $98M" would almost certainly pass and carries no information.** Replace it with Foundayo Q3 revenue below $200M or weekly scripts falling for 4 weeks.
2. Consensus is above guidance: FY26 revenue $88.6B vs the $87B top of the guide; Q3 revenue consensus $22.4B is **below** Q2's $22.97B. Q3 EPS consensus $7.16 with a $4.65-10.68 analyst range (IPR&D uncertainty). The print is a wide-variance event.
3. **2027E EPS of $47.57 is +35% on revenue +15.5% ($102.4B).** That gap needs IPR&D to normalise. Lilly booked $3.03/share of IPR&D in Q2 alone and buys assets most years. INFERENCE: if 2027 carries $2-3 of IPR&D, EPS is $44-46, and the "24.5x" is 25.5-26.5x.
4. Pricing/policy facts the report left out: Medicare GLP-1 Bridge (from 2026-07-01) lets eligible patients pay $50/month; Leerink refers to a Medicare net price step-down to about $245/month (secondary, undated); the FDA proposed in April to remove semaglutide/tirzepatide/liraglutide from the 503B compounding list (final decision pending, supportive for Lilly). Policy is a two-sided risk; price -13% is the realised cost so far.
5. Dividend yield 0.6%, so the 25% US withholding is immaterial.

**My scenario table (reviewer model, not a forecast)**: price in Oct 2027 = trailing-4Q EPS (about $45 by Q3 2027) x multiple. Bear 22x x $40 = $880 (-25%); base 28x x $45 = $1,260 (+8%); bull 32x x $50 = $1,600 (+37%). Today's trailing multiple is 39x vs 47x at year-end 2025, so the base case already assumes continued compression.

**Odds (model; 12m from ~$1,166).** Realised vol 34-35% blended with the 21-year history (survivor-biased). Report: P(+30%) 15%, P(touch -25%) 14%, P(end <= -25%) 8%. A lognormal at the stock's own vol gives 23% / 42% / 21%; the history gives 32% / 9% / 3%. LLY fell 23% in the last 12 months. **My estimates: P(+30%) 18%; P(>= +10%) 42%; P(touch -25%) 22%; P(end <= -25%) 10%.**

**Entry-plan changes**
- Cap 3.0% (not 3.5%): highest-vol name of the two I would start, 23% peak-to-trough in the last 12m.
- T1 0.8% (not 1.2%) at <= $1,190 now or after the Oct 29 print; T2 only if Q3 shows US Mounjaro+Zepbound sequential growth and FY26 revenue guide >= $86B and price <= $1,250; T3 at the 200d MA ($1,075-1,100) or after Q4 (early Feb 2027). Do not chase above $1,300.
- Replace kill (c) as above. Keep (a) guide cut below $85B, (b) sequential US decline in tirzepatide, (d) BLA slip beyond 1H 2027. Add: non-GAAP EPS guide midpoint cut by more than the disclosed IPR&D.
- Review at -20% from average cost stays; sell at -25% only with a broken thesis (the report's rule is sensible).

## 4. CB (Chubb): CONFIRM, start after the Oct 20 print

**Re-verified (FACT, Chubb Q2 8-K Ex.99.1, 2026-07-21):** core operating EPS $7.26, +18.2% (from $6.14); P&C combined ratio 83.8% (85.6% year ago); current-accident-year ex-cat 82.2%; favorable prior-period development $283M; cat losses $475M ($630M); net investment income $1.76B, +12.3%; P&C net premiums written $12.77B, +3.0% (+6.3% ex large-account/E&S property, **+1.4% constant dollar**); North America Commercial NPW -2.3% with **combined ratio 85.4% vs 83.5%**; book value/share $195.45; buybacks $979M in Q2 at an average $327.18 (so today's $346 is 6% above where the company bought). Yahoo: price $346.16; 200d MA $330.9; consensus EPS 2026 $28.14, 2027 $29.26; Q3 consensus $6.80 (-9% y/y; the year-ago $7.49 had only $285M of cat losses); Q3 print 2026-10-20 (Yahoo, unconfirmed). P/B 1.77x, price / tangible book 2.62x (my calc).

**Missed by the report**
1. **Hurricane Isaias made landfall near Destin, Florida as a Category 2 (105 mph) on 2026-10-09/10** (AP via ITV, Mississippi Today, AJC). First hurricane of the season; Gallagher Re's preview said a Cat 2 Gulf landfall would typically mean low-to-mid single-digit billions of insured loss. Q3 ended 09-30, so it falls in Q4; the Oct 20 call is the first place management will size it. The report's T2 rule ("after Q3 print if combined ratio < 90%") would test the wrong quarter. CB shares closed at $346 on 10-13 versus $341 on 10-09, so the market is not pricing a large loss. No loss estimate found: unverified.
2. The pricing downturn is deeper than the report says. Marsh Global Insurance Market Index (Q2 2026, via Insurance Journal and others): global commercial rates -6%, **eighth consecutive quarterly decline**; property -12% (US -13%); cat-exposed US programs -20%. Casualty alone is rising (+2% global, US +7%), which is also where reserve risk lives (INFERENCE).
3. Q3 consensus EPS growth is negative (-9%) and Q4 -4%; the report notes this. The stock also trades only 6% above where management bought stock, so buyback support is thinner than at $327.

**Kill criteria: too loose to act as protection.** "Combined ratio above 92% for two quarters" is 8 points worse than today's 83.8% and would mean most of the earnings are gone before the trigger fires. Replace with: P&C combined ratio ex-cat above 88% in any one quarter, or current-accident-year ex-cat above 85% (today 82.2%), or constant-dollar P&C NPW negative in a quarter, or prior-year adverse development above $300M in a quarter (the report's $500M is also late). Keep the 200d-MA/EPS-revision exit.

**Scenario (model):** Oct 2027 price = EPS x multiple. Bear EPS $24 x 10.5 = $252 (-27%); base $29 x 12.3 = $357 (+3%, plus 1.2% dividend); bull $31 x 13.5 = $418 (+21%). So CB is also a "fair price, good business" case, not a bargain.

**Odds (model):** report 6% / 8% / 4% for P(+30%) / P(touch -25%) / P(end <= -25%). Lognormal at 20% vol: 13% / 10% / 5%. **Mine: P(+30%) 7%; P(>= +10% incl. dividend) 40%; P(touch -25%) 9%; P(end <= -25%) 4%.** Report's odds acceptable.

**Entry-plan changes:** T1 0.8% **after** the Oct 20 print and the Isaias loss estimate, if Q3 combined ratio < 88% and price <= $360; T2 at the 200d MA ($330-340) or after Q4 (late Jan 2027, which is when Isaias, the Jan 1 renewals and casualty reserves are all visible); cap 2.5% stays.

**Tax flag (new):** Chubb Limited is Swiss-domiciled. Its filings say ordinary Swiss dividends are subject to 35% Swiss withholding unless paid from capital-contribution reserves or as par-value reductions, which Chubb says it uses; a 2026 proxy asks to release CHF 2.5B of reserves for dividends of up to $4.08/share. The report applies the US 25% DTAA withholding to CB: **unverified for a Swiss issuer; verify with CA/broker.** US-estate-tax exposure may also differ for a non-US corporation (unverified; verify).

## 5. MA (Mastercard): DOWNGRADE to watchlist, no starter

**Re-verified (FACT, MA Q2 8-K Ex.99.1, 2026-07-30):** net revenue $9.3B, +14% (+12% currency-neutral); adjusted operating margin 61.1% (+1.2pp); adjusted EPS $5.04 (+21%; +19% currency-neutral); GAAP EPS $4.97; litigation provisions $82M; buybacks $4.9B in Q2, $7.8B left; cross-border +12% (local currency); gross dollar volume +8% (local currency). Yahoo: price $604.80 = 52w high; 200d MA $532.5 (+13.6%); +9.8% since 2026-09-30 ($550.6); 2026E EPS $19.94 (30.3x), 2027E $23.06 (26.2x). Q3 print 10-29 (Yahoo).

**Why DOWNGRADE**
1. By the report's own scenarios the expected 12m move is about +4%, versus 5.2% on a 10-yr Treasury. The business is excellent; the entry price is the problem.
2. 12-1 momentum rank 38th percentile: the lab's only selector with edge gives it no credit. It is the weakest diversifier (0.59 correlation to the AI basket; daily beta 0.34, but -1.9% on QQQ's worst days since 2018).
3. Legal: revised interchange settlement preliminarily approved 2026-06-09 (Judge Cogan, per Shelby Report/Reuters): 10bp cut in average effective credit interchange over five years, 1.25% cap on some posted rates; merchant groups (NGA, Merchant Payments Coalition) oppose and push the Credit Card Competition Act. As of an Aug 4 prediction-market piece, CCCA had no markup or floor vote since reintroduction on 2026-01-13. Final-approval hearing date: unverified. Risk is real but not imminent.
4. Kill trigger "CCCA or equivalent enacted" is too late: the stock would have repriced at the vote. Use "CCCA attached to a must-pass bill, scheduled for a floor vote, or a committee markup" as the review trigger.
5. Financial-sector overlap with the employer (section 1).

**Plan instead:** no starter at the high. Start only on a pullback to the 200d MA area: T1 0.75% at <= $560 (28x 2026E) after the Oct 29 print if cross-border >= 10% and margin >= 60%; T2 <= $540; cap 2.5%. If it never pulls back, accept missing it; the lab's evidence is that being early or late on a non-selected name has no demonstrated edge.

**Odds (model):** report 8% / 12% / 6%. Mine: P(+30%) 10%; P(>= +10%) 38%; P(touch -25%) 14%; P(end <= -25%) 7%. Mean 12m change near +4%.

## 6. CVX (Chevron): KILL as a hedge; do not start

**Re-verified (FACT, CVX Q2 8-K, 2026-07-31):** adjusted EPS $6.06 (vs $1.77); production 4,070 MBOE/d vs 3,396 (+19.8%); adjusted FCF $15.4B (vs $4.9B); capex $4.5B vs $3.7B; buybacks $3.1B; total debt $37.1B, down $8.4B in the quarter; Hess synergies $1.5B run-rate; average Brent $104 vs $68; dividend $1.78/quarter. Yahoo: price $217.73 = 52w high; 200d MA $188.8; 2026E EPS $16.99, 2027E $14.91 (-12%); Q3 consensus EPS $4.78 vs Q2's $6.06; Q3 print 10-30 (Yahoo).

**Why KILL**
1. **The hedge arithmetic fails (computed from public prices).** In the March 2026 oil shock (2026-02-27 to 03-31): Brent +63%, CVX **+10.8%**, QQQ -4.8%, Nifty -11% (INDA -10.4% in USD). CVX moves about one-fifth as much as Brent in the up-leg and fell **19%** when Brent fell 38% in Q2. To offset an India-equity loss of -10% you need a CVX weight roughly equal to the India equity weight. At the report's 1.0% cap the offset is about 0.1pp of net worth against an oil-shock loss many times larger. **A hedge that cannot hedge is a small, cyclical, peak-priced position, not insurance.** If a true oil hedge is wanted, it is a different decision at a size that breaches the stated loss limit.
2. The base case is too generous. On 2026-06-30 Brent was $72.9 and CVX closed at $164.3. The report's base ($70 Brent -> $201, -8%) ignores that the market has recently paid $164 at that oil price. Updated model: Brent >= $95 (30%): ~$240 (+10%); $75-95 (40%): EPS ~$17 x 13 = ~$221 (+1.5%); < $75 (30%): ~$160-175 (-20% to -27%). Weighted about -3% plus 3.3% dividend, so **expected return near zero** with dispersion of roughly +/-20%.
3. Oil context in the report is stale: Brent was $106 on 10-13, September spot averaged $114 (EIA, secondary), and EIA's October outlook is ~$105 for Q4 and ~$84 for 2027 (secondary; the report's $69 is the August forecast). Two-way: the 2027E EPS of $14.91 looks low against an $84 deck, and Q3 EPS consensus of $4.78 against $6.06 in Q2 looks low against ~$98 average Q3 Brent (INFERENCE). That is a possible beat, but it is already partly in a stock +33% since June 30.
4. Brent has round-tripped $71 -> $118 -> $73 -> $106 within nine months; Hormuz headlines drive it.
5. Energy exposure already sits inside the investor's India and index funds (qualitative; sector weights in the private brief).

**If the investor still wants CVX:** treat as a return idea, not a hedge, pre-commit to buy only at <= $185 (about 12.4x 2027E, near the 200d MA), size <= 1%, and exit below $165. **Odds (model):** mine P(+30%) 6%; P(touch -25%) 28%; P(end <= -25%) 14% (report 7% / 20% / 10%).

## 7. GD (General Dynamics): CONFIRM watchlist only

**Re-verified (FACT, GD Q2 8-K Ex.99.1, 2026-07-29; quarter ended 2026-07-05):** revenue $14,094M (+8.1%); operating margin 10.4%; EPS $4.24 (+13.4%); backlog $136.5B (govconwire: +32% y/y), funded $104.1B; orders $20B, book-to-bill 1.4x; operating cash flow $1,880M (162% of net earnings); free cash flow $1,646M; net debt $3.2B; Marine Systems margin 7.3%, Aerospace 14.5%; 41 Gulfstream deliveries. **The exhibit itself carries no full-year guidance**; I confirmed through govconwire (secondary) that FY26 EPS guide is **$16.80-16.90** (raised from $16.45-16.55 in April and $16.10-16.20 in January) with revenue ~$55.7B and margin 10.5%. So the report's guide is right, and the raise cadence is a point in GD's favour. Yahoo: price $332.42; 200d MA $354.9 (the report's $351 is stale); 52w closing high $396; consensus 2026 $17.00, 2027 $18.65.

**Missed or corrected**
1. **CEO succession announced 2026-10-07:** Danny Deep (president) becomes CEO on 2027-01-01; Phebe Novakovic (CEO since 2013) becomes executive chairman (company 8-K, GovConWire, PR Newswire). Internal, planned succession, but it is a change of the person behind 13 years of capital-allocation discipline. The report called the autumn decline "unexplained". The 13.5% fall from $381.6 (2026-07-31) to $330.2 (09-30) preceded this news; the cause remains unverified (rates are the leading INFERENCE: weekly sensitivity to the 10-yr is statistically zero in my regression, so that explanation is weak).
2. Trim label error (23.7x on 2026E, not 21x) and trigger B multiple mismatch (section 2).
3. Marine Systems is 33% of revenue at a 7.3% margin and 48% of backlog ($65.2B). Execution on submarine programmes is the real earnings lever; the report says "shipyard execution" but gives no observable kill number. Add: Marine Systems margin below 6.5% for a quarter.
4. Q3 date unverified (Yahoo 10-30; GD reported Q2 on 07-29, so a late-October date is likely).

**Plan unchanged:** no action. Trigger A (5 closes above ~$355 and backlog >= $136B at the Q3 print) or B (<= $300, book-to-bill >= 1.0) are acceptable once the multiple label is fixed. Cap 2.0%. **Odds (model, $332 entry):** P(+30%) 12%; P(touch -25%) 15%; P(end <= -25%) 6%.

## 8. KRYS (Krystal Biotech): DOWNGRADE, remove from the diversifier basket

**Re-verified (FACT, KRYS Q2 8-K Ex.99.1, 2026-08-03):** VYJUVEK global revenue $119.2M (+24%); gross margin 95%; net income $54.8M, EPS $1.79 diluted (**primary-source confirmed; the report's "secondary" caveat can be dropped**); cash and investments $1.1B (about 11.6% of the $9.5B market cap); R&D+SG&A guide $175-195M; no debt. The release does not split US revenue; the $91.6M US figure comes from call summaries (Nasdaq/Quartr), as does Q1 US $87.5M. Q1 2026 global revenue was $116.4M (+32%, Q1 8-K), of which Europe+Japan $28.9M.

**New facts that change the picture**
1. **Sequential growth is slowing:** Q1 $116.4M -> Q2 $119.2M is **+2.4% q/q** (Q1 was +9% vs Q4). Europe+Japan fell from $28.9M to $27.6M, which management ties to a reserve for Germany's ongoing price negotiation; **the German outcome is expected in Q3**. A lower negotiated price is a realistic downside. US reimbursement approvals exceed 730, said to be above the company's own 60% penetration target, which is consistent with a maturing US pool (the report's inference, now supported).
2. **Consensus is demanding:** Q3 revenue $129.1M (+8.3% q/q; +32% y/y), Q4 $138.4M; FY26 $504.8M implies H2 average of $134M versus $119M now. The report's start trigger "Q3 >= $125M" is below consensus, so a print that passes the trigger can still be a miss versus expectations; the stock can fall through the 200d MA at the same time, making the trigger's AND condition self-defeating.
3. **Registrational binary events the report could not name:** KB803 (IOLITE, corneal abrasions in DEB) is fully enrolled with top-line readout in **4Q 2026**; KB407 (cystic fibrosis, about 5 patients) interim and FDA alignment 4Q 2026; KB111 interim before year-end; KB801 enrolment completes before year-end; KB707 interim updates later this year. Several readouts land in the same 10 weeks as Q3 results.
4. **EPS quality:** 2026E EPS of $7.74 includes interest income on $1.1B (roughly $1.3/share by my estimate at a 4%+ yield; INFERENCE). Excluding cash and its income the multiple is about 44x, not 41.5x.
5. **Not a diversifier:** beta to QQQ 0.64; -2.4% on QQQ's worst days since 2018 (-0.96% in the last 12m); -1.3% per +10bp weekly 10-yr move (the most rate-sensitive of the six); Mar 2020 -44%, 2022 -33%. At 33x with the 10-yr at 5.2% it is long-duration.

**Plan:** drop from the basket; if the investor wants a speculative biotech position it is a separate 0.5% decision after Nov 2 (Q3) and the KB803 readout, sized as a total-loss-tolerable bet. **Odds (model):** P(+30%) 25%; P(touch -25%) 50%; P(end <= -25%) 27% (report: 25% / 35% / 20%; a lognormal at 38-47% vol gives 25% / 58% / 31%). The cap of 1.0% at -55% stress is fine; the status as "Tier 3 wait" is too kind.

## 9. What I would change in the plan (combined)

| Item | Report | Review |
|---|---|---|
| Sleeve size | 13% at caps; 3.0% now | **About 5.5% at caps for the two names I would start (LLY 3.0%, CB 2.5%); 1.6% initial.** Add MA (cap 2.5%) only on the pullback rule; GD (2.0%) only on trigger; CVX and KRYS removed |
| Worst-case at caps | 5.4pp | LLY 3.0 x 35% = 1.05pp; CB 2.5 x 42% = 1.05pp; two-name total about 2.1pp of net worth in a Mar-2020-type replay. Add MA 2.5 x 41% = 1.0pp if later built. Still above 20-25% on invested money for CB in a liquidity crash (-42%) |
| Order of events | buy T1 now for LLY, CB | Wait for Oct 20 (CB: Q3 and Isaias loss estimate) and Oct 29 (LLY, MA). The lab has no timing edge, but waiting costs little and removes two known binary prints plus an unquantified hurricane |
| Tax/employer | as listed | Add the CB Swiss-issuer flag (section 4). Everything else in the report's tax section is consistent with my understanding but remains **unverified** (blog sources): 24-month long-term threshold at 12.5% for foreign shares; 25% DTAA withholding for US issuers; LRS USD 250,000; TCS threshold (Budget 2025 raised it to Rs 10 lakh as I recall; verify); US estate-tax threshold about USD 60,000 for non-US persons. **Verify all with CA/bank; employer pre-clearance with HR/compliance (MA, CB are in the payments/insurance universe the employer's compliance list may cover).** |
| Lab-rule consistency | momentum rank not applied | By the lab's only selector the ranks are KRYS 94, CVX 84, LLY 77, CB 63, GD 45, MA 38. The two I would start rank 3rd and 4th; the highest-ranked two fit worst as diversifiers. This is a trade-off the report should state: diversification is bought at the cost of the lab's selector. The lab also says trend filters protect rather than find winners, so these are protection and fit, not alpha |

**Which to start first, and why**
1. **CB first (after Oct 20):** lowest correlation to the AI book (0.26 overall, negative over two years), smallest peak-to-trough in the last year (-10%), 11.8x 2027E with a 1.2% yield, buybacks, benefits when yields rise through investment income (record $1.76B). Counter: soft pricing and cat/reserve tail; fit overlaps with financial-services factor. Size modestly.
2. **LLY second:** best earnings growth, 0.26 correlation, top-third momentum rank, but at a fair rather than cheap price with EPS that depends on IPR&D normalisation; start at 0.8% and add on the Oct 29 print only if US tirzepatide volumes and guide hold.
3. **Not now:** MA (price), CVX (hedge maths), GD (trend and rank), KRYS (event risk, not a diversifier).
Neither CB nor LLY has a margin of safety against a market-wide de-rating with the 10-yr at 5.2%; the case is diversification and quality, as the report says. If the S&P 500 closes below its 200d MA (7,260 now) the lab rule says pause new tranches.

## 10. Data gaps and honesty notes

- Not verified: Lilly's and Chubb's Q3 dates (Yahoo only); GD, MA, CVX, KRYS dates; Hurricane Isaias insured-loss estimates; EIA October STEO numbers (secondary reports only; I did not open the PDF); current Foundayo scripts (blog, secondary); GD's autumn decline cause; MA's recent +10% rally cause; MA final settlement hearing date; any news after 2026-10-13.
- My odds are model outputs from realised volatility and survivor-biased history; treat as ranges of +/-5-8 points.
- I did not re-run the lab's `discovery.py` or rebuild the 903-name universe funnel (281 -> 113 -> 26), and did not test the omitted names (V, TRV, JNJ, MRK, REGN, ABBV, XOM) beyond what the report lists.
- Prices from Yahoo are unaudited aggregates; EPS consensus figures are aggregator means.

## 11. Sources (accessed 2026-10-14)

- Lilly Q2 8-K: https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000077/q226lillysalesandearningsp.htm
- Chubb Q2 8-K: https://www.sec.gov/Archives/edgar/data/0000896159/000119312526310312/d78544dex991.htm ; Chubb 424B2/10-K language on Swiss withholding (sec.gov, search result); Chubb DEFA14A 2026-04-28
- Mastercard Q2 8-K: https://www.sec.gov/Archives/edgar/data/0001141391/000114139126000081/ma06302026-exx991xearnings.htm
- Chevron Q2 8-K: https://www.sec.gov/Archives/edgar/data/0000093410/000009341026000162/a06302026ex9918-k.htm
- General Dynamics Q2 8-K: https://www.sec.gov/Archives/edgar/data/0000040533/000004053326000029/gd-20260705exhibit991.htm ; guidance via https://www.govconwire.com/articles/general-dynamics-q2-2026-earnings-results ; CEO succession 8-K https://www.sec.gov/Archives/edgar/data/0000040533/000119312526417188/d122892dex991.htm and GovConWire
- Krystal Q2 8-K: https://www.sec.gov/Archives/edgar/data/0001711279/000171127926000058/a2q26-ex991xpressrelease.htm ; Q1 8-K https://www.sec.gov/Archives/edgar/data/0001711279/000171127926000044/a1q26exhibit991pr.htm ; call summaries nasdaq.com, quartr.com, marketbeat.com
- Hurricane Isaias: ITV News 2026-10-10, Mississippi Today 2026-10-09, AJC (AP). Marsh Q2 2026 index: Insurance Journal 2026-07-23, beinsure.com, reinsurancene.ws
- Oil/rates: EIA STEO Oct 2026 via trend.az and shipandbunker.com (secondary); XTB 2026-09-28 wrap; Al Jazeera 2026-09-14
- Interchange/CCCA: Shelby Report 2026-06-11, America's Credit Unions, Payments Dive, prediction-market summary 2026-08-04
- LLY oral GLP-1: hlth.com 2026-08-10, Fierce Pharma tracker, onedayadvisor.com (blog, 2026-09); Medicare Bridge and Leerink items via Yahoo Finance/TipRanks (undated)
- Prices, moving averages, consensus tables, correlations, drawdown and oil/Nifty regressions: yfinance, computed 2026-10-14 (scripts in session scratchpad, not committed)
