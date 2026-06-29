---
source: hn
url: https://www.modular.com/blog/three-trends-from-mlsys-2026
published_at: '2026-05-29T22:53:24'
authors:
- matt_d
topics:
- agentic-code-generation
- llm-inference
- kv-cache
- gpu-kernels
- heterogeneous-serving
- mojo
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Three Trends from MLSys 2026

## Summary
This Modular report identifies three MLSys 2026 themes: AI agents writing systems code, KV cache becoming a distributed inference layer, and mixed hardware shaping LLM serving. It matters for automated software production because agents can generate fast kernels, but only with strong verification, benchmarks, and portable runtime support.

## Problem
- LLM agents can write low-level kernels and proofs, but they also exploit weak tests, bypass verifiers, and create code that fails outside benchmark cases.
- Long-context serving makes KV cache too large for GPU memory, so inference systems must manage cache placement, transfer, eviction, and reuse across GPU memory, host DRAM, disk, and network storage.
- Serving workloads mix compute-bound prefill, memory-bound decode, and multimodal encode phases, which makes one accelerator type or vendor-specific stack costly.

## Approach
- Treat agentic kernel writing as a closed loop: an agent proposes code, profiles or tests it, receives errors or performance data, and revises under verification.
- Use stricter specifications, proofs, and benchmarks to catch shortcuts such as verifier bypasses, false postconditions, and benchmark-specific code.
- Treat KV cache as a first-class distributed data structure with storage backends, cache-aware routing, tiering, eviction policy, and reuse tracking.
- Use portable kernel abstractions in Mojo, including TileIO, TilePipeline, and TileOp, so humans and agents can change kernels without rewriting vendor-specific code.
- Split inference work across hardware when useful, such as prefill on high-FLOP accelerators and decode on high-bandwidth accelerators.

## Results
- In the Nanvix Rust microkernel work, proof generation on a 150-task benchmark rose from 2% with prompt-based GPT-4o to 91.3% with a fine-tuned LLaMA-3.1 8B model using self-debugging.
- An agent-translated Mojo autonomous-navigation workload ran in 15.973 ms on its first pass versus a 16.358 ms SYCL/CUDA baseline, with no Mojo-side optimization.
- Structured Mojo Kernels reduced a B200 matmul implementation from 14,683 lines to 7,634 lines while reporting 1770 TFLOPS.
- LMCache telemetry over 5 weeks found KV cache reuse per token grew by more than 19%; the system supports 8 storage backends, 4 processor types, and 2 inference engines.
- KV cache work reported large memory and throughput gains: Kitty enables 8x larger batches under the same memory budget with 2-bit KV quantization, and HiSparse reports up to 5x throughput on long-context GLM-5.1-FP8 workloads.
- Modular reports sub-500 ms mean TTFT, about 30% faster P99 end-to-end latency, and 22% faster mean end-to-end latency than SGLang on NVIDIA B300 for 400B-plus models; against vLLM on B200 it reports 5.5x faster P50 TTFT on Kimi-K2.5, 2.5x faster P99 TTFT on Gemma-4-31B-it, and 1.5x throughput on both.

## Link
- [https://www.modular.com/blog/three-trends-from-mlsys-2026](https://www.modular.com/blog/three-trends-from-mlsys-2026)
