# 09 - Actively managed funds with a named, verifiable manager (as of 2026-10-09)

Research support, not personal advice; the investor decides. No orders were placed or prepared. Follows `00_decision_memo.md`, `04_sectors.md`, `07_sector_funds.md`, `08_windmill_trackers.md`. Sector view used: autos fair/leaning cheap; power/grid improving; private banks cheap and improving; FMCG fair; NBFCs fair/leaning cheap; avoid pharma, metals, realty; IT cheap for a reason. Profile: Zerodha (Coin, Direct plans), about Rs 1 lakh staged over about 5 months, optional SIP up to Rs 15,000 a month, loss limit 25% of money invested.

## 1. Bottom line

1. **Most long records in this space no longer belong to the person running the fund.** Of the 18 funds shortlisted, 9 have a lead manager who took over after the start of the 3- or 5-year window that the fund advertises: ICICI Infrastructure (manager left 15 Jun 2026), Invesco Infrastructure (co-manager left Invesco 25 Nov 2025), Nippon Power & Infra (Aug 2024), SBI PSU (Jun 2024), HDFC Value (Feb 2024), HDFC Flexi Cap (Feb 2026), ICICI Energy Opportunities (the launch manager, Sankaran Naren, left 1 Nov 2025), Kotak Infrastructure (Oct 2023, only 3 of 5 years) and ICICI Transportation & Logistics (both launch managers left Sep 2023). Section 5 re-computes each record for the current manager only.
2. **Only four funds combine a manager who has run the same fund for 6+ years with returns that beat a sector proxy over that tenure:** Tata India Consumer (Sonam Udasi, since 1 Apr 2016), Nippon India Multi Cap (Sailesh Raj Bhan, AMC lists "since March 2005"), SBI Banking & Financial Services (Milind Agrawal, since Aug 2019) and Invesco India Financial Services (Hiten Jain, since 19 May 2020). The fifth long tenure, UTI Transportation & Logistics (Sachin Trivedi, since Sep 2016), has returned 11.8% a year under him against 11.4% for the Nifty 50 ETF: index-like, not skill.
3. **Autos: keep the ICICI Prudential Nifty Auto Index Fund (Direct) as the core.** Two active funds beat it by 6 to 9 points a year over 2.3 to 3.1 years (HDFC Transportation & Logistics, Priya Ranjan, with a shallower worst fall of -23.5% against -28.3%; SBI Automotive Opportunities, Tanmaya Desai, -29.2%). But both are new, have never faced more than the Sep 2024 to Apr 2025 fall, cost 0.9 to 1.0% against 0.25%, and most of their lead came from one stretch: calendar 2026 to date, when the Nifty Auto proxy fell 12.3% and they did not (in 2025 both lagged it). At most a small satellite.
4. **Power/grid: no active fund is a clean match.** ICICI Prudential Energy Opportunities is the only credible substitute for the Windmill Energy Tracker (1y +8.6% against -10.9%, no tax events for you), but it is 34% oil and gas and 34% capital goods, turns its portfolio over 1.65 times a year, and its headline manager has left.
5. **Verdict:** Tata India Consumer is the one fund that clearly earns a place on named-manager evidence, in a consumption slot. Invesco India Financial Services (or SBI BFSI) is a second-tier banking option that duplicates existing financials exposure. HDFC Transportation & Logistics and ICICI Energy Opportunities earn a conditional, small place for autos and power. Nippon India Multi Cap is the best-verified diversified alternative. Infrastructure, manufacturing, PSU, business-cycle, value and flexi-cap funds do not earn a place now. Details in sections 8 and 9.
6. **Regulatory:** nothing adverse found on the shortlisted AMCs after 2024 apart from small settlements, one Nippon order disclosed in Feb 2025 whose charges I did not read, and one Supreme Court ruling (Kotak, Jul 2026, 2021-22 debt-fund matter). The Axis Mutual Fund front-running case ended in a SEBI final order on its former chief dealer (24 Jul 2026, per press). I excluded all quant Mutual Fund schemes because of the reported front-running probe and settlement application (no SEBI order found). None of 25 manager names appears in the title of a SEBI order, but the SEBI search matches titles only. Section 7.

## 2. Method, sources, and how far to trust each number

| Tag | Source | Date | Trust |
|---|---|---|---|
| [F] | AMC factsheets or one-pagers, read as text: ICICI Pru scheme PDFs (31 Aug 2026), HDFC MF factsheet Aug 2026, SBI all-scheme factsheet Aug 2026, Nippon India factsheet Sep 2026 (data 31 Aug), Tata MF factsheet Aug 2026, Invesco factsheet Aug 2026, Kotak one-pagers (data 31 Jul 2026) and Kotak web factsheet pages (Aug 2026), Kotak "About our fund managers" page | Jul to Sep 2026 | Primary |
| [N] | AMFI daily NAV file `portal.amfiindia.com/spages/NAVAll.txt` (NAV date 8 Oct 2026; used to find ISINs, plans and codes) plus daily NAV history from the free `api.mfapi.in` mirror of AMFI data. Direct Growth only. My arithmetic. Split-adjusted (see below) | to 8 Oct 2026 | Primary data, my calculation. My 1/3/5-year figures matched Coin's displayed returns to within about 0.1 point on every fund I spot-checked |
| [S] | SEBI orders pages (`sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=2&ssid=9&smid=N`) and its keyword search endpoint | to 8 Oct 2026 | Primary, titles only (see section 7) |
| [C] | Zerodha Coin fund page | 8 Oct 2026 | Broker display of vendor data. Shows one manager, no tenure, "BER" not "TER" |
| [P] | Reputable press (Business Standard, BusinessToday, Moneylife, LiveLaw, Value Research, Reuters via Yahoo) | various | Secondary |
| [A] | Aggregator or search-engine summary (Sharpely, Anand Rathi, Groww, Business Today fund pages, INDmoney) | various | **Do not rely.** Marked wherever used |

How the numbers were built:
- **Universe.** The AMFI file of 8 Oct 2026 lists 222 Direct Growth sectoral/thematic schemes plus 39 flexi cap, 29 multi cap, 22 value, 4 contra and 10 dividend-yield schemes. I pulled NAV history for about 105 of them and screened on sector fit, record length, drawdown and rolling returns, then kept 18 where I could also obtain an AMC document naming the manager and tenure. Schemes with 2.6 years of history or less (SBI, Kotak and Baroda BNP energy funds, Kotak Transportation & Logistics, HDFC Manufacturing, Invesco Business Cycle, Abakkus Flexi Cap) were dropped from the 18.
- **Split adjustment.** Single-day NAV falls of 85% or more were treated as unit splits (Nippon Nifty 50, Bank and PSU Bank BeES on 23 Dec 2019; ICICI Nifty FMCG ETF on 13 May 2024) and earlier values were scaled. Falls of 12% to 17% on 23 Mar 2020 and 4 Jun 2024 were real market falls and left alone.
- **Benchmark proxies (important).** I could not get TRI history (niftyindices returned errors in file 07). I used the Direct NAV of index funds and ETFs as proxies: Nifty Auto = Nippon Nifty Auto ETF (from Jan 2022); Nifty Infrastructure = Nippon Infrastructure BeES (from Nov 2016); Nifty Bank = Nippon Bank BeES; Nifty India Consumption = Nippon Consumption ETF (from Apr 2014); Nifty CPSE = CPSE ETF (not the BSE PSU index the funds use); Nifty India Manufacturing = Navi index fund (from Aug 2022); Nifty 500 = Motilal Oswal Nifty 500 Index Fund (from Sep 2019); Nifty 50 = Nippon Nifty 50 BeES. These are net of fund costs, so they understate their TRI by roughly 0.2 to 0.6 points a year (tracking differences in file 07). There is **no proxy** for the Nifty Transportation & Logistics TRI, Nifty Energy TRI (history starts Oct 2025), BSE PSU TRI, BSE India Infrastructure TRI or Nifty Financial Services TRI; the nearest proxy is used and labelled. AMC-printed benchmark figures at 31 Aug 2026 are shown separately in section 4.1.
- **Rolling-return bias.** "Beat Nifty 500" in rolling tables only covers windows that start after Sep 2019, so it is flattered by the post-2020 rally. The sector-proxy comparison uses a longer window where the proxy exists.
- **"Since launch".** For funds older than 2013 the AMFI data starts with the Direct plan in Jan 2013, so "since launch" means since Jan 2013. AMC-printed since-inception figures are in section 4.1.
- **Costs.** Under the SEBI (Mutual Funds) Regulations 2026 AMCs now print a Base Expense Ratio (BER) that excludes brokerage and transaction costs. Where the AMC prints both, TER is higher: SBI BFSI 1.20% against BER 0.68%; SBI Automotive 0.99% against 0.71%; SBI PSU 0.91% against 0.72%. Coin shows BER. Compare funds on TER where printed.
- **Tax** (unchanged from file 07, secondary sources only): equity-oriented funds, gains within 12 months 20%, after 12 months 12.5% above Rs 1.25 lakh a year across all equity gains. Each staged tranche has its own 12-month clock.

## 3. The shortlist (18 funds)

Numbering F1 to F18 is used in all tables. "Dir" = Direct Growth. AUM in Rs crore.

### 3.1 People: who runs each fund, since when, and who ran it before

