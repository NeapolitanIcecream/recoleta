---
source: hn
url: https://github.com/jsingh6/arch-decision
published_at: '2026-05-30T22:45:31'
authors:
- jsingh2525
topics:
- architecture-decision-records
- code-intelligence
- multi-agent-systems
- claude-code
- software-engineering-agents
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Arch-Decision – A multi-agent architecture tool for Claude Code

## Summary
arch-decision is a Claude Code plugin that turns a GitHub issue, Jira ticket, or plain request into an Architecture Decision Record after codebase analysis and human approval. It targets the time cost that stops teams from recording why architecture choices were made.

## Problem
- Teams often ship architecture decisions without ADRs, so later engineers repeat the same debate when code changes.
- The author says a senior engineer needs 2–4 hours to research the codebase, compare options, and write an ADR.
- The tool matters because ADRs preserve design intent near the code, but manual writing adds enough friction that teams skip it.

## Approach
- The plugin runs inside Claude Code and accepts a GitHub issue URL, Jira text, or plain-language request.
- An 8-phase orchestrator detects language, existing ADRs, and project context; reads the problem; asks clarifying questions; creates options; waits for approval; writes the ADR; and links it back to the source issue.
- In Phase 2, 3 explorer agents run in parallel to inspect prior art, code impact, and constraints.
- In Phase 4, it generates 3 approaches: Minimal, Clean, and Pragmatic.
- A synthesizer combines the agent outputs into a trade-off table and recommendation, then a Phase 6 approval gate blocks file writes until the user signs off.

## Results
- Claimed time reduction: ADR preparation drops from 2–4 hours of senior-engineer work to minutes; the cited run finished in under 5 minutes.
- Case study: on refinedev/refine issue #7338, the tool found prior art in `crudFiltersToColumnFilters`, identified a constraint in `packages/core`, and recommended an `onParse` callback scoped to the antd wrapper.
- Independent comparison: community PR #7385 used the same callback name, scope, and placement as the tool's recommendation, according to the excerpt.
- The system has 8 phases, 3 parallel explorer agents, 3 generated solution options, 1 synthesizer agent, and 1 required human approval gate.
- The excerpt provides no benchmark suite, sample size, accuracy rate, ablation, or controlled comparison against other code agents.

## Link
- [https://github.com/jsingh6/arch-decision](https://github.com/jsingh6/arch-decision)
