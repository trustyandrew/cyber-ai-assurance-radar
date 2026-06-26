"""Stage 5 — assemble dashboard.json, the daily Markdown brief, the static-page
data file, and a daily history snapshot (used by the weekly newsletter).

Outputs:
  data/dashboard.json
  data/daily/YYYY-MM-DD.md
  data/history/YYYY-MM-DD.json
  dashboard/dashboard-data.js   (window.DASHBOARD_DATA = {...} for file:// use)
"""
from __future__ import annotations

import json

from radar_common import (
    CACHE, DAILY, DASHBOARD, DASHBOARD_JSON, HEALTH_FILE, HISTORY,
    SOURCES_YAML, STANDARDS_YAML,
    load_json, load_yaml, log, now_iso, save_json, today_str,
)

THEME_LABELS = {
    "ASD": "ASD / ACSC cyber assurance expectations",
    "CyberResilience": "cyber resilience under pressure",
    "SC27": "the ISO/IEC 27000 family",
    "ISO27000": "the ISO/IEC 27000 family",
    "SC42": "ISO/IEC 42001 and AI management systems",
    "ISO42000": "ISO/IEC 42001 and AI management systems",
    "ResponsibleAI": "responsible AI governance",
    "PublicSector": "Australian public sector AI assurance",
    "Regulation": "regulatory and operational-resilience change",
    "Privacy": "privacy and data protection",
}

ITEM_FIELDS = [
    "id", "title", "source", "source_type", "published_date", "retrieved_at",
    "url", "priority", "relevance_score", "lens", "summary", "why_it_matters",
    "suggested_action", "newsletter_candidate", "tags", "is_new", "enriched_by",
]

# Dashboard section -> lenses that feed it.
SECTION_LENSES = {
    "asd_acsc": {"ASD", "CyberResilience"},
    "sc27": {"SC27", "ISO27000"},
    "sc42": {"SC42", "ISO42000", "ResponsibleAI"},
    "au_gov_ai": {"PublicSector"},
    "regulatory": {"Regulation", "Privacy"},
}
SECTION_TITLES = {
    "asd_acsc": "ASD / ACSC radar",
    "sc27": "SC 27 / 27000 family radar",
    "sc42": "SC 42 / 42000 & AI assurance radar",
    "au_gov_ai": "Australian Government AI assurance",
    "regulatory": "Regulatory & sector watch",
}


def _clean(item: dict) -> dict:
    return {k: item.get(k) for k in ITEM_FIELDS}


