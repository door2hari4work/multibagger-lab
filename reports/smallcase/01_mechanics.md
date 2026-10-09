# smallcase investing: how it works today (as of 2026-10-09)

Prepared for an Indian retail investor. Every number below carries a source and a date. Anything I could not verify is marked **UNVERIFIED** and collected in section 11. Nothing here is investment advice, and nothing here is filled in from memory.

## 0. How this was researched, and how far to trust it

- **Primary documents read in full as raw text** (downloaded and converted by me, not summarised by a tool): SEBI Master Circular for Research Analysts (6 Feb 2026), SEBI Master Circular for Investment Advisers (6 Feb 2026), SEBI circular of 8 Jan 2025 and the SEBI RA FAQ of 23 Jul 2025, the CBDT capital-gains FAQ on PIB (24 Jul 2024), the PIB Budget 2026-27 highlights (1 Feb 2026), the PIB Income Tax Act 2025 release (1 Feb 2026), the SEBI registered Research Analyst list page (snapshot "as on Oct 08, 2026"), and a live smallcase factsheet PDF (last updated 8 Oct 2026).
- **smallcase, broker and Zerodha pages** were read through WebFetch, which returns a small-model summary of the page. The figures are reliable where they match across pages. Treat exact wording as paraphrase unless shown in quotation marks.
- **WebSearch summaries are not evidence.** One of them was wrong when I opened the real page: it said a recent smallcase factsheet disclaims "backtested or simulated results"; the factsheet I read says "Returns and CAGR numbers don't include backtested data". Others were vague or mixed old and new SIP rules. I used search mainly to find URLs.
- Government sites (incometaxindia.gov.in, indiabudget.gov.in) returned HTTP 403, so I could not read the Income-tax Act 2025 section text or the Finance Act 2026. Tax rates therefore rest on the PIB/CBDT FAQ plus the absence of any change in the PIB Budget 2026-27 highlights.

## 1. What a smallcase is, and who does what

| Party | Role | Source |
|---|---|---|
| Investor | Owns the shares directly. "The shares you buy settle directly in your own Demat account." | smallcase, How to Invest in smallcase, 12 Jan 2026 |
| Broker | Places the orders, holds the demat, charges brokerage/DP/STT-related costs. You log into your broker and authorise smallcase to place and track orders. | same page |
| Manager | A SEBI-registered Research Analyst (RA) or Investment Adviser (IA) who picks the basket, weights and rebalance updates. "created and managed by SEBI-registered investment professionals". | smallcase, What is a smallcase, 15 Jan 2026 |
| smallcase (CASE Platforms Pvt Ltd) | "only a technology provider and is not an intermediary in terms of the applicable SEBI regulations"; "does not provide any research recommendations or advice on its own". | smallcase Disclosures page (undated) |

Notes:
- A smallcase is defined as "a basket or portfolio of stocks/ETFs representing an idea" (smallcase, 15 Jan 2026). It is not a pooled fund and there are no units.
- The smallcase group has affiliates that are themselves registered. The Disclosures page lists Essential Investment Managers Pvt Ltd as an IA (INA000017912, valid "24th April 2023 to Perpetual") and says it "does not provide any advisory services on the Platform". It also lists WCPL (the Windmill Capital entity, RA and portfolio manager). So a "smallcase" from a smallcase-group manager is still a separate manager relationship from the platform.
- Under SEBI's model-portfolio rules (Annexure A of the RA Master Circular, 6 Feb 2026), an RA's basket is a "model portfolio" with a factsheet, rationale, methodology, launch date, update dates, risk disclosure and a benchmark. Weights must be stated.
- Created or customised smallcases (ones you build yourself) are not advice, and they do not get rebalance updates: "Created and customised smallcases don't receive rebalance updates, so you must monitor and rebalance them yourself" (Upstox help, undated).

## 2. How investing works, step by step

