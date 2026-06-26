"""Stage 4 — enrich material items with summary / why_it_matters / suggested_action.

DEFAULT: deterministic, free, no network. Generic-but-honest guidance built only
from the item's own metadata — never fabricating facts.

PRO-PLAN PATH (no API billing): every run writes a ready-to-paste prompt pack to
data/daily/<date>-enrichment-prompt.md. Paste it into Claude Desktop (Pro/Max plan),
save the JSON reply to data/_cache/enrichment-in.json, then run
`python src/apply_enrichment.py`.

OPTIONAL PAID API: only if BOTH RADAR_USE_API=1 and ANTHROPIC_API_KEY are set
(off by default — this is billed separately from a Claude subscription).

Output: data/_cache/enriched.json
"""
from __future__ import annotations

import json
import os
import urllib.request

from radar_common import CACHE, DAILY, load_json, log, save_json, today_str

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = os.environ.get("RADAR_MODEL", "claude-sonnet-4-6")
MAX_ENRICH = int(os.environ.get("RADAR_MAX_LLM", "30"))
BATCH = 8

# Lens-specific framing for the deterministic fallback (no fabricated facts).
LENS_WHY = {
    "ASD": "Bears on ASD/ACSC expectations (ISM, Essential Eight); check the impact on baseline controls and audit evidence.",
    "CyberResilience": "Affects cyber-resilience posture; weigh against attack-surface, patching, IAM and incident-response controls.",
    "SC27": "Touches the ISO/IEC 27000 family; assess the impact on ISMS scope, Annex A controls and certification.",
    "ISO27000": "Touches the ISO/IEC 27000 family; assess the impact on ISMS scope, Annex A controls and certification.",
    "SC42": "Touches ISO/IEC 42001 and AI management systems; assess the impact on AIMS controls and AI governance evidence.",
    "ISO42000": "Touches ISO/IEC 42001 and AI management systems; assess the impact on AIMS controls and AI governance evidence.",
    "ResponsibleAI": "Relevant to responsible AI governance (transparency, oversight, AI risk); consider impact assessment and assurance evidence.",
    "Privacy": "Privacy / data-protection relevance; weigh against ISO/IEC 27701, Privacy Act reform and customer assurance.",
    "Regulation": "Regulatory / operational-resilience signal; assess obligations, CPS 230/234 alignment and board reporting.",
    "PublicSector": "Australian public sector AI assurance relevance; check DTA standards, AI impact assessment and procurement.",
}
DEFAULT_WHY = "Relevant to cyber/AI assurance; assess the impact on ISO/IEC 27001 / 42001 positioning, control design or audit practice."
DEFAULT_ACTION = "Review the source and decide whether it changes advisory positioning, control design or client guidance."

SYSTEM = (
    "You are an assurance analyst for a boutique cyber security and responsible AI "
    "advisory. Audience: an ISO/IEC 27001 and ISO/IEC 42001 lead auditor advising "
    "Australian enterprise and public sector clients. Be precise about standards, use "
    "Australian English, never fabricate facts, and never invent standard numbers or "
    "publication claims. If the input is thin, stay general rather than inventing detail."
)

INSTRUCTION = (
    "For each item, return STRICT JSON: an array of objects with keys id, score, "
    "summary, why_it_matters and suggested_action.\n"
    "- score: integer 1-5 for assurance relevance. 5 = critical (mandatory change, "
    "ASD/ISM/Essential Eight expectation, certification/conformity, regulatory "
    "obligation, board-level cyber/AI accountability); 4 = high advisory/newsletter "
    "value; 3 = useful watch; 2 = low; 1 = ignore. Prefer primary sources and "
    "actionable advisories; routine statistics, telco/broadcasting notices and generic "
    "news score low.\n"
    "- summary: <=45 words, factual.\n"
    "- why_it_matters: 1-2 sentences tying it to cyber/AI assurance, ISO 27001/42001, "
    "ASD/ISM/Essential Eight or Australian public sector assurance.\n"
    "- suggested_action: one imperative sentence.\n"
    "Output JSON only."
)


