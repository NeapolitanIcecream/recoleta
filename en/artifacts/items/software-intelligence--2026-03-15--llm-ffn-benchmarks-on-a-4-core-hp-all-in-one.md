---
source: hn
url: https://rolv.ai/
published_at: '2026-03-15T23:19:37'
authors:
- heggenhougen
topics:
- llm-inference
- matrix-acceleration
- sparse-computing
- ffn-benchmark
- energy-efficiency
relevance_score: 0.77
run_id: materialize-outputs
language_code: en
---

# LLM FFN benchmarks on a 4‑core HP All‑in‑One

## Summary
This material claims to introduce a new matrix-computation primitive called rolvsparse, which can greatly reduce ineffective multiply-accumulate operations in LLM/Transformer FFN inference without changing hardware or retraining models, thereby significantly improving throughput while reducing time-to-first-token and energy consumption. Its core selling point is that it reportedly achieves speed advantages far beyond existing dense/sparse operators even with real weights, across platforms, and even in 0% sparsity (which the author describes as "fully dense") scenarios.

## Problem
- Existing AI processors mainly rely on dense or traditional sparse operators for matrix multiplication, leading to substantial ineffective computation, high energy use, high TTFT, and high hardware cost in LLM FFN/MoE inference.
- Sparse computation is usually considered to require high sparsity, and cross-hardware reproducibility and correctness verification are insufficient, limiting adoption on real model weights.
- For ultra-large models and edge devices, inference cost, power consumption, and VRAM/memory efficiency directly affect deployability and infrastructure economics, making this an important problem.

## Approach
- Proposes **rolvsparse** as a "compute primitive" that reconstructs matrix arithmetic at a low level, with the goal of **skipping zero-value multiplications** and reducing the number of multiply-accumulate operations actually executed.
- The method claims to require **no hardware modifications, model retraining, or model-architecture changes**, and to work directly on GPUs, TPUs, CPUs, mobile SoCs, and other processor types.
- Uses real HuggingFace weights for open models; for closed-source models (GPT-4o, Claude 3.5), it uses architecture-matched synthetic fp32 weights for FFN benchmarking.
- Results are validated for cross-platform consistency through **SHA-256 output hashes** and canonical checks, and the material cites an independent institution (University of Miami Frost Institute) for reproducibility confirmation.
- It also proposes **RSMT** as a threshold rule for when sparse storage is preferable to dense storage, though the primary contribution discussed is still rolvsparse's operator-level inference acceleration and energy savings.

## Results
- On **NVIDIA B200**, the author claims that using real weights for **Llama-4 Maverick MoE expert FFN** achieves **133.5× throughput improvement**, **99.9% energy reduction**, and **52.1× TTFT speedup**; for **Llama-4 400B**, **125.3× speedup** and **100.9× TTFT**; for **DeepSeek-R1**, **44.2×**.
- In architecture-matched FFN benchmarks for closed-source models, at **B=512** relative to cuBLAS: **GPT-4o class 68.7×** and **Claude 3.5 class 83×**; the material reports cuBLAS p99 values of **16.6 ms** and **29.0 ms**, respectively.
- In **Llama 4 Maverick** energy tests, energy per **1,000 iterations** drops from **786 J to 50.6 J**, a **93.6% reduction**, while claiming identical output.
- On a **$1,000 HP All-in-One (Intel i7-1165G7, 4 cores)** running **Mistral-7B**, the author claims **127× faster** than vendor dense and **474× faster** than vendor sparse; **TTFT 0.7 ms vs 13.4 ms**; **99.2% lower energy use**; and emphasizes that this is under **0% sparsity** with real weights.
- On **AMD MI300X**, the material claims **242× sparse speedup**; at **≥80% sparsity**, an approximately **$2,000 dual-Xeon** server can reportedly "match or exceed" an approximately **$40,000 B200** running optimized cuBLAS, though this comparison also involves different matrix sizes, so strict comparability is limited.
- The material does not provide full paper-style experiment tables, error bars, or peer-review details; most results come from the project page / benchmark summaries. The strongest claim is: **reproducible across NVIDIA/AMD/Intel/TPU/Apple, hash-consistent, and capable of order-of-magnitude inference speed and energy improvements with real weights**.

## Link
- [https://rolv.ai/](https://rolv.ai/)
