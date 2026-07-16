---
kind: trend
trend_doc_id: 1453
granularity: day
period_start: '2026-06-10T00:00:00'
period_end: '2026-06-11T00:00:00'
topics:
- coding agents
- agent governance
- software engineering benchmarks
- LLM security
- code translation
- agent memory
run_id: materialize-outputs
aliases:
- recoleta-trend-1453
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-governance
- topic/software-engineering-benchmarks
- topic/llm-security
- topic/code-translation
- topic/agent-memory
language_code: en
pass_output_id: 244
pass_kind: trend_synthesis
---

# Coding agents need state, measured harnesses, and action gates

## Overview
The day’s strongest signal is that coding agents are being treated as products that need memory, harness accounting, gates, and monitors. PROJECTMEM, Claw-SWE-Bench, and CodeSpear anchor a practical agenda: keep agents stateful, measure the harness, and test safety paths created by code-specific tooling.

## Findings

### Coding-agent harnesses and skills
Claw-SWE-Bench makes the harness itself part of the score. With the same GLM 5.1 model, OpenClaw rises from 19.1% Pass@1 with a minimal adapter to 73.4% with the full adapter. The paper also reports that harness choice changes Pass@1 by up to 27.4 percentage points under fixed models, and its Lite-80 set tracks the full 350-instance benchmark at about 23% of the run cost.

Several companion items treat agent operation as a maintained runtime. Loop-Harness schedules Claude Code runs in isolated git worktrees, then requires a second Claude session to print `VERDICT: PASS` before shipping. Agents All the Way Down favors command-line interface (CLI) agents for product integration and cites a matched task where Model Context Protocol (MCP) used about 35× more tokens than CLI. SkillJuror adds a smaller but useful result: reorganizing the same skill content with Progressive Disclosure improved pass rate from 42.0% to 46.1% across 410 matched trials.

#### Sources
- [Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks](../Inbox/2026-06-10--claw-swe-bench-a-benchmark-for-evaluating-openclaw-style-agent-harnesses-on-coding-tasks.md): Claw-SWE-Bench reports harness, model, Pass@1, Lite-80, and cost results.
- [Loop-Harness](../Inbox/2026-06-10--loop-harness-is-here.md): Loop-Harness describes scheduled agent runs, worktree isolation, verifier gates, and sample operational metrics.
- [Agents All the Way Down; A Methodology for Building Custom AI Agents from Substrate to Production](../Inbox/2026-06-10--agents-all-the-way-down-a-methodology-for-building-custom-ai-agents-from-substrate-to-production.md): Agents All the Way Down gives the five-phase custom-agent method and CLI versus MCP cost examples.
- [SkillJuror: Measuring How Agent Skill Organization Changes Runtime Behavior](../Inbox/2026-06-10--skilljuror-measuring-how-agent-skill-organization-changes-runtime-behavior.md): SkillJuror reports matched trials showing how skill organization changes runtime behavior and pass rate.

### Repository memory and multi-file localization
PROJECTMEM targets a common failure mode in coding sessions: the agent forgets failed fixes and repeats context reconstruction. It stores issues, attempts, fixes, decisions, and notes in an append-only plain-text log, then builds deterministic summaries for the agent. Its `precheck_file(path)` gate warns before edits to paths tied to failed attempts, open issues, or high churn. The paper estimates 5,000 to 20,000 tokens per session for rebuilding project context, though it does not report a controlled task-success benchmark.

Exploration Structure in LLM Agents attacks the file-localization step before patching. On an Ansible slice from SWE-bench Pro, it assigns domain agents to repository regions such as CLI, module utilities, plugins, and docs. The result favors subsystem-parallel search for small models. The same study also shows that bounded input matters: one large source file drops from 29,895 tokens to 719 tokens under bounded context, and a large docs file drops from 14,366 to 121 tokens.

