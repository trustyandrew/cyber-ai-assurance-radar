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
    "id": "b3526f078f3c5a01",
    "title": "The AI shift in cyber risk: why leaders must act now",
    "source": "UK NCSC — All updates",
    "lens": "ResponsibleAI",
    "url": "https://www.ncsc.gov.uk/news/the-ai-shift-in-cyber-risk-why-leaders-must-act-now",
    "context": ""
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
    "lens": "CyberResilience",
    "url": "https://www.ncsc.gov.uk/news/ncsc-ceo-hostile-states-linked-to-three-quarters-of-cyber-attacks",
    "context": "Dr Richard Horne highlighted the scale of cyber threats against the UK’s critical infrastructure at RUSI’s Annual Security Lecture."
  },
  {
    "id": "26bcb636d6619c8f",
    "title": "CRITICAL ALERT: Active exploitation of cPanel/WHM critical vulnerability",
    "source": "ASD ACSC — Alerts & advisories",
    "lens": "CyberResilience",
    "url": "https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/active-exploitation-of-cpanel-whm-critical-vulnerability",
    "context": "The Australian Signals Directorate’s Australian Cyber Security Centre (ASD's ACSC) is aware of exploitation of a vulnerability affecting the cPanel/ WebHost Manager (CVE-2026-4194) administration control interfaces for website and server management. This vulnerability has received a CVSS4.0 base score of 9.3."
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
    "id": "6b03dec649841343",
    "title": "Embedding Forbidden Text in Spyware to Discourage AI Analysis",
    "source": "Schneier on Security",
    "lens": "ResponsibleAI",
    "url": "https://www.schneier.com/blog/archives/2026/06/embedding-forbidden-text-in-spyware-to-discourage-ai-analysis-2.html",
    "context": "At least one malware developer is adding text about nuclear and biological weapons to their spyware, in an effort to stop automatic AI analysis. Details : The _index.js payload begins with a large JavaScript block comment containing fake system instructions and policy-triggering content. Because it is inside a comment, it does not affect JavaScript execution. The runtime skips it. The real…"
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
    "id": "a34e5bfa96fafa05",
    "title": "10 questions to ask when using AI models to find vulnerabilities",
    "source": "UK NCSC — All updates",
    "lens": "ResponsibleAI",
    "url": "https://www.ncsc.gov.uk/blogs/10-questions-ask-using-ai-models-find-vulnerabilities",
    "context": "Using Artificial Intelligence to find vulnerabilities can bring added security considerations."
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
    "id": "f3d20af9d2daee2f",
    "title": "Supporting AI adoption for UK cyber defence",
    "source": "UK NCSC — All updates",
    "lens": "ResponsibleAI",
    "url": "https://www.ncsc.gov.uk/blogs/supporting-ai-adoption-for-uk-cyber-defence",
    "context": "Adopting AI will require time, the development of new capabilities and careful oversight."
  },
  {
    "id": "13b8f39d41e90cc0",
    "title": "Cyber chief: UK faces \"perfect storm\" for cyber security",
    "source": "UK NCSC — All updates",
    "lens": "CyberResilience",
    "url": "https://www.ncsc.gov.uk/news/cyber-chief-uk-faces-perfect-storm-for-cyber-security",
    "context": "As the technology landscape develops, the definition of cyber security is expanding with it."
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
    "lens": "CyberResilience",
    "url": "https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/ongoing-targeting-of-online-code-repositories",
    "context": "The Australian Signals Directorate’s Australian Cyber Security Centre (ASD's ACSC) is aware of increased targeting of online code repositories, with threat actors employing various tactics to scan for and extract secrets, access private code bases, and modify packages to infect users. The ASD’s ACSC does not have information to indicate that a specific industry or sector is being targeted, with…"
  },
  {
    "id": "836093ee3cff4a19",
    "title": "AI and Liability",
    "source": "Schneier on Security",
    "lens": "ResponsibleAI",
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
    "id": "ad8704866c5f4a17",
    "title": "Professional Athletes and Wearables",
    "source": "Schneier on Security",
    "lens": "Privacy",
    "url": "https://www.schneier.com/blog/archives/2026/06/professional-athletes-and-wearables.html",
    "context": "I haven’t thought about the privacy issues surrounding professional athletes and wearables. Wearables present serious privacy issues for “Average Joe” consumers, who are entrusting tech companies to safely store and protect their biometric data. Imagine the stakes for a professional athlete, whose entire livelihood could be affected by a single biometric data point. To give one of many realistic…"
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
    "id": "8e875ec5110fcaba",
    "title": "Alert: NCSC issues advice following global targeting of Fortinet firewalls and VPN gateways",
    "source": "UK NCSC — All updates",
    "lens": "CyberResilience",
    "url": "https://www.ncsc.gov.uk/news/advice-following-global-targeting-of-fortinet-firewalls-and-vpn-gateways",
    "context": "Organisations using Fortinet services are being urged to take action following a campaign affecting firewalls and VPN gateways."
  },
  {
    "id": "c6f2968cc3cb337f",
    "title": "The 'vibe coding spectrum' approach to AI-assisted software development",
    "source": "UK NCSC — All updates",
    "lens": "ResponsibleAI",
    "url": "https://www.ncsc.gov.uk/blogs/the-vibe-coding-spectrum-approach-to-ai-assisted-software-development",
    "context": "Different code deserves different levels of oversight, so calibrate your approach to ‘vibe coding’ accordingly."
  },
  {
    "id": "207f823b11cc6557",
    "title": "Embedding Forbidden Text in Spyware to Discourage AI Analysis",
    "source": "Schneier on Security",
    "lens": "ResponsibleAI",
    "url": "https://www.schneier.com/blog/archives/2026/06/embedding-forbidden-text-in-spyware-to-discourage-ai-analysis.html",
    "context": "At least one malware developer is adding text about nuclear and biological weapons to their spyware, in an effort to stop automatic AI analysis. Details : The _index.js payload begins with a large JavaScript block comment containing fake system instructions and policy-triggering content. Because it is inside a comment, it does not affect JavaScript execution. The runtime skips it. The real…"
  },
  {
    "id": "327fdbfc07b8c48c",
    "title": "AI Use by the US Government",
    "source": "Schneier on Security",
    "lens": "ResponsibleAI",
    "url": "https://www.schneier.com/blog/archives/2026/06/ai-use-by-the-us-government.html",
    "context": "On 14 April, the Trump administration quietly acknowledged the widespread use of AI to automate government processes. The office of management and budget (OMB) disclosed a staggering 3,611 active or planned use cases for AI across the federal government. The list has ballooned by 70% from the one published in the final year of the Biden administration, and includes many disturbing-seeming plans…"
  },
  {
    "id": "dbc0e3f164b2e239",
    "title": "Could your choice of metrics be harming your SOC?",
    "source": "UK NCSC — All updates",
    "lens": "CyberResilience",
    "url": "https://www.ncsc.gov.uk/blogs/could-your-choice-of-metrics-be-harming-your-soc",
    "context": "Poor metrics can render a well-intentioned security operation centre entirely ineffective."
  },
  {
    "id": "b4d2cddf82eb0fe3",
    "title": "International cyber agencies share fresh advice to defend against China-linked covert networks",
    "source": "UK NCSC — All updates",
    "lens": "CyberResilience",
    "url": "https://www.ncsc.gov.uk/news/international-cyber-agencies-fresh-advice-defend-against-china-linked-covert-networks",
    "context": "New advisory highlights how to defend against attacker tactics believed to be used by China-linked actors to hide malicious cyber activity."
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
    "id": "58e8a99997d1d6a5",
    "title": "DTA’s new look site now live",
    "source": "Digital Transformation Agency — news",
    "lens": "PublicSector",
    "url": "https://www.dta.gov.au/media-releases/dtas-new-look-site-now-live",
    "context": "DTA’s new look site now live emily.farrelly Tue, 2025-09-02 11:29 The DTA has published a new look corporate site that shares details on our team, our culture, and our latest achievements. We have launched our new look corporate site. It delivers concise details about who we are, our reporting requirements, and our latest achievements. As part of this update, we have separated our corporate…"
  }
]
