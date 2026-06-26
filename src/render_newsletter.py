"""Weekly newsletter generator.

Reads the last 7 daily history snapshots, curates the strongest 3-7 items, picks a
theme, and writes copy/paste-ready outputs:
  data/weekly/YYYY-MM-DD-newsletter.md / .html
  data/weekly/YYYY-MM-DD-linkedin-post.md
  data/weekly/latest-newsletter.md / .html
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta

from radar_common import (
    DATA, FEEDBACK_FILE, HISTORY, WEEKLY, load_json, log, now, today_str, vote_of,
)

CTA = (
    "If your organisation is preparing for ISO/IEC 27001, ISO/IEC 42001, cyber "
    "assurance or responsible AI governance, I can help you separate what matters "
    "from what is noise, and build an evidence-based path forward."
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


TAGLINE = ("A focused brief on cyber security and responsible AI assurance: ISO/IEC "
           "27001 & 42001, ASD/ACSC guidance, and Australian public-sector developments. "
           "Signal, not noise.")


def _no_emdash(s: str) -> str:
    return s.replace("—", "-").replace("–", "-")


def _fmt_date(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{dt.day} {dt:%B %Y}"
    except ValueError:
        return date_str


def _header(date_str: str) -> list[str]:
    return [
        "# Cyber & Responsible AI Assurance Radar",
        f"**{_fmt_date(date_str)} · by Andrew Robinson**",
        "",
        f"_{TAGLINE}_",
        "",
    ]


def _toc(entries: list[str]) -> list[str]:
    out = ["## In this issue", ""]
    out += [f"{i}. {t}" for i, t in enumerate(entries, 1)]
    out += ["- Practical takeaway", "- About this newsletter", ""]
    return out


def _footer() -> list[str]:
    return [
        "---",
        "",
        "## About this newsletter",
        "",
        "The Cyber & Responsible AI Assurance Radar is a curated brief by Andrew "
        "Robinson, tracking cyber security and responsible AI assurance — ISO/IEC 27001 "
        "and 42001, ASD/ACSC guidance (ISM, Essential Eight), and Australian "
        "public-sector and regulatory developments. Signal, not noise.",
        "",
        CTA,
        "",
        "Forward this to a colleague who'd find it useful.",
        "",
        "_Curated by Andrew Robinson. Opinions are my own._",
        "",
        "Copyright © 2026 Andrew Robinson.",
    ]


_AREA_OF = {
    "ASD": "cyber", "CyberResilience": "cyber",
    "SC27": "iso27k", "ISO27000": "iso27k", "Privacy": "iso27k",
    "SC42": "ai", "ISO42000": "ai", "ResponsibleAI": "ai",
    "PublicSector": "ausreg", "Regulation": "ausreg",
}
_AREA_NAME = {
    "cyber": "ASD/ACSC cyber resilience",
    "iso27k": "the ISO/IEC 27000 family and privacy",
    "ai": "ISO/IEC 42001 and responsible AI",
    "ausreg": "Australian public-sector and regulatory change",
}
_AREA_INSIGHT = {
    "cyber": "On the cyber side, the message for your organisation is to turn these "
             "advisories into control evidence: confirm your patching cadence, identity "
             "hardening and incident readiness stand up against the Essential Eight and "
             "ISO/IEC 27001 Annex A.",
    "iso27k": "On information security and privacy, movement in the ISO/IEC 27000 family "
              "is a prompt to revisit your ISMS scope, control mappings and the assurance "
              "evidence your own customers and auditors ask for.",
    "ai": "On AI, the shift from principles to evidence is accelerating: if your "
          "organisation uses or builds AI, expect to demonstrate ISO/IEC 42001-style "
          "controls, impact assessments and human oversight, not just a policy.",
    "ausreg": "For Australian public-sector and regulated organisations, these are "
              "likely to surface in procurement requirements, board reporting and "
              "operational-resilience obligations.",
}


def _takeaway(items: list[dict], theme: str) -> str:
    if not items:
        return ("Nothing curated this edition. Once items are added, this takeaway will "
                "tie them together and point to the controls and assurance evidence your "
                "organisation should check.")
    counts = Counter(_AREA_OF.get(it.get("lens", ""), "cyber") for it in items)
    areas = [a for a, _ in counts.most_common()]
    names = [_AREA_NAME[a] for a in areas]
    sentences = [f"This edition spans {'; '.join(names)}. The common thread is {theme}."]
    sentences += [_AREA_INSIGHT[a] for a in areas[:2]]
    sentences.append(
        "The practical step: pick the two or three items most relevant to your "
        "environment, map each to a control or assurance question you can answer with "
        "evidence, and decide what your board, auditors or own customers need to see "
        "this quarter.")
    return " ".join(sentences)


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
    votes = load_json(FEEDBACK_FILE, {})
    return [it for it in by_id.values() if vote_of(votes.get(it["id"])) != "down"]


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


def compose_newsletter(items: list[dict], date: str) -> tuple[str, str]:
    """Copy/paste newsletter markdown from an explicit list of items (the user's 👍
    picks). Returns (markdown, theme). Lists every selected item, not just 3-7."""
    items = sorted(items, key=lambda x: (x.get("relevance_score", 0),
                                         x.get("published_date") or ""), reverse=True)
    theme = _theme(items)

    # Subject helper (pick one, delete the block) — kept above the masthead.
    L = [
        "SUBJECT OPTIONS — pick one, then delete these three lines:",
        f"  • This edition: {theme}",
        f"  • {len(items)} assurance signals worth your attention",
        "  • Assurance Radar: what changed, why it matters",
        "",
    ]
    L += _header(date)
    L += _toc([it["title"] for it in items] or ["(no items selected yet)"])
    L += ["---", "",
          f"The theme this edition is **{theme}**. Here are the developments I've "
          "flagged as worth your attention.", ""]

    if not items:
        L += ["_No items selected — give signals a 👍 on the dashboard, then build again._", ""]
    for i, it in enumerate(items, 1):
        L += [f"## {i}. {it['title']}", ""]
        if it.get("why_it_matters"):
            L += [it["why_it_matters"], ""]
        meta = f"_{it['source']}"
        if it.get("published_date"):
            meta += f" · {it['published_date']}"
        meta += f" · [read more]({it['url']})_"
        L += [meta, ""]

    L += ["## Practical takeaway", "", _takeaway(items, theme), ""]
    L += _footer()
    return _no_emdash("\n".join(L) + "\n"), theme


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
    watches = [
        ("Standards & assurance watch", _bucket(window, {"SC27", "ISO27000", "SC42", "ISO42000"})),
        ("Responsible AI watch", _bucket(window, {"ResponsibleAI"})),
        ("Cyber security watch", _bucket(window, {"ASD", "CyberResilience"})),
        ("Australian public sector & regulatory watch", _bucket(window, {"PublicSector", "Regulation", "Privacy"})),
    ]
    L = [
        "SUBJECT OPTIONS — pick one, then delete these three lines:",
        f"  • This week in assurance: {theme}",
        f"  • {len(top)} signals worth your attention — {theme}",
        "  • Assurance Radar: what changed, why it matters",
        "",
    ]
    L += _header(date)
    L += _toc([it["title"] for it in top] + [name for name, items in watches if items])
    L += ["---", "",
          f"This week's theme is **{theme}** — the developments most likely to matter "
          "for assurance, audit and advisory work.", "",
          "## Top developments", ""]
    for i, it in enumerate(top, 1):
        L.append(f"{i}. **[{it['title']}]({it['url']})** — {it['source']}"
                 f"{' · ' + it['published_date'] if it.get('published_date') else ''}")
        if it.get("why_it_matters"):
            L.append(f"   {it['why_it_matters']}")
        L.append("")
    for name, items in watches:
        L += _md_watch(name, items)
    L += ["## Practical takeaway", "", _takeaway(top, theme), ""]
    L += _footer()
    return _no_emdash("\n".join(L))


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
    return _no_emdash(f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Assurance Radar - {date}</title></head>
<body style="margin:0;background:#fff;color:#111;font-family:-apple-system,Segoe UI,Arial,sans-serif;">
<div style="max-width:640px;margin:0 auto;padding:28px 22px;">
  <p style="text-transform:uppercase;letter-spacing:.12em;font-size:12px;color:#666;margin:0;">
    Cyber &amp; Responsible AI Assurance Radar</p>
  <h1 style="font-size:22px;margin:6px 0 2px;">Week to {date}</h1>
  <p style="color:#444;margin:2px 0 0;">by Andrew Robinson · Theme: <strong>{_esc(theme)}</strong></p>
  <p style="color:#666;font-size:13px;margin:8px 0 20px;">{_esc(TAGLINE)}</p>
  <h2 style="font-size:15px;border-bottom:2px solid #111;padding-bottom:4px;">Top developments</h2>
  <ol style="padding-left:18px;">{''.join(rows)}</ol>
  <p style="background:#f4f4f4;border-left:3px solid #111;padding:12px 14px;color:#222;">{_esc(CTA)}</p>
  <hr style="border:none;border-top:1px solid #ddd;margin:24px 0;">
  <h2 style="font-size:14px;">About this newsletter</h2>
  <p style="color:#555;font-size:13px;line-height:1.5;">A curated brief by Andrew Robinson,
    tracking cyber security and responsible AI assurance — ISO/IEC 27001 and 42001, ASD/ACSC
    guidance, and Australian public-sector and regulatory developments. Forward freely.</p>
  <p style="color:#888;font-size:12px;">Copyright © 2026 Andrew Robinson. Opinions are my own.</p>
</div></body></html>
""")


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
