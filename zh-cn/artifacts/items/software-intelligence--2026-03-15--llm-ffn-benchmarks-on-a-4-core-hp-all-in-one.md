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
language_code: zh-CN
---

# LLM FFN benchmarks on a 4‑core HP All‑in‑One

## Summary
这篇材料宣称提出了一个名为 rolvsparse 的新矩阵计算原语，可在不改硬件、不重训练模型的情况下，大幅减少 LLM/Transformer FFN 推理中的无效乘加，从而显著提升吞吐、降低首 token 延迟和能耗。其核心卖点是即使在真实权重、跨平台、甚至 0% 稀疏（作者称“完全稠密”）场景下，也能获得远高于现有 dense/sparse 算子的速度优势。

## Problem
- 现有 AI 处理器在矩阵乘法上主要依赖 dense 或传统 sparse 算子，导致 LLM FFN/MoE 推理存在大量无效计算、能耗高、TTFT 高、硬件成本高。
- 稀疏计算通常被认为必须依赖高稀疏度，且跨硬件复现性与正确性验证不足，这限制了其在真实模型权重上的采用。
- 对超大模型和端侧设备而言，推理成本、功耗和显存/内存效率直接影响可部署性与基础设施经济性，因此这是重要问题。

## Approach
- 提出 **rolvsparse** 这一“compute primitive”，从底层重构矩阵算术，目标是**跳过零值乘法**，减少实际执行的 multiply-accumulate 数量。
- 方法宣称**不需要硬件修改、模型重训练或模型结构改造**，可直接作用于 GPUs、TPUs、CPUs、移动 SoCs 等多类处理器。
- 针对开放模型使用 HuggingFace 真实权重；针对闭源模型（GPT-4o、Claude 3.5）使用架构匹配的 synthetic fp32 权重进行 FFN 基准测试。
- 结果通过 **SHA-256 输出哈希** 与 canonical check 做跨平台一致性验证，并引用独立机构（University of Miami Frost Institute）做可复现性确认。
- 另外提出 **RSMT** 作为稀疏存储何时优于稠密存储的阈值规则，但文中主要贡献仍是 rolvsparse 的算子级推理加速与节能。

## Results
- 在 **NVIDIA B200** 上，作者称对 **Llama-4 Maverick MoE expert FFN** 使用真实权重可实现 **133.5× 吞吐提升**、**99.9% 能耗下降**、**52.1× TTFT 加速**；对 **Llama-4 400B** 为 **125.3× 速度提升**、**100.9× TTFT**；对 **DeepSeek-R1** 为 **44.2×**。
- 在架构匹配的闭源模型 FFN 基准上，**B=512** 时相对 cuBLAS：**GPT-4o class 68.7×**、**Claude 3.5 class 83×**；文中给出 cuBLAS p99 分别为 **16.6 ms** 与 **29.0 ms**。
- 在 **Llama 4 Maverick** 能耗测试中，每 **1,000 iterations** 的能耗从 **786 J 降至 50.6 J**，即 **93.6% 降低**，并声称输出相同。
- 在一台 **$1,000 HP All-in-One（Intel i7-1165G7, 4 cores）** 上，运行 **Mistral-7B** 时，作者称相对 vendor dense **127× 更快**、相对 vendor sparse **474× 更快**；**TTFT 0.7 ms vs 13.4 ms**；**能耗降低 99.2%**；并强调这是在 **0% sparsity**、真实权重条件下。
- 在 **AMD MI300X** 上，材料声称可获得 **242× sparse speedup**；在 **≥80% sparsity** 时，一台约 **$2,000 dual-Xeon** 服务器可“匹配或超过”约 **$40,000 B200** 上的优化 cuBLAS，但该比较同时涉及不同矩阵规模，严格可比性有限。
- 文中没有给出完整论文式实验表、误差区间或同行评审细节；多数结果来自项目页面/基准摘要。最强主张是：**跨 NVIDIA/AMD/Intel/TPU/Apple 可复现、哈希一致、真实权重下可获得数量级级别的推理速度和能耗改进**。

## Link
- [https://rolv.ai/](https://rolv.ai/)
