"""Stage 3 — score and prioritise items against the relevance rubric.

Transparent, deterministic keyword + source-tier scoring (1-5). The term lists
below are the machine-readable mirror of prompts/relevance-rubric.md — edit them
to tune the radar. Scoring assigns: relevance_score, priority, lens (refined),
tags, newsletter_candidate, and is_new (vs data/seen_items.json).

Output: data/_cache/scored.json
"""
from __future__ import annotations

import re

from radar_common import CACHE, SEEN_FILE, load_json, log, save_json

# --- Term lists (edit to tune relevance) ------------------------------------
# Strong assurance signals -> big boost. Keep these tight and authoritative.
CRITICAL_TERMS = [
    "iso/iec 27001", "iso 27001", "iso/iec 42001", "iso 42001",
    "essential eight", "essential 8", "information security manual", "ism",
    "conformity assessment", "certification", "accreditation",
    "ai assurance framework", "mandatory", "legislation", "regulation",
    "directive", "national ai assurance", "secure by design",
    "automated decision-making", "automated decision making",
]

# Lens detection + general relevance. lens -> terms (order = priority).
LENS_TERMS = {
    "ASD": ["acsc", "asd", "essential eight", "information security manual", "ism",
            "secure by design", "secure by default", "critical infrastructure",
            "post-quantum", "operational technology", "incident response"],
    "SC42": ["42001", "42003", "42005", "42006", "42007", "5259", "sc 42", "sc42",
             "ai management system", "aims", "ai conformity", "machine learning"],
    "ISO42000": ["42001", "ai management system", "aims", "ai impact assessment"],
    "ResponsibleAI": ["responsible ai", "ai governance", "ai safety", "transparency",
                      "explainability", "human oversight", "synthetic data",
                      "generative ai", "ai incident", "ai risk", "agentic"],
    "SC27": ["27001", "27002", "27005", "27006", "27017", "27018", "27701",
             "27560", "27561", "27565", "sc 27", "sc27", "15408"],
    "ISO27000": ["27001", "27002", "information security management", "isms"],
    "Privacy": ["privacy", "oaic", "gdpr", "personal information", "data protection",
                "privacy act", "pets", "de-identification"],
    "Regulation": ["cps 234", "operational resilience", "prudential standard",
                   "incident reporting", "regulatory reform", "privacy reform",
                   "enforcement", "mandatory reporting", "systemic risk"],
    "PublicSector": ["dta", "digital transformation", "public sector", "government",
                     "commonwealth", "procurement", "transparency statement"],
    "CyberResilience": ["vulnerability", "threat", "ransomware", "resilience",
                        "supply chain", "cloud security", "identity", "patch"],
}

# Vendor marketing / generic noise -> penalty toward "ignore".
IGNORE_TERMS = [
    "webinar", "sponsored", "magic quadrant", "buy now", "discount", "promo",
    "free trial", "register now", "download our", "product launch", "now available",
    "named a leader", "wins award", "partners with", "sign up", "ebook",
]

PRIORITY_BY_SCORE = {5: "Critical", 4: "High", 3: "Medium", 2: "Watch", 1: "Low"}

# Alphanumeric-boundary match so short terms don't match inside longer words
# (e.g. "aims" must not match "claims", "ism" must not match "mechanism").
_RX_CACHE: dict[str, re.Pattern] = {}


def _has(hay: str, term: str) -> bool:
    rx = _RX_CACHE.get(term)
    if rx is None:
        rx = re.compile(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])")
        _RX_CACHE[term] = rx
    return rx.search(hay) is not None


def _haystack(item: dict) -> str:
    return f" {item.get('title','')} {item.get('summary','')} ".lower()


def _tier_base(item: dict) -> int:
    tier = item.get("tier", 2)
    stype = item.get("source_type", "media")
    if stype in ("primary", "regulator", "standard_body", "government") or tier == 1:
        return 3
    if stype == "research" or tier == 2:
        return 2
    return 1


def detect_lens_and_tags(item: dict) -> tuple[str, list[str]]:
    hay = _haystack(item)
    hits: dict[str, int] = {}
    tags: list[str] = []
    for lens, terms in LENS_TERMS.items():
        for t in terms:
            if _has(hay, t):
                hits[lens] = hits.get(lens, 0) + 1
                if t.strip() not in tags and len(t.strip()) > 3:
                    tags.append(t.strip())
    if hits:
        best = max(hits, key=hits.get)
        return best, tags[:8]
    return item.get("lens", "CyberResilience"), tags[:8]


def score_item(item: dict) -> dict:
    hay = _haystack(item)
    base = _tier_base(item)

    critical_hits = sum(1 for t in CRITICAL_TERMS if _has(hay, t))
    lens, tags = detect_lens_and_tags(item)
    topic_hits = len(tags)
    ignore_hits = sum(1 for t in IGNORE_TERMS if _has(hay, t))

    score = base
    if critical_hits:
        score += 2
    if topic_hits >= 2:
        score += 1
    elif topic_hits == 0:
        score -= 1  # mentions nothing on the radar -> de-prioritise
    score -= 2 * ignore_hits

    score = max(1, min(5, score))

    item = dict(item)
    item["lens"] = lens
    item["tags"] = tags
    item["relevance_score"] = score
    item["priority"] = PRIORITY_BY_SCORE[score]
    item["newsletter_candidate"] = score >= 4
    return item


def score_all() -> list[dict]:
    items = load_json(CACHE / "normalised.json", [])
    seen = load_json(SEEN_FILE, {})

    scored = [score_item(it) for it in items]
    for it in scored:
        it["is_new"] = it["id"] not in seen

    ignored = sum(1 for it in scored if it["relevance_score"] <= 1)
    save_json(CACHE / "scored.json", scored)
    log(f"Scored {len(scored)} items "
        f"(material>=2: {sum(1 for i in scored if i['relevance_score']>=2)}, ignored: {ignored})")
    return scored


if __name__ == "__main__":
    score_all()
