"""Stress test of the current portfolio (weights in weights.py) + betas / worst drawdowns from yfinance data.
Run: python analysis/stock_ideas/fetch_stress_data.py  (once) ;  python analysis/stock_ideas/portfolio_stress.py
Every assumption is labelled ASSUMPTION in the code or printed output. Outputs: analysis/stock_ideas/out/*.csv"""
import os, numpy as np, pandas as pd
from weights import HOLDINGS, UNALLOCATED
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
from common import load_prices
P = load_prices()                         # Yahoo split artifact in NIFTYBEES/GOLDBEES fixed; holiday gaps carried <=5 days
R = P.pct_change(fill_method=None)
W0, W1 = "2020-02-19", "2020-03-23"       # Feb-Mar 2020 window: S&P 500 / Nasdaq-100 / Nifty peak-ish to trough
pd.set_option("display.width", 200); pd.set_option("display.float_format", lambda x: f"{x:,.3f}")

def win_ret(t, a=W0, b=W1):
    s = P[t].loc[a:b].dropna(); return s.iloc[-1] / s.iloc[0] - 1
def own_min(t, a=W0, b=W1):
    s = P[t].loc[a:b].dropna(); return s.min() / s.iloc[0] - 1
def maxdd(s):
    s = s.dropna(); dd = s / s.cummax() - 1; tr = dd.idxmin(); pk = s.loc[:tr].idxmax(); return dd.min(), pk, tr
def weekly(cols, end="2026-10-09", years=5):
    w = P[cols].resample("W-FRI").last().pct_change(fill_method=None); return w.loc[pd.Timestamp(end) - pd.DateOffset(years=years): end]
def beta(y, x, data):
    d = data[[y, x]].dropna(); b = np.polyfit(d[x], d[y], 1)[0]; r2 = d.corr().iloc[0, 1] ** 2
    dn = d[d[x] < 0]; bd = np.polyfit(dn[x], dn[y], 1)[0] if len(dn) > 20 else np.nan
    return b, r2, bd, len(d)

# ---------------- 1. does the replay window match the scenario the investor specified? ----------------
print("== 1. Window check", W0, "->", W1)
chk = pd.Series({t: win_ret(t) for t in ["^GSPC", "^NDX", "^NSEI", "NIFTYBEES.NS", "JUNIORBEES.NS", "MID150BEES.NS", "^CNXIT", "GOLDBEES.NS", "GLD", "INR=X"]})
print(chk.round(4).to_string())

# ---------------- 2. betas (weekly, 5y to 2026-10-09) ----------------
US = ["MSFT", "GOOGL", "TSM", "AMZN", "NVDA", "MU", "META", "APH", "BNY", "QQQ", "SMH"]
wk = weekly(US + ["SPY", "RSP", "NIFTYBEES.NS", "JUNIORBEES.NS", "MID150BEES.NS", "^CNXIT", "GOLDBEES.NS", "INR=X"])
rows = []
for t in US:
    b_s, r_s, bd_s, n = beta(t, "SPY", wk); b_q, r_q, bd_q, _ = beta(t, "QQQ", wk) if t != "QQQ" else (np.nan,) * 4
    rows.append((t, b_s, r_s, bd_s, b_q, r_q, n))
B = pd.DataFrame(rows, columns=["inst", "beta_SPY", "R2_SPY", "downside_beta_SPY", "beta_QQQ", "R2_QQQ", "n_weeks"]).set_index("inst")
print("\n== 2a. US betas, weekly, 5y to 2026-10-09 (downside = weeks when the index fell)"); print(B.round(2).to_string())
IB = {}
for t in ["JUNIORBEES.NS", "MID150BEES.NS", "^CNXIT", "GOLDBEES.NS"]:
    IB[t] = beta(t, "NIFTYBEES.NS", wk)
print("\n== 2b. India betas vs NIFTYBEES (weekly 5y): beta, R2, downside beta, n"); [print(k, tuple(round(x, 2) for x in v)) for k, v in IB.items()]
# Nifty vs S&P 500 (INR ETF vs USD index; weekly) and Nifty vs USD/INR
bn_spy = beta("NIFTYBEES.NS", "SPY", wk); print("Nifty(INR) on SPY weekly beta/R2:", [round(x, 2) for x in bn_spy[:2]])
bs_nif = beta("SPY", "NIFTYBEES.NS", wk); print("SPY on Nifty weekly beta/R2 (reverse spillover):", [round(x, 2) for x in bs_nif[:2]])
d = wk[["NIFTYBEES.NS", "INR=X"]].dropna(); sl, ic = np.polyfit(d["INR=X"], d["NIFTYBEES.NS"], 1)
print("Nifty weekly return on USDINR weekly return: slope %.2f R2 %.2f (n=%d)" % (sl, d.corr().iloc[0, 1] ** 2, len(d)))
d2 = wk[["NIFTYBEES.NS", "INR=X"]].dropna(); dn = d2[d2["INR=X"] > d2["INR=X"].quantile(0.9)]
print("Nifty mean weekly return in the worst-10pct rupee weeks: %.3f (n=%d); all weeks %.3f" % (dn["NIFTYBEES.NS"].mean(), len(dn), d2["NIFTYBEES.NS"].mean()))
beta_tab = B.copy(); beta_tab.to_csv(os.path.join(OUT, "betas_us.csv"))

