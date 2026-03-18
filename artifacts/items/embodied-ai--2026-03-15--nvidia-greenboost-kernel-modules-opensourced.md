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
---

# Nvidia GreenBoost kernel modules opensourced

## Summary
GreenBoost 是一个开源的 Linux 内核模块加 CUDA shim，用系统 DDR4 和 NVMe 透明扩展 GPU 显存，让超出 VRAM 的大模型无需修改推理软件即可运行。它主要面向消费级显卡上运行超大语言模型的场景，而不是机器人或具身基础模型研究。

## Problem
- 解决 **消费级 GPU 显存不足** 导致无法运行大于 VRAM 的模型，例如 12 GB 显存的 RTX 5070 无法直接运行 31.8 GB 的 `glm-4.7-flash:q8_0`。
- 现有替代方案代价高：CPU offload 会让速度下降 **5–10×**，更激进量化会损失推理质量，升级更大显存 GPU 成本过高。
- 这很重要，因为低成本硬件上运行更大模型是实际部署和个人研究中的常见瓶颈。

## Approach
- 核心机制是做一个 **三层显存扩展**：T1 用原生 GPU VRAM，T2 用通过 PCIe 直连的系统 DDR4，T3 用 NVMe 作为兜底溢出层。
- 内核模块 `greenboost.ko` 分配固定页 DDR4 内存并导出为 **DMA-BUF**，再让 GPU 通过 `cudaImportExternalMemory` 把这些页当成可访问的“设备内存”。
- 用户态 shim `libgreenboost_cuda.so` 通过 `LD_PRELOAD` 拦截 `cudaMalloc`/`cuMemAllocAsync` 等大块分配，把超出 VRAM 的分配重定向到 DDR4/NVMe，再返回 CUDA 指针给上层程序。
- 为适配 Ollama，它还拦截 `dlsym` 以及显存查询接口，让程序“看到”扩展后的可用显存，从而避免把层错误地下放到 CPU。
- 作者还集成 ExLlamaV3、KV cache 压缩和 ModelOpt 量化，核心思想是：**先透明扩容能跑，再尽量压缩到主要使用 VRAM/DDR4，而少碰 NVMe**。

## Results
- 在 **RTX 5070 12 GB** 上，作者声称可运行 **31.8 GB** 的 `glm-4.7-flash:q8_0`；内存层级配置为 **12 GB VRAM + 51 GB DDR4 + 64 GB NVMe**。
- 使用 **Ollama + GreenBoost shim** 时，解码速度约 **2–5 tok/s**，TTFT 约 **5–15 s**。
- 加上 **kvpress 50% KV compression** 后，速度提升到 **4–8 tok/s**，TTFT 降到 **3–10 s**。
- 使用 **ExLlamaV3 + GreenBoost cache** 时，达到 **8–20 tok/s**，TTFT **2–8 s**。
- 用 **ModelOpt FP8** 把模型压到约 **16 GB** 后，达到 **10–25 tok/s**，TTFT **1–5 s**。
- 当使用 **ExLlamaV3 EXL3 2bpw**、模型约 **8 GB** 且能完全放入 VRAM 时，速度最高到 **25–60 tok/s**，TTFT **0.5–2 s**；作者同时明确指出 **PCIe 4.0 ~32 GB/s** 是溢出到 DDR4 时的主要瓶颈。

## Link
- [https://forums.developer.nvidia.com/t/nvidia-greenboost-kernel-modules-opensourced/363486](https://forums.developer.nvidia.com/t/nvidia-greenboost-kernel-modules-opensourced/363486)
