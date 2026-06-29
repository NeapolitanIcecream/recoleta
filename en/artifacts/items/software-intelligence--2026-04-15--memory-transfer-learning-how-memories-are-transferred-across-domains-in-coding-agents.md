---
source: arxiv
url: http://arxiv.org/abs/2604.14004v1
published_at: '2026-04-15T15:50:29'
authors:
- Kangsan Kim
- Minki Kang
- Taeil Kim
- Yanlai Yang
- Mengye Ren
- Sung Ju Hwang
topics:
- coding-agents
- memory-transfer-learning
- cross-domain-generalization
- self-evolving-agents
- code-benchmarking
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Memory Transfer Learning: How Memories are Transferred Across Domains in Coding Agents

## Summary
This paper studies whether coding agents can reuse memories from different coding domains instead of only from the same benchmark. It finds that cross-domain memory helps, and that abstract memories such as general insights transfer better than raw traces.

## Problem
- Existing memory-based coding agents usually reuse past experience only within the same task domain or benchmark.
- Real coding work shares common structure across domains, including shells, languages, testing, debugging, and interface constraints, so single-domain memory leaves useful experience unused.
- The paper asks whether heterogeneous memories help, what kind of knowledge transfers, and which memory form makes transfer work.

## Approach
- The authors build **Memory Transfer Learning (MTL)**: for a target benchmark, the agent retrieves memories collected offline from other coding benchmarks and inserts them into the prompt at inference time.
- They test four memory formats with different abstraction levels: **Trajectory** (raw action/observation trace), **Workflow** (selected reusable actions), **Summary** (task and postmortem summary), and **Insight** (general lessons written to avoid task-specific details).
- Retrieval uses text embeddings and cosine similarity; the system selects top-3 memories for each query from a heterogeneous memory pool that excludes the target benchmark.
- Evaluation covers 6 coding benchmarks: LiveCodeBench v6, Aider-Polyglot, SWE-Bench Verified, TerminalBench2, ReplicationBench, and MLGym-Bench, using Pass@3.
- The analysis compares zero-shot agents, MTL variants, and prior self-evolving methods such as ReasoningBank and AgentKB, and also checks transfer across different base models.

## Results
- On **GPT-5-mini**, zero-shot average **Pass@3 = 0.523**. The best MTL variant, **Insight**, reaches **0.560**, an average gain of **+3.7%** across 6 benchmarks.
- GPT-5-mini benchmark gains with **Insight** are: **LiveCodeBench 0.910 -> 0.930 (+2.0%)**, **SWE-Bench Verified 0.730 -> 0.770 (+4.0%)**, **TerminalBench2 0.315 -> 0.360 (+4.5%)**, **ReplicationBench 0.111 -> 0.189 (+7.8%)**, **MLGym-Bench 0.667 -> 0.750 (+8.3%)**, and **Aider-Polyglot 0.470 -> 0.470 (0.0%)**.
- Cross-model transfer also helps: **DeepSeek V3.2** improves from **0.542 -> 0.568 (+2.6%)** average with Insight; **Qwen3-Coder-480B-A35B-Instruct** improves from **0.483 -> 0.501 (+1.8%)**.
- Against prior self-evolving baselines on three benchmarks, **MTL = 0.630** average Pass@3, compared with **ReasoningBank = 0.601** and **AgentKB = 0.613**. The reported margins are **+2.9%** over ReasoningBank and **+1.7%** over AgentKB.
- MTL uses **431 memories**, while **AgentKB** uses **5,899 memories** in this comparison, yet MTL still scores higher.
- The claimed transfer mechanism is mostly **meta-knowledge** such as inspect-edit-verify routines, validation habits, small safe patches, and environment-aware debugging. The excerpt states that **algorithmic strategy transfer accounts for only 5.5% of gains**.

## Link
- [http://arxiv.org/abs/2604.14004v1](http://arxiv.org/abs/2604.14004v1)
