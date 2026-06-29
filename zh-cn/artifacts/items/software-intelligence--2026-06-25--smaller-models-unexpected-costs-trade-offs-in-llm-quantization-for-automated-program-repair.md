---
source: arxiv
url: https://arxiv.org/abs/2606.27205v1
published_at: '2026-06-25T16:02:05'
authors:
- Fernando Vallecillos-Ruiz
- Giordano d'Aloisio
- Max Hort
- Luca Traini
- Antinisca Di Marco
- Leon Moonen
topics:
- llm-quantization
- automated-program-repair
- code-intelligence
- software-engineering
- energy-efficiency
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Smaller Models, Unexpected Costs: Trade-offs in LLM Quantization for Automated Program Repair

## Summary
## 摘要
本文表明，用于自动程序修复的 LLM 量化可以节省内存，但也可能改变被修复的 bug 集合，并提高推理成本。研究发现，在不同模型、基准和效率目标之间，没有单一的最佳量化设置。

## 问题
- 更大的代码 LLM 需要更高的 GPU 内存，这限制了本地 APR 使用，并提高了运行成本。
- 量化常用汇总基准分数来评判，但这些分数可能掩盖模型能修复哪些 bug 的变化。
- APR 需要这种分析，因为量化模型即使通过数量相近，也可能修复一组不同于基础模型的缺陷。

## 方法
- 作者评估了 13 种训练后量化配置，覆盖六个 LLM：Llama-3-8B、Llama-3-70B、DeepSeek-Coder-6.7B、DeepSeek-Coder-33B、Mistral-7B 和 Mixtral-8x7B。
- 他们测试了模型权重量化和 KV-cache 量化，在支持的情况下使用 AQLM、AWQ、BitsAndBytes、HQQ 和 Quanto，并采用 2、3、4、8 bit 设置。
- 他们在包含 164 个问题的 HumanEval-Java 和包含 525 个单函数 bug 的 Defects4J v2.0 子集上运行 APR。
- 他们测量 pass@10、通过提出的 Jaccard Consistency Rate 衡量的已解决集合重叠、推理时间、GPU 能耗、内存中的模型大小和峰值推理内存。
- 他们用帕累托支配关系比较配置，以找出在有效性和效率上都差于替代方案的设置。

## 结果
- 量化最多将内存占用降低 85%，但论文报告称，在许多设置中推理时间和能耗更高，原因归于测试栈上的硬件使用不佳。
- 在 HumanEval-Java 上，六个 LLM 中每一个都有至少一个量化变体超过基础模型。DeepSeek-Coder-6.7B 采用 quanto4 模型量化后，合理修复数从 90 提高到 107，增幅为 19%。
- 在 Defects4J 上，6 个模型案例中有 5 个的量化变体超过基础模型。DeepSeek-Coder-6.7B 的合理修复数从 43 提高到 82，增幅为 91%。
- 相近的修复数量往往来自不同的已解决问题集合，因此仅用 pass@10 无法捕捉量化后的行为变化。
- 极低 bit 设置经常失败：2 bit 或 3 bit 量化在多个案例中结果较弱，其中有四个案例在一个基准上只生成 0 或 1 个合理补丁。
- 帕累托分析发现，评估的量化配置中有 48% 被另一种设置严格支配。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.27205v1](https://arxiv.org/abs/2606.27205v1)
