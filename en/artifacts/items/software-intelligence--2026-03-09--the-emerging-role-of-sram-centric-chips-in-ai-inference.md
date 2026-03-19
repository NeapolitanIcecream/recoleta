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
- llm-serving
- heterogeneous-computing
relevance_score: 0.56
run_id: materialize-outputs
language_code: en
---

# The emerging role of SRAM-centric chips in AI inference

## Summary
This article analyzes why SRAM-centric AI accelerators are starting to show advantages over traditional GPUs for inference, especially in the LLM decode stage. The core argument is that the real architectural divide is not "SRAM vs HBM," but rather "near-compute memory vs far-compute memory," and that different inference stages should be mapped to different hardware.

## Problem
- The article aims to answer: **why certain AI inference workloads are better suited to SRAM-centric chips than GPUs, and how to determine the boundary between where each is applicable**.
- This matters because LLM inference is running into the **memory wall**: compute capability is growing faster than memory bandwidth, and agentic workloads are said in the article to generate about **15x** the token demand of traditional chat models, making end-to-end latency and throughput critical bottlenecks.
- The traditional approach of using "one piece of hardware for the entire inference pipeline" is becoming increasingly inefficient, especially in the autoregressive decode stage, which has low arithmetic intensity and high memory pressure, making it hard to fully utilize GPU compute.

## Approach
- The article uses an **architectural analysis + workload decomposition** approach to compare the fundamental differences between GPUs and SRAM-centric chips in memory physical properties and system design.
- The core mechanism can be summarized simply as: **if data can fit in on-chip memory very close to compute, movement is reduced, latency drops, and bandwidth increases; if the data is too large, the system must rely on higher-capacity remote memory, but it will be slower.**
- The authors argue that the key factor is not chip brand, but **working set size → arithmetic intensity → memory placement choice**: the larger the working set and the lower the reuse, the more it favors near-compute high-bandwidth memory; tasks with high reuse and high arithmetic intensity are better suited to GPUs.
- In the inference pipeline, the article emphasizes **separating prefill and decode**: prefill is more compute-intensive and better suited to high-throughput GPUs; decode is more memory-bandwidth-intensive and better suited to SRAM-centric hardware.
- It further proposes a more fine-grained **heterogeneous partitioning / multi-silicon scheduling** approach, such as placing the small draft model in speculative decoding on SRAM-centric hardware while running batch verification on GPUs.

## Results
- This is not an experimental paper, and **it does not provide systematic benchmark results or a unified experimental table**, so it lacks reproducible quantitative performance evaluation.
- Key hardware figures cited in the article include: **~1 ns SRAM read latency** versus **~10–15 ns DRAM/HBM reads**, used to illustrate the low-latency advantage of on-chip SRAM.
- The article lists GPU on-chip SRAM capacity as: **~50 MB SRAM for H100** and **~126 MB SRAM for B200**; more aggressive SRAM-centric designs devote more area to on-chip storage. As an upper-bound example, **Cerebras has ~44 GB SRAM on a full wafer-scale chip**, though even then large-model weights still need to be distributed across chips.
- The article cites industry-trend figures: NVIDIA reportedly licensed Groq IP for **$20 billion** in December 2024, and Cerebras announced a **750 MW** deal to serve OpenAI inference workloads, as signals of market validation for the SRAM-centric path.
- The article cites an industry observation from the d-Matrix CTO: compute performance grows by about **3x** every two years, while memory bandwidth grows only about **1.6x**, supporting the "memory wall" argument.
- On future designs, the article mentions that d-Matrix's upcoming Raptor is said to provide **10x the bandwidth of HBM4** through custom DRAM stacked above compute; however, this is a vendor claim, not a measured result in the article.

## Link
- [https://gimletlabs.ai/blog/sram-centric-chips](https://gimletlabs.ai/blog/sram-centric-chips)
