---
kind: ideas
granularity: day
period_start: '2026-05-31T00:00:00'
period_end: '2026-06-01T00:00:00'
run_id: de086bd3-22dd-425a-8e8b-efdc6623baee
status: succeeded
topics:
- coding agents
- token efficiency
- workflow automation
- LLM-assisted software
- domain modeling
tags:
- recoleta/ideas
- topic/coding-agents
- topic/token-efficiency
- topic/workflow-automation
- topic/llm-assisted-software
- topic/domain-modeling
language_code: en
pass_output_id: 219
pass_kind: trend_ideas
upstream_pass_output_id: 218
upstream_pass_kind: trend_synthesis
---

# Repository-Scale Coding Agent Governance

## Summary
Coding-agent adoption is getting practical support at the repo boundary: smaller startup context, code maps, usage logs, explicit workflow files, and review practices that protect domain vocabulary. The concrete work is to make agent behavior measurable and repeatable before teams trust it on larger code changes.

## Repository setup that caps startup context and measures coding-agent token use
Teams using Claude Code or Cursor can treat token waste as a repo hygiene issue. agent-stack gives a concrete pattern: generate `CLAUDE.md`, `AGENTS.md`, `.claudeignore`, hooks, Cursor rules, skills, and `.agent-stack/graph.md` in one setup step, then log usage through a Stop hook into `.agent-stack/usage.jsonl`.

The most useful part is the code map. It indexes source files and exported symbols so an agent can search one compact file before opening source. The README example claims 142 files and 906 top-level symbols in the map, a `CLAUDE.md` capped at 800 startup tokens, and a measured drop from 12,340 to 7,180 input tokens per day. Those numbers are project claims, so the practical adoption test is simple: run the setup on one active repo, keep the baseline, and compare input tokens per day after a week of normal agent work.

### Evidence
- [Agent-stack – one command to make any repo token-efficient for Claude Code](../Inbox/2026-05-31--agent-stack-one-command-to-make-any-repo-token-efficient-for-claude-code.md): Summarizes generated repo files, code map, usage logging, and the README token reduction claim.
- [Agent-stack – one command to make any repo token-efficient for Claude Code](../Inbox/2026-05-31--agent-stack-one-command-to-make-any-repo-token-efficient-for-claude-code.md): Shows the setup output with 20 generated files, wired hooks, verified setup, and generated code map.
- [Agent-stack – one command to make any repo token-efficient for Claude Code](../Inbox/2026-05-31--agent-stack-one-command-to-make-any-repo-token-efficient-for-claude-code.md): Describes the code map and the agent behavior of grepping the index before opening source files.

## JSON workflows for coding-agent tasks with explicit branch conditions
Agent teams with repeated multi-step work can move the control flow into workflow files. BotCircuits stores each workflow as JSON under `.botcircuits/workflows/`; after loading, the workflow becomes a callable tool. The LLM still handles each `agentAction`, while the runtime follows `start`, `next`, and compiled branch conditions.

This is a fit for tasks where the sequence matters: release checks, support triage, file-generation jobs, or codebase audits that must stop early under known conditions. The README shows an 11-step example with an `end_id` argument controlling early termination, plus a `/workflow add` command that drafts, previews, writes, and registers a workflow without a restart. The missing check is measurement: teams should log task completion, branch accuracy, latency, and token use before calling it safer than a plain agent prompt.

### Evidence
- [New AI Agent Architecture to fix LLM deviations and token costs](../Inbox/2026-05-31--new-ai-agent-architecture-to-fix-llm-deviations-and-token-costs.md): Summarizes BotCircuits’ deterministic workflow engine, JSON workflow files, branch conditions, and lack of benchmark results.
- [New AI Agent Architecture to fix LLM deviations and token costs](../Inbox/2026-05-31--new-ai-agent-architecture-to-fix-llm-deviations-and-token-costs.md): Shows workflows stored under `.botcircuits/workflows/` and registered as callable tools.
- [New AI Agent Architecture to fix LLM deviations and token costs](../Inbox/2026-05-31--new-ai-agent-architecture-to-fix-llm-deviations-and-token-costs.md): Shows workflow creation, preview, file writing, live registration, and direct workflow runs.

## Pull request review for generated code vocabulary and tests
Teams accepting LLM-generated code need review steps for names, boundaries, invariants, and tests. Martin Fowler’s essay frames code as machine instructions and as the conceptual model a team shares. For generated code, the risk is code that runs but introduces words, structures, or abstractions the team cannot explain during maintenance.

A practical change is to add a short generated-code section to pull request review: list any new domain terms, map them to existing bounded contexts or explain the new boundary, identify invariants in tests, and ask the author to remove names that only mirror the prompt. This gives the model better future context and gives reviewers a concrete way to catch cognitive debt before it spreads through the codebase.

### Evidence
- [What Is Code](../Inbox/2026-05-31--what-is-code.md): Summarizes the essay’s claim that LLM-assisted work depends on shared domain meaning, stable abstractions, and tests.
- [What Is Code](../Inbox/2026-05-31--what-is-code.md): Describes concepts, names, boundaries, relationships, and shared vocabulary as the visible conceptual model.
- [What Is Code](../Inbox/2026-05-31--what-is-code.md): Connects domain vocabulary to code structures such as types, interfaces, invariants, and workflows.
