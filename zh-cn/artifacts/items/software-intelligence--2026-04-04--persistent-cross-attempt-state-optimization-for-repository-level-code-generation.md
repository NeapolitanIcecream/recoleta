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
## 总结
LiveCoder 通过在同一任务的重复尝试之间保留任务特定状态，提升了仓库级代码生成。它保存哪些做法有效、哪些做法失败，以及当前找到的最佳仓库，再用这些状态指导后续尝试，避免退化。

## 问题
- 仓库级代码生成通常需要多次完整尝试，因为模型必须协调多个文件、模块和依赖。
- 现有方法通常把每次尝试单独优化，所以后续尝试可能重复错误路径、忘记有用的部分解，甚至比早先的仓库得分更低。
- 这很重要，因为重复的完整尝试生成成本高、稳定性差，而且在复杂软件任务中很常见。

## 方法
- 论文提出 **LiveCoder**，这是一个面向仓库级代码生成的跨尝试优化框架。
- 每次完整尝试后，LiveCoder 会更新三类持久状态：来自强仓库的 **Success Knowledge**，来自弱仓库和执行反馈的 **Failure Knowledge**，以及带有分数的 **historical-best repository**。
- Success 和 failure knowledge 以结构化文本保存，由 LLM 从生成的仓库以及测试和运行反馈中抽取；后续尝试会通过嵌入相似度检索相关条目，并把它们注入生成过程。
- historical-best repository 作为完整产物保留，因此如果它已经达到满分，系统可以直接复用；结束时也会始终返回迄今为止最好的结果。
- 在这个循环中，每次新尝试都基于前面的证据，而不是从头开始。

## 结果
- 在 **RAL-Bench** 上，LiveCoder 的功能分数最高提升 **22.94 个百分点**，仓库复用率最高达到 **81.58%**，并且从第一次到第四次尝试的成本最高降低 **53.63%**。
- 在 **RAL-Bench 表 1** 中，与 **Direct** 基线相比，LiveCoder 在 **GPT-5** 上的功能分数达到 **58.20 对 38.50**（**+19.70** 分），在 **DeepSeek-V3** 上达到 **34.37 对 24.37**（**+10.00**），在 **Claude-Sonnet-4.5** 上达到 **67.00 对 39.32**（**+27.68**），在 **Gemini-3-Pro** 上达到 **69.16 对 43.86**（**+25.30**）。
- 在同一表中，非功能质量在更强的底座上通常具有竞争力，或更高：**Claude-Sonnet-4.5** 从 **49.64** 升到 **64.81**，**Gemini-3-Pro** 从 **50.57** 升到 **67.03**；摘要说整体上非功能质量基本保持稳定。
- 论文给出一个具体例子：基线在三次尝试中先得 **86%**，再降到 **63%**，然后回到 **79%**；而 LiveCoder 把 **86%** 提升到 **92%**，并在后一次尝试更差时保留更强的仓库。
- 摘要提到 **RAL-Bench** 和 **NL2Repo-Bench** 是评测基准，但给出的定量表只展示了 **RAL-Bench** 的详细数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03632v1](http://arxiv.org/abs/2604.03632v1)
