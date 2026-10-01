# Common rules for every agent
- Read `config.py` first. Never redefine capital, dates, costs or lags.
- Money in rupees (Rs), formatted Indian-style (Rs 10,00,000). Start capital Rs 10,00,000.
- Tuning/diagnostics use 2010-2018 ONLY. Never load 2019+ data except via `holdout.load_range(..., final_run=True)`,
  and only the orchestrator does that, once.
- Report failures as prominently as successes. No result is "good" unless it beats the random baseline
  AND Nifty TRI on max drawdown, not just on returns.
- Write findings to `reports/<agent>.md`. State: what you ran, exact command, data used, numbers, caveats.
- If data is missing or synthetic, say so at the top of your report. Results on synthetic data prove nothing.
