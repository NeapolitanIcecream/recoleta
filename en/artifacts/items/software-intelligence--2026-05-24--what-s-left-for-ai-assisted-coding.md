---
source: hn
url: https://stephen.bochinski.dev/blog/2026/05/24/whats-left-for-ai-assisted-coding/
published_at: '2026-05-24T22:28:29'
authors:
- sbochins
topics:
- ai-assisted-coding
- code-intelligence
- software-agents
- developer-tools
- human-ai-interaction
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# What's Left for AI-Assisted Coding

## Summary
The piece argues that AI-assisted coding is held back by missing shared memory and safe autonomous testing access, especially on large teams. It matters because agents can write code for clear tasks, but larger projects require stable decisions and proof that changes work.

## Problem
- Agents lose requirements, prior decisions, and team context between sessions, so developers spend time restating information.
- Missing context can lead agents to make wrong assumptions that surface later in the project.
- Agents cannot safely verify many changes on their own because production-like testing requires access across deployment, testing, and permission systems.

## Approach
- Add persistent memory for individual developers so an agent carries requirements and preferences across sessions.
- Add shared team memory so project decisions, constraints, and known requirements are available to the agent.
- Give agents controlled access to deploy, test, and reach production-like environments when verification requires it.
- Handle access through least-privilege controls and escalation paths, since large companies have many access systems and deployment workflows.

## Results
- No quantitative results, datasets, metrics, or baseline comparisons are provided.
- The article identifies 2 missing capabilities for large-scale AI-assisted coding: shared memory and autonomous end-to-end testing.
- It claims agents already perform reasonably on clear tasks when given enough context, but gives no measured success rate.
- It claims that solving both gaps would move engineers toward writing specifications while agents handle downstream coding and verification.

## Link
- [https://stephen.bochinski.dev/blog/2026/05/24/whats-left-for-ai-assisted-coding/](https://stephen.bochinski.dev/blog/2026/05/24/whats-left-for-ai-assisted-coding/)
