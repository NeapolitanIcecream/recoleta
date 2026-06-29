---
source: arxiv
url: https://arxiv.org/abs/2605.00528v1
published_at: '2026-05-01T09:05:28'
authors:
- Dongxin Guo
- Jikun Wu
- Siu Ming Yiu
topics:
- agent-inference-serving
- gpu-scheduling
- kv-cache-management
- workflow-scheduling
- llm-serving
- software-agents
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters

## Summary
SAGA schedules an entire AI-agent task on GPU clusters instead of scheduling each LLM call separately. Its main gain comes from keeping reusable KV cache through tool-call gaps and routing later steps back to the same worker.

## Problem
- Agent tasks often make 10-100 chained LLM calls, separated by tool calls; request-level GPU schedulers discard session state and add 3-8x end-to-end latency.
- In a 32-GPU SWE-bench measurement with vLLM v0.6.0, 38% of execution time went to KV-cache regeneration, average GPU memory use was 42%, and end-to-end latency was 6.0x the inference-only baseline.
- This matters for coding agents, browser agents, and other interactive agents because the user-visible metric is full task completion time across all steps.

## Approach
- SAGA treats the agent workflow as the schedulable unit, so the scheduler tracks the whole task across reasoning, tool calls, and later LLM calls.
- Agent Execution Graphs record the expected step structure and help predict whether a session's KV cache will be reused after a tool call.
- Workflow-aware LRU with TTL keeps high-value KV cache in GPU memory across idle tool periods and evicts lower-value cache first under memory pressure.
- Session-affinity batching routes related requests to the same worker to reuse cache, while randomized work stealing moves work when load becomes uneven.
- Agent Fair Share schedules tenants by expected task completion time and includes a bounded-deviation fairness guarantee.

## Results
- On 64 A100 GPUs, SAGA reduced task completion time by 1.73x ± 0.11 on SWE-bench and 1.55x ± 0.09 on WebArena versus vLLM v0.15.1 with Automatic Prefix Caching; the geometric mean was 1.64x with p < 0.001.
- Against systems without workflow awareness, the reported task-completion improvement reached 3.01x.
- Its workflow-aware eviction came within 1.31x of Bélády's optimal offline cache policy on production agent traces.
- GPU memory utilization improved by 1.22x ± 0.05; the excerpt also reports 71% utilization for SAGA versus 42% for vLLM in the SWE-bench measurement.
- SAGA reached 99.2% SLO attainment under multi-tenant interference.
- The latency gain costs throughput: peak throughput was about 30% lower than throughput-optimal batch scheduling.

## Link
- [https://arxiv.org/abs/2605.00528v1](https://arxiv.org/abs/2605.00528v1)
