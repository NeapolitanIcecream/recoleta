---
source: arxiv
url: http://arxiv.org/abs/2603.11078v1
published_at: '2026-03-10T21:29:42'
authors:
- Kristen Pereira
- Neelabh Sinha
- Rajat Ghosh
- Debojyoti Dutta
topics:
- code-review
- benchmarking
- llm-evaluation
- software-engineering
- agent-evaluation
relevance_score: 0.95
run_id: materialize-outputs
---

# CR-Bench: Evaluating the Real-World Utility of AI Code Review Agents

## Summary
本文提出 **CR-Bench** 与 **CR-Evaluator**，用于更真实地评估 AI 代码审查代理在实际 PR 中发现缺陷的能力。核心结论是：仅看“找出多少 bug”会误导，因为代码审查代理存在显著的**召回率—噪声**权衡。

## Problem
- 现有代码审查评测通常缺少统一、细粒度且贴近真实仓库的基准，难以判断代理在开放式 PR 审查中的真实效用。
- 代码审查不同于编译/测试，没有明确的客观 pass/fail 信号；若代理为追求高召回而产生大量误报，会直接伤害开发者体验与采用率。
- 以往数据集常混合主观风格问题与客观缺陷，且很多任务过于小规模或合成化，无法反映多文件、大仓库场景的重要难点。

## Approach
- 构建 **CR-Bench**：从 **SWE-Bench** 转换得到真实 PR 级代码审查数据，只保留“在代码评审阶段可合理发现”的客观缺陷；提供 **584** 个任务，以及人工加强验证的 **CR-Bench-verified 174** 个任务。
- 为每个样本保留完整 PR 上下文，并标注 **category / impact / severity** 分类，以支持按缺陷类型和风险进行分析。
- 提出 **CR-Evaluator**：用 LLM-as-a-judge 将代理输出的评论分为 **Bug Hit / Valid Suggestion / Noise** 三类。
- 在传统 **Precision / Recall / F1** 之外，增加 **Usefulness Rate** 与 **SNR**，显式衡量“有用反馈占比”与“信号相对噪声”的开发者可接受性。
- 用两种代理范式做初步实验：**single-shot**（单轮直接审查）与 **Reflexion**（迭代自我反思以补漏），并在 **GPT-5.2** 与 **GPT-5-mini** 上比较。

## Results
- 数据集规模与定位：**CR-Bench = 584**，**CR-Bench-verified = 174**；相较已有基准，作者强调其是首个聚焦**客观缺陷检测**、保留**完整 PR 上下文**并提供 **P/R/F1/Usefulness/SNR** 联合评估的代码审查基准。
- 数据复杂度：CR-Bench 平均每样本 **10.28** 行修复、**41.03** 条 PR 评论、PR 描述长度 **906.63**；verified 子集分别为 **8.69 / 35.83 / 893.59**，显示任务来自较大规模真实仓库。
- verified 子集分布：**79.9%** 为 Structural Bugs，**93.1%** 的缺陷为 **Medium/High severity**；完整 CR-Bench 中 **90.2%** 的缺陷为 **Medium/High/Critical**，说明评测偏向高风险、生产级问题。
- **Single-shot + GPT-5.2**：**Recall 27.01%**, **Precision 3.56%**, **F1 6.30%**, **Usefulness 83.63%**, **SNR 5.11**；作者将其解读为噪声更低、开发者信任度更高。
- **Reflexion + GPT-5.2**：**Recall 32.76%**, **Precision 5.10%**, **F1 8.83%**, **Usefulness 66.10%**, **SNR 1.95**；相对 single-shot，召回提升 **5.75** 个百分点（从 **27.01%** 到 **32.76%**），但信噪比明显下降。
- **GPT-5-mini** 上同样体现该权衡：single-shot 为 **Recall 18.39% / SNR 2.89**，Reflexion 为 **Recall 27.59% / SNR 0.91**。整体上，论文的关键发现不是某个代理“全面更强”，而是代码审查代理被一个“找更多 bug vs. 制造更多噪声”的前沿所约束。

## Link
- [http://arxiv.org/abs/2603.11078v1](http://arxiv.org/abs/2603.11078v1)
