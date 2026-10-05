# Entry-state validation (tune window only)

Script: `analysis/timing/state_validation.py` (re-runnable; reads `prices_tune.parquet` and `us_prices_tune.parquet` only; no SEALED file is opened). Thresholds in `mblab/timing.py` (`TH`) were declared before this run from common practice and were NOT tuned to these results; this is the only run reported.

## Headline

- **India (Nifty 500 survivors)**: (attractive + confirmation) minus (overextended + breakout), 12m same-date excess mean = -5.6%, negative and its 90% interval excludes zero; median-return difference -5.1%, 10th-percentile difference -2.4%. attractive vs overextended alone: -5.4% (negative and its 90% interval excludes zero). confirmation vs overextended: -6.0% (negative and its 90% interval excludes zero).
- **US (S&P 500 survivors)**: (attractive + confirmation) minus (overextended + breakout), 12m same-date excess mean = +0.1%, not distinguishable from zero (90% interval spans zero); median-return difference +1.4%, 10th-percentile difference +0.5%. attractive vs overextended alone: +1.6% (positive and its 90% interval excludes zero). confirmation vs overextended: -0.7% (not distinguishable from zero (90% interval spans zero)).


## India (Nifty 500 survivors)

325 stocks used (8 excluded for one-day moves beyond -45%/+80%, likely unadjusted splits). 31,299 stock-month observations (106 month-grid dates, 2010-01 to 2018-12); 27,401 have a 12m forward return. State counts: too_early 11,168, setup_forming 7,314, overextended 6,116, attractive_entry 3,029, wait_for_pullback 1,899, confirmation_entry 1,666, unknown 102, breakout_entry 5.


### Forward 6-month return by state

| State | n | dates | mean | median | hit rate (>0) | 10th pct | worst | P(loss>20%) | excess mean vs same-date avg | excess median |
|---|---|---|---|---|---|---|---|---|---|---|
| attractive_entry | 2940 | 100 | +12.1% | +6.8% | 60.9% | -21.6% | -79.9% | 11.5% | +1.3% | -2.2% |
| confirmation_entry | 1618 | 99 | +11.2% | +8.2% | 65.0% | -16.8% | -63.3% | 7.2% | +1.1% | -1.1% |
| breakout_entry | 4 | 3 | -0.2% | -5.5% | 50.0% | -21.7% | -25.5% | 25.0% | -6.4% | -8.0% |
| setup_forming | 6963 | 100 | +12.0% | +5.4% | 58.8% | -23.4% | -85.7% | 13.3% | -0.3% | -4.2% |
| wait_for_pullback | 1839 | 99 | +10.8% | +6.4% | 61.8% | -20.6% | -87.8% | 10.8% | -0.0% | -2.7% |
| overextended | 5969 | 99 | +16.1% | +9.2% | 63.7% | -19.4% | -80.2% | 9.6% | +3.9% | -0.7% |
| too_early | 9917 | 100 | +7.5% | +2.5% | 54.0% | -27.1% | -92.4% | 16.9% | -2.6% | -6.5% |
| ALL (base) | 29349 | 100 | +11.2% | +5.6% | 58.9% | -23.4% | -92.4% | 13.1% | +0.0% | +0.0% |


### Forward 12-month return by state

| State | n | dates | mean | median | hit rate (>0) | 10th pct | worst | P(loss>20%) | excess mean vs same-date avg | excess median |
|---|---|---|---|---|---|---|---|---|---|---|
| attractive_entry | 2726 | 94 | +23.9% | +10.5% | 62.3% | -31.1% | -86.5% | 17.7% | +2.0% | -7.4% |
| confirmation_entry | 1516 | 93 | +21.0% | +12.7% | 66.5% | -23.1% | -90.7% | 12.2% | +1.3% | -3.6% |
| breakout_entry | 4 | 3 | +13.2% | -9.0% | 25.0% | -10.3% | -10.7% | 0.0% | -4.9% | -10.9% |
| setup_forming | 6482 | 94 | +26.6% | +12.4% | 62.6% | -31.2% | -94.0% | 17.7% | -1.1% | -9.8% |
| wait_for_pullback | 1731 | 93 | +19.2% | +10.9% | 61.8% | -29.7% | -90.5% | 16.3% | -1.3% | -7.1% |
| overextended | 5663 | 93 | +31.1% | +16.6% | 67.4% | -26.5% | -91.0% | 13.9% | +7.3% | -1.9% |
| too_early | 9182 | 94 | +26.2% | +10.9% | 60.2% | -33.1% | -94.0% | 20.8% | -4.3% | -14.1% |
| ALL (base) | 27401 | 94 | +26.3% | +12.5% | 62.9% | -30.8% | -94.0% | 17.6% | +0.0% | +0.0% |


