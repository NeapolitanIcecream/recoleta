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
language_code: zh-CN
---

# Nvidia GreenBoost kernel modules opensourced

## Summary
GreenBoost 是一个面向 Linux 的开源内核模块加 CUDA shim，用系统 DDR4 与 NVMe 透明扩展 GPU 显存，使超出 VRAM 的大模型无需修改推理软件即可运行。它主要针对消费级显卡运行大模型时显存不足、CPU offload 太慢、升级更大显卡成本过高的问题。

## Problem
- 目标问题是：12 GB 级消费级 GPU 无法直接容纳 31.8 GB 这类大模型，而传统 CPU offload 会让推理速度下降 **5–10×**。
- 更小量化会损失质量，购买 48 GB 级显卡又显著提高硬件成本，因此需要一种在现有 CUDA 软件栈中几乎透明的显存扩展方案。
- 该问题重要，因为它直接影响本地 LLM 推理、长上下文 KV cache 和消费者硬件上的模型可用性。

## Approach
- 核心机制是一个 **三层内存体系**：T1 为 GPU VRAM（12 GB，约 **336 GB/s**），T2 为通过 PCIe 4.0 + DMA-BUF 暴露给 GPU 的 DDR4（51 GB，约 **32 GB/s**），T3 为 NVMe 溢出层（64 GB，约 **1.8 GB/s**）。
- `greenboost.ko` 内核模块分配固定页 DDR4 内存并导出为 DMA-BUF，CUDA 侧通过 `cudaImportExternalMemory` 把它当作设备可访问内存使用，从而避免 CPU 拷贝。
- `libgreenboost_cuda.so` 通过 `LD_PRELOAD` 拦截 `cudaMalloc` / `cuMemAllocAsync` 等大块分配，把超出 VRAM 的权重或 KV cache 重定向到 DDR4 池，再映射回 CUDA 指针。
- 为兼容 Ollama 通过 `dlopen`/`dlsym` 解析 GPU 符号的行为，shim 还拦截 `dlsym`，并伪装可见总显存与 NVML 内存信息，避免框架错误地把层卸载到 CPU。
- 项目还集成 ExLlamaV3、kvpress、ModelOpt、TensorRT-Edge-LLM、Unsloth/LoRA 等工具，用于 KV 压缩、后训练量化和更优内存布局。

## Results
- 在作者的 **i9-14900KF + RTX 5070 12 GB + 64 GB DDR4 + PCIe 4.0 + 4 TB NVMe** 机器上，成功运行 **`glm-4.7-flash:q8_0`（31.8 GB）**，而不修改推理软件。
- 直接使用 **Ollama + GreenBoost shim** 时，解码速度约 **2–5 tok/s**，TTFT 约 **5–15s**。
- 加入 **kvpress 50% KV compression** 后，速度提升到 **4–8 tok/s**，TTFT 降至 **3–10s**。
- 使用 **ExLlamaV3 + GreenBoost cache** 时，达到 **8–20 tok/s**，TTFT **2–8s**。
- 进一步用 **ModelOpt FP8** 将模型压到约 **16 GB** 后，达到 **10–25 tok/s**，TTFT **1–5s**。
- 若采用 **ExLlamaV3 EXL3 2bpw** 让模型缩到约 **8 GB 并完全放入 VRAM**，可达 **25–60 tok/s**，TTFT **0.5–2s**；作者明确指出瓶颈是 PCIe 4.0 带宽（约 **32 GB/s**），最佳策略仍是尽量把模型缩回 VRAM，只把 DDR4 主要用于 KV cache。

## Link
- [https://forums.developer.nvidia.com/t/nvidia-greenboost-kernel-modules-opensourced/363486](https://forums.developer.nvidia.com/t/nvidia-greenboost-kernel-modules-opensourced/363486)
