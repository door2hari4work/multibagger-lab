"""
Price-only backtest of the TIMING + RISK engine (entry filter, ranking, stops, regime filter).
It does NOT test the fundamental (EBITDA/growth) gate - that needs point-in-time fundamentals.

Run:   python backtest.py --universe tickers.txt --bench ^NSEI --start 2010-01-01
       (tickers.txt: one Yahoo ticker per line, e.g. RELIANCE.NS. Include delisted names if you can,
        otherwise results are survivorship-biased and too optimistic.)
Needs: pip install yfinance pandas numpy
"""
import argparse, itertools
import numpy as np
import pandas as pd

def load_prices(tickers, start):
    import yfinance as yf
    df = yf.download(tickers, start=start, auto_adjust=True, progress=False)["Close"]
    return df.dropna(how="all")

def apply_end_policy(px, policy="zero"):
    """Series that END before the sample does (delisted/suspended) must not be ffilled at their last price.
    policy="zero": price collapses to ~0 the day after the last print (worst case; honest default)
    policy="last": old behaviour, dead name keeps last price (flatters results; use only to measure the bias)."""
    px = px.copy()
    if policy == "last":
        return px
    last = px.apply(lambda s: s.last_valid_index())
    for t, d in last.items():
        if d is not None and d < px.index[-1] - pd.Timedelta(days=10):
            nxt = px.index[px.index > d][0]
            px.loc[nxt:, t] = px.at[d, t] * 1e-4
    return px

def backtest(px, bench, top_n=15, stop=0.30, cost_bps=25, regime=True,
             mode="momentum", lookback=252, skip=21, ma=200, seed=0, end_policy="zero", start=None):
    """Monthly rebalance. Signals at close of day t are executed at close of t+1 (no look-ahead).
    Trailing stop breaches seen at close t are also executed at close t+1."""
    rng = np.random.default_rng(seed)
    px = apply_end_policy(px, end_policy).ffill()
    ret = px.pct_change().fillna(0.0)
    ma_ = px.rolling(ma).mean()
    mom = px.shift(skip) / px.shift(lookback) - 1
    hi52 = px.rolling(252).max()
    b_ok = (bench > bench.rolling(ma).mean()).reindex(px.index).ffill().fillna(False)
    dates = px.index
    last_of_month = set(px.groupby([dates.year, dates.month]).tail(1).index)

    w = pd.Series(0.0, index=px.columns)
    peak = pd.Series(np.nan, index=px.columns)
    entry = {}  # ticker -> entry price
    trades = []
    pending_target = None
    pending_exit = set()
    block = set()  # stopped out this month, cannot re-enter until next rebalance
    eq, eq_dates = [1.0], [dates[0]]

    for i in range(1, len(dates)):
        d = dates[i]
        # 1) earn today's return on weights held
        day_ret = float((w * ret.iloc[i]).sum())
        w = w * (1 + ret.iloc[i])
        tot = w.sum()
        nav = eq[-1] * (1 + day_ret)
        # drift weights relative to NAV (cash is the remainder)
        w = w / (1 + day_ret)

        # 2) execute stops flagged yesterday, then rebalance flagged yesterday
        cost = 0.0
        if pending_exit:
            for t in pending_exit:
                if w[t] > 0:
                    cost += w[t] * cost_bps / 1e4
                    trades.append((t, entry.get(t), px[t].iloc[i], "stop"))
                    w[t] = 0.0; peak[t] = np.nan; entry.pop(t, None)
            pending_exit = set()
        if pending_target is not None:
            tw = pending_target; pending_target = None
            cost += (tw - w).abs().sum() * cost_bps / 1e4
            for t in px.columns:
                if w[t] > 0 and tw[t] == 0:
                    trades.append((t, entry.get(t), px[t].iloc[i], "rebal"))
                    entry.pop(t, None); peak[t] = np.nan
                if tw[t] > 0 and w[t] == 0:
                    entry[t] = px[t].iloc[i]; peak[t] = px[t].iloc[i]
            w = tw.copy()
        nav *= (1 - cost)
        eq.append(nav); eq_dates.append(d)

        # 3) update peaks, flag stop breaches for tomorrow
        held = w[w > 0].index
        if len(held):
            peak[held] = np.fmax(peak[held], px.loc[d, held])
            breach = [t for t in held if px.at[d, t] < peak[t] * (1 - stop)]
            if breach:
                pending_exit.update(breach); block.update(breach)

        # 4) month-end: build next target
        if d in last_of_month:
            block = set()
            elig = (px.loc[d] > ma_.loc[d]) & (mom.loc[d] > 0) & (px.loc[d] >= 0.75 * hi52.loc[d])
            elig = elig.fillna(False)
            if mode == "random_all":  # unfiltered random picks among every name with a price today
                elig = px.loc[d].notna() & (mom.loc[d].notna())
            if start is not None and d < pd.Timestamp(start):
                elig = elig & False  # warm-up: no trading before TUNE_START
            cand = list(elig[elig].index)
            if mode == "momentum":
                cand = list(mom.loc[d, cand].sort_values(ascending=False).index)[:top_n]
            else:  # random baseline ("random" = same filters, "random_all" = no filters)
                rng.shuffle(cand); cand = cand[:top_n]
            tw = pd.Series(0.0, index=px.columns)
            if (not regime) or bool(b_ok.loc[d]):
                if cand:
                    tw[cand] = 1.0 / top_n  # unfilled slots stay in cash
            pending_target = tw

    eq = pd.Series(eq, index=eq_dates)
    return eq, trades