### Contrasts, 12-month (date-cluster bootstrap, 1000 draws over month-grid dates, 90% interval)

| Contrast (A minus B) | nA | nB | excess-mean diff [90% CI] | median-return diff [90% CI] | hit-rate diff [90% CI] | 10th-pct diff [90% CI] |
|---|---|---|---|---|---|---|
| attractive_entry vs overextended | 2726 | 5663 | -5.4% [-9.1%, -2.0%] | -6.1% [-9.9%, -2.4%] | -5.1% [-8.5%, -1.7%] | -4.6% [-7.5%, -1.8%] |
| confirmation_entry vs overextended | 1516 | 5663 | -6.0% [-9.3%, -3.2%] | -3.9% [-7.3%, -0.5%] | -0.9% [-4.4%, +2.4%] | +3.4% [-1.5%, +6.5%] |
| attractive_entry vs breakout_entry | 2726 | 4 | +nan% [-5.4%, +19.0%] | +nan% [-27.6%, +23.0%] | +nan% [+11.0%, +63.2%] | +nan% [-23.5%, -18.0%] |
| confirmation_entry vs breakout_entry | 1516 | 4 | +nan% [-6.4%, +18.7%] | +nan% [-24.3%, +24.8%] | +nan% [+14.9%, +66.7%] | +nan% [-17.7%, -9.1%] |
| (attractive + confirmation) vs (overextended + breakout) | 4242 | 5667 | -5.6% [-9.0%, -2.5%] | -5.1% [-8.5%, -1.7%] | -3.6% [-6.5%, -0.6%] | -2.4% [-5.5%, +0.6%] |
| attractive_entry vs ALL stocks in uptrend states (setup..overextended) | 2726 | 15396 | -0.3% [-3.0%, +2.4%] | -3.2% [-6.1%, -0.5%] | -2.4% [-4.9%, +0.4%] | -2.5% [-4.2%, -0.4%] |


### Contrasts, 6-month

| Contrast (A minus B) | nA | nB | excess-mean diff [90% CI] | median-return diff [90% CI] | hit-rate diff [90% CI] | 10th-pct diff [90% CI] |
|---|---|---|---|---|---|---|
| attractive_entry vs overextended | 2940 | 5969 | -2.6% [-4.6%, -0.9%] | -2.4% [-5.4%, -0.1%] | -2.9% [-6.9%, +0.8%] | -2.2% [-4.6%, -0.3%] |
| confirmation_entry vs overextended | 1618 | 5969 | -2.8% [-4.6%, -1.1%] | -1.0% [-3.7%, +1.0%] | +1.3% [-2.5%, +4.8%] | +2.6% [+0.2%, +4.9%] |
| attractive_entry vs breakout_entry | 2940 | 4 | +nan% [+1.0%, +13.9%] | +nan% [-24.4%, +30.0%] | +nan% [-6.9%, +30.3%] | +nan% [-10.8%, +4.7%] |
| confirmation_entry vs breakout_entry | 1618 | 4 | +nan% [+0.3%, +14.0%] | +nan% [-24.6%, +32.1%] | +nan% [-2.5%, +36.2%] | +nan% [-5.1%, +9.9%] |
| (attractive + confirmation) vs (overextended + breakout) | 4558 | 5973 | -2.7% [-4.4%, -1.2%] | -2.0% [-4.5%, +0.2%] | -1.4% [-5.1%, +2.0%] | -0.5% [-2.6%, +1.4%] |
| attractive_entry vs ALL stocks in uptrend states (setup..overextended) | 2940 | 16393 | -0.1% [-1.4%, +1.1%] | -0.5% [-2.5%, +1.2%] | -0.7% [-3.6%, +2.0%] | -0.5% [-2.2%, +0.9%] |


