"""Forward paper trading of FROZEN rules (paper/BOOKS.md). Run any time (weekly is enough); it is idempotent.

How it works: the engine in backtest.py is deterministic. Each run downloads recent prices, snapshots the index membership,
replays every book from its fixed start signal date over real prices (so NAV/holdings are always consistent), and appends what the
engine says to paper/signal_log.csv (append-only audit trail). No parameters may be changed after PAPER_START; to test a new idea,
add a NEW book with its own start date.

Rs 10,00,000 per book (US books are also expressed as Rs 10,00,000 of notional capital in USD terms: returns only, no FX).
Usage:  python paper/paper_trade.py
"""
import io, sys, json, time
from datetime import date
from pathlib import Path
import numpy as np, pandas as pd, requests, yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import backtest as bt  # noqa: E402

CAPITAL = 10_00_000
PAPER_START = "2026-10-30"          # first month-end signal date after the freeze (forward only; nothing before is simulated)
OUT = ROOT / "paper"; (OUT / "universe").mkdir(parents=True, exist_ok=True)
H = {"User-Agent": "Mozilla/5.0"}

MARKETS = {
    "IN": dict(index="^CRSLDX", bench="NIFTYBEES.NS", cost=25, cash=0.06, suffix=".NS"),
    "US": dict(index="^GSPC", bench="SPY", cost=10, cash=0.01, suffix=""),
}
# name -> (market, engine kwargs). FROZEN at PAPER_START. 'rebal' = frozen candidate; 'hold' = pre-declared challenger.
BOOKS = {
    "IN_rebal": ("IN", dict(top_n=25, stop=0.30, keep_winners=False)),
    "IN_hold": ("IN", dict(top_n=40, stop=0.40, keep_winners=True, exit_ma_break=True)),
    "US_rebal": ("US", dict(top_n=25, stop=0.30, keep_winners=False)),
    "US_hold": ("US", dict(top_n=40, stop=0.40, keep_winners=True, exit_ma_break=True)),
}


