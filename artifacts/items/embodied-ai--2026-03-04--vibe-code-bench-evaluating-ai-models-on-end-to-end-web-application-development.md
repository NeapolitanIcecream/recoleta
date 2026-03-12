---
source: arxiv
url: http://arxiv.org/abs/2603.04601v1
published_at: '2026-03-04T21:00:33'
authors:
- Hung Tran
- Langston Nashold
- Rayan Krishnan
- Antoine Bigeard
- Alex Gu
topics:
- code-generation-benchmark
- web-application-development
- browser-agent-evaluation
- agentic-coding
- software-engineering
relevance_score: 0.03
run_id: materialize-outputs
---

# Vibe Code Bench: Evaluating AI Models on End-to-End Web Application Development

## Summary
本文提出 Vibe Code Bench，一个评测模型是否能从自然语言需求直接构建可部署 Web 应用的端到端基准。结果显示，即使最强模型在测试集上也只有 61.8% 工作流通过率，说明“从零做出完整应用”仍远未被可靠解决。

## Problem
- 现有代码基准多评测函数补全、修 bug 或局部修改，不能衡量从零开始构建完整应用的真实能力。
- 对实际用户而言，真正重要的是模型能否把一段非技术需求变成可运行、可部署、可交互的软件，这直接关系到 AI 是否能扩大软件创造者范围。
- 缺少统一、实现无关、可复现的评测框架，使不同模型在完整应用开发上的能力难以公平比较。

## Approach
- 作者构建了一个包含 **100** 个 Web 应用规格的基准，分为 **50** 个公开验证任务和 **50** 个隐藏测试任务，覆盖 **964** 个浏览器工作流和 **10,131** 个子步骤。
- 每个模型在容器化开发环境中从文本规格出发，使用浏览器、终端以及常见服务（如 Supabase、MailHog、Stripe）在最多 **5 小时** 内开发完整应用。
- 评测时不看源码或固定 DOM 选择器，而是用自治浏览器代理直接像用户一样操作应用；当某工作流 **≥90%** 子步骤成功时记为通过。
- 该方法的核心可以简单理解为：**先让模型独立把应用做出来，再让另一个浏览器代理实际点点看、走完整流程，检查用户是否真的能用。**
- 论文还加入评测器对齐分析，比较不同自动评测器与人工标注之间的一致性，验证评测选择会显著影响结论。

## Results
- 在 **16** 个前沿模型上，测试集最好成绩为 **GPT-5.3-Codex: 61.77% ± 4.71**，其后是 **Claude Opus 4.6: 57.57% ± 4.37**、**GPT-5.2: 53.50% ± 5.07**、**Claude Sonnet 4.6: 51.48% ± 4.64**；最差的 **Grok 4.1 Fast Reasoning** 仅 **1.20% ± 1.20**。
- 该基准比现有代码基准更有区分度：论文称 **MiniMax M2.5 与 Claude Opus 4.6** 在 **SWE-Bench** 上只差 **2.8%**，但在 **Vibe Code Bench** 上差距达到 **42.7%**。
- 难度分层上，GPT-5.3-Codex 在 **Easy/Medium/Hard** 任务上的准确率分别为 **81.88% / 57.91% / 13.13%**；全模型平均分别为 **44.29% / 21.36% / 6.03%**，说明高难任务几乎仍未解决。
- 外部集成显著拉低表现：GPT-5.3-Codex 从**无集成**任务的 **71.25%** 降到同时需要 **Email+Stripe** 任务的 **29.58%**；全模型平均从 **34.18%** 降到 **13.49%**。
- 作者发现开发过程中的**自测行为**与最终性能强相关，Pearson 相关系数为 **r = 0.72**，表明会主动在浏览器里测试自己应用的模型通常做得更好。
- 评测器选择会实质影响结果：不同评测器之间的成对步骤级一致性范围为 **31.8%–93.6%**；论文据此强调评测对齐本身也是该方向的重要问题。

## Link
- [http://arxiv.org/abs/2603.04601v1](http://arxiv.org/abs/2603.04601v1)
