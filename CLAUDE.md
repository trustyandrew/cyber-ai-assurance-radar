# CLAUDE.md — Cyber & Responsible AI Assurance Radar

Repo-specific guidance for Claude Code. Andrew's global instructions still apply.

## What this is

An assurance **intelligence product**, not a news feed. The bar for including an
item is practical relevance to cyber/AI assurance, audit, certification, standards,
public sector, critical infrastructure, privacy, control design or responsible AI.
Do not include something just because it mentions "AI" or "cyber".

## Architecture

Python pipeline (stdlib + PyYAML only): `fetch → normalise → score → render →
validate`, orchestrated by `src/run.py`. **Never add paid-API calls to the default
path** — Andrew uses a Claude subscription, not pay-per-token API.

Orchestration is a **local Claude Code routine** (like the reference-vault refresh),
NOT GitHub Actions. The routine: (1) `python src/run.py daily`; (2) Claude — on the
subscription — writes assurance-framed enrichment to `data/_cache/enrichment-in.json`
(the task spec is in `src/summarise_items.py` SYSTEM/INSTRUCTION) and runs
`python src/apply_enrichment.py`; (3) commit + push to the **private** repo.

Hosting: repo is **private**, so no GitHub Pages (free Pages needs public). The
bookmarkable view is `DASHBOARD.md` (GitHub renders Markdown free on private repos).
The `RADAR_USE_API=1` + `ANTHROPIC_API_KEY` paid path still exists but is off and
unused. There are no GitHub Actions workflows.

SC 27 / SC 42 are a curated standards register (`standards.yaml`), separate from the
live signals — keep "news" and "standards radar" distinct.

## Run / verify

```bash
python src/run.py daily      # full daily pipeline (exits non-zero on validation fail)
python src/run.py weekly     # weekly newsletter
```

## Hard rules

- **Never fabricate facts, standard numbers, editions, stages or publication
  claims.** Every factual item must carry a real source URL.
- Keep **summary** (what happened), **why_it_matters** (interpretation) and
  **suggested_action** (what to do) distinct.
- Australian English. Precise on GRC standards (ISO/IEC 27001, 42001, SC 27, SC 42,
  ISM, Essential Eight). Independent, concise, not alarmist, not hype.
- Prefer primary sources over commentary.
- Newsletter stays under 1,000 words and curates — never dumps all items.

## Where things live

- `sources.yaml` — all sources (single source of truth).
- `prompts/` — relevance rubric, daily prompt, newsletter style guide.
- `src/score_items.py` — machine-readable scoring term lists (mirror of the rubric).
- `data/dashboard.json` — canonical daily output; `dashboard/dashboard-data.js` is
  the same data wrapped for the static page.
- `data/history/` — per-day snapshots the weekly newsletter reads.

## Open item

`standards.yaml` was seeded from the mock-up and is a manually maintained register.
Editions/stages are **not independently verified** — confirm at iso.org before relying
on any status. The pipeline renders this register; it must not assert publication facts.
