# Enrichment prompt — 2026-06-26

Paste everything below into Claude (Desktop/Pro). Save its JSON reply to `data/_cache/enrichment-in.json`, then run `python src/apply_enrichment.py`.

---

You are an assurance analyst for a boutique cyber security and responsible AI advisory. Audience: an ISO/IEC 27001 and ISO/IEC 42001 lead auditor advising Australian enterprise and public sector clients. Be precise about standards, use Australian English, never fabricate facts, and never invent standard numbers or publication claims. If the input is thin, stay general rather than inventing detail.

For each item, return STRICT JSON: an array of objects with keys id, score, summary, why_it_matters and suggested_action.
- score: integer 1-5 for assurance relevance. 5 = critical (mandatory change, ASD/ISM/Essential Eight expectation, certification/conformity, regulatory obligation, board-level cyber/AI accountability); 4 = high advisory/newsletter value; 3 = useful watch; 2 = low; 1 = ignore. Prefer primary sources and actionable advisories; routine statistics, telco/broadcasting notices and generic news score low.
- summary: <=45 words, factual.
- why_it_matters: 1-2 sentences tying it to cyber/AI assurance, ISO 27001/42001, ASD/ISM/Essential Eight or Australian public sector assurance.
- suggested_action: one imperative sentence.
Output JSON only.

