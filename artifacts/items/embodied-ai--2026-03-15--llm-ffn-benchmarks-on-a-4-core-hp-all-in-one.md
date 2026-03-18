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
---

# LLM FFN benchmarks on a 4‑core HP All‑in‑One

## Summary
该文介绍了 rolvsparse©，一种据称可在**不改硬件、不中断现有模型、无需重训**的前提下，重构矩阵乘法执行方式的新计算原语。核心卖点是在多种硬件和真实/结构匹配模型权重上，实现极高吞吐与能耗优势，且声称即使在**0%稀疏度的稠密权重**上也有效。

## Problem
- 大模型推理中的 FFN/矩阵乘法是主要计算与能耗瓶颈，现有 dense/cuBLAS 与 sparse/cuSPARSE 算子在成本、延迟和能效上受限。
- 业界通常认为**稀疏加速依赖显式稀疏性**，因此对“无需稀疏也能显著提速”的说法持怀疑态度；作者试图反驳这一点。
- 若能在现有 GPU/CPU/移动端上直接减少推理算力和电力开销，将显著影响云推理成本、边缘部署和设备续航。

## Approach
- 提出 rolvsparse© 作为新的“compute primitive”，通过**重构矩阵算术**来减少实际执行的乘加操作，从而提升吞吐并降低能耗。
- 方法声称适用于**真实模型权重**、多平台（NVIDIA/AMD/Intel/TPU/Apple/移动 SoC），且**无需硬件修改、无需模型重训**。
- 论文/页面重点在 **LLM 的 FFN 层基准测试**：使用真实 HuggingFace 权重评测开放模型；对 GPT-4o、Claude 3.5 等闭源模型，则采用**架构匹配的合成 fp32 权重**。
- 作者使用 **SHA-256 输出哈希**与所谓 canonical check 来证明跨平台数值一致与可复现，并引用第三方机构做独立验证。

## Results
- 在 **NVIDIA B200** 上，作者声称对 **Llama-4 Maverick MoE expert FFN** 用真实权重实现 **133.5× 吞吐提升**、**99.9% 能耗降低**、**52.1× TTFT 提升**；对 **Llama-4 400B** 为 **125.3×**，**TTFT 100.9×**；对 **DeepSeek-R1** 为 **44.2×**。
- 对闭源模型的架构匹配基准，在 **B=512**（作者称 cuBLAS 已充分优化）时，声称达到 **68.7×（GPT-4o class）** 和 **83×（Claude 3.5 class）**；对应 cuBLAS p99 延迟分别为 **16.6 ms** 和 **29.0 ms**。
- 在 **Llama 4 Maverick** 上，作者给出能耗从 **786 J 降至 50.6 J / 1000 iterations**，即 **93.6% 降低**，同时宣称输出完全一致。
- 在 **HP All-in-One（Intel i7-1165G7，4 核）** 上，使用真实 HuggingFace 权重，作者声称 **Mistral-7B** 相比 CPU dense **127× 更快**，相比厂商最佳 sparse operator **474× 更快**；**TTFT 0.7 ms vs 13.4 ms**；**能耗降低 99.2%**；并强调此结果发生在 **0% sparsity**。
- 在 **AMD MI300X** 上，文中声称可达 **242× sparse speedup**；在 **≥80% 稀疏度** 时，约 **$2,000 双 Xeon** 系统可匹配或超过 **$35k–$40k NVIDIA B200** 上优化 cuBLAS 的表现，但该比较使用了不同矩阵规模，作者称这仍偏向 NVIDIA。
- 可信度方面：文中反复强调结果经 **University of Miami Frost Institute** 独立验证、跨平台输出哈希一致、可复现；但从给定摘录看，内容更像**产品/基准宣称**而非完整学术论文，且部分关键结果依赖闭源模型的**合成权重**而非真实权重。

## Link
- [https://rolv.ai/](https://rolv.ai/)
