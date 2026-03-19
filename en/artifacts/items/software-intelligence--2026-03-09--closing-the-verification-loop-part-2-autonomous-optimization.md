---
source: hn
url: https://www.datadoghq.com/blog/ai/fully-autonomous-optimization/
published_at: '2026-03-09T23:05:28'
authors:
- chrisra
topics:
- llm-code-optimization
- formal-verification
- autonomous-deployment
- wasm-sandbox
- distributed-systems
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Closing the verification loop, Part 2: autonomous optimization

## Summary
This article presents a fully autonomous code optimization system for a distributed temporal aggregation service: an LLM automatically generates candidate implementations, and after formal verification, shadow-traffic validation, and WASM sandbox deployment, they are hot-updated directly into the production service. Its goal is to continuously generate better "provably correct" code for different tenants and workloads without human review.

## Problem
- Critical hot paths in distributed and high-throughput data systems are difficult to make both high-performance and correct, because concurrency, failures, network nondeterminism, and cross-machine invariants make bugs hard to test and reproduce.
- Traditional JIT/PGO is better at localized optimization at the microarchitectural level, and has difficulty automatically discovering "structural optimizations" such as replacing data structures or algorithms; meanwhile, earlier LLM evolution methods required humans to select targets, run benchmarks, review, and deploy, with cycles typically measured in hours.
- For systems like Unicron, where the aggregation loop executes for every message and every query, small inefficiencies become significant costs at the scale of hundreds of billions of time series, so optimization must happen per tenant, per workload, and in real time, while still guaranteeing unchanged outputs.

## Approach
- The system uses a "dual-server" architecture: the aggregation server handles real traffic; the evolution server continuously uses LLM-driven evolutionary search to generate optimized Rust/WASM aggregation modules, which can be hot-swapped without restart.
- A five-stage closed loop: **specialization** binds organization IDs and aggregation configurations as compile-time constants; **LLM evolution** programmatically explores and generates candidate code in a Git repository; **formal verification** uses Verus to prove the safety properties of the invoked codec libraries; **shadow evaluation** compares output hashes against the baseline on held-out validation traffic; **live hot-swap** switches validated WASM modules online.
- The core mechanism can be understood simply as: first write "this tenant's fixed rules" directly into the code, then let the LLM repeatedly try better implementations; any candidate is allowed into production only if it "can compile, prove safe, and produce completely identical outputs on real held-out traffic."
- Unlike ordinary compiler optimization, an LLM can perform algorithm-level rewrites. For example, it can transform O(N) logic of "scan all filter conditions for each data point" into a structural change that builds a HashMap during initialization and performs O(1) lookup at runtime.
- To ensure the safety of autonomous operation, the execution boundary is jointly enforced by the WASM sandbox, wasmparser validation, Ed25519 signatures, the WIT interface, and held-out validation traffic, reducing the risk that faulty code directly affects the host process.

## Results
- In one specific workload (an organization monitoring 100 services, with each query filtered by different service names and using 30-second SUM aggregation), baseline throughput was **7,106 msg/s**. After **3 generations** of evolution using **Claude Opus 4.6** and passing held-out traffic hash validation, the hot-updated version reached **26,263 msg/s**, a **270%** improvement over the current production generic aggregation function.
- In a second workload (with **100** different group-by tag combinations on the same metric), throughput improvement relative to the baseline reached **541%**.
- The article claims that the improved aggregation algorithm can complete verification and autonomously deploy to running services within **minutes**, with no human intervention and no service restart.
- Qualitatively, the authors note that **specialization** is the most stable and largest single source of gains; the most important breakthrough came from the LLM discovering **algorithm-level changes** that traditional JIT/PGO does not easily produce, such as the O(N)-to-O(1) HashMap refactor.

## Link
- [https://www.datadoghq.com/blog/ai/fully-autonomous-optimization/](https://www.datadoghq.com/blog/ai/fully-autonomous-optimization/)
