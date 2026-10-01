# Agent 4 - Fundamentals tester
Gate: EBITDA-margin trend (improving) + revenue/EBITDA growth + operating cash flow quality (OCF/EBITDA, FCF sign).
- Point-in-time only: a value is usable from `filed_date`, or `period_end + lag` (config.py) if filing date unknown.
  Use originally reported values, not restated.
- Test: strategy with vs without gate, on tune window. Report incremental CAGR, MDD, hit rate of >=5x names, and
  fraction of picks removed. Check financials-sector exclusion (EBITDA meaningless for banks/NBFCs).
- Sensitivity to lag (45/60/90/120d) and thresholds; plateau vs spike.
- Report data coverage: % of symbol-quarters with usable PIT data. Low coverage = biased subset.
Output `reports/4_fundamentals_tester.md`. TUNE WINDOW ONLY.
