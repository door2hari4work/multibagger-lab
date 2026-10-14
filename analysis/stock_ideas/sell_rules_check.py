"""Quick numerical checks for the sell / rebalance rules (yfinance adjusted closes; no costs, no taxes).
SURVIVORSHIP CAUTION: the single stocks are today's winners, so any rule that sells early looks costly here. Read together with the lab's
survivor-free-as-possible evidence (reports/3_risk_manager.md: trailing stops did not cut the tail and cost return)."""
import numpy as np, pandas as pd, os
from common import load_prices, OUT
P = load_prices(); pd.set_option("display.width", 220); pd.set_option("display.float_format", lambda x: f"{x:,.3f}")
TICK = ["MSFT", "GOOGL", "TSM", "AMZN", "NVDA", "MU", "META", "APH", "BNY"]; REF = ["QQQ", "SPY", "^NSEI"]

# ---------- (1) trailing stop on single names: hold vs stop (stay out) vs stop + re-enter above 200d MA ----------
def trailing(s, stop, reenter, start="2010-01-04"):
    s = s.dropna().loc[start:]; p = s.values; ma = s.rolling(200).mean().values
    # series has NaN MA until 200 days of history within slice -> compute MA on full history instead
    full = P[s.name].dropna(); ma = full.rolling(200).mean().reindex(s.index).values
    pos = True; hi = p[0]; val = 1.0; vals = [1.0]; stops = []; exit_px = None
    for t in range(1, len(p)):
        r = p[t] / p[t - 1] - 1
        if pos:
            val *= 1 + r; hi = max(hi, p[t])
            if p[t] <= hi * (1 - stop):          # trigger on close; exit at THIS close (optimistic: no gap beyond close)
                pos = False; stops.append(t); exit_px = p[t]
        else:
            if reenter and not np.isnan(ma[t]) and p[t] > ma[t]: pos = True; hi = p[t]
        vals.append(val)
    v = pd.Series(vals, index=s.index); dd = (v / v.cummax() - 1).min()
    wh = np.mean([p[min(t + 63, len(p) - 1)] > p[t] for t in stops]) if stops else np.nan   # whipsaw: higher 63d after the stop
    return v.iloc[-1], dd, len(stops), wh
rows = []
for t in TICK + REF:
    s = P[t].dropna(); s.name = t
    hold = s.loc["2010-01-04":]; hv = hold.iloc[-1] / hold.iloc[0]; hdd = (hold / hold.cummax() - 1).min()
    rows.append((t, "hold", hv, hdd, 0, np.nan))
    for stop in (0.20, 0.30):
        for re_ in (False, True):
            f, dd, n, wh = trailing(s, stop, re_); rows.append((t, f"stop{int(stop*100)}{'+re200' if re_ else ' stay-out'}", f, dd, n, wh))
T = pd.DataFrame(rows, columns=["t", "rule", "final_x", "maxDD", "n_stops", "whipsaw_63d_higher"])
print("== 1. Trailing stops, from 2010-01-04 (or listing) to 2026-10-13; final_x = multiple of starting value")
print(T.pivot(index="t", columns="rule", values="final_x").round(2).to_string())
print(T.pivot(index="t", columns="rule", values="maxDD").round(3).to_string())
print("stops / whipsaw share (higher 63d after stop):"); print(T[T.rule.str.startswith("stop")].groupby("rule").agg(n_stops=("n_stops", "sum"), whipsaw=("whipsaw_63d_higher", "mean")).round(3).to_string())
chk = T.pivot(index="t", columns="rule", values="final_x"); print("median final_x vs hold:", (chk.div(chk["hold"], axis=0)).median().round(2).to_dict())
T.to_csv(os.path.join(OUT, "trailing_stop_check.csv"), index=False)

# ---------- (2) weight drift: how fast does a 'target w0' satellite leave its band? (rest of portfolio = SPY) ----------
print("\n== 2. Weight drift of a satellite (start w0=3%, rest = SPY). Share of rolling windows in which the weight touched the level at any time")
def drift(t, w0=0.03, win=252, step=5):
    s = P[t].dropna(); b = P["SPY"].reindex(s.index).ffill(); out = []
    for i in range(0, len(s) - win, step):
        a = s.values[i:i + win + 1] / s.values[i]; m = b.values[i:i + win + 1] / b.values[i]
        w = w0 * a / (w0 * a + (1 - w0) * m); out.append((w.max() / w0, w.min() / w0))
    o = np.array(out); return (o[:, 0] >= 1.5).mean(), (o[:, 0] >= 2.0).mean(), (o[:, 1] <= 0.5).mean()
