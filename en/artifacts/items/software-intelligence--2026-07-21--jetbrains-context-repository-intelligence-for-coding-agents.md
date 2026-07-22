---
source: hn
url: https://blog.jetbrains.com/ai/2026/07/introducing-jetbrains-context-repository-intelligence-for-coding-agents/
published_at: '2026-07-21T23:18:13'
authors:
- monkey_monkey
topics:
- code-intelligence
- coding-agents
- repository-search
- semantic-retrieval
- multi-repository
- software-production
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# JetBrains Context: Repository Intelligence for Coding Agents

## Summary
JetBrains Context adds repository intelligence to coding agents by incrementally indexing code and retrieving relevant implementation knowledge. JetBrains reports lower agent effort, latency, and execution cost across open-source, production-monorepo, and code-localization evaluations, though the excerpt does not provide baseline details or independent validation.

## Problem
- Coding agents often spend substantial time searching repositories, reading files, and launching exploratory agents before they can implement or review changes.
- Limited visibility into APIs, dependencies, implementation patterns, and organization-wide code makes agents less effective on large codebases and can increase review, rework, and token costs.

## Approach
- JetBrains Context incrementally builds a semantic index of each repository and exposes semantic retrieval tools so agents can query concepts and related code instead of relying only on keyword search and repeated file exploration.
- Its multi-repository search lets agents find relevant code, APIs, dependencies, and implementation examples in repositories that are not checked out locally.
- The layer integrates with Claude Code, Codex CLI, and Junie CLI, and is accessible through JetBrains IDEs, Air, VS Code, and other supported editors.
- Agent hooks can automatically pre-index source code; JetBrains states that source code is not stored on its servers.

## Results
- JetBrains evaluated the system on 205 open-source SWE-bench tasks, 175 production-monorepo tasks, and 1,953 code-localization tasks.
- Across these evaluations, JetBrains reports reductions of up to 68% in agent turns, 59% in latency, and 48% in execution cost.
- The reported figures are maximum reductions rather than averages, and the excerpt does not identify the comparison baseline, task-level success changes, or independent evaluation results.
- JetBrains offers the capability in early access at no additional cost for subscribers to its JetBrains AI for Teams and Organizations plans.

## Link
- [https://blog.jetbrains.com/ai/2026/07/introducing-jetbrains-context-repository-intelligence-for-coding-agents/](https://blog.jetbrains.com/ai/2026/07/introducing-jetbrains-context-repository-intelligence-for-coding-agents/)
