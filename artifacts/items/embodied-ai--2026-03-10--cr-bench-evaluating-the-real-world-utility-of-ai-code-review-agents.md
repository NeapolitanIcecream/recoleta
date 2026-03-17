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
relevance_score: 0.03
run_id: materialize-outputs
---

# CR-Bench: Evaluating the Real-World Utility of AI Code Review Agents

## Summary
本文提出 **CR-Bench** 与 **CR-Evaluator**，用于更真实地评估 AI 代码审查代理在实际开发中的效用，而不只看是否“找到了问题”。核心结论是：代码审查代理存在明显的**召回率—噪声**权衡，高覆盖往往伴随更多误报，影响开发者信任与生产力。

## Problem
- 现有代码审查评测缺少统一、细粒度、贴近真实 PR 场景的基准，难以衡量代理在真实工作流中的价值。
- 仅看 resolution rate 或命中率会掩盖关键问题：**误报很多时，开发者体验会显著变差**，而这在代码审查中代价很高。
- 现有基准常混合主观风格问题与客观缺陷，且常缺少完整 PR/多文件上下文，无法充分评估真实缺陷检测能力。

## Approach
- 构建 **CR-Bench**：从 SWE-Bench 转换得到代码审查数据集，把真实仓库中的缺陷修复案例转成“在 PR 阶段是否应被审查发现”的任务。
- 通过 Git blame 与 GitHub API 回溯关联 PR，并用 LLM 过滤出**在代码审查阶段可检测**的缺陷；最终得到 **CR-Bench 584** 条、人工强化验证子集 **CR-Bench-verified 174** 条。
- 为每个样本生成审查评论目标与标签体系，覆盖 **bug category / impact / severity**，聚焦功能、性能、可靠性、安全等较客观的 defect-identifying reviews。
- 提出 **CR-Evaluator**：用 LLM-as-a-judge 将代理评论分成 **Bug Hit / Valid Suggestion / Noise** 三类，并计算 **Recall、Precision、F1、Usefulness Rate、SNR**。
- 用该框架评估两类代理：**single-shot** 一次性审查，与 **Reflexion** 迭代反思式审查；分别搭配 GPT-5.2 和 GPT-5-mini。

## Results
- 数据集规模上，作者声称 CR-Bench 是首个**聚焦客观缺陷检测且包含完整 PR 上下文**的代码审查基准：**CR-Bench 584** 条，**CR-Bench-verified 174** 条。
- 数据复杂度方面，CR-Bench 平均每实例 **10.28** 行修复、**41.03** 条 PR 评论、**906.63** 的 PR 描述长度；验证集分别为 **8.69 / 35.83 / 893.59**，说明任务具有较强真实上下文复杂度。
- 验证集缺陷分布中，**79.9%** 为 Structural Bugs，**93.1%** 为中高严重度；完整集里 **90.2%** 为 Medium/High/Critical，表明评测重点是高风险真实缺陷。
- 在 **CR-Bench-verified** 上，**Single-shot + GPT-5.2** 取得最高 **SNR 5.11**、**Usefulness 83.63%**，但 **Recall 27.01% / Precision 3.56% / F1 6.30%**，说明评论整体更“干净”但漏检较多。
- **Reflexion + GPT-5.2** 取得最高 **Recall 32.76%**、**Precision 5.10%**、**F1 8.83%**，相对 single-shot 的召回从 **27.01% 提升到 32.76%**；但 **Usefulness 降到 66.10%**、**SNR 降到 1.95**，表明更高覆盖伴随更多噪声。
- 较弱模型上，**Single-shot + GPT-5-mini** 为 **Recall 18.39% / Precision 3.51% / F1 5.90% / Usefulness 74.29% / SNR 2.89**；**Reflexion + GPT-5-mini** 为 **27.59% / 3.19% / 5.72% / 47.72% / 0.91**。最强结论是：**推动代理“多找 bug”会显著降低信噪比，真实可用性不能只看召回。**

## Link
- [http://arxiv.org/abs/2603.11078v1](http://arxiv.org/abs/2603.11078v1)
