# Small and micro caps: where multi-baggers live (tune window 2010-2018 only; today's members = survivor-biased, worst for micro caps)

## Forensic (analysis/forensic/lift.py; starts 2010-2015, forward 3y/5y outcomes)
| Segment | Stocks | 3x in 3y (base) | Top-decile momentum: 3x rate / lift | Big loss (-30% in 3y) base / top-decile | 10th-percentile 3y return (base) |
|---|---|---|---|---|---|
| India mid (150) | 95 | 16.5% | 29.8% / 1.81x | 12.1% / 4.1% | -36% |
| India small (250) | 133 | 23.2% | 31.4% / 1.35x | 14.1% / 14.2% | -42% |
| India micro (250) | 116 | 26.8% | 29.7% / 1.11x | 15.1% / 14.1% | -45% |
| US small (S&P 600) | 439 | 5.7% | 9.8% / 1.71x | 7.4% / 13.6% | -20% |
- Multi-baggers are more frequent as size falls (and survivor bias inflates the small/micro base rates most), but the momentum SELECTION edge falls toward zero in micro caps,
  and big-loss risk rises. Trend filters alone have no multi-bagger lift in any segment (0.78-0.96x).
- US small caps: momentum picks both more winners and 1.8x more big losers.

## Strategy on each segment (declared costs: India small 40 bps, micro 75 bps, US small 15 bps; 15-seed random baselines; results/tune/small_caps.csv)
| Segment | Rebalanced (N=25): CAGR / MaxDD / trades >=3x / >=5x | Hold winners (N=40): CAGR / MaxDD / >=3x / >=5x | Random same filters (median) | Survivor EW hold |
|---|---|---|---|---|
| India mid | 23.0% / -19.5% / 6 / 1 | 19.3% / -21.1% / 9 / 2 | 15.6% / -20.6% | 18.7% / -31.7% |
| India small | 22.1% / -28.6% / 9 / 3 | 22.3% / -29.4% / 19 / 8 | 13.4% / -31.6% | 21.2% / -39.8% |
| India micro | 23.7% / -35.9% / 11 / 3 | 28.3% / -33.7% / 17 / 7 | 14.7% / -36.7% | 20.5% / -44.2% |
| US small | 14.1% / -21.5% / 0 / 0 | 13.7% / -20.2% / 2 / 1 | 10.9% / -23.1% | 18.6% / -25.8% |
Benchmarks: Nifty TRI proxy 9.0% / -27.3%; SPY 11.4% / -19.3%.
- India small/micro with hold-winners is the only configuration that produced a meaningful number of multi-bagger trades (7-8 trades of 5x+ in nine years, versus 1-3 when rebalancing).
- Cost: drawdowns of -29% to -34% do not beat the Nifty (-27.3%) and sit near the -35% hard stop; returns assume 40-75 bps costs and Rs 25,000-position fills in names that may not trade that freely.
- US small caps: no multi-bagger capture, barely beats SPY. Not worth a book.
- Biases: survivorship is severe (96 of 250 micro caps and 113 of 249 small caps existed in 2010; delisted/wiped-out micro caps are absent), so the real multi-bagger rate is much lower than shown. Not validated.

## Decision
Added INS_hold and INM_hold as pre-declared forward paper books (paper/BOOKS.md) before the 2026-10-30 start. They test whether the multi-bagger capture survives without survivorship bias.
