# Protocol

## Question
Can a trend + quality framework find future multi-baggers in Nifty 500 (incl. delisted) without large losses?

## Phases
0. Data: supply PIT constituents, delisted prices, PIT fundamentals (see data/README.md). Run `pytest`.
1. Tune (2010-2018 only): agents 1-5 run in parallel; outputs in reports/.
2. Freeze: orchestrator writes `reports/FROZEN_RULES.md` (exact rules + params + commit hash). No changes after this.
3. Test (2019-2026, once): single run via `holdout.load_range(..., final_run=True)`. Results in results/test/.
4. Synthesis: `reports/FINAL.md` = final rule set, honest worst case (Rs), what is unproven.

## Pass criteria (all on test set; see config.CRITERIA)
- CAGR > Nifty 50 TRI and > median of 1000 random-pick runs
- Max drawdown shallower than Nifty 50 TRI and than random median
- Survives 2x cost stress

## Honesty rules
- Failures reported as prominently as successes; negative result is a valid outcome.
- Any deviation from this protocol is logged in reports/DEVIATIONS.md.
- If test set was peeked at, the lock file is removed only with a DEVIATIONS entry and results are labelled contaminated.