dr = pd.DataFrame({t: drift(t) for t in TICK + ["QQQ"]}, index=["touch 1.5x in 12m", "touch 2.0x in 12m", "fell to 0.5x in 12m"]).T
print(dr.round(3).to_string()); print("pooled single stocks:", dr.loc[TICK].mean().round(3).to_dict())

# ---------- (3) cost of trimming: position w0=5% vs SPY rest; hold vs trim-to-w0 when weight >= band x w0 vs annual rebalance ----------
print("\n== 3. Portfolio multiple 2010-01-04..2026-10-13 (or listing) of [5% stock + 95% SPY]: hold vs trim rules (no tax). Survivor bias: stocks are winners")
def trimsim(t, w0=0.05, band=None, annual=False):
    s = P[t].dropna().loc["2010-01-04":]; b = P["SPY"].reindex(s.index).ffill()
    rs = s.pct_change().fillna(0).values; rb = b.pct_change().fillna(0).values; idx = s.index
    x, y = w0, 1 - w0; last_year = idx[0].year
    for k in range(1, len(s)):
        x *= 1 + rs[k]; y *= 1 + rb[k]; tot = x + y
        if (band and x / tot >= band * w0) or (annual and idx[k].year != last_year):
            x, y = w0 * tot, (1 - w0) * tot
        last_year = idx[k].year
    return x + y
res = {t: {"hold": trimsim(t), "trim at 1.5x": trimsim(t, band=1.5), "trim at 2x": trimsim(t, band=2.0), "annual rebal": trimsim(t, annual=True)} for t in TICK}
R = pd.DataFrame(res).T; R["SPY only"] = P["SPY"].loc["2010-01-04":].iloc[-1] / P["SPY"].loc["2010-01-04"] if False else np.nan
spy_x = P["SPY"].loc["2010-01-04":]; spy_x = spy_x.iloc[-1] / spy_x.iloc[0]; R["SPY only"] = spy_x
print(R.round(2).to_string()); print("median trim-vs-hold ratio:", (R[["trim at 1.5x", "trim at 2x", "annual rebal"]].div(R["hold"], axis=0)).median().round(3).to_dict())
# the downside case: portfolio [5% stock + 95% SPY] through the stock's OWN worst drawdown since 2010 (peak -> trough), path started 2010-01-04
print("\n   Through each stock's worst drawdown since 2010: stock move, then portfolio move (% of portfolio) for hold vs trim rules")
def path(t, band=None, annual=False, w0=0.05):
    s = P[t].dropna().loc["2010-01-04":]; b = P["SPY"].reindex(s.index).ffill(); rs = s.pct_change().fillna(0).values; rb = b.pct_change().fillna(0).values
    x, y = w0, 1 - w0; ly = s.index[0].year; out = [1.0]; wt = [w0]
    for k in range(1, len(s)):
        x *= 1 + rs[k]; y *= 1 + rb[k]; tot = x + y
        if (band and x / tot >= band * w0) or (annual and s.index[k].year != ly): x, y = w0 * tot, (1 - w0) * tot
        ly = s.index[k].year; out.append(x + y); wt.append(x / (x + y))
    return pd.Series(out, index=s.index), pd.Series(wt, index=s.index)
for t in TICK:
    s = P[t].dropna().loc["2010-01-04":]; dd = s / s.cummax() - 1; tr = dd.idxmin(); pk = s.loc[:tr].idxmax()
    cells = []
    for nm, kw in [("hold", {}), ("trim1.5x", dict(band=1.5)), ("trim2x", dict(band=2.0)), ("annual", dict(annual=True))]:
        v, w = path(t, **kw); cells.append("%s %+.1f%% (wt at peak %.1f%%)" % (nm, (v.loc[tr] / v.loc[pk] - 1) * 100, w.loc[pk] * 100))
    print("   %-5s %s->%s stock %+.0f%% | %s" % (t, pk.date(), tr.date(), dd.min() * 100, " | ".join(cells)))

