---
source: arxiv
url: http://arxiv.org/abs/2603.28119v1
published_at: '2026-03-30T07:31:12'
authors:
- Haoxiang Jia
- Earl T. Barr
- Sergey Mechtaev
topics:
- code-context-compression
- llm-program-repair
- swe-bench
- issue-resolution
- code-intelligence
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Compressing Code Context for LLM-based Issue Resolution

## Summary
## 摘要
这篇论文提出了 SWEzze，这是一种用于基于 LLM 的软件问题修复的代码上下文压缩器。它从经由 oracle 蒸馏得到的最小充分上下文中学习，在缩小提示规模的同时，提高了 SWE-bench Verified 上的修复成功率。

## 问题
- LLM 问题修复系统通常会把过多仓库代码放入提示中，这会提高推理成本，并让模型把注意力放在无关代码上，而不是修复 bug 所需的证据上。
- 现有压缩器要么把代码当作普通文本处理，破坏了有用的程序结构；要么按浅层相似性裁剪，丢掉修复所需的成分，例如必要的变量、表达式或类型信息。
- 这对真实的 GitHub 问题修复很重要，因为补丁所需的上下文很稀疏，而且可能远离 bug 描述或已定位的文件。

## 方法
- 论文定义了**最小充分上下文**：从检索到的代码中选出的最小 1-minimal 子集，只要保留它，修复模型仍能生成通过测试的补丁。
- 它用 **Oracle-guided Code Distillation (OCD)** 构建这些上下文。OCD 使用修复与测试 oracle、用于寻找可通过子集的遗传算法，以及分层 delta debugging，移除任何单独来看并非必要的代码片段。
- 代码搜索和裁剪是在文件、函数、类头、语句块等结构化单元上进行的，被省略的代码会用占位符替换，以便提示保持原有结构。
- 蒸馏后的训练数据用于微调 **SWEzze**。它是一个轻量级交叉编码器，基于带有 LoRA 的 Qwen3-Reranker-0.6B。在推理时，SWEzze 对代码片段打分，并在 token 预算内贪心选择压缩后的上下文。
- 搜索过程由训练阶段的信号引导，包括与金标准补丁文件的重合、失败测试覆盖，以及与参考补丁的符号重合。

## 结果
- 在 **SWE-bench Verified** 上，针对 **GPT-5.2、DeepSeek-V3.2 和 Qwen3-Coder-Next**，SWEzze 保持了大约 **6x** 的稳定压缩率。
- 相比未压缩设置，它将总 token 预算降低了 **51.8% 到 71.3%**。
- 与未压缩设置相比，它在这三个前沿模型上将问题修复率提高了 **5.0% 到 9.2%**。
- 与之前的上下文压缩器相比，论文称它在修复效果、压缩率和延迟之间取得了最佳平衡，并表示 SWEzze 覆盖了任一基线所解决实例并集中的 **93.8% 到 99.2%**。
- 在一个 Matplotlib 案例研究中，SWEzze 相对于蒸馏后的最小上下文达到了 **BERTScore 0.44**，而 LongCodeZip 为 **0.20**，SWE-Pruner 为 **0.00**。
- 在训练数据方面，OCD 从 **41** 个仓库中蒸馏出 **3,157** 个成功实例，总计 **156,545** 个带标签片段；其中只有 **8.4%** 的片段相关，而移除遗传算法后，成功完成最小化的实例数减少了 **52.7%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28119v1](http://arxiv.org/abs/2603.28119v1)