### Is extension informative on its own? 12m forward return by ATR-extension from the 50d MA (stocks above a rising 200d MA with 50d>200d only)

| bucket | n | median | mean | hit rate | 10th pct | excess mean |
|---|---|---|---|---|---|---|
| <-2 | 2712 | +8.0% | +20.6% | 59.8% | -32.5% | -4.5% |
| -2..-1 | 1060 | +8.2% | +18.2% | 59.6% | -31.3% | -6.1% |
| -1..0 | 1228 | +12.5% | +28.2% | 65.2% | -30.8% | +2.8% |
| 0..1 | 1348 | +13.3% | +22.6% | 63.9% | -29.6% | -2.7% |
| 1..2 | 1398 | +11.2% | +25.8% | 62.5% | -30.0% | -0.3% |
| 2..3 | 1432 | +12.2% | +21.7% | 62.6% | -29.0% | -3.5% |
| 3..4 | 1568 | +12.0% | +21.3% | 63.0% | -29.9% | -3.5% |
| >4 | 7375 | +17.0% | +32.3% | 67.4% | -26.7% | +4.0% |


### 12m forward return by distance below the 52-week high (same stocks)

| bucket | n | median | mean | hit rate | 10th pct | excess mean |
|---|---|---|---|---|---|---|
| -30% or worse | 305 | +12.5% | +40.2% | 59.7% | -39.7% | -7.0% |
| -30..-20% | 1489 | +6.1% | +24.8% | 55.7% | -37.9% | -5.7% |
| -20..-10% | 5356 | +10.9% | +25.0% | 61.3% | -31.6% | -2.3% |
| -10..-5% | 4479 | +13.9% | +25.5% | 66.0% | -26.1% | +0.5% |
| within 5% | 6493 | +15.4% | +28.0% | 67.8% | -23.8% | +3.2% |


### Stability: sub-periods and market regime (12m, same-date excess mean)

| slice | attractive | confirmation | breakout (price only) | wait_for_pullback | overextended | too_early |
|---|---|---|---|---|---|---|
| 2010-2013 starts | +4.1% (n=1086; median +6.0%) | +3.9% (n=655; median +10.0%) | n=0 | +1.3% (n=693; median +7.6%) | +7.5% (n=2114; median +11.6%) | -4.2% (n=5536; median +6.6%) |
| 2014-2017 starts | +0.6% (n=1640; median +13.4%) | -0.7% (n=861; median +14.3%) | n=4 | -3.0% (n=1038; median +13.4%) | +7.2% (n=3549; median +20.4%) | -4.5% (n=3646; median +16.4%) |
| regime ON (EW universe > 200d MA) | +1.9% (n=2350; median +7.8%) | +2.1% (n=1365; median +11.2%) | n=4 | -0.7% (n=1579; median +9.8%) | +7.8% (n=5343; median +15.2%) | -7.4% (n=5225; median +2.1%) |
| regime OFF | +2.0% (n=376; median +24.4%) | -5.7% (n=151; median +24.2%) | n=0 | -7.2% (n=152; median +23.7%) | -0.9% (n=320; median +35.8%) | -0.2% (n=3957; median +24.0%) |


## US (S&P 500 survivors)

471 stocks used (1 excluded for one-day moves beyond -45%/+80%, likely unadjusted splits). 48,173 stock-month observations (108 month-grid dates, 2010-01 to 2018-12); 42,525 have a 12m forward return. State counts: overextended 12,766, setup_forming 11,015, too_early 10,293, confirmation_entry 6,492, wait_for_pullback 3,818, attractive_entry 3,670, unknown 95, breakout_entry 24.


### Forward 6-month return by state

