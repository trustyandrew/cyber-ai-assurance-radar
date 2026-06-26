"""Merge Pro-plan enrichment back into the dashboard (no API billing).

Workflow:
  1. Run `python src/run.py daily` — writes data/daily/<date>-enrichment-prompt.md.
  2. Paste that prompt into Claude Desktop (Pro/Max). Copy its JSON reply.
  3. Save the reply to data/_cache/enrichment-in.json  (a JSON array of
     {id, summary, why_it_matters, suggested_action}).
  4. Run `python src/apply_enrichment.py`.

This updates enriched.json in place and re-renders the dashboard + daily brief.
"""
from __future__ import annotations

import json
import sys

import render_dashboard
from score_items import PRIORITY_BY_SCORE
from radar_common import CACHE, load_json, log, save_json

IN_FILE = CACHE / "enrichment-in.json"
ENRICHED = CACHE / "enriched.json"


def main() -> int:
    if not IN_FILE.exists():
        log(f"Missing {IN_FILE}. Paste Claude's JSON reply there first.")
        return 1
    try:
        incoming = json.loads(IN_FILE.read_text(encoding="utf-8"))
        by_id = {o["id"]: o for o in incoming}
    except Exception as e:  # noqa: BLE001
        log(f"Could not parse {IN_FILE}: {repr(e)[:120]}")
        return 1

    enriched = load_json(ENRICHED, [])
    if not enriched:
        log("No enriched.json — run `python src/run.py daily` first.")
        return 1

    applied = 0
    for it in enriched:
        o = by_id.get(it["id"])
        if not o:
            continue
        it["summary"] = o.get("summary") or it.get("summary", "")
        it["why_it_matters"] = o.get("why_it_matters", it.get("why_it_matters", ""))
        it["suggested_action"] = o.get("suggested_action", it.get("suggested_action", ""))
        # LLM relevance score overrides the deterministic one and drives ranking/priority.
        s = o.get("score")
        if isinstance(s, (int, float)) and 1 <= int(s) <= 5:
            it["relevance_score"] = int(s)
            it["priority"] = PRIORITY_BY_SCORE[int(s)]
            it["newsletter_candidate"] = int(s) >= 4
        it["enriched_by"] = "pro-plan"
        applied += 1

    save_json(ENRICHED, enriched)
    log(f"Applied Pro-plan enrichment to {applied}/{len(enriched)} items; re-rendering…")
    render_dashboard.build()
    log("Done. Reload the dashboard.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
