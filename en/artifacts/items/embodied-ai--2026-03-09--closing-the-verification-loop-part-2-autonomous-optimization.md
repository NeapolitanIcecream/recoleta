---
source: hn
url: https://www.datadoghq.com/blog/ai/fully-autonomous-optimization/
published_at: '2026-03-09T23:05:28'
authors:
- chrisra
topics:
- autonomous-optimization
- llm-code-evolution
- formal-verification
- wasm-sandbox
- distributed-systems
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# Closing the verification loop, Part 2: autonomous optimization

## Summary
This article presents a fully autonomous code optimization system for a distributed time-series aggregation service: an LLM automatically generates candidate implementations, which can then be hot-swapped into production without human intervention after formal verification, shadow-traffic validation, and WASM sandbox deployment. Its core contribution is turning “whether it can be verified” into a closed loop, making it possible to evolve and optimize code in real time per tenant and per workload.

## Problem
- The target of optimization is the high-frequency aggregation hot path in a time-series database; under dynamic multi-tenant workloads and tens of billions of time series, even small inefficiencies accumulate into significant cost.
- Traditional JIT/PGO is better at localized microarchitectural optimization and struggles to discover and safely deploy new algorithmic structures online; meanwhile, prior LLM evolution depended on humans to select targets, review, and release, making it too slow.
- The key challenge is how to let AI aggressively search for better algorithms without human intervention while still allowing machines to reliably detect errors, verify correctness, and safely deploy to production.

## Approach
- A "two-server" architecture is used: the aggregation server handles real traffic, while the evolution server continuously uses LLM-driven evolutionary search to generate optimized Rust/WASM modules.
- A five-stage validation pipeline forms the closed loop: **specialization** (binding org_id and aggregation configuration as compile-time constants) → **LLM evolution** (evolving new code from historically high-scoring candidates) → **formal verification** (using Verus to prove safety properties of the underlying codec) → **shadow evaluation** (comparing output hashes on held-out validation traffic) → **live hot-swap** (zero-downtime replacement via WASM modules).
- The most central mechanism is first “baking” specific tenant/query configurations into the code, allowing both the compiler and the LLM to perform specialized rewrites around a known workload, then checking on previously unseen real traffic whether the results are exactly consistent with the baseline.
- Safety and isolation rely on the WASM sandbox, wasmparser validation, Ed25519 signatures, and a controlled host/guest interface; modules can be hot-swapped by organization ID and aggregation configuration without restarting the service.
- The authors emphasize that the breakthrough is not just conventional compiler optimization, but that under the constraints of the verification closed loop, the LLM discovered structural algorithmic changes—for example, rewriting an **O(N)** process that traverses all filter conditions for each point into an **O(1)** HashMap approach with table construction at initialization and a single lookup per point.

## Results
- On one specific Unicron workload (an organization monitoring **100** services, each query filtered by a different service name, performing **SUM** over a **30-second** window), baseline throughput was **7,106 msg/s**.
- For that workload, after specialization, **3 generations** of evolution based on **Claude Opus 4.6**, and held-out traffic hash-consistency validation, hot-swapped deployment reached **26,263 msg/s**, a **270%** improvement over the current production general-purpose aggregation function.
- On a second workload (with **100** different group-by tag combinations for the same metric), throughput improved by **541%** relative to the same baseline.
- The paper explicitly claims that these improvements can be verified and autonomously deployed within **minutes**, rather than the previous process that required human review and release and typically took **hours**.
- The authors also provide a qualitative conclusion: **specialization** is the most stable and largest single source of gains, while LLM evolution further discovers algorithm-level refactorings that traditional JIT/PGO would struggle to obtain automatically.

## Link
- [https://www.datadoghq.com/blog/ai/fully-autonomous-optimization/](https://www.datadoghq.com/blog/ai/fully-autonomous-optimization/)
