---
source: hn
url: https://www.axios.com/2026/04/07/anthropic-mythos-preview-cybersecurity-risks
published_at: '2026-04-07T23:02:18'
authors:
- FergusArgyll
topics:
- cybersecurity
- vulnerability-discovery
- autonomous-agents
- code-intelligence
- model-release-policy
relevance_score: 0.71
run_id: materialize-outputs
language_code: en
---

# Anthropic holds Mythos model due to hacking risks

## Summary
Anthropic is limiting access to Mythos Preview because the model can autonomously find and exploit software vulnerabilities at a level the company treats as dangerous for public release. The piece describes Mythos as a high-end offensive and defensive cybersecurity model, plus Anthropic's controlled rollout plan.

## Problem
- The article focuses on AI systems that can discover and weaponize software flaws faster and at larger scale than human security researchers.
- This matters because a model with strong autonomous bug-finding and exploit-writing ability could help defenders secure code, but it could also help attackers compromise operating systems, browsers, servers, and critical infrastructure.
- Anthropic treats uncontrolled release as a security risk, so the immediate problem is how to use such a model for defense without making offensive misuse easy.

## Approach
- Anthropic built Mythos Preview as an "extremely autonomous" model with advanced reasoning for cybersecurity tasks, aiming for the skill level of an advanced security researcher.
- In simple terms, the model scans software, finds vulnerabilities, reproduces them, and writes proof-of-concept exploits or exploit chains with little human help.
- Instead of public release, Anthropic is giving access to a small set of vetted organizations so they can use it for defensive scanning of their own code and open-source systems.
- The rollout includes Project Glasswing, where major companies such as AWS, Apple, Cisco, Google, Microsoft, Nvidia, Palo Alto Networks, and the Linux Foundation test the model in real security workflows.
- Anthropic is pairing the rollout with safeguards, government briefings, and funding for testers and open-source security groups.

## Results
- Mythos Preview can find "tens of thousands of vulnerabilities," according to Anthropic. The article gives no benchmark table or formal evaluation setup for that claim.
- Anthropic says its previous public model, Opus 4.6, found about **500 zero-days** in open-source software, and Mythos Preview produces far more than that.
- In testing, Mythos Preview found bugs in **every major operating system and web browser**, including flaws believed to be **decades old** that had not been found in repeated human-run security tests.
- The model reproduced vulnerabilities and created proof-of-concept exploits on the **first attempt in 83.1% of cases**.
- Anthropic says the model found several Linux kernel flaws and autonomously chained them to enable **complete control of a Linux machine**.
- In another reported case, the model found a **27-year-old** OpenBSD vulnerability that could let an attacker **remotely crash any machine** running it.

## Link
- [https://www.axios.com/2026/04/07/anthropic-mythos-preview-cybersecurity-risks](https://www.axios.com/2026/04/07/anthropic-mythos-preview-cybersecurity-risks)
