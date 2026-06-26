# Cyber & Responsible AI Assurance Radar

A lightweight, repo-based intelligence product that tracks, prioritises and
summarises developments relevant to **cyber security assurance**, the **ISO/IEC
27000** and **42000** families (SC 27 / SC 42), **ASD/ACSC** guidance (ISM,
Essential Eight), **Australian public sector** cyber and AI assurance, and
**responsible AI governance**.

It is an *assurance intelligence product, not a news aggregator*: every item is
scored 1–5 against an explicit rubric, primary sources are prioritised, and
vendor/marketing noise is filtered out.

## Outputs

1. **`DASHBOARD.md`** — the stable, bookmarkable rendered view (works on a private GitHub repo).
2. **Daily dashboard** — static HTML in `dashboard/` (`index.html`), for local viewing.
3. **Daily Markdown brief** — `data/daily/YYYY-MM-DD.md` (dated archive).
4. **Weekly newsletter** — copy/paste-ready `data/weekly/` (`.md`, `.html`, LinkedIn).

## Quick start

```bash
pip install -r requirements.txt          # PyYAML, tzdata

python src/run.py daily                   # fetch → score → enrich → render → validate
python src/run.py weekly                  # build the weekly newsletter

# open the dashboard
start dashboard/index.html                # Windows  (or just open the file)
```

### Smarter summaries — without paid API billing

The daily run is **deterministic and free** by default. For richer, assurance-framed
analysis using a **Claude Pro/Max subscription** (no per-token API charge):

1. `python src/run.py daily` → writes `data/daily/<date>-enrichment-prompt.md`.
2. Paste that prompt into **Claude Desktop** (Pro/Max). Copy its JSON reply.
3. Save the reply to `data/_cache/enrichment-in.json`.
4. `python src/apply_enrichment.py` → merges it in and re-renders.

> Paid API path (off by default, billed separately from a subscription): set
> `RADAR_USE_API=1` **and** `ANTHROPIC_API_KEY`. Only then does the pipeline call the API.

## How it works

| Stage | Script | Does |
|-------|--------|------|
| 1 | `fetch_sources.py` | Reads `sources.yaml`, fetches RSS/Atom, records `source_health.json` |
| 2 | `normalise_items.py` | Canonical item schema, dedup within run |
| 3 | `score_items.py` | Rubric scoring 1–5, lens, tags, newsletter flag, new-vs-seen |
| 4 | `summarise_items.py` | LLM enrichment if key present, else deterministic |
| 5 | `render_dashboard.py` | `dashboard.json`, daily brief, history snapshot, `dashboard-data.js` |
| — | `render_newsletter.py` | Weekly curation → newsletter outputs |
| — | `apply_enrichment.py` | Merge a Pro-plan JSON reply back into the dashboard |
| — | `validate_outputs.py` | URLs present, no dupes, no empty titles, word limit |

The SC 27 / SC 42 sections are a **curated standards register** (`standards.yaml`),
deliberately separate from the live news signals so the dashboard stays a
standards-led radar rather than a news dump.

Scoring is transparent and editable — see `prompts/relevance-rubric.md` (human) and
the term lists at the top of `src/score_items.py` (machine).

## Sources

`sources.yaml` is the single source of truth. Each entry has a `fetch` type
(`rss`/`atom`/`manual`), `tier`, `source_type` and `lens`. Standards bodies
(ISO/IEC, SC 27, SC 42) and several AU regulators publish no usable RSS, so they are
`manual` and surface in **source health** as review prompts. When a source shows
`fail`, fix its URL or switch it to `manual`.

## Automation & hosting (private, free)

This runs from a **local Claude Code routine** (the same pattern used to refresh the
reference vault) — no GitHub Actions, no paid API:

1. Routine runs `python src/run.py daily` (fetch → score → render).
2. Claude — on your subscription — writes assurance-framed summaries to
   `data/_cache/enrichment-in.json` and runs `python src/apply_enrichment.py`.
3. Routine commits and pushes to the **private** repo.

**Bookmark (free on a private repo):** GitHub renders Markdown, so the stable view is
[`DASHBOARD.md`](DASHBOARD.md):

```
https://github.com/trustyandrew/cyber-ai-assurance-radar/blob/main/DASHBOARD.md
```

The rich HTML dashboard (`dashboard/index.html`) stays for local viewing. GitHub Pages
is not used — free Pages requires a public repo.

## Design

The dashboard is built to the approved mock-up: crisp, standards-led, black/white/lime,
no stock cyber imagery. Sidebar navigation, hero + KPI tiles, signal cards, SC 27 / SC 42
register tables, source queue, source health and newsletter callouts. Theme tokens live
in `dashboard/styles.css`.

> **Standards register.** `standards.yaml` is a manually maintained watch-list, verified
> against iso.org / IEC on 2026-06-26. ISO stages move quickly — re-check DIS/FDIS/CD/AWI
> items before external publication. The pipeline renders this register; it does not
> assert publication facts of its own.

## Roadmap

- **Phase 1 (done):** sources, fetch, scoring, dashboard JSON, daily brief, validation, manual run.
- **Phase 2:** GitHub Actions schedules, source health, dedup, failure reporting *(workflows included)*.
- **Phase 3:** dashboard filters (basic done), source-family weighting, richer standards radar, trend-by-week, HTML scraping for `manual` sources.