# ---------- (4) regime state today and whipsaw counts ----------
print("\n== 4. Regime filters (index close vs 200d simple MA)")
for t, nm in [("^GSPC", "S&P 500"), ("^CRSLDX", "Nifty 500")]:
    s = P[t].dropna(); ma = s.rolling(200).mean(); on = (s > ma)[ma.notna()]
    last = s.index[-1]; cur = on.iloc[-1]; chg = on.ne(on.shift()).cumsum(); since = on[chg == chg.iloc[-1]].index[0]
    cross = on.ne(on.shift()).loc["2021-10-13":].sum() - 1  # raw flips in last 5y
    # confirmation variants: needs 2% band beyond MA to flip
    st = on.iloc[0]; flips = 0
    for d in s.index[ma.notna()]:
        if st and s[d] < ma[d] * 0.98: st = False; flips += 1 if d >= pd.Timestamp("2021-10-13") else 0
        elif (not st) and s[d] > ma[d] * 1.02: st = True; flips += 1 if d >= pd.Timestamp("2021-10-13") else 0
    print("%-10s last %s close %.0f, 200d MA %.0f, distance %+.1f%%, state %s since %s; raw flips last 5y: %d ; with +/-2%% band: %d; pct of days ON (all history) %.0f%%"
          % (nm, last.date(), s.iloc[-1], ma.iloc[-1], (s.iloc[-1] / ma.iloc[-1] - 1) * 100, "ON" if cur else "OFF", since.date(), cross, flips, on.mean() * 100))

# regime-state conditional index returns (state known at yesterday's close), 2010-2026, raw vs 2% band vs weekly confirmation
print("\n   Index daily return conditional on yesterday's regime state (annualised mean %, annualised vol %, share of days), 2010-01-01..2026-10-13")
def states(s, rule):
    ma = s.rolling(200).mean(); st = []; cur = True
    for d in s.index:
        if np.isnan(ma[d]): st.append(np.nan); continue
        if rule == "raw": cur = s[d] > ma[d]
        elif rule == "band2":
            if cur and s[d] < ma[d] * 0.98: cur = False
            elif (not cur) and s[d] > ma[d] * 1.02: cur = True
        st.append(cur)
    return pd.Series(st, index=s.index)
for t, nm in [("^GSPC", "S&P 500"), ("^CRSLDX", "Nifty 500")]:
    s = P[t].dropna().loc["2009-01-01":]; r = s.pct_change()
    for rule in ("raw", "band2"):
        st = states(s, rule).shift(1); d = pd.DataFrame({"r": r, "on": st}).dropna().loc["2010-01-01":]
        on, off = d[d.on == True].r, d[d.on == False].r
        nflip = int((d.on != d.on.shift()).sum() - 1)
        print("   %-9s %-5s ON: %5.1f%%/yr vol %4.1f%% days %2.0f%% | OFF: %5.1f%%/yr vol %4.1f%% days %2.0f%% | flips %d (%.1f/yr)" % (nm, rule, on.mean() * 252 * 100, on.std() * np.sqrt(252) * 100, len(on) / len(d) * 100,
              off.mean() * 252 * 100, off.std() * np.sqrt(252) * 100, len(off) / len(d) * 100, nflip, nflip / ((d.index[-1] - d.index[0]).days / 365.25)))

print("\n   Index timing result 2010-01-01..2026-10-13 (price index, cash 0% when OFF, no costs): always-in vs in-only-when-ON (state of yesterday)")
for t, nm in [("^GSPC", "S&P 500"), ("^CRSLDX", "Nifty 500")]:
    s = P[t].dropna().loc["2009-01-01":]; r = s.pct_change()
    for rule in ("raw", "band2"):
        st = states(s, rule).shift(1); d = pd.DataFrame({"r": r, "on": st}).dropna().loc["2010-01-01":]
        yrs = (d.index[-1] - d.index[0]).days / 365.25
        eq_a = (1 + d.r).cumprod(); eq_f = (1 + d.r.where(d.on == True, 0.0)).cumprod()
        print("   %-9s %-5s always-in CAGR %.1f%% maxDD %.1f%% | filtered CAGR %.1f%% maxDD %.1f%% | worst calendar-year always-in %.1f%% filtered %.1f%%" % (nm, rule,
              (eq_a.iloc[-1] ** (1 / yrs) - 1) * 100, (eq_a / eq_a.cummax() - 1).min() * 100, (eq_f.iloc[-1] ** (1 / yrs) - 1) * 100, (eq_f / eq_f.cummax() - 1).min() * 100,
              eq_a.resample("YE").last().pct_change().min() * 100, eq_f.resample("YE").last().pct_change().min() * 100))
