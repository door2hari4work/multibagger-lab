"""India direct-stock IDEAS screen (Nifty 500, multi-factor).  Discovery only: NOT a buy list, no orders, no personal data.

Usage: python research/screen_IN_ideas.py <workdir>
Inputs in <workdir> (all derived market data, no portfolio data):
  universe.csv      Nifty 500 current members + segment (large = Nifty 500 minus Midcap 150 minus Smallcap 250)
  close.parquet     Yahoo adjusted closes (auto_adjust=True: split AND dividend adjusted), 2020-09 .. 2026-10-12
  vol.parquet       Yahoo volume
  fund/<T>.pkl      per-ticker pickles of yfinance info + quarterly/annual statements
Output: <workdir>/scored.pkl (consumed by the report builder)

DATA LIMITS (read before trusting any number)
  * Yahoo India fundamentals: about 5 quarters and 4-5 fiscal years, restated/as-shown, no filing dates, LATEST-ONLY (never backtestable).
  * Own-history valuation = current P/E (or P/B) vs the same measure at each of the last <=5 fiscal year-ends, computed as
    dividend-adjusted price at FY end x CURRENT share count / FY net income (or equity).  Share-count changes (QIPs, buybacks)
    and dividend adjustment distort it; n is at most 5, so it is a rough guide, not a percentile.
  * The factor weights are DECLARED heuristics.  The lab has validated only the 12-1 momentum rank (India large/mid strong,
    micro ~none; survivor-inflated).  The quality gate was NOT validated.  Nothing here is a validated selector.
  * Universe = current index members (survivor bias).  No point-in-time membership.
"""
from __future__ import annotations
import sys, os, pickle, math, warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from mblab.data import fundamentals as F   # compute_metrics: YoY / margin / TTM with gap bridging

WORK = sys.argv[1] if len(sys.argv) > 1 else "."
TODAY = pd.Timestamp("2026-10-13")
ADV_FLOOR_CR = 5.0       # Rs 5 crore median 20d traded value (lab default)
EXCLUDE_SECTORS = {"Healthcare": "sector report: avoid (pharma/healthcare rich, flat EPS)",
                   "Metals & Mining": "sector report: avoid (peak earnings)",
                   "Realty": "sector report: avoid (peak-earnings trap, rate hike)"}
COVERED = {"ACUTAAS", "AETHER", "APARINDS", "ATHERENERG", "CPPLUS", "CUPID", "HFCL", "KIRLOSENG", "LAURUSLABS", "MTARTECH",
           "RRKABEL", "SANSERA", "STLTECH", "TDPOWERSYS", "WELCORP"}   # theses/IN/ exist -> already deep-dived, do not repeat


def row(df, names):
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        return pd.Series(dtype=float)
    for n in names:
        if n in df.index:
            return pd.to_numeric(df.loc[n], errors="coerce").sort_index()
    return pd.Series(dtype=float)


def last(s):
    s = s.dropna()
    return float(s.iloc[-1]) if len(s) else np.nan


def f(x):
    try:
        x = float(x)
        return None if (math.isnan(x) or math.isinf(x)) else x
    except Exception:
        return None


