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
本文提出 SWEzze，一个面向基于 LLM 的软件问题修复的代码上下文压缩器。它从经过 oracle 蒸馏的最小充分上下文中学习，在提升 SWE-bench Verified 上修复成功率的同时缩短提示长度。

## 问题
- 许多 LLM 问题修复系统会把过多仓库代码放进提示词，这会抬高推理成本，也会让模型把注意力放到无关代码上，而不是修复问题所需的证据上。
- 现有压缩器要么把代码当作普通文本处理，破坏有用的程序结构；要么只按浅层相似度裁剪，丢掉修复所需的变量、表达式或类型信息等关键内容。
- 在真实的 GitHub 问题修复中，这一点很重要，因为所需的补丁上下文通常很稀疏，而且可能离 bug 描述或定位到的文件很远。

## 方法
- 论文定义了**最小充分上下文**：从检索到的代码中选出的最小 1-最小子集，只要保留它，修复模型就还能生成通过测试的补丁。
- 这些上下文由 **Oracle-guided Code Distillation (OCD)** 构建。OCD 使用修复加测试的 oracle、用于寻找通过测试子集的遗传算法，以及分层 delta debugging 来移除任何单独不必要的代码段。
- 搜索和裁剪都在文件、函数、类头和语句块等结构化单元上进行，省略的代码会用占位符替换，以保留提示词结构。
- 蒸馏得到的训练数据用于微调 **SWEzze**，这是一个基于 Qwen3-Reranker-0.6B、带 LoRA 的轻量级 cross-encoder。推理时，SWEzze 会为代码片段打分，并在 token 预算内贪心选择压缩后的上下文。
- 搜索由训练阶段的信号引导，包括与 gold patch 文件的重叠、失败测试覆盖情况，以及与参考补丁的符号重叠。

## 结果
- 在 **SWE-bench Verified** 上，使用 **GPT-5.2、DeepSeek-V3.2 和 Qwen3-Coder-Next** 时，SWEzze 的压缩率稳定在约 **6x**。
- 相比未压缩设置，它把总 token 预算降低了 **51.8% 到 71.3%**。
- 在三种前沿模型上，它把问题修复成功率提高了 **5.0% 到 9.2%**。
- 与之前的上下文压缩器相比，论文声称它在修复效果、压缩率和延迟之间的平衡最好，并且 SWEzze 覆盖了任一基线方法能解决实例并集的 **93.8% 到 99.2%**。
- 在一个 Matplotlib 案例中，SWEzze 相对蒸馏出的最小上下文达到了 **BERTScore 0.44**，而 LongCodeZip 为 **0.20**，SWE-Pruner 为 **0.00**。
- 在训练数据方面，OCD 从 **41** 个仓库中蒸馏出 **3,157** 个成功实例，共 **156,545** 个已标注片段；只有 **8.4%** 的片段相关，去掉遗传算法后，成功最小化的实例减少了 **52.7%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28119v1](http://arxiv.org/abs/2603.28119v1)