def _det(item: dict) -> dict:
    item = dict(item)
    item["summary"] = item.get("summary") or item.get("title", "")
    item["why_it_matters"] = LENS_WHY.get(item.get("lens", ""), DEFAULT_WHY)
    item["suggested_action"] = DEFAULT_ACTION
    item["enriched_by"] = "deterministic"
    return item


def _payload(items: list[dict]) -> list[dict]:
    return [{"id": it["id"], "title": it["title"], "source": it["source"],
             "lens": it["lens"], "url": it["url"], "context": it.get("summary", "")}
            for it in items]


def _write_prompt_pack(items: list[dict]) -> None:
    """Pro-plan path: a prompt to paste into Claude Desktop (no API billing)."""
    pack = (
        f"# Enrichment prompt — {today_str()}\n\n"
        "Paste everything below into Claude (Desktop/Pro). Save its JSON reply to "
        "`data/_cache/enrichment-in.json`, then run `python src/apply_enrichment.py`.\n\n"
        "---\n\n"
        f"{SYSTEM}\n\n{INSTRUCTION}\n\nITEMS:\n"
        + json.dumps(_payload(items), ensure_ascii=False, indent=2)
        + "\n"
    )
    (DAILY / f"{today_str()}-enrichment-prompt.md").write_text(pack, encoding="utf-8")


def _llm_batch(items: list[dict], api_key: str) -> list[dict] | None:
    body = json.dumps({
        "model": MODEL, "max_tokens": 2000, "system": SYSTEM,
        "messages": [{"role": "user", "content": INSTRUCTION + "\n\nITEMS:\n"
                      + json.dumps(_payload(items), ensure_ascii=False)}],
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL, data=body, method="POST",
        headers={"x-api-key": api_key, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read())
        text = "".join(b.get("text", "") for b in data.get("content", []))
        text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        by_id = {o["id"]: o for o in json.loads(text)}
    except Exception as e:  # noqa: BLE001
        log(f"LLM batch failed, falling back: {repr(e)[:90]}")
        return None
    out = []
    for it in items:
        o = by_id.get(it["id"])
        if not o:
            out.append(_det(it)); continue
        it = dict(it)
        it["summary"] = o.get("summary") or it.get("summary", "")
        it["why_it_matters"] = o.get("why_it_matters", "")
        it["suggested_action"] = o.get("suggested_action", "")
        it["enriched_by"] = "llm"
        out.append(it)
    return out


def enrich() -> list[dict]:
    scored = load_json(CACHE / "scored.json", [])
    material = [it for it in scored if it.get("relevance_score", 0) >= 2]
    material.sort(key=lambda x: (x["relevance_score"], x.get("published_date", "")), reverse=True)

    _write_prompt_pack(material[:MAX_ENRICH])

    use_api = os.environ.get("RADAR_USE_API") == "1"
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()

    if use_api and api_key:
        log(f"RADAR_USE_API=1 — enriching up to {MAX_ENRICH} items via Claude API ({MODEL}, billed separately)")
        targets = material[:MAX_ENRICH]
        enriched = []
        for start in range(0, len(targets), BATCH):
            batch = targets[start:start + BATCH]
            result = _llm_batch(batch, api_key)
            enriched.extend(result if result is not None else [_det(it) for it in batch])
        enriched.extend(_det(it) for it in material[MAX_ENRICH:])
    else:
        log("Deterministic enrichment (free). Pro-plan prompt pack written to data/daily/.")
        enriched = [_det(it) for it in material]

    save_json(CACHE / "enriched.json", enriched)
    by = {}
    for it in enriched:
        by[it.get("enriched_by", "?")] = by.get(it.get("enriched_by", "?"), 0) + 1
    log(f"Enriched {len(enriched)} items {by}")
    return enriched


if __name__ == "__main__":
    enrich()