def build() -> dict:
    enriched = load_json(CACHE / "enriched.json", [])
    health = load_json(HEALTH_FILE, {})
    scored = load_json(CACHE / "scored.json", [])

    items = sorted(
        (_clean(it) for it in enriched),
        key=lambda x: (x["relevance_score"], x.get("published_date") or ""),
        reverse=True,
    )

    sections = {key: [] for key in SECTION_LENSES}
    for it in items:
        for key, lenses in SECTION_LENSES.items():
            if it["lens"] in lenses:
                sections[key].append(it)
                break

    current_signals = items[:12]
    newsletter_candidates = [it for it in items if it.get("newsletter_candidate")]
    action_queue = [
        {"item_id": it["id"], "title": it["title"], "url": it["url"],
         "priority": it["priority"], "action": it.get("suggested_action", "")}
        for it in items if it.get("suggested_action")
    ][:10]

    # Curated standards register + source-queue (rendered as tables in the mock-up).
    standards = load_yaml(STANDARDS_YAML) or {}
    source_queue = (load_yaml(SOURCES_YAML) or {}).get("search_strategy", [])
    standards_tracked = len(standards.get("sc27", [])) + len(standards.get("sc42", []))

    # Lead theme = dominant lens among newsletter candidates (fallback: current signals).
    pool = newsletter_candidates or current_signals
    theme = "cyber and responsible AI assurance"
    if pool:
        from collections import Counter
        top_lens = Counter(it.get("lens", "") for it in pool).most_common(1)[0][0]
        theme = THEME_LABELS.get(top_lens, theme)

    counts = {
        "sources_checked": health.get("summary", {}).get("total", 0),
        "sources_ok": health.get("summary", {}).get("ok", 0),
        "sources_failed": health.get("summary", {}).get("fail", 0),
        "sources_manual": health.get("summary", {}).get("manual", 0),
        "items_scored": len(scored),
        "items_material": len(items),
        "items_new": sum(1 for it in items if it.get("is_new")),
        "items_ignored": sum(1 for it in scored if it.get("relevance_score", 0) <= 1),
        "newsletter_candidates": len(newsletter_candidates),
        "standards_tracked": standards_tracked,
    }

    dashboard = {
        "generated_at": now_iso(),
        "generated_date": today_str(),
        "timezone": "Australia/Melbourne",
        "run_type": "daily",
        "counts": counts,
        "current_signals": current_signals,
        "sections": sections,
        "section_titles": SECTION_TITLES,
        "standards": standards,
        "source_queue": source_queue,
        "newsletter_theme": theme,
        "action_queue": action_queue,
        "newsletter_candidates": newsletter_candidates,
        "source_health": health,
    }

    save_json(DASHBOARD_JSON, dashboard)
    save_json(HISTORY / f"{today_str()}.json", items)
    _write_data_js(dashboard)
    _write_daily_md(dashboard)
    log(f"Dashboard built: {counts['items_material']} material items, "
        f"{counts['items_new']} new")
    return dashboard


def _write_data_js(dashboard: dict) -> None:
    DASHBOARD.mkdir(parents=True, exist_ok=True)
    js = "window.DASHBOARD_DATA = " + json.dumps(dashboard, ensure_ascii=False, indent=2) + ";\n"
    (DASHBOARD / "dashboard-data.js").write_text(js, encoding="utf-8")


def _md_item(it: dict) -> str:
    bits = [f"- **[{it['title']}]({it['url']})** "
            f"— {it['source']} · {it.get('published_date') or 'n/d'} "
            f"· {it['priority']} ({it['relevance_score']}/5)"]
    if it.get("summary"):
        bits.append(f"  {it['summary']}")
    if it.get("why_it_matters"):
        bits.append(f"  *Why it matters:* {it['why_it_matters']}")
    if it.get("suggested_action"):
        bits.append(f"  *Action:* {it['suggested_action']}")
    return "\n".join(bits)


def _write_daily_md(dashboard: dict) -> None:
    c = dashboard["counts"]
    lines = [
        f"# Cyber & Responsible AI Assurance Radar — {dashboard['generated_date']}",
        "",
        f"_Generated {dashboard['generated_at']} ({dashboard['timezone']})._",
        "",
        f"**{c['items_material']}** material items · **{c['items_new']}** new · "
        f"**{c['newsletter_candidates']}** newsletter candidates · "
        f"sources {c['sources_ok']}/{c['sources_checked']} ok "
        f"({c['sources_failed']} failed, {c['sources_manual']} manual).",
        "",
        "## Current signals",
        "",
    ]
    if dashboard["current_signals"]:
        lines += [_md_item(it) for it in dashboard["current_signals"]]
    else:
        lines.append("_No material signals this run._")

    for key, items in dashboard["sections"].items():
        lines += ["", f"## {SECTION_TITLES[key]}", ""]
        lines += [_md_item(it) for it in items] if items else ["_No items._"]

    if dashboard["action_queue"]:
        lines += ["", "## Action queue", ""]
        lines += [f"- [{a['priority']}] {a['action']} — [{a['title']}]({a['url']})"
                  for a in dashboard["action_queue"]]

    lines += ["", "## Source health", ""]
    for s in dashboard["source_health"].get("sources", []):
        lines.append(f"- {s['status'].upper()} — {s['name']}: {s['detail']}")

    (DAILY / f"{dashboard['generated_date']}.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
