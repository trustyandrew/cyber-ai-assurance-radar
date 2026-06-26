# Daily radar routine (local Claude Code)

The scheduled local routine that keeps the radar fresh. Same pattern as the
reference-vault refresh: a local Claude Code invocation runs these steps on your
Claude subscription (no paid API), then pushes to the **private** repo.

## What the routine does

Run from the repo root: `C:\Users\AndrewRobinson\source\repos\cyber-ai-assurance-radar`

1. **Research the feedless ("manual") sources.** Some important sources have no usable
   RSS (ISO committees bot-block; several AU bodies have no feed). For these, use web
   search / WebFetch to find genuinely NEW, material assurance developments since the
   last run, and maintain `data/manual_items.json`:
   - Read the existing file (a JSON array).
   - Append items not already present (dedup by URL), each shaped as:
     ```json
     {"title": "", "url": "", "source": "", "source_type": "regulator|government|standard_body",
      "lens": "ASD|SC27|SC42|ISO27000|ISO42000|ResponsibleAI|Regulation|Privacy|CyberResilience|PublicSector",
      "published_date": "YYYY-MM-DD", "summary": "", "found_at": "YYYY-MM-DD"}
     ```
   - Australian English. **Never fabricate** — only add items you can tie to a real URL.
   - Prune entries whose `found_at` is older than 30 days, then save.
   - Be efficient: a focused pass of a few targeted searches; finding nothing is fine.

   **Feedless sources to check:** ISO/IEC SC 27 & SC 42 work programmes (new or changed
   work items / stage moves), ASIC, ACCC, Attorney-General's Department (privacy reform),
   Home Affairs / CISC (critical infrastructure), ENISA, OECD.AI, Standards Australia.
   (OAIC, ACMA, DTA and digital.gov.au are now auto-fetched via RSS — no manual work.)

   **Standards register:** if your research finds an ISO/IEC SC 27 / SC 42 stage change
   (e.g. DIS→FDIS), a new edition, or a framework update (NIST, EU AI Act, ISM, PSPF…),
   edit `standards.yaml` (designation/status). The run then auto-emits a "Standards
   radar" signal card and badges the register row NEW/UPDATED — which you can 👍 into a
   newsletter. Keep `standards.yaml` aligned with the reference vault's tracked frameworks.

2. **Collect + score (deterministic):**
   ```bash
   python src/run.py daily
   ```
   Fetches the RSS sources, **merges `data/manual_items.json`**, scores everything, and
   writes `data/dashboard.json`, `DASHBOARD.md`, the dated brief, a history snapshot, and
   `data/daily/<date>-enrichment-prompt.md`.

3. **Enrich with the LLM (Claude, on the subscription):**
   - Read `data/daily/<date>-enrichment-prompt.md` (task spec + the day's top items as JSON).
   - Write the JSON reply — an array of `{id, score, summary, why_it_matters, suggested_action}` —
     to `data/_cache/enrichment-in.json`. `score` is 1–5 assurance relevance (5 critical … 1 ignore;
     routine stats score low). Australian English, assurance-framed, no fabrication.
   - Apply and re-render:
     ```bash
     python src/apply_enrichment.py
     ```

4. **On Fridays, also build the newsletter:**
   ```bash
   python src/run.py weekly
   ```

5. **Commit + push (private repo):**
   ```bash
   git add -A && git commit -m "Daily radar update <date>" && git push
   ```

## Bookmark

`https://github.com/trustyandrew/cyber-ai-assurance-radar/blob/main/DASHBOARD.md`
(GitHub renders Markdown free on private repos; updates each time the routine pushes.)

## Scheduling

Registered as the built-in scheduled task `daily-assurance-radar` (cron `0 8 * * *`,
fires ~08:10 Australia/Melbourne, or on next app launch if missed). No GitHub Actions,
no API key.
