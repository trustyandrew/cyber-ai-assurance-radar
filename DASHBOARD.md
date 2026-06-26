# Cyber & Responsible AI Assurance Radar

_Updated 2026-06-26T11:28:46+10:00 (Australia/Melbourne)._  
**37** signals · **0** new · **4** newsletter candidates · **32** standards tracked · sources 5/21 ok (1 failed).

## Current signals

- **[CRITICAL ALERT: Active exploitation of cPanel/WHM critical vulnerability](https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/active-exploitation-of-cpanel-whm-critical-vulnerability)** — ASD ACSC — Alerts & advisories · 2026-05-01 · High (4/5)
  ASD's ACSC reports active exploitation of a critical cPanel/WHM administration vulnerability (CVE-2026-4194). Patches are available and exposed hosting-management consoles are being targeted.
  *Why it matters:* A live test of patch-management discipline — Essential Eight 'patch applications' (ML2/ML3 timeframes) and ISM patching controls. Any client on cPanel-based or reseller hosting has an open exposure window now, not a future risk.
  *Action:* Alert clients running cPanel/WHM, confirm CVE-2026-4194 is patched, and capture the remediation timeline as Essential Eight / ISM control evidence.
- **[Preparing for a ‘vulnerability patch wave’](https://www.ncsc.gov.uk/blogs/prepare-for-vulnerability-patch-wave)** — UK NCSC — All updates · 2026-05-01 · High (4/5)
  UK NCSC warns of an incoming 'patch wave' as years of accumulated technical debt are addressed across products, and urges organisations to build patch-management capacity now.
  *Why it matters:* Speaks directly to ISO/IEC 27001 Annex A vulnerability- and change-management controls and Essential Eight patch cadence — useful framing for clients whose patch pipelines cannot absorb surge volumes.
  *Action:* Review clients' patch-management capacity and SLAs against expected surge volumes and flag where ML2 timeframes are unachievable.
- **[Preparing for severe cyber threat: why leaders must act now](https://www.ncsc.gov.uk/blogs/preparing-for-severe-cyber-threat-why-leaders-must-act-now)** — UK NCSC — All updates · 2026-04-20 · High (4/5)
  UK NCSC leadership calls on organisations to build collective cyber resilience ahead of a more severe threat environment.
  *Why it matters:* Board-level resilience messaging that maps to ISO/IEC 27001 leadership commitment (Clause 5) and cyber-governance reporting — good material for a board or risk-committee conversation.
  *Action:* Use as a prompt to brief client boards on resilience posture and ISMS leadership commitments.
- **[HIGH ALERT: Ongoing targeting of online code repositories](https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/ongoing-targeting-of-online-code-repositories)** — ASD ACSC — Alerts & advisories · 2025-09-19 · High (4/5)
  ASD's ACSC reports increased targeting of online code repositories, with threat actors scanning for exposed secrets and credentials.
  *Why it matters:* Directly relevant to secure-development, secrets-management and supply-chain controls (ISM; ISO/IEC 27001 Annex A 8.x; SSDF) — a common and easily checkable client weakness.
  *Action:* Advise clients to scan repositories for exposed secrets and enforce secret-management and access controls on their code platforms.
- **[Anthropic’s Fable and the State of AI](https://www.schneier.com/blog/archives/2026/06/anthropics-fable-and-the-state-of-ai.html)** — Schneier on Security · 2026-06-19 · Medium (3/5)
  Per Schneier's commentary, the US government classified Anthropic's newly released Fable model as a controlled munition and applied export controls — a notable escalation in how frontier AI is regulated.
  *Why it matters:* Signals AI export-control and dual-use governance entering the assurance picture, relevant to AI procurement, cross-border model use and ISO/IEC 42001 risk context. Treat as commentary — verify the underlying facts before citing.
  *Action:* Track as a watch item on AI export-control exposure for clients procuring or deploying frontier models; verify specifics before any client use.
- **[CRITICAL ALERT: Reported widespread credential exposure affecting Fortinet Firewalls and VPN Gateways](https://www.cyber.gov.au/about-us/view-all-content/Reported-widespread-credential-exposure-affecting-Fortinet-Firewalls-and-VPN-Gateways)** — ASD ACSC — Alerts & advisories · 2026-06-18 · Medium (3/5)
  ASD's ACSC reports a malicious campaign and widespread credential exposure affecting Fortinet firewalls and VPN gateways.
  *Why it matters:* Edge-device and remote-access compromise is a high-impact ISM and Essential Eight concern (MFA, restrict admin privileges, patching) — directly actionable for clients running Fortinet perimeter kit.
  *Action:* Have clients on Fortinet edge devices rotate credentials, enforce MFA, patch, and review VPN/admin access logs for signs of compromise.
- **[NCSC CEO: Hostile states linked to three-quarters of cyber attacks affecting UK's critical systems](https://www.ncsc.gov.uk/news/ncsc-ceo-hostile-states-linked-to-three-quarters-of-cyber-attacks)** — UK NCSC — All updates · 2026-06-17 · Medium (3/5)
  UK NCSC CEO Dr Richard Horne told RUSI's annual lecture that hostile states are linked to roughly three-quarters of cyber attacks on the UK's critical infrastructure.
  *Why it matters:* Strong board and newsletter framing on nation-state threat and critical-infrastructure resilience; aligns with SOCI-style obligations and ISO/IEC 27001 risk context for regulated sectors.
  *Action:* Use as a lead talking point on nation-state risk for critical-infrastructure and regulated clients.
- **[Software supply chain attacks: check your dependencies](https://www.ncsc.gov.uk/blogs/software-supply-chain-attacks-check-your-dependencies)** — UK NCSC — All updates · 2026-06-04 · Medium (3/5)
  UK NCSC warns that attackers are compromising open-source packages and asks defenders to review dependencies to reduce supply-chain risk.
  *Why it matters:* Maps to supply-chain and secure-development controls (ISO/IEC 27001 Annex A; SSDF; ISM) — a concrete, evidence-producing control area for clients that build software.
  *Action:* Advise software clients to inventory and monitor dependencies (SBOM, pinning, provenance) and capture it as supply-chain control evidence.
- **[Thinking carefully before adopting agentic AI](https://www.ncsc.gov.uk/blogs/thinking-carefully-before-adopting-agentic-ai)** — UK NCSC — All updates · 2026-05-15 · Medium (3/5)
  UK NCSC urges caution and maturity — 'walk before you run' — before adopting agentic AI.
  *Why it matters:* Directly relevant to responsible AI governance and ISO/IEC 42001 — agentic autonomy raises human-oversight, control and risk-assessment questions clients are beginning to ask.
  *Action:* Offer clients an agentic-AI readiness and oversight check framed against ISO/IEC 42001 controls before deployment.
- **[Executive Summary: Defending against China-nexus covert networks of compromised devices](https://www.ncsc.gov.uk/news/executive-summary-defending-against-china-nexus-covert-networks-of-compromised-devices)** — UK NCSC — All updates · 2026-04-23 · Medium (3/5)
  International cyber agencies advise organisations to baseline edge-device traffic — especially VPN and remote access — and apply dynamic threat-feed filtering against known covert-network indicators.
  *Why it matters:* Actionable edge and network-monitoring guidance tied to ISM and ISO/IEC 27001 monitoring controls; relevant to clients with significant remote-access estates.
  *Action:* Recommend clients baseline edge/VPN traffic and add covert-network indicator filtering to their monitoring.
- **[New cross domain guidance for government, industry and the wider security community](https://www.ncsc.gov.uk/blogs/new-cross-domain-guidance-for-government-industry-and-the-wider-security-community)** — UK NCSC — All updates · 2026-04-21 · Medium (3/5)
  UK NCSC issued new cross-domain guidance to help government, industry and the wider security community deploy cross-domain technologies more consistently.
  *Why it matters:* Relevant to high-assurance and public-sector environments that move data across security domains; a useful reference for government and defence-adjacent clients.
  *Action:* Flag to public-sector and high-assurance clients evaluating cross-domain solutions.
- **[The AI shift in cyber risk: why leaders must act now](https://www.ncsc.gov.uk/news/the-ai-shift-in-cyber-risk-why-leaders-must-act-now)** — UK NCSC — All updates · 2026-06-22 · Watch (2/5)
  UK NCSC argues that AI is materially shifting cyber risk and that leaders must act now to adapt their defences.
  *Why it matters:* Bridges cyber and AI assurance — connects board cyber accountability with AI-era threat acceleration; a strong newsletter lead linking the ISO/IEC 27001 and 42001 narratives.
  *Action:* Use to frame the AI-and-cyber-risk conversation for boards spanning ISO/IEC 27001 and 42001 programs.

## SC 27 / 27000 family register

| Standard / work item | Area | Status | Why watch it |
|---|---|---|---|
| [ISO/IEC 27000:2018](https://www.iso.org/standard/73906.html) | ISMS overview and vocabulary | Published | Defines the vocabulary for the whole ISMS family — the normative terms used in 27001 audits and certification scope statements (free from ISO). |
| [ISO/IEC 27001:2022 (+ Amd 1:2024)](https://www.iso.org/standard/27001) | ISMS requirements | Published | Core assurance anchor. Amendment 1 (2024) adds climate-action considerations to clauses 4.1/4.2; base edition remains 2022. |
| [ISO/IEC 27002:2022](https://www.iso.org/standard/75652.html) | Information security controls | Published | Control library (93 controls, 4 themes) for ISO 27001 Annex A interpretation, policy rationalisation and audit evidence. |
| [ISO/IEC 27004:2016](https://www.iso.org/standard/64120.html) | ISMS monitoring, measurement, analysis and evaluation | Published (revision underway) | Guidance for ISO 27001 clause 9.1 performance evaluation — the metrics and effectiveness evidence auditors look for. A DIS revision is in progress. |
| [ISO/IEC 27005:2022](https://www.iso.org/standard/80585.html) | Information security risk management | Published | Risk-process bridge between the ISMS, cyber resilience, supplier risk and AI-enabled system risk; aligned to 27001:2022 and ISO 31000. |
| [ISO/IEC 27006-1:2024](https://www.iso.org/standard/82908.html) | Requirements for ISMS certification bodies | Published | Certification-integrity baseline for audit bodies; the two-year transition concluded around March 2026. |
| [ISO/IEC 27007:2020](https://www.iso.org/standard/77802.html) | Guidelines for ISMS auditing | Published | How-to for planning and conducting ISMS audits (first/second party); complements the 27006-1 third-party certification requirements. |
| [ISO/IEC 27017:2015](https://www.iso.org/standard/43757.html) | Cloud information security controls | Published (2nd ed. at FDIS) | Current in-force edition is 2015; the 2nd edition is at FDIS (publication expected 2026). Watch for alignment to current cloud/SaaS/sovereign-cloud assurance. |
| [ISO/IEC 27018:2025](https://www.iso.org/standard/88150.html) | PII protection in public clouds | Published | 3rd edition (Aug 2025), aligned to 27002:2022 with a new Annex B; useful for SaaS privacy, processor obligations and customer assurance packs. |
| [ISO/IEC 27035-1:2023](https://www.iso.org/standard/78973.html) | Information security incident management (principles and process) | Published | Underpins 27001/27002 incident controls; the detect/report/respond/learn process assessed in audits and expected under DORA, GDPR and APRA CPS 234. |
| [ISO/IEC 27701:2025](https://www.iso.org/standard/27701.html) | Privacy information management systems (PIMS) | Published | 2nd edition (Oct 2025) — now a standalone, independently certifiable PIMS (no longer a 27001 extension). Bridges ISMS, privacy and Privacy Act reform. Transition ~Oct 2028. |
| [ISO/IEC 27565:2026](https://www.iso.org/standard/80398.html) | Privacy preservation using zero-knowledge proofs | Published | Edition 1 (Feb 2026). Relevant to PETs, digital identity, verifiable credentials and sensitive AI use cases. |
| [ISO/IEC 15408 series:2026](https://www.iso.org/standard/88134.html) | IT security evaluation / Common Criteria (parts 1-5) | Published | 5th edition, parts published Apr-May 2026 (superseding the 2022 edition). SC 27-relevant for formal product/security assurance and Common Criteria certificates. |

## SC 42 / 42000 & AI assurance register

| Standard / work item | Area | Status | Why watch it |
|---|---|---|---|
| [ISO/IEC 22989:2022](https://www.iso.org/standard/74296.html) | AI concepts and terminology | Published | Foundational AI vocabulary normatively referenced across SC 42 (incl. 42001); consistent definitions for AI assurance. (Gen-AI amendment in progress.) |
| [ISO/IEC 23894:2023](https://www.iso.org/standard/77304.html) | AI risk management guidance | Published | The AI-specific companion to ISO 31000 and the de-facto reference for AI risk management; underpins risk treatment in ISO/IEC 42001 audits. |
| [ISO/IEC 5338:2023](https://www.iso.org/standard/81118.html) | AI system life cycle processes | Published | Defines the AI system life cycle (built on 15288/12207) — the process backbone that V&V, data-quality and impact-assessment work hang off. |
| [ISO/IEC 42001:2023](https://www.iso.org/standard/42001) | AI management system | Published | Anchor for responsible AI governance — internal audit, management review and continual improvement. World's first AI management system standard. |
| [ISO/IEC AWI 42003](https://www.iso.org/standard/91021.html) | Implementation guidance for ISO/IEC 42001 | Under development (AWI) | Practical AIMS implementation guidance; early stage (preparatory). Likely a key implementation playbook once published. |
| [ISO/IEC 42005:2025](https://www.iso.org/standard/42005) | AI system impact assessment | Published | Maps directly to use-case triage, impact assessment, benefits/harms and risk evidence; Annex A maps to ISO/IEC 42001. |
| [ISO/IEC 42006:2025](https://www.iso.org/standard/42006) | Requirements for bodies auditing/certifying AIMS | Published | Published (Jul 2025) — turns AI management systems into a certification and assessor-competence conversation. Builds on ISO/IEC 17021-1. |
| [ISO/IEC DIS 42007](https://www.iso.org/standard/89967.html) | AI conformity assessment schemes | Under development (DIS) | DIS ballot registered Jun 2026. May shape AI assurance market models beyond management-system certification; supplementary to ISO/IEC 17067. |
| [ISO/IEC TS 42119-2:2025](https://www.iso.org/standard/84127.html) | Testing of AI systems (overview) | Published | First publication in the AI-testing series; relevant to model/system validation, QA, safety, robustness and assurance evidence. |
| [ISO/IEC DTS 42119-3.2](https://www.iso.org/standard/85072.html) | Verification and validation analysis of AI systems | Under development (DTS) | High value for model assurance and AI lifecycle testing once published; currently at draft TS ballot. |
| [ISO/IEC 5259-5:2025](https://www.iso.org/standard/84150.html) | Data quality governance framework (analytics/ML) | Published | Useful for AI data governance, training-data quality and auditability. |
| [ISO/IEC TR 5259-6:2026](https://www.iso.org/standard/86532.html) | Data quality visualisation framework | Published | Technical Report (May 2026); useful where AI data observability or reporting is in scope. |
| [ISO/IEC 12792:2025](https://www.iso.org/standard/84111.html) | Transparency taxonomy of AI systems | Published | Relevant to explainability, transparency statements, public-sector AI and user-facing disclosure (e.g. EU AI Act Art. 13). |
| [ISO/IEC TS 6254:2025](https://www.iso.org/standard/82148.html) | Explainability and interpretability of ML/AI | Published | Technical Specification (Sep 2025); objectives and approaches for explainability — useful for responsible AI control design and assurance language. |
| [ISO/IEC TR 5469:2024](https://www.iso.org/standard/81283.html) | Functional safety and AI systems | Published | Bridges AI with classical functional safety (IEC 61508, ISO 26262); high value for clients deploying AI in safety-related functions. |
| [ISO/IEC DIS 42105](https://www.iso.org/standard/86902.html) | Guidance for human oversight of AI systems | Under development (DIS) | High newsletter value; aligns with public-sector responsible AI and EU-style control expectations. (iso.org shows DIS; a national mirror shows FDIS — re-check.) |
| [ISO/IEC CD TS 25568](https://www.iso.org/standard/90754.html) | Guidance on risks in generative AI systems | Under development (CD) | Track for agentic AI, public LLMs, prompt injection, model governance and procurement advice. |
| [ISO/IEC AWI 25870](https://www.iso.org/standard/91804.html) | Data elements for reporting AI system incidents | Under development (AWI) | Connects AI governance with incident, breach, safety and regulator reporting; early stage. |
| [ISO/IEC AWI TS 25864](https://www.iso.org/standard/91831.html) | Resilience assessment of AI systems | Under development (AWI) | Model/system resilience framing alongside cyber resilience; early stage (SC 42/WG 3). |

## Newsletter candidates

- [CRITICAL ALERT: Active exploitation of cPanel/WHM critical vulnerability](https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/active-exploitation-of-cpanel-whm-critical-vulnerability) — ASD ACSC — Alerts & advisories (High)
- [Preparing for a ‘vulnerability patch wave’](https://www.ncsc.gov.uk/blogs/prepare-for-vulnerability-patch-wave) — UK NCSC — All updates (High)
- [Preparing for severe cyber threat: why leaders must act now](https://www.ncsc.gov.uk/blogs/preparing-for-severe-cyber-threat-why-leaders-must-act-now) — UK NCSC — All updates (High)
- [HIGH ALERT: Ongoing targeting of online code repositories](https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/ongoing-targeting-of-online-code-repositories) — ASD ACSC — Alerts & advisories (High)

## Source health

- OK — ASD ACSC — Alerts & advisories: 4 items
- OK — UK NCSC — All updates: 20 items
- OK — NIST — Cybersecurity news: 0 items
- FAIL — CISA — Cybersecurity advisories: <HTTPError 403: 'Forbidden'>
- OK — APRA — News & publications: 10 items
- MANUAL — OAIC — News & privacy guidance: manual source — not auto-fetched
- MANUAL — ASIC — Media & guidance: manual source — not auto-fetched
- MANUAL — ACCC — News: manual source — not auto-fetched
- MANUAL — ACMA — News & media: manual source — not auto-fetched
- MANUAL — Home Affairs — Critical infrastructure / cyber: manual source — not auto-fetched
- MANUAL — Attorney-General's Department — Privacy reform: manual source — not auto-fetched
- MANUAL — Digital Transformation Agency — AI in government: manual source — not auto-fetched
- MANUAL — Dept of Finance / DTA — AI assurance framework: manual source — not auto-fetched
- MANUAL — ISO/IEC JTC 1/SC 27 — Information security: manual source — not auto-fetched
- MANUAL — ISO/IEC JTC 1/SC 42 — Artificial intelligence: manual source — not auto-fetched
- MANUAL — ISO/IEC 42001 — AI management system: manual source — not auto-fetched
- MANUAL — ISO/IEC 27001 — ISMS: manual source — not auto-fetched
- MANUAL — Standards Australia — Updates: manual source — not auto-fetched
- MANUAL — ENISA — News & publications: manual source — not auto-fetched
- OK — Schneier on Security: 10 items
- MANUAL — OECD.AI — Policy observatory: manual source — not auto-fetched

---

_If your organisation is preparing for ISO/IEC 27001, ISO/IEC 42001, cyber assurance or responsible AI governance, I can help you separate what matters from what is noise — and build an evidence-based path forward._

