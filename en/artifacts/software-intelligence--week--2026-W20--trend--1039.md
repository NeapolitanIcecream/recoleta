---
kind: trend
trend_doc_id: 1039
granularity: week
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-18T00:00:00'
topics:
- code agents
- agent evaluation
- executable feedback
- software engineering benchmarks
- runtime traces
- agent security
run_id: materialize-outputs
aliases:
- recoleta-trend-1039
tags:
- recoleta/trend
- topic/code-agents
- topic/agent-evaluation
- topic/executable-feedback
- topic/software-engineering-benchmarks
- topic/runtime-traces
- topic/agent-security
language_code: en
pass_output_id: 160
pass_kind: trend_synthesis
---

# Code agents need executable proof, bounded work loops, and auditable traces

## Overview
Code-agent research this week set a higher bar for useful work. SWE-Cycle and SaaSBench score setup, integration, tests, and delivered behavior. Rollout Cards adds reporting discipline for agent runs. The shared demand is simple: agents need evidence that a task was completed under real operating constraints.

## Clusters

### End-to-end software delivery benchmarks
Benchmarks treated coding as a full work cycle. SWE-Cycle asks agents to set up repositories, change code, and write verification tests across 489 GitHub issue instances. Phoenix-bench adds hardware-engineering repositories and executable EDA checks, where agents transfer poorly because domain toolchains and project structure matter. SaaSBench and WebGameBench push the same standard into delivered applications: enterprise SaaS systems and playable browser games are judged by runtime behavior, configuration, and cross-component integration.

#### Evidence
- [SWE-Cycle: Benchmarking Code Agents across the Complete Issue Resolution Cycle](../Inbox/2026-05-13--swe-cycle-benchmarking-code-agents-across-the-complete-issue-resolution-cycle.md): Item summary describing SWE-Cycle as a 489-instance end-to-end GitHub issue benchmark with setup, code changes, and verification tests.
- [Is Agentic AI Ready for Real-World Hardware Engineering? A Deep Dive with Phoenix-bench](../Inbox/2026-05-13--is-agentic-ai-ready-for-real-world-hardware-engineering-a-deep-dive-with-phoenix-bench.md): Item summary describing Phoenix-bench and its executable EDA checks for Verilog/SystemVerilog repository issues.
- [SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering](../Inbox/2026-05-17--saasbench-exploring-the-boundaries-of-coding-agents-in-long-horizon-enterprise-saas-engineering.md): Item summary describing SaaSBench failures around setup, configuration, and cross-component integration.
- [WebGameBench: Requirement-to-Application Evaluation for Coding Agents via Browser-Native Games](../Inbox/2026-05-17--webgamebench-requirement-to-application-evaluation-for-coding-agents-via-browser-native-games.md): Item summary describing WebGameBench evaluation through real-browser playability and requirement satisfaction.

### Executable feedback for training and task design
Several papers used execution results as the source of supervision or task pressure. DuST trains from execution-labeled candidate code produced during test-time scaling. FrontierSmith turns closed coding tasks into open-ended optimization problems, and DIO-Agent uses execution errors during code discovery. Orchard adds reusable sandbox infrastructure so agents can run tasks across software engineering, browser use, and assistant settings. The practical point is consistent: scoring, errors, and sandbox state are becoming part of the data pipeline.

#### Evidence
- [FrontierSmith: Synthesizing Open-Ended Coding Problems at Scale](../Inbox/2026-05-14--frontiersmith-synthesizing-open-ended-coding-problems-at-scale.md): Item summary describing FrontierSmith’s open-ended optimization-style coding problems for training LLM coders.
- [Orchard: An Open-Source Agentic Modeling Framework](../Inbox/2026-05-14--orchard-an-open-source-agentic-modeling-framework.md): Item summary describing Orchard’s Kubernetes-based sandbox infrastructure for agent training across task domains.

### Auditability for benchmarks, traces, and tool access
The week also treated agent scores as objects that need inspection. BenchJack audits benchmarks for reward-hacking paths before normal runs and found exploits across 10 popular benchmarks. Rollout Cards asks agent papers to publish rollout records, views, reporting rules, and omitted fields so scores can be rechecked. Model Context Protocol (MCP) deployments raise the same control issue for enterprise tools: access, permissions, and third-party skills need review paths before agents act in production settings.

#### Evidence
- [Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack](../Inbox/2026-05-12--do-androids-dream-of-breaking-the-game-systematically-auditing-ai-agent-benchmarks-with-benchjack.md): Item summary describing BenchJack exploits across popular agent benchmarks.
- [Rollout Cards: A Reproducibility Standard for Agent Research](../Inbox/2026-05-12--rollout-cards-a-reproducibility-standard-for-agent-research.md): Item summary describing Rollout Cards and the requirement to publish rollout records and reporting rules.
- [Exploiting LLM Agent Supply Chains via Payload-less Skills](../Inbox/2026-05-14--exploiting-llm-agent-supply-chains-via-payload-less-skills.md): Item summary describing payload-less third-party skills that can cause coding agents to generate and run malicious code.

### Verified vulnerability repair loops
Security repair work focused on runtime evidence and reusable repair knowledge. ContraFix compares crashing and safe executions to infer what a patch must enforce, then stores successful repair specifications and input-mutation strategies. MemRepair adds persistent memory for repository-level vulnerability repair and reports gains on SEC-Bench, PatchEval, and Multi-SWE-bench C++. These systems treat past fixes and concrete executions as inputs to the next repair attempt, which makes evaluation depend on trace quality as much as patch text.

#### Evidence
- [ContraFix: Agentic Vulnerability Repair via Differential Runtime Evidence and Skill Reuse](../Inbox/2026-05-17--contrafix-agentic-vulnerability-repair-via-differential-runtime-evidence-and-skill-reuse.md): Item summary describing ContraFix’s paired crashing and safe executions plus stored repair specifications.
- [MemRepair: Hierarchical Memory for Agentic Repository-Level Vulnerability Repair](../Inbox/2026-05-17--memrepair-hierarchical-memory-for-agentic-repository-level-vulnerability-repair.md): Item summary describing MemRepair’s persistent repair memory and reported benchmark gains.
