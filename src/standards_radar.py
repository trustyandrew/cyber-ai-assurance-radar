"""Detect changes to the standards / frameworks register and surface them.

Compares standards.yaml against data/standards_seen.json:
  * a NEW entry or a STATUS change becomes a signal item (written to
    data/_cache/standards_changes.json, merged by normalise_items -> scored, enriched,
    rendered as a 👍-able card), and
  * the entry is flagged change=new|updated with changed_at, so the register tables can
    badge it NEW / UPDATED for a window.

First run (empty snapshot) seeds the baseline silently — only later changes signal.
"""
from __future__ import annotations

from radar_common import (
    CACHE, DATA, STANDARDS_YAML, load_json, load_yaml, log, save_json, stable_id, today_str,
)

STANDARDS_SEEN = DATA / "standards_seen.json"
GROUP_LENS = {"sc27": "SC27", "sc42": "SC42"}  # frameworks carry their own `lens`


def _entries() -> list[dict]:
    reg = load_yaml(STANDARDS_YAML) or {}
    out = []
    for group, items in reg.items():
        if not isinstance(items, list):
            continue
        for e in items:
            out.append({**e, "group": group,
                        "lens": e.get("lens") or GROUP_LENS.get(group, "SC27")})
    return out


def detect() -> list[dict]:
    entries = _entries()
    seen = load_json(STANDARDS_SEEN, {})
    first_run = not seen
    today = today_str()
    changes, new_seen = [], {}

    for e in entries:
        desig, status = e["designation"], e.get("status", "")
        prev = seen.get(desig)
        if first_run:
            new_seen[desig] = {"status": status, "changed_at": None, "change": ""}
            continue
        if prev is None:
            change, changed_at = "new", today
        elif prev.get("status") != status:
            change, changed_at = "updated", today
        else:
            change, changed_at = prev.get("change", ""), prev.get("changed_at")
        new_seen[desig] = {"status": status, "changed_at": changed_at, "change": change}
        if change in ("new", "updated") and changed_at == today:
            verb = "added to the radar" if change == "new" else f"now {status}"
            changes.append({
                "id": stable_id(f"std|{desig}|{status}"),
                "title": f"Standards radar: {desig} — {e.get('area', '')} ({verb})",
                "source": "Standards radar",
                "source_type": "standard_body",
                "lens": e["lens"],
                "published_date": today,
                "url": e.get("url", ""),
                "summary": e.get("why", ""),
            })

    save_json(STANDARDS_SEEN, new_seen)
    save_json(CACHE / "standards_changes.json", changes)
    log(f"Standards radar: {'seeded baseline' if first_run else str(len(changes)) + ' change(s)'}")
    return changes


if __name__ == "__main__":
    detect()