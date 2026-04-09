---
source: arxiv
url: http://arxiv.org/abs/2604.03632v1
published_at: '2026-04-04T08:03:03'
authors:
- Ruwei Pan
- Jiangshuai Wang
- Qisheng Zhang
- Yueheng Zhu
- Linhao Wu
- Zixiong Yang
- Yakun Zhang
- Lu Zhang
- Hongyu Zhang
topics:
- repository-level-code-generation
- code-generation
- llm-agents
- cross-attempt-optimization
- software-engineering
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Persistent Cross-Attempt State Optimization for Repository-Level Code Generation

## Summary
## 摘要
LiveCoder 通过在同一任务的多次尝试之间保留任务特定状态，提升了仓库级代码生成效果。它会保存哪些方法有效、哪些方法失败，以及目前找到的最佳仓库，并用这些状态指导后续尝试，避免结果倒退。

## 问题
- 仓库级代码生成往往需要多次完整尝试，因为模型必须协调多个文件、模块和依赖关系。
- 现有方法通常将每次尝试分开优化，因此后续尝试可能重复错误路径，丢失有用的部分解，甚至比分数更早的仓库更差。
- 这很重要，因为在复杂软件任务中，重复进行完整尝试的生成成本高、不稳定，而且很常见。

## 方法
- 论文提出了 **LiveCoder**，一个用于仓库级代码生成的跨尝试优化框架。
- 每次完整尝试后，LiveCoder 会更新三类持久状态：来自高质量仓库的 **Success Knowledge**、来自低质量仓库和执行反馈的 **Failure Knowledge**，以及带有分数的 **historical-best repository**。
- Success 和 Failure Knowledge 以结构化文本形式存储，由 LLM 根据生成的仓库以及测试和运行时反馈提取；后续尝试会通过嵌入相似度检索相关条目，并将其注入生成过程。
- historical-best repository 会作为完整产物保留，因此如果它已经达到满分，系统可以直接复用它，并且在结束时始终返回当前最佳结果。
- 在这个循环中，每次新尝试都由先前证据引导，而不是从零开始。

## 结果
- 在 **RAL-Bench** 上，LiveCoder 报告称功能得分最高提升 **+22.94 个百分点**，仓库复用率最高达到 **81.58%**，从第一次到第四次尝试的成本最高降低 **53.63%**。
- 在 **RAL-Bench Table 1** 中，相比 **Direct** 基线，LiveCoder 在 **GPT-5** 上的功能得分达到 **58.20 vs 38.50**（**+19.70 分**），在 **DeepSeek-V3** 上为 **34.37 vs 24.37**（**+10.00**），在 **Claude-Sonnet-4.5** 上为 **67.00 vs 39.32**（**+27.68**），在 **Gemini-3-Pro** 上为 **69.16 vs 43.86**（**+25.30**）。
- 在同一张表中，非功能质量在更强的基础模型上通常具有竞争力或更高：**Claude-Sonnet-4.5** 从 **49.64** 升至 **64.81**，**Gemini-3-Pro** 从 **50.57** 升至 **67.03**；摘要称整体非功能质量大体保持稳定。
- 论文给出一个具体示例：基线在三次尝试中的得分分别为 **86%**、随后降到 **63%**、再到 **79%**，而 LiveCoder 从 **86%** 提升到 **92%**，并且当后续尝试更差时会保留更强的仓库。
- 摘要提到 **RAL-Bench** 和 **NL2Repo-Bench** 是评测基准，但所给的定量表格只展示了 **RAL-Bench** 的详细数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03632v1](http://arxiv.org/abs/2604.03632v1)
