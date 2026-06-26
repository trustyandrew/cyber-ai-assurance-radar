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
    ROOT, CACHE, DATA, DAILY, DASHBOARD, DASHBOARD_JSON, FEEDBACK_FILE, HEALTH_FILE,
    HISTORY, SOURCES_YAML, STANDARDS_YAML,
    load_json, load_yaml, log, now_iso, save_json, today_str, vote_of,
)

CTA = ("If your organisation is preparing for ISO/IEC 27001, ISO/IEC 42001, cyber "
       "assurance or responsible AI governance, I can help you separate what matters "
       "from what is noise — and build an evidence-based path forward.")

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
    "suggested_action", "newsletter_candidate", "tags", "is_new", "enriched_by", "vote",
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

    # Apply 👍/👎 feedback: drop dismissed items everywhere; force 👍 as candidates.
    votes = load_json(FEEDBACK_FILE, {})
    items = [it for it in items if vote_of(votes.get(it["id"])) != "down"]
    for it in items:
        it["vote"] = vote_of(votes.get(it["id"]))
        if it["vote"] == "up":
            it["newsletter_candidate"] = True

    sections = {key: [] for key in SECTION_LENSES}
    for it in items:
        for key, lenses in SECTION_LENSES.items():
            if it["lens"] in lenses:
                sections[key].append(it)
                break

    # Diversify current signals — a hard cap per source so one prolific feed (e.g. NCSC,
    # which publishes far more than ASD) can't dominate, even when few sources are active.
    # Items are already score-sorted; take up to `cap` per source. Showing fewer than 12
    # is fine — better a diverse 9 than 7-of-12 from one feed.
    cap, counts, picked = 3, {}, []
    for it in items:
        if counts.get(it["source"], 0) < cap:
            picked.append(it)
            counts[it["source"]] = counts.get(it["source"], 0) + 1
    current_signals = picked[:12]

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
        "sources_research": health.get("summary", {}).get("research", 0),
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
        "feedback": votes,
    }

    save_json(DASHBOARD_JSON, dashboard)
    save_json(HISTORY / f"{today_str()}.json", items)
    _write_data_js(dashboard)
    _write_daily_md(dashboard)
    _write_markdown_dashboard(dashboard)
    log(f"Dashboard built: {counts['items_material']} material items, "
        f"{counts['items_new']} new")
    return dashboard


def _md_std_table(rows: list[dict]) -> str:
    if not rows:
        return "_None tracked._"
    out = ["| Standard / work item | Area | Status | Why watch it |", "|---|---|---|---|"]
    for r in rows:
        out.append(f"| [{r['designation']}]({r['url']}) | {r['area']} | "
                   f"{r['status']} | {r['why']} |")
    return "\n".join(out)


def _write_markdown_dashboard(d: dict) -> None:
    """Stable-named DASHBOARD.md — the rendered view for a private GitHub repo
    (GitHub renders Markdown free on private repos; bookmark its URL)."""
    c = d["counts"]
    L = [
        "# Cyber & Responsible AI Assurance Radar",
        "",
        f"_Updated {d['generated_at']} ({d['timezone']})._  ",
        f"**{c['items_material']}** signals · **{c['items_new']}** new · "
        f"**{c['newsletter_candidates']}** newsletter candidates · "
        f"**{c['standards_tracked']}** standards tracked · "
        f"sources {c['sources_ok']}/{c['sources_checked']} ok "
        f"({c['sources_failed']} failed).",
        "",
    ]
    new_items = sorted(
        [it for sec in d["sections"].values() for it in sec if it.get("is_new")],
        key=lambda x: x.get("relevance_score", 0), reverse=True,
    )
    L += ["## 🆕 New since last run", ""]
    if new_items:
        L += [f"- 🆕 **[{it['title']}]({it['url']})** — {it['source']} · "
              f"{it['lens']} · {it['priority']} ({it['relevance_score']}/5)"
              for it in new_items]
    else:
        L += ["_Nothing new since the last run — all current signals carried over._"]
    L += ["", "## Current signals", ""]
    L += [_md_item(it) for it in d["current_signals"]] or ["_No material signals._"]
    L += ["", "## SC 27 / 27000 family register", "", _md_std_table(d["standards"].get("sc27", []))]
    L += ["", "## SC 42 / 42000 & AI assurance register", "", _md_std_table(d["standards"].get("sc42", []))]
    L += ["", "## Newsletter candidates", ""]
    L += [f"- [{it['title']}]({it['url']}) — {it['source']} ({it['priority']})"
          for it in d["newsletter_candidates"]] or ["_None this run._"]
    L += ["", "## Source health", ""]
    for s in d["source_health"].get("sources", []):
        L.append(f"- {s['status'].upper()} — {s['name']}: {s['detail']}")
    L += ["", "---", "", f"_{CTA}_", ""]
    (ROOT / "DASHBOARD.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def _write_data_js(dashboard: dict) -> None:
    DASHBOARD.mkdir(parents=True, exist_ok=True)
    js = "window.DASHBOARD_DATA = " + json.dumps(dashboard, ensure_ascii=False, indent=2) + ";\n"
    (DASHBOARD / "dashboard-data.js").write_text(js, encoding="utf-8")


def _md_item(it: dict) -> str:
    flag = "🆕 " if it.get("is_new") else ""
    bits = [f"- {flag}**[{it['title']}]({it['url']})** "
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
        f"({c['sources_failed']} failed, {c['sources_research']} via research).",
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
