"""Step 3: Yahoo snapshot fields (valuation, consensus, balance sheet) for the universe. Unaudited aggregator data: context, cross-check against filings.
Usage: python step3_yahoo_info.py <universe_csv> <out_json>"""
import sys, json, time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import yfinance as yf
KEYS = ["marketCap", "enterpriseValue", "trailingPE", "forwardPE", "trailingEps", "forwardEps", "priceToBook", "priceToSalesTrailing12Months",
        "enterpriseToEbitda", "enterpriseToRevenue", "totalDebt", "totalCash", "ebitda", "freeCashflow", "operatingCashflow", "totalRevenue",
        "returnOnEquity", "returnOnAssets", "profitMargins", "operatingMargins", "grossMargins", "earningsGrowth", "earningsQuarterlyGrowth",
        "revenueGrowth", "targetMeanPrice", "targetHighPrice", "targetLowPrice", "recommendationMean", "numberOfAnalystOpinions",
        "shortPercentOfFloat", "beta", "dividendYield", "sharesOutstanding", "currentRatio", "debtToEquity", "heldPercentInstitutions",
        "heldPercentInsiders", "currentPrice", "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "lastFiscalYearEnd", "mostRecentQuarter", "bookValue",
        "payoutRatio", "quoteType", "financialCurrency", "exchange"]
def one(t):
    for a in range(3):
        try:
            info = yf.Ticker(t).info
            if info and len(info) > 5:
                return t, {k: info.get(k) for k in KEYS}
        except Exception:
            pass
        time.sleep(1.5 * (a + 1))
    return t, None
uni = pd.read_csv(sys.argv[1]); out = {}; t0 = time.time()
with ThreadPoolExecutor(6) as ex:
    for i, (t, v) in enumerate(ex.map(one, uni["ticker"].tolist()), 1):
        out[t] = v
        if i % 100 == 0: print(i, f"{time.time()-t0:.0f}s", flush=True)
json.dump(out, open(sys.argv[2], "w"))
print("done; missing:", [t for t, v in out.items() if v is None], flush=True)
