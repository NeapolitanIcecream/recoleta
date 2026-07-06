---
source: hn
url: https://github.com/Vage91/Kortex
published_at: '2026-07-04T22:47:59'
authors:
- Vage91
topics:
- llm-inference
- out-of-core-inference
- gpu-streaming
- rust
- gguf
- quantization
relevance_score: 0.64
run_id: materialize-outputs
language_code: en
---

# Out-of-core LLM inference engine written from scratch in Rust

## Summary
Kortex is a Rust LLM inference engine that runs models larger than GPU VRAM by streaming weights across NVMe, RAM, VRAM, and GPU compute. Its strongest claim is Llama-3.3-70B Q4_K_M on a 20 GB Radeon RX 7900 XT at about 2 tok/s, compared with 0.21 tok/s for llama.cpp partial offload on the same machine.

## Problem
- Large GGUF models often exceed consumer GPU VRAM, so common partial-offload runners place some layers on CPU and hit system DRAM bandwidth limits.
- This matters because a 70B quantized model can be usable on a 20 GB GPU only if inference keeps GPU compute busy while weights move through slower storage and memory tiers.
- The project also gives an independent Rust implementation of GGUF parsing, tokenization, quantized GPU kernels, and decoding, with token-level checks against llama.cpp.

## Approach
- Kortex treats decoding as a streaming schedule: layer weights are placed in VRAM, cached in RAM, or read from NVMe, then moved through a ring of VRAM slots while the GPU computes nearby layers.
- The Windows streaming path uses Win32 unbuffered direct I/O, a RAM cache tier, optional reads from a mirrored model copy on a second NVMe drive, and Vulkan staging memory imported into wgpu.
- All model compute stays on the GPU for streamed models; Kortex streams weights to the GPU instead of computing non-resident layers on the CPU.
- Quantized weights are dequantized inside fused WGSL matmul kernels, and the KV cache is stored as packed f16 to reduce memory traffic.
- Speculative decoding uses a small VRAM-resident draft model to propose tokens, then verifies several positions with one pass through the larger model.

## Results
- On one test machine, Radeon RX 7900 XT 20 GB, 32 GB RAM, two NVMe drives, Windows 11, Kortex runs Llama-3.3-70B Q4_K_M, 42.5 GB weights, at 1.95 tok/s, described as about 2 tok/s.
- On the same 70B setup, llama.cpp b9860 Vulkan with 30 of 80 layers offloaded reaches 0.21 tok/s; Kortex claims about a 9x speedup by avoiding CPU-side layer execution.
- For a fully VRAM-resident 30B MoE model, Kortex reports 160 tok/s and token-identical output against llama.cpp.
- For a dense 8B model that fits in VRAM, llama.cpp plain decode is about 20% faster; with speculative decoding, Kortex reports 114 tok/s versus 109 tok/s for llama.cpp in the cited comparison.
- Correctness claims include greedy output matching llama.cpp token-for-token, streamed execution matching fully resident execution, speculative greedy matching plain greedy, and perplexity within 0.6% of llama.cpp.
- Current limits are concrete: Windows 11 only for streaming, no HTTP server or multi-turn REPL, streamed MoE rejected today, Qwen3-30B MoE needs about 18 GB VRAM fully resident, and Linux support is planned rather than tested.

## Link
- [https://github.com/Vage91/Kortex](https://github.com/Vage91/Kortex)
