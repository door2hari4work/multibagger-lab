"""Portfolio weights as % of total net worth (from the investor brief). WEIGHTS ONLY: no amounts, cost, units or P&L.
PRIVACY: these are personal weights. The repo is PUBLIC (docs/PRODUCT_SPEC.md); decide before any commit whether this file
should be gitignored. Nothing here has been committed or pushed."""
# sleeve tags: 'semi' (semiconductors), 'mega' (mega-cap tech/platform), 'emp' (employer), 'rest' (other US equity),
#              'ndx' (Nasdaq-100 fund), 'in50' 'next50' 'mid' 'flexi' 'infra' 'digital' (India funds), 'gold'
HOLDINGS = [
    # name,                 weight, tag,    region, usd_linked
    ("MSFT",                 6.8,  "mega",  "US", True),
    ("GOOGL",                5.4,  "mega",  "US", True),
    ("TSM",                  3.2,  "semi",  "US", True),
    ("AMZN",                 3.2,  "mega",  "US", True),
    ("NVDA",                 2.6,  "semi",  "US", True),
    ("MU",                   2.4,  "semi",  "US", True),
    ("META",                 1.4,  "mega",  "US", True),
    ("APH",                  1.1,  "rest",  "US", True),
    ("BNY (employer ESOP)",  5.8,  "emp",   "US", True),
    ("MO Nifty 50 Idx",     16.6,  "in50",  "IN", False),
    ("ICICI Nasdaq-100 Idx",15.8,  "ndx",   "US", True),
    ("MO Midcap 150 Idx",    9.5,  "mid",   "IN", False),
    ("PPFAS Flexi Cap",      7.8,  "flexi", "IN", False),
    ("Navi Nifty 50 Idx",    5.4,  "in50",  "IN", False),
    ("Mirae Infra",          5.1,  "infra", "IN", False),
    ("HDFC Nifty Next 50",   4.0,  "next50","IN", False),
    ("Axis Gold&Silver FoF", 2.0,  "gold",  "IN", True),   # gold priced in INR -> moves with USD/INR
    ("Tata Digital India",   0.8,  "digital","IN", False),
]
UNALLOCATED = round(100 - sum(h[1] for h in HOLDINGS), 2)   # 1.1 -> treated as cash/other, zero shock (assumption)
