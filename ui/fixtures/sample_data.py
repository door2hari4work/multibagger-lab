"""SYNTHETIC sample data for the UI. Every company, ticker, price, number and source here is invented; nothing is research about a real firm.
Tickers are fictional. URLs use the reserved .invalid domain. Used only when the real thesis store is empty."""
from __future__ import annotations
from mblab.schema import (Thesis, Evidence, ScoreComponent, Scenario, Catalyst, EntryPlan, ExitTrigger, AdversarialReview, PortfolioFit)

SAMPLE_AS_OF = "2026-10-05"
SAMPLE_NOTE = "SAMPLE (synthetic, fictional company)"
_URL = "https://filings.example.invalid/"


def _ev(i, claim, kind, stype="", date="", period="", note=""):
    return Evidence(id=i, claim=claim, kind=kind, source_type=stype, source_url=(_URL + i) if stype in ("filing", "call", "exchange", "investor_presentation", "news") else "",
                    source_date=date, period=period, note=note)


def _scores(**kw):
    out = []
    for name, v in kw.items():
        val, basis = v if isinstance(v, tuple) else (v, "")
        out.append(ScoreComponent(name=name, value=val, basis=basis, data_quality="ok" if val is not None else "missing"))
    return out


def _overall(scores):
    vals = [s.value for s in scores if s.value is not None]
    return round(sum(vals) / len(vals), 2) if vals else None


def _mk(**kw) -> Thesis:
    t = Thesis(**kw)
    t.overall_score = _overall(t.scores)
    return t