def metrics(eq, trades=None):
    r = eq.pct_change().dropna()
    yrs = max((eq.index[-1] - eq.index[0]).days / 365.25, 1e-9)
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    mdd = (eq / eq.cummax() - 1).min()
    sharpe = r.mean() / r.std() * np.sqrt(252) if r.std() > 0 else np.nan
    out = dict(CAGR=cagr, MaxDD=mdd, Sharpe=sharpe)
    if trades:
        rets = np.array([(x / e - 1) for _, e, x, _ in trades if e])
        if len(rets):
            out.update(Trades=len(rets), HitRate=(rets > 0).mean(),
                       Over2x=(rets >= 1).mean(), Over5x=(rets >= 4).mean(), WorstTrade=rets.min(), AvgWin=rets[rets > 0].mean() if (rets > 0).any() else 0,
                       AvgLoss=rets[rets <= 0].mean() if (rets <= 0).any() else 0)
    return out

def buy_hold(px):
    # average only over names that have a price on both days; fillna(0) before the mean would count unlisted names as 0% returns
    r = px.pct_change(fill_method=None).mean(axis=1).fillna(0)
    return (1 + r).cumprod()

def periods(eq, bench, splits):
    rows = []
    for name, (a, b) in splits.items():
        e = eq.loc[a:b]; bb = bench.loc[a:b]
        if len(e) < 60: continue
        e = e / e.iloc[0]; bb = bb / bb.iloc[0]
        m, mb = metrics(e), metrics(bb)
        rows.append(dict(period=name, strat_CAGR=m["CAGR"], strat_MaxDD=m["MaxDD"],
                         bench_CAGR=mb["CAGR"], bench_MaxDD=mb["MaxDD"]))
    return pd.DataFrame(rows)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe"); ap.add_argument("--bench", default="^NSEI")
    ap.add_argument("--start", default="2010-01-01")
    a = ap.parse_args()
    tickers = [t.strip() for t in open(a.universe) if t.strip()]
    px = load_prices(tickers, a.start)
    bench = load_prices([a.bench], a.start).iloc[:, 0]
    report(px, bench)

def report(px, bench):
    pd.set_option("display.float_format", lambda x: f"{x:,.3f}")
    base = dict(top_n=15, stop=0.30, cost_bps=25, regime=True)
    eq, tr = backtest(px, bench, **base)
    print("\n=== BASE CASE ==="); print(pd.Series(metrics(eq, tr)))
    print("\n=== BASELINES ===")
    print("Equal-weight buy&hold of universe:", {k: round(v, 3) for k, v in metrics(buy_hold(px)).items()})
    print("Benchmark:", {k: round(v, 3) for k, v in metrics(bench / bench.iloc[0]).items()})
    rnd = [metrics(backtest(px, bench, mode="random", seed=s, **base)[0])["CAGR"] for s in range(10)]
    print(f"Random picks (same filters+stops), 10 seeds: CAGR mean {np.mean(rnd):.3f}, range {min(rnd):.3f} to {max(rnd):.3f}")
    print("Momentum ranking adds value only if base CAGR clearly beats that range.")

    print("\n=== REGIMES (edit dates for your market) ===")
    splits = {"2010-14": ("2010-01-01", "2014-12-31"), "2015-17": ("2015-01-01", "2017-12-31"),
              "2018-19": ("2018-01-01", "2019-12-31"), "2020 crash+rebound": ("2020-01-01", "2020-12-31"),
              "2021": ("2021-01-01", "2021-12-31"), "2022 bear": ("2022-01-01", "2022-12-31"),
              "2023-26": ("2023-01-01", "2026-12-31")}
    print(periods(eq, bench, splits).to_string(index=False))

    print("\n=== PARAMETER SENSITIVITY (a robust rule works across the grid, not at one lucky spot) ===")
    rows = []
    for n, s, rg in itertools.product([10, 15, 25], [0.20, 0.30, 0.40], [True, False]):
        e, t = backtest(px, bench, top_n=n, stop=s, cost_bps=25, regime=rg)
        m = metrics(e, t); rows.append(dict(top_n=n, stop=s, regime=rg, CAGR=m["CAGR"], MaxDD=m["MaxDD"], Sharpe=m["Sharpe"]))
    print(pd.DataFrame(rows).to_string(index=False))

    print("\n=== COST STRESS ===")
    for c in [25, 50, 100]:
        e, t = backtest(px, bench, cost_bps=c, **{k: v for k, v in base.items() if k != "cost_bps"})
        print(f"cost {c} bps/side -> CAGR {metrics(e)['CAGR']:.3f}, MaxDD {metrics(e)['MaxDD']:.3f}")

if __name__ == "__main__":
    main()