| State | n | dates | mean | median | hit rate (>0) | 10th pct | worst | P(loss>20%) | excess mean vs same-date avg | excess median |
|---|---|---|---|---|---|---|---|---|---|---|
| attractive_entry | 3473 | 102 | +9.2% | +8.4% | 68.4% | -14.1% | -65.1% | 5.6% | +0.2% | -1.1% |
| confirmation_entry | 6194 | 102 | +8.4% | +8.2% | 72.7% | -9.8% | -61.3% | 2.9% | -0.3% | -0.7% |
| breakout_entry | 20 | 16 | +12.7% | +9.7% | 85.0% | -1.0% | -1.9% | 0.0% | +2.9% | +2.0% |
| setup_forming | 10306 | 102 | +9.1% | +8.5% | 71.2% | -12.2% | -71.7% | 4.1% | -0.2% | -0.9% |
| wait_for_pullback | 3634 | 102 | +8.1% | +7.4% | 70.2% | -12.2% | -51.2% | 4.5% | -0.2% | -1.5% |
| overextended | 12183 | 102 | +7.8% | +6.9% | 69.5% | -11.4% | -75.5% | 3.8% | -0.4% | -1.4% |
| too_early | 9442 | 102 | +12.7% | +11.6% | 73.3% | -12.2% | -74.2% | 5.2% | +0.9% | -0.3% |
| ALL (base) | 45347 | 102 | +9.3% | +8.4% | 71.1% | -11.8% | -75.5% | 4.2% | +0.0% | +0.0% |


### Forward 12-month return by state

| State | n | dates | mean | median | hit rate (>0) | 10th pct | worst | P(loss>20%) | excess mean vs same-date avg | excess median |
|---|---|---|---|---|---|---|---|---|---|---|
| attractive_entry | 3070 | 96 | +20.9% | +18.1% | 77.8% | -12.4% | -85.5% | 5.9% | +1.0% | -1.8% |
| confirmation_entry | 5877 | 96 | +17.7% | +15.9% | 81.2% | -7.6% | -71.3% | 3.4% | -1.3% | -3.2% |
| breakout_entry | 20 | 16 | +21.4% | +10.1% | 85.0% | -3.0% | -7.3% | 0.0% | +2.7% | -0.1% |
| setup_forming | 9680 | 96 | +19.7% | +17.3% | 78.6% | -11.0% | -74.4% | 4.8% | -0.2% | -2.1% |
| wait_for_pullback | 3448 | 96 | +18.2% | +15.1% | 78.4% | -9.7% | -56.1% | 3.7% | -0.5% | -3.1% |
| overextended | 11581 | 96 | +18.0% | +15.2% | 78.8% | -9.6% | -76.3% | 4.0% | -0.6% | -3.2% |
| too_early | 8756 | 96 | +23.6% | +20.0% | 77.8% | -13.5% | -89.7% | 6.5% | +1.7% | -1.9% |
| ALL (base) | 42525 | 96 | +19.7% | +16.8% | 78.8% | -10.6% | -89.7% | 4.7% | +0.0% | +0.0% |


### Contrasts, 12-month (date-cluster bootstrap, 1000 draws over month-grid dates, 90% interval)

| Contrast (A minus B) | nA | nB | excess-mean diff [90% CI] | median-return diff [90% CI] | hit-rate diff [90% CI] | 10th-pct diff [90% CI] |
|---|---|---|---|---|---|---|
| attractive_entry vs overextended | 3070 | 11581 | +1.6% [+0.3%, +2.9%] | +2.9% [+0.7%, +4.8%] | -1.0% [-3.9%, +1.6%] | -2.8% [-5.4%, -0.3%] |
| confirmation_entry vs overextended | 5877 | 11581 | -0.7% [-1.8%, +0.5%] | +0.7% [-1.0%, +2.4%] | +2.4% [-0.0%, +4.9%] | +2.0% [+0.3%, +4.0%] |
| attractive_entry vs breakout_entry | 3070 | 20 | -1.7% [-13.6%, +8.2%] | +8.0% [-8.5%, +13.2%] | -7.2% [-19.8%, +4.7%] | -9.4% [-16.3%, -4.6%] |
| confirmation_entry vs breakout_entry | 5877 | 20 | -4.0% [-15.7%, +6.2%] | +5.8% [-10.5%, +10.9%] | -3.8% [-16.5%, +8.2%] | -4.6% [-10.9%, -0.2%] |
| (attractive + confirmation) vs (overextended + breakout) | 8947 | 11601 | +0.1% [-0.9%, +1.0%] | +1.4% [-0.4%, +3.0%] | +1.2% [-1.2%, +3.6%] | +0.5% [-1.4%, +2.4%] |
| attractive_entry vs ALL stocks in uptrend states (setup..overextended) | 3070 | 30606 | +1.6% [+0.5%, +2.7%] | +2.1% [+0.6%, +3.6%] | -1.4% [-3.5%, +0.5%] | -2.8% [-4.9%, -1.0%] |


