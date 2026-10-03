"""Point-in-time US annual fundamentals from SEC XBRL companyfacts (free, includes filing dates).
Per (company, fiscal-year end): ORIGINAL (earliest-filed) value of revenue, operating income, D&A, OCF, capex.
EBITDA = operating income + D&A. filed_date = latest of the earliest-filed dates of the metrics used (conservative).
Universe: current S&P 500 (survivor-biased; companies already gone are not in this list). Raw JSON is not stored."""
import os, json, time, requests, pandas as pd, numpy as np
from concurrent.futures import ThreadPoolExecutor
import config
UA = {"User-Agent": "multibagger-lab research " + os.environ["SEC_CONTACT"], "Accept-Encoding": "gzip, deflate"}  # SEC fair-access: contact email via env var, never committed
CONC = {
 "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet", "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueGoodsNet"],
 "opinc": ["OperatingIncomeLoss"],
 "da": ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization", "DepreciationAmortizationAndAccretionNet", "DepreciationNonproduction"],
 "ocf": ["NetCashProvidedByUsedInOperatingActivities"],
 "capex": ["PaymentsToAcquirePropertyPlantAndEquipment"],
}
sp = pd.read_csv(config.ROOT / "data/raw/sp500_current.csv")
tick = requests.get("https://www.sec.gov/files/company_tickers.json", headers=UA, timeout=60).json()
cik = {v["ticker"].upper().replace(".", "-"): int(v["cik_str"]) for v in tick.values()}

def annual_facts(facts, concepts):
    """period_end -> (value, earliest filed) from the first concept that has the period; annual duration, 10-K forms only."""
    out = {}
    for c in concepts:
        for u in facts.get(c, {}).get("units", {}).get("USD", []):
            if u.get("form") not in ("10-K", "10-K/A", "10-KT") or "start" not in u: continue
            dur = (pd.Timestamp(u["end"]) - pd.Timestamp(u["start"])).days
            if not 340 <= dur <= 380: continue
            k = u["end"]; f = u["filed"]
            if k not in out or f < out[k][1]: out[k] = (u["val"], f, c) if k not in out or f < out[k][1] else out[k]
    return out

def one(sym):
    if sym not in cik: return sym, None
    for attempt in range(3):
        try:
            r = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik[sym]:010d}.json", headers=UA, timeout=90)
            if r.status_code == 404: return sym, None
            r.raise_for_status(); facts = r.json().get("facts", {}).get("us-gaap", {}); break
        except Exception: time.sleep(2 + attempt * 3); facts = None
    if facts is None: return sym, None
    m = {k: {} for k in CONC}
    for k, cs in CONC.items():  # per period take the first concept (priority order) that exists, earliest-filed value
        seen = {}
        for c in cs:
            for e, v in annual_facts(facts, [c]).items():
                if e not in seen: seen[e] = v
        m[k] = seen
    rows = []
    for e in m["revenue"]:
        if e in m["opinc"] and e in m["da"]:
            rev, op, da = m["revenue"][e], m["opinc"][e], m["da"][e]
            ocf = m["ocf"].get(e); cap = m["capex"].get(e)
            filed = max(rev[1], op[1], da[1], ocf[1] if ocf else "0")
            rows.append(dict(symbol=sym, period_end=e, filed_date=filed, revenue=rev[0], ebitda=op[0] + da[0],
                             ocf=ocf[0] if ocf else np.nan, capex=cap[0] if cap else np.nan, period_type="A"))
    time.sleep(0.3)
    return sym, rows

if __name__ == "__main__":
    t0 = time.time(); res = {}
    with ThreadPoolExecutor(4) as ex:
        for sym, rows in ex.map(one, sp["Symbol"].tolist()): res[sym] = rows
    allr = [r for rows in res.values() if rows for r in rows]
    df = pd.DataFrame(allr).merge(sp.rename(columns={"Symbol": "symbol", "GICS Sector": "sector"})[["symbol", "sector"]], on="symbol")
    df.to_parquet(config.ROOT / "data/pit/us_fundamentals.parquet")
    n = df.symbol.nunique(); print(f"{n} of {len(sp)} symbols with data | rows {len(df)} | {time.time()-t0:.0f}s")
    print("period_end range", df.period_end.min(), df.period_end.max()); print("missing:", [s for s, r in res.items() if not r][:30])
    # coverage in tune window: symbols with >=2 FY rows filed before 2018-12-31
    t = df[pd.to_datetime(df.filed_date) <= "2018-12-31"].groupby("symbol").size(); print("symbols with >=2 FY filed by 2018-12-31:", int((t >= 2).sum()))
