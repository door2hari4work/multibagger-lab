# FROZEN RULES (frozen before the 2019-2026 test; no changes after this commit)

Engine: backtest.py as committed with this file. Candidate config (analysis/improve/stress.py `CAND`):
- Universe: today's Nifty 500 (data/raw/nifty500_current.csv), Yahoo adjusted closes. SURVIVOR-BIASED (also in the test period).
- Rebalance: month-end close; trades execute at NEXT close. Start from cash on 2019-01-01 with Rs 10,00,000.
- Eligibility: price > 200d MA, 12-1 month momentum > 0, price >= 75% of 52-week high.
- Ranking: momentum / annualised 252d daily volatility (S_mom_vol); hold top 25, equal weight; unfilled slots stay cash.
- Regime: invest only if Nifty 500 index (^CRSLDX) > its 200d MA at month-end, else all cash.
- Exit: 30% trailing stop from peak, executed next close. No portfolio drawdown breaker (dd_breaker=None).
- Costs: 25 bps per side. Idle cash earns 6% a year (assumption). Taxes not in the base curve (reported separately).
- Benchmarks: Nifty BeES dividend-adjusted (Nifty 50 TRI proxy); random picks (150 seeds each: same filters; no filters).
Selection history: 72 cells tried on 2010-2018 (regime x score x breaker x N) after an earlier 144-cell grid; chosen as the simplest
config inside the best-drawdown band, not the single best cell. The 2018 drawdown was known when the design was made (partly in-sample).
Pass criteria on the test (all four): CAGR > BeES and > random medians; MaxDD shallower than BeES and than random medians; survive 2x cost.

Freeze commit: 6bc9ac667c53 (parent of the commit adding this line)