def sample_theses() -> list:
    out = []

    out.append(_mk(
        ticker="QGRD", company="Quillon Grid Systems (sample)", market="US", version=3, status="attractive_entry", research_level=5, as_of="2026-10-02",
        created_at="2026-10-02T06:10:00+00:00", price=41.8, price_ts="2026-10-02", currency="USD", time_horizon_months=24, confidence="medium", next_review="2026-11-14",
        why_now="Order backlog doubled in two quarters and the share price pulled back to its 50-day average while the backlog was growing, so the setup looks better than a month ago.",
        thesis="Quillon makes grid-scale power electronics. Utilities are replacing ageing equipment, and Quillon's newest product wins share because it cuts installation time.",
        multibagger_mechanism="Revenue is small today. If backlog converts at current margins and a second factory fills, profit could grow several times, and investors usually pay a higher multiple for visible growth.",
        expectations_gap="Most analysts model backlog turning into revenue slowly. Faster conversion is the main surprise. If a second large utility signs on, the market may treat Quillon as a platform instead of a supplier.",
        bull_case=Scenario("bull", "Two more utility contracts and margins reach the top of management's range.", 4.0, 7.0, 0.15, 24),
        base_case=Scenario("base", "Backlog converts on schedule, margins improve modestly.", 1.8, 2.8, 0.45, 24),
        bear_case=Scenario("bear", "Contract delays and a component shortage push profit out by two years, and the multiple compresses.", 0.5, 0.75, 0.40, 24),
        catalysts=[Catalyst("Second factory begins shipments", "Q1 FY27 results (Feb 2027)", "pending", ["QG-3"]), Catalyst("Utility framework contract renewal", "Dec 2026", "pending", ["QG-4"]),
                   Catalyst("Backlog disclosure above $400m", "Q3 FY26 results", "occurred", ["QG-1"])],
        risks=["One utility is 38% of backlog; a delay there would hurt twice.", "Gross margin depends on a single imported component.", "Valuation already assumes about 30% annual revenue growth."],
        valuation={"ev_sales": 5.2, "ev_ebitda": 28.0, "pe_fwd": 36.5, "fcf_yield": 0.9, "market_cap": 2150},
        scores=_scores(business_quality=(0.7, "Gross margin 34%, steady for four years"), growth_acceleration=(0.82, "Revenue growth 41% year on year, up from 22%"),
                       earnings_inflection=(0.75, "Operating margin turned positive two quarters ago"), tam_expansion=(0.65, "Grid replacement spend rising in US and EU"),
                       catalyst_strength=(0.7, "Two dated catalysts inside 6 months"), competitive_advantage=(0.6, "Faster installation, but patents are narrow"),
                       valuation_asymmetry=(0.55, "Priced for growth; upside needs execution"), market_confirmation=(0.78, "Above 200-day average, relative strength top decile"),
                       timing=(0.72, "Pullback to 50-day average on lower volume"), risk=(0.45, "Customer concentration and single-source part"),
                       thesis_robustness=(0.62, "Survived adversarial review with a downgrade of the bull case"), portfolio_fit=(0.6, "Adds US industrials, low overlap")),
        entry=EntryPlan("attractive_entry", [38.0, 42.0], [42.0, 46.0], [50.0, 56.0], [34.0, 37.0], 33.0,
                        "Ideal zone is the 50-day average band plus one ATR below it. The chase zone starts about 20% above that band."),
        exit_rules=[ExitTrigger("thesis_invalidation", "Backlog falls below $300m or the lead utility cancels", "armed"), ExitTrigger("earnings_deterioration", "Gross margin below 28% for two quarters", "armed"),
                    ExitTrigger("valuation_excess", "EV/Sales above 9 without a matching rise in guidance", "armed")],
        adversarial=AdversarialReview(True, "skeptic-agent", "downgraded", "A single-customer delay plus a part shortage could erase two years of growth, and the valuation leaves no room.",
                                      {"What would make this a value trap?": "Backlog that never converts because of utility budget cycles.", "Who is on the other side of this trade?": "Funds who see Quillon as a cyclical supplier and size it small."},
                                      "2026-09-28"),
        portfolio_fit=PortfolioFit(0.6, "Adds US industrial exposure. Low overlap with your current India-heavy holdings.", ["Moderate overlap with other power-equipment names if you add more."], 4.0),
        evidence=[_ev("QG-1", "Reported backlog of $412m, up from $198m two quarters earlier.", "FACT", "filing", "2026-09-18", "Q2 FY26"),
                  _ev("QG-2", "Gross margin was 34.1% for the quarter.", "FACT", "filing", "2026-09-18", "Q2 FY26"),
                  _ev("QG-3", "Management said the second factory starts shipping by February.", "FACT", "call", "2026-09-19"),
                  _ev("QG-4", "The framework contract with the lead utility is likely to be renewed on similar terms.", "INFERENCE", note="Based on two prior renewals"),
                  _ev("QG-5", "A hyperscaler could become a customer for the same product.", "SPECULATION")],
        change_log=["Adversarial review completed", "entry state: setup_forming -> attractive_entry", "new evidence: QG-2"], parent_version=2))

    out.append(_mk(
        ticker="VLDM", company="Veldt Microsystems (sample)", market="IN", version=2, status="preparing_to_enter", research_level=4, as_of="2026-10-03",
        created_at="2026-10-01T06:10:00+00:00", price=1865.0, price_ts="2026-10-03", currency="INR", time_horizon_months=18, confidence="medium", next_review="2026-10-25",
        why_now="Quarterly profit more than doubled and the stock is forming a base just under its recent high. Entry zones are drafted but price is not there yet.",
        thesis="Veldt designs sensors for electric two-wheelers. Volume is rising with vehicle sales, and each new model carries more of Veldt's content per vehicle.",
        multibagger_mechanism="Content per vehicle rises each model year while vehicle volumes grow. Together these could multiply revenue, and operating leverage could lift profit faster.",
        expectations_gap="The market treats Veldt as a small auto supplier. If exports to Southeast Asia start in FY27, the revenue base is larger than most estimates assume.",
        bull_case=Scenario("bull", "Exports start on time and content per vehicle rises 30%.", 3.5, 5.5, 0.15, 18),
        base_case=Scenario("base", "Domestic growth continues, exports are small.", 1.5, 2.2, 0.50, 18),
        bear_case=Scenario("bear", "Two-wheeler demand slows and a larger rival wins the next platform.", 0.55, 0.8, 0.35, 18),
        catalysts=[Catalyst("Export pilot order", "H2 FY27", "pending"), Catalyst("New platform award from top-3 OEM", "Jan-Mar 2027", "pending")],
        risks=["Top customer is 44% of sales.", "Subsidy changes could slow electric two-wheeler demand.", "Thin trading: about Rs 4 crore a day."],
        valuation={"pe_ttm": 41.0, "ev_ebitda": 24.5, "roce": 0.22, "mcap_cr": 3100},
        scores=_scores(business_quality=(0.66, "ROCE 22%, low debt"), growth_acceleration=(0.78, "Sales up 36%, previous year 19%"), earnings_inflection=(0.8, "Profit after tax up 112% year on year"),
                       tam_expansion=(0.6, "Electric two-wheeler penetration still low"), catalyst_strength=(0.55, "Both catalysts are undated"), competitive_advantage=(0.5, "Switching cost is real but modest"),
                       valuation_asymmetry=(0.45, "Not cheap on trailing earnings"), market_confirmation=(0.7, "Within 6% of 52-week high"), timing=(0.5, "Base still forming"),
                       risk=(0.4, "Liquidity and customer concentration"), thesis_robustness=(0.58, "Review done, bear case partly unanswered"), portfolio_fit=(0.7, "New sector for you")),
        entry=EntryPlan("setup_forming", [1680.0, 1760.0], [1760.0, 1830.0], [1980.0, 2100.0], None, 1540.0, "Ideal zone sits at the 50-day average band and the base lows. Price is about 6% above it."),
        exit_rules=[ExitTrigger("thesis_invalidation", "Top customer cuts orders by more than 25%", "armed"), ExitTrigger("technical", "Weekly close below Rs 1,540", "armed")],
        adversarial=AdversarialReview(True, "skeptic-agent", "survives", "Customer concentration: losing one platform would remove a third of profit.", {}, "2026-09-26"),
        portfolio_fit=PortfolioFit(0.7, "Adds auto-electronics, a sector you do not hold.", [], 3.0),
        evidence=[_ev("VL-1", "Profit after tax rose 112% year on year to Rs 41 crore.", "FACT", "exchange", "2026-09-12", "Q2 FY27"),
                  _ev("VL-2", "Management guided to two new platform launches in H2.", "FACT", "call", "2026-09-13"),
                  _ev("VL-3", "Export orders are likely to start within a year.", "INFERENCE"),
                  _ev("VL-4", "A global sensor maker may acquire Veldt.", "SPECULATION")],
        change_log=["Level 4 research completed", "status: 'watchlist' -> 'preparing_to_enter'", "new evidence: VL-1, VL-2"], parent_version=1))

    out.append(_mk(
        ticker="HRBL", company="Harbourline Specialty Chemicals (sample)", market="IN", version=1, status="watchlist", research_level=3, as_of="2026-09-29",
        created_at="2026-09-29T06:10:00+00:00", price=912.0, price_ts="2026-10-03", currency="INR", time_horizon_months=24, confidence="low", next_review="2026-11-05",
        why_now="Capacity doubles next year, but the stock has run 25% in six weeks. The business looks interesting; the price does not yet.",
        thesis="Harbourline makes fluorine-based specialty chemicals used in battery materials. A new plant doubles capacity in 2027.",
        multibagger_mechanism="If the new plant fills and prices hold, revenue could roughly double with little extra cost, which lifts profit by more than revenue.",
        expectations_gap="The market has priced in the capacity. It may not have priced in how long qualification with battery makers takes.",
        bull_case=Scenario("bull", "Plant fills in two quarters and prices hold.", 3.0, 4.5, 0.12, 24),
        base_case=Scenario("base", "Plant fills over four quarters.", 1.3, 1.9, 0.48, 24),
        bear_case=Scenario("bear", "Qualification slips and chemical prices fall.", 0.5, 0.8, 0.40, 24),
        catalysts=[Catalyst("New plant commissioning", "Q2 FY27", "pending")],
        risks=["Commodity-linked pricing.", "Customer qualification can take 12 months or more.", "Environmental clearances."],
        valuation={"pe_ttm": 33.0, "ev_ebitda": 19.0, "net_debt_ebitda": 1.8},
        scores=_scores(business_quality=0.6, growth_acceleration=0.55, earnings_inflection=0.5, tam_expansion=0.7, catalyst_strength=0.5, competitive_advantage=0.55,
                       valuation_asymmetry=0.4, market_confirmation=0.8, timing=0.25, risk=0.4),
        entry=EntryPlan("wait_for_pullback", [790.0, 840.0], None, None, None, None, "Waiting for a pullback toward the 50-day average. Zones are provisional: adversarial review is not done."),
        exit_rules=[],
        evidence=[_ev("HR-1", "The new plant is 85% complete according to the company.", "FACT", "investor_presentation", "2026-08-30"),
                  _ev("HR-2", "Battery customers will qualify the product within two quarters.", "SPECULATION")],
        change_log=["initial version"]))

    out.append(_mk(
        ticker="PNTA", company="Pentara Semicap Tools (sample)", market="US", version=1, status="watchlist", research_level=3, as_of="2026-09-20",
        created_at="2026-09-20T06:10:00+00:00", price=18.4, price_ts="2026-10-03", currency="USD", time_horizon_months=24, confidence="low",
        why_now="Order growth turned positive after four weak quarters, but there is only one quarter of evidence.",
        thesis="Pentara sells inspection tools to chip makers. Orders follow factory spending, which is recovering.",
        base_case=Scenario("base", "Orders recover to the prior peak.", 1.4, 2.0, 0.5, 24),
        bear_case=Scenario("bear", "Factory spending stays weak for another year.", 0.5, 0.8, 0.5, 24),
        risks=["Cyclical: orders can fall 40% in a year."],
        scores=_scores(business_quality=0.55, growth_acceleration=0.5, earnings_inflection=0.45, market_confirmation=0.5, timing=0.4),
        entry=EntryPlan("too_early"),
        evidence=[_ev("PN-1", "Orders grew 9% quarter on quarter, the first rise in a year.", "FACT", "filing", "2026-08-20", "Q2 FY26")],
        change_log=["initial version"]))

    out.append(_mk(
        ticker="TSLY", company="Tessaly Biologics (sample)", market="US", version=1, status="research_required", research_level=2, as_of="2026-10-04",
        created_at="2026-10-04T06:10:00+00:00", price=9.35, price_ts="2026-10-03", currency="USD", confidence="low",
        why_now="A small-cap with accelerating revenue and a recent price breakout. The screen flagged it; the business has not been studied.",
        risks=["Clinical-stage risk is not yet assessed."],
        scores=_scores(growth_acceleration=(0.7, "Revenue up 60% year on year"), market_confirmation=(0.85, "New 52-week high on volume"), business_quality=None),
        entry=EntryPlan("too_early"),
        evidence=[_ev("TS-1", "Revenue grew 60% year on year.", "FACT", "filing", "2026-08-12", "Q2 FY26")],
        change_log=["initial version"]))

    out.append(_mk(
        ticker="MRWL", company="Marrow Logistics Tech (sample)", market="IN", version=1, status="early_discovery", research_level=1, as_of="2026-10-05",
        created_at="2026-10-05T06:10:00+00:00", price=244.0, price_ts="2026-10-03", currency="INR", confidence="low",
        why_now="Flagged by the daily screen for strong price momentum and rising trading volume. No research done.",
        scores=_scores(market_confirmation=(0.77, "Momentum rank in top 5%")), entry=EntryPlan("unknown"), change_log=["initial version"]))

    out.append(_mk(
        ticker="ORRN", company="Orrin Foods (sample)", market="IN", version=4, status="hold", research_level=5, as_of="2026-09-30",
        created_at="2026-09-24T06:10:00+00:00", price=1420.0, price_ts="2026-10-03", currency="INR", time_horizon_months=24, confidence="medium", next_review="2026-12-01",
        why_now="Thesis is on track. One exit condition is showing a warning: volume growth slowed for a second quarter.",
        thesis="Orrin sells packaged snacks in small towns. New distribution reaches more shops each quarter.",
        multibagger_mechanism="Shop count is growing faster than sales per shop is falling, so total sales keep compounding.",
        base_case=Scenario("base", "Shop growth continues at current pace.", 1.4, 1.9, 0.55, 24), bull_case=Scenario("bull", "Margins widen with scale.", 2.5, 3.5, 0.15, 24),
        bear_case=Scenario("bear", "Volume growth stays below 8% and the multiple falls.", 0.6, 0.85, 0.30, 24),
        risks=["Input costs for palm oil.", "Volume growth slowing."], valuation={"pe_ttm": 38.0, "ev_sales": 4.4},
        scores=_scores(business_quality=0.72, growth_acceleration=0.5, earnings_inflection=0.4, valuation_asymmetry=0.35, timing=0.4, risk=0.55),
        entry=EntryPlan("overextended", [1180.0, 1260.0], [1260.0, 1340.0], [1500.0, 1600.0], [1250.0, 1320.0], 1100.0, "Price is above the acceptable zone, so adding is not planned."),
        exit_rules=[ExitTrigger("earnings_deterioration", "Volume growth below 6% for two quarters", "warning"), ExitTrigger("thesis_invalidation", "Shop count stops growing", "armed")],
        adversarial=AdversarialReview(True, "skeptic-agent", "survives", "Small-town demand is price sensitive and rivals can match distribution.", {}, "2026-06-12"),
        evidence=[_ev("OR-1", "Volume growth was 7% in the latest quarter, down from 11%.", "FACT", "filing", "2026-08-30", "Q1 FY27")],
        change_log=["exit trigger moved to warning", "new evidence: OR-1"], parent_version=3))

    out.append(_mk(
        ticker="KLNR", company="Kelner Offshore Services (sample)", market="IN", version=5, status="trim", research_level=5, as_of="2026-10-02",
        created_at="2026-10-02T06:10:00+00:00", price=2380.0, price_ts="2026-10-03", currency="INR", time_horizon_months=18, confidence="medium",
        why_now="The stock reached the valuation level the thesis set as a trim trigger.",
        thesis="Kelner services offshore rigs. The upcycle has largely played out in the share price.",
        base_case=Scenario("base", "Earnings hold but the multiple cannot rise further.", 0.9, 1.2, 0.6, 12), bear_case=Scenario("bear", "Rig demand softens.", 0.55, 0.8, 0.4, 12),
        risks=["Cyclical downturn in rig demand."], valuation={"pe_ttm": 29.0},
        scores=_scores(business_quality=0.6, valuation_asymmetry=0.15, timing=0.2),
        entry=EntryPlan("overextended"),
        exit_rules=[ExitTrigger("valuation_excess", "P/E above 27 with flat earnings guidance", "triggered"), ExitTrigger("thesis_invalidation", "Day rates fall 15%", "armed")],
        adversarial=AdversarialReview(True, "skeptic-agent", "survives", "Most of the easy gain is already in the price.", {}, "2026-05-02"),
        evidence=[_ev("KL-1", "Trailing P/E reached 29, above the 27 trigger.", "FACT", "price", "2026-10-02")],
        change_log=["status: 'hold' -> 'trim'", "exit trigger valuation_excess triggered"], parent_version=4))

    out.append(_mk(
        ticker="BRXT", company="Braxton Solar Cells (sample)", market="US", version=3, status="thesis_broken", research_level=4, as_of="2026-09-26",
        created_at="2026-09-26T06:10:00+00:00", price=6.1, price_ts="2026-10-03", currency="USD", confidence="medium",
        why_now="Not applicable: the thesis no longer holds.", thesis="Braxton planned to lead on a new cell design. The pilot line failed yields, so the core claim is gone.",
        risks=["Pilot-line yields below 40%."], scores=_scores(business_quality=0.3, thesis_robustness=0.1),
        entry=EntryPlan("thesis_deteriorating"), exit_rules=[ExitTrigger("thesis_invalidation", "Pilot yield below 60% by Q3", "triggered")],
        adversarial=AdversarialReview(True, "skeptic-agent", "killed", "The technical claim failed on the company's own numbers.", {}, "2026-09-26"),
        evidence=[_ev("BX-1", "Company reported pilot yields of 38%.", "FACT", "filing", "2026-09-22", "Q2 FY26")],
        change_log=["status: 'watchlist' -> 'thesis_broken'", "adversarial verdict: survives -> killed"], parent_version=2))

    out.append(_mk(
        ticker="DLMR", company="Dalmere Textiles (sample)", market="IN", version=2, status="rejected", research_level=3, as_of="2026-08-10",
        created_at="2026-08-10T06:10:00+00:00", price=330.0, price_ts="2026-10-03", currency="INR", confidence="low",
        why_now="Rejected after review.", thesis="Looked like a turnaround; the review found accounts that did not reconcile.",
        risks=["Receivables grew twice as fast as sales."], scores=_scores(business_quality=0.2, thesis_robustness=0.1), entry=EntryPlan("unknown"),
        adversarial=AdversarialReview(True, "skeptic-agent", "killed", "Receivables growth suggests revenue quality problems.", {}, "2026-08-10"),
        evidence=[_ev("DL-1", "Receivables grew 48% against sales growth of 21%.", "FACT", "filing", "2026-07-30", "Q1 FY27")],
        change_log=["status: 'research_required' -> 'rejected'"], parent_version=1))
    return out


