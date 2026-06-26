"""Weekly newsletter generator.

Reads the last 7 daily history snapshots, curates the strongest 3-7 items, picks a
theme, and writes copy/paste-ready outputs:
  data/weekly/YYYY-MM-DD-newsletter.md / .html
  data/weekly/YYYY-MM-DD-linkedin-post.md
  data/weekly/latest-newsletter.md / .html
"""
from __future__ import annotations

from collections import Counter
from datetime import timedelta

from radar_common import DATA, HISTORY, WEEKLY, load_json, log, now, today_str

CTA = (
    "If your organisation is preparing for ISO/IEC 27001, ISO/IEC 42001, cyber "
    "assurance or responsible AI governance, I can help you separate what matters "
    "from what is noise — and build an evidence-based path forward."
)

THEME_LABELS = {
    "ASD": "ASD / ACSC cyber assurance expectations",
    "CyberResilience": "cyber resilience",
    "SC27": "the ISO/IEC 27000 family",
    "ISO27000": "the ISO/IEC 27000 family",
    "SC42": "ISO/IEC 42001 and AI management systems",
    "ISO42000": "ISO/IEC 42001 and AI management systems",
    "ResponsibleAI": "responsible AI governance",
    "PublicSector": "Australian public sector AI assurance",
    "Regulation": "regulatory and operational-resilience change",
    "Privacy": "privacy and data protection",
}


def _load_window(days: int = 7) -> list[dict]:
    cutoff = (now() - timedelta(days=days)).date().isoformat()
    by_id: dict[str, dict] = {}
    for f in sorted(HISTORY.glob("*.json")):
        if f.stem < cutoff:
            continue
        for it in load_json(f, []):
            cur = by_id.get(it["id"])
            if cur is None or it.get("relevance_score", 0) > cur.get("relevance_score", 0):
                by_id[it["id"]] = it
    votes = load_json(DATA / "feedback.json", {})
    return [it for it in by_id.values() if votes.get(it["id"]) != "down"]


def _select(items: list[dict]) -> list[dict]:
    items = sorted(
        items,
        key=lambda x: (x.get("newsletter_candidate", False), x.get("relevance_score", 0),
                       x.get("published_date") or ""),
        reverse=True,
    )
    top = [it for it in items if it.get("relevance_score", 0) >= 4]
    if len(top) < 3:
        top = items[:5]
    return top[:7]


def _theme(items: list[dict]) -> str:
    if not items:
        return "cyber and responsible AI assurance"
    common = Counter(it.get("lens", "") for it in items).most_common(1)[0][0]
    return THEME_LABELS.get(common, "cyber and responsible AI assurance")


def _bucket(items, lenses):
    return [it for it in items if it.get("lens") in lenses]


def build() -> dict:
    window = _load_window()
    top = _select(window)
    theme = _theme(top)
    date = today_str()

    md = _newsletter_md(top, window, theme, date)
    html = _newsletter_html(top, theme, date)
    linkedin = _linkedin_md(top, theme, date)

    WEEKLY.mkdir(parents=True, exist_ok=True)
    for name, content in [
        (f"{date}-newsletter.md", md),
        (f"{date}-newsletter.html", html),
        (f"{date}-linkedin-post.md", linkedin),
        ("latest-newsletter.md", md),
        ("latest-newsletter.html", html),
    ]:
        (WEEKLY / name).write_text(content, encoding="utf-8")

    words = len(md.split())
    log(f"Newsletter built: {len(top)} items, theme='{theme}', {words} words")
    return {"items": len(top), "theme": theme, "words": words}


