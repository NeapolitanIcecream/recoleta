---
kind: trend
trend_doc_id: 180
granularity: day
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-07T00:00:00'
topics:
- coding-agents
- reinforcement-learning
- software-testing
- program-repair
- verification
- workflow-automation
run_id: materialize-outputs
aliases:
- recoleta-trend-180
tags:
- recoleta/trend
- topic/coding-agents
- topic/reinforcement-learning
- topic/software-testing
- topic/program-repair
- topic/verification
- topic/workflow-automation
language_code: en
pass_output_id: 38
pass_kind: trend_synthesis
---

# Software-agent research is converging on verifiable training loops and hard control gates

## Overview
The clearest work on this day makes software agents easier to score, easier to rerun, and easier to block when they fail checks. Atomic-skill RL, Agent-CoEvo, and Nidus each tighten the control loop in a different place: training target, repository repair, and engineering governance. Compared with the prior few days, the emphasis is less on showing that agents can act in real environments and more on building training and verification setups that keep those actions measurable.

## Clusters

### Execution-scored RL for engineering agents
Reinforcement learning is getting more usable because the training target is narrower and the environment is faster. *Scaling Coding Agents via Atomic Skills* breaks software work into five verifiable skills and reports an average 18.7% gain across ten tasks, including SWE-bench Verified at 0.585 from 0.507. *SandMLE* applies the same execution-first logic to machine learning engineering: synthetic tasks cut runtime from about 200 seconds to under 15 seconds, then improve Any Medal rate by 20.3% to 66.9% on MLE-bench-lite. The common pattern is simple: make each step cheap to run and easy to score, then scale on-policy RL.

#### Evidence
- [Scaling Coding Agents via Atomic Skills](../Inbox/2026-04-06--scaling-coding-agents-via-atomic-skills.md): Atomic-skill RL setup and cross-task gains for coding agents
- [Synthetic Sandbox for Training Machine Learning Engineering Agents](../Inbox/2026-04-06--synthetic-sandbox-for-training-machine-learning-engineering-agents.md): Synthetic sandbox design, 13x speedup, and MLE gains

### Behavior-first evaluation at repository and service level
Repository agents are being judged on whether they can repair behavior, not just patch files. *Agent-CoEvo* searches over code patches and test patches together, then scores them through a pass-fail matrix. It reports 41.33% resolved on SWE-bench Lite and 46.4% on SWT-bench Lite, with higher test quality than the listed baselines. In microservices, *Mirage* keeps the model in the dependency loop during testing and reaches 99% status-code fidelity and 99% response-shape fidelity across 110 scenarios. Both papers put the model inside an executable feedback loop where behavior is checked as it unfolds.

#### Evidence
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): Joint code-test search and benchmark results on SWE-bench Lite and SWT-bench Lite
- [MIRAGE: Online LLM Simulation for Microservice Dependency Testing](../Inbox/2026-04-06--mirage-online-llm-simulation-for-microservice-dependency-testing.md): Runtime dependency simulation and fidelity metrics for microservice testing

### Deterministic and solver-checked control layers
A second line of work is reducing runtime model freedom once the task is clear enough to compile or verify. *Compiled AI* generates a small code artifact once, validates it, and then runs deterministically. On BFCL it reaches 96% task completion, breaks even after about 17 transactions, and runs at 4.5 ms median latency with 100% reproducibility. *Nidus* pushes harder on governance: every change is checked against a solver-backed living specification, and the paper reports a self-hosted 100,000-line system with proof obligations on every commit. This day’s strongest systems do not ask the model to be careful on its own. They bind it to code, tests, or formal checks.

#### Evidence
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): Compiled workflow generation, validation pipeline, and cost/latency results
- [Nidus: Externalized Reasoning for AI-Assisted Engineering](../Inbox/2026-04-06--nidus-externalized-reasoning-for-ai-assisted-engineering.md): Solver-checked living specification and self-hosting evidence