1. **Browse without a broker.** "link one only when you're ready to invest" (smallcase, 12 Jan 2026).
2. **Click Buy, pick lump sum or SIP.** Paid smallcases show pricing first. For a manager-run smallcase you complete a manager onboarding step (details, manager's terms, plan). The live factsheet (Quantace, 8 Oct 2026) shows the flow as: add email, select plan, add billing, pay; then "Invest Now", choose "One-time + SIP" or "One-time", confirm amount, review, place order.
3. **Link a broker.** Select the broker, log in, authorise. Brokers named by smallcase on 12 Jan 2026: Zerodha, Groww, Upstox, HDFC Securities, ICICI Securities. A demat account is required.
4. **Minimum investment.** smallcase's developer documentation says the minimum is calculated "that ensures that user buys at least one share of every stock" while "maintaining the prescribed weighting scheme". You may invest any amount above it. For an "invest more", the minimum is recalculated using the current weights (developers.gateway.smallcase.com, Transactions, undated). The minimum is shown on each smallcase page and rises with the share price of the stocks in it.
5. **Shares per stock** are "calculated as per the prescribed weights" (same doc). Orders are exchange-traded shares or ETFs, so quantities are whole units. **UNVERIFIED:** no smallcase page I could open states "whole shares only" or "no fractional shares" in so many words. It follows from the "at least one share" language and from NSE cash-market trading, but I did not find it written down.
6. **Leftover cash.** **UNVERIFIED.** I found no smallcase or broker page that says what happens to the rupees left over after whole-share rounding. The plausible outcome is that unused money stays in your broker account and is not part of the smallcase. Confirm in your order book after the first buy.
7. **Weight drift.** Between rebalances nothing trades. Prices move, so weights drift from the target. This is my reasoning, supported by smallcase's statement that "Rebalance updates aren't applied automatically" (smallcase blog, 5 Sep 2025) and that skipping can make the stock mix and returns drift. smallcase says it will "try to move the weighting scheme as close as possible to the prescribed weighting scheme" when you apply a rebalance (Rebalancing 101, 15 Jan 2026), which also implies exact weights are not always reachable.
8. **Exit.** "Exit smallcase" for whole or partial. "There is no exit load in smallcase." There is no lock-in. Orders can only process in market hours (smallcase, How to Sell a smallcase, 13 Jan 2026). Partial exit is only allowed if the investment is above the minimum for that smallcase, and the amount you can withdraw is limited so that the rest still meets the minimum (smallcase dev docs).

## 3. SIP: what exists today

This is the area that changed most recently and where old guides are wrong.

- **Manual SIP has been retired and renamed "Investment Reminder".** smallcase, "Say hello to Investment Reminders", 4 May 2026: the company is "retiring Manual SIP for good"; Manual SIPs on stock and ETF smallcases migrate automatically; you get a reminder on the due date and place the order yourself.
- **Automated SIP (AutoSIP)** is supported only at certain brokers. The same post (4 May 2026) lists "Zerodha, SBI Securities, HDFC Securities, Axis Securities, ICICI Securities, Kotak Neo". With a SIP "Your orders will be placed automatically on the scheduled date."
- **Groww:** "SIP is no longer supported on smallcase for Groww." What was Manual SIP there "is now called Investment Reminder" (smallcase blog on Groww charges, 13 Aug 2026).
- **Upstox, Angel One, others:** not in the May 2026 AutoSIP list. Upstox's own help page (undated) still talks about "SIP (auto or manual)", which looks stale against the 4 May 2026 post. I did not find an Angel One AutoSIP statement. **UNVERIFIED** for Upstox, Angel One and any other broker.
- **Minimum SIP.** For AutoSIP the minimum SIP is "equal to the minimum investment amount of the smallcase" (smallcase blog "Musings with analyst", 7 Oct 2023, describing Auto SIP). So a Rs 10,000 AutoSIP is only possible on baskets whose minimum investment is Rs 10,000 or less. That blog's formula for the old manual SIP minimum (2 x the highest-priced stock, rounded to the nearest thousand) belongs to the retired product. An older smallcase page quotes SIPs "starting from Rs 294" (smallcase, 6 Oct 2023). Do not rely on that figure.
- **Does each SIP buy the whole basket?** For AutoSIP, the same 2023 blog says orders are executed on number of shares: "in every auto SIP order that many shares will get purchased for each stock". That suggests each AutoSIP run buys every stock, at the fixed share counts. The post does not say so in so many words, and it is dated 2023. The developer documentation describes a different logic for SIPs (purchases split across instalments, not all stocks every time), so the two sources conflict. Treat "full basket every time" as **likely but UNVERIFIED for 2026**.
- **Bank mandate.** smallcase's SIP guide mentions a bank mandate that transfers the SIP amount; the flow for AutoSIP at Zerodha (UPI AutoPay vs eMandate) is **UNVERIFIED**.
- **Frequency.** Monthly is standard. The older smallcase page also says quarterly or other intervals (smallcase, 6 Oct 2023). Current frequency options per broker: **UNVERIFIED**.
- **Charges:** see section 5. AutoSIP run: Rs 10 + GST (capped at 1.5% of the SIP). Investment Reminder top-up: Rs 100 (capped at 1.5%) + GST, per the Aug 2026 notices.

## 4. Rebalancing mechanics

- **Who triggers:** the manager decides when and what. smallcase says "The rebalance frequency is decided by the creator of the smallcase" (investor help page, undated); the developer docs say it can be "daily/monthly/quarterly/half-yearly/yearly depending on the type". Most are quarterly (smallcase Rebalancing 101, 15 Jan 2026; Upstox help: "usually quarterly"). Example: the Quantace factsheet (8 Oct 2026) shows monthly, last 25 Sep 2026, next 25 Oct 2026.
- **Does it need investor action:** yes. "Rebalance updates aren't applied automatically." You get an in-app/push/email notification, can review it, apply it in two clicks, or skip (Upstox help; smallcase blog 5 Sep 2025). A smallcase blog dated 9 Apr 2026 says you can exclude specific stocks from an update. Whether you can edit quantities is not confirmed by smallcase's own pages (a third-party guide says so). **UNVERIFIED.**
- **Order of trades:** "Stocks being removed are sold first"; proceeds fund new purchases; if purchases cost more, the gap comes from your broker account; if sales exceed purchases, "the surplus is credited back" (smallcase blog, 9 Apr 2026).
- **If you skip:** the update stays until the next one or until you click skip. Applying a later update aligns you to the latest recommendation, but "returns and CAGR may differ from the original smallcase" (smallcase blog, 5 Sep 2025).
- **Costs:** no smallcase platform fee on rebalance or exit (smallcase Fees page, 15 Jan 2026; Groww notice and Upstox notice, 13 Aug 2026). Statutory and broker costs still apply to every trade, and the sells are tax events (section 6).
- **If a manager's subscription lapses on a paid smallcase:** "You lose access to rebalance updates and premium research. You can keep tracking existing investments and add to them" (smallcase subscription page, 15 Jan 2026).

## 5. All the costs

### 5a. smallcase platform ("transaction") fee

| Event | Fee | Source and date |
|---|---|---|
| Buy / invest more (lump sum) | Rs 100 + GST, capped at 1.5% of order value | smallcase Fees page, 15 Jan 2026 |
| AutoSIP run | Rs 10 + GST, capped at 1.5% of the SIP amount | same page |
| Investment Reminder top-up (Groww, Upstox) | Rs 100 or 1.5% of the amount, whichever is lower, + GST | smallcase notices for Groww and Upstox, both 13 Aug 2026 |
| Rebalance, manage, partial or full exit | Rs 0 platform fee | same pages |

- The Rs 100 is per order, not one-off per smallcase: "Each one-time order", "Every scheduled SIP run" (smallcase notice, 15 Jan 2026).
- Worked examples from smallcase: Rs 1,000 buy costs Rs 15; Rs 3,000 invest-more costs Rs 45; Rs 500 SIP costs Rs 7.50 (all + GST).
- The fee applies to free smallcases too. It is separate from the manager's subscription (smallcase FAQ, 11 Nov 2022). It was introduced on 21 Nov 2022; before that the cap was 2.5% (Upstox and Groww notices of 2022, via search; the Upstox 13 Aug 2026 notice also quotes the old "capped at 2.5%").
- "A lifetime free offer" can waive transaction fees until exit (smallcase FAQ, 11 Nov 2022).
- **Per broker:**
  - Zerodha: charges page lists "Buy & Invest More: 100 | SIP: 10", "Per transaction" (zerodha.com/charges, copyright "2010 - 2026", no effective date).
  - Groww: Rs 100 (cap 1.5%) lump sum; no SIP offered; Investment Reminder at the same Rs 100 rule (smallcase notice, 13 Aug 2026).
  - Upstox: smallcase notice 13 Aug 2026 gives Rs 100 or 1.5% for lump sum and Investment Reminder. Upstox's own help page (undated) says "Rs 100 or 1.5% ... + GST" lump sum and "Rs 10 or 1.5% ... + GST" for SIP. The two disagree on GST wording inside the page itself. Use the dated notice.
  - Angel One: **UNVERIFIED.** No official Angel One or smallcase page found with a smallcase fee. smallcase says "most partners follow the standard" and "a few brokers may quote a different platform fee or waive part of it during promotions" (15 Jan 2026).
  - HDFC Securities, ICICI Securities, Dhan, Kotak and others: **UNVERIFIED**, same caveat.
- **GST rate on the platform fee:** smallcase says "GST applies" but I did not find the rate on a smallcase page. This report uses 18%, which Zerodha and Upstox pages state for brokerage and transaction charges. A forum user quoted Rs 118 on Rs 100 (consistent with 18%) but that is not an official source.

### 5b. Manager subscription

- Set by each manager; billed monthly, quarterly or annually, upfront for the chosen period (smallcase subscription page, 15 Jan 2026). Flat or AUM-based. The page does not mention a one-time payment option, so I cannot confirm that one exists.
- Free smallcases cost Rs 0 in subscription. smallcase says it neither sets nor controls these fees (smallcase blog, 18 Oct 2021).
- No refund for the unused period after cancelling; access continues until the cycle ends; e-Mandate subscriptions need an email to cancel (same 15 Jan 2026 page).
- **Real example price (illustration, not a recommendation):** the Quantace "Smallcap Quant" factsheet (8 Oct 2026) lists 3 months Rs 3,200, 6 months Rs 5,000, 12 months Rs 8,400, "Inclusive of all taxes". The same factsheet says "A minimum investment of Rs 5 lakhs is recommended for cost efficiency". On a Rs 1,00,000 holding, Rs 8,400 is 8.4% a year.
- SEBI limits what RAs can charge Individual/HUF clients: Rs 1,51,000 per annum per family, excluding statutory charges (RA Master Circular, 6 Feb 2026, Annexure/para 1.x fee clause). IAs: up to 2.5% of AUA per annum per family, or fixed fee up to Rs 1,51,000 per annum (IA Master Circular, 6 Feb 2026). Pre-mature termination: RAs must refund proportionate fees and "shall not charge any breakage fee" (RA Master Circular). That conflicts with smallcase's "no refund" subscription wording; I could not reconcile it, so ask the manager before paying. Advance fee: the RA Master Circular body says up to one year; its MITC annexure says "presently it is one quarter". The document is internally inconsistent.

### 5c. Broker and statutory costs (Zerodha shown; verify yours)

Source: zerodha.com/charges (no effective date, copyright to 2026), read 9 Oct 2026.

- Equity delivery brokerage: Rs 0.
- STT on delivery: 0.1% on buy and sell.
- NSE transaction charge: 0.00307%.
- SEBI turnover fee: Rs 10 per crore.
- Stamp duty: 0.015% on buy side only.
- GST: 18% on brokerage, SEBI charges and transaction charges.
- DP charge on sale: Rs 15.34 per scrip, regardless of quantity (CDSL Rs 3.5, Zerodha Rs 9.5, GST Rs 2.34). Charged on each scrip sold, so a full exit of a 15-stock basket costs 15 x Rs 15.34 = Rs 230.10.

Other brokers (each page read 9 Oct 2026, none carrying an effective date unless stated):
- Groww (groww.in/pricing): brokerage "Rs 20 / 0.1% per executed order whichever is lower, minimum Rs 5" (the page does not separate delivery); DP on sell: CDSL Rs 3.5 plus Groww Rs 16.5; AMC Rs 0; NSE transaction charge 0.00297%.
- Upstox (upstox.com/brokerage-charges): delivery brokerage "Rs 20 per executed order"; DP "Rs 20.0 per scrip per day only on sell" plus GST; NSE 0.00307% from 1 Mar 2026; AMC zero for the first year for newly onboarded customers, otherwise Rs 300 + GST per year (non-BSDA).
- Angel One (angelone.in/pricing): brokerage "lower of Rs 20 or 0.1% per executed order, minimum Rs 5" after a 30-day Rs 500 offer; DP Rs 20 + GST per scrip on sell; AMC non-BSDA Rs 60 + GST per quarter after the first year.
- **Open question:** whether Groww, Upstox and Angel One apply per-order delivery brokerage to each stock order generated by a smallcase. Upstox's smallcase help says "regular Upstox delivery charges such as brokerage, STT" apply. If so, a 15-stock basket multiplies the per-order brokerage by 15. Not tested; **UNVERIFIED** how it is applied in practice.
- STT on delivery was not changed in Budget 2026-27; the PIB highlights (1 Feb 2026) raise STT on futures to 0.05% and options to 0.15% only.

### 5d. Taxes: see section 6.

## 6. Taxation of gains

**Rules (listed equity shares on which STT is paid; resident individual):**

| Item | Rule | Source |
|---|---|---|
| Short-term capital gain (STCG) | 20% (was 15% before 23 Jul 2024) | CBDT FAQ on PIB, 24 Jul 2024, Q6 |
| Long-term capital gain (LTCG) | 12.5% (was 10%), only on gains above Rs 1,25,000 in the year | same FAQ, Q6 and Q7 |
| Exemption limit | Rs 1.25 lakh (up from Rs 1 lakh), "for FY 2024-25 and subsequent years" | same FAQ, Q7 |
| Holding period for "long-term" | "The holding period of all listed assets will be now one year" | same FAQ, Q4 |
| Effective date | Transfers on or after 23 Jul 2024 (the earlier 15%/10% rates applied before) | same FAQ |
| Budget 2026-27 | PIB highlights (1 Feb 2026) list buyback taxation, STT on F&O, etc.; they do not list any change to these rates or the exemption | PIB, 1 Feb 2026 |
| New Act | "The Income Tax Act, 2025 is slated to come into effect from 1st April 2026" | PIB, 1 Feb 2026 |

**What I could not verify:**
- That the 20%/12.5%/Rs 1.25 lakh numbers are unchanged inside the Income-tax Act 2025 and the Finance Act 2026. The PIB highlights suggest no change, and secondary sites (Tata Mutual Fund page dated 20 Feb 2026; taxguru) say no change, but I could not read the Acts (403 errors). Section numbers under the new Act: secondary sources conflict (195/196 vs 197/198). Do not cite section numbers from this report.
- Surcharge and 4% cess on top of these rates. Not checked.
- Which lots are treated as sold first (FIFO) when you sell part of a holding. Not checked.
- Set-off and carry-forward of capital losses. Not checked.
- That smallcase delivery investing is always taxed as capital gains rather than business income. Not checked.
- Note a stale statement on smallcase's own page: "How to Sell a smallcase" (13 Jan 2026) says short-term profit is "taxed at 15%" and long-term "at 10%" above Rs 1.25 lakh. That is inconsistent with the CBDT FAQ (20% and 12.5%). Follow the CBDT figures; the smallcase page is wrong or stale.

**How rebalancing triggers tax:** every rebalance that sells shares is a transfer. Gain or loss is measured against your purchase cost, and the holding period runs from the purchase date of the shares sold. smallcase's own rebalancing blog (9 Apr 2026) says sold stocks "create realised gains or losses relative to your average buying price" and lists "potential capital gains" as a cost of rebalancing, but gives no tax rate. Notably, buying with fresh SIP lots creates many lots with different holding periods.

**Dividends:** shares in your demat pay dividends to you directly. The treatment is slab-rate taxation, with TDS of 10% where dividends from a company exceed Rs 10,000 in a year (raised from Rs 5,000 with effect from 1 Apr 2025). **UNVERIFIED** from official sources: I only have secondary sites (taxguru, Motilal Oswal, Quicko) and one of them notes the new Act may differ. Budget 2026-27 PIB highlights do not mention a dividend change for retail shareholders. Also **UNVERIFIED:** one blog claimed that from 1 Apr 2026 interest cannot be deducted against dividend income; I found no second source.

## 7. Investor protections and risks

**SEBI framework (what I verified in the Feb 2026 master circulars):**
- RAs must display their name as registered with SEBI, registration number, address, compliance officer and grievance officer on their website and in client correspondence (RA Master Circular).
- Model-portfolio rules: a factsheet, rationale, methodology, "true to label" naming, investment horizon, predefined update frequency, rebalance communicated with rationale, risk disclosure, and a benchmark with performance "duly validated by agency/body as specified by SEBI" (Annexure A).
- No claims of returns or assured performance: SEBI's advertisement rules bar "reference to past performance or risk-return metrics" unless "verified by Past Risk and Return Verification Agency (PaRRVA)" and made in the SEBI-specified manner (RA Master Circular, advertisement clause).
- Interim rule before PaRRVA: certified past performance may be given "only on specific request" and "on a one-to-one basis" and "shall not be made available to general public through public media/website of RA" (para 23, RA Master Circular, 6 Feb 2026).
- RA registration "remains valid till it is suspended or cancelled. There is no requirement of renewal", subject to fees every five years (SEBI RA FAQ, 23 Jul 2025).
- Terms disclosed to clients (MITC) must state that the RA may suspend or terminate services on suspension or cancellation of registration, and must refund the residual fee (RA Master Circular, MITC annex).
- PaRRVA status: reported as live from 4 May 2026 with enrolment extended to 3 Sep 2026 by a circular of 3 Aug 2026 (Outlook Money, 4 Aug 2026). I did not read the SEBI circular itself. **UNVERIFIED** at primary level.
- Open tension I could not resolve: smallcase pages show manager returns publicly, with the wording "validated by an independent CA, in line with SEBI guidelines" and "not verified by PaRRVA". The SEBI interim rule above says that kind of CA-certified data should go only to clients on request, one to one. smallcase's position is that it is "a tool to communicate factual & verifiable returns on behalf of the portfolio creator. It should not be considered as an advertisement". I do not know how SEBI treats this. Read published returns as manager-reported, not SEBI-verified.

**Risks and limits:**
- Past performance is not a guide: "Past performance is no guarantee of future results" (smallcase factsheet, 8 Oct 2026). "Registration with SEBI ... is not a guarantee or assurance of future returns."
- Returns shown by smallcase exclude your costs: "transaction fees and other related costs" are not in the index (smallcase Return Calculation Methodology, undated).
- Execution gap: smallcase computes rebalances at the T+1 OHLC average because "It is unlikely that these investment transactions will be executed at the previous day's close price" (same page). Your fills will differ; for small-cap baskets the gap can be larger (the factsheet itself flags "average liquidity").
- smallcase says its data comes from exchange-approved vendors and "has neither been audited nor validated by the Company" (factsheet and methodology pages).
- **Exit liquidity:** you hold exchange-traded shares, there is no lock-in, and you can sell any time during market hours (smallcase, 13 Jan 2026). In illiquid small-caps, selling your own quantity can move the price. No smallcase page quantifies this.
- **Manager stops publishing / is suspended / disappears:** **UNVERIFIED.** I found no smallcase page that says what happens. Facts I do have: you keep the shares in your own demat; you can exit any time; on a fee-based smallcase you lose updates when the subscription lapses; SEBI's MITC wording says services may end on suspension or cancellation of registration and that unexpired fees are refundable. How smallcase flags a dead or suspended manager in the app is unknown.
- Concentration risk: the factsheet example holds 15-20 small-caps with a "High Volatility" label and a 3-4 year suggested horizon.
- Investment Reminder and AutoSIP can fail or lapse if you or your mandate do not act; the reminder form requires you to log in and place the order each time.

## 8. How to check a manager, and how to read a smallcase page

**Check the registration:**
1. On the smallcase page or factsheet, copy the manager's name and "SEBI Reg No" (factsheet example format: INH000018258, "BSE Reg No" 6367). RA numbers on the pages I saw start INH, IA numbers INA (e.g. EIMPL INA000017912).
2. Look the number up on SEBI's registered Research Analyst list: `https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpi=yes&intmId=14`. I opened it: "Registered intermediaries as on date Oct 08, 2026", 2,271 records, each with name, registration number, address, contact and a "Validity" field such as "Apr 13, 2026 - Perpetual". Search by name or registration number. I did not open the Investment Adviser list; the same section of SEBI's site has one, but I did not verify its URL.
3. Check that name, number and "Validity" match, that it is not shown as suspended or cancelled, and that the entity is the one selling the service (an RA number does not cover portfolio management or advice under an IA licence; Windmill's disclosures list separate RA and PMS numbers).
4. Confirm the manager's own website shows the same number, as SEBI requires it to be displayed.
5. Open the manager's disclosures and complaint data (the RA Master Circular requires complaint data to be displayed, Annexure E).
6. SEBI's intermediary portal snippet said RA/IA registration administration had moved to BSE; I could not verify this. Use SEBI's list as the first check.

**Read the page honestly:**
- **Live vs backtested.** smallcase's headline numbers use only live data from the launch date ("Returns and CAGR numbers don't include backtested data", factsheet). Check the factsheet date line (the example reads "Last updated on: October 08, 2026") and the Launch Date field (example: November 12, 2021).
- **CAGR since launch.** The label "15.3% CAGR" on the example is the annual rate "from the date of launch"; for portfolios live less than one year it shows absolute returns instead. A CAGR since launch depends on the start date: a basket launched in a trough looks better than the same logic launched at a peak. Always compare the same period against the benchmark index the page offers (Nifty 50, 100, Midcap 150, Smallcap 100, etc.).
- **Launch date vs track record.** SEBI defines "launch date" as the date the model portfolio report was issued. A short life means little statistical evidence.
- **Minimum amount.** Use the minimum investment on the page, but also read the manager's own note. The example says the minimum is the platform's, while the manager "recommended" Rs 5 lakh for "cost efficiency". If a basket's recommended amount is far above the minimum, fixed costs per order (Rs 118, DP per scrip) eat more of a small investment.
- **Costs are not in the returns.** Subtract the Rs 118 lump-sum fee, per-scrip DP on sells, STT, stamp duty, the manager's subscription and tax.
- **Volatility label, horizon, rebalance frequency and last/next rebalance dates** are on the factsheet. A monthly-rebalance basket means about 12 sell/buy cycles a year, each a tax event.
- **Methodology page:** the platform shows at most history from 1 Jan 2019, and the index does not include costs.

## 9. Worked examples (hypothetical, assumptions stated)

**Common assumptions.** Zerodha charges as in 5c (the only broker whose full page I have read for smallcase fees plus statutory charges). Basket of 15 stocks. 18% GST on the platform fee. Gains and prices are invented to show the mechanics; they are not a forecast. Rs 99,000 of the Rs 1,00,000 lands in shares and Rs 1,000 is left unallocated (leftover cash assumed, **UNVERIFIED** behaviour). Arithmetic done by script.

### 9a. Rs 1,00,000 lump sum into a free smallcase, held 24 months

| Step | Item | Rs |
|---|---|---|
| Entry | smallcase fee: Rs 100 + 18% GST (1.5% of 1,00,000 = 1,500, so the Rs 100 applies) | 118.00 |
| | Brokerage (Zerodha delivery) | 0 |
| | STT 0.1% on 99,000 | 99.00 |
| | NSE transaction charge 0.00307% | 3.04 |
| | SEBI fee + GST on charges | 0.66 |
| | Stamp duty 0.015% | 14.85 |
| | **Entry total** | **235.55** |
| Year-1 rebalances (applied by investor) | Assume rebalances sell Rs 40,000 across 6 scrips and rebuy Rs 40,000. smallcase fee Rs 0. Sell side: STT 40.00, exchange/SEBI/GST 1.50, DP 6 x 15.34 = 92.04. Buy side: STT 40.00, charges 1.50, stamp 6.00 | 181.03 |
| | Realised gain assumed Rs 4,000 (STCG). Tax 20% | 800.00 |
| Exit at month 24 | Assume sale value Rs 1,25,000. STT 125.00, exchange/SEBI/GST 4.67, DP 15 x 15.34 = 230.10. smallcase fee Rs 0 | 359.78 |
| | Remaining gain = (1,25,000 - 99,000) - 4,000 = Rs 22,000, assumed long-term, below the Rs 1.25 lakh yearly exemption. LTCG tax | 0 |
| **All-in cost, free smallcase** | 235.55 + 181.03 + 359.78 + 800.00 | **about Rs 1,576 (1.6% of Rs 1,00,000)** |

Sensitivities:
- If the investor's Rs 1.25 lakh LTCG exemption is already used up by other equity sales in the year, LTCG tax would be 12.5% x 22,000 = Rs 2,750 instead of nil.
- If the investor does not apply the rebalances, there is no STCG and no year-1 trade costs: total about Rs 595 (235.55 + 359.78) and tax nil. But the basket then drifts from the manager's design.
- If the smallcase is paid at the factsheet-example price, Rs 8,400 a year, two years is Rs 16,800, which would push all-in costs to about Rs 18,376. That is 65% of the assumed Rs 26,000 gross gain. Even a single year at Rs 8,400 is 32% of it.
- Any broker that charges per-order delivery brokerage (Groww, Upstox, Angel One in 5c) adds to this. At Rs 20 per executed order across 15 stocks, entry could carry up to about Rs 300 plus GST, plus the same on the Rs 40,000 rebalance buys and sells and on exit. **UNVERIFIED** whether smallcase orders are charged this way.
- Dividends received are extra and taxed at the investor's slab (section 6, UNVERIFIED at primary level).

### 9b. Rs 10,000 a month AutoSIP for 24 months (free smallcase, Zerodha)

Precondition: the basket's minimum investment must be Rs 10,000 or less, and the broker must offer AutoSIP (Zerodha does; Groww does not). If the minimum is higher, this SIP is not possible as stated.

| Item | Rs |
|---|---|
| smallcase AutoSIP fee: Rs 10 + 18% GST = Rs 11.80 a run (1.5% of 10,000 = 150, so Rs 10 applies) x 24 | 283.20 |
| Statutory on each Rs 10,000 buy (STT 10.00, stamp 1.50, exchange/SEBI/GST 0.37) = 11.87 x 24 | 284.98 |
| Brokerage | 0 |
| Total invested Rs 2,40,000; assumed exit value Rs 2,70,000 (gross gain Rs 30,000) | |
| Exit costs: STT 270.00, exchange/SEBI/GST 10.10, DP 15 x 15.34 = 230.10; smallcase fee Rs 0 | 510.20 |
| Tax: of the Rs 30,000 gain, assume Rs 7,000 sits in lots under 12 months (STCG 20% = Rs 1,400) and Rs 23,000 in lots over 12 months (LTCG, below the Rs 1.25 lakh exemption, nil) | 1,400.00 |
| **All-in cost, free smallcase, no rebalances applied** | **about Rs 2,478 (1.03% of Rs 2,40,000)** |

Notes:
- If the same SIP is run as an Investment Reminder (Groww, or any broker where AutoSIP is not available) the fee per top-up is Rs 100 + GST = Rs 118, which is 10 times the AutoSIP fee. 24 top-ups = Rs 2,832 in platform fees, instead of Rs 283. At the Rs 10,000 amount 1.5% is Rs 150, so the Rs 100 cap is the binding number. Whether Zerodha applies Rs 100 or Rs 10 to a reminder-based top-up is **UNVERIFIED** (its charges page is undated and still shows "SIP: 10").
- Rebalances were left out here. Each applied rebalance adds trade costs and possible STCG as in 9a.
- Because AutoSIP buys whole shares at fixed counts, weights will not match the manager's target after each run, and some of each Rs 10,000 will not be deployed (**UNVERIFIED** treatment of the residual).
- FIFO or specific-lot treatment of which SIP lots are sold first was not checked; the 7,000/23,000 split is an assumption.

## 10. The facts that matter most

1. smallcase is a technology layer; the manager is the SEBI-registered RA or IA and the shares sit in your own demat.
2. Manual SIP was retired (4 May 2026). Real automated SIP exists only at some brokers (Zerodha, SBI Sec, HDFC Sec, Axis Sec, ICICI Sec, Kotak Neo); Groww has none.
3. Platform fee: Rs 100 + GST per lump-sum or reminder top-up (capped at 1.5% of the amount), Rs 10 + GST per AutoSIP run, nothing on rebalance or exit. On a small Rs 5,000 top-up the cap makes it 1.5% = Rs 75 + GST = Rs 88.50, which is still a 1.8% drag before any other cost.
4. Costs that bite are the manager's subscription (example Rs 8,400 a year) and exit-time DP charges per scrip (Rs 15.34 each at Zerodha, Rs 20 + GST at Upstox and Angel One), not the headline fee.
5. Rebalances are never automatic and every sell is a taxable event: 20% STCG under 12 months, 12.5% LTCG above Rs 1.25 lakh a year for transfers on or after 23 Jul 2024.

## 11. What I could not verify

- Whole-share-only behaviour, leftover cash handling, fractional shares.
- Whether each AutoSIP run buys every stock in 2026 (2023 blog says same share counts; developer docs describe splitting across instalments).
- AutoSIP availability at Upstox, Angel One and others; the exact bank mandate flow; current frequency options and exact minimums at each broker.
- Angel One's smallcase platform fee; fee at HDFC/ICICI/Dhan/Kotak; whether brokers' per-order delivery brokerage applies to smallcase constituent orders.
- The GST rate on the smallcase fee on a smallcase page; Zerodha's treatment of Investment Reminder fees.
- Whether the Income-tax Act 2025 and Finance Act 2026 left 20%/12.5%/Rs 1.25 lakh untouched (PIB highlights show no change; Acts unread). Surcharge/cess, FIFO and loss set-off. Dividend taxation and the TDS threshold (secondary sources only).
- What happens if a manager stops publishing, is suspended, or retires a smallcase.
- PaRRVA's operational status at primary level; how public display of CA-certified returns squares with SEBI's interim one-to-one rule.
- Who runs RA/IA registration after the reported move to BSE; the URL of the IA search list.
- Conflicts left unresolved: Upstox help vs the Aug 2026 Upstox notice (Rs 10 vs Rs 100 for non-auto SIP); smallcase's "no refund" subscription wording vs SEBI's proportionate-refund rule; smallcase sell page quoting 15%/10% tax.

## 12. Sources (all opened 2026-10-09)

smallcase
- Fees and charges: https://www.smallcase.com/learn/smallcase-fees-and-charges/ (15 Jan 2026)
- Transaction charges notice: https://www.smallcase.com/blog/transaction-charges-for-smallcases-on-zerodha-have-been-revised/ (15 Jan 2026, despite the URL)
- Groww notice: https://www.smallcase.com/blog/transaction-charges-for-smallcases-on-groww-have-been-revised/ (13 Aug 2026)
- Upstox notice: https://www.smallcase.com/blog/transaction-charges-for-smallcases-on-upstox-have-been-revised/ (13 Aug 2026)
- Investment Reminders: https://www.smallcase.com/blog/say-hello-to-investment-reminders-a-smarter-way-to-stay-consistent/ (4 May 2026)
- Pricing FAQ: https://www.smallcase.com/blog/faqs-pricing-smallcases/ (11 Nov 2022)
- Charges page: https://www.smallcase.com/blog/charges-associated-with-smallcases-now-more-transparent-and-simpler/ (18 Oct 2021)
- Subscription: https://www.smallcase.com/learn/how-does-smallcase-subscription-work/ (15 Jan 2026)
- How to invest: https://www.smallcase.com/learn/how-to-invest-in-smallcase/ (12 Jan 2026)
- How to sell: https://www.smallcase.com/learn/how-to-sell-a-smallcase/ (13 Jan 2026)
- What is a smallcase: https://www.smallcase.com/learn/what-is-smallcase/ (15 Jan 2026)
- SIP explainers: https://www.smallcase.com/blog/understanding-sips-in-smallcases/ (6 Oct 2023), https://www.smallcase.com/blog/musings-with-analyst-september-2023/ (7 Oct 2023), https://www.smallcase.com/learn/how-to-invest-in-sip/
- Rebalancing: https://www.smallcase.com/blog/rebalancing-101/ (15 Jan 2026), https://www.smallcase.com/blog/what-happens-if-i-miss-a-rebalance-update/ (5 Sep 2025), https://www.smallcase.com/blog/rebalancing-a-windmill-capital-smallcase-everything-you-need-to-know/ (9 Apr 2026)
- Return methodology: https://www.smallcase.com/meta/return-calculation/ (undated); Disclosures: https://www.smallcase.com/meta/disclosures/ (undated)
- Check-before-investing guide: https://www.smallcase.com/blog/8-things-to-check-before-investing-in-a-smallcase-your-essential-guide/ (19 Jun 2024)
- Developer docs: https://developers.gateway.smallcase.com/docs/smallcase-orders (undated)
- Example factsheet PDF (used only to show page structure, not an endorsement): https://assets.smallcase.com/factsheets/QUREMO_0018.pdf (8 Oct 2026)
- Investor help example: https://investorai.smallcase.com/help (undated)

Brokers
- https://zerodha.com/charges; https://groww.in/pricing; https://upstox.com/brokerage-charges/; https://www.angelone.in/pricing; https://upstox.com/help-center/t-248924 (smallcase charges); https://upstox.com/help-center/t-248919 (rebalancing); https://groww.in/help/stocks,-f&o,-ipo-&-mtf/searchable/what-are-smallcase-charges-on-groww--78 (undated)

SEBI and government
- SEBI Master Circular for Research Analysts, 6 Feb 2026: https://www.sebi.gov.in/legal/master-circulars/feb-2026/master-circular-for-research-analysts_99571.html (PDF https://www.sebi.gov.in/sebi_data/attachdocs/feb-2026/1770375507051.pdf)
- SEBI Master Circular for Investment Advisers, 6 Feb 2026: https://www.sebi.gov.in/legal/master-circulars/feb-2026/master-circular-for-investment-advisers_99569.html
- SEBI Guidelines for Research Analysts, 8 Jan 2025: https://www.sebi.gov.in/legal/circulars/jan-2025/guidelines-for-research-analysts_90634.html
- SEBI RA FAQ, 23 Jul 2025: https://www.sebi.gov.in/legal/circulars/jul-2025/frequently-asked-questions-faqs-related-to-regulatory-provisions-for-research-analysts_95549.html
- SEBI registered RA list (as on 8 Oct 2026): https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpi=yes&intmId=14
- CBDT capital gains FAQ, 24 Jul 2024: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2036604
- PIB Highlights of Union Budget 2026-27, 1 Feb 2026: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2221455
- PIB Income Tax Act 2025 release, 1 Feb 2026: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2221416
- PIB Budget 2025-26 direct tax release, 1 Feb 2025: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2098362 (read; it did not state the dividend TDS threshold)
- Secondary only: Outlook Money on PaRRVA enrolment (4 Aug 2026), Tata Mutual Fund post-budget page (20 Feb 2026), taxguru/Motilal Oswal/Quicko on dividend TDS.
