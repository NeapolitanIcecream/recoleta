---
source: arxiv
url: https://arxiv.org/abs/2607.15769v1
published_at: '2026-07-17T08:58:54'
authors:
- Jinjin Gao
- Luyang Li
- Shufen Guo
- Ligang He
- Xiaoning Sun
topics:
- open-source-governance
- coding-agents
- ai-contribution-review
- software-engineering
- human-ai-collaboration
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Making Agent-Mediated Contributions Governable: A Project-Level Governance Manifest for Open-Source AI Collaboration

## Summary
The paper proposes the Agent Governance Manifest (AGM), a repository-hosted framework for making AI-mediated open-source contributions easier to assess under project rules. It shifts evidence preparation toward contributors and agents while preserving maintainer authority over verification and acceptance.

## Problem
- Coding agents can increase the rate of contribution generation faster than maintainers can assess correctness, security, maintainability, evidence, and accountability.
- Existing agent-readable instructions and traceability records do not consistently define contribution-specific risks, evidence obligations, accountability states, or review gates.
- This matters because maintainers must make acceptance decisions with limited review capacity and incomplete information about AI-mediated changes.

## Approach
- The paper distinguishes three governance layers: agent-readability for repository guidance, traceability for recording AI-mediated work, and governability for organizing review under project rules.
- It defines project-side governability infrastructure as rules and decision arrangements covering risk classifications, evidence obligations, accountability, review gates, and maintainer decision rights.
- AGM implements this model as a repository-hosted, machine- and human-readable boundary resource linking contributor-side evidence packages and confirmation declarations with maintainer-side verification gates.
- The study uses a diagnostic audit of 50 public GitHub repositories, followed by reviewer-side and contributor-side evaluations of AGM-supported workflows.

## Results
- The audit examined 50 repositories, 23,237 pull requests, and 19,884 issues; it found widespread general governance artifacts and agent-readable guidance but uneven, fragmented AI-governance cues.
- No audited repository provided a project-wide arrangement that coordinated shared rules, contributor preparation obligations, verification rights, and maintainer decision authority across AI-mediated contribution workflows.
- In the reviewer-side evaluation, 15 participants produced 75 task-level outputs. Exact risk-label recovery was 37/38 with AGM-supported materials versus 15/37 without them.
- Perceived review support increased from 3.27 to 6.14 on a 1–7 scale in the AGM condition.
- In the contributor-side feasibility check, 15 participants completed 45 tasks; all final packages represented the core governance state correctly, and 41 passed strict structural validation.

## Link
- [https://arxiv.org/abs/2607.15769v1](https://arxiv.org/abs/2607.15769v1)