def _newsletter_md(top, window, theme, date) -> str:
    L = [
        f"# Cyber & Responsible AI Assurance Radar — week to {date}",
        "",
        "**Subject line options**",
        f"1. This week in assurance: {theme}",
        f"2. {len(top)} signals worth your attention — {theme}",
        "3. Assurance Radar: what changed, why it matters",
        "",
        f"**Preview text:** A focused read on {theme} and what it means for "
        "ISO/IEC 27001, ISO/IEC 42001 and Australian assurance practice.",
        "",
        "---",
        "",
        "Hi — here's this week's signal, not noise.",
        "",
        f"The theme this week is **{theme}**. "
        f"Below are the developments most likely to matter for assurance, audit and "
        "advisory work, with a practical takeaway at the end.",
        "",
        "## Top developments",
        "",
    ]
    for i, it in enumerate(top, 1):
        L.append(f"{i}. **[{it['title']}]({it['url']})** — {it['source']}"
                 f"{' · ' + it['published_date'] if it.get('published_date') else ''}")
        if it.get("why_it_matters"):
            L.append(f"   {it['why_it_matters']}")
        L.append("")

    L += _md_watch("Standards & assurance watch", _bucket(window, {"SC27", "ISO27000", "SC42", "ISO42000"}))
    L += _md_watch("Responsible AI watch", _bucket(window, {"ResponsibleAI"}))
    L += _md_watch("Cyber security watch", _bucket(window, {"ASD", "CyberResilience"}))
    L += _md_watch("Australian public sector & regulatory watch", _bucket(window, {"PublicSector", "Regulation", "Privacy"}))

    takeaway = top[0]["why_it_matters"] if top and top[0].get("why_it_matters") else (
        "Keep your control evidence and AI governance artefacts current — the "
        "expectations are tightening faster than the standards are reissued.")
    L += ["## Practical takeaway", "", takeaway, "", "---", "", CTA, ""]
    return "\n".join(L)


def _md_watch(title, items) -> list[str]:
    if not items:
        return []
    items = sorted(items, key=lambda x: x.get("relevance_score", 0), reverse=True)[:4]
    out = [f"## {title}", ""]
    out += [f"- [{it['title']}]({it['url']}) — {it['source']}" for it in items]
    out.append("")
    return out


def _newsletter_html(top, theme, date) -> str:
    rows = []
    for i, it in enumerate(top, 1):
        why = it.get("why_it_matters", "")
        rows.append(
            f'<li style="margin:0 0 14px;"><a href="{it["url"]}" '
            f'style="color:#111;font-weight:600;">{_esc(it["title"])}</a> '
            f'<span style="color:#666;">— {_esc(it["source"])}</span>'
            f'<div style="color:#333;margin-top:3px;">{_esc(why)}</div></li>'
        )
    # Neutral, email-safe styling. Visual identity (black/white/lime) pending mock-up.
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Assurance Radar — {date}</title></head>
<body style="margin:0;background:#fff;color:#111;font-family:-apple-system,Segoe UI,Arial,sans-serif;">
<div style="max-width:640px;margin:0 auto;padding:28px 22px;">
  <p style="text-transform:uppercase;letter-spacing:.12em;font-size:12px;color:#666;margin:0;">
    Cyber &amp; Responsible AI Assurance Radar</p>
  <h1 style="font-size:22px;margin:6px 0 2px;">Week to {date}</h1>
  <p style="color:#444;margin:0 0 20px;">Theme: <strong>{_esc(theme)}</strong></p>
  <h2 style="font-size:15px;border-bottom:2px solid #111;padding-bottom:4px;">Top developments</h2>
  <ol style="padding-left:18px;">{''.join(rows)}</ol>
  <p style="background:#f4f4f4;border-left:3px solid #111;padding:12px 14px;color:#222;">{_esc(CTA)}</p>
</div></body></html>
"""


def _linkedin_md(top, theme, date) -> str:
    L = [f"This week's Cyber & Responsible AI Assurance Radar — theme: {theme}.", ""]
    for it in top[:3]:
        L.append(f"• {it['title']} ({it['source']})")
    L += ["",
          "My read: the assurance bar keeps rising between standard revisions. "
          "Treat these as evidence and governance prompts, not just news.",
          "", CTA, "",
          "#ISO27001 #ISO42001 #CyberSecurity #ResponsibleAI #GRC #Assurance"]
    return "\n".join(L)


def _esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


if __name__ == "__main__":
    build()
