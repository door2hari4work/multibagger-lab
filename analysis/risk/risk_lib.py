"""Risk-manager tooling. Own engine mirroring backtest.backtest() (which is NOT modified) plus:
sizing variants (equal / inverse-vol / vol-target overlay / max-weight cap), detailed stop-fill logging,
max position weight tracking. Tune window only (data_loader.load_tune)."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np, pandas as pd
import config, data_loader
from backtest import apply_end_policy

CAP0 = config.START_CAPITAL_INR


def prep(px, bench, ma=200, lookback=252, skip=21):
    px = apply_end_policy(px, "zero").ffill()
    ret = px.pct_change().fillna(0.0)
    return dict(
        px=px, ret=ret, ma_=px.rolling(ma).mean(),
        mom=px.shift(skip) / px.shift(lookback) - 1, hi52=px.rolling(252).max(),
        vol63=ret.rolling(63).std() * np.sqrt(252),
        b_ok=(bench > bench.rolling(ma).mean()).reindex(px.index).ffill().fillna(False),
        bench=bench)


def run(P, top_n=15, stop=0.30, regime=True, cost_bps=25, sizing="equal", cap=None, vol_target=None,
        mode="momentum", seed=0, start="2010-01-01"):
    """sizing: 'equal' (1/top_n each, unfilled slots cash) | 'invvol' (inverse 63d vol, same gross as equal).
    cap: max weight per name at rebalance (excess to cash, or redistributed for invvol).
    vol_target: annualised vol target for a gross-exposure overlay (basket of picks, 63d)."""
    rng = np.random.default_rng(seed)
    px, ret = P["px"], P["ret"]
    cols = px.columns; n = len(cols); dates = px.index
    pxv, retv = px.values, ret.values
    last_of_month = set(px.groupby([dates.year, dates.month]).tail(1).index)
    w = np.zeros(n); peak = np.full(n, np.nan); entry = {}
    entry_i = {}
    trades = []; stops = []
    pending_target = None; pending_exit = set(); pending_exit_info = {}
    eq = [1.0]; eq_dates = [dates[0]]; maxw = [0.0]; gross = [0.0]
    for i in range(1, len(dates)):
        d = dates[i]
        day_ret = float((w * retv[i]).sum())
        w = w * (1 + retv[i]); nav = eq[-1] * (1 + day_ret); w = w / (1 + day_ret)
        cost = 0.0
        if pending_exit:
            for t in pending_exit:
                if w[t] > 0:
                    cost += w[t] * cost_bps / 1e4
                    e = entry.get(t)
                    trades.append(dict(t=cols[t], entry_i=entry_i.get(t), exit_i=i, entry=e, exit=pxv[i, t], why="stop", w=w[t]))
                    st = pending_exit_info[t]
                    stops.append(dict(t=cols[t], trig_i=i - 1, fill_i=i, level=st[0], trig_close=st[1], fill=pxv[i, t],
                                      entry=e, w=w[t], nav=nav))
                    w[t] = 0.0; peak[t] = np.nan; entry.pop(t, None)
            pending_exit = set()
        if pending_target is not None:
            tw = pending_target; pending_target = None
            cost += np.abs(tw - w).sum() * cost_bps / 1e4
            for t in range(n):
                if w[t] > 0 and tw[t] == 0:
                    trades.append(dict(t=cols[t], entry_i=entry_i.get(t), exit_i=i, entry=entry.get(t), exit=pxv[i, t], why="rebal", w=w[t]))
                    entry.pop(t, None); peak[t] = np.nan
                if tw[t] > 0 and w[t] == 0:
                    entry[t] = pxv[i, t]; entry_i[t] = i; peak[t] = pxv[i, t]
            w = tw.copy()
        nav *= (1 - cost)
        eq.append(nav); eq_dates.append(d); maxw.append(w.max()); gross.append(w.sum())
        # peaks + stop flags
        held = np.where(w > 0)[0]
        if len(held):
            peak[held] = np.fmax(peak[held], pxv[i, held])
            if stop is not None:
                for t in held:
                    if pxv[i, t] < peak[t] * (1 - stop):
                        pending_exit.add(t); pending_exit_info[t] = (peak[t] * (1 - stop), pxv[i, t])
        if d in last_of_month:
            elig = (P["px"].loc[d] > P["ma_"].loc[d]) & (P["mom"].loc[d] > 0) & (P["px"].loc[d] >= 0.75 * P["hi52"].loc[d])
            elig = elig.fillna(False)
            if mode == "random_all":
                elig = P["px"].loc[d].notna() & P["mom"].loc[d].notna()
            if start is not None and d < pd.Timestamp(start):
                elig = elig & False
            cand = list(elig[elig].index)
            if mode == "momentum":
                cand = list(P["mom"].loc[d, cand].sort_values(ascending=False).index)[:top_n]
            else:
                rng.shuffle(cand); cand = cand[:top_n]
            tw = np.zeros(n)
            if (not regime) or bool(P["b_ok"].loc[d]):
                if cand:
                    idx = [cols.get_loc(c) for c in cand]
                    tw[idx] = _weights(P, d, cand, idx, top_n, sizing, cap, vol_target)
            pending_target = tw
    eqs = pd.Series(eq, index=eq_dates)
    return dict(eq=eqs, trades=trades, stops=stops, maxw=pd.Series(maxw, index=eq_dates), gross=pd.Series(gross, index=eq_dates), cols=cols, dates=dates, px=pxv)


def _weights(P, d, cand, idx, top_n, sizing, cap, vol_target):
    k = len(cand)
    if sizing == "equal":
        wt = np.full(k, 1.0 / top_n)
    elif sizing == "invvol":
        v = P["vol63"].loc[d, cand].values.astype(float)
        v = np.where(np.isfinite(v) & (v > 0), v, np.nanmedian(v) if np.isfinite(v).any() else 0.3)
        raw = 1 / v; target_gross = k / top_n
        wt = raw / raw.sum() * target_gross
        if cap is not None:  # water-fill: clip and redistribute
            for _ in range(20):
                over = wt > cap
                if not over.any(): break
                excess = (wt[over] - cap).sum(); wt[over] = cap
                free = ~over & (wt < cap)
                if not free.any(): break
                wt[free] += excess * raw[free] / raw[free].sum()
            wt = np.minimum(wt, cap)
    else:
        raise ValueError(sizing)
    if cap is not None and sizing == "equal":
        wt = np.minimum(wt, cap)
    if vol_target:
        r = P["ret"].loc[:d, cand].iloc[-63:].mean(axis=1)
        bv = float(r.std() * np.sqrt(252))
        if bv > 0:
            wt = wt * min(1.0, vol_target / bv)
    return wt


# ---------------- risk statistics on a Rs equity curve ----------------
def rs_curve(eq, start="2010-01-01"):
    return data_loader.window(eq, start)

def inr(x):
    x = float(x); neg = x < 0; x = abs(round(x)); s = str(x if False else int(x))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        s = ",".join(parts + [tail])
    return ("-" if neg else "") + "Rs " + s

def underwater_stretches(e):
    """list of (peak_date, trough_date, recovery_date or None, depth, calendar_days_peak_to_recovery_or_end)"""
    rm = e.cummax(); out = []; i = 0; idx = e.index; n = len(e)
    while i < n:
        if e.iloc[i] < rm.iloc[i]:
            j = i
            while j > 0 and e.iloc[j - 1] < rm.iloc[j - 1]: j -= 1
            pk = idx[j - 1] if j > 0 else idx[0]
            k = i
            while k < n and e.iloc[k] < rm.iloc[k]: k += 1
            seg = e.iloc[j:k]
            tr = seg.idxmin()
            rec = idx[k] if k < n else None
            end = rec if rec is not None else idx[-1]
            out.append(dict(peak=pk, trough=tr, recovery=rec, depth=seg.min() / rm.iloc[i] - 1,
                            peak_val=rm.iloc[i], trough_val=seg.min(), days=(end - pk).days,
                            days_to_trough=(tr - pk).days))
            i = k
        else:
            i += 1
    return out

def risk_stats(e):
    """e: Rs equity curve (daily). Returns dict of the requested risk numbers."""
    dd = e / e.cummax() - 1
    tr = dd.idxmin(); pk = e.loc[:tr].idxmax()
    after = e.loc[tr:]; rec = after[after >= e.loc[pk]]
    rec_date = rec.index[0] if len(rec) else None
    uw = underwater_stretches(e)
    longest = max(uw, key=lambda s: s["days"]) if uw else None
    yrs = e.resample("YE").last(); yr_prev = pd.concat([pd.Series([e.iloc[0]], index=[e.index[0]]), yrs])
    yr = (yrs / yr_prev.shift(1).iloc[1:].values - 1)
    mo = e.resample("ME").last(); mo_prev = pd.concat([pd.Series([e.iloc[0]]), mo.reset_index(drop=True)]).values[:-1]
    mo_ret = pd.Series(mo.values / mo_prev - 1, index=mo.index)
    r12 = e / e.shift(252) - 1; r12 = r12.dropna()
    r12_end = r12.idxmin(); r12_start = e.index[e.index.get_loc(r12_end) - 252]
    yrs_n = (e.index[-1] - e.index[0]).days / 365.25
    rr = e.pct_change().dropna()
    return dict(
        CAGR=(e.iloc[-1] / e.iloc[0]) ** (1 / yrs_n) - 1, final=e.iloc[-1],
        mdd=dd.min(), mdd_peak=pk, mdd_trough=tr, mdd_peak_val=e.loc[pk], mdd_trough_val=e.loc[tr],
        mdd_rs=e.loc[pk] - e.loc[tr], mdd_recovery=rec_date,
        mdd_days_to_recover=(rec_date - pk).days if rec_date is not None else None,
        mdd_days_peak_trough=(tr - pk).days,
        worst_year=yr.idxmin().year, worst_year_ret=yr.min(), year_rets=yr,
        worst_12m=r12.min(), worst_12m_start=r12_start, worst_12m_end=r12_end,
        worst_12m_rs=e.loc[r12_end] - e.loc[r12_start],
        worst_month=mo_ret.idxmin().strftime("%Y-%m"), worst_month_ret=mo_ret.min(),
        worst_day=rr.min(), worst_day_date=rr.idxmin(),
        uw_days=longest["days"] if longest else 0, uw_peak=longest["peak"] if longest else None,
        uw_recovery=longest["recovery"] if longest else None, uw_depth=longest["depth"] if longest else None,
        vol=rr.std() * np.sqrt(252), sharpe0=rr.mean() / rr.std() * np.sqrt(252),
        calmar=(((e.iloc[-1] / e.iloc[0]) ** (1 / yrs_n) - 1) / -dd.min()),
        pct_time_underwater_10=(dd < -0.10).mean(), ulcer=np.sqrt((dd ** 2).mean()))
