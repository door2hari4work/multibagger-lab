# Portfolio import and intelligence (mblab/portfolio.py)

Purpose: tell the owner how a candidate fits THEIR portfolio (overlap, hidden concentration, missing exposure) without ever storing holdings in git.

## Privacy rules (hard)
- Real holdings, snapshots and analytics live only under `private/` (gitignored). `portfolio.write_private()` refuses any other path.
- Importer reports (`ImportResult.report()`) contain column mappings and counts, never holding names or amounts.
- Tests and fixtures are synthetic. `tests/test_portfolio.py` asserts `private/` is git-ignored and nothing under it is tracked.
- `analyze_portfolio()` output contains holding names: keep it under `private/`. Feed only the numbers you need into theses (`PortfolioFit` carries a summary, not holdings).

## Two ways in
1. **IndMoney (read-only)**: the connected IndMoney tools. Only read tools are used (`networth_snapshot`, `networth_holdings`, `get_family_asset_holdings`, `get_mf_funds_details`, `get_us_stocks_details`). No order, SIP or trade tool is ever called.
   Save the raw responses to `private/raw/indmoney_raw.json` (+ fund details in `private/raw/mf_details_raw.json`, referenced by `fund_details_file`), then run
   `python -m mblab.portfolio build-snapshot` -> `private/portfolio_snapshot.json` and `private/portfolio_analytics.json`. It prints only aggregate counts.
   Optional `private/overrides.json` = `{"sector": {name: sector}, "market": {name: "US"}, "market_cap": {name: "large"}}` for rows the source cannot classify (e.g. ESOP/RSU lines, which come as an issuer slug with no ticker).
2. **CSV / Excel upload (Finboom or any broker export)**: `load_holdings_csv(path)`, `load_holdings_excel(path)`, `load_holdings(path)`. Excel needs `openpyxl` (not in requirements.txt yet).

## IndMoney response formats (structure only)
All tools return `{"result": "<JSON string>"}`; the normaliser accepts that or the parsed dict.
- `networth_snapshot`: `total_networth`, `investments[]` (per asset type: invested_value, current_value), `assets[]` (asset-class split), `market_cap[]` (DIRECT stocks only), `sector[]` (always empty: no sector analytics), `liabilities`.
- `networth_holdings(asset_type)`: `holdings[]` rows `{investment_code, investment (name), asset_type, assetclass_l2, invested_amount, market_value (INR), total_units, unit_price, ...}` plus `asset_summary`. US_STOCK rows add `invested_value_usd`, `current_value_usd` and a `market_cap` string; `unit_price` is INR per unit (implied USD/INR = market_value / current_value_usd). `investment_code` is the scheme id for MFs and the ticker for US stocks. IND_STOCK also returns derivative/position blocks (ignored by analytics); the account used for development had no Indian direct stocks, so that row shape is assumed identical to the others.
- `get_family_asset_holdings(asset)`: per member `holdings[]` with `name` (slug), `current_value`, `quantity`, `unit_price`. Used for ESOP/RSU (no ticker, INR only). Other asset types (`gold`, `fd`, `bond`, `epf`, `ppf`, ...) go in `raw["family_holdings"]`.
- `get_mf_funds_details(fund_ids, includes=[asset_allocation, sector_allocation, holdings])`: `data[].data` with `fund_detail` (name, category, benchmark_name), `asset_allocation[]` (Equity vs Debt & Cash, with a market-cap split of the equity part), `sector_allocation[]` (percentages OF THE EQUITY PART; sector names are Morningstar style: Tech, Health, Industrial...), `holdings.holdings[].holds[]` (`name`, `perc` as a string, `sector`).
  Important: `holds` lists about 20 arbitrary holdings, NOT the top 20 and not the full list, even where `holdings_count` suggests otherwise (sampled coverage observed: ~8% to ~44% of a fund). No tickers, names only.
- `get_us_stocks_details(symbols)`: `entity_basic.sector`, `entity_basic.market_cap` ("Mega Cap"), USD price. Used for sector / cap of direct US stocks.

## Look-through quality (what is achievable)
Per fund, `FundProfile.quality`:
- `full`: holdings fully disclosed (e.g. a fund-of-funds over two ETFs).
- `partial` (typical for equity funds via IndMoney): sector split, market-cap split, equity/debt split are COMPLETE; stock-level holdings are a sample. Stock-level and theme exposure through funds is therefore reported as `lower_bound_pct` (direct + disclosed) and `estimated_pct` (the disclosed sample extrapolated over the fund's equity part). Neither is exact; the estimate is only as good as the sample is representative.
- `category`: no breakdown available (file imports, funds without details): declared category-level assumptions in `CATEGORY_RULES` (market-cap mix, country, asset class; sector "Unclassified"). Never presented as measured.
- `none`: unrecognised fund, treated as unclassified.
Fund country comes from benchmark/name (US index vs Indian index) or, for other funds, an estimate from the disclosed sample. Index funds with no stock detail cannot reveal individual constituents; a candidate that is a large index constituent can therefore be under-reported as "not owned via funds".
Portfolio-level quality is reported in `look_through_quality` (label, % of portfolio by quality, assumption notes).

## Analytics (`analyze_portfolio`, all % of total portfolio value in INR)
Exposure by sector, industry (direct holdings only), theme, country, currency (held vs economic), market cap, asset class, direct vs via-funds; concentration (top 1/3/5/10, HHI and effective N of positions and of equity sectors, top underlying stocks as a lower bound); duplicate companies across holdings; fund pairs tracking the same benchmark or sharing disclosed names; plain-language warnings such as "Effective exposure to X is N times your direct holdings".

## Theme map
`THEME_RULES` in portfolio.py: a holding gets a theme if its base ticker is listed or a keyword appears as a whole word in its name/industry. Themes: ai, semiconductors, data_centre_power, defence_aerospace, cloud_software, it_services, internet_platforms, ev_clean_energy, infrastructure, precious_metals. `CATEGORY_THEMES` adds a floor for sector funds (e.g. an infrastructure fund is counted as infrastructure). The map is deliberately coarse (for example "power" matches utilities and power equipment alike; large platforms appear in both ai and internet_platforms). Edit it as the lab learns; tests pin the behaviour.

## Fit scoring
`fit_score(candidate, analytics) -> schema.PortfolioFit`. Candidate: `{ticker, sector, themes, market, market_cap_bucket, name?}`.
Score 0..1 (about 0.5 neutral): weighted blend of theme novelty vs crowding (0.35), sector (0.25), same-company overlap incl. via funds (0.15), market/country (0.10) and market-cap (0.15). Absence of an exposure raises the score; exposure above ~20% (theme) or ~30% (sector) lowers it. `suggested_max_weight_pct` = a size cap by market-cap bucket (large 8, mid 5, small 3, micro 1) scaled by fit and limited by headroom under a 50% theme ceiling. These constants are declared defaults, not validated. The summary always states that concentration can be appropriate and diversification is not automatically better. No portfolio -> `score=None` and the summary says so.

## Limitations
- Fund look-through is sampled (see above); sector-level truth, stock-level estimates.
- Theme tags are keyword heuristics. ESOP/RSU lines have no ticker; market is inferred from the issuer name unless overridden.
- Direct holdings of unlisted/PMS/AIF, insurance, real estate, EPF/PPF/NPS appear only as totals when the source gives no rows.
- Currency exposure assumes country = currency (US -> USD, India -> INR).
- Excel reading needs `openpyxl`; Finboom's real format is unknown, so unmapped columns are reported and can be forced with `mapping={field: header}`.
