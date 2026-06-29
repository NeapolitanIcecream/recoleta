---
source: arxiv
url: https://arxiv.org/abs/2605.08017v2
published_at: '2026-05-08T17:06:54'
authors:
- Young Jo
- Chung
- Safwat Hassan
topics:
- ai-coding-agents
- pull-request-workflows
- code-review
- software-governance
- human-ai-interaction
- empirical-software-engineering
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Collaborator or Assistant? How AI Coding Agents Partition Work Across Pull Request Lifecycles

## Summary
This paper studies 29,585 GitHub pull requests involving OpenAI, Copilot, Devin, Cursor, and Claude Code to measure who starts AI-agent PR work and who merges it. It finds that agents often initiate work in some tools, but humans almost always retain merge authority.

## Problem
- Teams need to know where human oversight belongs when AI coding agents create branches, write code, and submit PRs.
- Prior studies report merge rates, review counts, or productivity, but they do not reconstruct who initiated, reviewed, revised, and merged each PR.
- This matters because agent-led coding can look autonomous while the merge decision remains human-controlled or recorded only as an automation event.

## Approach
- The authors analyze the AIDev dataset: 33,600 raw PRs and 29,585 PRs after excluding 15 without commits and 4,000 without terminal outcomes.
- They classify each actor as Agent or Human using GitHub actor.type plus login patterns such as bot, copilot, devin, cursor, codex, openai, and claude; validation reports 0.36% residual error.
- Each PR is mapped through phases: created, review, revision, merged and closed, or unmerged and closed.
- The core mechanism is simple: identify who made the first commit, identify who executed the merge if one occurred, then assign the PR to one of six Initiator × Approver scenarios.
- They compute per-tool transition probabilities and median times, then compare tool-scenario association with a chi-square test and Cramér's V.

## Results
- Tool identity predicts the interaction pattern: chi-square = 29,817, df = 20, p < 0.001; Cramér's V = 0.50.
- Cursor, Devin, and Copilot fall on the Collaborator side, with at least 96% agent-initiated PRs; OpenAI and Claude fall on the Assistant side, with at least 95.6% human-initiated PRs.
- Merge authority stays human: Agent-Init + Agent-Approved PRs total 14 and stay below 0.1% per tool.
- Review routing differs by tool: Copilot routes 90.3% of PRs through review, Cursor 51.3%, Devin 52.2%, while OpenAI resolves 76.5% directly and Claude 37.6% directly.
- Revision loops are more common for Collaborator tools: Revision-to-Review return rates are 95.5% for Copilot and 72.3% for Devin; median review time is 3.0 h for Copilot, 2.0 h for Devin, and 0.7 h for OpenAI.
- Closure timing varies: median time to unmerged close is 67.8 h for Devin, 0.2 h for Copilot, and 1.4 h for OpenAI.

## Link
- [https://arxiv.org/abs/2605.08017v2](https://arxiv.org/abs/2605.08017v2)