### Contrasts, 6-month

| Contrast (A minus B) | nA | nB | excess-mean diff [90% CI] | median-return diff [90% CI] | hit-rate diff [90% CI] | 10th-pct diff [90% CI] |
|---|---|---|---|---|---|---|
| attractive_entry vs overextended | 3473 | 12183 | +0.7% [-0.2%, +1.5%] | +1.5% [+0.3%, +2.9%] | -1.2% [-4.0%, +1.5%] | -2.7% [-4.5%, -1.1%] |
| confirmation_entry vs overextended | 6194 | 12183 | +0.1% [-0.6%, +0.8%] | +1.3% [+0.2%, +2.4%] | +3.1% [+0.5%, +5.8%] | +1.6% [+0.3%, +2.9%] |
| attractive_entry vs breakout_entry | 3473 | 20 | -2.7% [-8.7%, +2.8%] | -1.3% [-9.0%, +6.6%] | -16.6% [-29.2%, -2.4%] | -13.1% [-17.3%, -10.7%] |
| confirmation_entry vs breakout_entry | 6194 | 20 | -3.3% [-9.1%, +2.3%] | -1.5% [-9.1%, +6.1%] | -12.3% [-25.1%, +1.7%] | -8.8% [-12.3%, -7.1%] |
| (attractive + confirmation) vs (overextended + breakout) | 9667 | 12203 | +0.3% [-0.3%, +0.9%] | +1.3% [+0.3%, +2.4%] | +1.5% [-0.9%, +3.9%] | +0.1% [-1.2%, +1.4%] |
| attractive_entry vs ALL stocks in uptrend states (setup..overextended) | 3473 | 32337 | +0.6% [-0.1%, +1.2%] | +0.7% [-0.3%, +1.9%] | -2.4% [-4.5%, -0.4%] | -2.7% [-4.2%, -1.4%] |


### Is extension informative on its own? 12m forward return by ATR-extension from the 50d MA (stocks above a rising 200d MA with 50d>200d only)

| bucket | n | median | mean | hit rate | 10th pct | excess mean |
|---|---|---|---|---|---|---|
| <-2 | 4993 | +17.7% | +19.8% | 80.1% | -9.8% | -0.1% |
| -2..-1 | 1848 | +18.0% | +19.8% | 79.9% | -10.5% | +0.5% |
| -1..0 | 2030 | +16.4% | +19.0% | 78.7% | -10.0% | +0.3% |
| 0..1 | 2335 | +16.4% | +18.4% | 79.7% | -9.9% | -0.3% |
| 1..2 | 2658 | +16.8% | +19.4% | 79.2% | -9.2% | +0.7% |
| 2..3 | 2830 | +16.7% | +18.9% | 78.7% | -9.7% | +0.2% |
| 3..4 | 2772 | +14.3% | +17.3% | 77.8% | -10.6% | -0.8% |
| >4 | 14207 | +15.5% | +18.3% | 78.7% | -9.8% | -0.0% |


### 12m forward return by distance below the 52-week high (same stocks)

| bucket | n | median | mean | hit rate | 10th pct | excess mean |
|---|---|---|---|---|---|---|
| -30% or worse | 103 | +21.3% | +35.1% | 79.6% | -13.6% | +13.5% |
| -30..-20% | 782 | +18.1% | +26.2% | 73.3% | -17.0% | +6.6% |
| -20..-10% | 4970 | +19.0% | +21.5% | 76.9% | -13.9% | +1.4% |
| -10..-5% | 8321 | +17.0% | +19.2% | 79.4% | -10.3% | +0.2% |
| within 5% | 19500 | +15.2% | +17.4% | 79.6% | -8.4% | -0.8% |


