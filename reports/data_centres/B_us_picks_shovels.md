# B. US "picks and shovels" for data centres: valuation vs growth vs customer concentration

As of 2026-10-19. Prices are 2026-10-16 closes (yfinance). Research for one investor's decision, not advice; nothing is executed. Public file: no personal rupee or holding numbers.
Tags: **FACT** (source named), **INFERENCE** (my arithmetic/reasoning), **SPECULATION**, **unverified** (aggregator, single secondary source, or not found). Probabilities are labelled model estimates.

**Method and limits (read first).** P/E, EV/EBITDA, FCF yield, debt and consensus EPS are Yahoo Finance aggregates (yfinance 1.7.0, pulled 2026-10-19), so all of them are *unverified* against filings. I cross-checked consensus against company guidance where I could: VRT FY26 guide adj EPS $6.70 vs Yahoo 6.74; EME $32.00-33.25 vs 32.99; HUBB $20.25-20.55 vs 20.51; NVT $5.00-5.10 vs 5.16; ETN $13.40-13.60 vs 13.59; JCI ~$5.05 vs 5.07; NTAP $9.73-10.03 vs 10.00 (all within range, so the consensus feed looks current). Company facts (backlog, customers, guidance) come from web-search summaries of 8-Ks, 10-Ks/10-Qs and call write-ups; I did **not** read the full filings (I tried Vertiv's FY25 10-K: the customer-concentration note was not in the text I could reach). "Net debt/EBITDA" uses Yahoo gross debt (it can include leases, non-recourse and finance-arm debt), so it overstates leverage for HPE, NRG, VST, CEG, TLN. "Own 5y median" = median of (price on each report date / trailing-4Q adjusted EPS) over the last 5 years, built from Yahoo reported-EPS history: a rough yardstick, not a forward-multiple history (forward-multiple history was not obtainable). Correlations are 3y daily (2023-10-17 to 2026-10-16) against the equal-weight average of MSFT, GOOGL, AMZN, NVDA, TSM, MU.
Already downgraded by the lab and not re-proposed: Sterlite Tech, HFCL, TD Power, Kirloskar Oil Engines, Vicor, MaxLinear, Viavi, FormFactor, Amphenol (held). Nothing material has changed since 5 Oct that I found.

## 0. Bottom line

1. **Backdrop (FACT, lab macro report F, 2026-10-14):** Fed hiked 16 Sep to 3.75-4.00%, 10y ~5.2%, Brent ~$125, Shiller CAPE 41.8; SOX 16.6% below its June record. The AI-hardware complex has been derating on rates and "AI optics profit-taking" (FACT: 247wallst, 15 Oct: Coherent -7%, Lumentum -5% in a day on rotation, no company news). Most names below are 20-50% off highs, **which is not a valuation argument**; I show the arithmetic instead.
2. **Four names offer the best valuation-vs-growth with the least dependence on a few hyperscaler orders (START-SMALL, tiny size):** EMCOR (EME), Vertiv (VRT), HPE, NRG Energy. Each has a specific hole (see section 3): EME is a thin-margin contractor and its data-centre share is unverified; VRT is the most AI-correlated and the Q3 print is days away; HPE's FY26 EPS jump is partly Juniper and its "cheap" multiple has already doubled vs its own history; NRG is levered and its hyperscaler deal is not final.
3. **Priced for perfection (AVOID at these prices):** Bloom Energy, Lumentum, Credo, Arista, Ciena, Corning, GE Vernova, Quanta, plus Everpure (ex-Pure Storage). Several also have the worst customer concentration (2-3 customers = 40-84% of sales).
4. **Cheap for a reason (concentration or cash burn):** Celestica (3 customers = 62% of 2025 revenue), Modine (one hyperscaler agreement ~half of capacity), Coherent (negative FCF), Super Micro (FCF yield -40%), AAON (3 customers >=10%, negative FCF).
5. **Portfolio fit:** the investor already holds ~31% AI look-through (semis ~15%). Nothing here diversifies away from AI: 3y correlation to the six AI holdings runs 0.26 (GNRC) to 0.47 (ETN, VRT 0.46); the market itself (SPY) is 0.61. In the worst 10% days for those six stocks, correlation of the shortlist rises to 0.5-0.67 (section 4). Treat every START-SMALL name as an addition to AI exposure, not a hedge; fund it by trimming, or accept AI above ~31%.
6. **The 20-25% loss limit will probably be touched on any single name** (model estimate: 32-68% chance of a -25% touch inside 12 months at realised vol, section 4). Only small size and a basket cap control this, not stock selection.

## 1. Ranked table (valuation snapshot, 2026-10-16)

FY0/FY1 = current/next fiscal year consensus EPS (year-ends differ: VRT, ETN, EME, HUBB, NVT, GNRC, NRG, VST, CEG, TLN, CLS, ANET, TT calendar; JCI, POWL, HPE, CIEN Sept/Oct; DELL Jan; MOD, NTAP, CRDO Mar/Apr; COHR, LITE Jun). PEG = P/E FY0 divided by FY1 EPS growth %. "Req CAGR" = EPS growth per year, FY0 to three years on, needed to earn 10%/yr if the stock exits at 20x (first number) or 15x (second); negative means today's price already assumes shrinkage (INFERENCE, simple reverse-DCF, no dividends, no dilution).

| Name | Px | Cap $B | P/E FY0 | P/E FY1 | EPS g FY1 % | PEG | EV/EBITDA | FCF yld % | ND/EBITDA | Div % | Trailing adj P/E now vs own 5y median | vs 52w high % | Corr 6 AI | Req CAGR @20x/@15x |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EME | 721.66 | 32 | 21.9 | 19.3 | 13 | 1.65 | 15.8 | 3.1 | -0.2 | 0.22 | 24.3 vs 19.7 | -24 | 0.39 | 13 / 25 |
| VRT | 206.42 | 79 | 30.6 | 22.5 | 36 | 0.84 | 29.8 | 3.4 | 0.1 | 0.12 | 39.0 vs 37.5 | -46 | 0.46 | 27 / 40 |
| HPE | 55.13 | 73 | 14.4 | 11.7 | 23 | 0.62 | 12.7 | 6.5 | 2.0* | 1.03 | 22.1 vs 7.1 | -25 | 0.32 | -1 / 9 |
| NRG | 103.75 | 22 | 11.8 | 9.3 | 27 | 0.44 | 14.1 | 3.5 | 7.2* | 1.83 | 15.3 vs 13.2 | -45 | 0.34 | -8 / 2 |
| ETN | 391.25 | 152 | 28.8 | 24.0 | 20 | 1.45 | 26.0 | 2.0 | 3.1 | 1.12 | 31.7 vs 27.3 | -18 | 0.47 | 24 / 37 |
| GNRC | 192.68 | 11 | 19.9 | 14.8 | 34 | 0.58 | 19.7 | 2.5 | 1.8 | 0.00 | 23.6 vs 23.4 | -35 | 0.26 | 10 / 21 |
| NVT | 142.03 | 23 | 27.5 | 21.1 | 31 | 0.90 | 23.2 | 2.0 | 1.3 | 0.59 | 32.7 vs 20.1 | -23 | 0.43 | 22 / 35 |
| JCI | 145.47 | 88 | 28.7 | 23.7 | 21 | 1.38 | 22.4 | 3.4 | 2.0 | 1.10 | 30.6 vs 20.8 | -9 | 0.33 | 24 / 37 |
| HUBB | 461.10 | 24 | 22.5 | 20.0 | 12 | 1.82 | 19.5 | 2.0 | 3.4 | 1.23 | 23.8 vs 22.6 | -18 | 0.37 | 14 / 26 |
| SBGSY (Schneider ADR) | 55.91 | 157 | 24.5 | 19.9 | 23 | 1.06 | 20.4 | 3.4 | 1.9 | 1.76 | n/a | -22 | 0.42 | 18 / 30 |
| VST | 152.02 | 51 | 15.9 | 14.7 | 8 | 1.95 | 11.1 | 0.1 | 3.0* | 0.61 | 27.4 vs 24.0 | -26 | 0.37 | 2 / 12 |
| CLS | 303.81 | 38 | 27.2 | 15.7 | 73 | 0.37 | 22.7 | 1.9 | 0.3 | 0.00 | 37.2 vs 14.5 | -36 | 0.43 | 22 / 34 |
| MOD | 148.86 | 8 | 22.9 | 14.7 | 56 | 0.41 | 18.9 | -0.9 | 1.3 | 0.00 | 27.1 vs 23.6 | -54 | 0.38 | 15 / 27 |
| COHR | 232.90 | 46 | 24.7 | 16.6 | 49 | 0.50 | 33.4 | -1.4 | 1.1 | 0.00 | 41.6 vs 26.7 | -47 | 0.42 | 18 / 30 |
| DELL | 451.71 | 287 | 17.4 | 16.9 | 4 | 4.97 | 17.5 | 2.1 | 1.3* | 0.56 | 24.6 vs 12.2 | -24 | 0.35 | 5 / 16 |
| TLN | 354.81 | 17 | 16.1 | 11.4 | 40 | 0.40 | 45.3 | 7.5 | 16.1* | 0.00 | 24.6 vs 29.0 | -21 | 0.34 | 2 / 13 |
| CEG | 271.37 | 96 | 22.4 | 20.4 | 10 | 2.34 | 15.2 | -6.9 | 3.0* | 0.63 | 25.5 vs 30.0 | -33 | 0.33 | 14 / 26 |
| NTAP | 203.80 | 40 | 20.4 | 18.3 | 11 | 1.77 | 18.6 | 2.9 | -0.5 | 1.02 | 25.0 vs 13.7 | -15 | 0.32 | 11 / 22 |
| POWL | 165.14 | 6 | 30.8 | 24.2 | 27 | 1.14 | 22.8 | 3.2 | -2.7 | 0.22 | 31.7 vs 23.4 | -50 | 0.29 | 27 / 40 |
| TT | 458.89 | 101 | 30.0 | 26.0 | 16 | 1.93 | 24.2 | 3.1 | 0.8 | 0.92 | 33.5 vs 30.7 | -9 | 0.33 | 26 / 39 |
| FIX | 1439.07 | 51 | 29.4 | 23.9 | 23 | 1.29 | 24.5 | 3.6 | -0.8 | 0.25 | 35.4 vs 24.5 | -31 | 0.41 | 25 / 38 |
| PWR | 631.86 | 95 | 37.7 | 31.8 | 19 | 2.03 | 33.2 | 2.1 | 2.0 | 0.07 | 47.1 vs 32.2 | -20 | 0.40 | 36 / 50 |
| AAON | 73.73 | 6 | 30.9 | 20.7 | 50 | 0.62 | 21.8 | -3.5 | 1.5 | 0.54 | 38.2 vs 46.7 | -51 | 0.28 | 27 / 40 |
| ANET | 176.98 | 223 | 43.0 | 33.9 | 27 | 1.60 | 45.2 | 1.7 | -2.9 | 0.00 | 51.2 vs 38.3 | -19 | 0.43 | 42 / 56 |
| CIEN | 332.73 | 47 | 46.4 | 32.2 | 44 | 1.05 | 46.6 | 1.3 | 0.6 | 0.00 | 55.4 vs 25.9 | -48 | 0.35 | 46 / 60 |
| GLW | 132.00 | 114 | 40.2 | 30.2 | 33 | 1.22 | 29.7 | 0.6 | 1.7 | 0.85 | 46.0 vs 18.8 | -51 | 0.32 | 39 / 53 |
| GEV | 921.20 | 245 | 30.3 | 37.6 | -20 | n/a | 60.5 | 6.4 | -2.3 | 0.22 | 48.4 vs 100.2 | -23 | 0.40 | 26 / 39 |
| LITE | 824.13 | 75 | 37.8 | 22.9 | 65 | 0.58 | 91.0 | 0.3 | -1.3 | 0.00 | 98.5 vs 25.6 | -28 | 0.37 | 36 / 50 |
| CRDO | 169.70 | 32 | 26.9 | 17.5 | 54 | 0.50 | 57.4 | 0.8 | -1.4 | 0.00 | 41.4 vs 115.6 | -45 | 0.40 | 21 / 34 |
| BE | 221.31 | 65 | 81.7 | 44.8 | 82 | 0.99 | 156.1 | 0.8 | 0.2 | 0.00 | 121.6 vs 140.4 | -37 | 0.26 | 76 / 94 |
| SMCI | 31.63 | 21 | 7.3 | 5.9 | 23 | 0.32 | 9.5 | -39.7 | 0.6 | 0.00 | 8.8 vs 15.9 | -44 | 0.33 | -21 / -14 |
| Everpure (ex-PSTG, now "P") | 124.01 | 41 | n/a | 29.5 | n/a | n/a | n/a | n/a | n/a | n/a | trailing 170 | n/a | not computed | not computed |

\* gross-debt artefact (finance arm, non-recourse or acquisition debt): see section 5. Everpure: ticker changed from PSTG; Yahoo "P" quote used, other fields not pulled (unverified). Also not tabulated: Carrier (16.6x FY1, 15% growth, 1.8% yield) and Lennox (13.9x, 10% growth): both are mainly building HVAC; I found no verified data-centre revenue share, so they are not data-centre theses. Fabrinet (16.7x FY1, FCF yield -0.4%, off 51%): customer concentration not verified; not pursued.

### Verdict, role, concentration, key bear point

Peers in parentheses are used for relative value. "Conc." = what I found on customer concentration.

| # | Name | Role in chain | Conc. (source) | Key bear point | Verdict |
|---|---|---|---|---|---|
| 1 | **EME** EMCOR | Electrical/mechanical contractor for DC builds | Many customers; RPO $17.14B vs $11.91B a year ago (FACT, Q2 8-K via search). DC share of revenue **unverified** (network and communications revenue +45%) | 10.6% operating margin (thin); a contractor is hostage to hyperscaler build schedules; 24.3x trailing vs 19.7x own median | **START-SMALL** |
| 2 | **VRT** Vertiv | Power + thermal equipment, ~largest pure DC infra | No >=10% customer figure found (**unverified**); 10-K risk factor says large customers are "material" and loss of one "could have an outsized impact" | Q2 revenue slipped on "timing shifts"; Q3 guide needs +40% y/y; beta 2.4, 3y max drawdown -61% | **START-SMALL (gated on Q3 print)** |
| 3 | **HPE** | Servers + Juniper networking | Not disclosed in what I found; AI deals include neoclouds, sovereigns, Oracle (Juniper win) | FY26 EPS +97% is partly acquisition; EV/FCF depends on one-quarter FCF; supply-constrained; trailing P/E 22 vs 7 own median | **START-SMALL (smallest)** |
| 4 | **NRG** | Independent power / retailer | Retail base of millions; hyperscaler 1.2 GW Texas deal "aligned on principal terms", **not final** (FACT, Q2 call summary) | Leverage (3x target pushed from 2028 to 2029), Q2 EPS $1.49 missed $1.66 and "tracking below midpoint", hedges on LS Power assets | **START-SMALL (smallest)** |
| 5 | ETN Eaton | Switchgear, UPS, power distribution | No concentration data found; Electrical Americas DC revenue +~65% (FACT, call summary) | 24x FY1 for 20% growth, 2.0% FCF yield; near highs | WATCH-WITH-TRIGGER |
| 6 | GNRC Generac | Backup gensets for DC | DC backlog ~$1.6B, **second hyperscale customer not yet in backlog**; DC revenue ~$450M of ~$4.4B (about 10%) | Q2 margin helped by a $71M pretax tariff refund (FY0 EPS flattered); home-standby is rate-sensitive | WATCH-WITH-TRIGGER |
| 7 | NVT nVent | Liquid cooling, enclosures, power connections | DC sales ~$2B in 2026 (~35-40% of sales, INFERENCE); concentration **unverified** | Q2 organic sales +47% but organic orders only "low double digits": orders lag sales | WATCH-WITH-TRIGGER |
| 8 | JCI | HVAC/chillers/CDUs | DC "high-teens %" of FY26 sales, to ~1/3 in 3-5 yrs (FACT, call summary); backlog $21.0B +32% | 28.7x FY0, trailing P/E 30.6 vs 20.8 own median, 9% off high | WATCH |
| 9 | HUBB Hubbell | Grid/T&D + DC electrical | Utility-led; Utility book-to-bill ~1.2 H1 | 22.5x for 12% growth; operating margin fell to 20.4% from 22.7%; gross debt/EBITDA 3.4 | WATCH |
| 10 | SBGSY Schneider | Global power/cooling | Diversified | Euro ADR on OTC: **whether IndMoney/Drivewealth can buy it is unverified**; Yahoo data thin (3 analysts) | WATCH (access) |
| 11 | VST Vistra | Independent power | Merchant + contracts; Texas DC "audits" may be delayed (FACT, Q2 call summary) | FY1 EPS growth only 8% after a 4x FY0 jump; FCF ~0; ~3x leverage | WATCH |
| 12 | CLS Celestica | Hyperscale switch/server ODM | **3 customers 32%/14%/12% of FY25; Q4 36%/15%/12%** (call; 10-K note not read) | 12% gross margin; FY1 EPS +73% must happen; PEG looks tiny because of concentration | WATCH-WITH-TRIGGER |
| 13 | MOD Modine | DC cooling | **One hyperscaler agreement takes ~half of capacity FY27-29** (FACT, release summary) | FCF -0.9% yield, supply snags cut DC margin to 14.8%, 54% off high | WATCH-WITH-TRIGGER |
| 14 | COHR Coherent | Optical transceivers/lasers | Top two customers 20% and 12% (secondary) | FCF about -$650M TTM (capex); optics stocks falling on rotation | WATCH-WITH-TRIGGER |
| 15 | DELL | AI servers | AI backlog $95B; Q2 AI orders $60.9B in one quarter (FACT, release summary); customer concentration **not disclosed in what I found** | FY1 EPS growth +4% after FY0 +151%: peak-earnings risk; trailing P/E 24.6 vs 12.2 own median | WATCH-WITH-TRIGGER |
| 16 | TLN Talen | Independent power | ~2 GW AWS contract; ~4 GW DC sites (FACT, Q2 call summary): one-counterparty reliance | Gross debt/TTM EBITDA 16x (TTM understates after the Cornerstone deal); GAAP net loss in Q2 | WATCH-WITH-TRIGGER |
| 17 | CEG | Nuclear/IPP | Long-term nuclear contracts, ~1 GW signed in Q2; Amazon 190 MW (FACT, call summary) | FCF -6.9% yield (Calpine, buybacks), 22x for 10% growth | WATCH |
| 18 | NTAP | Enterprise storage | Hyperscaler share **not found**; mostly enterprise | Trailing P/E 25 vs 13.7 own median; FY27 revenue guide +~10% | WATCH |
| 19 | POWL Powell | Switchgear | **One DC award >$400M = ~43% of $934M Q3 orders** (FACT, release summary) | 30.8x FY0 for +8% growth; 50% off high | WATCH |
| 20 | TT Trane | Chillers/HVAC | DC part of "broad-based" strength; backlog $12.1B +70% | 30x FY0, near highs | WATCH |
| 21 | FIX Comfort Systems | Mechanical contractor | Concentration unverified | 29x FY0, trailing 35 vs 24.5 median | AVOID at price |
| 22 | AAON | Cooling units | **3 customers each >=10% of 2025 revenue** (10-K, via search) | FCF yield -3.5% | AVOID |
| 23 | SMCI | AI servers | n/a | FCF yield -39.7%; 11% gross margin; (from memory, unverified in this session: auditor resignation and DOJ probe in 2024) | AVOID (value trap) |
| 24 | Everpure (P) | Flash storage | Meta dependence (from memory, **unverified**) | 29.5x FY1, trailing 170x | AVOID |

### Priced for perfection (all AVOID at current price)
| Name | Why |
|---|---|
| Bloom Energy | 44.8x FY1, EV/EBITDA 156, EV/sales 21; **two customers 44% and 21% of Q2 revenue** (10-Q, one a related party); needs ~76% EPS growth a year for 3 years to earn 10%/yr at a 20x exit |
| Lumentum | EV/sales 24, EV/EBITDA 91; **two customers 26.6% + 15.0% = 41.6%** (secondary); trailing P/E 98 vs own median 26 |
| Credo | EV/sales 19.6; **three end-customers 33/32/19% = 84% of FY26 revenue** (secondary reading of 10-K); expects 3-4 customers >10% to persist |
| Arista | 43x FY0 / 34x FY1, EV/EBITDA 45, EV/sales 20; **two customers ~26% and ~16% of 2025 revenue** (secondary; customers unnamed in 10-K) |
| Ciena | 46x FY0 / 32x FY1; **hyperscaler-linked revenue 53% of FQ3** (FACT, call summary), backlog $8.5B but needs 46%/yr EPS growth for a 10% return at 20x |
| Corning | 40x FY0, trailing 46 vs own median 18.8 (+144%); Springboard plan and an Amazon supply deal (FACT, release) already in the price |
| GE Vernova | EV/EBITDA 60; Yahoo shows FY1 EPS **below** FY0 (24.5 vs 30.4; the FY0 figure probably includes one-offs: unverified), so 37.6x FY1; slot reservations are not take-or-pay (lab finding on TD Power / GE gas pipeline) |
| Quanta | 37.7x FY0 / 31.8x FY1, trailing 47 vs 32 median; backlog $53.4B is real, but "technology and data centre" is only ~15-20% of the business, so you pay a DC multiple for a utility-services business |

## 2. How much growth is already priced in (arithmetic)

Method: price today P; assume 20x or 15x exit P/E in 3 years and a 10%/yr required return. Required FY+3 EPS = P x 1.331 / exit multiple. Compare the implied EPS growth with consensus FY1 growth. Source of EPS: Yahoo consensus (unverified, checked against guidance above).

- **EME:** $721.66 x 1.331 / 20 = $48.0 EPS needed in ~3 years vs FY0 $32.99: 13.3%/yr (FY1 consensus growth 13.3%). Price therefore assumes growth just continues; it is neither cheap nor stretched (INFERENCE). At a 15x exit it needs 25%/yr.
- **VRT:** $206.42 x 1.331 / 20 = $13.74 vs FY0 $6.74: 26.8%/yr vs consensus 36% for FY1 and FY26 guidance +31% organic (FACT, guide). Margin of safety if growth decays gently; thin if the 20x exit is too generous.
- **HPE:** at 20x exit price already assumes EPS can fall 1%/yr; at 15x it needs 8.5%/yr vs consensus +23% FY1 and FY27 revenue guide +13-17% (FACT, release summary). The low hurdle is the main argument for HPE. The counter-argument: a 15x exit for a hardware company with 12-14% operating margin (INFERENCE) is not conservative.
- **NRG:** at 15x needs 1.6%/yr; at 9.3x FY1 P/E it is priced for earnings to fall. FY1 EPS +27% is partly the full-year LS Power effect (FACT: LS Power drove Q2 EBITDA), not organic growth, and the company says 2026 is tracking below the midpoint of $7.90-9.90 (call summary).
- **ETN / JCI / TT / PWR:** need 24-26% / 24% / 26% / 36% EPS growth a year to earn 10% at 20x. They are priced for the growth to continue for 3+ years, i.e. fair-to-full, with Quanta full.
- **ANET, CIEN, GLW, BE, LITE:** required EPS CAGRs of 42%, 46%, 39%, 76%, 36% at a 20x exit. Consensus FY1 growth is 27%, 44%, 33%, 82%, 65%, so the higher growth ones (BE, LITE) are "priced for perfection" in the literal sense: only an unbroken 3-year hypergrowth earns 10%.
- Caveat (INFERENCE): FY1 growth is a 1-year number; consensus beyond FY1 was not obtainable, so "required vs consensus" is a sanity check, not a forecast.

## 3. START-SMALL names: thesis, entry, sizing, kill triggers

Sizing tiers are % of net worth (new-money amount unknown). Loss maths: position weight x drawdown = pp of net worth. Drawdown evidence from lab data (analysis/stock_ideas/out/dd_inputs.csv): QQQ -35%, SMH -45% (2021-11 to 2022-12), SMH worst -64%, NVDA -66%, MU -50% in the same window. Our own 3y worst drawdowns: VRT -61%, EME -36%, HPE -48%, NRG -48%.

### 3.1 EMCOR (EME) - rank 1
- **Business:** largest US electrical and mechanical contractor; builds the power, cooling and network systems inside data centres, plus hospitals, water, industrial.
- **Thesis (INFERENCE):** RPO $17.14B (+44% y/y, FACT) covers ~10 months of 2026 revenue guidance ($20.0-20.5B, raised from $18.5-19.25B, FACT); EPS guide raised to $32.00-33.25 from $28.25-29.75 (FACT). Net cash. Many project customers, so no single hyperscaler can sink it. 19.3x FY1 vs Fix 23.9x and Quanta 31.8x (same labour/electrical build-out exposure).
- **Priced in:** 21.9x FY0, trailing 24.3x vs own 5y median 19.7x (+24%); 24% off its high; 3.1% FCF yield; needs 13%/yr EPS growth for 10%/yr at 20x.
- **Bear points:** (1) thin 10.6% operating margin: a project slip or wage inflation hits EPS hard; (2) the beat-and-raise cadence has already lifted the multiple above its median; (3) data-centre share of revenue is unverified, and the build cycle (power availability, interconnect queues) can push work right.
- **Entry:** T1 (1/3) now to $740 (<= ~19.8x FY1). T2 (1/3) after the Q3 print (consensus date 29 Oct, Yahoo, unverified) if RPO is >= $17.1B and 2026 EPS guide holds. T3 (1/3) at <= $650 (17.4x FY1) or after two further clean quarters. Wait for: the print, not a dip.
- **Accumulate on:** RPO up q/q and book-to-bill > 1; FY1 EPS revisions flat or up. Do not average down on a falling backlog.
- **Kill / thesis-break:** RPO falls q/q for two quarters; operating margin < 9.5% (Q2 10.6%); FY1 consensus cut > 10%; management says hyperscaler schedules slip.
- **Trim:** >= 24x FY1 (~$897 on today's EPS) or position > 1.5% of net worth. **Cap:** 1.0% of net worth. Worst case at -40%: 0.40 pp of net worth.
- **Model-estimate odds (12m):** P(+30%) ~25%; P(touch -25%) ~47%.

### 3.2 Vertiv (VRT) - rank 2, gated on the Q3 print
- **Business:** power (UPS, switchgear, busway), thermal (chillers, liquid cooling CDUs) and services for data centres; FY25 net sales $10.23B, 62% Americas (FACT, 10-K).
- **Thesis:** FY26 guide $14.0B sales (+31% organic), adj EPS $6.70, raised in Q2 (FACT, release); Q3 guide $3.65-3.85B sales (~+40% y/y), adj EPS $1.77-1.83, 24.5% op margin (FACT, release summary); backlog $15.0B at Dec 2025, +109%, book-to-bill ~2.9x (secondary; the TIKR "binding POs" wording is the blog's own). Net debt about $1.1-1.2B at Dec 2025 (derived from 10-K debt $2.93B vs cash $1.73B+$0.10B ST investments), ~0.1x on Yahoo TTM figures.
- **Priced in:** 30.6x FY0 / 22.5x FY1 vs Eaton 24.0x, nVent 21.1x, Schneider 19.9x; trailing 39x vs own median 37x (about fair vs itself); 46% below its $379.93 high and -29% in 3 months (FACT: Marketbeat on gap-downs 14 Sep and later; Q2 "revenue timing" miss). Needs 27%/yr EPS growth at a 20x exit.
- **Bear points:** (1) highest AI co-movement in the list (corr 0.46 to the six holdings, 0.65 in their worst 10% days; beta 2.4); (2) a second consecutive "timing" slip would confirm that supply or site-readiness, not demand, limits revenue; (3) customer concentration undisclosed in what I found, while the 10-K itself warns of "outsized impact" from losing one large customer.
- **Entry:** do not buy before the Q3 print (dates conflict: 21 Oct by Yahoo-quoted sources, 28 Oct by Yahoo calendar and Trefis). T1 (1/3) after the print if Q3 sales are within or above $3.65-3.85B and the FY guide is held, at <= $220 (24x FY1). T2 (1/3) at <= $184 (20x FY1) or after the Q4 print (Feb). T3 only if backlog or orders disclosed grow faster than sales.
- **Accumulate on:** organic orders > organic sales growth (book-to-bill > 1); op margin >= 22.5%.
- **Kill:** Q3 sales below $3.65B or FY26 guide cut; backlog flat/down q/q; adjusted op margin < 22%; a named hyperscaler cuts 2027 capex guidance.
- **Trim:** >= 30x FY1 (~$276) or > 1.5% of net worth. **Cap:** 1.0%. Worst case at -60% (3y worst -61%): 0.60 pp.
- **Odds:** P(+30%) ~27%; P(touch -25%) ~65% (realised vol 63%).

### 3.3 HPE - rank 3 (smallest)
- **Business:** servers (incl. AI systems), networking (Juniper, acquired), storage, financing arm.
- **Thesis:** FQ3 (Jul-26) revenue $12.2B +34%, networking $2.9B +~75%, record orders and backlog, supply-constrained; FY26 revenue growth 34-37% then FY27 +13-17% (FACT, release summary); at least 75% of FCF returned in Q4; Juniper/Oracle AI data-centre networking win.
- **Priced in:** 14.4x FY0 / 11.7x FY1 (Dell 16.9x, NetApp 18.3x, Cisco n/a); FCF yield 6.5% (Yahoo TTM; one quarter's FCF was $1.0B, so check annualisation: unverified); dividend 1.0%; 25% off high; but trailing 22x vs own 5y median 7x, i.e. the market has re-rated it 3x on a depressed EPS base (INFERENCE). At a 20x exit the price embeds -1%/yr EPS; at 15x, +8.5%/yr.
- **Bear points:** (1) FY26 EPS +97% includes acquisition and base effects; the organic run-rate is lower; (2) supply constraints (memory) and low AI-server margins can cap profit conversion; (3) Yahoo shows 2.0x debt/EBITDA but that includes the financing arm (unverified true figure), and 3y max drawdown is -48%.
- **Entry:** T1 (1/3) <= $56 (11.9x FY1). T2 (1/3) after FQ4 results and FY27 guide (early Dec, date unverified) if guide revenue >= +13% and FCF guide is stated. T3 at <= $48 (10x FY1).
- **Kill:** FY27 revenue guide < +10%; FCF guide cut; networking growth turns negative q/q; net debt rising while orders fall.
- **Trim:** >= $70 (near the 71.7 Yahoo mean target, ~15x FY1) or > 1.0% of net worth. **Cap:** 0.75%. Worst case at -50%: 0.38 pp.
- **Odds:** P(+30%) ~27%; P(touch -25%) ~55%.

### 3.4 NRG Energy - rank 4 (smallest; the only non-equipment name)
- **Business:** retail electricity + large generation fleet (Texas, East after LS Power).
- **Thesis:** Adj EBITDA ~$1.2B in Q2 (+34%, LS Power); 2026 guide EBITDA $5.325-5.825B, FCF before growth $2.8-3.3B (FACT, call summary), i.e. 13-15% of a $21.8B market cap on the company's own definition (INFERENCE, non-GAAP); ≥$1B buybacks and $407M dividends planned; 1.2 GW Texas CCGT with an investment-grade hyperscaler, ≥$500M annual EBITDA at ~$3.2B cost, late 2029 (terms not final). Hyperscaler optionality, but earnings do not depend on it.
- **Priced in:** 11.8x FY0 / 9.3x FY1 vs Vistra 14.7x, Constellation 20.4x, Talen 11.4x; EV/EBITDA 14.1 (gross debt basis); dividend 1.8%; 45% off high, -39% 1y. Price assumes flat-to-falling EPS.
- **Bear points:** (1) leverage: net-leverage target pushed from 2028 to 2029, Yahoo gross debt/EBITDA 7.2x (includes non-recourse; true corporate figure unverified); (2) Q2 EPS missed ($1.49 vs $1.66) and management says tracking below midpoint; Texas EBITDA fell $131M on weaker load/prices; (3) policy risk: FERC/PJM co-location rules still unsettled (FERC order 18 Dec 2025; paper hearing outcome not confirmed), rates at 5.2% on a debt-funded growth story.
- **Entry:** T1 (1/3) <= $105. T2 (1/3) after Q3 results (consensus 5 Nov, unverified) if guidance is reaffirmed and the hyperscaler deal is signed. T3 <= $90 (8.1x FY1).
- **Kill:** 2026 adj EBITDA guide cut below $5.325B; leverage target slips beyond 2029; hyperscaler deal abandoned and capex stays committed; a PJM/ERCOT rule change that voids co-location economics.
- **Trim:** >= $145 (13x FY1) or > 1.0% of net worth. **Cap:** 0.75%. Worst case at -50%: 0.38 pp.
- **Odds:** P(+30%) ~27%; P(touch -25%) ~54%.

### 3.5 Basket cap and fit
All four together: 3.5% of net worth. If all fall 50%: 1.75 pp of net worth; with VRT -60%, EME -40%, HPE -50%, NRG -50%: 0.60+0.40+0.38+0.38 = 1.76 pp. Count VRT 100% and EME/HPE/NRG ~50% toward the AI-theme cap (their 6-stock correlation is 0.32-0.46 and they have non-AI revenue), so the AI look-through rises by ~2.0 pp, from ~31% to ~33%, unless funded from a trim of an existing AI position (INFERENCE). Staging all four over 3 tranches and 2-3 months; the lab found timing states carry no return edge, so staging is for risk (event dates), not for return.

## 4. Correlation and tail check (3y daily, to 2026-10-16)

| Name | Corr to 6-stock AI basket | Same, in basket's worst 10% days | Avg own return on those days % (basket -3.19%) | Ann. vol | Model P(touch -25% in 12m)* | Model P(+30% at 12m)** |
|---|---|---|---|---|---|---|
| VRT | 0.68 | 0.65 | -5.2 | 0.63 | 65% | 27% |
| ETN | 0.69 | 0.66 | -2.8 | 0.35 | 41% | 24% |
| NVT | 0.64 | 0.50 | -3.1 | 0.42 | 49% | 26% |
| CLS | 0.63 | 0.59 | -5.3 | 0.69 | 68% | 27% |
| EME | 0.58 | 0.61 | -2.5 | 0.39 | 47% | 25% |
| PWR | 0.58 | 0.57 | -2.7 | 0.39 | 46% | 25% |
| HPE | 0.47 | 0.52 | -2.7 | 0.48 | 55% | 27% |
| NRG | 0.49 | 0.56 | -2.7 | 0.47 | 54% | 27% |
| VST | 0.53 | 0.67 | -3.7 | 0.57 | 61% | 27% |
| CEG | 0.47 | 0.65 | -3.5 | 0.54 | 59% | 27% |
| JCI | 0.49 | 0.53 | -1.7 | 0.29 | 32% | 22% |
| HUBB | 0.55 | 0.44 | -2.1 | 0.31 | 35% | 23% |
| GNRC | 0.39 | 0.21 | -2.6 | 0.47 | 54% | 27% |
| DELL | 0.51 | 0.57 | -3.6 | 0.63 | 65% | 27% |

(The 0.26-0.47 numbers in section 1 are the average of the six pairwise correlations; this table uses the equal-weight basket, which gives higher figures.) *Zero-drift lognormal barrier at realised 3y vol: 2 x N(ln 0.75 / sigma). **Lognormal with 8% assumed annual drift. Both are crude model estimates, not forecasts; realised vol includes the 2024-26 AI boom and may overstate or understate future vol. Reading: every name has a better-than-one-in-three chance of touching the investor's -25% line within a year, and in AI sell-offs these stocks fall with the basket (VRT and CLS fall more than the basket on its worst days, -5.2% and -5.3% vs -3.2%). Lowest co-movement in a crash: GNRC (0.21), HUBB (0.44), NVT (0.50).

## 5. Data-centre-specific risks (and how each name is exposed)

| Risk | Evidence / mechanism | Most exposed | Least exposed |
|---|---|---|---|
| Power-grid constraints | PJM 2027/28 auction cleared 6,623 MW short of the reliability requirement, ~5,100 MW attributed to AI load (FACT, search summary); GE Vernova slots reach 2031; Texas DC "audits" may delay load (Vistra call) | Contractors and equipment makers whose revenue depends on energisation dates (EME, FIX, VRT, MOD) | IPPs benefit from scarcity (NRG, VST, TLN) until regulators cap it |
| Customer concentration | Section 1 table: 2-3 customers = 40-84% at BE, CRDO, LITE, ANET, CLS, AAON | CLS, CRDO, LITE, BE, ANET, AAON, MOD | EME, ETN, HUBB, JCI, TT, NRG |
| Financing / debt | Hyperscaler debt funded 32% of capex LTM; ~$820B lease commitments; S&P cut Oracle to BBB- (9 Jul) (FACT, lab report F, FactSet/secondary) | Suppliers to Oracle, neoclouds, OpenAI-linked builds (DELL, SMCI, HPE partly) | Utility-grid exposed names (HUBB, PWR) |
| Lease cancellations / overbuild | Cancellations show up first in orders and RPO, then in revenue 2-4 quarters later (INFERENCE) | Order-lumpy: POWL (one >$400M award), NVT (orders lag sales), MOD | Backlog-heavy diversified: JCI, TT |
| Obsolescence | GPU life 5-6y vs 3-4y scenario; PP&E $434B bought vs ~$149B depreciation (secondary, lab report F) | AI-server OEMs with peak margins: DELL, SMCI | Power/thermal gear has longer life: VRT, ETN |
| Interest rates | 10y 5.2%, real 2.87% (+110bp y/y); Fed hiking, next FOMC 27-28 Oct (FACT, FRED/Fed, lab report F) | Levered/long-duration: NRG, TLN, VST, CEG, high-multiple optics | Net-cash: EME, ANET, POWL |
| Regulation (IPPs) | FERC co-location order (18 Dec 2025) with the final tariff terms not confirmed by me | TLN, VST, CEG, NRG | Equipment makers |
| Supply chain / tariffs | Modine: key-component shortages; nVent: tariff cost ~$100M; HPE/Dell: memory constraints | MOD, NVT, HPE, DELL | EME |

## 6. What would make this whole thesis wrong

1. A hyperscaler capex guide-down or a visible slowdown in orders (not just revenue) at Vertiv, nVent, Eaton or Dell in the October-November prints: backlogs convert to revenue only if sites get power and customers keep paying.
2. Nvidia's report on 19 Nov (FACT per lab report F) showing sequential deceleration, or any large AI customer (OpenAI/Oracle-linked) failing to fund a build.
3. The 10y yield moving above ~5.75% or the Fed hiking again on 27-28 Oct / 8-9 Dec: this hits multiples on all of these and IPP leverage first.
4. Consensus FY1 EPS being a peak: DELL FY1 growth is +4% after +151%, and the industrial names' 20-35% FY1 growth is guided from a single up-cycle (SOX -16.6% from the June high already hints the market is discounting peak growth: SPECULATION).
5. Policy: FERC/PJM or Texas rules that block co-location or add large-load costs, hitting IPP contract economics.
6. The lab's own evidence: momentum rank is the only selector with edge; trend filters protect but do not find multi-baggers; 5x outcomes are rare. None of these names is a multi-bagger candidate: all of them are valuation-and-growth ideas with a plausible range of +30% to -30% over 12 months. Backtest returns are survivor-inflated.

## 7. Catalyst calendar (Yahoo estimates unless stated; dates unverified until the company confirms)

| Date | Event |
|---|---|
| Oct 21-28 | Vertiv Q3 (sources conflict: 21 vs 28 Oct) |
| Oct 22 | Bloom, Comfort Systems |
| Oct 26-30 | Celestica, Hubbell, Modine, JCI, Corning, GNRC, Generac, Trane, EME, Quanta, GE Vernova (28), nVent (30) |
| Oct 27-28 | FOMC (FACT, lab report F) |
| Nov 2-9 | Eaton (3), Arista (3), Super Micro (3), Talen (3), Coherent (4), Lumentum (5), NRG (5), Vistra (6), Constellation (9) |
| Nov 17 | Powell |
| Nov 19 | Nvidia (FACT, lab report F) |
| Nov 27 | Dell |
| Early Dec | HPE FQ4 and FY27 guide; NetApp (1 Dec) |
| 8-9 Dec | FOMC with projections (FACT, lab report F) |

## 8. Tax, employer and access flags (verify with CA/HR)

- Not verified in this session: current Indian tax treatment of US-share gains (holding-period threshold and rate), US dividend withholding for Indian residents (W-8BEN rate), and any LRS/TCS limits on funding. Verify with a CA.
- Employer (BNY) trading restrictions are unknown to me; buying tech-infrastructure names unrelated to the employer is unlikely to be restricted, but check pre-clearance and blackout rules with HR.
- Schneider ADR (SBGSY) is OTC; whether the investor's US broker route supports it is unverified. Everpure's ticker changed (PSTG to "P", per a German site and Yahoo; NYSE notice not seen).

## 9. Honest summary of confidence

- Highest confidence: that Bloom, Lumentum, Credo, Arista, Ciena, Corning, Quanta and GE Vernova are priced for continued hypergrowth (their required-CAGR numbers are 36-76%/yr at a 20x exit) and that CLS/CRDO/LITE/BE/ANET/AAON are concentrated (customer percentages are disclosed, via secondary reading).
- Medium: that EME, VRT, HPE and NRG are the better valuation-for-growth trades among the diversified-customer names; this rests on Yahoo consensus (cross-checked to guidance) and on customer-concentration data I could not fully verify for VRT, HPE, EME's data-centre share, Dell and nVent.
- Low: any statement about margins, true leverage (HPE, NRG, VST, TLN, CEG) and company-defined FCF; they come from aggregators and call summaries.
- Next steps if the investor wants conviction: read the VRT, EME, HPE and NRG 10-Q customer-concentration notes and debt notes; re-run this table after the late-October prints.
