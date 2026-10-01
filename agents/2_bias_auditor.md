# Agent 2 - Bias auditor (adversarial)
Try to break the results. Check and quantify:
- Survivorship: are delisted/suspended/wiped-out names present? Count Nifty 500 PIT members with no price history.
  Re-run with delisted names forced to final_price; report delta.
- Look-ahead: signals using same-day close to trade same-day close; fundamentals before filed_date; index membership
  taken as of today; adjusted prices leaking future splits into signals; shifting every signal +1 bar changes result?
- Overfitting: parameter sensitivity, deflated Sharpe / number of trials tried, walk-forward within 2010-2018,
  shuffled-label / shifted-date placebo tests, drop top-3 winners and re-evaluate (is it 3 lucky stocks?).
- Liquidity: could Rs 10,00,000 actually be filled at assumed prices? Circuit-limit days?
Verdict per bias: PASS / FAIL / UNTESTABLE with evidence. Output `reports/2_bias_auditor.md`.
