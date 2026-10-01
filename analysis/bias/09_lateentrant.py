"""Upper-bound stress for index-membership look-ahead: assume the best-performing X% of names (2010-01 -> 2018-12 total return)
were NOT yet index members (they 'joined later because they rose') and delete them from the universe. Extreme by construction
(selection on the outcome) - a bound, not an estimate. Compare with EW buy&hold on the same reduced universe."""
from common import *
import indep
px, b = load(); pxf = indep.prep(px)
d0 = pxf.loc[START:].index[0]; s0 = pxf.loc[d0]; s1 = pxf.iloc[-1]; tr_ = (s1/s0 - 1).dropna()
tr_ = tr_[pxf.loc[d0].notna()]            # names that exist on day 1 of trading
rank = tr_.sort_values(ascending=False); N = len(rank); print("names with price on 2010-01-01:", N)
rows = []
for frac in (0, .05, .10, .20, .33):
    drop = list(rank.index[:int(N*frac)])
    p = px.drop(columns=drop); eq, tr = indep.sim(indep.prep(p), b)
    e = eq.loc[START:]; e = e/e.iloc[0]; m = met(e); ew = met(bt.buy_hold(p.loc[START:]))
    rows.append(dict(excluded_top_frac=frac, n_dropped=len(drop), strat_CAGR=m["CAGR"], strat_MaxDD=m["MaxDD"], EW_CAGR=ew["CAGR"], EW_MaxDD=ew["MaxDD"]))
R = pd.DataFrame(rows); print(R.round(4).to_string(index=False)); R.to_csv("out_late_entrant.csv", index=False)
