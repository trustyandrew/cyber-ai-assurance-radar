"""Stage 2 — normalise fetched entries into canonical items.

Output: data/_cache/normalised.json (list of items, deduped by id within the run).
"""
from __future__ import annotations

from radar_common import CACHE, load_json, log, now_iso, save_json, stable_id, truncate


def normalise() -> list[dict]:
    fetched = load_json(CACHE / "fetched.json", [])
    retrieved_at = now_iso()
    items: dict[str, dict] = {}

    for src in fetched:
        for e in src.get("entries", []):
            url = e.get("url", "").strip()
            title = e.get("title", "").strip()
            if not (url and title):
                continue
            iid = stable_id(url, title)
            if iid in items:
                continue
            items[iid] = {
                "id": iid,
                "title": title,
                "source": src["name"],
                "source_type": src.get("source_type", "media"),
                "tier": src.get("tier", 2),
                "published_date": e.get("published_date", ""),
                "retrieved_at": retrieved_at,
                "url": url,
                "lens": src.get("lens", "CyberResilience"),
                "summary": truncate(e.get("summary", ""), 400),
                "tags": [],
            }

    out = list(items.values())
    save_json(CACHE / "normalised.json", out)
    log(f"Normalised {len(out)} unique items")
    return out


if __name__ == "__main__":
    normalise()
