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
language_code: zh-CN
---

# Out-of-core LLM inference engine written from scratch in Rust

## Summary
## 摘要
Kortex 是一个 Rust LLM 推理引擎，通过在 NVMe、RAM、VRAM 和 GPU 计算之间流式传输权重，运行大于 GPU VRAM 的模型。它最强的主张是：在 20 GB Radeon RX 7900 XT 上运行 Llama-3.3-70B Q4_K_M，速度约为 2 tok/s；同一台机器上，llama.cpp 部分卸载的速度为 0.21 tok/s。

## 问题
- 大型 GGUF 模型经常超过消费级 GPU 的 VRAM，因此常见的部分卸载运行器会把部分层放到 CPU 上，并碰到系统 DRAM 带宽限制。
- 这很关键，因为 70B 量化模型要在 20 GB GPU 上可用，推理就必须在权重经过较慢的存储和内存层级时让 GPU 计算保持忙碌。
- 该项目还提供了 GGUF 解析、分词、量化 GPU kernel 和解码的独立 Rust 实现，并与 llama.cpp 做 token 级检查。

## 方法
- Kortex 把解码当作流式调度：层权重放在 VRAM 中、缓存在 RAM 中，或从 NVMe 读取，然后在 GPU 计算相邻层时通过一组 VRAM 环形槽移动。
- Windows 流式路径使用 Win32 无缓冲直接 I/O、RAM 缓存层、可选的第二块 NVMe 硬盘上的镜像模型副本读取，以及导入到 wgpu 的 Vulkan staging memory。
- 对于流式模型，所有模型计算都留在 GPU 上；Kortex 将权重流式传到 GPU，而不是在 CPU 上计算未驻留的层。
- 量化权重在融合的 WGSL matmul kernel 内反量化，KV cache 以 packed f16 存储，以减少内存流量。
- 推测解码使用一个小型 VRAM 驻留 draft model 提出 token，然后通过大模型的一次前向传递验证多个位置。

## 结果
- 在一台测试机器上，Radeon RX 7900 XT 20 GB、32 GB RAM、两块 NVMe 硬盘、Windows 11，Kortex 运行 Llama-3.3-70B Q4_K_M，权重 42.5 GB，速度为 1.95 tok/s，描述为约 2 tok/s。
- 在同一 70B 配置上，llama.cpp b9860 Vulkan 卸载 80 层中的 30 层，达到 0.21 tok/s；Kortex 声称通过避免 CPU 端层执行获得约 9x 加速。
- 对于一个完全驻留在 VRAM 中的 30B MoE 模型，Kortex 报告 160 tok/s，并且输出与 llama.cpp token 完全一致。
- 对于能放入 VRAM 的 dense 8B 模型，llama.cpp 普通解码快约 20%；在引用的对比中，使用推测解码时，Kortex 报告 114 tok/s，llama.cpp 为 109 tok/s。
- 正确性主张包括：greedy 输出与 llama.cpp 逐 token 匹配，流式执行与完全驻留执行匹配，speculative greedy 与 plain greedy 匹配，perplexity 与 llama.cpp 的差异在 0.6% 以内。
- 当前限制很具体：流式运行仅支持 Windows 11，没有 HTTP server 或多轮 REPL，当前会拒绝 streamed MoE，Qwen3-30B MoE 完全驻留需要约 18 GB VRAM，Linux 支持已计划但尚未测试。

## Problem

## Approach

## Results

## Link
- [https://github.com/Vage91/Kortex](https://github.com/Vage91/Kortex)
