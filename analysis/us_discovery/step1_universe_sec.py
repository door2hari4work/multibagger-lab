"""Step 1 of the US discovery screen: build the S&P 500 + S&P 400 universe (Wikipedia, current members, survivor-biased)
and pull SEC XBRL companyfacts (annual + discrete quarterly) into a compact per-ticker JSON cache.
SEC fair access: User-Agent built from env SEC_CONTACT (never written to a file), <= 4 requests/second, sequential.
Usage: SEC_CONTACT=<email> python step1_universe_sec.py <cache_dir> <universe_csv_out>"""
import io, os, sys, json, time
import pandas as pd, requests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from mblab.data import universe as U

cache_dir, uni_out = sys.argv[1], sys.argv[2]
os.makedirs(cache_dir, exist_ok=True)
UA = {"User-Agent": "multibagger-lab research " + os.environ["SEC_CONTACT"], "Accept-Encoding": "gzip, deflate"}

def wiki(url):
    t = pd.read_html(io.StringIO(U._get(url)))
    return next(x for x in t if "Symbol" in x.columns and "Security" in x.columns)

def build_universe():
    a = wiki("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"); a["index"] = "SP500"
    b = wiki(U.US_PAGES["mid"]); b["index"] = "SP400"
    df = pd.concat([a, b], ignore_index=True)
    df["ticker"] = df["Symbol"].map(U._yahoo_us)
    df = df.rename(columns={"Security": "name", "GICS Sector": "sector", "GICS Sub-Industry": "subindustry"})
    df = df.drop_duplicates("ticker")
    return df[["ticker", "name", "sector", "subindustry", "index", "CIK"]] if "CIK" in df else df[["ticker", "name", "sector", "subindustry", "index"]]

SEC_LAST = [0.0]
def sec_get(url):
    wait = 0.26 - (time.time() - SEC_LAST[0])
    if wait > 0: time.sleep(wait)
    SEC_LAST[0] = time.time()
    return requests.get(url, headers=UA, timeout=90)

FLOW = {
 "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet", "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueGoodsNet", "SalesRevenueServicesNet"],
 "opinc": ["OperatingIncomeLoss"],
 "netinc": ["NetIncomeLoss", "ProfitLoss"],
 "ocf": ["NetCashProvidedByUsedInOperatingActivities"],
 "capex": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
 "da": ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization", "DepreciationAmortizationAndAccretionNet"],
 "pretax": ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
 "intexp": ["InterestExpense", "InterestExpenseDebt", "InterestAndDebtExpense"],
 "eps": ["EarningsPerShareDiluted"],
 "shares": ["WeightedAverageNumberOfDilutedSharesOutstanding"],
}
UNITS = {"eps": "USD/shares", "shares": "shares"}

def series(facts, concepts, unit):
    """list of dict(start,end,val,filed,form) for the first concept that has data; latest-filed wins per (start,end)."""
    for c in concepts:
        items = facts.get(c, {}).get("units", {}).get(unit, [])
        if not items: continue
        best = {}
        for u in items:
            if "start" not in u: continue
            k = (u["start"], u["end"])
            if k not in best or u["filed"] > best[k]["filed"]: best[k] = u
        if best: return list(best.values()), c
    return [], None

def split_periods(items):
    ann, q = {}, {}
    fy = []
    for u in items:
        d = (pd.Timestamp(u["end"]) - pd.Timestamp(u["start"])).days
        if 340 <= d <= 380: ann[u["end"]] = u["val"]; fy.append((u["start"], u["end"], u["val"]))
        elif 80 <= d <= 100: q[u["end"]] = u["val"]
    # derive Q4 = FY - (Q1+Q2+Q3) when exactly three discrete quarters sit inside the fiscal year
    for s, e, v in fy:
        if e in q: continue
        ins = [qe for qe in q if pd.Timestamp(s) - pd.Timedelta(days=5) <= pd.Timestamp(qe) - pd.Timedelta(days=85) and pd.Timestamp(qe) < pd.Timestamp(e) - pd.Timedelta(days=30)]
        if len(ins) == 3: q[e] = v - sum(q[x] for x in ins)
    return ann, q

def extract(facts):
    out = {"ann": {}, "qtr": {}, "concepts": {}}
    for k, cs in FLOW.items():
        items, c = series(facts, cs, UNITS.get(k, "USD"))
        a, q = split_periods(items)
        if k in ("eps", "shares"): q = {}  # per-share series only used annually (split-factor handling downstream)
        out["ann"][k] = dict(sorted(a.items())[-8:]); out["qtr"][k] = dict(sorted(q.items())[-12:]); out["concepts"][k] = c
    return out

if __name__ == "__main__":
    uni = build_universe()
    tick = sec_get("https://www.sec.gov/files/company_tickers.json").json()
    cik_map = {v["ticker"].upper().replace(".", "-"): int(v["cik_str"]) for v in tick.values()}
    if "CIK" in uni: uni["cik"] = [int(c) if pd.notna(c) else cik_map.get(t) for c, t in zip(uni["CIK"], uni["ticker"])]
    else: uni["cik"] = uni["ticker"].map(cik_map)
    uni.loc[uni["cik"].isna(), "cik"] = uni.loc[uni["cik"].isna(), "ticker"].map(cik_map)
    uni.drop(columns=[c for c in ["CIK"] if c in uni]).to_csv(uni_out, index=False)
    print("universe", len(uni), uni["index"].value_counts().to_dict(), "no cik:", int(uni["cik"].isna().sum()), flush=True)
    t0 = time.time(); n = 0; miss = []
    for _, r in uni.iterrows():
        p = os.path.join(cache_dir, r["ticker"] + ".json")
        if os.path.exists(p) or pd.isna(r["cik"]):
            if pd.isna(r["cik"]): miss.append(r["ticker"])
            continue
        ok = False
        for attempt in range(3):
            try:
                resp = sec_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{int(r['cik']):010d}.json")
                if resp.status_code == 404: break
                resp.raise_for_status()
                f = resp.json()
                facts = f.get("facts", {}).get("us-gaap", {})
                ex = extract(facts); ex["entity"] = f.get("entityName"); ex["cik"] = int(r["cik"])
                json.dump(ex, open(p, "w")); ok = True; break
            except Exception as e:
                time.sleep(3 + 3 * attempt)
        if not ok: miss.append(r["ticker"])
        n += 1
        if n % 50 == 0: print(n, f"{time.time()-t0:.0f}s", flush=True)
    print("done", n, "missing/no data:", len(miss), miss[:60], flush=True)
