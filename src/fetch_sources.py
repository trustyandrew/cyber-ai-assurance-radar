"""Stage 1 — fetch configured sources.

Reads sources.yaml, fetches RSS/Atom feeds, records source health. HTML / search
/ manual source types are recorded but not auto-parsed in the MVP (they show up in
source_health.json so they can be refined over time).

Output: data/_cache/fetched.json  +  data/source_health.json
"""
from __future__ import annotations

import xml.etree.ElementTree as ET

from radar_common import (
    CACHE,
    HEALTH_FILE,
    SOURCES_YAML,
    http_get,
    load_yaml,
    log,
    now_iso,
    parse_date,
    save_json,
    strip_html,
    truncate,
)


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _first_text(elem, names) -> str:
    for child in elem:
        if _local(child.tag) in names and child.text:
            return child.text.strip()
    return ""


def _link(elem) -> str:
    # Atom: <link href="..."/>, prefer rel=alternate. RSS: <link>text</link>.
    atom_alt = ""
    atom_any = ""
    for child in elem:
        if _local(child.tag) == "link":
            href = child.attrib.get("href")
            if href:
                if child.attrib.get("rel", "alternate") == "alternate":
                    atom_alt = atom_alt or href
                atom_any = atom_any or href
            elif child.text:
                return child.text.strip()
    return atom_alt or atom_any


def parse_feed(raw: bytes) -> list[dict]:
    """Parse RSS or Atom bytes into a list of entry dicts."""
    root = ET.fromstring(raw)
    entries = []
    item_tags = {"item", "entry"}
    for el in root.iter():
        if _local(el.tag) not in item_tags:
            continue
        title = _first_text(el, {"title"})
        url = _link(el)
        published = _first_text(el, {"pubdate", "published", "date", "updated"})
        summary = _first_text(el, {"description", "summary", "content", "encoded"})
        if not (title and url):
            continue
        entries.append(
            {
                "title": strip_html(title),
                "url": url.strip(),
                "published_raw": published,
                "published_date": parse_date(published),
                "summary": truncate(strip_html(summary), 400),
            }
        )
    return entries


def fetch_all() -> dict:
    config = load_yaml(SOURCES_YAML) or {}
    sources = config.get("sources", [])
    fetched = []
    health = {"checked_at": now_iso(), "sources": []}

    for src in sources:
        if not src.get("enabled", True):
            continue
        sid = src["id"]
        stype = src.get("fetch", "rss").lower()
        entry = {
            "id": sid,
            "name": src["name"],
            "tier": src.get("tier", 2),
            "source_type": src.get("source_type", "media"),
            "lens": src.get("lens", "CyberResilience"),
        }

        if stype not in ("rss", "atom"):
            health["sources"].append(
                {**entry, "status": "research", "items": 0,
                 "detail": "no feed — covered by the daily routine's web research"}
            )
            continue

        url = src.get("url", "")
        try:
            raw = http_get(url)
            items = parse_feed(raw)
            fetched.append({**entry, "url": url, "entries": items})
            health["sources"].append(
                {**entry, "status": "ok", "detail": f"{len(items)} items", "items": len(items)}
            )
            log(f"OK   {sid}: {len(items)} items")
        except Exception as e:  # noqa: BLE001 - record every failure mode
            health["sources"].append(
                {**entry, "status": "fail", "detail": repr(e)[:140], "items": 0}
            )
            log(f"FAIL {sid}: {repr(e)[:80]}")

    ok = sum(1 for s in health["sources"] if s["status"] == "ok")
    fail = sum(1 for s in health["sources"] if s["status"] == "fail")
    research = sum(1 for s in health["sources"] if s["status"] == "research")
    health["summary"] = {"ok": ok, "fail": fail, "research": research, "total": len(health["sources"])}

    save_json(CACHE / "fetched.json", fetched)
    save_json(HEALTH_FILE, health)
    log(f"Fetched {sum(len(f['entries']) for f in fetched)} raw items "
        f"({ok} ok, {fail} fail, {research} research)")
    return {"fetched": fetched, "health": health}


if __name__ == "__main__":
    fetch_all()
