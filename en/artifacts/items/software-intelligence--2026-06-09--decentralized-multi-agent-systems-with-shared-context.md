---
source: arxiv
url: https://arxiv.org/abs/2606.10662v1
published_at: '2026-06-09T10:13:07'
authors:
- Yuzhen Mao
- Azalia Mirhoseini
topics:
- decentralized-agents
- shared-context
- multi-agent-systems
- software-engineering-agents
- long-context-reasoning
- test-time-scaling
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Decentralized Multi-Agent Systems with Shared Context

## Summary
DeLM replaces a main multi-agent controller with agents that share a verified problem state and take work from a task queue. It targets coding agents and long-context QA, where controller bottlenecks can waste test-time compute and lose useful intermediate findings.

## Problem
- Most multi-agent LLM systems route subagent work through one main agent, so communication and result merging become serial bottlenecks as the number of subtasks grows.
- In software repair, isolated attempts repeat failed searches and cannot reuse partial fixes; in long-context QA, a main agent may assign evidence chunks before knowing which evidence matters.
- This matters because test-time scaling only helps when extra agents create reusable progress, rather than extra calls that repeat work or lose details during merging.

## Approach
- DeLM uses parallel agents, a shared verified context, and a task queue. Agents claim queued subtasks asynchronously, read current shared progress, reason locally, and write back compact updates.
- The shared context stores gists: short entries about facts, failed hypotheses, constraints, source evidence, and partial solutions. Agents can unfold a gist into detailed summaries or raw evidence when needed.
- Before an update enters the shared context, an LLM verifier checks it against its source evidence or reasoning trace. Failed updates are rejected or regenerated.
- When the queue is empty, the most recently completed agent checks the shared state, adds more subtasks if needed, or produces the final answer.

## Results
- On SWE-bench Verified with Gemini 3 Flash, DeLM reports 65.7% Avg.@1, 72.9% Pass@2, and 77.4% Pass@4. The strongest listed baseline on Avg.@1 is AOrchestra-Parallel at 56.4%, so the gain is 9.3 percentage points.
- On SWE-bench Verified with Gemini 3 Flash, DeLM reports $0.12 cost per task, compared with $0.24 for AOrchestra, $0.25 for AOrchestra-Parallel, and $0.26 for mini-SWE-agent.
- On SWE-bench Verified with Claude Opus 4.6, DeLM reports 78.0% Avg.@1, 80.7% Pass@2, and 82.5% Pass@4, ahead of mini-SWE-agent at 76.9%, 79.8%, and 81.7%.
- On LongBench-v2 Multi-Doc QA, the paper says DeLM has the highest average accuracy across GPT-5.4, Claude Sonnet 4.6, Gemini 3 Flash, and DeepSeek-V4-Pro, with gains up to 5.7 percentage points over the strongest baseline.
- The LongBench-v2 setting contains 125 samples: 15 financial, 23 government, 23 multi-news, 14 legal, and 50 academic.
- On OOLONG, the excerpt gives no table values. It says vanilla DeLM trails RLM on exact row-level aggregation, while RLM plus DeLM gets the best accuracy and lowest cost.

## Link
- [https://arxiv.org/abs/2606.10662v1](https://arxiv.org/abs/2606.10662v1)
