---
kind: trend
trend_doc_id: 1604
granularity: day
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-23T00:00:00'
topics:
- LLM agents
- coding agents
- enterprise benchmarks
- procedural memory
- software security
- context recovery
- SysML
- Text-to-SQL
run_id: materialize-outputs
aliases:
- recoleta-trend-1604
tags:
- recoleta/trend
- topic/llm-agents
- topic/coding-agents
- topic/enterprise-benchmarks
- topic/procedural-memory
- topic/software-security
- topic/context-recovery
- topic/sysml
- topic/text-to-sql
language_code: en
pass_output_id: 276
pass_kind: trend_synthesis
---

# Agent research is putting workplace delivery, context recovery, and security evidence on the same scorecard

## Overview
The day’s strongest work treats large language model (LLM) agents as production systems that need task context, reusable procedures, and security checks. DeepDiscovery, EnterpriseClawBench, and AFTER give the clearest evidence, with concrete tasks, artifacts, and transfer tests.

## Clusters

### Repository context for coding agents
DeepDiscovery targets a common failure in coding agents: finding the obvious file while missing registration code, configuration links, tests, or dependency-injection paths. Its Location-Inference method starts with high-confidence task anchors, then expands over explicit dependencies, implicit configuration links, and module proximity under a budget.

The reported gains are practical. In industrial repositories with 2.67 million lines of code and more than 25,000 files, it improves Full Recall Rate by 2.5 to 7.4 percentage points on medium tasks and 1.6 to 9.2 points on large-subproject tasks. On SWE-bench Verified, the equipped system reaches a 78.6% solve rate, 8.2 points above its baseline.

#### Evidence
- [From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases](../Inbox/2026-06-22--from-fragments-to-paths-task-level-context-recovery-for-large-industrial-codebases.md): DeepDiscovery method, industrial repository scale, file-recovery gains, and SWE-bench Verified result.

### Workplace benchmarks with artifacts and reusable skills
EnterpriseClawBench turns internal enterprise sessions into reproducible tasks with files, expected deliverables, role labels, rules, and text or visual rubrics. The best Lite score is 0.663 across 32 harness-model combinations, which leaves many artifact-delivery and content-quality failures visible. The benchmark also reports cost, runtime, tool calls, and harness-model pairings, so a base model score cannot hide execution problems.

AFTER studies procedural memory as versioned skill files. Static skills add 2.8 accuracy points on average, and one refinement round adds 3.7 to 6.7 points. Skills trained on diverse multi-model traces reach 73.1% cross-model test accuracy, while narrow skill updates can lose accuracy when moved across roles.

#### Evidence
- [EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions](../Inbox/2026-06-22--enterpriseclawbench-benchmarking-agents-from-real-workplace-sessions.md): EnterpriseClawBench construction pipeline, scoring dimensions, Lite score, and harness-model results.
- [Managing Procedural Memory in LLM Agents: Control, Adaptation, and Evaluation](../Inbox/2026-06-22--managing-procedural-memory-in-llm-agents-control-adaptation-and-evaluation.md): AFTER task set, procedural skill evaluation, refinement gains, cross-model transfer, and cross-role failures.

### Security evidence for AI-built software
The vibe-coding security study supplies the largest warning signal in the period. The authors collect 10,517 mostly AI-authored applications and audit 200 deployed web apps. Human reviewers validate 1,471 exploitable vulnerabilities after deduplication and exploitability checks. Repeated bug types include broken access control, cryptographic failures, injection, secret exposure, placeholder logic, and unfiltered input.

EVerest adds a different kind of security evidence: a public dataset linking requirements, architecture, documentation, and code for an electric-vehicle charging stack. It contains 84 security requirements and 1,445 fine-grained labels. During construction, the authors found and disclosed a real CWE-1295 plain-text token storage weakness.

#### Evidence
- [Understanding the (In)Security of Vibe-Coded Applications](../Inbox/2026-06-22--understanding-the-in-security-of-vibe-coded-applications.md): VibeApps corpus size, deployed-app audit process, validated vulnerability count, and recurring vulnerability types.
- [The EVerest Dataset for Secure Software Engineering](../Inbox/2026-06-22--the-everest-dataset-for-secure-software-engineering.md): EVerest dataset contents, traceability labels, architecture coverage, and discovered CWE-1295 weakness.

### Domain context and human review in specialized engineering tasks
The SysML v2 fault-localization paper shows how small code models can improve when domain rules are supplied as training data and inference context. A vehicle-domain knowledge graph encodes physical interface and unit-compatibility rules, then guides synthetic fault generation and repair prompts. On the reported evaluation set, Qwen2.5 Coder 1.5B records 95.7% semantic repair accuracy with fine-tuned full-code output and 91.9% with patch output; its baseline semantic repair accuracy is 0.62%.

WisdomAI’s Text-to-SQL post makes a related production claim for enterprise analytics. Its Adaptive Context Engine builds and updates business context using schemas, logs, dbt, LookML, knowledge bases, feedback, and admin review. On five filtered LiveSQLBench query-only datasets, the reported aggregate accuracy is 20% at baseline, 50% after adding knowledge files, and 85% after context learning.

#### Evidence
- [Automated Semantic Fault Localization in SysML v2: A Human-in-the-Loop Framework Using Knowledge-Graph Augmented LLMs](../Inbox/2026-06-22--automated-semantic-fault-localization-in-sysml-v2-a-human-in-the-loop-framework-using-knowledge-graph-augmented-llms.md): SysML v2 knowledge graph method, synthetic data setup, fine-tuning setup, semantic repair accuracy, and patch-token results.
- [What it takes to get high Text-to-SQL accuracy in production](../Inbox/2026-06-22--what-it-takes-to-get-high-text-to-sql-accuracy-in-production.md): Adaptive Context Engine inputs, context-learning loop, and reported Text-to-SQL accuracy results.