# ---------------- 3. worst drawdowns (full history, adjusted closes, from 2005 or listing) ----------------
dd_rows = []
for t in ["MSFT", "GOOGL", "TSM", "AMZN", "NVDA", "MU", "META", "APH", "BNY", "QQQ", "SPY", "SMH", "NIFTYBEES.NS", "JUNIORBEES.NS", "MID150BEES.NS", "^CNXIT", "GOLDBEES.NS", "^NSEI", "^CRSLDX"]:
    m, pk, tr = maxdd(P[t]); m22, pk22, tr22 = maxdd(P[t].loc["2021-11-01":"2022-12-31"])
    m25, pk25, tr25 = maxdd(P[t].loc["2024-06-01":"2026-10-13"])
    dd_rows.append((t, P[t].dropna().index[0].date(), m, pk.date(), tr.date(), m22, m25, win_ret(t) if t in P and P[t].loc[:W0].dropna().shape[0] else np.nan))
DD = pd.DataFrame(dd_rows, columns=["inst", "start", "maxDD_all", "peak", "trough", "DD_2021-11_to_2022-12", "DD_since_2024-06", "ret_2020win"]).set_index("inst")
print("\n== 3. Worst drawdowns"); print(DD.to_string()); DD.to_csv(os.path.join(OUT, "drawdowns.csv"))

# SMH episodes >= 20%: how often has a 'semis -40%' happened since 2005?
def episodes(s, thr):
    s = s.dropna(); dd = s / s.cummax() - 1; out = []; inep = False
    for i, (t, v) in enumerate(dd.items()):
        if v <= -thr and not inep: inep = True; pk = s.loc[:t].idxmax(); lo = v; lot = t
        if inep:
            if v < lo: lo, lot = v, t
            if v == 0: out.append((pk.date(), lot.date(), lo)); inep = False
    if inep: out.append((pk.date(), lot.date(), lo))
    return pd.DataFrame(out, columns=["peak", "trough", "depth"])
for t in ["SMH", "QQQ"]:
    print("\n  drawdown episodes >= 20%%: %s" % t); print(episodes(P[t], 0.20).to_string(index=False))

# ---------------- 4. Nasdaq-100 fund look-through to the AI-bust factors (data-driven, not from memory) ----------------
f = P[["QQQ", "SMH", "MSFT", "GOOGL", "AMZN", "META", "RSP"]].resample("W-FRI").last().pct_change(fill_method=None).loc["2023-10-01":"2026-10-09"].dropna()
f["MEGA4"] = f[["MSFT", "GOOGL", "AMZN", "META"]].mean(axis=1)
X = np.column_stack([f["SMH"], f["MEGA4"], f["RSP"]]); y = f["QQQ"].values
coef, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(f)), X]), y, rcond=None)
a, b_semi, b_mega, b_rest = coef; res = y - np.column_stack([np.ones(len(f)), X]) @ coef; r2 = 1 - res.var() / y.var()
print("\n== 4. QQQ = a + b_semi*SMH + b_mega*MEGA4 + b_rest*RSP (weekly, 3y, n=%d): a=%.4f b_semi=%.2f b_mega=%.2f b_rest=%.2f R2=%.2f" % (len(f), a, b_semi, b_mega, b_rest, r2))
NDX_AI_BUST = b_semi * -0.40 + b_mega * -0.30 + b_rest * -0.10
print("   implied Nasdaq-100 move in the AI bust: %.1f%% ; implied 'AI' share of the Nasdaq-100 fund (b_semi+b_mega) = %.0f%%" % (NDX_AI_BUST * 100, (b_semi + b_mega) * 100))

