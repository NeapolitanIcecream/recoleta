---
kind: trend
trend_doc_id: 898
granularity: day
period_start: '2026-05-08T00:00:00'
period_end: '2026-05-09T00:00:00'
topics:
- coding agents
- software engineering benchmarks
- formal verification
- agent governance
- repository automation
run_id: materialize-outputs
aliases:
- recoleta-trend-898
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/formal-verification
- topic/agent-governance
- topic/repository-automation
language_code: en
pass_output_id: 136
pass_kind: trend_synthesis
---

# Coding agents are being judged on restraint, proofs, and repository discipline

## Overview
Coding-agent research is testing decision quality under executable checks. FixedBench measures when agents should leave code untouched. SWE Atlas scores everyday repository work. VeriContest shows that ordinary code generation still falls short of machine-checked correctness.

## Findings

### Abstention and engineering-quality benchmarks
FixedBench targets a failure mode that normal issue-resolution scores miss: agents edit code after the correct patch has already been applied. In the main resolved setting, agents still made unwanted executable-code edits in 35% to 65% of cases. A direct “Abstain or Fix” prompt improved abstention for some models, but it also caused harmful inaction on partially fixed issues.

SWE Atlas widens evaluation to codebase Q&A, test writing, and refactoring across 18 active repositories. Its rubric checks expose quality gaps after functional tests pass. Top native-scaffold results stay near the low 40s in Pass@1, and best Pass³ values reach only 29.2, so consistency remains a clear bottleneck.

#### Sources
- [Coding Agents Don't Know When to Act](../Inbox/2026-05-08--coding-agents-don-t-know-when-to-act.md): FixedBench design, abstention rates, prompt effects, and partial-fix failure mode.
- [SWE Atlas: Benchmarking Coding Agents Beyond Issue Resolution](../Inbox/2026-05-08--swe-atlas-benchmarking-coding-agents-beyond-issue-resolution.md): SWE Atlas task categories, repository scope, Pass@1 and Pass³ results, and rubric-quality gaps.

### Formal verification exposes the proof bottleneck
VeriContest gives coding models a stricter target: generate Rust/Verus code, specifications, and machine-checkable proofs for 946 competitive-programming problems. The benchmark includes expert-validated specifications, judge-accepted Rust code, checked proofs, and large positive and negative test suites.

The results separate code fluency from verified correctness. GPT-5.5 reaches 92.18% pass@1 on natural-language-to-code generation, then drops to 48.31% on specification generation, 13.95% on proof generation, and 5.29% end-to-end verified generation. All evaluated models stay below 6% end-to-end.

#### Sources
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): VeriContest dataset construction, task counts, verification artifacts, and pass@1 results.

### Repository agents need better action credit and prepared context
The CLI (command-line interface) agent paper treats shell work as a structured action sequence. A3 parses shell commands into abstract syntax tree signatures, shares credit across similar actions, and combines that with σ-Reveal, which selects an initial file-tree view under a token budget. On ShellOps exact-match string tasks, A3 with σ-Reveal scores 48.5%, while the strongest non-A3 baseline shown scores 27.5%.

A separate GitHub dataset shows how teams already prepare repositories for agents. It contains 15,591 configuration artifacts across 4,738 repositories, covering context files, skills, subagents, commands, rules, settings, hooks, and Model Context Protocol configurations. Context files dominate the sample, with 9,470 artifacts across 4,463 repositories.

#### Sources
- [Learning CLI Agents with Structured Action Credit under Selective Observation](../Inbox/2026-05-08--learning-cli-agents-with-structured-action-credit-under-selective-observation.md): A3, σ-Reveal, ShellOps scope, and reported performance on multi-turn filesystem tasks.
- [A Dataset of Agentic AI Coding Tool Configurations](../Inbox/2026-05-08--a-dataset-of-agentic-ai-coding-tool-configurations.md): Repository-level agent configuration dataset, tool coverage, artifact counts, and mechanism breakdown.

### Agent deployment research is pinning down control points
Security and governance papers focus on where constraints must sit during execution. The subagent-inheritance study reports four vulnerability classes in multi-agent systems: unrestricted memory inheritance, missing resource access control, asynchronous memory divergence, and unauthorized cross-agent termination. The authors describe working proof-of-concept exploits against stock OpenClaw and checks across additional vendors.

SARC places constraints inside the agent loop through pre-action gates, action-time monitors, post-action auditors, and escalation routing. In a synthetic procurement task over 50 seeds, it reports zero hard-constraint violations under exact predicates and an 89.5% reduction in soft-window overages against a policy-as-code-only baseline.

Pull-request evidence adds an operational boundary. In 29,585 AI-agent-related GitHub PRs, agents often initiate work for some tools, yet agent-approved PRs total only 14 and stay below 0.1% per tool. Human merge authority remains the norm in this dataset.

#### Sources
- [When Child Inherits: Modeling and Exploiting Subagent Spawn in Multi-Agent Networks](../Inbox/2026-05-08--when-child-inherits-modeling-and-exploiting-subagent-spawn-in-multi-agent-networks.md): Subagent inheritance threat model, vulnerability classes, tested systems, and exploit claims.
- [SARC: A Governance-by-Architecture Framework for Agentic AI Systems](../Inbox/2026-05-08--sarc-a-governance-by-architecture-framework-for-agentic-ai-systems.md): SARC runtime control sites and synthetic procurement results.
- [Collaborator or Assistant? How AI Coding Agents Partition Work Across Pull Request Lifecycles](../Inbox/2026-05-08--collaborator-or-assistant-how-ai-coding-agents-partition-work-across-pull-request-lifecycles.md): GitHub PR lifecycle study, agent initiation patterns, and human merge authority findings.
