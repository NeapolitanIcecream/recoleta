---
kind: trend
trend_doc_id: 2079
granularity: day
period_start: '2026-07-23T00:00:00'
period_end: '2026-07-24T00:00:00'
topics:
- coding agents
- agent evaluation
- reliability harnesses
- human oversight
- neuro-symbolic reasoning
run_id: materialize-outputs
aliases:
- recoleta-trend-2079
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/reliability-harnesses
- topic/human-oversight
- topic/neuro-symbolic-reasoning
language_code: en
pass_output_id: 346
pass_kind: trend_synthesis
---

# Agent evaluation reaches ambiguous projects as reliability moves into the harness

## Overview
After several days centered on executable feedback inside coding loops, today’s evidence broadens the control surface. New benchmarks test agents on incomplete product intent and mixed workplace tasks, while reliability mechanisms deliver memory, logic, and review at defined checkpoints. Results remain early: several studies lack broad quantitative comparisons, and one workflow improves auditability at substantial cost.

## Findings

### Broader coding-agent evaluation
ICAE-Bench tests whether an agent can clarify incomplete requirements and build a repository, rather than solve a fully specified edit. Its 480 tasks span 12 languages; six models across two harnesses still struggled with hidden constraints, boundary cases, and long-horizon integration.

Tencent WorkBuddy Bench extends evaluation across code, web, office, and security work. Its 260 tasks are reverse-engineered and rewritten to reduce recovery through web search, then released with environments and verifiers for auditability. The suite deliberately avoids a single aggregate score because each domain uses a different verification method. Together, the benchmarks make task construction and evaluator design part of the capability claim, not background implementation detail.

#### Sources
- [ICAE-Bench: Evaluating Coding Agents as Interactive Project Builders](../Inbox/2026-07-23--icae-bench-evaluating-coding-agents-as-interactive-project-builders.md): Reports the 480-task, 12-language benchmark and failures on hidden constraints, boundary cases, and long-horizon integration.
- [Tencent WorkBuddy Bench: A Multi-Domain Coding-Agent Benchmark with Contamination-Resistant Task Construction](../Inbox/2026-07-23--tencent-workbuddy-bench-a-multi-domain-coding-agent-benchmark-with-contamination-resistant-task-construction.md): Describes rewritten, contamination-resistant tasks across four work domains and the open evaluation package.

### Reliability as enforced infrastructure
Three systems place critical controls outside the model’s voluntary behavior. Cue-anchored working memory injects scoped facts when files, symbols, or lifecycle events trigger them; the agent made no memory calls in 114 turns under the strongest voluntary control, while harness delivery survived repeated compaction. Euclid-MCP delegates rule deduction to Prolog and returns proof traces, although its reported performance advantage lacks numerical baseline results.

For economic theory, pAI-Econ-claude uses inspectable intermediate records, targeted gates, and human checkpoints where no automatic oracle exists. Blinded evaluators preferred it in four of five matched tasks, but it consumed 4.6 to 18 times the baseline usage allowance. The common finding is bounded: enforced delivery and explicit gates improve traceability and error interception, but they do not establish cheap or general correctness.

#### Sources
- [Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents](../Inbox/2026-07-23--delivery-not-storage-cue-anchored-working-memory-as-a-harness-property-for-coding-agents.md): Reports zero voluntary memory operations in 114 turns, deterministic delivery, and successful delivery across 138 forced compact-resumes.
- [Euclid-MCP: A Model Context Protocol Server for Deterministic Logical Reasoning via Prolog](../Inbox/2026-07-23--euclid-mcp-a-model-context-protocol-server-for-deterministic-logical-reasoning-via-prolog.md): Defines an MCP interface that delegates deduction to SWI-Prolog and exposes proof traces.
- [pAI-Econ-claude: A Gated Human-in-the-Loop Multi-Agent Architecture for AI-Assisted Economic Theory Development](../Inbox/2026-07-23--pai-econ-claude-a-gated-human-in-the-loop-multi-agent-architecture-for-ai-assisted-economic-theory-development.md): Reports four wins in five blinded comparisons, lower failure severity, higher usefulness, and the bounded auditability claim.
