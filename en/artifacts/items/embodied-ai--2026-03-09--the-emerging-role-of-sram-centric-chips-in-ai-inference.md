---
source: hn
url: https://gimletlabs.ai/blog/sram-centric-chips
published_at: '2026-03-09T23:10:19'
authors:
- gmays
topics:
- ai-inference
- sram-centric-accelerators
- memory-hierarchy
- llm-decode
- heterogeneous-serving
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# The emerging role of SRAM-centric chips in AI inference

## Summary
This is an industry- and systems-design-oriented analysis discussing why SRAM-centric AI inference chips are becoming important in large-model inference. The core argument is that the real key is not just SRAM versus HBM, but the architectural tradeoff of **near-compute memory vs. far-compute memory**, and that different inference stages should be matched to different hardware.

## Problem
- The article aims to answer: **what kinds of AI inference workloads are better suited to SRAM-centric chips rather than traditional GPUs**, and why this difference arises.
- This matters because LLM inference is increasingly constrained by the **memory wall**, especially during the autoregressive **decode** stage; the article notes that agentic workloads generate about **15×** as many tokens as traditional chat models, increasing both latency and throughput pressure.
- Without understanding the relationship between a workload’s **arithmetic intensity** and memory placement, it is difficult to choose the right hardware for training, prefill, decode, and inference sharding/scheduling.

## Approach
- The article explains the issue with a simple framework: it compares the physical and system-level differences between **SRAM (on-chip, low-latency, low-capacity)** and **HBM/DRAM (off-chip, high-capacity, higher-latency)**, and emphasizes that the real tradeoff is **how close memory is to compute**.
- It treats GPUs as a **hierarchical-cache / far-memory compute** architecture, and views Cerebras, Groq, and d-Matrix as **flatter near-memory compute** architectures; the former relies on caching and data reuse, while the latter sacrifices some compute to gain larger on-chip working memory and higher bandwidth.
- The article proposes that the key mechanism determining the winner is **working set size → arithmetic intensity → optimal memory architecture**: if data reuse is high and arithmetic intensity is high, GPUs are better; if data reuse is low and performance is memory-bandwidth-bound, SRAM-centric chips are better.
- In LLM inference, **prefill** is generally more compute-intensive because it processes many tokens in batch and can amortize weight loading; **decode** is generally more memory-intensive because it is autoregressive token-by-token and repeatedly moves weights, making it better suited to SRAM-centric chips.
- Based on this, the article argues for **heterogeneous inference disaggregation**: place prefill on high-compute hardware, place decode or a speculative decoder on high-memory-bandwidth hardware, and even split execution of the same model across accelerators from different vendors.

## Results
- The article provides several key hardware figures to support the analysis: **SRAM read latency is about 1 ns**, while **DRAM/HBM reads are about 10–15 ns**, showing that on-chip SRAM is significantly faster in access latency.
- It compares on-chip SRAM capacity investment: **NVIDIA H100 has about 50 MB of SRAM, and B200 about 126 MB**; more aggressive SRAM-centric designs allocate even more on-chip storage. Even so, the article also points out that a wafer-scale design like **Cerebras** “still only” has about **44 GB of SRAM**, so large-model weights still need to be distributed across chips.
- As industry signals, the article cites two strong supporting examples: **NVIDIA licensed Groq IP for $20B in December 2024**; **Cerebras announced a 750 MW OpenAI inference workload deal**. These are not algorithmic benchmarks, but the authors view them as major proof points for the commercial viability of SRAM-centric architectures.
- The article cites industry data from d-Matrix’s CTO: **compute performance grows about 3× every two years, while memory bandwidth grows only 1.6×**, illustrating the worsening memory bottleneck in inference.
- On application demand, the article says **agentic workloads require about 15× the tokens of traditional chat**, further reinforcing the need to optimize decode latency/throughput.
- The article **does not provide formal quantitative benchmarks for its own system** (such as specific tokens/s, latency, energy, or direct comparisons against GPU baselines); its strongest quantitative claims come mainly from hardware parameters, industry events, and trend judgments rather than paper-style experimental results.

## Link
- [https://gimletlabs.ai/blog/sram-centric-chips](https://gimletlabs.ai/blog/sram-centric-chips)