| # | Fund (AMC; SEBI category) | Named manager(s) and tenure on THIS fund | Other funds they run / background | Previous manager(s) of this fund | Source |
|---|---|---|---|---|---|
| F1 | SBI Automotive Opportunities Fund (SBI Funds Management; Thematic) | Tanmaya Desai, 17 yrs experience, since Jun 2024 (inception 7 Jun 2024) | SBI Healthcare Opportunities (since Jun 2011), SBI MNC Fund | None (new fund) | [F] SBI Aug 2026 |
| F2 | ICICI Prudential Transportation & Logistics Fund (ICICI Pru AMC; Thematic) | Rajat Chandak (18 yrs) and Priyanka Khandelwal (12 yrs), both since Sep 2023 (w.e.f. 18 Sep 2023) | Chandak runs 5 schemes (4 jointly), Khandelwal 4; overseas sleeve: Sharmila D'Silva | Harish Bihani and Sharmila D'Silva, inception 28 Oct 2022 to 18 Sep 2023 | [F] ICICI Aug 2026 |
| F3 | HDFC Transportation and Logistics Fund (HDFC AMC; Thematic) | Priya Ranjan, 18+ yrs, since 17 Aug 2023 (inception). Gold/silver sleeve: Bhagyesh Kagalkar from 26 Aug 2026. Overseas: Dhruv Muchhal (to 31 Aug 2026), Gopal Agrawal from 1 Sep 2026 | Also co-manages HDFC Defence Fund. HDFC notice (via search summary [A]): joined HDFC AMC as Senior Equity Analyst on 17 Nov 2020, so this is a first lead-manager role | None (new fund) | [F] HDFC Aug 2026 |
| F4 | UTI Transportation and Logistic Fund (UTI AMC; Sectoral/Thematic) | Sachin Trivedi, since Sep 2016 | At UTI since 2001; heads equity research [A]. UTI factsheet for 2026 not obtained | n/v | [A]/UTI presentation Jul 2022 via search summary. **Not confirmed from a 2026 AMC document** |
| F5 | ICICI Prudential Energy Opportunities Fund (ICICI Pru AMC; Thematic) | Nitya Mishra (14 yrs; the same factsheet says "since July 2024" in the scheme box and "since Nov 2024" in the note), Priyanka Khandelwal (Jul 2024), Sharmila D'Silva (Jul 2024) | Mishra runs 6 schemes (5 jointly) | **Sankaran Naren ceased w.e.f. 1 Nov 2025** | [F] ICICI Aug 2026 |
| F6 | Nippon India Power & Infra Fund (Nippon Life India AMC; Sectoral) | Rahul Modi, 20 yrs, since Aug 2024; his only scheme | None other | Not named on the AMC pages read; Business Today fund pages list Sanjay Doshi as lead from Jan 2017 [A] | [F] Nippon Sep 2026 |
| F7 | ICICI Prudential Infrastructure Fund (ICICI Pru AMC; Thematic) | Sanket Gaidhani, ~10 yrs. Factsheet says "since July 2026" in the note and "June, 2026" in the box | Manages 2 schemes | **Ihab Dalwai ceased w.e.f. 15 Jun 2026** | [F] ICICI Aug 2026 |
| F8 | Kotak Infrastructure & Economic Reform Fund (Kotak Mahindra AMC; Thematic) | Nalin Rasik Bhatt, 20 yrs, since 1 Oct 2023 | Also Kotak Transportation & Logistics (with Abhishek Bisen, since 16 Dec 2024). Earlier: Motilal Oswal Securities, Angel Broking, Sushil Stock Brokers | Not named in pages read | [F] Kotak "About our fund managers" Aug 2026 |
| F9 | Invesco India Infrastructure Fund (Invesco AMC; Thematic) | Sagar Gandhi, 16 yrs, since 1 Mar 2025 (co-manager with Amit Nigam until Nov 2025, then sole) | Also co-manages Invesco PSU Equity (with Hiten Jain, since 1 Jul 2025) | Amit Nigam, sole manager before 1 Mar 2025 and co-manager to 25 Nov 2025, when he left Invesco [P] Value Research | [F] Invesco Aug 2026; [P] |
| F10 | Kotak Manufacture in India Fund (Kotak AMC; Thematic) | Harsha Upadhyaya (20+ yrs) since 1 Oct 2023; Abhishek Bisen since 22 Feb 2022 (inception) | Upadhyaya also runs Kotak Flexi Cap and Large & Mid Cap (both since Aug 2012), ELSS (Aug 2015), Quant, MNC (co). Earlier: DSP BlackRock, UTI AMC, Reliance Group, SG Asia. Kotak lists Bisen against 83 funds | Harish Krishnan with Bisen until 30 Sep 2023 [P] Value Research | [F] Kotak Aug 2026; [P] |
| F11 | Invesco India Financial Services Fund (Invesco AMC; Sectoral) | Hiten Jain, 17 yrs, since 19 May 2020; Haresh Kapoor, 11 yrs, since 1 Jan 2026 | Jain also runs Invesco Large Cap (since Dec 2023) and PSU Equity (co, Jul 2025) | Dhimant Kothari co-managed until about 2025 [A] | [F] Invesco Aug 2026 |
| F12 | SBI Banking & Financial Services Fund (SBI Funds Management; Sectoral) | Milind Agrawal, 18 yrs, since Aug 2019 | Also SBI ELSS Tax Saver (from Jan 2026) | Not named | [F] SBI Aug 2026 |
| F13 | Tata India Consumer Fund (Tata AMC; Thematic) | Sonam Udasi (28 yrs experience) since 1 Apr 2016; Aditya Bagul (13 yrs) since 3 Oct 2023 | Other schemes not read | Fund launched 28 Dec 2015; Udasi from 1 Apr 2016 | [F] Tata Aug 2026 |
| F14 | SBI PSU Fund (SBI Funds Management; Sectoral) | Rohit Shimpi, 19 yrs, since Jun 2024 | Also SBI ESG Exclusionary Strategy (since Jan 2022), US equity FoF (Feb 2025). Joined SBI 2006; in Mutual Fund Dept since Nov 2018 [A] | Not named | [F] SBI Aug 2026 |
| F15 | Kotak Business Cycle Fund (Kotak AMC; Thematic) | Harish Bihani since 20 Oct 2023; Abhishek Bisen since 28 Sep 2022 (inception) | Bihani also runs Kotak Pioneer and Small Cap (both Oct 2023). Before Kotak he was an ICICI Pru MF fund manager, including F2 until Sep 2023 | None before Bisen | [F] Kotak Aug 2026 |
| F16 | HDFC Value Fund (HDFC AMC; Value) | Anand Laddha, 22 yrs, since 1 Feb 2024; Kagalkar (gold/silver) from 26 Aug 2026 | Co-manages HDFC Banking & Financial Services and HDFC Consumption | Gopal Agrawal until 31 Jan 2024 [P] Value Research | [F] HDFC Aug 2026; [P] |
| F17 | Nippon India Multi Cap Fund (Nippon Life India AMC; Multi Cap) | Sailesh Raj Bhan, 30 yrs; AMC lists "Managing since March 2005" | Also Nippon India Pharma Fund (Jun 2004) and Large Cap Fund (Aug 2007) | none | [F] Nippon Sep 2026 |
| F18 | HDFC Flexi Cap Fund (HDFC AMC; Flexi Cap) | Amit Ganatra, 19 yrs, since 1 Feb 2026 | Also HDFC Focused Fund. Press: rejoined HDFC in Feb 2026 after a long spell at Invesco [A] | Chirag Setalvad per HDFC notice reported by Value Research [P]; INDmoney and Business Standard describe Roshi Jain as the previous lead manager [A]. The sources conflict | [F] HDFC Aug 2026; [P] |

Coin shows only one name per fund and gave a different name for ICICI Pru Business Cycle (Divya Jain) and DSP TIGER (Charanjit Singh), which I did not verify against AMC documents; those two are in section 9 as screened-out.

### 3.2 Terms and cost