# ---------------- 5. scenarios ----------------
# 5a. replay shocks per holding (price, local currency)
ratio = lambda t, base="NIFTYBEES.NS": win_ret(t) / win_ret(base)
NIFTY_SHOCK, MID_SHOCK = -0.38, -0.40     # investor-specified
sh_a = {}
for h in HOLDINGS:
    n, w, tag, reg, usd = h
    if tag in ("mega", "semi", "rest", "emp"):
        tk = {"BNY (employer ESOP)": "BNY"}.get(n, n); sh_a[n] = win_ret(tk)            # actual instrument replay
    elif tag == "ndx": sh_a[n] = win_ret("^NDX")                                         # = about -28% (investor-specified -28)
    elif tag == "in50": sh_a[n] = NIFTY_SHOCK
    elif tag == "mid": sh_a[n] = MID_SHOCK
    elif tag == "next50": sh_a[n] = NIFTY_SHOCK * ratio("JUNIORBEES.NS")                 # replay relative to Nifty, scaled to -38%
    elif tag == "digital": sh_a[n] = NIFTY_SHOCK * ratio("^CNXIT", "^NSEI")             # ASSUMPTION: Tata Digital ~ Nifty IT index
    elif tag == "flexi": sh_a[n] = NIFTY_SHOCK                                           # ASSUMPTION: no NAV data; conservative beta 1.0 (real fund holds cash/foreign: likely less)
    elif tag == "infra": sh_a[n] = MID_SHOCK                                             # ASSUMPTION: capital-goods/PSU heavy -> midcap-like
    elif tag == "gold": sh_a[n] = 0.0                                                    # investor says 'gold up'; not credited (actual window: GLD -3.6%, GOLDBEES -4.6%)
# beta-scaled cross-check for US names: downside beta vs SPY x -34%  (Nasdaq fund: -28%)
sh_a_beta = dict(sh_a)
for h in HOLDINGS:
    n, w, tag, reg, usd = h
    if tag in ("mega", "semi", "rest", "emp"):
        tk = {"BNY (employer ESOP)": "BNY"}.get(n, n); sh_a_beta[n] = -0.34 * B.loc[tk, "downside_beta_SPY"]

# 5b. AI bust: semis -40, mega-cap tech -30, rest -10 (investor-specified)
sh_b = {}
for h in HOLDINGS:
    n, w, tag, reg, usd = h
    sh_b[n] = {"semi": -0.40, "mega": -0.30, "ndx": NDX_AI_BUST, "gold": 0.0}.get(tag, -0.10)   # rest/emp/India funds: -10 applied flat (conservative; India beta to S&P is lower, see sensitivity)
# 5c. rupee -10%: USD/INR +10%; US assets and INR gold gain, India equity unchanged
FX = 0.10
sh_c = {h[0]: 0.0 for h in HOLDINGS}
# 5d. Nifty -20 (rate-hike/oil): beta to Nifty
b_j = IB["JUNIORBEES.NS"][0]; b_m = IB["MID150BEES.NS"][0]; b_it = IB["^CNXIT"][0]
beta_d = {"in50": 1.0, "next50": b_j, "mid": b_m, "digital": b_it, "flexi": 1.0, "infra": b_m}   # flexi/infra = ASSUMPTION (see above)
sh_d = {h[0]: (-0.20 * beta_d.get(h[2], 0.0)) for h in HOLDINGS}
# 5e. combined = worst of price shocks (a,b,d) per holding, then rupee +10% on USD-linked holdings
sh_e_px = {h[0]: min(sh_a[h[0]], sh_b[h[0]], sh_d[h[0]]) for h in HOLDINGS}
def with_fx(sh, fx):
    return {h[0]: ((1 + sh[h[0]]) * (1 + fx) - 1 if h[4] else sh[h[0]]) for h in HOLDINGS}
sh_e = with_fx(sh_e_px, FX)
# 5g. stacked tail: 2020-style crash AND the AI bust on top for AI names (multiplicative); India = (a). Severe, not a forecast.
sh_st_px = dict(sh_a)
for h in HOLDINGS:
    if h[2] in ("semi", "mega", "ndx"): sh_st_px[h[0]] = (1 + sh_a[h[0]]) * (1 + sh_b[h[0]]) - 1
sh_st = with_fx(sh_st_px, FX)
# 5f. extra: employer-specific shock (BNY -50%) - not in the investor's list
sh_f = {h[0]: (-0.50 if h[2] == "emp" else 0.0) for h in HOLDINGS}

SC = {"(a) Feb-Mar 2020 replay": sh_a, "(a') same, beta-scaled US names": sh_a_beta, "(b) AI/semis bust": sh_b,
      "(c) INR -10% (USD/INR +10%)": with_fx(sh_c, FX), "(d) India rate/oil, Nifty -20": sh_d,
      "(e) combined worst-of + INR -10%": sh_e, "(e') combined, no FX cushion": sh_e_px, "(g) stacked crash+AI bust, INR -10%": sh_st, "(g') stacked, no FX cushion": sh_st_px, "(f) BNY -50% idiosyncratic": sh_f}
