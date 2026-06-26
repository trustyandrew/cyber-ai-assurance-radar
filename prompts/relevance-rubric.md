# Relevance rubric

This is the human-readable rubric. The machine-readable mirror lives in
`src/score_items.py` (the `CRITICAL_TERMS`, `LENS_TERMS` and `IGNORE_TERMS` lists).
Keep the two in step when you tune the radar.

## Scoring (1–5)

- **5 — Critical signal.** Materially affects ISO/IEC 27001 or 42001 assurance,
  ASD / ISM / Essential Eight expectations, public sector cyber or AI assurance,
  certification or audit practice, regulatory obligations, AI governance evidence,
  cyber resilience expectations, or board-level cyber/AI accountability.
- **4 — High-value signal.** Not mandatory but likely to affect advisory
  positioning, client conversations, newsletter themes, assurance methodology,
  control design, risk assessment, AI impact assessment, or privacy/cloud assurance.
- **3 — Useful watch item.** Relevant but not urgent.
- **2 — Low-value item.** Retain only if useful for future context.
- **1 — Ignore.** Generic, repetitive, vendor-led or low-assurance-value. Excluded
  from the dashboard; counted as "ignored" in source health.

## How the deterministic score is built

```
base       = 3 if source is primary/regulator/standard_body/government (tier 1)
             2 if research (tier 2)
             1 if media/vendor (tier 3)
+2         if any CRITICAL_TERM appears (e.g. "ISO/IEC 27001", "Essential Eight",
             "Information Security Manual", "conformity assessment", "mandatory")
+1         if 2+ lens/topic terms match
-1         if no lens/topic term matches (on the radar in name only)
-2 each    for vendor-marketing / noise terms ("webinar", "magic quadrant", …)
score      = clamp(1, 5)
priority   = 5 Critical · 4 High · 3 Medium · 2 Watch · 1 Low
newsletter_candidate = score >= 4
```

## Inclusion principle

Do **not** include an item simply because it mentions AI or cyber. Include it only
if it has practical relevance to assurance, governance, audit, certification,
standards, public sector, critical infrastructure, privacy, control design or
responsible AI. Prefer primary sources over commentary.

## Lenses

`ASD · SC27 · SC42 · ISO27000 · ISO42000 · ResponsibleAI · Regulation · Privacy ·
CyberResilience · PublicSector`
