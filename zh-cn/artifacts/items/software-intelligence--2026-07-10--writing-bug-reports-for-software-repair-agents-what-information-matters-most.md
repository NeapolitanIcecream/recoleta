---
source: arxiv
url: https://arxiv.org/abs/2607.09553v1
published_at: '2026-07-10T16:00:57'
authors:
- Vincenzo Luigi Bruno
- Alessandro Giagnorio
- Daniele Bifolco
- Leon Wienges
- Massimiliano Di Penta
- Gabriele Bavota
topics:
- software-repair-agents
- code-intelligence
- bug-reporting
- automated-software-production
- agentic-workflows
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Writing Bug Reports for Software Repair Agents: What Information Matters Most?

## Summary
## 摘要
论文研究哪些错误报告信息有助于软件修复代理生成能通过测试的补丁。研究发现，修复指导信息，尤其是受影响代码的位置和建议修复方案，比面向人工读者的冗长描述更有助于代理完成修复。

## 问题
- 在代理优先的软件开发中，错误报告会成为代理的任务说明，因此缺乏针对性的信息可能降低正确修复的成功率。
- 现有错误报告指南强调便于人工理解、复现过程和行为背景，但关于哪些信息能帮助自动化修复的证据仍然有限。

## 方法
- 作者为 SWE-bench Verified 中的全部 500 个问题标注九类信息；排除 41 个功能请求和 18 个重构任务后，保留 441 个缺陷报告。
- 作者使用 GPT-5-mini、MiniMax M2.5 和 Gemini 3 Flash 驱动的 mini-SWE-agent，并以测试套件通过情况衡量修复是否成功。
- 混合效应二项回归用于估计各类信息与代理成功率之间的关联，同时控制问题长度、代码提及次数、标准补丁大小、难度、模型和代码仓库效应。
- 消融实验从 65 个信息完整的报告中移除不同的信息类别，并评估 4,680 次经过修改的任务运行结果。

## 结果
- 研究使用了 3,969 次观察运行：441 个问题、3 个 LLM 主干模型，以及每个问题 3 次重复运行。提供的摘录没有包含确切的优势比和通过率提升数据。
- 定位线索，尤其是对受影响代码行和函数的引用，与修复成功呈正相关。
- 代码或自然语言中的建议修复方案与通过测试套件的概率之间呈现出较强的正相关。
- 当定位线索或修复建议仍然存在时，移除复现步骤或预期行为并不会显著降低代理的修复效果。
- 同时移除定位线索和建议修复方案会造成最大程度的性能下降。这支持了这样一个结论：能够缩小代码检查位置或指明代码修改方式的信息有助于代理完成修复。
- 标注覆盖 500 个问题中的 3,752 个文本片段，字符级一致率为 78.6%，问题级 Cohen's kappa 为 0.57；消融编辑过程的 kappa 达到 0.96。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.09553v1](https://arxiv.org/abs/2607.09553v1)
