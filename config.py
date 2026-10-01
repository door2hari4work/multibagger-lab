"""Single source of truth for the experiment protocol. Do not override in other files."""
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent

# Capital (all money in rupees)
START_CAPITAL_INR = 10_00_000

# Hard split: tune on TUNE only; TEST is touched once (see holdout.py)
TUNE_START, TUNE_END = date(2010, 1, 1), date(2018, 12, 31)
TEST_START, TEST_END = date(2019, 1, 1), date(2026, 9, 30)

# Universe: Nifty 500 *point-in-time* membership, including names later delisted
UNIVERSE = "NIFTY500_PIT"
BENCHMARK = "NIFTY50_TRI"          # use total-return index, not price index

# Baselines every rule set must beat (returns AND max drawdown)
RANDOM_BASELINE_RUNS = 1000        # same N positions, same rebalance dates, same costs
RANDOM_SEED = 42

# Costs (round trip, per side in bps) -- stress = multiples of base
BASE_COST_BPS = 25                 # brokerage + STT + stamp + impact, per side (placeholder: confirm)
COST_STRESS_MULTIPLES = [1, 2, 3]
SLIPPAGE_BPS_ILLIQUID = 50         # for names below the liquidity floor
MIN_ADV_INR = 1_00_00_000          # min 20d avg daily traded value to hold a name

# Fundamentals: point-in-time reporting lag (days after period end before data is usable)
QUARTERLY_LAG_DAYS = 60            # SEBI allows 45d; add buffer
ANNUAL_LAG_DAYS = 90               # 60d filing deadline + buffer

# Success criteria (must ALL hold on TEST)
CRITERIA = {
    "beats_nifty_cagr": True,
    "beats_random_median_cagr": True,
    "max_drawdown_better_than_nifty": True,
    "max_drawdown_better_than_random_median": True,
}
# A "multi-bagger" = >= 5x (5.0) from entry within holding window
MULTIBAGGER_X = 5.0
