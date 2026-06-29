---
source: arxiv
url: http://arxiv.org/abs/2604.01508v1
published_at: '2026-04-02T00:42:29'
authors:
- Akshey Sigdel
- Rista Baral
topics:
- agent-benchmark
- tool-use
- reliability-evaluation
- fault-injection
- code-agents
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# ToolMisuseBench: An Offline Deterministic Benchmark for Tool Misuse and Recovery in Agentic Systems

## Summary
ToolMisuseBench is an offline benchmark for testing how tool-using agents fail and recover when tool calls break in specific ways. Its main contribution is deterministic, replayable fault injection with explicit limits on steps, calls, and retries, so reliability can be measured in a controlled way.

## Problem
- Tool-using agents often fail for operational reasons such as invalid arguments, schema drift, timeouts, rate limits, weak retry logic, and authorization errors, even when their language understanding is strong.
- Existing agent benchmarks usually measure broad capability, but they do not isolate tool misuse and recovery under fixed budgets with exact replay of the same failures.
- This matters for deployment because agents can look capable in static tests and still fail repeatedly once strict tool schemas, policy rules, and retry limits are enforced.

## Approach
- The paper introduces a deterministic benchmark where each task includes an instruction, tool schemas, initial state, success criteria, a fault plan, and budget limits for steps, tool calls, and retries.
- It uses offline simulators across four domains: CRUD, retrieval, file, and scheduling. Faults are injected in replayable ways, including schema drift, rate limit, timeout, authorization failure, and adversarial error rewriting.
- Evaluation tracks more than final task completion. It measures success, invalid call behavior, policy violations, recovery success, tool-call efficiency, budget overruns, and budgeted success under call caps.
- The released package includes data generation, evaluation, trace logging, aggregate reports, and support for both built-in baselines and external agents through a simple reset/act interface.
- The dataset has 6,800 tasks with fixed splits: 5,000 train, 800 development, and 1,000 public test.

## Results
- On the 1,000-task public test split, all three baselines reach the same overall task success: **0.250**. The heuristic baseline averages **2.95** tool calls, while schema-repair and policy-aware baselines average **3.25** calls.
- Overall policy violations are **0.168** for the heuristic baseline and **0.166** for both schema-repair and policy-aware baselines. Overall recovery is **0.000** for heuristic and **0.250** for the other two baselines.
- For **timeout** faults, success is **0.499** for heuristic and **0.502** for schema-repair and policy-aware. Recovery on timeout rises from **0.000** with heuristic to **0.502** with the repair-based methods.
- For **schema drift** faults, success is **0.503** for heuristic and **0.497** for schema-repair and policy-aware. Recovery on schema drift rises from **0.000** with heuristic to **0.497** with the repair-based methods.
- For **authorization** and **rate limit** subsets, all baselines have **0.000** success in the released setting.
- Budgeted success curves are flat with **AUC 0.25** for all agents, which the paper interprets as evidence that better recovery heuristics alone do not fix the main bottleneck under the current fault mix and budget constraints.

## Link
- [http://arxiv.org/abs/2604.01508v1](http://arxiv.org/abs/2604.01508v1)