ITEMS:
[
  {
    "id": "26bcb636d6619c8f",
    "title": "CRITICAL ALERT: Active exploitation of cPanel/WHM critical vulnerability",
    "source": "ASD ACSC — Alerts & advisories",
    "lens": "ASD",
    "url": "https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/active-exploitation-of-cpanel-whm-critical-vulnerability",
    "context": "The Australian Signals Directorate’s Australian Cyber Security Centre (ASD's ACSC) is aware of exploitation of a vulnerability affecting the cPanel/ WebHost Manager (CVE-2026-4194) administration control interfaces for website and server management. This vulnerability has received a CVSS4.0 base score of 9.3."
  },
  {
    "id": "1e995fdeb15ded28",
    "title": "Anthropic’s Fable and the State of AI",
    "source": "Schneier on Security",
    "lens": "ResponsibleAI",
    "url": "https://www.schneier.com/blog/archives/2026/06/anthropics-fable-and-the-state-of-ai.html",
    "context": "On June 9th, Anthropic released its Fable generative AI model. Three days later, the US government classified it as a dangerous munition, and used its export-control authority to prohibit any foreign nationals from accessing it. Unable to differentiate between Americans and foreigners, the company shut off access for everyone. The government’s actions won’t help . The problem isn’t any one…"
  },
  {
    "id": "e9d757e534f1f0d2",
    "title": "CRITICAL ALERT: Reported widespread credential exposure affecting Fortinet Firewalls and VPN Gateways",
    "source": "ASD ACSC — Alerts & advisories",
    "lens": "ASD",
    "url": "https://www.cyber.gov.au/about-us/view-all-content/Reported-widespread-credential-exposure-affecting-Fortinet-Firewalls-and-VPN-Gateways",
    "context": "The Australian Signals Directorate’s Australian Cyber Security Centre (ASD's ACSC) is aware of public reporting of a malicious campaign against Fortinet Firewalls and VPN Gateways"
  },
  {
    "id": "6c75dee5fc404218",
    "title": "NCSC CEO: Hostile states linked to three-quarters of cyber attacks affecting UK's critical systems",
    "source": "UK NCSC — All updates",
    "lens": "ASD",
    "url": "https://www.ncsc.gov.uk/news/ncsc-ceo-hostile-states-linked-to-three-quarters-of-cyber-attacks",
    "context": "Dr Richard Horne highlighted the scale of cyber threats against the UK’s critical infrastructure at RUSI’s Annual Security Lecture."
  },
  {
    "id": "78e47568529ad914",
    "title": "Preparing for a ‘vulnerability patch wave’",
    "source": "UK NCSC — All updates",
    "lens": "CyberResilience",
    "url": "https://www.ncsc.gov.uk/blogs/prepare-for-vulnerability-patch-wave",
    "context": "Organisations must act now to prepare for a wave of patches that will address decades of technical debt."
  },
  {
    "id": "d0bc636fd27fbc36",
    "title": "Preparing for severe cyber threat: why leaders must act now",
    "source": "UK NCSC — All updates",
    "lens": "CyberResilience",
    "url": "https://www.ncsc.gov.uk/blogs/preparing-for-severe-cyber-threat-why-leaders-must-act-now",
    "context": "A call to action to collectively build UK resilience."
  },
  {
    "id": "e96386b842920f36",
    "title": "HIGH ALERT: Ongoing targeting of online code repositories",
    "source": "ASD ACSC — Alerts & advisories",
    "lens": "ASD",
    "url": "https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/ongoing-targeting-of-online-code-repositories",
    "context": "The Australian Signals Directorate’s Australian Cyber Security Centre (ASD's ACSC) is aware of increased targeting of online code repositories, with threat actors employing various tactics to scan for and extract secrets, access private code bases, and modify packages to infect users. The ASD’s ACSC does not have information to indicate that a specific industry or sector is being targeted, with…"
  },
  {
    "id": "b3526f078f3c5a01",
    "title": "The AI shift in cyber risk: why leaders must act now",
    "source": "UK NCSC — All updates",
    "lens": "CyberResilience",
    "url": "https://www.ncsc.gov.uk/news/the-ai-shift-in-cyber-risk-why-leaders-must-act-now",
    "context": ""
  },
  {
    "id": "049c8ea23448cce1",
    "title": "Quarterly Superannuation Product Statistics",
    "source": "APRA — News & publications",
    "lens": "Regulation",
    "url": "https://www.apra.gov.au/news-and-publications/quarterly-superannuation-product-statistics",
    "context": "Breadcrumb Home Statistical Publication Quarterly Superannuation Product Statistics Superannuation Published 22 June 2026 Print On this page On this page APRA publishes statistics on the superannuation products on a quarterly basis. The Quarterly Superannuation Product Statistics (QSPS) leverages new reporting standards implemented in Phase 1 of the Superannuation Data Transformation project to…"
  },
  {
    "id": "7149933a07e4fd46",
    "title": "Quarterly Fund-Level Statistics",
    "source": "APRA — News & publications",
    "lens": "Regulation",
    "url": "https://www.apra.gov.au/news-and-publications/quarterly-fund-level-statistics",
    "context": "Breadcrumb Home Statistical Publication Quarterly Fund-Level Statistics Superannuation Published 22 June 2026 Print On this page On this page APRA publishes statistics on superannuation funds on a quarterly basis. In June 2024 APRA released the inaugural quarterly fund-level statistics. The third in a suite of new publications which leverage new reporting standards implemented in Phase 1 of the…"
  },
  {
    "id": "2c7f806049783451",
    "title": "Quarterly Superannuation Industry publication",
    "source": "APRA — News & publications",
    "lens": "Regulation",
    "url": "https://www.apra.gov.au/news-and-publications/quarterly-superannuation-industry-publication",
    "context": "Breadcrumb Home Statistical Publication Quarterly Superannuation Industry publication Superannuation Published 22 June 2026 Print On this page On this page The Quarterly Superannuation Industry Publication (QSIP) contains data on superannuation products, investment options, member demographics and investments. Quarterly Superannuation Industry Publication - March 2026 XLSX 416.78 KB ‧ 22 June…"
  },
  {
    "id": "ad8704866c5f4a17",
    "title": "Professional Athletes and Wearables",
    "source": "Schneier on Security",
    "lens": "Privacy",
    "url": "https://www.schneier.com/blog/archives/2026/06/professional-athletes-and-wearables.html",
    "context": "I haven’t thought about the privacy issues surrounding professional athletes and wearables. Wearables present serious privacy issues for “Average Joe” consumers, who are entrusting tech companies to safely store and protect their biometric data. Imagine the stakes for a professional athlete, whose entire livelihood could be affected by a single biometric data point. To give one of many realistic…"
  },
  {
    "id": "8e875ec5110fcaba",
    "title": "Alert: NCSC issues advice following global targeting of Fortinet firewalls and VPN gateways",
    "source": "UK NCSC — All updates",
    "lens": "CyberResilience",
    "url": "https://www.ncsc.gov.uk/news/advice-following-global-targeting-of-fortinet-firewalls-and-vpn-gateways",
    "context": "Organisations using Fortinet services are being urged to take action following a campaign affecting firewalls and VPN gateways."
  },
  {
    "id": "d1230fe571401997",
    "title": "Software supply chain attacks: check your dependencies",
    "source": "UK NCSC — All updates",
    "lens": "CyberResilience",
    "url": "https://www.ncsc.gov.uk/blogs/software-supply-chain-attacks-check-your-dependencies",
    "context": "Attackers are compromising open-source packages to spread malware. Cyber defenders are asked to review dependencies to reduce risks"
  },
  {
    "id": "e3cf8ffebab07a87",
    "title": "Have your say on the CCA discussion paper",
    "source": "digital.gov.au — digital, data & AI policy",
    "lens": "PublicSector",
    "url": "https://www.digital.gov.au/have-your-say/consultation-CCA",
    "context": "Have your say on the CCA discussion paper Consultation on the CCA discussion paper Have your say on the discussion paper created by the Digital Transformation Agency (DTA) to establish seller eligibility for consideration of future coordinated contracting arrangements (CCAs), also known as single seller arrangements (SSAs). 2/06/2026 - 16/06/26 The consultation carley.frost Tue, 2026-05-26 18:10…"
  },
  {
    "id": "395560d6009eee7a",
    "title": "Thinking carefully before adopting agentic AI",
    "source": "UK NCSC — All updates",
    "lens": "ResponsibleAI",
    "url": "https://www.ncsc.gov.uk/blogs/thinking-carefully-before-adopting-agentic-ai",
    "context": "When it comes to using agentic AI, make sure you can walk before you run."
  },
  {
    "id": "5419f3a314e214b7",
    "title": "HIGH ALERT: New steps for organisations running Cisco Firepower and Secure Firewall products",
    "source": "ASD ACSC — Alerts & advisories",
    "lens": "ASD",
    "url": "https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/new-steps-for-organisations-running-cisco-firepower-and-secure-firewall-products",
    "context": "ASD partners CISA and NCSC have identified new malware affecting Cisco Firepower and Secure Firewall products."
  },
  {
    "id": "1736b123361f4d57",
    "title": "Executive Summary: Defending against China-nexus covert networks of compromised devices",
    "source": "UK NCSC — All updates",
    "lens": "CyberResilience",
    "url": "https://www.ncsc.gov.uk/news/executive-summary-defending-against-china-nexus-covert-networks-of-compromised-devices",
    "context": "Organisations should map and baseline their edge device traffic, especially VPN and remote access connections, and adopt dynamic threat feed filtering that includes known covert network indicators."
  },
  {
    "id": "f20549bc96ecdc16",
    "title": "New cross domain guidance for government, industry and the wider security community",
    "source": "UK NCSC — All updates",
    "lens": "PublicSector",
    "url": "https://www.ncsc.gov.uk/blogs/new-cross-domain-guidance-for-government-industry-and-the-wider-security-community",
    "context": "Ensuring cross domain technologies are better understood - and more easily deployed - across sectors."
  },
  {
    "id": "836093ee3cff4a19",
    "title": "AI and Liability",
    "source": "Schneier on Security",
    "lens": "CyberResilience",
    "url": "https://www.schneier.com/blog/archives/2026/06/ai-and-liability.html",
    "context": "Earlier this month, a German court ruled that Google is liable for its AI search summaries. Rejecting defenses like “users can check for themselves,” and that they generally know “that information generated with AI should not be blindly trusted,” the court held that the AI’s summaries are reflections of the company and “above all an expression of Google’s business activities.” This is the latest…"
  },
  {
    "id": "9a25c67747344fc8",
    "title": "Interesting Paper Exploring Prompt Injection",
    "source": "Schneier on Security",
    "lens": "CyberResilience",
    "url": "https://www.schneier.com/blog/archives/2026/06/interesting-paper-exploring-prompt-injection.html",
    "context": "This is a fascinating explotation of how LLMs fall for prompt injection attacks. It turns out that they learn to recognize the style of text in different role/instruction blocks, and not just the tags. Their conclusion: Role tags were a formatting trick that became the security architecture and the cognitive scaffolding of modern LLMs. We’ve shown that this architecture doesn’t survive into the…"
  },
  {
    "id": "6b03dec649841343",
    "title": "Embedding Forbidden Text in Spyware to Discourage AI Analysis",
    "source": "Schneier on Security",
    "lens": "CyberResilience",
    "url": "https://www.schneier.com/blog/archives/2026/06/embedding-forbidden-text-in-spyware-to-discourage-ai-analysis-2.html",
    "context": "At least one malware developer is adding text about nuclear and biological weapons to their spyware, in an effort to stop automatic AI analysis. Details : The _index.js payload begins with a large JavaScript block comment containing fake system instructions and policy-triggering content. Because it is inside a comment, it does not affect JavaScript execution. The runtime skips it. The real…"
  },
  {
    "id": "ccd5d6489330c69f",
    "title": "Anthropic’s Fable 5 Model Jailbroken Within Days",
    "source": "Schneier on Security",
    "lens": "CyberResilience",
    "url": "https://www.schneier.com/blog/archives/2026/06/anthropics-fable-5-model-jailbroken-within-days.html",
    "context": "Fable 5 is the supposed safe version of Anthropic’s Mythos Preview, with guardrails to ensure that it can’t be used to create cyberattacks. Well, that restriction was bypassed within days."
  },
  {
    "id": "41f3f0e26725b16f",
    "title": "Friday Squid Blogging: Victims of Unregulated Squid Fishing",
    "source": "Schneier on Security",
    "lens": "CyberResilience",
    "url": "https://www.schneier.com/blog/archives/2026/06/friday-squid-blogging-victims-of-unregulated-squid-fishing.html",
    "context": "Dolphins, sharks, turtles, and human workers are all victims of unregulated squid fishing fleets. Another news article . As usual, you can also use this squid post to talk about the security stories in the news that I haven’t covered. Blog moderation policy."
  },
  {
    "id": "c6f2968cc3cb337f",
    "title": "The 'vibe coding spectrum' approach to AI-assisted software development",
    "source": "UK NCSC — All updates",
    "lens": "CyberResilience",
    "url": "https://www.ncsc.gov.uk/blogs/the-vibe-coding-spectrum-approach-to-ai-assisted-software-development",
    "context": "Different code deserves different levels of oversight, so calibrate your approach to ‘vibe coding’ accordingly."
  },
  {
    "id": "327fdbfc07b8c48c",
    "title": "AI Use by the US Government",
    "source": "Schneier on Security",
    "lens": "PublicSector",
    "url": "https://www.schneier.com/blog/archives/2026/06/ai-use-by-the-us-government.html",
    "context": "On 14 April, the Trump administration quietly acknowledged the widespread use of AI to automate government processes. The office of management and budget (OMB) disclosed a staggering 3,611 active or planned use cases for AI across the federal government. The list has ballooned by 70% from the one published in the final year of the Biden administration, and includes many disturbing-seeming plans…"
  },
  {
    "id": "72c95cc1ca5f710a",
    "title": "Proposed apparatus licensing arrangements for rail services in the 1800 MHz band",
    "source": "ACMA — News & media",
    "lens": "Regulation",
    "url": "https://www.acma.gov.au/consultations/2026-06/proposed-apparatus-licensing-arrangements-rail-services-1800-mhz-band",
    "context": "Proposed apparatus licensing arrangements for rail services in the 1800 MHz band Andrew.Wallace… Tue, 2026-06-16 14:55 Status Open Closing in 27 days ( 22 July 2026 ) In progress Key documents download pdf Consultation paper: New apparatus licensing arrangements for 1800 MHz band rail services [pdf, 319.49 KB] download docx Draft RALI MS34 [docx, 667.31 KB] The issue As part of the expiring…"
  },
  {
    "id": "db030d1451835fef",
    "title": "Cost recovery arrangements for marine radio",
    "source": "ACMA — News & media",
    "lens": "Regulation",
    "url": "https://www.acma.gov.au/consultations/2026-06/cost-recovery-arrangements-marine-radio",
    "context": "Cost recovery arrangements for marine radio Andrew.Wallace… Thu, 2026-06-11 09:39 Status Open Closing in 11 days ( 06 July 2026 ) In progress Key documents download pdf Draft Cost Recovery Implementation Statement: Maritime certificates of proficiency, handbooks and associated administrative services for the calendar year 2026 [pdf, 305.73 KB] The issue We have prepared a draft Cost Recovery…"
  },
  {
    "id": "4209ded7f2318687",
    "title": "Proposal to remake the Radiocommunications (Aircraft and Aeronautical Mobile Stations) Class Licence 2016",
    "source": "ACMA — News & media",
    "lens": "Regulation",
    "url": "https://www.acma.gov.au/consultations/2026-06/proposal-remake-radiocommunications-aircraft-and-aeronautical-mobile-stations-class-licence-2016",
    "context": "Proposal to remake the Radiocommunications (Aircraft and Aeronautical Mobile Stations) Class Licence 2016 peter.watts Tue, 2026-06-09 10:09 Status Open Closing in 26 days ( 21 July 2026 ) In progress Key documents download pdf Consultation paper: Proposal to remake the Radiocommunications (Aircraft and Aeronautical Mobile Stations) Class Licence 2016 [pdf, 239.74 KB] download pdf Draft…"
  },
  {
    "id": "b1afd7ff1062b817",
    "title": "Review of the 2.5 GHz band spectrum licence technical framework",
    "source": "ACMA — News & media",
    "lens": "Regulation",
    "url": "https://www.acma.gov.au/consultations/2026-06/review-25-ghz-band-spectrum-licence-technical-framework",
    "context": "Review of the 2.5 GHz band spectrum licence technical framework Andrew.Wallace… Thu, 2026-06-04 11:55 Status Open Closing in 13 days ( 08 July 2026 ) In progress Key documents download pdf Consultation paper: Review of the 2.5 GHz band spectrum licence technical framework [pdf, 1.02 MB] download pdf Draft Radiocommunications Advisory Guidelines (Managing Interference from Spectrum Licensed…"
  }
]