names = [h[0] for h in HOLDINGS]; wts = pd.Series({h[0]: h[1] for h in HOLDINGS})
contrib = pd.DataFrame({k: pd.Series(v) * wts for k, v in SC.items()}).reindex(names)   # % of NW (weight% x shock)
shock = pd.DataFrame({k: pd.Series(v) for k, v in SC.items()}).reindex(names)
tot = contrib.sum()
print("\n== 5. Shock per holding (price move, %)"); print((shock * 100).round(1).to_string())
print("\n== 5. Contribution to net worth (percentage points of NW); total row = portfolio move"); c2 = contrib.copy(); c2.loc["TOTAL"] = tot; print(c2.round(2).to_string())
contrib.to_csv(os.path.join(OUT, "stress_contrib.csv")); shock.to_csv(os.path.join(OUT, "stress_shock.csv"))

# sensitivities
print("\n== 6. Sensitivities")
def total(sh): return sum(wts[k] * sh[k] for k in names)
# (a) with the actual INR move of the window (+5.7%) on USD-linked assets, and with gold +10%
fx_a = win_ret("INR=X"); print("(a) with actual window INR move %+.1f%%: %.2f" % (fx_a * 100, total(with_fx(sh_a, fx_a))))
g = dict(sh_a); g["Axis Gold&Silver FoF"] = 0.10; print("(a) with gold +10%% instead of 0: %.2f" % total(g))
# (b) India scaled by Nifty beta to S&P; APH as AI hardware -30
bb = dict(sh_b)
for h in HOLDINGS:
    if h[3] == "IN" and h[2] not in ("gold",): bb[h[0]] = -0.10 * bn_spy[0] * (beta_d.get(h[2], 1.0))
print("(b) India funds = -10%% x beta(Nifty on SPY %.2f): %.2f" % (bn_spy[0], total(bb)))
bb2 = dict(sh_b); bb2["APH"] = -0.30; print("(b) APH as AI hardware -30%%: %.2f" % total(bb2))
b0 = {h[0]: (-0.40 if h[2] == "semi" else -0.30 if h[2] == "mega" else (b_semi * -0.40 + b_mega * -0.30) if h[2] == "ndx" else 0.0) for h in HOLDINGS}
print("(b) AI-only: semis -40, mega-cap -30, everything else 0 (Nasdaq fund = AI factors only): %.2f" % total(b0))
bb3 = dict(sh_b); bb3["ICICI Nasdaq-100 Idx"] = -0.30; print("(b) Nasdaq-100 fund at -30 (if fully mega-cap): %.2f" % total(bb3))
# (c) India equity co-moves with rupee weakness: use the regression slope (negative => equity falls when INR weakens)
cc = with_fx(sh_c, FX)
for h in HOLDINGS:
    if h[3] == "IN" and not h[4]: cc[h[0]] = sl * FX * beta_d.get(h[2], 1.0)
print("(c) India equity moves slope(%.2f) x 10%% (regression, weak R2): %.2f" % (sl, total(cc)))
# (d) US spillover: US holdings move by (SPY-on-Nifty beta) x (their beta to SPY) x Nifty shock
dd_ = dict(sh_d)
for h in HOLDINGS:
    if h[3] == "US" and h[2] in ("mega", "semi", "rest", "emp"):
        tk = "BNY" if h[2] == "emp" else h[0]; dd_[h[0]] = -0.20 * bs_nif[0] * B.loc[tk, "beta_SPY"] / 1.0
    if h[2] == "ndx": dd_[h[0]] = -0.20 * bs_nif[0] * B.loc["QQQ", "beta_SPY"]
print("(d) with US spillover (SPY-on-Nifty beta %.2f x each name's beta to SPY): %.2f" % (bs_nif[0], total(dd_)))
print("Unallocated %.1f%% of NW treated as cash/other with 0 shock (ASSUMPTION)." % UNALLOCATED)

# group views for (a)(b)(e)
grp = {"US direct (8 + employer)": [h[0] for h in HOLDINGS if h[3] == "US" and h[2] != "ndx"], "Nasdaq-100 fund": ["ICICI Nasdaq-100 Idx"],
       "India equity funds": [h[0] for h in HOLDINGS if h[3] == "IN" and h[2] != "gold"], "Gold": ["Axis Gold&Silver FoF"]}