def sample_alerts() -> list:
    return [
        {"severity": "high", "ticker": "KLNR", "kind": "exit trigger", "title": "Kelner Offshore Services hit its valuation exit trigger", "detail": "P/E reached 29 against a trigger of 27, with flat guidance. Review whether to trim.", "ts": "2026-10-02"},
        {"severity": "medium", "ticker": "QGRD", "kind": "entry setup", "title": "Quillon Grid Systems moved into its attractive entry zone", "detail": "Price fell to $41.8, inside the $38 to $42 ideal range. The thesis is unchanged.", "ts": "2026-10-02"},
        {"severity": "medium", "ticker": "ORRN", "kind": "exit warning", "title": "Orrin Foods volume growth slowed again", "detail": "7% against a warning level of 8%. The exit trigger needs two quarters below 6%.", "ts": "2026-09-30"},
        {"severity": "low", "ticker": "VLDM", "kind": "thesis update", "title": "Veldt Microsystems thesis updated to version 2", "detail": "Profit result added. Status moved to getting ready.", "ts": "2026-10-01"},
        {"severity": "info", "ticker": "", "kind": "data", "title": "US price data for 2 tickers is 3 days old", "detail": "Prices refresh at the next scheduled run.", "ts": "2026-10-05"},
    ]


def sample_candidates() -> list:
    return [
        {"ticker": "MRWL", "market": "IN", "name": "Marrow Logistics Tech (sample)", "score": 0.77, "note": "Momentum rank in top 5% with rising volume. No business research yet."},
        {"ticker": "ZNTR", "market": "US", "name": "Zentrell Robotics (sample)", "score": 0.71, "note": "Revenue growth above 50% and a new 52-week high."},
        {"ticker": "OSKR", "market": "IN", "name": "Oskar Defence Electronics (sample)", "score": 0.68, "note": "Order book jump reported to the exchange; price breakout."},
    ]


def sample_portfolio_summary() -> dict:
    return {"currency": "INR", "value": 4850000, "n_holdings": 14, "cash_pct": 0.08,
            "notes": ["Largest sector is financials at 31% of equity.", "India is 82% of the portfolio; US is 18%.", "Sample figures, not a real portfolio."], "as_of": SAMPLE_AS_OF}


def sample_paper_status() -> dict:
    books = [("IN_rebal", "OFF"), ("IN_hold", "OFF"), ("US_rebal", "ON"), ("US_hold", "ON"), ("INS_hold", "OFF"), ("INM_hold", "OFF")]
    return {"books": [{"name": n, "started": "not yet", "regime": r, "nav": 1000000, "benchmark": 1000000, "drawdown": 0.0, "flags": "-"} for n, r in books],
            "note": "Books start at the 2026-10-30 month-end signal. Until then they hold cash, so there is no performance to judge."}