def members(mk):
    if mk == "IN":
        t = pd.read_csv(io.StringIO(requests.get("https://archives.nseindia.com/content/indices/ind_nifty500list.csv", headers=H, timeout=60).text))
        return sorted(t["Symbol"].str.strip() + ".NS")
    t = pd.read_html(io.StringIO(requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", headers=H, timeout=60).text))[0]
    return sorted(t["Symbol"].str.replace(".", "-", regex=False))


def snapshot(mk):
    """Save a dated membership snapshot when membership changed; returns {snapshot_date: set(symbols)} (point-in-time history from now on)."""
    cur = members(mk); files = sorted((OUT / "universe").glob(f"{mk}_*.csv"))
    if not files or set(pd.read_csv(files[-1])["symbol"]) != set(cur):
        pd.DataFrame({"symbol": cur}).to_csv(OUT / "universe" / f"{mk}_{date.today().isoformat()}.csv", index=False)
    return {pd.Timestamp(f.stem.split("_")[1]): set(pd.read_csv(f)["symbol"]) for f in sorted((OUT / "universe").glob(f"{mk}_*.csv"))}


def prices(symbols, start="2025-01-01"):
    fr = []
    for i in range(0, len(symbols), 50):
        for attempt in range(3):
            try:
                fr.append(yf.download(symbols[i:i + 50], start=start, auto_adjust=True, progress=False, threads=True)["Close"]); break
            except Exception:
                time.sleep(3)
    px = pd.concat(fr, axis=1).dropna(how="all"); px.index = pd.to_datetime(px.index).tz_localize(None)
    return px.loc[:, px.notna().sum() > 60].ffill(limit=5)


def run_market(mk, books):
    cfg = MARKETS[mk]; snaps = snapshot(mk)
    syms = sorted(set().union(*snaps.values()))
    px = prices(syms)
    ex = yf.download([cfg["index"], cfg["bench"]], start="2025-01-01", auto_adjust=True, progress=False)["Close"]; ex.index = pd.to_datetime(ex.index).tz_localize(None)
    idx = ex[cfg["index"]].dropna(); bench = ex[cfg["bench"]].dropna()
    reg = idx > idx.rolling(200).mean()
    mom, vol = px.shift(21) / px.shift(252) - 1, px.pct_change(fill_method=None).rolling(252).std() * np.sqrt(252)
    score = mom / vol
    gate = pd.DataFrame({d: pd.Series({s: s in m for s in px.columns}) for d, m in snaps.items()}).T  # membership as of snapshot dates, ffilled in engine
    results = {}
    for name, (m_, kw) in books.items():
        if m_ != mk: continue
        st = {}
        eq, tr = bt.backtest(px, idx, cost_bps=cfg["cost"], regime=True, regime_series=reg, score=score, cash_rate=cfg["cash"], start=PAPER_START, gate=gate, state=st, **kw)
        live = eq.loc[PAPER_START:] if pd.Timestamp(PAPER_START) <= eq.index[-1] else eq.iloc[:0]
        if len(live):
            nav = live / live.iloc[0] * CAPITAL; b = bench.loc[live.index[0]:]; bn = (b / b.iloc[0] * CAPITAL).reindex(nav.index).ffill()
        else:
            nav = pd.Series([CAPITAL], index=[eq.index[-1]]); bn = nav.copy()
        pd.DataFrame({"nav_rs": nav.round(0), "benchmark_rs": bn.round(0)}).to_csv(OUT / f"nav_{name}.csv")
        w = st["w"]; held = w[w > 0].sort_values(ascending=False)
        hold = pd.DataFrame({"weight": held.round(4), "rs_value": (held * float(nav.iloc[-1])).round(0), "entry_px": [st["entry"].get(t) for t in held.index], "last_px": px.loc[px.index[-1], held.index].round(2)})
        hold.to_csv(OUT / f"holdings_{name}.csv")
        # latest month-end signal (what the engine intends to hold next), logged append-only
        pend = st["pending"]; target = [] if pend is None else [t for t in pend.index if (pd.isna(pend[t]) or pend[t] > 0)]
        results[name] = dict(nav=float(nav.iloc[-1]), bench=float(bn.iloc[-1]), asof=str(px.index[-1].date()), regime_on=bool(reg.iloc[-1]), n_hold=int(len(held)),
                             target=target, dd=float((nav / nav.cummax() - 1).iloc[-1]), maxdd=float((nav / nav.cummax() - 1).min()), started=bool(len(live)))
    return results


def kill_switch(r):
    flags = []
    if r["dd"] <= -0.35: flags.append("HARD STOP: drawdown <= -35% from peak")
    elif r["dd"] <= -0.25: flags.append("WARNING: drawdown <= -25% from peak")
    return flags


def main():
    allr = {}
    for mk in MARKETS:
        try: allr.update(run_market(mk, BOOKS))
        except Exception as e: print(f"{mk}: FAILED {e!r}")
    log = OUT / "signal_log.csv"; rows = []
    for n, r in allr.items():
        rows.append(dict(run_date=date.today().isoformat(), book=n, asof=r["asof"], regime_on=r["regime_on"], n_hold=r["n_hold"], nav_rs=round(r["nav"]), benchmark_rs=round(r["bench"]), target=" ".join(r["target"])))
    if rows:
        pd.DataFrame(rows).to_csv(log, mode="a", header=not log.exists(), index=False)
    lines = [f"# Paper trading status (run {date.today().isoformat()}, prices as of {max(r['asof'] for r in allr.values()) if allr else 'n/a'})", "",
             f"Books start at the {PAPER_START} month-end signal with Rs {CAPITAL:,.0f} each; before that they are in cash. Rules are frozen (paper/BOOKS.md).", "",
             "| Book | Started | Regime | Holdings | NAV (Rs) | Benchmark (Rs) | Drawdown now | Worst DD | Flags |", "|---|---|---|---|---|---|---|---|---|"]
    for n, r in allr.items():
        lines.append(f"| {n} | {'yes' if r['started'] else 'not yet'} | {'ON' if r['regime_on'] else 'OFF'} | {r['n_hold']} | {r['nav']:,.0f} | {r['bench']:,.0f} | {r['dd']:.1%} | {r['maxdd']:.1%} | {'; '.join(kill_switch(r)) or '-'} |")
    (OUT / "STATUS.md").write_text("\n".join(lines) + "\n"); print("\n".join(lines))


if __name__ == "__main__":
    main()
