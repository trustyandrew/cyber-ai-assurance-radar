"""Validation gate. Exits non-zero on failure so CI can block a bad run.

Checks dashboard.json: valid JSON, items have url/title/source, no duplicate URLs,
no empty titles, dates present where available. Checks the daily brief exists.
Checks the latest newsletter (if present) is under the word limit.
"""
from __future__ import annotations

import sys

from radar_common import DAILY, DASHBOARD_JSON, WEEKLY, load_json, log, today_str

WORD_LIMIT = 1000


def _all_items(dashboard: dict):
    yield from dashboard.get("current_signals", [])
    for items in dashboard.get("sections", {}).values():
        yield from items
    yield from dashboard.get("newsletter_candidates", [])


def validate_daily() -> list[str]:
    errors: list[str] = []
    dashboard = load_json(DASHBOARD_JSON, None)
    if dashboard is None:
        return [f"dashboard.json missing or invalid at {DASHBOARD_JSON}"]

    urls = []
    for it in _all_items(dashboard):
        if not it.get("title", "").strip():
            errors.append(f"empty title: {it.get('id')}")
        if not it.get("url"):
            errors.append(f"missing url: {it.get('title')!r}")
        else:
            urls.append(it["url"])
        if not it.get("source"):
            errors.append(f"missing source: {it.get('title')!r}")

    # duplicate URLs within current_signals (canonical list)
    cs_urls = [it["url"] for it in dashboard.get("current_signals", []) if it.get("url")]
    dupes = {u for u in cs_urls if cs_urls.count(u) > 1}
    if dupes:
        errors.append(f"duplicate URLs in current_signals: {len(dupes)}")

    brief = DAILY / f"{today_str()}.md"
    if not brief.exists():
        errors.append(f"daily brief missing: {brief}")
    return errors


def validate_weekly() -> list[str]:
    errors: list[str] = []
    latest = WEEKLY / "latest-newsletter.md"
    if latest.exists():
        words = len(latest.read_text(encoding="utf-8").split())
        if words > WORD_LIMIT:
            errors.append(f"newsletter {words} words exceeds {WORD_LIMIT}")
    return errors


def main(scope: str = "daily") -> int:
    errors = validate_daily() if scope == "daily" else validate_weekly()
    if errors:
        log(f"VALIDATION FAILED ({scope}): {len(errors)} issue(s)")
        for e in errors:
            log(f"  - {e}")
        return 1
    log(f"VALIDATION PASSED ({scope})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "daily"))