### Stability: sub-periods and market regime (12m, same-date excess mean)

| slice | attractive | confirmation | breakout (price only) | wait_for_pullback | overextended | too_early |
|---|---|---|---|---|---|---|
| 2010-2013 starts | +0.8% (n=1647; median +21.0%) | -1.8% (n=2667; median +19.3%) | n=7 | -0.5% (n=1805; median +18.0%) | -0.1% (n=5884; median +18.3%) | +1.4% (n=4099; median +22.9%) |
| 2014-2017 starts | +1.2% (n=1423; median +15.0%) | -0.9% (n=3210; median +13.0%) | n=13 | -0.6% (n=1643; median +11.9%) | -1.1% (n=5697; median +12.4%) | +2.0% (n=4657; median +18.0%) |
| regime ON (EW universe > 200d MA) | +1.1% (n=2756; median +17.5%) | -1.0% (n=5554; median +15.7%) | n=20 | -0.4% (n=3319; median +14.9%) | -0.5% (n=11410; median +15.2%) | +1.9% (n=6212; median +18.3%) |
| regime OFF | -0.0% (n=314; median +21.5%) | -5.9% (n=323; median +18.1%) | n=0 | -5.1% (n=129; median +17.0%) | -5.9% (n=171; median +15.4%) | +1.3% (n=2544; median +23.8%) |


## Caveats that bind every number above

- **Survivor bias.** The universes are today's Nifty 500 / S&P 500 members; stocks that fell out or were delisted are absent, and members that joined because they rose are present. Every forward return is flattered, and the flattery is probably larger for stocks that were 'down and recovering' (attractive_entry, setup_forming) than for steady uptrenders, so the contrast is biased toward pullback states. Read the DIFFERENCES between states, not the levels, and treat even those as upper bounds.
- **Close-only data.** No volume and no High/Low exist in the tune files. ATR is the mean absolute close-to-close change (a lower bound on true range, so extension in ATR units is slightly overstated). Volume confirmation of breakouts is NOT testable here: `breakout_entry` below is a price-only breakout (prior 60-day closing high exceeded within 5 days, from a base no wider than 25%). The production rule withholds the state if volume is present and below 1.5x average; that filter is unvalidated.
- **Overlap and dependence.** One observation per stock per month; 12m windows overlap heavily and stocks move together within a month, so effective independent samples are far fewer than n. Intervals come from a bootstrap over month-grid dates (which respects cross-sectional dependence but not serial overlap), so they are still too narrow.
- **Same-date excess** subtracts the average return of all sampled stocks on that date, removing the market and the bull/bear cycle, but not size/sector/momentum effects. The lab's own finding (reports/ENGINE_FINDINGS.md) is that the 12-1 momentum rank is the only validated selector in India; states near highs overlap with momentum, so a good result for near-high states may be momentum, not timing.
- **Regime.** The regime used here is an equal-weight universe index above its 200d MA (a proxy), not the Nifty 500 / S&P 500 filter the product will pass in. States are computed with regime_on=True so each state describes the stock's own chart; the regime split is in the stability table.
- **Unadjusted-split artefacts** may remain below the -45%/+80% one-day filter. Data is Yahoo; no corporate-action audit.
- **Small windows.** Two markets, ten years, one market cycle each (2009-2018 was a long bull market with a 2011 / 2015-16 / 2018 setbacks). A state that looks good here has not been tested in a prolonged bear market.
- Not tested at all: the zones themselves (whether price returning to the 'ideal zone' beats waiting), the thesis_deteriorating state (needs fundamentals), and the regime downgrade.


## What this does and does not justify

Entry states are descriptive labels of where price sits in its trend. They are shown beside, never instead of, the research gates (level >= 4, adversarial review, fresh evidence). Whatever the tables show, they are not evidence that a labelled state will make money out of sample; the sealed windows are untouched and must stay that way until the states are frozen.