| # | Launch | AUM (date) | Direct cost | Benchmark (AMC) | Exit load | Lump sum / SIP minimum |
|---|---|---|---|---|---|---|
| F1 | 7 Jun 2024 | 6,354.70 (31 Aug) [F] | TER 0.99%, BER 0.71% | Nifty Auto TRI | 1% within 30 days | Rs 5,000 / SIP Rs 500 |
| F2 | 28 Oct 2022 | 4,119.31 (31 Aug) [F] | BER 0.87% | Nifty Transportation & Logistics TRI | 1% within 1 month | Rs 5,000 (add'l Rs 1,000) / SIP n/v |
| F3 | 17 Aug 2023 | 2,115.78 (31 Aug) [F] | BER 0.93% (incl. levies; Coin shows 0.82%) | Nifty Transportation & Logistics TRI | 1% within 30 days | Rs 100 purchase and additional / SIP n/v |
| F4 | n/v | 4,341 (8 Oct) [C]; 3,962 (Jul) [A] | 0.69% [C]; aggregator 0.89% [A]: conflict | Nifty Transportation & Logistics [A] | n/v | Rs 5,000 [C] / SIP n/v |
| F5 | 22 Jul 2024 | 8,276.04 (31 Aug) [F] | BER 0.61% | Nifty Energy TRI | 1% within 3 months | Rs 1,000 [F] (Coin shows Rs 5,000) / SIP n/v |
| F6 | 8 May 2004 | 8,136.78 (31 Aug) [F] | BER 0.80% in Aug (0.94% in the FY25-26 table) | Nifty Infrastructure TRI | 1% within 1 month | Rs 5,000 / SIP Rs 100 |
| F7 | 31 Aug 2005 | 8,558.09 (31 Aug) [F] | BER 0.99% | BSE India Infrastructure TRI | 1% within 15 days | Rs 1,000 [F] (Coin Rs 5,000) / SIP n/v |
| F8 | 25 Feb 2008 | 2,429.85 (31 Jul) [F] | TER 0.74% | Nifty Infrastructure TRI | 0.5% (period not read) | Rs 100 / SIP Rs 100 |
| F9 | n/v (not in factsheet) | 1,547.6 (31 Aug) [F] | BER 0.76% | BSE India Infrastructure TRI | Nil up to 10% of units; else 1% within 1 year | Rs 1,000 / SIP n/v |
| F10 | 22 Feb 2022 | 3,126.86 (31 Aug, web page) [F] | TER 0.65% | Nifty India Manufacturing TRI | 0.5% within 90 days | Rs 100 / SIP Rs 100 |
| F11 | 14 Jul 2008 | 1,895.57 (31 Aug) [F] | BER 0.70% | Nifty Financial Services TRI | Nil up to 10% of units; else 1% within 1 year | Rs 1,000 / SIP n/v |
| F12 | 26 Feb 2015 | 10,872.12 (31 Aug) [F] | TER 1.20%, BER 0.68% | Nifty Financial Services TRI | 0.5% within 30 days | Rs 5,000 / SIP Rs 500 |
| F13 | 28 Dec 2015 | 2,900.93 (31 Aug) [F] | BER 0.62% (as of 31 May 2026) | Nifty India Consumption TRI | 0.25% within 30 days | Rs 5,000 / SIP Rs 100 |
| F14 | 7 Jul 2010 | 6,693.32 (31 Aug) [F] | TER 0.91%, BER 0.72% | BSE PSU TRI | 0.5% within 30 days | Rs 5,000 / SIP Rs 500 |
| F15 | 28 Sep 2022 | 3,508.76 (31 Aug) [F] | TER 0.67% | Nifty 500 TRI | 0.5% within 90 days | Rs 100 / SIP Rs 100 |
| F16 | 1 Feb 1994 | 8,265.95 (31 Aug) [F] | BER 1.01% | Nifty 500 TRI | 1% within 1 year | Rs 100 / SIP n/v |
| F17 | n/v (AMC lists manager since Mar 2005) | 56,297.62 (31 Aug) [F] | BER 0.68% | Nifty 500 Multicap 50:25:25 TRI | 10% of units free; else 1% within 12 months | Rs 100 / SIP Rs 100 |
| F18 | 1 Jan 1995 | 113,606.47 (31 Aug) [F] | BER 0.67% | Nifty 500 TRI | 1% within 1 year | Rs 100 / SIP n/v |

For comparison, ICICI Pru Nifty Auto Index Fund (Direct): BER 0.25%, AUM Rs 253 cr (31 Aug), tracking difference -0.47% (1y) and -0.56% (3y), exit load nil, minimum Rs 1,000 (file 07).

Each Coin SIP tranche starts its own exit-load clock; for a 5-month staging the 30-day and 1-month loads only matter for an early exit of the last tranche. The 3-month load on F5 and 90-day loads on F8/F10/F15 are worth remembering if the investor may sell a recent tranche.

## 4. Performance and risk

### 4.1 Returns to 8 Oct 2026 (Direct Growth NAV, my calculation [N]); 1y simple, longer annualised

"Proxy" = the benchmark proxy from section 2, same dates. "Since 31 Dec 2024" is the annualised return over the last 21 months, to show what has happened after the 2023-24 rally. "Under current manager" is the return since the lead manager's start date in section 3.1 (CAGR where over a year).

| # | 1y | 3y | 5y | Since launch (years) | Proxy 1y / 3y / 5y | Since 31 Dec 2024: fund vs proxy | Under current manager: fund vs proxy |
|---|---|---|---|---|---|---|---|
| F1 | 16.7 | n/a | n/a | 8.8 (2.3) | Auto: -6.9 / 16.0 / n/a | 17.9 vs 4.9 | 8.8 vs -0.4 (2.3y) |
| F2 | 1.1 | 19.5 | n/a | 21.2 (3.9) | Auto: -6.9 / 16.0 / n/a | 9.5 vs 4.9 | 18.4 vs 14.4 (3.1y); before 18 Sep 2023: +27.3% total vs +24.5% (0.9y) |
| F3 | 2.3 | 22.2 | n/a | 22.6 (3.1) | Auto: -6.9 / 16.0 / n/a | 13.3 vs 4.9 | 22.6 vs 16.6 (3.1y) |
| F4 | -6.3 | 15.4 | 16.9 | 17.8 (13.8, from Jan 2013) | Auto: -6.9 / 16.0 / n/a; Nifty 50: -10.3 / 5.4 / 5.6 | 6.3 vs 4.9 | 11.8 vs Nifty 50 11.4 (since Nov 2016) |
| F5 | 8.6 | n/a | n/a | 5.4 (2.2) | Nifty 500: -5.7 / 8.5 / 7.8 (no Nifty Energy proxy) | 9.6 vs -1.0 | since Nov 2024: 7.1 vs -1.6 (1.9y); Naren era (to 31 Oct 2025): +7.6% total vs +4.9% |
| F6 | 4.6 | 16.3 | 18.7 | 14.6 (13.8) | Infra: -6.3 / 10.8 / 10.6 | 2.8 vs 0.4 | -0.2 vs -3.6 (2.1y) |
| F7 | -3.4 | 15.1 | 18.7 | 15.5 (13.8) | Infra: -6.3 / 10.8 / 10.6 | 1.4 vs 0.4 | Gaidhani: -6.5% total in 0.3y vs -9.1%. Dalwai-era last 5y to 15 Jun 2026: 24.1 vs 15.9 |
| F8 | 4.8 | 15.1 | 17.3 | 15.0 (11.7) | Infra: -6.3 / 10.8 / 10.6 | 1.0 vs 0.4 | 15.0 vs 10.6 (3.0y) |
| F9 | 2.5 | 17.0 | 17.4 | 18.3 (13.8) | Infra: -6.3 / 10.8 / 10.6 | 0.6 vs 0.4 | Gandhi: 17.4 vs 6.7 (1.6y). Nigam era, 5y to 28 Feb 2025: 24.4 vs 20.6 |
| F10 | 12.8 | 19.3 | n/a | 19.7 (4.6) | Mfg: 0.2 / 15.6 / n/a | 10.3 vs 4.6 | 18.8 vs 15.0 (3.0y) |
| F11 | 2.0 | 15.6 | 13.0 | 15.1 (13.8) | Bank: -2.3 / 7.7 / 8.2 | 6.5 vs 4.6 | Jain: 23.3 vs 20.0 (6.4y, starts right after the Mar 2020 low) |
| F12 | -3.3 | 14.2 | 11.3 | 14.0 (11.6) | Bank: -2.3 / 7.7 / 8.2 | 5.8 vs 4.6 | Agrawal: 13.9 vs 9.8 (7.2y) |
| F13 | 1.1 | 12.9 | 12.0 | 16.6 (10.8) | Consumption: -11.4 / 8.8 / 8.8 | -0.4 vs -2.5 | Udasi: 17.6 vs 12.5 (10.5y) |
| F14 | -1.4 | 17.4 | 20.4 | 10.9 (13.8) | CPSE: -5.7 / 18.6 / 22.8 | 3.2 vs 1.0 | Shimpi: -2.3 vs -5.0 (2.3y) |
| F15 | 2.2 | 14.8 | n/a | 15.0 (4.0) | Nifty 500: -5.7 / 8.5 / n/a | 4.6 vs -1.0 | Bihani: 15.3 vs 8.8 (3.0y) |
| F16 | 2.0 | 14.3 | 12.3 | 15.4 (13.8) | Nifty 500: -5.7 / 8.5 / 7.8 | 3.9 vs -1.0 | Laddha: 9.5 vs 4.2 (2.7y) |
| F17 | -5.2 | 11.3 | 14.5 | 15.1 (13.8) | Nifty 500: -5.7 / 8.5 / 7.8 | -0.5 vs -1.0 | Since Sep 2019: 18.6 vs 13.9 (7.1y) |
| F18 | -4.3 | 14.0 | 14.9 | 15.4 (13.8) | Nifty 500: -5.7 / 8.5 / 7.8 | 2.8 vs -1.0 | Ganatra: -5.1% total in 0.7y vs -5.7% |
| ICICI Nifty Auto IF (reference) | -6.9 | 15.7 | n/a | 18.5 (4.0) | Auto ETF: -6.9 / 16.0 / n/a | 4.8 | n/a |

AMC-printed returns at 31 Aug 2026 against the AMC benchmark (stale by 5 weeks of a falling market, but they are against the true TRI benchmark; Direct unless stated):

| # | Fund returns 1y / 3y / 5y / since inception | Benchmark returns | Plan basis |
|---|---|---|---|
| F2 | 17.71 / 23.40 / n/a / 24.03 | 9.77 / 21.63 / n/a / 22.19 (Nifty Transportation & Logistics TRI) | Growth (as printed) |
| F3 | 18.18 / 26.14 / n/a / 26.32 | 9.77 / 21.63 / n/a / 22.04 | Regular |
| F5 | 18.03 / n/a / n/a / 6.98 | 13.96 / n/a / n/a / -3.31 (Nifty Energy TRI) | Growth (as printed) |
| F6 | 15.61 / 20.70 / 21.82 / 15.39 | 4.29 / 16.51 / 15.43 / 11.06 (Nifty Infrastructure TRI) | Direct |
| F7 | 7.31 / 18.58 / 22.06 / 15.41 | 1.38 / 18.29 / 19.87 / n/a (BSE India Infrastructure TRI) | Growth (as printed) |
| F9 | 9.42 / 19.56 / 18.71 / 10.78 | 1.38 / 18.29 / 19.87 / 7.58 | Regular. **Trails its benchmark over 5y** |
| F11 | 14.79 / 20.13 / 15.13 / 15.88 | 3.75 / 11.35 / 8.80 / 13.63 (Nifty Financial Services TRI) | Direct |
| F12 | 6.86 / 17.37 / 13.14 / 14.86 | 3.75 / 11.35 / 8.80 / 12.18 | Direct |
| F13 | 9.47 / 16.36 / 15.26 / 17.63 | -1.35 / 13.50 / 12.43 / 13.08 (Nifty India Consumption TRI) | Direct |
| F14 | 14.98 / 23.54 / 24.49 / 11.78 | 14.55 / 24.76 / 25.75 / 8.04 (BSE PSU TRI) | Direct. **Trails its benchmark over 1, 3 and 5y** |
| F17 | 3.61 / 14.29 / 18.02 / n/a | 7.51 / 13.97 / 13.20 (Nifty 500 Multicap 50:25:25 TRI) | Direct |
| F18 | -0.36 (1y), 17.49 (3y) to May 2026 | 0.28, 13.92 | Regular, HDFC leaflet via search [A] |

SIP-basis figures only (no lumpsum table read): F8 since-inception SIP return 15.34% against 11.07% for Nifty Infrastructure TRI (31 Jul 2026); F10 SIP 3-year 13.77% against 14.27% for the Nifty India Manufacturing TRI (30 Jun 2026, Regular).

### 4.2 Risk: drawdowns, capture, rolling consistency [N]

Drawdown = peak-to-trough fall of Direct NAV. "2024 peak" = highest NAV during calendar 2024. Capture = average monthly fund return in months when the proxy fell (down) or rose (up) divided by the proxy's, using month-end NAVs; below 100 on the down side is better. Rolling windows are daily start dates.

| # | Worst fall since 2013 (or launch), dates | Feb-Mar 2020 fall: fund / sector proxy (Nifty 50: -38.4%) | 2024 peak > worst trough after it > now vs that peak | Now vs all-time high | Capture vs sector proxy, down / up (months); vs Nifty 500 | Rolling 3y: median / worst / % positive / % beating proxy | 1y volatility |
|---|---|---|---|---|---|---|---|
| F1 | -29.2% (27 Sep 24 > 7 Apr 25) | not alive | 27 Sep 24 > -29.2% > +10.9% | -10.5% (20 Aug 26) | 81 / 110 (28); N500 99 / 150 | n/a (1y: median 21.0, 77% positive, beat proxy 58%) | 18.8% |
| F2 | -23.6% (27 Sep 24 > 7 Apr 25) | not alive | 27 Sep 24 > -23.6% > +3.1% | -11.7% (20 Aug 26) | 71 / 91 (48); N500 82 / 131 | 26.3 / 19.9 / 100 / 63 | 19.0% |
| F3 | -23.5% (27 Sep 24 > 7 Apr 25) | not alive | 27 Sep 24 > -23.5% > +9.2% | -10.6% (20 Aug 26) | 70 / 96 (38); N500 94 / 145 | only 35 windows: 25.6 / 22.8 / 100 / 100 | 18.4% |
| F4 | -56.9% (12 Jan 18 > 23 Mar 20) | -43.7 (no proxy) | 27 Sep 24 > -24.9% > -5.6% | -12.2% (20 Aug 26) | 82 / 87 (57); N500 79 / 107 | 19.7 / -18.8 / 86 / 0 | 18.2% |
| F5 | -18.7% (27 Sep 24 > 28 Feb 25) | not alive | 27 Sep 24 > -18.7% > +7.6% | -7.9% (22 Jun 26) | vs Nifty 500 only: 79 / 119 (27) | n/a (1y: median 12.3, 90% positive) | 14.6% |
| F6 | -53.2% (15 Jan 18 > 24 Mar 20) | -40.4 / -37.4 | 27 Sep 24 > -25.6% > -4.5% | -8.1% (22 Jun 26) | 95 / 114 (119); N500 97 / 124 | 18.5 / -14.2 / 91 / 73 | 16.4% |
| F7 | -46.8% (23 Jan 18 > 23 Mar 20) | -41.9 / -37.4 | 1 Oct 24 > -19.1% > -6.2% | -9.4% (6 Jul 26) | 89 / 110 (119); N500 89 / 120 | 18.2 / -12.4 / 92 / 83 | 15.6% |
| F8 | -46.0% (12 Jan 18 > 24 Mar 20) | -40.5 / -37.4 | 27 Sep 24 > -27.7% > -4.7% | -5.4% (8 Sep 26) | 83 / 104 (119); N500 85 / 115 | 19.4 / -11.2 / 90 / 78 | 17.3% |
| F9 | -36.2% (20 Feb 20 > 24 Mar 20) | -36.2 / -37.4 | 5 Jul 24 > -26.6% > -5.0% | -8.9% (22 Jun 26) | 79 / 107 (119); N500 86 / 121 | 22.8 / -4.6 / 98 / 100 | 18.2% |
| F10 | -22.3% (27 Sep 24 > 28 Feb 25) | not alive | 27 Sep 24 > -22.3% > +10.7% | -5.5% (23 Sep 26) | 82 / 99 (50); N500 72 / 116 | 22.0 / 15.7 / 100 / 41 | 15.6% |
| F11 | -42.4% (12 Feb 20 > 23 Mar 20) | -42.4 / -48.6 (bank) | 10 Dec 24 > -14.9% > +5.6% | -7.9% (13 Jul 26) | 75 / 93 (119); N500 103 / 108 | 18.7 / -4.1 / 98 / 89 | 17.6% |
| F12 | -43.8% (20 Feb 20 > 23 Mar 20) | -43.8 / -48.6 (bank) | 10 Dec 24 > -10.7% > +5.1% | -11.6% (12 Feb 26) | 75 / 93 (119); N500 102 / 105 | 17.2 / -2.0 / 99 / 88 | 16.2% |
| F13 | -32.5% (31 Aug 18 > 23 Mar 20) | -31.1 / -29.2 | 23 Sep 24 > -20.7% > -5.9% | -7.8% (25 Aug 26) | 80 / 105 (130); N500 69 / 90 | 18.7 / 2.1 / 100 / 99 | 14.3% |
| F14 | -47.1% (6 Nov 17 > 24 Mar 20) | -34.4 / -39.5 (CPSE) | 1 Aug 24 > -24.1% > -7.9% | -14.6% (26 Feb 26) | 82 / 87 (119); N500 103 / 121 | 10.8 / -15.4 / 85 / 39 | 14.9% |
| F15 | -18.4% (23 Sep 24 > 3 Mar 25) | not alive | 23 Sep 24 > -18.4% > +2.7% | -5.5% (10 Aug 26) | vs Nifty 500: 78 / 105 (48) | 18.3 / 14.8 / 100 / 100 | 14.2% |
| F16 | -43.9% (23 Jan 18 > 23 Mar 20) | -40.9 / -37.3 (N500) | 26 Sep 24 > -18.2% > -1.4% | -6.6% (31 Aug 26) | vs Nifty 500: 95 / 106 (85) | 17.3 / -10.0 / 96 / 98 | 14.0% |
| F17 | -42.8% (27 May 19 > 23 Mar 20) | -41.0 / -37.3 (N500) | 26 Sep 24 > -18.6% > -7.1% | -8.3% (5 Aug 26) | vs Nifty 500: 93 / 111 (85) | 17.0 / -8.8 / 94 / 100 | 14.1% |
| F18 | -41.8% (4 Jul 19 > 23 Mar 20) | -40.2 / -37.3 (N500) | 26 Sep 24 > -12.3% > -1.2% | -7.7% (3 Aug 26) | vs Nifty 500: 85 / 105 (85) | 17.7 / -8.0 / 95 / 100 | 12.9% |
| ICICI Nifty Auto IF | -28.3% (27 Sep 24 > 7 Apr 25) | not alive | 27 Sep 24 > -28.3% > -10.2% | -17.4% (7 Aug 26) | vs Nifty 500: 99 / 129 (48) | 26.2 / 16.2 / 100 / n/a | 20.9% |
| Reference: Nifty 500 proxy | -37.3% (Feb-Mar 2020) | -37.3 | 26 Sep 24 > -18.6% > -10.2% | n/a | n/a | n/a | 14.2% |

Reading it:
- **No fund on the autos or energy list has been through a full bear market.** F1, F2, F3, F5, F10 and F15 were all launched after Mar 2020. Their worst fall (-18% to -29%) is one 6-month episode. Funds that were alive in Feb-Mar 2020 fell 31% to 44%; UTI Transportation & Logistics fell 43.7% and 56.9% peak-to-trough in 2018-20.
- **Downside capture is mostly 70% to 95% against the sector proxy** (better than 100) but close to or above 100% against Nifty 500 for the banking and PSU funds, which says they carry market-like risk.
- **Rolling 3-year consistency is high everywhere** because every 3-year window of the past six years includes the 2021 or 2023 rallies. It is not evidence of resilience in a flat or falling market. Since 31 Dec 2024 the infrastructure, PSU, Multi Cap and Consumer funds have returned -0.5% to 3.2% a year.

## 5. Whose record is it? Where the outperformance came from

**A. The record belongs to someone else (do not use the 3y or 5y figure as manager evidence):**
- **F7 ICICI Infrastructure:** 5y 18.7% (Regular 22.1% at 31 Aug) was earned under Ihab Dalwai, who left on 15 Jun 2026. Over the five years to that date the fund returned 24.1% a year against 15.9% for the infrastructure proxy. Under Sanket Gaidhani it has been 0.3 years: -6.5% against -9.1%.
- **F9 Invesco Infrastructure:** 5y record (24.4% a year against 20.6%) was Amit Nigam's, and he left Invesco on 25 Nov 2025. Sagar Gandhi, 16 years' experience, has run it alone since then and with Nigam since 1 Mar 2025 (17.4% against 6.7% over 1.6 years). Invesco's own table shows the fund **trailing its BSE India Infrastructure benchmark over 5 years** (18.71% against 19.87%). 56% of the portfolio is small-cap.
- **F6 Nippon Power & Infra:** 5y 18.7% and 3y 16.3% mostly predate Rahul Modi (Aug 2024). Under him the fund has returned -0.2% a year against -3.6% for the infrastructure proxy. The fund's calendar years: 2021 +49.7%, 2023 +59.0%, 2025 +0.4%, 2026 to date +4.6%.
- **F14 SBI PSU:** 5y 20.4% was mostly the 2021 to 2024 PSU rally (calendar 2023: +55.7%). Under Rohit Shimpi (Jun 2024): -2.3% a year against -5.0% for the CPSE proxy. It trails the BSE PSU TRI over 1, 3 and 5 years in SBI's own table.
- **F16 HDFC Value:** Anand Laddha took over from Gopal Agrawal on 1 Feb 2024; 5y 12.3% and the 13.8-year history are not his. His 2.7 years: 9.5% against 4.2%.
- **F18 HDFC Flexi Cap:** Amit Ganatra took over on 1 Feb 2026 (0.7 years: -5.1% against -5.7%). The record is HDFC's earlier managers'. Press conflicts on who preceded him (Setalvad per HDFC notice reported by Value Research; Roshi Jain per INDmoney/Business Standard).
- **F5 ICICI Energy Opportunities:** The fund launched under Sankaran Naren; he left on 1 Nov 2025. Under Naren (launch to 31 Oct 2025, 1.3 years) it returned +7.6% total (5.9% a year) against +4.9% for the Nifty 500 proxy. Since he left (11 months to 8 Oct 2026, run by Mishra, Khandelwal and D'Silva) it is +4.4% against -8.1%. That is a short post-Naren record, but it has not collapsed. Nitya Mishra's own listed start (Nov 2024) overlaps Naren's tenure, so there is no clean solo record.
- **F2 ICICI Transportation & Logistics:** Harish Bihani and Sharmila D'Silva ran the first 11 months (+27.3% against +24.5%); Chandak and Khandelwal have run it since 18 Sep 2023 (18.4% a year against 14.4%). Bihani now runs Kotak Business Cycle (F15).
- **F8 Kotak Infrastructure:** Nalin Bhatt took over on 1 Oct 2023: 15.0% a year against 10.6% for the infrastructure proxy over 3.0 years is his. The 5y 17.3% is not.

**B. Outperformance that came from one rally or from a style that has since reversed:**
- Infrastructure, PSU and power funds (F6 to F9, F14): calendar 2021 (+40% to +60%) and 2023 (+39% to +59%) produced most of the 3y and 5y figures. Since 31 Dec 2024: ICICI Infra 1.4% a year, Kotak Infra 1.0%, Invesco Infra 0.6%, Nippon P&I 2.8%, SBI PSU 3.2% against 0.4% for the infrastructure proxy.
- F1, F2 and F3 (auto and transport funds): the lead over the Nifty Auto proxy is lumpy. Calendar years (fund against proxy): F1 2024 (from June) -9.0 against about -9.0, 2025 +22.1 against +24.2, 2026 to 8 Oct +9.5 against -12.3. F2 2024 +27.1 against +23.3, 2025 +19.6 against +24.2, 2026 -1.9 against -12.3. F3 2024 +30.1 against +23.3, 2025 +21.9 against +24.2, 2026 +2.3 against -12.3. So all three **lagged the index in 2025 and their entire recent lead comes from 2026 year to date**, when the index fell and they held up. F1 holds 39.6% in small caps and 86.5% in autos and components, while the index is dominated by M&M, Maruti, Bajaj Auto, Eicher and TVS (file 07). I could not check which holdings drove the 2026 gap without earlier portfolios.
- F1 AUM: Rs 6,354.70 crore after 28 months. Inflows tend to follow a good run; capacity for a 40% small-cap portfolio is a question I cannot answer from the data.
- F11 Invesco Financial Services and F12 SBI BFSI: the "under current manager" return starts at or just after the Mar 2020 low (F11 from May 2020), so the 6- to 7-year figures include the strongest recovery in the sample. The relative result (+3 to +4 points a year over the bank proxy) is more reliable than the absolute number.

**C. Holdings that no longer match the sector story** (portfolio figures from AMC documents, 31 Jul to 31 Aug 2026):
- **F10 Kotak Manufacture in India:** pharma and biotech 16.8%, ferrous and non-ferrous metals about 7.3% (Tata Steel 3.73%, Hindalco 2.64%, Jindal Steel 0.93%): 24% in the sectors file 04 says to avoid. Top holdings include Sun Pharma, Rubicon Research, Divi's.
- **F5 ICICI Energy Opportunities:** oil, gas and consumable fuels 34.0% (Reliance 9.26%, ONGC 5.26%, Oil India 4.05%, BPCL, IOC); capital goods 34.2%; NTPC is the only utility in the top ten (7.33%). The "power/grid improving" call is only a small part of it.
- **F7 ICICI Infrastructure:** InterGlobe 8.27%, Oberoi Realty 4.45%, Brigade 3.26% (realty is on the avoid list), L&T 5.56%.
- **F8 Kotak Infrastructure:** Bharti Airtel 8.76% plus Indus Towers 3.62% (telecom 12.4%), Reliance 7.75%.
- **F15 Kotak Business Cycle:** banks 16.6%, healthcare services 9.9% (Aster DM, KIMS, Vijaya Diagnostic), retailing 10.3%; autos only 5.5%. Not an autos or power fund.
- **F2 ICICI Transportation & Logistics:** automobiles and components 60.2%, but Eternal 9.59% and Swiggy 3.30% (consumer services 13.8%) plus InterGlobe 6.05% and Delhivery are 20%+ of the fund; "mobility" is stretched.
- **F3 HDFC Transportation & Logistics:** top ten are all automotive except Eternal 7.75%; Bosch 7.80%, Sona 6.53%, Gabriel 4.98% mean it is largely an auto-ancillary fund.
- **F11 Invesco Financial Services:** banks about 50%, but capital-markets names (MCX 4.50%, ICICI Pru AMC 3.88%, BSE 3.85%, Nuvama 3.46%, CDSL, CAMS, KFin) are about 22% (sector split from the Invesco one-pager, via search summary [A]). This is a bet beyond "private banks and NBFCs".
- **F13 Tata India Consumer:** FMCG about 31%, consumer services 18% (Eternal 9.36%), durables 18% (Titan 6.97%), autos and components 16% (CarTrade, Ather, Bajaj Auto) (sector weights from Tata's fund page via search summary [A]). A consumer-discretionary tilt, not an FMCG fund; this is why it fell much less than the Nifty FMCG ETF.
- **F16 and F17:** diversified; IT and pharma appear in the top ten (Infosys, Sun Pharma in F16; Infosys 3.43% in F17).

### 5.1 Portfolio concentration, cap mix, turnover

| # | Top 10 share | Number of stocks | Cap mix L / M / S (% of NAV) | Turnover | Top five holdings |
|---|---|---|---|---|---|
| F1 | 51.6% | n/v | 38.6 / 19.3 / 39.6 | 0.52x | M&M 12.92, Eicher 5.64, TVS 4.92, Sona BLW 4.48, Samvardhana Motherson 4.30 |
| F2 | 63.8% | n/v | n/v | 0.57x | M&M 12.63, Eternal 9.59, TVS 7.43, Maruti 6.44, Hyundai 6.17 |
| F3 | 63.4% | n/v | n/v | 28.9% | Eicher 9.02, Maruti 8.77, Bosch 7.80, Eternal 7.75, Tata Motors 7.35 |
| F4 | 66.9% [A, 30 Jun] | 44 [A] | n/v | n/v | M&M 12.5, Maruti 9.1, Eternal 9.2, Eicher 7.5, Adani Ports 6.4 [A] |
| F5 | 44.1% | n/v | n/v | **1.65x** | Reliance 9.26, NTPC 7.33, ONGC 5.26, Oil India 4.05, Cummins 3.43 |
| F6 | 37.4% | n/v | n/v | 0.46x | Reliance 7.31, L&T 6.68, NTPC 5.07, NTPC Green 3.83, BHEL 3.48 |
| F7 | 40.6% | n/v | n/v | 0.68x | InterGlobe 8.27, L&T 5.56, Reliance 4.52, Oberoi Realty 4.45, NTPC 3.30 |
| F8 | 48.1% | n/v | 50.0 / 12.5 / 36.5 | 27.8% | L&T 10.21, Bharti Airtel 8.76, Reliance 7.75, Solar Industries 4.09, Indus Towers 3.62 |
| F9 | 46.7% | 37 | 25.6 / 14.5 / 55.9 | 0.94x | Honeywell Automation 9.04, L&T 7.93, Schneider Electric Infra 5.19, ABB 4.03, Grindwell Norton 3.81 |
| F10 | 35.6% | about 57 (my count of the AMC page list) | 41.7 / 20.0 / 33.8 | 35.5% | Rubicon Research 4.85, Sun Pharma 4.76, M&M 3.94, Divi's 3.78, TVS 3.47 |
| F11 | 55.2% | 35 | n/v | 0.31x | ICICI Bank 13.32, Axis 6.90, HDFC Bank 5.65, Karur Vysya 5.18, MCX 4.50 |
| F12 | 63.4% | n/v | 62.8 / 11.7 / 15.9 (4.2% derivatives) | 0.99x (1.62x gross) | HDFC Bank 13.48, ICICI Bank 10.79, Kotak 9.82, Bajaj Finance 7.52, SBI 4.87 |
| F13 | 50.6% | n/v | n/v | 59% | Eternal 9.36, Titan 6.97, Nestle 5.90, Radico Khaitan 5.34, CarTrade 4.74 |
| F14 | 69.7% | n/v | 71.6 / 17.1 / 9.1 | 0.23x | SBI 16.39, NTPC 8.28, BEL 7.97, Power Grid 7.11, GAIL 6.78 |
| F15 | 39.7% | about 52 (my count) | 43.6 / 21.6 / 34.3 | 26.1% | ICICI Bank 8.23, Aditya Infotech 5.17, Eternal 4.04, Axis 3.78, Aster DM 3.56 |
| F16 | 31.8% | n/v | n/v | 25.5% | ICICI Bank 6.60, HDFC Bank 4.43, SBI 3.40, Axis 3.30, Bharti Airtel 2.85 |
| F17 | 28.8% | n/v | n/v | 0.38x | HDFC Bank 6.64, Axis 5.14, Infosys 3.43, ICICI Bank 3.12, L&T 1.79 |
| F18 | 44.0% | n/v | n/v | 12.6% (13.3% total) | ICICI Bank 9.19, Axis 6.19, HDFC Bank 5.71, SBI 4.16, Eternal 3.39 |

"Number of stocks" and cap mix are blank wherever the AMC page I read did not print them. Turnover is shown as printed (a ratio in "x" or a percentage). A turnover of 1.65x means the fund bought and sold the equivalent of its whole portfolio more than once in a year; at the TER-versus-BER gap seen on SBI funds, that is where hidden costs sit.

## 6. Manager risk and key-person structure

| # | Single point of failure? | Recent change in the last 3 years | Rating |
|---|---|---|---|
| F1 | Tanmaya Desai alone; also runs Healthcare and MNC funds | None (new fund) | Medium-high: one manager, AUM growth, no cycle |
| F2 | Two managers, both since Sep 2023 | Both launch managers left Sep 2023 | Medium |
| F3 | Priya Ranjan alone for equity; first lead role (joined as an analyst Nov 2020 [A]) | Sleeve changes for gold/silver and overseas in Aug-Sep 2026 | Medium-high |
| F4 | Sachin Trivedi alone; also heads research | Not confirmed in 2026 | Medium (tenure long, 2026 AMC document missing) |
| F5 | Three names, none a star | Launch manager Naren left Nov 2025 | **High** (the brand manager left; turnover 1.65x) |
| F6 | Rahul Modi alone, one scheme | Manager change Aug 2024 | High |
| F7 | Sanket Gaidhani alone | **Manager change 15 Jun 2026** | **High** |
| F8 | Nalin Bhatt alone | Oct 2023 | Medium-high |
| F9 | Sagar Gandhi alone since Nov 2025 | Nigam left Invesco Nov 2025 | High |
| F10 | Two managers; Bisen is listed on 83 funds | Oct 2023 | Medium |
| F11 | Hiten Jain plus Haresh Kapoor (Jan 2026) | Co-manager added | Medium-low |
| F12 | Milind Agrawal alone (also runs ELSS from Jan 2026) | none | Medium |
| F13 | Sonam Udasi plus Aditya Bagul (Oct 2023) | Assistant added | Medium-low (Udasi has 28 yrs of experience) |
| F14 | Rohit Shimpi alone | Jun 2024 | High |
| F15 | Bihani and Bisen | Bihani joined Oct 2023 | Medium |
| F16 | Anand Laddha, co-manager arrangements | Feb 2024 | Medium-high |
| F17 | Sailesh Raj Bhan alone, 30 years' experience; Rs 56,298 crore fund | none | Medium (key-person is very large: the man and the size) |
| F18 | Amit Ganatra alone | **Feb 2026** | High |
| ICICI Nifty Auto Index Fund | None (rule-based; a named desk manager exists but does not choose stocks) | none | Low |
| Windmill Energy Tracker | Unnamed analyst team of a SEBI-registered research analyst (Windmill Capital, INH200007645) | none found | High on transparency of the person; rules are published but weights are hand-set (file 08) |

## 7. Regulatory standing: what I could and could not verify

**How I checked.** (a) SEBI orders pages: the listing loads, and its keyword search endpoint returns results by title only (it does not search the body of an order or a noticee list). I ran every AMC name, "front running", "Axis", "Quant", "Mutual Fund", and the names of the 25 managers in section 3.1 plus Dhruv Muchhal and Aditya Bagul, across the Orders of AO, Orders of Chairperson/Members, Settlement Orders, Orders of SAT and Orders of Courts lists. (b) News searches on each AMC and on the Axis and Quant matters. (c) Tool limits: SEBI's search did not return the Axis final order of 24 Jul 2026, so that fact rests on press. Absence of a title match is not proof of absence.

| Entity | What I found | Source | Bearing on the shortlist |
|---|---|---|---|
| **Axis Mutual Fund** (not shortlisted) | SEBI interim order-cum-SCN, 28 Feb 2023, front running of Axis MF trades. Settlement orders titled for Meenal Baheti (9 Jul 2025) and Deepak Agrawal (15 Sep 2025) "in the matter of Axis Mutual Fund". Adjudication orders on front running of Axis MF trades by clients of two brokers (30 Apr 2026 and 22 Jul 2026). Settlement of Axis AMC and trustee on TER charging (26 Nov 2024) and a further Axis AMC settlement (24 Mar 2025). **Final order, 24 Jul 2026, per press:** former chief dealer Viresh Joshi barred 7 years, Rs 3 crore penalty, 20 others barred 3 to 7 years, about Rs 30.55 crore wrongful gains; period 1 Sep 2021 to 31 Mar 2022; alleged tipping to a Dubai-based operator. | [S] titles; [P] Business Today, Moneylife, CAalley | No Axis fund was shortlisted. Shows the risk is the dealing desk and the fund manager's trades leaking, which affects any AMC. The investor cannot see this from a factsheet |
| **quant Mutual Fund** (excluded: quant BFSI, Infrastructure, Manufacturing, PSU, Business Cycle, Flexi Cap) | SEBI search and seizure in Jun 2024 over suspected front running; reports (BW Businessworld) that Sandeep Tandon and another person filed for settlement; Tandon said the regulator had not charged Quant or its staff. **No SEBI order against Quant or Tandon found** by title search. | [P] | I excluded these funds on this basis, not because a violation is proven. quant BFSI has a 3y of 19.5%, which would otherwise have ranked high |
| ICICI Prudential AMC | Settlement order 16 Apr 2026 on ICICI Prudential Venture Capital Fund (delayed winding-up of a 2013 real-estate scheme), Rs 14.35 lakh, no admission. Adjudication order 23 Dec 2019 on two entities in the ICICI Pru MF matter (FMCG fund due diligence, Rs 5 lakh per press). Settlement 29 Nov 2018 (AMC and Nimesh Shah). Nothing on front running. | [S], [P] | Minor, old or unrelated to equity schemes |
| SBI Funds Management | Adjudication order 13 Apr 2020 about selective disclosure of UPSI by Manappuram Finance; I read the order: **disposed of without penalty**. Settlement 28 Sep 2018 (SBI MF, Padmini Technologies). Nothing after 2020. | [S] read | None |
| HDFC AMC | Settlements 4 Dec 2018 (Rs 3.78 crore per an undated press item) and 16 Apr 2020 (Essel-related FMP exposure, about Rs 4 crore per press). Several SEBI orders in 2018-2019 are about **outsiders front running HDFC AMC's own trades** (HDFC as the victim). HDFC publishes a penalties and litigation disclosure (Dec 2025 edition exists) which I did not read. | [S] titles, [P] | Old; no front-running by HDFC staff found |
| Kotak Mahindra AMC | SEBI order 30 Jun 2022 on six Kotak FMPs (Essel); penalties on the AMC, MD and others. **Supreme Court upheld SEBI's penalties on 13 Jul 2026** (about Rs 2.1 crore in total per press arithmetic). SAT in Mar 2026 had set aside the fee-disgorgement direction. | [S] title, [P] LiveLaw, Free Press Journal | Debt-fund due diligence, not equity. Still a live governance mark against Kotak |
| Nippon Life India AMC | Adjudication 8 Aug 2024: charging TER to AMC books on five ETFs, Rs 3 lakh. A Feb 2025 disclosure of an order covering Jul 2017 to Sep 2019 (details not read; Nippon said it would appeal). Settlement orders for Nippon India AIF schemes, Jul and Sep 2026 | [S], [P] | Minor, not about the Multi Cap or Power & Infra funds |
| Invesco Asset Management (India) | Settlement 24 Apr 2024, about Rs 4.98 crore, six parties incl. CEO, over inter-scheme transfers and lack of separation between MF and PMS; SEBI took no enforcement action; fixed-income managers involved. Hinduja group's IIHL stake purchase approved by CCI in Aug 2024 | [S], [P] Business Standard, Moneylife | An AMC-level control failure in 2021-23; the FS and Infra fund managers are equity |
| UTI AMC | Adjudication 18 Sep 2023 on UTI MF, UTI AMC and India Debt Opportunities Fund Ltd (UTI International); outcome not read | [S] title | Not equity schemes |
| Tata AMC | Nothing found | [S] | None |
| Named managers (25 names) | **No match in any SEBI order title.** Also no news item found for them in the AMC searches | [S] | Not verified beyond titles; no check of SEBI's investor-complaint data or of past employers |

## 8. Comparison with the index-fund plan and the Windmill Energy Tracker

Per Rs 1 lakh invested. Costs for active funds are the Direct TER or BER in section 3.2. Windmill and index figures are from files 00, 07 and 08.

| | ICICI Pru Nifty Auto Index Fund (Dir) | HDFC Transp. & Logistics (F3) | SBI Automotive (F1) | Windmill Energy Tracker | ICICI Energy Opportunities (F5) | Nippon Power & Infra (F6) |
|---|---|---|---|---|---|---|
| Running cost a year | BER 0.25% (Rs 250); tracking difference -0.47% / -0.56% | BER 0.93% (Rs 930) | TER 0.99% (Rs 990) | No subscription; about Rs 672 a year per Rs 1 lakh including entry and exit charges (file 00) | BER 0.61% (Rs 610; TER n/v) | BER 0.80% (Rs 800) |
| Extra cost against the auto index fund | - | about Rs 680 | about Rs 740 | n/a | n/a | n/a |
| Return the active fund needs to earn to cover that | - | 0.7 point; it delivered +6.2 points a year over 3.1 years | 0.7 point; it delivered +9.3 points over 2.3 years | n/a | n/a | n/a |
| Tax events for you | None until you redeem; each tranche has its own 12-month clock | None until you redeem | None until you redeem | Every applied rebalance sells stocks (taxable; 1.5 trade rounds a year for Energy per file 08, Rs 15,000 to 40,000 sold a year) | None until you redeem | None until you redeem |
| Transparency | Monthly factsheet; index is rule-based | Monthly factsheet with full holdings | Monthly factsheet; top 10 | Public model-portfolio PDF with 11 stocks (Power Grid 10.5%, ONGC 10.5%, Coal India 10.2%, Reliance 10.0%, NTPC 9.5%...); hand-set weights | Monthly factsheet | Monthly factsheet |
| Worst fall seen | -28.3% (Sep 2024 to Apr 2025); 17.4% below its Aug 2026 high | -23.5% (same episode) | -29.2% | about -27% below peak (Jul 2024), 1y -10.9%, 2y -12.5% a year (file 07) | -18.7% (Sep 2024 to Feb 2025) | -25.6% since the 2024 peak (-53.2% in 2018-20) |
| 1y / 3y / 5y (NAV to 8 Oct) | -6.9 / 15.7 / n/a | 2.3 / 22.2 / n/a | 16.7 / n/a / n/a | -10.9 / 9.2 / n/a (price series, file 07) | 8.6 / n/a / n/a | 4.6 / 16.3 / 18.7 |
| Composition vs the sector view | Nifty Auto: M&M 22.8%, Maruti 13.7%, Bajaj Auto 10.4%, Eicher 8.5%, TVS 7.9% | about 85% auto OEMs and components plus Eternal | 86.5% autos and components, 39.6% small-cap | 43.6% power utilities (Power Grid, NTPC, Tata Power, NHPC, JSW Energy), 56.4% oil, gas, coal | 34% oil and gas, 34% capital goods, NTPC 7.3% | Reliance 7.3%, L&T 6.7%, NTPC 5.1%, NTPC Green 3.8%, BHEL, cement |
| Manager risk | Low | Medium-high (one analyst-turned-lead since 2023) | Medium-high | Unnamed team | High: headline manager left Nov 2025 | High: manager since Aug 2024 |
| Staging on Coin | Any amount from Rs 100 | Rs 100 | SIP Rs 500 | Rs 12,296 minimum per purchase; SIP only at Rs 15,000 | Lump Rs 1,000 per AMC (Coin shows Rs 5,000) | SIP Rs 100 |

What this says:
- **Autos.** The active funds have been better on every measured axis except cost and track record length. They would cost about Rs 700 a year more per Rs 1 lakh and have beaten the index fund by far more than that in the only market they have seen. The index fund has the shortest list of ways to disappoint (no manager, no capacity, 0.25%); the active funds have the longest list of unknowns (one cycle, small-cap capacity, a first-time lead manager in F3, Rs 6,355 crore in F1).
- **Energy.** If the investor wants a power/energy slot, ICICI Energy Opportunities beats the Windmill Energy Tracker on return (1y +8.6% against -10.9%), shallower fall, no tax events and no trading by the investor. It loses on composition: Windmill holds 43.6% power utilities; ICICI holds NTPC 7.3% and a large slice of equipment and oil. The Windmill tracker already skipped its Sep 2026 rebalance (file 08). Choose one, not both: they overlap on Reliance, ONGC, NTPC.
- **PSU/power utilities.** SBI PSU Fund (F14) has 16.9% power (NTPC 8.28%, Power Grid 7.11%) alongside SBI 16.4% and Bank of Baroda 5.1%, but the manager is two years in and the fund trails its benchmark. Not a substitute for a power slot.

## 9. Ranking, top five and verdict

Evidence grade: **A** = same manager 6+ years and beat a proxy over that tenure; **B** = manager since launch or 2 to 3.5 years, one rally and one correction seen; **C** = record belongs to a predecessor or the fund holds the avoid list.

| Rank | Fund | Sector slot | Grade | Why | Main reason not to |
|---|---|---|---|---|---|
| 1 | **F13 Tata India Consumer Fund** (Sonam Udasi) | Consumption | A | Udasi since 1 Apr 2016 (10.5 years): 17.6% a year against 12.5% for the consumption proxy; fell 20.7% from its 2024 peak against 22.0% (proxy), 5.9% below that peak now against 16.7%; worst fall 32.5% (2018-20); 3y rolling 100% positive; BER 0.62%; SIP Rs 100; AUM Rs 2,901 crore; assistant added 2023 | Consumption is "fair", FMCG still falling (file 04, 07). The fund is partly consumer-discretionary (Eternal, Titan, Ather); 1y +1.1%, 2y -0.7% a year, flat since Dec 2024. Turnover 59% |
| 2 | **F17 Nippon India Multi Cap** (Sailesh Raj Bhan) | Diversified core alternative | A | AMC lists Bhan since Mar 2005; 18.6% a year since Sep 2019 against 13.9% for Nifty 500; diversified (top 10 28.8%); AMC 5y 18.02% against 13.20%; BER 0.68%; SIP Rs 100 | Not a sector fund (HDFC Bank, Axis, Infosys at top); Rs 56,298 crore; fell 41% in Feb-Mar 2020; 1y -5.2%, flat since Dec 2024; downside capture 93% |
| 3 | **F11 Invesco India Financial Services** (Hiten Jain, Haresh Kapoor) | Banks / financials | A | Jain since 19 May 2020: +3.3 points a year over the bank proxy; 3y 15.6% against 7.7%; downside capture 75%; turnover 0.31x; BER 0.70%; co-manager from Jan 2026; AMC 31 Aug: 3y 20.1% against 11.35% | Overlaps the financials the investor already holds through index funds (file 00); about 22% in exchanges/capital markets, not "private banks and NBFCs"; fell 42.4% in Mar 2020; AUM only Rs 1,896 crore |
| 4 | **F3 HDFC Transportation & Logistics** (Priya Ranjan) | Autos | B | 22.6% a year over 3.1 years against 16.6% for Nifty Auto; fall of 23.5% against 28.3%; downside capture 70%; AUM Rs 2,116 crore; turnover 29%; Rs 100 minimum | First lead-manager role (joined as an analyst Nov 2020 [A]); one cycle; 63% in ten stocks; BER 0.93% against 0.25% |
| 5 | **F5 ICICI Prudential Energy Opportunities** (Nitya Mishra, Priyanka Khandelwal, Sharmila D'Silva) | Power / energy (alternative to Windmill Energy Tracker) | B | 1y +8.6%, fall 18.7%, AUM Rs 8,276 crore, BER 0.61%, no tax events; clear improvement on the Windmill tracker | Naren left Nov 2025; turnover 1.65x; 34% oil and gas, 34% capital goods; 2.2 years of history |
| Alternates | F12 SBI BFSI (Agrawal; closer to the sector view but TER 1.20%, turnover 0.99x); F1 SBI Automotive (Desai) | | A / B | F12: +4.1 points a year over the bank proxy for 7.2 years; F1: 16.7% a year over 2.3 years | F12 higher cost; F1 Rs 6,355 crore and 40% small-cap |

**Verdict by sector**
- **Consumption:** F13 deserves a place if the investor wants a consumption slot. It is the strongest named-manager evidence in the whole set. The sector view is only "fair", so it is a conviction-in-the-manager holding, not a sector call.
- **Autos:** the ICICI Pru Nifty Auto Index Fund stays core. F3 (or F1) earns at most a small satellite if the investor wants a named manager; neither has a 5-year record or any test beyond the Sep 2024 to Apr 2025 fall.
- **Power/grid:** no active fund matches the "power and grid" view. F5 is a conditional replacement for the Windmill Energy Tracker, not an addition to it.
- **Private banks / NBFCs:** F11 is the best active option, but the cheaper and more direct vehicle in file 07 is the ICICI Pru Nifty Private Bank ETF (0.13%), and the investor already holds a fifth in financials. Low priority.
- **Infrastructure, capital goods, manufacturing, PSU, business cycle, value, flexi cap:** no place now. F6 to F9 and F14 earned their numbers under managers who have left or in the 2021 and 2023 rallies; F10 and F15 hold the avoid list or other sectors; F16 and F18 have new managers; F4 is index-like.
- **Diversified:** F17 is the only multi-year, same-manager, size-tested diversified record. It does not express a sector view.

**Illustrative stakes (arithmetic, not advice).** If the investor wants a named-manager sleeve alongside the ICICI Nifty Auto Index Fund, one set of stakes and the loss each would show on the worst fall seen in its own history:

| Fund | Stake | Worst fall observed | Loss at that fall |
|---|---|---|---|
| ICICI Pru Nifty Auto Index Fund | Rs 20,000 | -28.3% (fund history starts 2022; the Windmill Auto Tracker series showed about -53%, file 07) | Rs 5,660 |
| F13 Tata India Consumer | Rs 10,000 | -32.5% (2018-20) | Rs 3,250 |
| F3 HDFC Transportation & Logistics | Rs 10,000 | -23.5% (no 2020 test; UTI F4 fell 43.7% in Feb-Mar 2020) | Rs 2,350 (Rs 4,370 on a 2020-style fall) |
| F5 ICICI Energy Opportunities | Rs 10,000 | -18.7% (no 2020 test; no Nifty Energy proxy) | Rs 1,870 (about Rs 3,800 on a -38% fall) |
| Total | Rs 50,000 | | Rs 13,130 (26% of Rs 50,000) on observed falls; about Rs 17,100 (34%) on a 2020-style fall |

Measured on the Rs 50,000 invested in the sleeve, a 2020-style fall is over a 25% limit; measured on the full Rs 1 lakh, it is 13% to 17%. Staging in 5 tranches reduces timing risk but does not cap a fall.

## 10. Screened out (with reason)

All figures [N] to 8 Oct 2026, Direct Growth; manager names from Coin [C] unless marked.

| Fund | 1y / 3y / 5y | Worst fall | Reason not shortlisted |
|---|---|---|---|
| DSP India T.I.G.E.R. Fund (Charanjit Singh [C]) | 9.7 / 18.3 / 19.6 | -46.9% | Strong, but I did not obtain an AMC document naming manager and tenure; infrastructure/PSU mix; not read |
| DSP Natural Resources & New Energy (Rohit Singhania [C]) | 9.2 / 18.1 / 14.3 | -48.0% | Natural resources include metals (avoid list) |
| ICICI Pru Business Cycle (Divya Jain [C]) | -6.4 / 13.3 / 13.6 | -14.4% | Launched Jan 2021; business-cycle mix; manager not verified |
| ICICI Pru Value (Sankaran Naren [C]), ICICI Pru Multi Cap (Lalit Kumar [C]), Tata Resources & Energy | -8.8 / 10.2 / 12.1; 1.7 / 13.4 / 12.9; 1.2 / 13.6 / 10.6 | -36.7% to -38.9% | Not the plan's sectors; managers not verified |
| SBI Contra (Dinesh Balachandran [C]) | -6.6 / 9.1 / 13.1 | -44.7% | Lags Nifty 500 over 3y |
| ICICI Pru PSU Equity (Antariksha Banerjee [C]), Invesco PSU Equity (Sagar Gandhi [C]) | -1.1 / 18.0 / n/a; -4.6 / 16.9 / 18.4 | -23.0%, -33.4% | PSU rally; trail the CPSE proxy over 1y (ICICI) and 3y (Invesco) |
| UTI Infrastructure, Franklin Build India | -3.5 / 10.6 / 12.0; -5.5 / 13.7 / 16.3 | -42.8% | Managers not verified |
| Parag Parikh Flexi Cap (Rajeev Thakkar [C]) | -5.8 / 11.8 / 10.5 | -31.2% | 52% downside capture is the best in the sample, but its portfolio is global and its sector profile does not match the plan; not read |
| Kotak Transportation & Logistics, SBI/Kotak/Baroda BNP Energy funds, HDFC Manufacturing, Invesco Business Cycle, Abakkus Flexi Cap | various (SBI Energy: 1.8% a year since Feb 2024) | various | 2.6 years of history or less |
| quant BFSI, Infrastructure, Manufacturing, PSU, Business Cycle, Flexi Cap | quant BFSI 8.9 / 19.5 / n/a | various | Excluded because of the reported SEBI front-running probe (section 7), not because a violation is proven |
| Axis Business Cycles, Axis India Manufacturing | -0.1 / 12.0 / n/a; 10.8 / n/a / n/a | -19.3%, -23.0% | Short history; Axis AMC carries the front-running case |

## 11. What I could not verify (not filled from memory)

- **Benchmark TRI history.** All "proxy" comparisons use index-fund or ETF NAVs (net of cost) instead of TRIs. No proxy exists for the Nifty Transportation & Logistics TRI, Nifty Energy TRI (history only from Oct 2025), BSE PSU TRI, BSE India Infrastructure TRI or Nifty Financial Services TRI. The CPSE ETF is not the BSE PSU index. Capture ratios and "beat the proxy" percentages are therefore indicative.
- **Rolling returns versus Nifty 500** begin only in Sep 2019 and include the 2020-21 rally.
- **UTI Transportation & Logistics:** no 2026 UTI factsheet obtained. Manager tenure rests on UTI's Jul 2022 presentation and 2026 aggregator pages; portfolio, expense ratio and exit load are aggregator or Coin figures.
- **Number of stocks and cap mix** are missing for most ICICI, HDFC, Nippon, Tata and UTI funds because the pages read do not print them. Counts of 57 and 52 for the Kotak funds are my count of the AMC page list.
- **SIP minimums** for ICICI Pru (F2, F5, F7), UTI, Invesco and HDFC funds are not in the documents read; Coin's SIP screen shows them. Coin lump-sum minimums differ from the AMC's for ICICI Energy (Rs 5,000 on Coin, Rs 1,000 in the AMC document) and ICICI Infrastructure (same).
- **Exit load period** for Kotak Infrastructure; **launch dates** for Invesco Infrastructure, UTI T&L and Nippon Multi Cap are not in the pages read.
- **AMFI fund-manager records** were not used; tenure is from the AMC documents above. For F6, F8, F14, F11, F16 and F18 the predecessor is from press or aggregators.
- **ICICI Pru Energy Opportunities:** the same factsheet gives two start dates for Nitya Mishra (July 2024 and Nov 2024) and two for Sanket Gaidhani (June 2026 and July 2026). I show both.
- **Press conflicts:** HDFC Flexi Cap's predecessor (Setalvad per HDFC notice via Value Research against Roshi Jain per INDmoney/Business Standard).
- **Regulatory:** SEBI search is title-only; the Axis final order of 24 Jul 2026 is not retrievable through it; no check of SAT/High Court dockets for the managers, SEBI complaint data, or of each AMC's own "penalties and litigation" disclosure. Absence of a hit is not proof.
- **Tax law text:** not read; rates from file 07.
- **No stress-test beyond observed data.** Funds launched after 2020 have no Feb-Mar 2020 observation. Numbers cannot say how they fall in a 35%+ market drop.
- **TER versus BER:** only SBI (and Kotak, which prints TER) give both. For ICICI, HDFC, Nippon, Invesco and Tata the printed figure is the BER and the real TER is likely higher.

## 12. Sources

Primary:
- AMFI NAV file: https://portal.amfiindia.com/spages/NAVAll.txt (NAV date 8 Oct 2026); history mirror https://api.mfapi.in/mf/<scheme code> (codes: 152657, 150685, 151901, 120731, 152728, 118763, 120621, 133801, 120405, 149841, 120385, 133859, 135805, 119732, 150624, 118935, 118650, 118955; proxies 149465, 140102, 140087, 128331, 140107, 150515, 147625, 140084; reference 150643)
- ICICI Pru scheme factsheets, 31 Aug 2026: https://www.icicipruamc.com/blob/knowledgecentre/factsheet-schemes/Schemes/1.%20Equity%20Schemes/ICICI%20Prudential%20Transportation%20and%20Logistics%20Fund.pdf (same folder: Energy Opportunities Fund, Infrastructure Fund)
- HDFC MF factsheet Aug 2026: https://files.hdfcfund.com/s3fs-public/2026-09/HDFC%20MF%20Factsheet%20-%20August%202026.pdf
- SBI all-scheme factsheet Aug 2026: https://www.sbimf.com/docs/default-source/scheme-factsheets/all-sbimf-schemes-factsheet-august-2026.pdf
- Nippon India factsheet Sep 2026 (data 31 Aug): https://mf.nipponindiaim.com/InvestorServices/FactSheetsDocuments/Nippon-FS-September-2026.pdf
- Tata MF factsheet Aug 2026: https://www.tatamutualfund.com/system/files/2026-09/TataMF%20Factsheet%20-%20August%202026.pdf
- Invesco MF factsheet Aug 2026: https://www.invescomutualfund.com/docs/default-source/factsheet/invesco-mf-factsheet-august-2026.pdf
- Kotak: https://www.kotakmf.com/factsheet/August_2026/kotak/KOTAK-MANUFACTURE-IN-INDIA-FUND.html ; https://www.kotakmf.com/factsheet/August_2026/kotak/KOTAK-BUSINESS-CYCLE-FUND.html ; one-pager PDFs `.../Download_pdf/Kotak Infrastructure & Economic Reform Fund_Factsheet One Pager.pdf` (data 31 Jul 2026) ; https://www.kotakmf.com/factsheet/August_2026/kotak/ABOUTOUR-direct.html
- Zerodha Coin pages: https://coin.zerodha.com/mf/fund/<ISIN> (8 Oct 2026)
- SEBI orders: https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=2&ssid=9&smid=6 (and smid=2, 3, 1, 7); SBI Funds 2020 order: https://www.sebi.gov.in/enforcement/orders/apr-2020/adjudication-order-in-respect-of-sbi-funds-management-private-limited-in-the-matter-of-selective-disclosure-of-unpublished-price-sensitive-information-by-manappuram-finance-ltd-_46509.html ; Invesco settlement 24 Apr 2024: https://www.sebi.gov.in/enforcement/orders/apr-2024/settlement-order-in-the-matter-of-invesco-asset-management-india-private-limited_82989.html ; Nippon TER order 8 Aug 2024: https://www.sebi.gov.in/enforcement/orders/aug-2024/adjudication-order-in-the-matter-of-practice-of-charging-ter-to-amc-books-in-respect-of-nippon-life-india-asset-management-limited-and-nippon-life-india-trustee-limited-_85561.html

Press and aggregators (labelled [P] or [A]):
- Axis final order: https://www.businesstoday.in/latest/corporate/story/axis-mf-front-running-case-sebi-bars-former-mf-dealer-viresh-joshi-for-7-years-imposes-rs3-crore-penalty-545155-2026-07-24 ; https://www.moneylife.in/article/axis-mutual-fund-frontrunning-sebi-bars-exchief-dealer-viresh-joshi-for-7-years-imposes-3-crore-fine-21-entities-face-market-ban-3056-crore-disgorgement/81162.html
- Quant: https://www.businessworld.in/article/another-high-profile-front-running-case-sandeep-tandon-sumana-paruchuri-file-for-sebi-settlement-544442 ; https://moneylife.in/article/sebi-investigates-quant-mutual-fund-for-suspected-frontrunning-amid-rapid-growth-moneycontrol/74473.html
- Kotak Supreme Court: https://www.livelaw.in/supreme-court/investors-got-profit-no-defence-for-breach-supreme-court-upholds-sebi-penalty-on-kotak-amc-in-mutual-funds-case-540985
- ICICI Pru VCF settlement: https://moneylife.in/article/icici-prudential-entities-settle-sebi-case-for-1435-lakh-over-delayed-windingup-of-venture-capital-fund/80263.html
- Invesco settlement: https://moneylife.in/article/invesco-asset-management-ceo-and-4-others-pay-rs498-crore-to-settle-sebi-charges-on-mixing-mf-and-pms-activities/74025.html
- Manager changes: Value Research (HDFC Flexi Cap https://www.valueresearchonline.com/stories/227607/fund-manager-changes-in-a-few-schemes-of-hdfc-mutual-fund/ ; Invesco https://www.valueresearchonline.com/stories/223319/fund-manager-changes-in-a-few-schemes-of-invesco-mutual-fund/ ; Nigam exit https://www.valueresearchonline.com/stories/227007/amit-nigam-leaves-invesco-india-mutual-fund/ ; Kotak https://www.valueresearchonline.com/stories/46482/fund-manager-change-in-schemes-of-kotak-mahindra-mutual-fund ; HDFC Value https://www.valueresearchonline.com/stories/53911/fund-manager-changes-for-hdfc-capital-builder-value-fund/)
- UTI T&L: https://doc.utimf.com/uticontainer/Presentation_UTI%20Transportation%20%20Logistics%20Fund_Jul%202022-16220221014-220003.pdf ; holdings https://sharpely.in/mutual-funds/uti-transportation-and-logistics-fund-directgrowth/15955/holdings [A]
- Local reports: `00_decision_memo.md`, `04_sectors.md`, `07_sector_funds.md`, `08_windmill_trackers.md`
