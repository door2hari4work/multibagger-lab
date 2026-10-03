# US quality gate on SEC point-in-time data (tune window 2010-2018 only; US 2019+ test untouched)

Data: SEC XBRL companyfacts for current S&P 500 members (fetch_sec.py). Annual 10-K figures, ORIGINAL (earliest-filed) value, usable from the
filing date. EBITDA = operating income + D&A, with documented fallbacks (D&A = depreciation + intangible amortisation; EBIT = pre-tax income +
interest). 471 of 503 symbols have usable data; 384 had filings by 2018. Financials excluded by the gate. Survivor-biased universe.
Rule: same as the India candidate (Nifty->S&P 500 > 200d MA regime, momentum/vol rank, top 25, 30% stop), 10 bps/side, 1% cash.
Gate (untuned placeholders from pit_gate.py): EBITDA margin up YoY, revenue and EBITDA growth >= 10%, OCF/EBITDA >= 0.5.

| Variant (8 declared, none dropped) | CAGR | Max DD | 2018 | Avg names passing | Final Rs (from 10,00,000) |
|---|---|---|---|---|---|
| G0 no gate, full universe | 16.2% | -20.8% | +10.9% | 452 | 38,52,026 |
| G1 no gate, covered non-financial names (fair baseline) | 14.6% | -18.4% | +6.2% | 265 | 33,92,953 |
| G2 full gate | 8.6% | -22.8% | +8.6% | 33 | 21,07,235 |
| G3 full gate, ignore filing date, 90-day lag | 10.4% | -22.1% | +8.0% | 37 | 24,38,029 |
| G4 growth threshold 5% | 11.1% | -21.3% | +10.7% | 54 | 25,71,203 |
| G5 growth threshold 15% | 5.8% | -20.8% | +6.8% | 21 | 16,61,097 |
| G6 margin trend only | 12.5% | -19.4% | +4.6% | 113 | 28,93,571 |
| G7 cash quality only | 13.3% | -17.8% | +8.5% | 189 | 30,70,429 |
| SPY (total-return proxy) | 11.4% | -19.3% | | | |
Random picks inside the full-gate pool (30 runs): median 8.5% / -22.5%, i.e. the momentum ranking added nothing once the gate had picked the pool.

## Verdict: the quality gate does NOT help in this test. It cuts return by about 6 points a year versus the same covered universe and does not reduce drawdown.
- Every gated variant has lower CAGR than ungated (G1). The best single component (cash quality only) gives 1.3 pts less CAGR and a 0.6-pt
  shallower drawdown, which is noise-level. Stricter growth (G5) is worst: fewer than 21 names pass on average.
- Likely reasons (hypotheses, not proven): momentum already selects improving businesses, so the gate mostly removes cyclical rebounds and
  recovering names; annual data lags up to a year; very concentrated pools (20-50 names) raise single-name risk.
- Caveats: gate thresholds untuned (tuning them toward a pass would be data mining); 57.5% data coverage of symbol-months (early years thin,
  XBRL only from ~2009-11); annual rather than quarterly data; survivors only; EBITDA tag fallbacks differ across companies; 32 symbols missing
  (REITs, insurers, a few like GOOGL and XOM with unusual tags); US-only evidence, India untestable.
- The US strategy without the gate also failed the drawdown criterion in tune (see us_tune.py: -20.8% vs SPY -19.3%), so no US rule was frozen and the
  sealed US 2019+ data was not used.
