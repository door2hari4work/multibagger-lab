# MultibaggerLab product spec v1 (Phase 1)
Decisions confirmed by the owner (2026-10-05): extend this lab (not a new repo); portfolio via IndMoney (read-only) with CSV/Excel upload from Finboom as fallback;
universe = India and US mid + small caps with a liquidity floor (microcaps only by explicit approval, flagged very high risk); research agents run as scheduled Claude sessions.

## One-line purpose
Reduce the hours of research to a few evidence-backed decisions: what is worth my time, why now, what could go wrong, where to enter, what makes me exit, how it fits MY portfolio.
It outputs versioned THESES, never "BUY XYZ". Language is probabilistic; every probability is a labelled model estimate; the user decides; no trade execution.

## Honest basis (from the lab's evidence)
- Price-based selection edge exists but is modest and survivor-inflated; momentum rank is the only validated selector (strong India large/mid, weak US, ~none micro).
- The EBITDA/growth/cash quality gate did NOT help in the one market tested; so fundamentals are used as thesis evidence and risk flags, not as a validated filter.
- Theses cannot be backtested point-in-time (no archive of what was knowable). Validation = forward tracking (paper books, thesis scorecard) + leakage-safe tests of the numeric components only.

## Time horizon
Primary 12-24 months. "Great company" != "great investment at this price" != "great asymmetric opportunity now"; only the third is surfaced prominently.

## Opportunity lifecycle (Status) and entry timing (EntryState): see mblab/schema.py
early_discovery -> research_required -> watchlist -> preparing_to_enter -> attractive_entry -> accumulate -> hold -> trim -> exit | thesis_broken | rejected.
Entry timing is separate and explicit: too_early, setup_forming, attractive_entry, confirmation_entry, breakout_entry, overextended, wait_for_pullback, thesis_deteriorating.
Hard gates (enforced in code by validate()): entry/accumulate requires research level >= 4, a completed adversarial review that did not kill it, explicit exit rules, and a FACT newer than 120 days.

## Pipeline (levels)
L1 Discovery (quant, whole universe, automatic) -> L2 Qualification (business/financial/valuation snapshot) -> L3 Deep dive (primary sources, citations) ->
L4 Adversarial review (devil's advocate may kill/downgrade) -> L5 Portfolio fit -> L6 Timing. Compute budget goes to the top candidates only.

## Opportunity score: decomposable, weights are declared defaults to be validated, never a single opaque number
Components (0..1 each, with basis and data quality): business_quality, growth_acceleration, earnings_inflection, tam_expansion, catalyst_strength, competitive_advantage,
valuation_asymmetry, market_confirmation, timing, risk (inverse), thesis_robustness, portfolio_fit. mblab/scoring.py computes overall from available components,
reweights over missing ones and lowers `confidence` when data is missing. Components that cannot be assessed stay None; they are never guessed.
Multibagger potential, probability, timing, downside and portfolio fit are shown separately (a 20x with tiny probability does not outrank a likelier 5x).

## Entry and exit
Entry zones are rounded ranges with the derivation stated (e.g. 50-day MA band, ATR, base lows), never false precision. Exits are THESIS-based (invalidation, earnings deterioration,
catalyst failure, valuation excess, narrative saturation, technical break when relevant, rotation, target/partial profit); actions: hold / add / trim / exit / emergency thesis review.

## Modules (owner-disjoint; each with tests)
mblab/schema.py, store.py (done) | mblab/data/{universe,prices,fundamentals}.py | mblab/discovery.py | mblab/timing.py | mblab/scoring.py | mblab/monitor.py |
mblab/portfolio.py | mblab/freshness.py | research/ (agent prompts + queue) | ui/today.py (decision-first dashboard).
Scheduled Claude sessions run: discovery (daily), deep research on the queue (several per week), adversarial review, monitoring/alerts (daily), weekly digest.

## Privacy / safety
Holdings live ONLY in private/ (gitignored) and are never committed. The repo is currently PUBLIC: recommend making it private before personal data or real theses accumulate.
No credentials in code; SEC contact email via env var. No trading. Alerts only on material change (de-duplicated, severity-ranked); no spam.

## What success looks like
Home screen answers "what deserves my attention today": high-priority opportunities, changed theses, improved entry setups, triggered exits, new discoveries. Each opportunity page answers
should-I-spend-time, why, what must go right, what could go wrong, why now, price attractiveness, upside/downside, likelihood, entry, exit, portfolio fit, what to watch next.
