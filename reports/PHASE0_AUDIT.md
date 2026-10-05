# Phase 0 audit: multibagger-lab (as of 2026-10-05)

## What this repository actually is
A quantitative RESEARCH LAB, not a product. 58 Python files (~3,200 lines), 32 passing tests, 20 commits over 5 days (19 by Claude, 1 upload by the owner).
There is NO frontend, backend/API, database, authentication, deployment config, user accounts, LLM agent runtime, prompts-as-code, or portfolio ingestion.
The "agents/" folder holds markdown briefs used for one-off research subagents, not a runtime. `paper/` is a scheduled forward-test.

## Inventory and verdicts
| Area | What exists | Verdict |
|---|---|---|
| Backtest engine (`backtest.py`) | Daily engine: monthly rebalance, next-close execution, stops, regime series, custom score, gate hook, hold-winners, cash yield, state export. Defaults regression-checked | WORKS, reusable for the timing/validation layer. Not a thesis engine |
| Data (`fetch_*.py`) | Yahoo adjusted prices: Nifty 500, Microcap 250, S&P 500, S&P 600 (CURRENT members); SEC XBRL annual fundamentals with filing dates (US) | PARTIAL. Survivor-biased, no delisted names, no India fundamentals, no intraday, no corporate-action table |
| Point-in-time gate (`analysis/fundamentals/pit_gate.py`) | Leak-tested EBITDA/growth/cash gate, 32 tests | WORKS, but only validated on US annual data; hurt returns there |
| Validation protocol (`holdout.py`, `config.py`, PROTOCOL.md) | Tune/test split with one-shot lock; used once | WORKS; reusable as the anti-self-deception layer |
| Reports (`reports/`) | Audits, forensic lift, decomposition, small-cap study, final synthesis | Valuable knowledge; honest negative results |
| Paper trading (`paper/`) | 6 frozen books, weekly routine, kill-switches, membership snapshots | WORKS locally; routine unverified until first Friday run |
| Portfolio awareness | None (IndMoney and Zerodha connectors exist in this environment but are unused) | MISSING |
| Thesis/research/catalyst/news/filings layers | None | MISSING |
| UI / alerts / monitoring | STATUS.md only | MISSING |

## What the existing methodology says (from our evidence)
- Price-based rule (trend filters + regime + momentum rank) has real but modest selection edge: strong in India large/mid, weak in the US, fading to ~zero in micro caps.
- The 'quality' gate did not help in the one market we could test.
- 5x trades are rare (0-1 per 9 years in large/mid; 7-8 in India small/micro with higher drawdowns and the worst survivor bias).
- The test-period result (34% CAGR) is survivor-inflated; honest expectation is roughly index-like to mid-teens with large drawdowns.

## Dangerous or misleading things in the current state
1. Backtest CAGRs are inflated by survivorship (survivor hold 20-27% vs index 9-12%); never show them to a user as expected returns.
2. 'Top picks' in results/live_*.csv are momentum screens, not theses; many are +100-500% in a year (chasing risk).
3. India small/micro results assume 40-75 bps costs and fills in thin names.
4. Yahoo data has unadjusted corporate actions (found in the test period); needs a data-reliability layer before any recommendation.

## Gaps vs the MultibaggerLab vision (ranked)
1. A product shell: app, data store, thesis objects, versioning (none exists).
2. A research engine that reads primary sources (filings, calls) with citations and freshness tracking (none).
3. Inflection/catalyst detection from fundamentals and filings (US possible via SEC; India needs a source).
4. Adversarial review step with power to downgrade (only manual, via subagents).
5. Portfolio look-through (needs holdings + fund constituents).
6. Entry/exit state machine tied to thesis (only price-based stops exist).
7. A historical validation harness for the scoring of theses (the engine validates price rules only).

## Reusable foundation (keep)
backtest engine, holdout protocol, PIT fundamentals gate, SEC fetcher, paper-trading harness, reports, kill-switch rules.

## Proposed roadmap (to be confirmed after your answers)
P1 Product spec + thesis schema (versioned JSON) | P2 Data layer with provider abstraction (prices, SEC, corporate actions, portfolio) | P3 Discovery engine
(universe -> quant screen -> inflection flags -> candidates) | P4 Research agents with citations + adversarial review | P5 Thesis store + entry/exit state machine |
P6 Portfolio look-through | P7 Monitoring + alerts | P8 Minimal decision UI | P9 Validation: false-positive/leakage audit, paper-forward tracking.
Honest limit: P3-P5 can be built and tested now; whether the thesis layer has real predictive value can only be shown by forward tracking, because historical theses cannot be reconstructed point-in-time.
