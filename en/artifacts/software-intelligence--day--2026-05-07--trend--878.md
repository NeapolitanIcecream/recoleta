---
kind: trend
trend_doc_id: 878
granularity: day
period_start: '2026-05-07T00:00:00'
period_end: '2026-05-08T00:00:00'
topics:
- coding agents
- software engineering benchmarks
- repository evaluation
- test evolution
- agent control
- maintainability
run_id: materialize-outputs
aliases:
- recoleta-trend-878
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/repository-evaluation
- topic/test-evolution
- topic/agent-control
- topic/maintainability
language_code: en
pass_output_id: 134
pass_kind: trend_synthesis
---

# Repository-grade coding exposes where agents still break

## Overview
The day’s clearest signal is stricter evaluation for large language model (LLM) software agents. Generated code must satisfy architecture, tests, migrations, and real developer traces. TACT and ASTOR improve control. Repository evidence still shows many agents miss structural and maintenance requirements.

## Findings

### Structural constraints in real codebases
Backend generation, enterprise migration, and architectural repair all show the same weak point: agents can produce runnable code that fails engineering constraints.

Constraint Decay fixes one OpenAPI contract across 80 backend tasks and varies architecture, database, and object-relational mapping requirements. Capable configurations lose about 30 percentage points in assertion pass rate under full constraints. Database choices cause the largest losses.

ScarfBench makes agents migrate Java applications among Spring, Jakarta EE, and Quarkus. Only 1 of 204 directed migrations reaches full behavioral equivalence. Even the strongest whole-application run reports 87% compile success, 40% deploy success, and 12% test success.

SmellBench adds a design-maintenance angle. Expert review finds 63.1% of hard static smell detections are false positives. The best agent resolves 47.7% of cases, and the most aggressive repair setting introduces 140 new smells.

#### Sources
- [Constraint Decay: The Fragility of LLM Agents in Backend Code Generation](../Inbox/2026-05-07--constraint-decay-the-fragility-of-llm-agents-in-backend-code-generation.md): Reports the constraint-decay setup and the roughly 30 percentage-point drop under full backend constraints.
- [ScarfBench: A Benchmark for Cross-Framework Application Migration in Enterprise Java](../Inbox/2026-05-07--scarfbench-a-benchmark-for-cross-framework-application-migration-in-enterprise-java.md): Gives ScarfBench task design and migration success rates, including 1 of 204 full equivalents.
- [SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair](../Inbox/2026-05-07--smellbench-evaluating-llm-agents-on-architectural-code-smell-repair.md): Provides SmellBench labels, resolution rate, false-positive rate, and new-smell count.

### Tests and developer intent need repository search
Two benchmarks focus on information that agents cannot get from a single failing test.

TEBench asks agents to update tests after a production-code commit. Across seven configurations, affected-test identification F1 stays between 45.7% and 49.4%. Stale tests are hardest, with average F1 around 36%, because passing tests can still need semantic updates.

ProCodeBench measures proactive intent prediction from real VS Code traces and repository context. The dataset contains about 4.63 million integrated development environment (IDE) events from 1,246 developers and 5,492 annotated intent samples. The paper reports that LLM, retrieval, and agent baselines perform much worse on real traces than on simulated traces, and that repository context helps prediction.

#### Sources
- [Breaking, Stale, or Missing? Benchmarking Coding Agents on Project-Level Test Evolution](../Inbox/2026-05-07--breaking-stale-or-missing-benchmarking-coding-agents-on-project-level-test-evolution.md): Defines TEBench and reports affected-test identification F1, stale-test difficulty, and dataset size.
- [An Empirical Study of Proactive Coding Assistants in Real-World Software Development](../Inbox/2026-05-07--an-empirical-study-of-proactive-coding-assistants-in-real-world-software-development.md): Summarizes ProCodeBench data collection, real-versus-simulated trace findings, and repository-context effect.

### Control methods improve long agent runs
Several papers add explicit control over how agents spend steps, choose tasks, or recover from errors.

TACT diagnoses overthinking and overacting at each agent step, then steers hidden activations at test time. It reports AUC around 0.9 for separating drift states, +5.8 percentage points average resolve rate on Qwen3.5-27B, +4.8 points on Gemma-4-26B-A4B-it, and up to 26 fewer steps to resolve.

MAS-Algorithm uses five roles for competitive programming: algorithm selection, retrieval, planning, coding, and judging. Across five Qwen models it raises average accepted-solution rate by 6.48 points. In the same study, LoRA fine-tuning on accepted solutions adds only 0.89 points.

ASTOR applies reinforcement learning (RL) across code I/O prediction, code generation, unit test generation, and commit message generation. One shared model beats the best task-specific specialist by 9.0% on Qwen2.5-Coder-7B and 9.5% on Qwen3-8B.

#### Sources
- [TACT: Mitigating Overthinking and Overacting in Coding Agents via Activation Steering](../Inbox/2026-05-07--tact-mitigating-overthinking-and-overacting-in-coding-agents-via-activation-steering.md): Reports TACT’s drift labels, activation steering method, solve-rate gains, and step reductions.
- [MAS-Algorithm: A Workflow for Solving Algorithmic Programming Problems with a Multi-Agent System](../Inbox/2026-05-07--mas-algorithm-a-workflow-for-solving-algorithmic-programming-problems-with-a-multi-agent-system.md): Describes MAS-Algorithm’s five-agent workflow and acceptance-rate gains over direct prompting and fine-tuning.
- [Schedule-and-Calibrate: Utility-Guided Multi-Task Reinforcement Learning for Code LLMs](../Inbox/2026-05-07--schedule-and-calibrate-utility-guided-multi-task-reinforcement-learning-for-code-llms.md): Summarizes ASTOR’s multi-task RL method and improvements over specialists and baselines.

### Generated code must remain inspectable and maintainable
The day also includes evidence about code after the initial generation step.

Build-and-Find treats an agent-written repository as context for later agents. A builder creates a codebase from a hidden specification. A finder then answers questions about intended behavior and design choices using only the artifact. Compile-pass artifact-conditioned recovery reaches 98.9%, but the protocol gates inspection-effort claims on reliable recovery, so fast reading does not count when answers are unstable.

A maintenance study over the AIDev dataset tracks 508 agent-created files and 508 matched human-created files for at least six months. Agent-created files receive fewer maintenance commits and smaller relative edits. Humans still perform 83.21% of follow-up commits to agent-created files, so post-merge ownership remains largely human.

#### Sources
- [BUILD-AND-FIND: An Effort-Aware Protocol for Evaluating Agent-Managed Codebases](../Inbox/2026-05-07--build-and-find-an-effort-aware-protocol-for-evaluating-agent-managed-codebases.md): Provides Build-and-Find’s builder/finder protocol, recovery metrics, and effort-gating rule.
- [To What Extent Does Agent-generated Code Require Maintenance? An Empirical Study](../Inbox/2026-05-07--to-what-extent-does-agent-generated-code-require-maintenance-an-empirical-study.md): Reports the six-month maintenance study, commit counts, maintenance types, and human follow-up share.
