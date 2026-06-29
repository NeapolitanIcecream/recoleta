---
source: arxiv
url: https://arxiv.org/abs/2606.23130v1
published_at: '2026-06-22T10:19:07'
authors:
- Junquan Deng
- Zhiyu Fan
- Ruijie Meng
topics:
- vibe-coding-security
- llm-agents
- code-intelligence
- software-security
- human-ai-interaction
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Understanding the (In)Security of Vibe-Coded Applications

## Summary
This paper studies security bugs in applications built mostly by AI coding agents through vibe coding. It builds a corpus of 10,517 such apps and validates 1,471 exploitable vulnerabilities in a random sample of 200 deployed web apps.

## Problem
- Vibe coding lets users create and deploy full applications through natural-language instructions, often with little code review or security knowledge.
- Security decisions move to AI agents that choose architecture, authentication, input handling, database access, and deployment settings.
- A repeated agent mistake can spread across many public apps, so the risk matters beyond one repository.

## Approach
- The authors collect GitHub repositories with agent fingerprints from Claude Code and Lovable, then filter for application-like projects with enough documentation, code, and commit history.
- They classify a repository as vibe-coded when the first commit is AI-authored and both AI-authored commits and AI-authored code lines exceed 85%.
- They focus vulnerability analysis on deployed web apps, since 9,935 of 10,517 collected apps are web apps.
- For 200 randomly sampled deployed web apps, they run four audit setups: Claude Code with Claude Sonnet 4.6 and GitHub Copilot with GPT-5.3-Codex, each paired with two security skill sets.
- They deduplicate agent reports, use an exploitability-checking agent, then require two security reviewers to confirm each vulnerability and assign OWASP severity and category.

## Results
- The VibeApps corpus contains 10,517 vibe-coded applications, selected from 74,800 candidate repositories and 37,962 higher-quality application repositories.
- Web apps dominate the corpus: 9,935 of 10,517 apps, or 94.5%, are web applications; 1,226 of all apps, or 11.7%, have validated reachable deployment links.
- The sampled audit covers 200 deployed web apps from 1,170 reachable deployed web apps and produces 9,353 raw reports, reduced to 1,934 candidates, 1,513 potential vulnerabilities, and 1,471 validated vulnerabilities.
- Human validation reports strong agreement, with Cohen’s kappa of 0.87 between two security reviewers.
- The paper reports recurring vulnerability types including broken access control, cryptographic failures, injection, secret exposure, placeholder logic, and unfiltered input; the excerpt does not provide per-category counts.
- The corpus shows fast, large app creation: the median repository has 8,351 lines of code across 101 files, the median development span is 9.8 days, 94.5% exceed 5,000 lines of code, and 66.3% are developed in under 30 days.

## Link
- [https://arxiv.org/abs/2606.23130v1](https://arxiv.org/abs/2606.23130v1)
