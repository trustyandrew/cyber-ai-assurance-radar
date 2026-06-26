# Daily radar routine (local Claude Code)

The scheduled local routine that keeps the radar fresh. Same pattern as the
reference-vault refresh: a local Claude Code invocation runs these steps on your
Claude subscription (no paid API), then pushes to the **private** repo.

## What the routine does

Run from the repo root: `C:\Users\AndrewRobinson\source\repos\cyber-ai-assurance-radar`

1. **Collect + score (deterministic):**
   ```bash
   python src/run.py daily
   ```
   Produces `data/dashboard.json`, `DASHBOARD.md`, the dated brief, history snapshot,
   and `data/daily/<date>-enrichment-prompt.md`.

2. **Enrich with the LLM (Claude, on the subscription):**
   - Read `data/daily/<date>-enrichment-prompt.md` (it contains the analyst task spec
     and the day's top items as JSON).
   - Write the JSON reply — an array of `{id, summary, why_it_matters,
     suggested_action}` — to `data/_cache/enrichment-in.json`. Australian English,
     assurance-framed, never fabricate standards or publication facts.
   - Apply and re-render:
     ```bash
     python src/apply_enrichment.py
     ```

3. **On Fridays, also build the newsletter:**
   ```bash
   python src/run.py weekly
   ```

4. **Commit + push (private repo):**
   ```bash
   git add -A && git commit -m "Daily radar update <date>" && git push
   ```

## Bookmark

`https://github.com/trustyandrew/cyber-ai-assurance-radar/blob/main/DASHBOARD.md`
(GitHub renders Markdown free on private repos; updates each time the routine pushes.)

## Scheduling

Wire steps 1–4 into the same local scheduler you use for the reference-vault refresh,
to fire at **08:00 Australia/Melbourne**. The Claude invocation must run in a context
that can do step 2 (i.e. Claude Code, so enrichment uses the subscription).

> No GitHub Actions and no API key are involved. The `RADAR_USE_API` path exists but
> stays off.
