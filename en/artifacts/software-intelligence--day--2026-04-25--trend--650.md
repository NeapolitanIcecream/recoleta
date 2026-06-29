---
kind: trend
trend_doc_id: 650
granularity: day
period_start: '2026-04-25T00:00:00'
period_end: '2026-04-26T00:00:00'
topics:
- agent-evaluation
- coding-agents
- benchmarks
- software-engineering
- repository-execution
run_id: materialize-outputs
aliases:
- recoleta-trend-650
tags:
- recoleta/trend
- topic/agent-evaluation
- topic/coding-agents
- topic/benchmarks
- topic/software-engineering
- topic/repository-execution
language_code: en
pass_output_id: 108
pass_kind: trend_synthesis
---

# Executable evidence is setting the bar for coding and agent research

## Overview
April 25’s coding research is strongest where claims meet executable evidence. Simulating and Evaluating Agentic Systems and CUJBench both insist on judging agents through full runs, tool traces, state changes, and reproducible artifacts. Repository work stays tough: RAT improves setup, but real commit studies still show compile, analysis, and test failures after generation.

## Clusters

### Evaluation is moving from transcript checks to full-run evidence
Evaluation work is getting closer to full agent behavior. The strongest example is a sim/eval stack for agentic systems that tests multi-step actions, tool use, backend state, and user-visible outcomes in one run. It separates scenario design, simulation, and grading, then logs world state, tool traces, transcripts, and surface artifacts. CUJBench applies the same demand for grounded evidence to failure diagnosis. It freezes browser and backend evidence into reproducible incident snapshots, and current agents still reach only 19.7% accuracy. The shared lesson is simple: transcript scoring is too weak for systems that act through tools and changing state.

#### Evidence
- [Simulating and Evaluating Agentic Systems](../Inbox/2026-04-25--simulating-and-evaluating-agentic-systems.md): Sim/eval design for multi-step agent behavior, structured logs, and deterministic assertions.
- [CUJBench: Benchmarking LLM-Agent on Cross-Modal Failure Diagnosis from Browser to Backend](../Inbox/2026-04-25--cujbench-benchmarking-llm-agent-on-cross-modal-failure-diagnosis-from-browser-to-backend.md): Cross-modal benchmark with 87 scenarios and 19.7% accuracy shows diagnosis remains hard even with richer evidence.

### Coding agents are being judged by whether they run, build, and survive project checks
Repository-level coding still fails on basic software gates. RAT targets environment setup, a common reason code agents cannot even start, and reports much higher environment setup success on its 2,000-plus repository benchmark, including 63.2% on Python and 98.7% on Rust. A separate study of 212 real commits in eight C projects shows why this matters after setup: generated patches still fail to compile, trip static analysis, and miss tests, even when the original commits are small. This keeps execution, buildability, and repository context at the center of coding-agent research.

#### Evidence
- [I reverse-engineered Claude Desktop's storage to give it memory](../Inbox/2026-04-25--i-reverse-engineered-claude-desktop-s-storage-to-give-it-memory.md): Repository environment configuration benchmark and ESSR gains across languages.
- [Can LLMs be Effective Code Contributors? A Study on Open-source Projects](../Inbox/2026-04-25--can-llms-be-effective-code-contributors-a-study-on-open-source-projects.md): Real open-source commit study documents compile errors, static-analysis failures, and uneven project success.

### Constrained code tasks are yielding clearer gains than broad autonomy
Two papers push code assistance into narrower, more concrete settings. MOSAIC tackles scientific workflow generation when no test cases exist. It uses teacher-student distillation and a compact shared context, then improves SciCode results across GPT-4o, Claude Sonnet 4, and Gemini 2.5 Flash. Another study asks what small local models can do offline for Python bug detection. On 349 BugsInPy cases, LLaMA 3.2 and Mistral reach about 43% to 45% exact accuracy, with many partial answers that point to the right area but miss the full fix. The practical pattern is targeted help under clear constraints, not general autonomous coding.

#### Evidence
- [Knowledge Lever Risk Management for Software Engineering: A Stochastic Framework for Mitigating Knowledge Loss](../Inbox/2026-04-25--knowledge-lever-risk-management-for-software-engineering-a-stochastic-framework-for-mitigating-knowledge-loss.md): Scientific code generation without test cases, with measured gains on SciCode.
- [An Empirical Evaluation of Locally Deployed LLMs for Bug Detection in Python Code](../Inbox/2026-04-25--an-empirical-evaluation-of-locally-deployed-llms-for-bug-detection-in-python-code.md): Offline bug detection results on BugsInPy with exact and partial accuracy breakdowns.
