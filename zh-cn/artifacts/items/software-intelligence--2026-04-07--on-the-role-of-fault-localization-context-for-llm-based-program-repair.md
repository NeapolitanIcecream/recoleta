---
source: arxiv
url: http://arxiv.org/abs/2604.05481v1
published_at: '2026-04-07T06:21:55'
authors:
- Melika Sepidband
- Hung Viet Pham
- Hadi Hemmati
topics:
- program-repair
- fault-localization
- llm-code
- swe-bench
- empirical-study
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# On the Role of Fault Localization Context for LLM-Based Program Repair

## Summary
## 总结
本文研究故障定位上下文对基于 LLM 的程序修复有多大帮助。作者在 500 个 SWE-bench Verified 任务上使用 GPT-5-mini 进行实验，发现文件级上下文最重要，更宽的上下文只在部分情况下有帮助，额外的行级上下文往往会带来负面影响。

## 问题
- 基于 LLM 的程序修复仍然依赖故障定位，但以往工作没有测试文件级、元素级和行级上下文如何影响修复成功率。
- 更多上下文可能帮助模型理解 bug，也可能引入无关代码、提高 token 成本，并掩盖真正的修改位置。
- 这对 APR 系统设计很重要，因为在大型代码库中，定位会同时影响修复质量和推理成本。

## 方法
- 作者在 **500 个 SWE-bench Verified** 实例上，使用 **GPT-5-mini** 做了一个包含 **61 种故障定位配置** 的因子研究。
- 他们在三个层级上变化上下文：**文件**（无、bug 文件、基于规则的相关文件、LLM 检索文件）、**元素**（无、bug 元素、调用图元素、LLM 检索元素）和 **行**（无、bug 行、±10 行窗口、静态切片、LLM 检索行）。
- 为了隔离上下文质量的影响，他们使用 **真实补丁位置** 来定义有问题的文件、元素和行，然后测试超出这些位置扩展上下文是否有帮助。
- 他们比较了语义型 LLM 检索和结构化启发式方法，并同时测量上下文大小和 token 成本。

## 结果
- **文件级上下文是主要驱动因素**：加入文件上下文带来相对无文件基线 **15–17 倍** 的提升。
- 当提示中包含大约 **6–10 个相关文件** 时，成功修复最常见。
- **基于 LLM 的文件检索** 在大多数设置下优于基于规则的文件扩展，而且使用的上下文更少：LLM 检索平均为 **8.54 个文件 / 58,273 个 token**，而基于规则的检索为 **18.12 个文件 / 96,237 个 token**。
- 真实 bug 文件平均为 **1.25 个文件**，每个实例大约 **12,131 个 token**。
- **元素级上下文** 比没有元素信息更有帮助，但在 bug 元素之外继续扩展是否有效，取决于文件上下文质量；在大多数配置中，**LLM 检索的元素** 比 **调用图元素** 表现更好。
- **行级扩展往往会拖累效果**：上下文窗口和静态切片经常降低修复性能，而精确的 **bug 行** 表现更好；该摘要没有报告 61 种配置全部对应的完整修复率百分比。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05481v1](http://arxiv.org/abs/2604.05481v1)
