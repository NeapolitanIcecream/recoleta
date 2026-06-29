---
source: arxiv
url: https://arxiv.org/abs/2606.01969v1
published_at: '2026-06-01T09:32:25'
authors:
- Lo Gullstrand Heander
- Agnia Sergeyuk
- Ilya Zakharov
- "Emma S\xF6derberg"
- Nikita Mukhortov
topics:
- code-review
- llm-generated-code
- human-ai-interaction
- developer-tools
- trust-calibration
- ide-workflows
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Trust-Calibrated Code Review: A Participatory Design Study of Review Workflows for LLM-Generated Multi-File Changes

## Summary
## 摘要
本文研究开发者应如何审查由 LLM 生成、跨多个文件的变更。核心结论是，IDE 审查工具应通过在合适的细节层级展示风险、理由和安全执行边界，帮助审查者校准信任。

## 问题
- 开发者越来越常审查由 LLM 代理生成的代码，但现有 IDE 和 diff 工具对判断大规模多文件变更的支持很弱。
- 这个任务很重要，因为当生成的变更看起来一致，但局部仍有失败时，审查者可能会漏掉 bug、安全风险、架构漂移或可维护性问题。
- 研究把信任校准确定为主要审查问题：审查者需要知道哪些文件、哪些行、哪些代理动作值得更仔细关注。

## 方法
- 作者与 JetBrains 一起做了一项参与式设计研究，使用 Double Diamond 流程：Discover、Define、Develop 和 Deliver。
- 在 Discover 阶段，17 名专业从业者识别了 LLM 生成的多文件变更带来的审查挑战；其中 7 人返回参加 Develop 阶段，绘制工作流和工具想法草图。
- 核心方法是一个三级审查工作流：overview 用于理解整体变更，file-analysis 用于按风险给文件排序，code-snippet review 用于检查具体行或代码块。
- 提出的工具设计使用 7 个构件：chunk、risk-per-line、risk-per-file、judge、walk-through、zooming in/out 和 security cage。
- 简单说，IDE 会先解释代理改了什么，然后指出高风险文件和行，再让审查者查看具体代码，并提供安全与置信度信号。

## 结果
- 工作坊参与者提出了 64 条挑战记录，分为 Trust、Lack of control、Quality 和 UI 四组；Trust 得到 17 票里 12 票红色“dangerous”票，Lack of control 得到其余 5 票。
- Define 阶段把挑战归纳为 12 个主题，包括 Broken code（13 次）、Intent misalignment（8 次）、Bad UI/UX（6 次）、Overcomplexity（6 次）、Cognitive load（6 次）、Lack of trust（5 次）和 Lack of transparency/explainability（5 次）。
- 验证问卷收到 97 份回复；其中 54 份被删除，因为它们很可能是 LLM 生成或无效回复，最后留下 43 份从业者回复。
- 问卷中，三个工作流层级的得分都高于中性中点，5 分量表上的平均 Likert 分数介于 3.50 到 3.91 之间。
- 63% 的受访者预计原型会比现有工具减少总体审查工作量，52% 的受访者预计会减少信任评估工作量。
- 论文没有报告受控审查实验中的代码质量提升、缺陷检测准确率或任务时间测量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.01969v1](https://arxiv.org/abs/2606.01969v1)