def long_table(t, d):
    parts = []
    for key, ptype, ocfkey in (("qi", "Q", "qc"), ("ai", "A", None)):
        q = d.get(key)
        if q is None or q.empty:
            continue
        ocf = row(d.get(ocfkey), ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"]) if ocfkey else pd.Series(dtype=float)
        parts.append(F._stmt_rows(q, ocf, t, ptype))
    return pd.concat(parts, ignore_index=True) if parts else F._empty()


def fy_price(close, dt):
    s = close.dropna()
    s = s[s.index <= dt]
    return float(s.iloc[-1]) if len(s) else np.nan


def metrics_one(t, close, vol, d):
    out = dict(ticker=t)
    s = close.dropna(); s = s[s > 0]
    n = len(s)
    out["n_obs"] = n
    out["price"] = float(s.iloc[-1]); out["price_date"] = str(s.index[-1].date())
    tv = (close * vol).dropna().tail(20)
    out["adv_cr"] = float(tv.median() / 1e7) if len(tv) >= 15 else np.nan
    if n >= 253:
        out["mom_12_1"] = float(s.iloc[-22] / s.iloc[-253] - 1)
        out["ret_6m"] = float(s.iloc[-1] / s.iloc[-127] - 1)
        out["vol_ann"] = float(s.pct_change().dropna().tail(252).std() * np.sqrt(252))
    if n >= 200:
        ma200 = s.tail(200).mean(); ma50 = s.tail(50).mean()
        out["ma200"] = float(ma200); out["ma50"] = float(ma50)
        out["ext_ma200"] = float(s.iloc[-1] / ma200 - 1)
        out["above_ma200"] = bool(s.iloc[-1] > ma200)
        out["ma200_slope_60d"] = float(ma200 / s.iloc[-260:-60].tail(200).mean() - 1) if n >= 260 else np.nan
        hi = s.tail(252).max(); lo = s.tail(252).min()
        out["hi52"] = float(hi); out["lo52"] = float(lo)
        out["dd_52w_high"] = float(s.iloc[-1] / hi - 1)
        out["above_52w_low"] = float(s.iloc[-1] / lo - 1)
        out["dd_2y_peak"] = float(s.iloc[-1] / s.tail(504).max() - 1)
        w = s.tail(504); out["maxdd_2y"] = float((w / w.cummax() - 1).min())
    info = d.get("info", {}) or {}
    qi, ai, ab, ac = d.get("qi"), d.get("ai"), d.get("ab"), d.get("ac")
    shares = last(row(ab, ["Ordinary Shares Number", "Share Issued"]))
    sq = last(row(d.get("qb"), ["Ordinary Shares Number", "Share Issued"]))
    if not np.isnan(sq):
        shares = sq
    mcap_info = f(info.get("marketCap"))
    mcap = shares * out["price"] if shares == shares and shares > 0 else mcap_info
    out["shares_cr"] = shares / 1e7 if shares == shares else np.nan
    out["mcap_cr"] = mcap / 1e7 if mcap else np.nan
    lt = long_table(t, d)
    m = F.compute_metrics(lt, today=TODAY) if len(lt) else {}
    for k in ("latest_period", "staleness_days", "rev_yoy0", "rev_yoy1", "rev_accel", "margin0", "margin_delta", "margin_basis",
              "ebitda_yoy0", "ttm_revenue", "ttm_net_income", "ocf_ebitda"):
        out["q_" + k] = m.get(k)
    if qi is not None and not qi.empty:
        ni = row(qi, ["Net Income", "Net Income Common Stockholders"]).dropna()
        if len(ni):
            p0 = ni.index[-1]
            pm = [p for p in ni.index if abs((p0 - p).days - 365) <= 25]
            if pm and ni[pm[0]] > 0:
                out["q_ni_yoy"] = float(ni[p0] / ni[pm[0]] - 1)
            elif pm and ni[pm[0]] <= 0 and ni[p0] > 0:
                out["q_ni_turnaround"] = True
        out["q_n_quarters"] = int(qi.shape[1])
    rev = row(ai, ["Total Revenue", "Operating Revenue"]).dropna()
    ni_a = row(ai, ["Net Income", "Net Income Common Stockholders"]).dropna()
    ebitda_a = row(ai, ["EBITDA", "Normalized EBITDA"]).dropna()
    ebit_a = row(ai, ["EBIT", "Operating Income"]).dropna()
    intexp = row(ai, ["Interest Expense", "Interest Expense Non Operating"]).dropna()
    out["fy_last"] = str(rev.index[-1].date()) if len(rev) else None
    out["n_fy"] = int(len(rev))
    if len(rev) >= 2 and rev.iloc[-2] > 0:
        out["fy_rev_yoy"] = float(rev.iloc[-1] / rev.iloc[-2] - 1)
    if len(rev) >= 3 and rev.iloc[0] > 0 and rev.iloc[-1] > 0:
        yrs = (rev.index[-1] - rev.index[0]).days / 365.25
        out["fy_rev_cagr"] = float((rev.iloc[-1] / rev.iloc[0]) ** (1 / yrs) - 1); out["fy_span_yrs"] = round(yrs, 1)
    if len(ni_a) >= 3 and ni_a.iloc[0] > 0 and ni_a.iloc[-1] > 0:
        yrs = (ni_a.index[-1] - ni_a.index[0]).days / 365.25
        out["fy_ni_cagr"] = float((ni_a.iloc[-1] / ni_a.iloc[0]) ** (1 / yrs) - 1)
    if len(ni_a) >= 2 and ni_a.iloc[-2] > 0:
        out["fy_ni_yoy"] = float(ni_a.iloc[-1] / ni_a.iloc[-2] - 1)
    if len(ebitda_a) and len(rev):
        mg = (ebitda_a / rev.reindex(ebitda_a.index)).dropna()
        if len(mg):
            out["fy_ebitda_margin"] = float(mg.iloc[-1])
            if len(mg) >= 2:
                out["fy_margin_delta_1y"] = float(mg.iloc[-1] - mg.iloc[-2])
            if len(mg) >= 4:
                out["fy_margin_delta_vs_prior3avg"] = float(mg.iloc[-1] - mg.iloc[-4:-1].mean())
    eq = row(ab, ["Stockholders Equity", "Common Stock Equity", "Total Equity Gross Minority Interest"]).dropna()
    ta = row(ab, ["Total Assets"]).dropna()
    cl = row(ab, ["Current Liabilities", "Total Current Liabilities"]).dropna()
    debt = row(ab, ["Total Debt"]).dropna()
    cash = row(ab, ["Cash Cash Equivalents And Short Term Investments", "Cash And Cash Equivalents"]).dropna()
    if len(eq) and len(ni_a):
        idx = ni_a.index.intersection(eq.index)
        if len(idx):
            roe = (ni_a[idx] / eq[idx]).dropna()
            if len(roe):
                out["roe_fy"] = float(roe.iloc[-1]); out["roe_fy_avg3"] = float(roe.tail(3).mean())
    if len(ta) and len(cl) and len(ebit_a):
        idx = ebit_a.index.intersection(ta.index).intersection(cl.index)
        if len(idx):
            ce = (ta[idx] - cl[idx])
            roce = (ebit_a[idx] / ce).where(ce > 0).dropna()
            if len(roce):
                out["roce_fy"] = float(roce.iloc[-1]); out["roce_fy_avg3"] = float(roce.tail(3).mean())
    if len(debt) and len(eq) and eq.iloc[-1] > 0:
        out["de_fy"] = float(debt.iloc[-1] / eq.iloc[-1])
    if len(debt) and len(ebitda_a):
        nd = debt.iloc[-1] - (cash.iloc[-1] if len(cash) else 0)
        out["netdebt_cr"] = float(nd / 1e7)
        if ebitda_a.iloc[-1] > 0:
            out["netdebt_ebitda"] = float(nd / ebitda_a.iloc[-1])
    if len(ebit_a) and len(intexp) and intexp.iloc[-1] > 0:
        out["int_cover"] = float(ebit_a.iloc[-1] / intexp.iloc[-1])
    ocf = row(ac, ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"]).dropna()
    fcf = row(ac, ["Free Cash Flow"]).dropna()
    if len(ocf) and len(ebitda_a):
        idx = ocf.index.intersection(ebitda_a.index)
        if len(idx):
            r = (ocf[idx] / ebitda_a[idx]).where(ebitda_a[idx] > 0).dropna()
            if len(r):
                out["ocf_ebitda_fy"] = float(r.iloc[-1]); out["ocf_ebitda_fy_avg3"] = float(r.tail(3).mean())
    if len(ocf) and len(ni_a):
        idx = ocf.index.intersection(ni_a.index)[-3:]
        if len(idx) >= 2 and ni_a[idx].sum() > 0:
            out["ocf_ni_cum3"] = float(ocf[idx].sum() / ni_a[idx].sum())
    if len(fcf):
        out["fcf_fy_cr"] = float(fcf.iloc[-1] / 1e7)
        if mcap:
            out["fcf_yield"] = float(fcf.iloc[-1] / mcap)
    ttm_ni = out.get("q_ttm_net_income"); basis = "TTM(4q)"
    if ttm_ni is None or (isinstance(ttm_ni, float) and np.isnan(ttm_ni)):
        ttm_ni = float(ni_a.iloc[-1]) if len(ni_a) else None; basis = "FY"
    out["pe_basis"] = basis
    if mcap and ttm_ni and ttm_ni > 0:
        out["pe_now"] = float(mcap / ttm_ni); out["ttm_ni_cr"] = float(ttm_ni / 1e7)
    out["pe_yahoo"] = f(info.get("trailingPE")); out["fwd_pe_yahoo"] = f(info.get("forwardPE"))
    if mcap and len(eq) and eq.iloc[-1] > 0:
        out["pb_now"] = float(mcap / eq.iloc[-1])
    hist_pe, hist_pb = [], []
    if shares == shares and shares > 0:
        for dt in ni_a.index:
            p = fy_price(close, dt)
            if p == p and ni_a[dt] > 0:
                hist_pe.append(p * shares / ni_a[dt])
        for dt in eq.index:
            p = fy_price(close, dt)
            if p == p and eq[dt] > 0:
                hist_pb.append(p * shares / eq[dt])
    out["pe_hist_n"] = len(hist_pe)
    if len(hist_pe) >= 3:
        out["pe_hist_median"] = float(np.median(hist_pe)); out["pe_hist_min"] = float(min(hist_pe)); out["pe_hist_max"] = float(max(hist_pe))
        if out.get("pe_now"):
            out["pe_rel_hist"] = out["pe_now"] / out["pe_hist_median"]
    out["pb_hist_n"] = len(hist_pb)
    if len(hist_pb) >= 3:
        out["pb_hist_median"] = float(np.median(hist_pb))
        if out.get("pb_now"):
            out["pb_rel_hist"] = out["pb_now"] / out["pb_hist_median"]
    if mcap and len(debt) and len(ebitda_a) and ebitda_a.iloc[-1] > 0:   # own EV/EBITDA: market cap + last FY net debt over last FY EBITDA
        out["ev_ebitda"] = float((mcap + debt.iloc[-1] - (cash.iloc[-1] if len(cash) else 0)) / ebitda_a.iloc[-1])
    g = out.get("fy_ni_cagr")
    if out.get("pe_now") and g and g > 0.02:
        out["peg_like"] = out["pe_now"] / (min(g, 0.6) * 100)
    out["held_insiders_yahoo"] = f(info.get("heldPercentInsiders")); out["held_inst_yahoo"] = f(info.get("heldPercentInstitutions"))
    tm = f(info.get("targetMeanPrice"))
    out["target_mean_upside"] = (tm / out["price"] - 1) if tm else np.nan
    out["n_analysts"] = f(info.get("numberOfAnalystOpinions"))
    out["yahoo_industry"] = info.get("industry"); out["yahoo_name"] = info.get("shortName")
    return out


def pr(s, higher_better=True):
    """percentile rank 0..1 within the pool (NaN stays NaN)."""
    return s.rank(pct=True, na_option="keep", ascending=higher_better)


def score(g, fin):
    if not fin:
        val = pd.concat([pr(g.pe_rel_hist, False), pr(g.peg_like, False), pr(g.fcf_yield, True), pr(g.ev_ebitda, False)], axis=1).mean(axis=1, skipna=True)
        gro = pd.concat([pr(g.q_rev_yoy0), pr(g.q_ni_yoy), pr(g.q_margin_delta), pr(g.fy_ni_cagr), pr(g.fy_margin_delta_vs_prior3avg)], axis=1).mean(axis=1, skipna=True)
        qua = pd.concat([pr(g.roce_fy_avg3), pr(g.ocf_ebitda_fy_avg3), pr(g.ocf_ni_cum3), pr(g.int_cover.clip(upper=50))], axis=1).mean(axis=1, skipna=True)
        bs = pd.concat([pr(g.netdebt_ebitda.clip(-3, 10), False), pr(g.de_fy.clip(upper=3), False)], axis=1).mean(axis=1, skipna=True)
    else:
        val = pd.concat([pr(g.pb_rel_hist, False), pr(g.pe_rel_hist, False), pr(g.peg_like, False)], axis=1).mean(axis=1, skipna=True)
        gro = pd.concat([pr(g.q_ni_yoy), pr(g.fy_ni_cagr), pr(g.fy_rev_cagr), pr(g.q_rev_yoy0)], axis=1).mean(axis=1, skipna=True)
        qua = pd.concat([pr(g.roe_fy_avg3), pr(g.roe_fy)], axis=1).mean(axis=1, skipna=True)
        bs = pd.Series(np.nan, index=g.index)
    above = g.above_ma200.fillna(False).astype(bool)
    pos = 0.5 + 0.25 * above.astype(float) - 0.25 * (~above).astype(float)
    pos = pos - 0.25 * (g.ext_ma200 > 0.40).astype(float) - 0.25 * (g.dd_52w_high < -0.35).astype(float)
    price = (pr(g.mom_12_1).fillna(0.5) * 2 + pos.clip(0, 1)) / 3
    return pd.DataFrame({"s_value": val, "s_growth": gro, "s_quality": qua, "s_balance": bs, "s_price": price})


def main():
    u = pd.read_csv(os.path.join(WORK, "universe.csv"))
    close = pd.read_parquet(os.path.join(WORK, "close.parquet")); vol = pd.read_parquet(os.path.join(WORK, "vol.parquet"))
    rows, missing = [], []
    for _, r in u.iterrows():
        t = r.ticker
        p = os.path.join(WORK, "fund", f"{t}.pkl")
        if t not in close.columns or close[t].dropna().empty or not os.path.exists(p):
            missing.append(t); continue
        d = pickle.load(open(p, "rb"))
        try:
            m = metrics_one(t, close[t], vol[t], d)
        except Exception as e:
            missing.append(f"{t}:{type(e).__name__}:{e}"); continue
        m.update(name=r["Company Name"], nse_industry=r.Industry, segment=r.segment, symbol=r.Symbol)
        m["financial"] = bool(r.Industry == "Financial Services")
        yi = (m.get("yahoo_industry") or "").lower()
        m["bank_nbfc"] = bool(m["financial"] and any(k in yi for k in ("bank", "credit services", "mortgage finance")))
        rows.append(m)
    df = pd.DataFrame(rows)
    df["excl_reason"] = ""
    df.loc[df.adv_cr < ADV_FLOOR_CR, "excl_reason"] = "illiquid (<Rs 5 cr/day)"
    df.loc[df.n_obs < 273, "excl_reason"] = "short history"
    df.loc[~(df.ttm_ni_cr > 0), "excl_reason"] = "no positive TTM earnings / not computable"
    mask = df.nse_industry.isin(EXCLUDE_SECTORS)
    df.loc[mask, "excl_reason"] = df.loc[mask, "nse_industry"].map(lambda x: "sector avoid: " + EXCLUDE_SECTORS[x])
    df.loc[df.symbol.isin(COVERED), "excl_reason"] = "already deep-dived (theses/IN)"
    el = df[df.excl_reason == ""]
    comps = []
    for g, fin in ((el[~el.financial], False), (el[el.financial], True)):
        c = score(g, fin)
        w = {"s_price": 0.30, "s_value": 0.20, "s_growth": 0.20, "s_quality": 0.20, "s_balance": 0.10}
        if fin:
            w = {"s_price": 0.30, "s_value": 0.30, "s_growth": 0.20, "s_quality": 0.20}
        c["n_missing_comp"] = c[list(w)].isna().sum(axis=1)
        c["composite"] = sum(c[k].fillna(0.5) * v for k, v in w.items())   # missing component = neutral 0.5, counted in n_missing_comp
        comps.append(c)
    df = df.join(pd.concat(comps))
    return df, missing


if __name__ == "__main__":
    df, missing = main()
    df.to_pickle(os.path.join(WORK, "scored.pkl"))
    print(df.shape, "missing", len(missing), missing[:10])
    print((df.excl_reason == "").sum(), "eligible")
    print(df.excl_reason.value_counts().head(10))
