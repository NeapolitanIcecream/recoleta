---
source: arxiv
url: https://arxiv.org/abs/2606.05548v1
published_at: '2026-06-04T01:00:54'
authors:
- Jintao Huang
- Xiaomin Li
- Gaurav Mittal
- Yu Hu
topics:
- agent-development-kits
- llm-as-developer
- code-intelligence
- software-agents
- benchmarking
- multi-agent-systems
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# ADK Arena: Evaluating Agent Development Kits via LLM-as-a-Developer

## Summary
ADK Arena automates comparison of 51 Python Agent Development Kits by asking the same LLM coding agent to build benchmark agents for each kit. The paper treats generation effort as an API usability signal and task performance as a measure of agent effectiveness.

## Problem
- Developers have many ADKs to choose from, but little empirical evidence about which kits produce better agents or lower development cost.
- Manual benchmark implementations scale poorly: 51 frameworks across 4 benchmarks would require 204 expert-written agent implementations and could bias results toward familiar APIs.
- Existing agent benchmarks mostly compare models while holding the ADK fixed; developer surveys report opinions rather than runtime behavior.

## Approach
- The core method is LLM-as-a-Developer: one coding agent reads each ADK's documentation and source code, writes an `agent.py` file with `solve(prompt, workdir)`, and repairs it after validation feedback.
- ADK Arena runs each framework in an isolated Docker image with the same prompts, tools, and budgets, so the main variable is the ADK.
- Validation has three levels: static checks for imports and framework use, a real LLM smoke test, and one real benchmark task with an early-exit success check.
- The system evaluates generated agents on SWE-bench Verified, $\tau^2$-bench, Terminal-Bench, and MCP-Atlas, using a proxy to route and measure LLM calls.

## Results
- The study covers 51 Python ADK frameworks and 204 agent-benchmark pairs.
- Agent generation succeeds in 57% of runs.
- Generation cost varies by 5.6x across frameworks, from $0.6 to $3.4 per generated agent.
- The best single-benchmark ADK agents resolve up to 80% of tasks, while the median framework resolves 32%.
- Some ADK agents beat general-purpose frontier coding agents at lower cost, according to the paper.
- Information-source ablations show genuine framework usage stays between 28% and 40%; it reaches 33% even with no reference material, suggesting docs, source code, and model prior knowledge often substitute for one another.

## Link
- [https://arxiv.org/abs/2606.05548v1](https://arxiv.org/abs/2606.05548v1)
