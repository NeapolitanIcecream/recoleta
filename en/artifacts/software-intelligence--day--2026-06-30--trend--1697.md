---
kind: trend
trend_doc_id: 1697
granularity: day
period_start: '2026-06-30T00:00:00'
period_end: '2026-07-01T00:00:00'
topics:
- coding agents
- software maintenance
- performance engineering
- C-to-Rust migration
- agent governance
- benchmarking
run_id: materialize-outputs
aliases:
- recoleta-trend-1697
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-maintenance
- topic/performance-engineering
- topic/c-to-rust-migration
- topic/agent-governance
- topic/benchmarking
language_code: en
pass_output_id: 294
pass_kind: trend_synthesis
---

# Coding agents need explicit artifacts before they can earn trust

## Overview
The day’s strongest evidence favors coding agents that bind model output to explicit software artifacts: feature maps, profiling traces, compiler errors, benchmarks, and approval records. FeatX, MOA, and AdaTrans show the clearest gains, while protocol and cost studies expose limits in governance and task economics.

## Clusters

### Repository-scale code editing
FeatX and MOA ask a large language model (LLM) to work through software evidence before editing code. FeatX maps repository features to Java classes and methods, then generates diffs through a three-stage agent. Its study reports a NASA-TLX workload drop from 12.5 to 7.4 against ChatGPT, plus 0.385 F1 for function-level modification localization on 38 commits.

MOA applies the same discipline to memory optimization. It turns profiling traces into validated anti-patterns, static checkers, and patches. On OpenHarmony, it reports 13 anti-patterns, 10,067 detected inefficiencies, 769 generated patches, and 92.5% expert acceptance. These results make the current emphasis clear: agents are strongest when the task surface is narrowed by source maps, runtime traces, and validation loops.

#### Evidence
- [FeatX: Editing Software by Editing Features for Repository-Level Code Evolution](../Inbox/2026-06-30--featx-editing-software-by-editing-features-for-repository-level-code-evolution.md): FeatX summary and reported user-study and localization metrics.
- [MOA: A Profiling-Guided LLM Framework for Memory-Optimization Automation at Codebase Scale](../Inbox/2026-06-30--moa-a-profiling-guided-llm-framework-for-memory-optimization-automation-at-codebase-scale.md): MOA summary, profiling-based process, and OpenHarmony results.

### Compiler-guided migration and Java performance benchmarks
AdaTrans shows how compiler feedback can drive safer C-to-Rust migration. It maps Rust compiler errors to repair templates and documentation, then checks builds and output behavior. On 104 algorithmic problems, it reports 95.51% compilation pass rate, 81.09% solve rate, and 1.19% unsafe file rate.

JETO-Bench gives performance-fix agents a harder Java target. Its collection tool scanned 3,686 repositories and nearly 1.8 million commits, then produced 660 execution-time improvement patches and 91 manually verified executable tasks. OpenHands fixed 13 of those 91 tasks. The benchmark also finds that many Java projects lack tests that demonstrate execution-time improvement, which limits automatic scoring.

#### Evidence
- [AdaTrans: Automated C to Rust Transformation via Error-Adaptive Repair](../Inbox/2026-06-30--adatrans-automated-c-to-rust-transformation-via-error-adaptive-repair.md): AdaTrans method and C-to-Rust migration results.
- [JETO-Bench: A Reproducible Benchmark for Execution Time Improvement Patches in Java](../Inbox/2026-06-30--jeto-bench-a-reproducible-benchmark-for-execution-time-improvement-patches-in-java.md): JETO-Bench collection scale, verified task count, and OpenHands result.

### Agent cost and governance controls
Agent capability is being measured with task cost and decision control in view. Artificial Analysis reports Claude Sonnet 5 at 53 on its Intelligence Index, 6 points above Sonnet 4.6. At max effort, it uses about 40% more output tokens per task and about three times the agentic turns on AA-Briefcase and GDPval-AA, raising measured cost to $2.29 per task at standard pricing.

Governance work adds a second constraint. A protocol study finds that MCP, A2A, ACP, ANP, and ERC-8004 do not fully support any of six governance dimensions: membership, deliberation, voting, dissent preservation, human escalation, and audit/replay. Serval’s Catalyst product points to a product-level answer for one setting: proposed automation changes are staged for review, and teams can require second-person approval before publication.

#### Evidence
- [Claude Sonnet 5: strong agentic performance at a higher cost per task](../Inbox/2026-06-30--claude-sonnet-5-strong-agentic-performance-at-a-higher-cost-per-task.md): Claude Sonnet 5 benchmark, token-use, turn-count, and cost findings.
- [Governance Gaps in Agent Interoperability Protocols: What MCP, A2A, and ACP Cannot Express](../Inbox/2026-06-30--governance-gaps-in-agent-interoperability-protocols-what-mcp-a2a-and-acp-cannot-express.md): Governance gap analysis across agent interoperability protocols.
- [Catalyst: Automating a task forever should be easier than doing it manually once](../Inbox/2026-06-30--catalyst-automating-a-task-forever-should-be-easier-than-doing-it-manually-once.md): Catalyst staging, approval, and automation setup details.

### Code-understanding data and obfuscation tests
Two papers make code-agent evaluation less dependent on clean snippets. CoCoMUT extracts Java method context with callers, callees, class data, documentation, and source-bytecode reconciliation. Across 20 repositories, it emitted 56,512 method-context records and reconciled 97.8% of recognized project call targets to source methods.

The obfuscated-code study tests whether models still follow program behavior when names and control flow are distorted. Reasoning-tuned models track human task difficulty with positive Spearman correlations, while coder and instruction-tuned models show near-zero alignment. Control-flow flattening reduces accuracy as dispatcher complexity rises. This matters for review, audit, reverse engineering, and security work where surface cues may be misleading.

#### Evidence
- [CoCoMUT: A Tool for Code-Context Mining and Automated Dataset Generation](../Inbox/2026-06-30--cocomut-a-tool-for-code-context-mining-and-automated-dataset-generation.md): CoCoMUT extraction method and dataset-quality results.
- [Do Machines Struggle Where Humans Do? LLM and Human Comprehension of Obfuscated Code](../Inbox/2026-06-30--do-machines-struggle-where-humans-do-llm-and-human-comprehension-of-obfuscated-code.md): Obfuscated-code evaluation setup and model-human alignment results.
