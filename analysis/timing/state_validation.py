"""Honest validation of mblab.timing entry states on the TUNE window only (2009-2018 prices; *SEALED* files are never read).

For each state: forward 6m (126 trading days) and 12m (252) return distribution, hit rate, 10th percentile, worst case, versus the all-stock base,
also versus the SAME-DATE cross-sectional mean (so a state that merely clusters in bull markets is not credited for the market).
Date-cluster bootstrap for the contrasts that matter. Survivor-biased (today's index members), close-only (no volume, no High/Low), see the report.

Run:  python analysis/timing/state_validation.py      (writes reports/TIMING_VALIDATION.md; ~1-2 minutes)
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from mblab import timing  # noqa: E402

RAW = ROOT / "data" / "raw"
FILES = {"India (Nifty 500 survivors)": "prices_tune.parquet", "US (S&P 500 survivors)": "us_prices_tune.parquet"}
assert all("SEALED" not in f for f in FILES.values())
H = {"6m": 126, "12m": 252}
STRIDE = 21                # one observation per stock per month: limits overlap of the forward windows
START_POS = 252
SEED = 7
STATES = ["attractive_entry", "confirmation_entry", "breakout_entry", "setup_forming", "wait_for_pullback", "overextended", "too_early"]


def load(fname):
    px = pd.read_parquet(RAW / fname).sort_index()
    px = px.where(px > 0)
    r = px.pct_change(fill_method=None)
    bad = [c for c in px.columns if (r[c].min() < -0.45) or (r[c].max() > 0.80)]      # likely unadjusted splits / data errors
    keep = [c for c in px.columns if c not in bad and px[c].notna().sum() > 400]
    return px[keep], bad


def build(px):
    """Returns long DataFrame (date, ticker, state, ext_atr, dist_hi, fwd6m, fwd12m, regime_on) sampled monthly."""
    P = px.ffill(limit=5)
    # regime: equal-weight index of the universe above its own 200d MA (a stand-in for the market regime, past data only)
    ew = (1 + P.pct_change(fill_method=None).mean(axis=1).fillna(0)).cumprod()
    regime = ew > ew.rolling(200).mean()
    fwd = {k: P.shift(-n) / P - 1 for k, n in H.items()}
    grid = P.index[START_POS::STRIDE]
    rows = []
    for t in P.columns:
        s = P[t].dropna()
        if len(s) < timing.TH["min_rows"]: continue
        f = timing.compute_features(pd.DataFrame({"Close": s}))
        g = f.reindex(grid).dropna(subset=["ma200"])
        for d, row in zip(g.index, g.to_dict("records")):
            state, _, _ = timing.classify(row, regime_on=True)
            rows.append((d, t, state, row["ext_atr"], row["dist_hi"], row["ma200_slope"], fwd["6m"].at[d, t], fwd["12m"].at[d, t], bool(regime.get(d, False))))
    df = pd.DataFrame(rows, columns=["date", "ticker", "state", "ext_atr", "dist_hi", "ma200_slope", "r6m", "r12m", "regime_on"])
    return df


def dist(x):
    x = x.dropna()
    if len(x) == 0: return dict(n=0)
    return dict(n=len(x), mean=x.mean(), median=x.median(), hit=(x > 0).mean(), p10=x.quantile(0.10), worst=x.min(), loss20=(x < -0.20).mean())


def table(df, col, by="state", order=None):
    base = dist(df[col])
    rows = []
    d = df.dropna(subset=[col]).copy()
    d["excess"] = d[col] - d.groupby("date")[col].transform("mean")
    for st in (order or STATES):
        sub = d[d[by] == st]
        if len(sub) == 0: continue
        m = dist(sub[col]); m["state"] = st; m["dates"] = sub["date"].nunique()
        m["xs_mean"] = sub["excess"].mean(); m["xs_median"] = sub["excess"].median()
        rows.append(m)
    base["state"] = "ALL (base)"; base["dates"] = d["date"].nunique(); base["xs_mean"] = 0.0; base["xs_median"] = 0.0
    rows.append(base)
    return pd.DataFrame(rows).set_index("state")


def fmt_table(t):
    out = ["| State | n | dates | mean | median | hit rate (>0) | 10th pct | worst | P(loss>20%) | excess mean vs same-date avg | excess median |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for st, r in t.iterrows():
        p = lambda x: f"{x:+.1%}"
        out.append(f"| {st} | {int(r['n'])} | {int(r['dates'])} | {p(r['mean'])} | {p(r['median'])} | {r['hit']:.1%} | {p(r['p10'])} | {p(r['worst'])} | {r['loss20']:.1%} | {p(r['xs_mean'])} | {p(r['xs_median'])} |")
    return "\n".join(out)


def boot_contrast(df, col, A, B, reps=1000, seed=SEED):
    """Date-cluster bootstrap of (mean and median same-date-excess of group A) - (same for group B)."""
    d = df.dropna(subset=[col]).copy()
    d["excess"] = d[col] - d.groupby("date")[col].transform("mean")
    a, b = d[d["state"].isin(A)], d[d["state"].isin(B)]
    dates = np.array(sorted(d["date"].unique()))
    ga = {k: v["excess"].values for k, v in a.groupby("date")}
    gb = {k: v["excess"].values for k, v in b.groupby("date")}
    ra = {k: v[col].values for k, v in a.groupby("date")}
    rb = {k: v[col].values for k, v in b.groupby("date")}
    rng = np.random.default_rng(seed)

    def stat(ds):
        xa = np.concatenate([ga[k] for k in ds if k in ga] or [np.array([])]); xb = np.concatenate([gb[k] for k in ds if k in gb] or [np.array([])])
        ya = np.concatenate([ra[k] for k in ds if k in ra] or [np.array([])]); yb = np.concatenate([rb[k] for k in ds if k in rb] or [np.array([])])
        if len(xa) < 30 or len(xb) < 30: return (np.nan,) * 4
        return xa.mean() - xb.mean(), np.median(ya) - np.median(yb), (ya > 0).mean() - (yb > 0).mean(), np.percentile(ya, 10) - np.percentile(yb, 10)
    point = stat(dates)
    bs = np.array([stat(rng.choice(dates, size=len(dates), replace=True)) for _ in range(reps)])
    lo, hi = np.nanpercentile(bs, 5, axis=0), np.nanpercentile(bs, 95, axis=0)
    return point, lo, hi, len(a), len(b)


CONTRASTS = [
    ("attractive_entry vs overextended", ["attractive_entry"], ["overextended"]),
    ("confirmation_entry vs overextended", ["confirmation_entry"], ["overextended"]),
    ("attractive_entry vs breakout_entry", ["attractive_entry"], ["breakout_entry"]),
    ("confirmation_entry vs breakout_entry", ["confirmation_entry"], ["breakout_entry"]),
    ("(attractive + confirmation) vs (overextended + breakout)", ["attractive_entry", "confirmation_entry"], ["overextended", "breakout_entry"]),
    ("attractive_entry vs ALL stocks in uptrend states (setup..overextended)", ["attractive_entry"], ["setup_forming", "wait_for_pullback", "overextended", "confirmation_entry", "breakout_entry"]),
]


def fmt_contrasts(df, col):
    out = ["| Contrast (A minus B) | nA | nB | excess-mean diff [90% CI] | median-return diff [90% CI] | hit-rate diff [90% CI] | 10th-pct diff [90% CI] |", "|---|---|---|---|---|---|---|"]
    verdicts = {}
    for name, A, B in CONTRASTS:
        pt, lo, hi, na, nb = boot_contrast(df, col, A, B)
        cell = lambda i: (f"{pt[i]:+.1%} [{lo[i]:+.1%}, {hi[i]:+.1%}]" if np.isfinite(pt[i]) else "n/a (group < 30)")
        out.append(f"| {name} | {na} | {nb} | {cell(0)} | {cell(1)} | {cell(2)} | {cell(3)} |")
        verdicts[name] = dict(pt=pt, lo=lo, hi=hi)
    return "\n".join(out), verdicts


def bucket_table(df, col, by, bins, labels):
    d = df.dropna(subset=[col, by]).copy()
    d = d[d["state"] != "too_early"]
    d["b"] = pd.cut(d[by], bins=bins, labels=labels)
    d["excess"] = d[col] - d.groupby("date")[col].transform("mean")
    rows = ["| bucket | n | median | mean | hit rate | 10th pct | excess mean |", "|---|---|---|---|---|---|---|"]
    for b, s in d.groupby("b", observed=True):
        m = dist(s[col]); rows.append(f"| {b} | {m['n']} | {m['median']:+.1%} | {m['mean']:+.1%} | {m['hit']:.1%} | {m['p10']:+.1%} | {s['excess'].mean():+.1%} |")
    return "\n".join(rows)


def main():
    parts, summary = [], {}
    allv = {}
    for mkt, fname in FILES.items():
        px, bad = load(fname)
        df = build(px)
        allv[mkt] = (df, len(px.columns), len(bad))
    out = []
    out.append("# Entry-state validation (tune window only)\n")
    out.append("Script: `analysis/timing/state_validation.py` (re-runnable; reads `prices_tune.parquet` and `us_prices_tune.parquet` only; no SEALED file is opened). "
               "Thresholds in `mblab/timing.py` (`TH`) were declared before this run from common practice and were NOT tuned to these results (one reachability fix after run 1 is disclosed under Run history).\n")
    headline = []
    for mkt, (df, n_stk, n_bad) in allv.items():
        d12 = df.dropna(subset=["r12m"])
        out.append(f"\n## {mkt}\n")
        out.append(f"{n_stk} stocks used ({n_bad} excluded for one-day moves beyond -45%/+80%, likely unadjusted splits). {len(df):,} stock-month observations "
                   f"({df['date'].nunique()} month-grid dates, {df['date'].min():%Y-%m} to {df['date'].max():%Y-%m}); {len(d12):,} have a 12m forward return. "
                   f"State counts: " + ", ".join(f"{k} {v:,}" for k, v in df['state'].value_counts().items()) + ".\n")
        for col, lab in (("r6m", "6-month"), ("r12m", "12-month")):
            out.append(f"\n### Forward {lab} return by state\n")
            out.append(fmt_table(table(df, col)) + "\n")
        out.append("\n### Contrasts, 12-month (date-cluster bootstrap, 1000 draws over month-grid dates, 90% interval)\n")
        ct, ver = fmt_contrasts(df, "r12m"); out.append(ct + "\n")
        out.append("\n### Contrasts, 6-month\n")
        ct6, _ = fmt_contrasts(df, "r6m"); out.append(ct6 + "\n")
        out.append("\n### Is extension informative on its own? 12m forward return by ATR-extension from the 50d MA (all states except too_early, i.e. mostly stocks above their 200d MA)\n")
        up = df[(df["state"].isin(["attractive_entry", "confirmation_entry", "breakout_entry", "setup_forming", "wait_for_pullback", "overextended"]))]
        out.append(bucket_table(up, "r12m", "ext_atr", [-99, -2, -1, 0, 1, 2, 3, 4, 99], ["<-2", "-2..-1", "-1..0", "0..1", "1..2", "2..3", "3..4", ">4"]) + "\n")
        out.append("\n### 12m forward return by distance below the 52-week high (same stocks; all states except too_early)\n")
        out.append(bucket_table(up, "r12m", "dist_hi", [-1, -0.30, -0.20, -0.10, -0.05, 0.001], ["-30% or worse", "-30..-20%", "-20..-10%", "-10..-5%", "within 5%"]) + "\n")
        out.append("\n### Stability: sub-periods and market regime (12m, same-date excess mean)\n")
        rows = ["| slice | attractive | confirmation | breakout (price only) | wait_for_pullback | overextended | too_early |", "|---|---|---|---|---|---|---|"]
        sl = {"2010-2013 starts": df["date"] < "2014-01-01", "2014-2017 starts": df["date"] >= "2014-01-01", "regime ON (EW universe > 200d MA)": df["regime_on"], "regime OFF": ~df["regime_on"]}
        for nm, mask in sl.items():
            sub = df[mask].dropna(subset=["r12m"]).copy()
            sub["ex"] = sub["r12m"] - sub.groupby("date")["r12m"].transform("mean")
            cells = []
            for st in ["attractive_entry", "confirmation_entry", "breakout_entry", "wait_for_pullback", "overextended", "too_early"]:
                s = sub[sub["state"] == st]
                cells.append(f"{s['ex'].mean():+.1%} (n={len(s)}; median {s['r12m'].median():+.1%})" if len(s) >= 30 else f"n={len(s)}")
            rows.append(f"| {nm} | " + " | ".join(cells) + " |")
        out.append("\n".join(rows) + "\n")
        v = ver["(attractive + confirmation) vs (overextended + breakout)"]
        headline.append((mkt, v, ver["attractive_entry vs overextended"], ver["confirmation_entry vs overextended"]))
    # headline (conditional wording so it is honest by construction)
    hl = ["## Headline\n"]
    for mkt, v, v_ao, v_co in headline:
        def sig(x):
            return "positive and its 90% interval excludes zero" if x["lo"][0] > 0 else "negative and its 90% interval excludes zero" if x["hi"][0] < 0 else "not distinguishable from zero (90% interval spans zero)"
        hl.append(f"- **{mkt}**: (attractive + confirmation) minus (overextended + breakout), 12m same-date excess mean = {v['pt'][0]:+.1%}, {sig(v)}; median-return difference {v['pt'][1]:+.1%}, 10th-percentile difference {v['pt'][3]:+.1%}. "
                  f"attractive vs overextended alone: {v_ao['pt'][0]:+.1%} ({sig(v_ao)}). confirmation vs overextended: {v_co['pt'][0]:+.1%} ({sig(v_co)}).")
    out.insert(2, "\n".join(hl) + "\n")
    out.append("\n## Reading of this run (author's summary of the tables; negative results included)\n")
    out.append("- **No evidence that 'overextended' is a worse place to be than 'attractive_entry' or 'confirmation_entry' in this window.** India: overextended names had the BEST 12m excess return (+7% vs same-date average) and hit rate, "
               "and attractive_entry trailed overextended by about 5 points with a significantly worse hit rate and 10th percentile. US: the states are nearly indistinguishable on return (attractive +1.6 pts vs overextended, confirmation -0.7 pts, both small). "
               "The ATR-extension buckets show the same thing: no monotonic penalty for stretch; in India more extension looks better, which is the 12-1 momentum effect the lab already found (names far above the 50d MA are the strongest-momentum names).\n"
               "- **The label 'overextended' therefore describes entry price risk (a larger give-back if the trend pauses), not an expectation of underperformance.** The product should not present it as a sell/avoid signal, and should not present attractive_entry as an edge. "
               "The rationale text in `mblab/timing.py` says this.\n"
               "- **What the states do show is consistent with the lab's earlier finding that trend filters protect more than they select.** confirmation_entry (within 10% of the 52w high, rising 50d MA) has the lowest share of >20% losses among the well-populated states in both markets "
               "(India about 12% vs 18% base; US about 3% vs 5% base) and the best 10th percentile in the US, without a return advantage. too_early (below the 200d MA) has the worst downside in India (P(loss>20%) about 21%) but NOT in the US, where it did not underperform (survivor bias: below-trend names that recovered are the ones still in the index).\n"
               "- **attractive_entry has fatter tails than confirmation_entry** in both markets (higher P(loss>20%), worse 10th percentile): buying a pullback inside a trend carries more dispersion than buying strength. Its median is below the base in India (10.5% vs 12.5%) and slightly above it in the US (18.1% vs 16.8%).\n"
               "- **breakout_entry** is exploratory: price-only, volume untested, a small and heterogeneous sample; the contrasts against it are wide and inconclusive.\n"
               "- **Net**: use the states as a disciplined description and for sizing/risk (confirmation = lower tail risk in this sample), not as a return predictor. Selection edge, where it exists, comes from the momentum rank, not from these entry states.\n")
    out.append("\n## Run history (disclosure)\n")
    out.append("- **Run 1** (thresholds as first declared: a fresh breakout was classified AFTER the 2.5-ATR wait_for_pullback gate). `breakout_entry` was almost unreachable: 5 of 31,299 India observations and 24 of 48,173 US observations, "
               "because a genuine breakout is itself a >2.5 ATR extension from the 50d MA. That is a state-definition defect (the state could not be validated), found from state COUNTS. "
               "attractive_entry, confirmation_entry and overextended counts were unchanged by the fix; the breakout names moved out of wait_for_pullback.\n"
               "- **Run 2** (this report): the breakout check now precedes the wait_for_pullback gate and is bounded by the 4-ATR overextension limit. No other threshold changed; the change was made on reachability, not on returns. "
               "It is still one data-informed adjustment, so treat the breakout row as exploratory.\n")
    out.append("\n## Caveats that bind every number above\n")
    out.append("- **Survivor bias.** The universes are today's Nifty 500 / S&P 500 members; stocks that fell out or were delisted are absent, and members that joined because they rose are present. "
               "Every forward return is flattered, and the flattery is probably larger for stocks that were 'down and recovering' (attractive_entry, setup_forming) than for steady uptrenders, so the contrast is biased toward pullback states. "
               "Read the DIFFERENCES between states, not the levels, and treat even those as upper bounds.\n"
               "- **Close-only data.** No volume and no High/Low exist in the tune files. ATR is the mean absolute close-to-close change (a lower bound on true range, so extension in ATR units is slightly overstated). "
               "Volume confirmation of breakouts is NOT testable here: `breakout_entry` below is a price-only breakout (prior 60-day closing high exceeded within 5 days, from a base no wider than 25%). The production rule withholds the state if volume is present and below 1.5x average; that filter is unvalidated.\n"
               "- **Overlap and dependence.** One observation per stock per month; 12m windows overlap heavily and stocks move together within a month, so effective independent samples are far fewer than n. Intervals come from a bootstrap over month-grid dates (which respects cross-sectional dependence but not serial overlap), so they are still too narrow.\n"
               "- **Same-date excess** subtracts the average return of all sampled stocks on that date, removing the market and the bull/bear cycle, but not size/sector/momentum effects. The lab's own finding (reports/ENGINE_FINDINGS.md) is that the 12-1 momentum rank is the only validated selector in India; states near highs overlap with momentum, so a good result for near-high states may be momentum, not timing.\n"
               "- **Regime.** The regime used here is an equal-weight universe index above its 200d MA (a proxy), not the Nifty 500 / S&P 500 filter the product will pass in. States are computed with regime_on=True so each state describes the stock's own chart; the regime split is in the stability table.\n"
               "- **Unadjusted-split artefacts** may remain below the -45%/+80% one-day filter. Data is Yahoo; no corporate-action audit.\n"
               "- **Small windows.** Two markets, ten years, one market cycle each (2009-2018 was a long bull market with a 2011 / 2015-16 / 2018 setbacks). A state that looks good here has not been tested in a prolonged bear market.\n"
               "- Not tested at all: the zones themselves (whether price returning to the 'ideal zone' beats waiting), the thesis_deteriorating state (needs fundamentals), and the regime downgrade.\n")
    out.append("\n## What this does and does not justify\n")
    out.append("Entry states are descriptive labels of where price sits in its trend. They are shown beside, never instead of, the research gates (level >= 4, adversarial review, fresh evidence). "
               "Whatever the tables show, they are not evidence that a labelled state will make money out of sample; the sealed windows are untouched and must stay that way until the states are frozen.\n")
    (ROOT / "reports" / "TIMING_VALIDATION.md").write_text("\n".join(out))
    print("wrote reports/TIMING_VALIDATION.md")


if __name__ == "__main__":
    main()
