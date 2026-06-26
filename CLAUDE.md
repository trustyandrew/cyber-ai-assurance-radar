# CLAUDE.md — Cyber & Responsible AI Assurance Radar

Repo-specific guidance for Claude Code. Andrew's global instructions still apply.

## What this is

An assurance **intelligence product**, not a news feed. The bar for including an
item is practical relevance to cyber/AI assurance, audit, certification, standards,
public sector, critical infrastructure, privacy, control design or responsible AI.
Do not include something just because it mentions "AI" or "cyber".

## Architecture

Hybrid, **LLM-optional** Python pipeline (stdlib + PyYAML only):
`fetch → normalise → score → summarise → render → validate`, orchestrated by
`src/run.py`. Runs deterministically with no API key; enriches the top items via the
Claude API when `ANTHROPIC_API_KEY` is set. Daily and weekly GitHub Actions in
`.github/workflows/`.

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

Dashboard visual identity is **provisional** pending Andrew's design mock-up. Keep
structure stable; retheme via CSS variables in `dashboard/styles.css`.
