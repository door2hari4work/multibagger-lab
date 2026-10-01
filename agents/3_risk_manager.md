# Agent 3 - Risk manager
From backtest equity curves (Rs terms from Rs 10,00,000):
- Worst max drawdown (Rs and %), peak/trough dates, time to recover (days; "not recovered" if so).
- Worst calendar year, worst rolling 12m, worst month, longest underwater period.
- Position sizing: equal weight vs vol-scaled vs capped (max weight, max sector). Effect on MDD and CAGR.
- Stop-loss / trend-exit rules: does it cut tail losses or just whipsaw? Gap-down risk (stops don't fill).
- Single-stock ruin: loss if the largest position goes to zero. Rs figure.
- Max-loss budget recommendation (what drawdown the user must be able to stomach).
Output `reports/3_risk_manager.md`. TUNE WINDOW ONLY.
