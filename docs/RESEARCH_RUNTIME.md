# Research runtime

How the research agents run, what they read and write, how to schedule them, and what limits to expect. Product rules live in `docs/PRODUCT_SPEC.md`; the thesis object in `mblab/schema.py`.

## Design in one paragraph
There is no model API key and no always-on server. Each research agent is a scheduled Claude Code session that starts from a clean checkout, reads `research/PLAYBOOK.md`, picks work from `research/queue.json`, researches with web access, builds a `Thesis` through `mblab/thesis_builder.py`, which validates it, saves it with `mblab.store.save_new_version`, appends to `research/log.md`, and pushes a branch for the owner to review. Everything that can be done without an LLM (queue building, level-1 snapshots, staleness, change detection, validation) is plain Python with tests; the LLM only does reading, judging and writing evidence.

## Files
| Path | Purpose |
|---|---|
| `research/PLAYBOOK.md` | the procedure every session follows |
| `research/prompts/*.md` | one self-contained prompt per role: `level2_qualifier`, `level3_deep_dive`, `devils_advocate`, `source_reliability`, `monitoring_agent`, `weekly_digest`, `ai_value_chain_mapper` (`_common_rules.md` is the shared block inlined into each) |
| `research/queue.py`, `research/queue.json` | builds/prioritises tasks from `research/candidates_*.json` (owned by the discovery agent); tasks: pending, in_progress, done, blocked, failed |
| `research/log.md` | append-only log, one entry per task attempt (including failures and blocked sources) |
| `research/monitoring/`, `research/digests/`, `research/themes/` | outputs of monitoring, weekly digest and the AI value-chain mapper (created by the sessions) |
| `mblab/thesis_builder.py` | level-1 snapshot from a candidate row (no LLM); `assemble_deep_thesis`, `apply_adversarial`, `save_payload`; CLI `python -m mblab.thesis_builder snapshot|assemble` |
| `mblab/freshness.py` | staleness classes (fresh/aging/stale/unknown) for evidence and prices; `what_changed_since(thesis, current)`; CLI `python -m mblab.freshness` |

## Queue rules (research/queue.py)
- Source: every `research/candidates_*.json` (list of rows, or an object with `candidates`/`rows`/`results`). Order within a file: `rank` ascending, else score descending, else file order. Priority is 100 at the top of a file, falling linearly.
- Per name, the next step is decided from its latest thesis: none or level 1 => `level2_qualifier`; level 2 => `level3_deep_dive`; level >= 3 without adversarial review => `devils_advocate`; finished and fresh (created within 30 days and `next_review` not passed) => skipped; finished and stale => `level3_deep_dive` refresh; rejected / thesis_broken / exit => skipped.
- At most `--cap` (default 5) new tasks per build; no duplicate open task; 3-day cooldown after a done/blocked/failed attempt; `in_progress` tasks older than 2 days are re-opened.

## Suggested routines
Routines run from cron in UTC unless prefixed with `CRON_TZ=`; the minimum interval is hourly and minutes are deliberately off the hour (shared schedulers are busiest at :00 and :30). Times below are IST for an owner in India; adjust as needed. Create each as a routine that starts a **fresh session per firing** in this repo's environment (each run then begins from a clean checkout and stays independent of earlier context), with the prompt shown.

| Routine | Cron | Prompt to the session |
|---|---|---|
| Daily discovery queue | `CRON_TZ=Asia/Kolkata 43 7 * * 1-5` | "Follow research/PLAYBOOK.md, section 8 'Discovery queue'. Build the queue from candidates_*.json, commit and push research/queue.json on branch research/<today>." |
| Deep research, 3x weekly | `CRON_TZ=Asia/Kolkata 12 9 * * 1,3,5` | "Follow research/PLAYBOOK.md. Take the top tasks of type level3_deep_dive and devils_advocate (then level2_qualifier if time remains), within the per-session caps." |
| Level-2 qualification (optional, daily) | `CRON_TZ=Asia/Kolkata 27 11 * * 2,4` | "Follow research/PLAYBOOK.md. Take up to 3 level2_qualifier tasks." |
| Daily monitoring | `CRON_TZ=Asia/Kolkata 7 18 * * 1-5` | "Follow research/PLAYBOOK.md section 8 'Monitoring' with research/prompts/monitoring_agent.md." Optionally add a second run around 07:50 IST for the US close. |
| Weekly digest | `CRON_TZ=Asia/Kolkata 11 8 * * 0` | "Follow research/PLAYBOOK.md section 8 'Weekly digest'; write research/digests/<today>.md." |
| AI value-chain map (optional, weekly or monthly) | `CRON_TZ=Asia/Kolkata 21 10 * * 6` | "Follow research/PLAYBOOK.md section 8 'AI value chain'." |

Start with discovery + one deep-research routine + monitoring + digest; add the rest once the log shows the sessions finish inside their budget.

## Limits and what to expect
- **Session time and context.** A session has a finite time and context budget. A real Level-3 deep dive (several filings and two transcripts) can consume most of one; hence the per-session caps (1 deep dive, 3 qualifiers). A session that runs out marks the task `blocked` with a note and pushes what validated. Prefer a missed task over a thin one.
- **Network.** Outbound traffic goes through the environment's proxy and may be restricted to an allowlist. Check the environment's network settings and test the sources a routine needs: `sec.gov` (EDGAR; needs a User-Agent with a contact email, read from the environment secret `SEC_CONTACT`), `bseindia.com`, `nseindia.com` (known to block automated clients intermittently), company IR sites. If a host is blocked, the session must say so in the log and not substitute memory (see PLAYBOOK section 6). Add allowed hosts in the environment rather than letting sessions improvise around the proxy.
- **No connectors in routines.** Treat routines as having no brokerage, portfolio or other connector access: no IndMoney/Zerodha, no Drive. That is by design: research sessions never see holdings (`private/` is gitignored and must not be read) and never trade. Portfolio-fit (Level 5) is a separate local step. If a routine is created with connectors, they are not needed and should be removed.
- **Persistence.** The container is discarded after a run. Work survives only if committed and pushed, which is why the PLAYBOOK ends with pushing a `research/<date>` branch (never `main`). Review and merge those branches; unmerged branches do not feed the next run's queue, so merge daily or run the queue build and research on the same branch lineage.
- **Secrets.** `SEC_CONTACT` is set as an environment secret, never committed or echoed. No API keys exist or are needed.
- **Repo visibility.** The repo is currently public (see the product spec): theses and logs pushed to it are public. Make it private before real research accumulates.
- **Cost and rate.** Each firing consumes plan usage. Keep the cadence above rather than hourly polling; monitoring is once a day because filings arrive at that rhythm.
- **Honest failure.** A run that could not reach its sources is a valid run if it says so. `research/log.md` and the weekly digest's "Research health" section surface blocked tasks, stale theses and anything that looks wrong, so silent data failure shows up.

## Local use
All of it also works by hand from the repo root: `python research/queue.py build`, `python research/queue.py next`, `python -m mblab.thesis_builder snapshot row.json`, `python -m pytest tests/test_research_runtime.py`. No network is needed for the tests.
