---
source: hn
url: https://www.sepo.sh/
published_at: '2026-07-19T22:40:04'
authors:
- liangqiyao99
topics:
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- human-ai-interaction
- agent-memory
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Self-evolving repo for team and coding agent collaboration

## Summary
Sepo turns a GitHub repository into a structured workspace where coding agents answer questions, implement changes, review pull requests, and iterate under human supervision. Its main contribution is persistent, traceable agent work combined with project-specific rubrics and memory.

## Problem
- Coding-agent work on long-horizon tasks can become difficult to trace, verify, and coordinate across humans and agents.
- Teams need a shared record of requests, decisions, reviews, and code changes so that later agent runs can use project context rather than repeat prior work.

## Approach
- Users mention `@sepo-agent` in GitHub issues, pull requests, or discussions; the agent responds in the thread and records work as linked issues, pull requests, and comments.
- Commands such as `/implement`, `/review`, `/fix-pr`, and `/orchestrate` support implementation, rubric-based review, repair, and repeated implement-review-fix loops.
- The system stores agent work on an `agent/memory` branch, distills lessons from discussions and reviews into project rubrics, and uses those rubrics to guide later implementations.
- Large tasks can be split into sub-issues, while scheduled jobs can inspect the repository and propose improvements that humans may review and approve before merging.

## Results
- The provided material reports no quantitative benchmark, accuracy metric, task-completion rate, latency evaluation, or comparison with another coding-agent system.
- It gives concrete workflow claims: a single issue can trigger an implement-review-fix loop, large issues can fan out into sub-issues, and agent changes remain organized as GitHub issues and pull requests.
- The setup is described as a 3-step process: create or install the repository template, install the GitHub App and add a model credential, then mention the agent in an issue.
- The example review identifies missing retry safeguards while checking rubric items and tests, but the excerpt does not report whether the resulting code passed an independent evaluation.

## Link
- [https://www.sepo.sh/](https://www.sepo.sh/)
