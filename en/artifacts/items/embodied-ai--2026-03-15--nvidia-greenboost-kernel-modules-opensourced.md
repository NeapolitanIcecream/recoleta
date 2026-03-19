---
source: hn
url: https://forums.developer.nvidia.com/t/nvidia-greenboost-kernel-modules-opensourced/363486
published_at: '2026-03-15T23:47:08'
authors:
- cma
topics:
- gpu-memory-extension
- cuda-shim
- kernel-module
- llm-inference
- dma-buf
relevance_score: 0.04
run_id: materialize-outputs
language_code: en
---

# Nvidia GreenBoost kernel modules opensourced

## Summary
GreenBoost is an open-source Linux kernel module plus CUDA shim that transparently extends GPU memory with system DDR4 and NVMe, allowing large models that exceed VRAM to run without modifying inference software. It is mainly aimed at running very large language models on consumer GPUs, rather than robotics or embodied foundation model research.

## Problem
- It addresses the problem of **insufficient VRAM on consumer GPUs**, which prevents running models larger than VRAM; for example, an RTX 5070 with 12 GB of VRAM cannot directly run the 31.8 GB `glm-4.7-flash:q8_0`.
- Existing alternatives are costly: CPU offload can reduce speed by **5–10×**, more aggressive quantization can hurt inference quality, and upgrading to a GPU with more VRAM is too expensive.
- This matters because running larger models on low-cost hardware is a common bottleneck in real-world deployment and personal research.

## Approach
- The core mechanism is a **three-tier memory extension**: T1 uses native GPU VRAM, T2 uses system DDR4 connected directly over PCIe, and T3 uses NVMe as a fallback overflow tier.
- The kernel module `greenboost.ko` allocates pinned-page DDR4 memory and exports it as **DMA-BUF**, then lets the GPU treat those pages as accessible “device memory” via `cudaImportExternalMemory`.
- The user-space shim `libgreenboost_cuda.so` intercepts large allocations such as `cudaMalloc`/`cuMemAllocAsync` through `LD_PRELOAD`, redirects allocations beyond VRAM to DDR4/NVMe, and then returns CUDA pointers to the upper-layer program.
- To support Ollama, it also intercepts `dlsym` and VRAM query interfaces so the program “sees” the expanded available memory, thereby avoiding incorrectly offloading layers to the CPU.
- The author also integrated ExLlamaV3, KV cache compression, and ModelOpt quantization. The core idea is: **first transparently expand capacity so the model can run, then compress as much as possible so it mainly uses VRAM/DDR4 and touches NVMe as little as possible**.

## Results
- On an **RTX 5070 12 GB**, the author claims to be able to run **31.8 GB** `glm-4.7-flash:q8_0`; the memory hierarchy is configured as **12 GB VRAM + 51 GB DDR4 + 64 GB NVMe**.
- Using **Ollama + GreenBoost shim**, decoding speed is about **2–5 tok/s**, with TTFT around **5–15 s**.
- With **kvpress 50% KV compression**, speed improves to **4–8 tok/s**, and TTFT drops to **3–10 s**.
- Using **ExLlamaV3 + GreenBoost cache**, it reaches **8–20 tok/s**, with TTFT of **2–8 s**.
- After compressing the model to about **16 GB** with **ModelOpt FP8**, it reaches **10–25 tok/s**, with TTFT of **1–5 s**.
- When using **ExLlamaV3 EXL3 2bpw**, with the model at about **8 GB** and fully fitting in VRAM, throughput peaks at **25–60 tok/s**, with TTFT of **0.5–2 s**; the author also explicitly notes that **PCIe 4.0 ~32 GB/s** is the main bottleneck when overflowing into DDR4.

## Link
- [https://forums.developer.nvidia.com/t/nvidia-greenboost-kernel-modules-opensourced/363486](https://forums.developer.nvidia.com/t/nvidia-greenboost-kernel-modules-opensourced/363486)