G = pd.DataFrame({k: contrib.loc[v].sum() for k, v in grp.items()}).T; G["w"] = [wts[v].sum() for v in grp.values()]
print("\n== group contributions (pp of NW)"); print(G.round(2).to_string()); G.to_csv(os.path.join(OUT, "stress_groups.csv"))
# weights by theme for reference
for nm, tags in {"AI direct (mega+semi)": ("mega", "semi"), "semis direct": ("semi",), "US direct ex-employer": ("mega", "semi", "rest")}.items():
    print(nm, round(sum(h[1] for h in HOLDINGS if h[2] in tags), 2))
print("India-linked sum %.1f ; USD-linked (incl gold) %.1f" % (sum(h[1] for h in HOLDINGS if h[3] == "IN"), sum(h[1] for h in HOLDINGS if h[4])))

# ---------------- 7. back-cast: today's weights applied to proxy history since 2019-02 (INR terms) ----------------
# ASSUMPTION proxies: Nifty-50 funds = ^NSEI (price index; ~1.2%/yr dividends missing), Next-50 = JUNIORBEES, Midcap = MID150BEES,
# Flexi = Nifty 500 (^CRSLDX; conservative, no cash/foreign cushion), Infra = MID150BEES, Digital = ^CNXIT (Nifty IT), Gold = GOLDBEES (INR),
# Nasdaq fund = ^NDX x USDINR, US stocks/BNY = USD price x USDINR. Weights held constant (daily rebalanced). No fees.
fxr = P["INR=X"]
proxy = {"MSFT": P["MSFT"] * fxr, "GOOGL": P["GOOGL"] * fxr, "TSM": P["TSM"] * fxr, "AMZN": P["AMZN"] * fxr, "NVDA": P["NVDA"] * fxr, "MU": P["MU"] * fxr,
         "META": P["META"] * fxr, "APH": P["APH"] * fxr, "BNY (employer ESOP)": P["BNY"] * fxr, "ICICI Nasdaq-100 Idx": P["^NDX"] * fxr,
         "MO Nifty 50 Idx": P["^NSEI"], "Navi Nifty 50 Idx": P["^NSEI"], "HDFC Nifty Next 50": P["JUNIORBEES.NS"], "MO Midcap 150 Idx": P["MID150BEES.NS"],
         "Mirae Infra": P["MID150BEES.NS"], "PPFAS Flexi Cap": P["^CRSLDX"], "Tata Digital India": P["^CNXIT"], "Axis Gold&Silver FoF": P["GOLDBEES.NS"]}
PX = pd.DataFrame(proxy).loc["2019-02-05":].ffill(limit=5).dropna()
rr = PX.pct_change().dropna(); ww = wts.reindex(rr.columns) / 100.0
port = (rr * ww).sum(axis=1); nav = (1 + port).cumprod()
m, pk, tr = maxdd(nav); print("\n== 7. Back-cast of today's weights (INR terms, %.1f%% of NW in proxies, rest cash): maxDD %.1f%% peak %s trough %s" % (ww.sum() * 100, m * 100, pk.date(), tr.date()))
for a, b in [("2020-02-19", "2020-03-23"), ("2021-11-01", "2022-12-31"), ("2024-06-01", "2026-10-13"), ("2025-01-01", "2025-06-30")]:
    seg = nav.loc[a:b]; mm, p_, t_ = maxdd(seg); print("   %s..%s: window return %.1f%%, max DD inside %.1f%% (%s -> %s)" % (a, b, (seg.iloc[-1] / seg.iloc[0] - 1) * 100, mm * 100, p_.date(), t_.date()))
print("   annualised vol of the back-cast mix: %.1f%% ; worst day %.1f%% ; worst 21d %.1f%%" % (port.std() * np.sqrt(252) * 100, port.min() * 100, ((1 + port).rolling(21).apply(np.prod, raw=True) - 1).min() * 100))
parts = {"US direct+BNY": [h[0] for h in HOLDINGS if h[3] == "US" and h[2] != "ndx"], "Nasdaq fund": ["ICICI Nasdaq-100 Idx"], "India equity": [h[0] for h in HOLDINGS if h[3] == "IN" and h[2] != "gold"]}
for k, v in parts.items():
    sub = (rr[v] * ww[v]).sum(axis=1) / ww[v].sum(); n_ = (1 + sub).cumprod(); mm, p_, t_ = maxdd(n_); print("   sleeve %-14s maxDD %.1f%% (%s -> %s); vol %.1f%%" % (k, mm * 100, p_.date(), t_.date(), sub.std() * np.sqrt(252) * 100))
nav.to_csv(os.path.join(OUT, "backcast_nav.csv"))
