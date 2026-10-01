"""Independent re-implementation of the backtest.py strategy (written from the spec, share/Rs based, numpy).
Adds: signal lag k (k=0 = base: signal at close t -> fill at close t+1; k=+1 extra bar late; k=-1 = same-bar fill = LOOK-AHEAD
cheat), whole-share mode, dated trade log, injectable candidate lists (for placebos). Does not touch backtest.py."""
import numpy as np, pandas as pd

def prep(px):
    return px.ffill()

def signals(px, bench, top_n=15, lookback=252, skip=21, ma=200, start="2010-01-01", pool=None, filt=True):
    """For each month-end index i: ordered candidate list (column idx) and regime flag. Pure numpy per date."""
    P = px.values; dates = px.index; n = len(dates)
    s = pd.Series(np.arange(n), index=dates)
    me = s.groupby([dates.year, dates.month]).tail(1).values
    bma = bench.rolling(ma).mean()
    breg = (bench > bma).reindex(dates).ffill().fillna(False).values
    out = {}
    for i in me:
        if dates[i] < pd.Timestamp(start) or i < lookback: 
            out[i] = ([], bool(breg[i])); continue
        cur = P[i]
        w200 = P[i-ma+1:i+1]
        ma_v = w200.mean(axis=0)               # NaN if any NaN in window
        w252 = P[i-251:i+1]
        hi = w252.max(axis=0)
        has = ~np.isnan(w252).any(axis=0)
        mom = P[i-skip] / P[i-lookback] - 1
        ok = has & (cur > ma_v) & (mom > 0) & (cur >= 0.75*hi)
        ok = ok & ~np.isnan(mom)
        if not filt: ok = ~np.isnan(cur) & ~np.isnan(mom)       # 'random_all' universe: any name with a price and a momentum value
        idx = np.where(ok)[0]
        idx = idx[np.argsort(-mom[idx], kind="stable")]
        out[i] = (list(idx), bool(breg[i]))
    return out

def sim(px, bench, sig=None, top_n=15, stop=0.30, cost_bps=25, regime=True, k=0, capital=1_000_000.0,
        whole_shares=False, perm=None, start="2010-01-01", **sk):
    """k: extra bars of delay between signal close and fill close (k=0 => t+1).  perm: dict month_end_idx -> other month_end_idx
    whose candidate list is used instead (placebo)."""
    P = px.values; dates = px.index; n = len(dates); cols = px.columns
    if sig is None: sig = signals(px, bench, top_n=top_n, start=start, **sk)
    reg = {i: v[1] for i, v in sig.items()}
    sh = np.zeros(P.shape[1]); cash = capital
    peak = np.full(P.shape[1], np.nan); ent_px = np.full(P.shape[1], np.nan); ent_i = np.full(P.shape[1], -1)
    pend_exit = {}; pend_tgt = {}
    nav_hist = np.full(n, np.nan); nav_hist[0] = capital
    trades = []   # (name, entry_idx, exit_idx, entry_px, exit_px, reason, entry_value)
    ent_val = np.zeros(P.shape[1])
    bps = cost_bps / 1e4
    def nav(i): return cash + np.nansum(sh * P[i])
    def do_exit(names, i):
        nonlocal cash
        for j in names:
            if sh[j] > 0:
                v = sh[j] * P[i, j]; cash += v - v * bps
                trades.append((cols[j], ent_i[j], i, ent_px[j], P[i, j], "stop", ent_val[j]))
                sh[j] = 0; peak[j] = np.nan
    def do_target(cand, i):
        nonlocal cash
        cur_val = sh * np.where(np.isnan(P[i]), 0, P[i])
        N = nav(i)
        tgt = np.zeros(len(sh))
        pos = N / top_n
        for j in cand:
            if not np.isnan(P[i, j]): tgt[j] = pos
        turn = np.abs(tgt - cur_val).sum()
        cf = turn * bps / N
        tgt = tgt * (1 - cf)           # same convention as backtest.py: cost scales the whole book
        for j in range(len(sh)):
            if sh[j] > 0 and tgt[j] == 0:
                trades.append((cols[j], ent_i[j], i, ent_px[j], P[i, j], "rebal", ent_val[j])); peak[j] = np.nan
            if tgt[j] > 0 and sh[j] == 0:
                ent_px[j] = P[i, j]; ent_i[j] = i; peak[j] = P[i, j]
        newsh = tgt / np.where(np.isnan(P[i]), 1, P[i])
        if whole_shares: newsh = np.floor(newsh)
        for j in range(len(sh)):
            if newsh[j] > 0 and sh[j] == 0: ent_val[j] = newsh[j] * P[i, j]
        # cash: total nav after cost minus invested
        sh[:] = newsh
        cash = N * (1 - cf) - np.nansum(sh * P[i])
    for i in range(1, n):
        if i in pend_exit: do_exit(pend_exit.pop(i), i)
        if i in pend_tgt: do_target(pend_tgt.pop(i), i)
        held = np.where(sh > 0)[0]
        if len(held):
            peak[held] = np.fmax(peak[held], P[i, held])
            br = [j for j in held if P[i, j] < peak[j] * (1 - stop)]
            if br:
                e = i + 1 + k
                if e <= i: do_exit(br, i)
                elif e < n: pend_exit.setdefault(e, set()).update(br)
        if i in sig:
            src = perm.get(i, i) if perm else i
            cand, _ = sig[src]
            ok_reg = (not regime) or reg[i]
            cand = list(cand[:top_n]) if ok_reg else []
            if perm and ok_reg:   # placebo list may contain names with no price today: do_target drops them
                pass
            e = i + 1 + k
            if e <= i: do_target(cand, i)
            elif e < n: pend_tgt[e] = cand
        nav_hist[i] = nav(i)
    eq = pd.Series(nav_hist, index=dates).ffill()
    return eq, trades

def trades_df(trades, dates):
    d = pd.DataFrame(trades, columns=["name","ei","xi","epx","xpx","why","eval"])
    d["edate"] = dates[d.ei.values]; d["xdate"] = dates[d.xi.values]
    d["ret"] = d.xpx / d.epx - 1
    d["pnl_frac"] = d["ret"] * d["eval"]
    return d
