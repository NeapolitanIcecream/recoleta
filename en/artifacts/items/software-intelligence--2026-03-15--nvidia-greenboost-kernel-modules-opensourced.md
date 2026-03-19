---
source: hn
url: https://forums.developer.nvidia.com/t/nvidia-greenboost-kernel-modules-opensourced/363486
published_at: '2026-03-15T23:47:08'
authors:
- cma
topics:
- gpu-memory-extension
- cuda-shim
- llm-inference
- linux-kernel-module
- consumer-gpu
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Nvidia GreenBoost kernel modules opensourced

## Summary
GreenBoost is an open-source Linux kernel module plus CUDA shim that transparently extends GPU VRAM with system DDR4 and NVMe, allowing large models that exceed VRAM to run without modifying inference software. It mainly targets the problems of insufficient VRAM when running large models on consumer GPUs, CPU offload being too slow, and the high cost of upgrading to a larger GPU.

## Problem
- The target problem is that 12 GB-class consumer GPUs cannot directly fit large models around 31.8 GB, while traditional CPU offload reduces inference speed by **5–10×**.
- Smaller quantization can hurt quality, while buying a 48 GB-class GPU significantly increases hardware cost, so a VRAM extension solution that is nearly transparent within the existing CUDA software stack is needed.
- This problem matters because it directly affects local LLM inference, long-context KV cache, and model usability on consumer hardware.

## Approach
- The core mechanism is a **three-tier memory hierarchy**: T1 is GPU VRAM (12 GB, about **336 GB/s**), T2 is DDR4 exposed to the GPU through PCIe 4.0 + DMA-BUF (51 GB, about **32 GB/s**), and T3 is the NVMe overflow tier (64 GB, about **1.8 GB/s**).
- The `greenboost.ko` kernel module allocates pinned-page DDR4 memory and exports it as DMA-BUF; on the CUDA side, it is used as device-accessible memory via `cudaImportExternalMemory`, thereby avoiding CPU copies.
- `libgreenboost_cuda.so` intercepts large allocations such as `cudaMalloc` / `cuMemAllocAsync` through `LD_PRELOAD`, redirects weights or KV cache that exceed VRAM into the DDR4 pool, and then maps them back to CUDA pointers.
- To remain compatible with Ollama’s behavior of resolving GPU symbols through `dlopen`/`dlsym`, the shim also intercepts `dlsym` and spoofs visible total VRAM and NVML memory information, preventing frameworks from mistakenly offloading layers to the CPU.
- The project also integrates tools such as ExLlamaV3, kvpress, ModelOpt, TensorRT-Edge-LLM, and Unsloth/LoRA for KV compression, post-training quantization, and better memory layout.

## Results
- On the author's **i9-14900KF + RTX 5070 12 GB + 64 GB DDR4 + PCIe 4.0 + 4 TB NVMe** machine, it successfully ran **`glm-4.7-flash:q8_0` (31.8 GB)** without modifying inference software.
- Using **Ollama + GreenBoost shim** directly, decoding speed was about **2–5 tok/s**, with TTFT around **5–15s**.
- After adding **kvpress 50% KV compression**, speed improved to **4–8 tok/s**, and TTFT dropped to **3–10s**.
- Using **ExLlamaV3 + GreenBoost cache**, it reached **8–20 tok/s**, with TTFT of **2–8s**.
- After further compressing the model to about **16 GB** with **ModelOpt FP8**, it reached **10–25 tok/s**, with TTFT of **1–5s**.
- If **ExLlamaV3 EXL3 2bpw** is used to shrink the model to about **8 GB and fit it entirely in VRAM**, performance can reach **25–60 tok/s**, with TTFT of **0.5–2s**; the author explicitly notes that the bottleneck is PCIe 4.0 bandwidth (about **32 GB/s**), and that the best strategy is still to shrink the model back into VRAM as much as possible, using DDR4 mainly for KV cache.

## Link
- [https://forums.developer.nvidia.com/t/nvidia-greenboost-kernel-modules-opensourced/363486](https://forums.developer.nvidia.com/t/nvidia-greenboost-kernel-modules-opensourced/363486)
