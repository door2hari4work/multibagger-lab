
## 2026-10-02: post-test data-integrity checks (sealed files read directly, rules unchanged)
After the one-shot frozen test, found the Nifty BeES benchmark has an unadjusted split on 2019-12-19 (-89.9% day) and 9 stocks have
>45% single-day moves in 2019+. Read sealed files directly (bypassing holdout.py, which is already locked) for two diagnostics only:
(a) corrected BeES benchmark, (b) strategy re-run without the flagged names (analysis/improve/test_sensitivity.py). The official frozen result
is unchanged; no rule or parameter was altered after seeing test results. Treat the test set as used.
