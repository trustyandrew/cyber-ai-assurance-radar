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

1. **Daily dashboard** — static site in `dashboard/` (`index.html`).
2. **Daily Markdown brief** — `data/daily/YYYY-MM-DD.md`.
3. **Weekly newsletter** — copy/paste-ready `data/weekly/` (`.md`, `.html`, LinkedIn).

## Quick start

```bash
pip install -r requirements.txt          # PyYAML, tzdata

python src/run.py daily                   # fetch → score → enrich → render → validate
python src/run.py weekly                  # build the weekly newsletter

# open the dashboard
start dashboard/index.html                # Windows  (or just open the file)
```

### Optional: smarter summaries

The pipeline is **hybrid and LLM-optional**. Without a key it runs fully
deterministically (keyword/rubric scoring + template summaries). Set an Anthropic
API key to enrich the top items with assurance-framed analysis:

```bash
export ANTHROPIC_API_KEY=sk-...           # Windows: setx ANTHROPIC_API_KEY sk-...
export RADAR_MODEL=claude-sonnet-4-6      # optional (default)
python src/run.py daily
```

## How it works

| Stage | Script | Does |
|-------|--------|------|
| 1 | `fetch_sources.py` | Reads `sources.yaml`, fetches RSS/Atom, records `source_health.json` |
| 2 | `normalise_items.py` | Canonical item schema, dedup within run |
| 3 | `score_items.py` | Rubric scoring 1–5, lens, tags, newsletter flag, new-vs-seen |
| 4 | `summarise_items.py` | LLM enrichment if key present, else deterministic |
| 5 | `render_dashboard.py` | `dashboard.json`, daily brief, history snapshot, `dashboard-data.js` |
| — | `render_newsletter.py` | Weekly curation → newsletter outputs |
| — | `validate_outputs.py` | URLs present, no dupes, no empty titles, word limit |

Scoring is transparent and editable — see `prompts/relevance-rubric.md` (human) and
the term lists at the top of `src/score_items.py` (machine).

## Sources

`sources.yaml` is the single source of truth. Each entry has a `fetch` type
(`rss`/`atom`/`manual`), `tier`, `source_type` and `lens`. Standards bodies
(ISO/IEC, SC 27, SC 42) and several AU regulators publish no usable RSS, so they are
`manual` and surface in **source health** as review prompts. When a source shows
`fail`, fix its URL or switch it to `manual`.

## Automation

`.github/workflows/` runs the daily build (08:00 Melbourne) and weekly newsletter
(Friday 08:00 Melbourne) once the repo is on GitHub. Add `ANTHROPIC_API_KEY` as a
repo secret to enable enrichment. See the DST note in the workflow files.

## Design status

The dashboard styling is **provisional/neutral** pending the design mock-up. The
intended identity (crisp, professional, black/white/lime, no stock cyber imagery)
drops into the CSS variables in `dashboard/styles.css` without structural change.

## Roadmap

- **Phase 1 (done):** sources, fetch, scoring, dashboard JSON, daily brief, validation, manual run.
- **Phase 2:** GitHub Actions schedules, source health, dedup, failure reporting *(workflows included)*.
- **Phase 3:** dashboard filters (basic done), source-family weighting, richer standards radar, trend-by-week, HTML scraping for `manual` sources.
