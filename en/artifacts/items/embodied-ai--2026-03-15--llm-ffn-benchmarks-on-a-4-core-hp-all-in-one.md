---
source: hn
url: https://rolv.ai/
published_at: '2026-03-15T23:19:37'
authors:
- heggenhougen
topics:
- llm-inference
- matrix-arithmetic
- sparse-computing
- benchmarking
- energy-efficiency
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# LLM FFN benchmarks on a 4‑core HP All‑in‑One

## Summary
This article introduces rolvsparse©, a new compute primitive that allegedly restructures matrix multiplication execution **without changing hardware, disrupting existing models, or requiring retraining**. Its core selling point is that it achieves extremely large throughput and energy-efficiency gains across multiple hardware platforms and real/architecture-matched model weights, and claims to remain effective even on **dense weights with 0% sparsity**.

## Problem
- FFN/matrix multiplication in large-model inference is a primary bottleneck for computation and energy consumption, and existing dense/cuBLAS and sparse/cuSPARSE operators are limited in cost, latency, and energy efficiency.
- The industry generally believes that **sparse acceleration depends on explicit sparsity**, so it is skeptical of claims that one can achieve major speedups **without sparsity**; the author is trying to refute this.
- If inference compute and power costs can be directly reduced on existing GPU/CPU/mobile platforms, it would significantly affect cloud inference costs, edge deployment, and device battery life.

## Approach
- It proposes rolvsparse© as a new “compute primitive” that **restructures matrix arithmetic** to reduce the number of multiply-accumulate operations actually executed, thereby increasing throughput and lowering energy use.
- The method claims to work with **real model weights**, across multiple platforms (NVIDIA/AMD/Intel/TPU/Apple/mobile SoC), and **requires no hardware changes and no model retraining**.
- The paper/page focuses on **LLM FFN layer benchmarking**: it uses real HuggingFace weights to evaluate open models; for closed models such as GPT-4o and Claude 3.5, it uses **architecture-matched synthetic fp32 weights**.
- The author uses **SHA-256 output hashes** and a so-called canonical check to demonstrate cross-platform numerical consistency and reproducibility, and cites third-party organizations for independent verification.

## Results
- On **NVIDIA B200**, the author claims that for **Llama-4 Maverick MoE expert FFN** using real weights, it achieves **133.5× throughput improvement**, **99.9% energy reduction**, and **52.1× TTFT improvement**; for **Llama-4 400B** it reports **125.3×** and **100.9× TTFT**; for **DeepSeek-R1** it reports **44.2×**.
- For architecture-matched benchmarks of closed models, at **B=512** (which the author says is where cuBLAS is fully optimized), it claims **68.7× (GPT-4o class)** and **83× (Claude 3.5 class)**, with corresponding cuBLAS p99 latencies of **16.6 ms** and **29.0 ms**.
- On **Llama 4 Maverick**, the author reports energy dropping from **786 J to 50.6 J / 1000 iterations**, i.e. a **93.6% reduction**, while also claiming output is fully identical.
- On an **HP All-in-One (Intel i7-1165G7, 4 cores)** using real HuggingFace weights, the author claims **Mistral-7B** is **127× faster** than CPU dense and **474× faster** than the vendor’s best sparse operator; **TTFT 0.7 ms vs 13.4 ms**; **99.2% lower energy use**; and emphasizes that this occurs at **0% sparsity**.
- On **AMD MI300X**, the article claims up to **242× sparse speedup**; at **≥80% sparsity**, an approximately **$2,000 dual-Xeon** system can match or exceed optimized cuBLAS performance on a **$35k–$40k NVIDIA B200**, though this comparison uses different matrix sizes, which the author says still favors NVIDIA.
- On credibility: the article repeatedly emphasizes that results were independently verified by the **University of Miami Frost Institute**, that output hashes are consistent across platforms, and that results are reproducible; however, based on the provided excerpt, the content looks more like **product/benchmark claims** than a complete academic paper, and some key results rely on **synthetic weights** for closed models rather than real weights.

## Link
- [https://rolv.ai/](https://rolv.ai/)
