---
source: arxiv
url: http://arxiv.org/abs/2604.13120v1
published_at: '2026-04-13T13:51:13'
authors:
- Rajesh Kumar
- Waqar Ali
- Junaid Ahmed
- Najma Imtiaz Ali
- Shaban Usman
topics:
- multi-agent-llm
- autonomous-software-engineering
- execution-grounding
- swe-bench
- code-repair
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering

## Summary
AgentForge is a multi-agent software engineering system that requires every code change to pass real execution in a Docker sandbox before the change moves forward. The paper argues that this execution-grounded loop gives stronger correctness feedback than plain code generation.

## Problem
- LLMs can write plausible code, but they often cannot tell whether the code actually works in a real repository.
- Real bug fixing needs a loop over existing code, tests, execution output, and revision; one-shot generation misses multi-file context and regression checks.
- Prior agent systems may simulate execution or make verification optional, which lets wrong assumptions pass through the pipeline.

## Approach
- AgentForge splits the work across five agents: Planner, Coder, Tester, Debugger, and Critic.
- The key rule is mandatory execution grounding: every generated patch runs inside a network-isolated Docker sandbox before it can be accepted or revised further.
- The system retrieves two kinds of context for each task: similar past solved tasks from episodic memory and relevant files from a live repository index.
- The Coder edits files with minimal unified diffs when possible, the Tester writes pytest cases, and the Debugger uses real stdout/stderr and test failures for up to 3 repair attempts.
- The paper also formulates the workflow as an MDP over repository states, where reward is 1 only when all fail-to-pass tests pass and no pass-to-pass tests regress.

## Results
- On SWE-bench Lite, AgentForge reaches **40.0% resolution**.
- The paper says this beats single-agent baselines by **26 to 28 percentage points**.
- Evaluation uses **SWE-bench Lite**, a benchmark of **300** real GitHub issues from **11** Python repositories.
- The execution environment is a constrained Docker sandbox with **512 MB RAM**, **0.5 CPU**, no network access, and a **64-process** PID cap.
- The debugger loop retries failed code up to **3** times.
- The excerpt does not include the full ablation table, but the paper claims ablations show that both execution feedback and role decomposition improve performance on their own.

## Link
- [http://arxiv.org/abs/2604.13120v1](http://arxiv.org/abs/2604.13120v1)
