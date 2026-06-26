"""Pipeline orchestrator.

Usage:
    python src/run.py daily     # fetch -> normalise -> score -> enrich -> render -> validate
    python src/run.py weekly    # build the weekly newsletter -> validate

Run from the repository root.
"""
from __future__ import annotations

import sys

import fetch_sources
import normalise_items
import score_items
import summarise_items
import render_dashboard
import render_newsletter
import validate_outputs
from radar_common import CACHE, SEEN_FILE, ensure_dirs, load_json, log, now_iso, save_json


def _update_seen(dashboard: dict) -> None:
    seen = load_json(SEEN_FILE, {})
    ts = now_iso()
    items = list(dashboard.get("current_signals", []))
    for sec in dashboard.get("sections", {}).values():
        items += sec
    for it in items:
        rec = seen.get(it["id"], {"first_seen": ts})
        rec.update({"last_seen": ts, "title": it["title"], "url": it["url"]})
        seen[it["id"]] = rec
    save_json(SEEN_FILE, seen)
    log(f"seen_items.json now tracks {len(seen)} items")


def run_daily() -> int:
    ensure_dirs()
    log("=== DAILY RUN START ===")
    fetch_sources.fetch_all()
    normalise_items.normalise()
    score_items.score_all()
    summarise_items.enrich()
    dashboard = render_dashboard.build()
    _update_seen(dashboard)
    rc = validate_outputs.main("daily")
    log("=== DAILY RUN DONE ===")
    return rc


def run_weekly() -> int:
    ensure_dirs()
    log("=== WEEKLY RUN START ===")
    render_newsletter.build()
    rc = validate_outputs.main("weekly")
    log("=== WEEKLY RUN DONE ===")
    return rc


if __name__ == "__main__":
    scope = sys.argv[1] if len(sys.argv) > 1 else "daily"
    if scope == "daily":
        sys.exit(run_daily())
    elif scope == "weekly":
        sys.exit(run_weekly())
    else:
        print("usage: python src/run.py [daily|weekly]")
        sys.exit(2)
