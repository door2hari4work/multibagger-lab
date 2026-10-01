"""Skeptic helpers. Instrumented COPY of backtest.backtest (backtest.py is untouched). Tune window only."""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np, pandas as pd
import config, data_loader, backtest as bt

START = pd.Timestamp(config.TUNE_START)

def load():
    px, b = data_loader.load_tune()
    return px, b

def bt_instr(px, bench, top_n=15, stop=0.30, cost_bps=25, regime=True, lookback=252, skip=21, ma=200, start=START):
    """Same logic as backtest.backtest(mode='momentum', end_policy='zero') plus logging."""
    px = bt.apply_end_policy(px, "zero").ffill()
    ret = px.pct_change().fillna(0.0)
    ma_ = px.rolling(ma).mean()
    mom = px.shift(skip) / px.shift(lookback) - 1
    hi52 = px.rolling(252).max()
    b_ok = (bench > bench.rolling(ma).mean()).reindex(px.index).ffill().fillna(False)
    dates = px.index
    last_of_month = set(px.groupby([dates.year, dates.month]).tail(1).index)
    cols = px.columns
    w = pd.Series(0.0, index=cols); peak = pd.Series(np.nan, index=cols)
    entry = {}; entry_date = {}; basis = {}
    pending_target = None; pending_exit = set()
    eq = [1.0]; eq_dates = [dates[0]]
    log = dict(stops=[], rebal_exits=[], realized=[], months=[], turnover=[], contrib=np.zeros((len(dates), len(cols))), wprev=[], cost=[])
    for i in range(1, len(dates)):
        d = dates[i]
        r = ret.iloc[i]
        log["contrib"][i] = (w * r).values * eq[-1]       # NAV-units contribution of each name today
        day_ret = float((w * r).sum())
        w = w * (1 + r); nav = eq[-1] * (1 + day_ret); w = w / (1 + day_ret)
        cost = 0.0; traded = 0.0
        if pending_exit:
            for t in pending_exit:
                if w[t] > 0:
                    cost += w[t] * cost_bps / 1e4; traded += w[t]
                    val = w[t] * nav
                    log["stops"].append(dict(ticker=t, entry_date=entry_date.get(t), exit_date=d, entry=entry.get(t), exit=px[t].iloc[i],
                                             peak=peak[t], flag_px=px[t].iloc[i-1]))
                    log["realized"].append((d, t, val - basis.get(t, val), (d - entry_date.get(t, d)).days))
                    w[t] = 0.0; peak[t] = np.nan; entry.pop(t, None); entry_date.pop(t, None); basis.pop(t, None)
            pending_exit = set()
        if pending_target is not None:
            tw = pending_target; pending_target = None
            dv = (tw - w)
            cost += dv.abs().sum() * cost_bps / 1e4; traded += dv.abs().sum()
            for t in cols:
                v0 = w[t] * nav; v1 = tw[t] * nav
                if w[t] > 0 and tw[t] == 0:
                    log["rebal_exits"].append(dict(ticker=t, entry_date=entry_date.get(t), exit_date=d, entry=entry.get(t), exit=px[t].iloc[i]))
                    log["realized"].append((d, t, v0 - basis.get(t, v0), (d - entry_date.get(t, d)).days))
                    entry.pop(t, None); entry_date.pop(t, None); basis.pop(t, None); peak[t] = np.nan
                elif w[t] > 0 and tw[t] > 0:
                    if v1 < v0:
                        f = 1 - v1 / v0; b0 = basis.get(t, v0)
                        log["realized"].append((d, t, (v0 - v1) - b0 * f, (d - entry_date.get(t, d)).days)); basis[t] = b0 * (1 - f)
                    else:
                        basis[t] = basis.get(t, v0) + (v1 - v0)
                elif w[t] == 0 and tw[t] > 0:
                    entry[t] = px[t].iloc[i]; entry_date[t] = d; peak[t] = px[t].iloc[i]; basis[t] = v1
            w = tw.copy()
        nav *= (1 - cost)
        log["turnover"].append((d, traded)); log["cost"].append((d, cost))
        eq.append(nav); eq_dates.append(d)
        held = w[w > 0].index
        if len(held):
            peak[held] = np.fmax(peak[held], px.loc[d, held])
            breach = [t for t in held if px.at[d, t] < peak[t] * (1 - stop)]
            if breach: pending_exit.update(breach)
        if d in last_of_month:
            elig = ((px.loc[d] > ma_.loc[d]) & (mom.loc[d] > 0) & (px.loc[d] >= 0.75 * hi52.loc[d])).fillna(False)
            if start is not None and d < pd.Timestamp(start): elig = elig & False
            cand = list(elig[elig].index)
            cand = list(mom.loc[d, cand].sort_values(ascending=False).index)[:top_n]
            tw = pd.Series(0.0, index=cols)
            on = bool(b_ok.loc[d])
            if on and cand: tw[cand] = 1.0 / top_n
            log["months"].append(dict(date=d, regime_on=on, n_elig=int(elig.sum()), n_sel=len(cand), cands=cand))
            pending_target = tw
    eq = pd.Series(eq, index=eq_dates)
    log["contrib"] = pd.DataFrame(log["contrib"], index=dates, columns=cols)
    return eq, log

def cagr(eq):
    eq = eq.loc[START:]; eq = eq / eq.iloc[0]
    yrs = (eq.index[-1] - eq.index[0]).days / 365.25
    return eq.iloc[-1] ** (1 / yrs) - 1

def mdd(eq):
    eq = eq.loc[START:]; return (eq / eq.cummax() - 1).min()

def rs(x):
    """Indian digit grouping."""
    neg = x < 0; x = int(round(abs(x))); s = str(x)
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]; parts = []
        while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        s = ",".join(parts + [tail])
    return ("-" if neg else "") + "Rs " + s