#### Sources
- [PROJECTMEM: A Local-First, Event-Sourced Memory and Judgment Layer for AI Coding Agents](../Inbox/2026-06-10--projectmem-a-local-first-event-sourced-memory-and-judgment-layer-for-ai-coding-agents.md): PROJECTMEM summary covers event-sourced memory, pre-action warnings, token estimates, implementation details, and evaluation limits.
- [Exploration Structure in LLM Agents for Multi-File Change Localization](../Inbox/2026-06-10--exploration-structure-in-llm-agents-for-multi-file-change-localization.md): The multi-file localization paper reports domain-scoped agents, Ansible SWE-bench Pro setup, and token reductions from bounded I/O.

### Runtime governance and agent oversight
Production-agent safety is being specified at the action layer. The five-plane reference architecture checks intent, delegation chains, capability sets, and session state before actions reach enterprise infrastructure. It also proposes stop-anywhere mediation with pause, escalate, narrow, modify, defer, and rollback, plus tamper-evident audit records. The paper’s evidence is mostly structural, with microsecond policy-core timings and no live full-system benchmark.

Two practical variants appear in the same period. agent-gate makes completion fail closed unless all required evidence fields are true, including deterministic checks, independent review, no secrets, human approval for irreversible acts, and an honest receipt. Bootstrapped Monitoring adds a model oversight protocol: a stronger untrusted monitor reviews actions, while a weaker trusted model audits the monitor’s raw chain-of-thought (CoT). The gains depend on access to raw CoT; summarized reasoning sharply weakens detection in the reported tests.

#### Sources
- [A Five-Plane Reference Architecture for Runtime Governance of Production AI Agents](../Inbox/2026-06-10--a-five-plane-reference-architecture-for-runtime-governance-of-production-ai-agents.md): The five-plane architecture summary covers delegated-action risk, stop-anywhere mediation, composite principals, audit records, and evaluation scope.
- [Agent-gate – fail-closed agent gate and tamper-evident receipts as an MCP server](../Inbox/2026-06-10--agent-gate-fail-closed-agent-gate-and-tamper-evident-receipts-as-an-mcp-server.md): agent-gate describes fail-closed gates, required checks, SHA-256 hash-chained receipts, and demo outcomes.
- [Bootstrapped Monitoring: Leveraging Transparent Reasoning to Oversee Stronger AI Agents](../Inbox/2026-06-10--bootstrapped-monitoring-leveraging-transparent-reasoning-to-oversee-stronger-ai-agents.md): Bootstrapped Monitoring reports the three-role protocol, catch-rate examples, and dependence on raw chain-of-thought.

### Code-specific safety and semantic verification
Code generation has its own safety failure path. CodeSpear shows that grammar-constrained decoding (GCD), a technique used to force syntactically valid code, can remove natural-language refusals from the output space. On local models such as Qwen2.5-Coder-7B, the attack reaches an 81.82% average success rate, and across tested models it beats representative jailbreak baselines by more than 30 percentage points on average. CodeShield answers by training harmless code outputs for cases where grammar constraints force code.

Multisage addresses a different code-specific weakness: translation outputs that compile while changing program behavior. It extracts control flow, types, and API signals from the source, generates several semantic views, then filters them with execution validation, code mutations, and cross-view checks before prompting the translator. On HumanEval-X, it reports success-rate gains up to 2.22× over vanilla prompting, with the largest relative gains on smaller models.

#### Sources
- [Grammar-Constrained Decoding Can Jailbreak LLMs into Generating Malicious Code](../Inbox/2026-06-10--grammar-constrained-decoding-can-jailbreak-llms-into-generating-malicious-code.md): CodeSpear summary gives the GCD jailbreak mechanism, evaluated models, attack success rates, benchmarks, and CodeShield mitigation.
- [Enhancing LLM-Based Code Translation with Verified Multi-Semantic Representations](../Inbox/2026-06-10--enhancing-llm-based-code-translation-with-verified-multi-semantic-representations.md): Multisage summary reports semantic extraction, calibration checks, HumanEval-X results, and relative gains by model size.
