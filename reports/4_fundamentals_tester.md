# Agent 4 - Fundamentals gate tester

## VERDICT: UNTESTABLE ON REAL DATA
No point-in-time (PIT) fundamentals covering 2010-2018 exist in the repo or are reachable from this sandbox.
**No with-vs-without-gate backtest was run. No incremental CAGR / MDD / >=5x hit-rate / %-picks-removed numbers exist.**
Nothing was backfilled from today's numbers (that would be look-ahead). Everything below on the gate code is
mechanics tested on SYNTHETIC toy data; it says nothing about Indian markets.

## What was checked (2026-10-01, tune-window rules; sealed files and post-2018 data not read)
`data/pit/` is empty. Only prices/benchmark exist in `data/raw/`.

| Source | Reachable? | Fundamentals history | Usable for 2010-18 PIT? |
|---|---|---|---|
| yfinance (financials / quarterly_financials / cashflow / get_income_stmt) | yes | 10 named large caps: annual 4-5 FYs (earliest FY-end Mar-2022 or Mar-2023), quarterly 5-6 qtrs (from Mar/Jun-2025). Random 40 of Nifty-500: 39 returned data, earliest FY-end 2021-2025, **0 of 40 reach 2018 or earlier**. Banks (HDFCBANK, BAJFINANCE) have no EBITDA row. No filing dates. | NO (0% coverage of 2010-18) |
| screener.in (public HTML, UA header) | 200 | Annual columns from ~Mar-2015/16 only (as of today), ~12 quarters, TODAY'S restated numbers, no filing dates, login wall for export | NO: not PIT, starts after most of the window, ToS/scraping risk |
| stockanalysis.com | 200 | FY2022-2026 only | NO |
| BSE site front pages / bhavcopy dir | 200 | pages only; `api.bseindia.com` results/announcement APIs -> 403 | NO (blocked) |
| nseindia.com | 403 (api path returned 200 shell, no data) | - | NO (blocked) |
| web.archive.org | availability API 200; snapshot content 403; CDX timeout | would have been the only genuinely PIT route (2016+ snapshots) | NO (content blocked) |
| macrotrends, sec.gov, valueresearchonline | 403 | - | blocked |
| trendlyne, moneycontrol | 301 redirect / no usable payload | - | not obtainable |
| eodhd (401, key needed), alphavantage (key needed, ~5y, US-centric), financialmodelingprep (301) | paid/keyed | - | not tested, no key |
| Yahoo query1 chart API directly | 429 (rate limit; yfinance wrapper works) | - | - |

Conclusion: best free coverage is ~4-5 years ending 2026 => zero overlap with 2010-2018. Even screener-style 10Y data is
restated (not "originally reported") and has no filing dates. Coverage of symbol-quarters in the tune window: **0%**.

## Deliverables
1. `analysis/fundamentals/pit_gate.py` - `pit_eligibility(fund, rebalance_dates, symbols, sectors, params)` returns a long
   (rebalance_date, symbol, eligible, reason, diagnostics) table; `eligibility_matrix()` gives dates x symbols booleans to AND
   with the backtest candidate mask; `coverage()` / `symbol_quarter_coverage()` report coverage; CLI `python
   analysis/fundamentals/pit_gate.py` prints UNTESTABLE (exit 2) if `data/pit/fundamentals.parquet` is absent.
   - Usable date = `filed_date`, else `period_end + QUARTERLY_LAG_DAYS (60)` / `ANNUAL_LAG_DAYS (90)`; inclusive `<= rebalance date`.
   - Originally reported value: earliest-filed version per period; later restatements discarded (value and availability).
   - Gate (defaults, all parameters in `GateParams`, to be swept for plateau-vs-spike once data exists):
     TTM EBITDA margin > year-ago TTM margin; TTM revenue growth >= 10%; TTM EBITDA growth >= 10%; EBITDA > 0 both years;
     OCF/EBITDA >= 0.5 (quarterly OCF if supplied for all 4 qtrs, else latest filed FY); optional FCF>0 if `capex` given.
     Needs 8 contiguous quarters (falls back to 2 consecutive FYs). Missing/stale/gapped data => ineligible (fail closed).
   - Financials excluded by sector keyword (financ/bank/nbfc/insur/housing finance/asset management/broking); unknown sector
     policy 'allow' or 'exclude'. Refuses rebalance dates after TUNE_END unless `allow_post_tune=True`.
   - Thresholds (10%, 0.5, 200d staleness) are my placeholders, NOT tuned on anything.
2. `tests/test_pit_gate.py` - 32 tests pass (whole `tests/` dir: `python -m pytest tests -q`, 32 passed). Cover: future quarter filed
   after date leaves verdict AND diagnostics unchanged (lags 45/60/90/120); same row filed on the date flips it (inclusive
   boundary); lag boundary exact at period_end+lag for 45/60/90/120; annual lag; filed_date overrides lag unless `force_lag`;
   restatement ignored; truncation invariance (output on full table == output on table pre-filtered to rows known by d, 6 random
   symbols x 13 dates); 25-draw fuzz of future values; margin/growth/OCF/missing-OCF/gap/stale/negative-EBITDA failures;
   financials exclusion; post-tune refusal; corrupt dates rejected. Mutation check: a 1-day lookahead injected into the filter
   made 5 tests fail.
3. Data requirements (below).

## Data the user must supply -> `data/pit/fundamentals.parquet`
Long table, one row per symbol x reported period (include delisted names, and merge renamed symbols to the price-file symbol):

| column | required | notes |
|---|---|---|
| symbol | yes | same key as `prices_tune.parquet` columns |
| period_type | recommended | 'Q' single-quarter or 'A' full year (default 'Q'); Q4 must be derived (FY minus 9M) |
| period_end | yes | quarter/FY end date |
| filed_date | strongly | date results were filed with BSE/NSE (exchange timestamp). If absent the lag from config.py is used |
| revenue | yes | total operating revenue as ORIGINALLY reported |
| ebitda | yes | = operating profit before D&A (PBIDT) as originally reported; state standalone vs consolidated and keep it consistent |
| ocf | yes | cash from operations; Indian companies report it only half-yearly/annually, so supply 'A' rows (or H1/H2 split into Q rows) |
| capex | optional | for the FCF-sign test |
| sector | recommended | NSE industry, to exclude financials |

Hard requirements: originally reported (not restated) values, ideally keep every filing version with its own filed_date;
>= 2009 onward (gate needs 8 quarters before the first 2010 rebalance); PIT-universe coverage including later-delisted names
(otherwise the same survivorship bias as prices). Plausible sources: Capitaline / Prowess (CMIE) / Ace Equity / Bloomberg
exports, or exchange XBRL result filings (BSE/NSE) parsed with their filing timestamps. Free scrapes of today's pages are NOT PIT.

## Once data arrives (not done)
Run the gate over month-end rebalances in 2010-2018, AND the matrix with backtest candidate masks (do not edit `backtest.py`
in place; wrap), report coverage first, flag any run with < ~70% evaluable symbol-dates as a biased subset, then report
CAGR/MDD/>=5x hit rate/% picks removed with vs without gate, lag 45/60/90/120, and a threshold grid, against the random baseline and
Nifty TRI. Also note the price universe is survivorship-biased (272 names live on 2010-01-04), so any result is an upper bound.
