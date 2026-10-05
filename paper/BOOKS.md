# Paper-trading books (FROZEN as of 2026-10-05; first signal date 2026-10-30)

Forward-only test: nothing before 2026-10-30 is simulated. Each book starts with Rs 10,00,000 (US books in USD-equivalent return terms, no FX).
Do not edit parameters. A new idea = a new book with its own start date, declared here BEFORE it starts.

| Book | Market | Logic | Status of evidence |
|---|---|---|---|
| IN_rebal | India, Nifty 500 | The frozen candidate (reports/FROZEN_RULES.md): Nifty 500 > 200d MA regime, filters, momentum/vol rank, top 25, monthly rebalance, 30% stop, 25 bps, 6% cash | Tune pass; 2019-26 test: beat Nifty and random on return, failed drawdown vs random |
| IN_hold | India, Nifty 500 | Pre-declared challenger: same filters/regime/rank, top 40, hold until 40% stop or close below 200d MA, new names fill free slots | Tune only; best drawdown cell in the grid |
| US_rebal | US, S&P 500 | Same rule as IN_rebal with S&P 500 regime, 10 bps, 1% cash | Tune: failed drawdown vs SPY; unvalidated |
| US_hold | US, S&P 500 | Same as IN_hold | Tune only; unvalidated |
| INS_hold | India, Nifty Smallcap 250 | IN_hold logic on small caps, 40 bps assumed cost (declared 2026-10-05, before start) | Tune only, survivors: 22.3% / -29.4%, 19 trades >= 3x |
| INM_hold | India, Nifty Microcap 250 | IN_hold logic on micro caps, 75 bps assumed cost (declared 2026-10-05, before start) | Tune only, survivors: 28.3% / -33.7%, 17 trades >= 3x; worst survivor bias |
Benchmarks: Nifty BeES (India, dividend-adjusted) and SPY (US).

Universe: current index members, re-snapshotted on every run into paper/universe/ (dated). From now on membership is point-in-time: a name is eligible at date d only if it
was in the latest snapshot on or before d. This builds the point-in-time membership history that is missing for the past.

Kill-switches (from the skeptic's report): WARNING at -25% drawdown from peak, HARD STOP at -35% (stop trading the book), review if underwater > 30 months.
Judgement after 12 months, per book: beat benchmark return AND drawdown shallower than benchmark. Anything less = not proven.

Files: STATUS.md (latest summary), nav_<book>.csv, holdings_<book>.csv, signal_log.csv (append-only; what the engine said each run), universe/.
Run: `python paper/paper_trade.py` (needs pandas numpy yfinance requests lxml html5lib pyarrow). Scheduled weekly (Fri 22:17 UTC).
