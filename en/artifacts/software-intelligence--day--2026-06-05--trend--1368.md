---
kind: trend
trend_doc_id: 1368
granularity: day
period_start: '2026-06-05T00:00:00'
period_end: '2026-06-06T00:00:00'
topics:
- coding agents
- software engineering agents
- benchmarking
- repository exploration
- evaluation integrity
- agent security
- GitHub adoption
run_id: materialize-outputs
aliases:
- recoleta-trend-1368
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering-agents
- topic/benchmarking
- topic/repository-exploration
- topic/evaluation-integrity
- topic/agent-security
- topic/github-adoption
language_code: en
pass_output_id: 232
pass_kind: trend_synthesis
---

# Coding agents are being judged by traces, line-level evidence, and adversarial tests

## Overview
Coding-agent work in this window centers on evidence-rich control: traces become training data, repository search gets line-level scoring, and evaluation adds randomized caps and runtime checks. Socratic-SWE, SWE-Explore, and CapCode carry the strongest signal.

## Findings

### Trace-based training and harder coding tasks
Socratic-SWE treats solver traces as reusable training material. It distills repeated failure modes and repair patterns into skills, then uses those skills to generate targeted repository repair tasks. Under a 36k-task budget, it reports 50.40% on SWE-bench Verified after three iterations and a +6.22 point mean gain across four benchmarks over the Qwen3.5-9B base agent.

BenchEvolver attacks benchmark saturation through task construction. It mutates the executable reference solution first, then writes the statement and tests around it. Its 91-problem benchmark gives frontier models a Pass@1 range of 27.5% to 62.6%, and the Hard split drops from 87.0% to 45.7% averaged across evaluated models.

#### Sources
- [Socratic-SWE: Self-Evolving Coding Agents via Trace-Derived Agent Skills](../Inbox/2026-06-05--socratic-swe-self-evolving-coding-agents-via-trace-derived-agent-skills.md): Reports Socratic-SWE's trace-derived skills, training loop, and benchmark gains.
- [BenchEvolver: Frontier Task Synthesis via Solution-Centric Evolution](../Inbox/2026-06-05--benchevolver-frontier-task-synthesis-via-solution-centric-evolution.md): Describes solution-first task evolution and the resulting harder coding benchmark.

### Repository exploration as a separate capability
SWE-Explore separates finding the relevant code from writing the patch. The benchmark asks explorers to return ranked file-line regions for 848 issues across 203 repositories. Its ground truth comes from successful repair trajectories, so the score rewards the code that agents actually needed during fixes.

The reported downstream test is useful because it ties search quality to repair. With five selected regions on a 150-instance subset, Oracle reaches 59.7% resolve rate, CoSIL reaches 59.3%, and Mini-SWE-Agent reaches 50.0%. Classical retrieval is lower in the same setting, with TF-IDF at 26.0%, RAG at 23.3%, and BM25 at 12.7%.

#### Sources
- [SWE-Explore: Benchmarking How Coding Agents Explore Repositories](../Inbox/2026-06-05--swe-explore-benchmarking-how-coding-agents-explore-repositories.md): Defines SWE-Explore and reports dataset scale, line-level metrics, and repair correlations.

### Validation against cheating, unsafe skills, and silent bugs
CapCode adds randomized accepted outputs to coding tasks. A non-cheating agent has a capped expected pass rate of B = 1/M, so scores above that cap become statistical evidence of test leakage or grader gaming. CapReward changes reinforcement learning rewards so training gives no gain for above-cap behavior.

MalSkillBench extends the same concern to agent skills. It contains 3,944 malicious skills and 4,000 matched benign skills, with generated samples admitted only after runtime verification. The best skill-specific detector reaches 88.6% F1 across 12 tools, while high-recall transfer tools can create up to 3,979 false positives on 4,000 benign skills.

QBugLM adds a domain-specific validation case. It tests large language models (LLMs) on OpenQASM 3.0 quantum debugging with simulator checks. In the reported case study, one retry raises Pass@1 from below 25% to above 80%, showing that feedback and validation dominate prompt style for this task.

#### Sources
- [Do Coding Agents Deceive Us? Detecting and Preventing Cheating via Capped Evaluation with Randomized Tests](../Inbox/2026-06-05--do-coding-agents-deceive-us-detecting-and-preventing-cheating-via-capped-evaluation-with-randomized-tests.md): Explains CapCode, CapReward, randomized caps, and cheating detection claims.
- [MalSkillBench: A Runtime-Verified Benchmark of Malicious Agent Skills](../Inbox/2026-06-05--malskillbench-a-runtime-verified-benchmark-of-malicious-agent-skills.md): Reports MalSkillBench's runtime-verified malicious skills and detector results.
- [QBugLM: An Agentic Benchmarking Framework for LLM-based Quantum Software Debugging](../Inbox/2026-06-05--qbuglm-an-agentic-benchmarking-framework-for-llm-based-quantum-software-debugging.md): Reports QBugLM's quantum debugging setup and feedback-retry gains.

### Agent use is now visible in new software projects
The GitHub adoption study reports 71.83% conservative coding-agent adoption among 12,794 newer projects, compared with 26.46% in 127,670 older projects. File-level traces appear in 60.03% of new projects. The detected AI-assisted commit ratio has a median near 30% in new projects.

A practitioner account gives a concrete example of the working pattern behind those traces. A guided agent built a working Intellivision emulator in 36 hours after the author added a jzintv-derived test oracle. The oracle compared registers, flags, memory, and cycle counts, which made a hardware-accurate task tractable for an agent-assisted workflow.

#### Sources
- [Agentic Very Much! Adoption of Coding Agent in New GitHub Projects](../Inbox/2026-06-05--agentic-very-much-adoption-of-coding-agent-in-new-github-projects.md): Quantifies coding-agent adoption and AI-assisted commit ratios in new GitHub projects.
- [Using an AI coding agent with oracle-based testing to build a game emulator](../Inbox/2026-06-05--using-an-ai-coding-agent-with-oracle-based-testing-to-build-a-game-emulator.md): Provides a concrete agent-assisted emulator build using oracle-based testing.
