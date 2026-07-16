---
kind: trend
trend_doc_id: 1588
granularity: day
period_start: '2026-06-21T00:00:00'
period_end: '2026-06-22T00:00:00'
topics:
- agent evaluation
- coding agents
- open weights
- local observability
- cost governance
- architecture boundaries
run_id: materialize-outputs
aliases:
- recoleta-trend-1588
tags:
- recoleta/trend
- topic/agent-evaluation
- topic/coding-agents
- topic/open-weights
- topic/local-observability
- topic/cost-governance
- topic/architecture-boundaries
language_code: en
pass_output_id: 272
pass_kind: trend_synthesis
---

# Agent work is being judged by study tests, boundary checks, and local receipts

## Overview
The day’s clearest signal is accountability around agents. Machine Studying asks whether agents can learn a new corpus before an exam. ANMA, PeekAI, and Lupen make coding-agent behavior easier to block, trace, and audit on local machines.

## Findings

### Corpus expertise evaluation
Machine Studying gives a concrete test for an agent’s ability to prepare on an unseen document corpus before downstream tasks are revealed. The proposed StudyBench covers DSPy code, OpenClaw code, and machine-learning literature. Its metric rewards accuracy at lower inference-token budgets, so an agent that needs many search loops receives less credit.

The early result is cautious. Retrieval-augmented generation, long context, and simple fine-tuning do not reliably create usable corpus expertise. One example shows Qwen3.5-9B improving on DSPy when forced to use 20 search iterations, but the broader point is that accessible evidence can remain unused without better study behavior.

#### Sources
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): Summary of Machine Studying, StudyBench design, expertise metric, and early results.

### Open-weight coding models
Z.ai’s GLM-5.2 release frames open weights as an operational choice for coding-agent teams. The model card claims 753 billion parameters, an MIT license, downloadable weights, and a 1-million-token context window. Those claims matter for groups that need to run agents over large repositories while controlling data handling and access risk.

The benchmark numbers are specific but still vendor-published. Z.ai reports 62.1 on SWE-bench Pro and 81.0 on Terminal-Bench 2.1 with its Terminus-2 run. The stronger evidence is deployment evidence: copied weights are harder to withdraw than hosted API access.

#### Sources
- [China's Z.ai open-sourced a frontier coding model as Washington bans it rival](../Inbox/2026-06-21--china-s-z-ai-open-sourced-a-frontier-coding-model-as-washington-bans-it-rival.md): Summary of GLM-5.2 release, licensing, context length, and benchmark claims.

### Architecture boundaries for cheaper coding agents
ANMA targets a narrow failure mode: coding agents editing across declared module boundaries. Developers write YAML contracts for modules, then `anma sync` generates Claude Code guidance, hooks, backend configs, continuous integration checks, and optional ownership files.

The strongest evidence is on cheaper models. In the Python benchmark, Claude Haiku 4.5 violated boundaries in 13 of 19 plain-repo runs, while ANMA had 0 violations in 20 runs. A TypeScript follow-up reports 18 of 20 control violations and 0 of 20 with ANMA. The authors also state that Claude Opus 4.8 respected the Python boundary without ANMA, which narrows the claim to governance and cheaper-agent use.

#### Sources
- [Show HN: ANMA, boundary contracts for cheaper AI coding agents](../Inbox/2026-06-21--show-hn-anma-boundary-contracts-for-cheaper-ai-coding-agents.md): Summary of ANMA contracts, generated artifacts, language support, and benchmark results.

### Local traces and cost receipts
PeekAI and Lupen both treat agent operations as local records that developers should inspect without uploading sensitive logs. PeekAI instruments Python agent calls through `peekai.init()`, records large language model calls, tool calls, tokens, cost, errors, and replay runs in a local SQLite database. Its demo shows a three-span trace with runtime, token, and cost breakdowns, but no formal benchmark.

Lupen focuses on Claude Code and Codex spending. It reads local JSONL logs, groups activity by session, turn, step, skill group, and sub-agent, then recomputes cost from token counts and public price tables. Its CLI can fail budget or verification checks with exit code 4, which makes cost drift and runaway sessions easier to catch in scripts.

#### Sources
- [Show HN: PeekAI – Local-first observability for Python AI agents](../Inbox/2026-06-21--show-hn-peekai-local-first-observability-for-python-ai-agents.md): Summary of PeekAI local tracing, storage, replay, demo metrics, and lack of formal benchmark.
- [Show HN: Lupen – an itemized, verified receipt for Claude Code and Codex spend](../Inbox/2026-06-21--show-hn-lupen-an-itemized-verified-receipt-for-claude-code-and-codex-spend.md): Summary of Lupen local log parsing, cost recomputation, verification, and budget gates.
