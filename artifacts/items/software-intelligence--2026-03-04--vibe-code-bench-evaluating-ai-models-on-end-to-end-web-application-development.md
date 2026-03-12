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
- benchmarking
- code-generation
- web-app-development
- agentic-coding
- browser-agent-evaluation
relevance_score: 0.95
run_id: materialize-outputs
---

# Vibe Code Bench: Evaluating AI Models on End-to-End Web Application Development

## Summary
本文提出 Vibe Code Bench，一个专门评测模型是否能从自然语言需求**端到端构建并部署完整 Web 应用**的基准。结果表明，即使最强模型在测试集上也只有 **61.8%** 准确率，说明“从零到一”的可靠自动开发仍远未解决。

## Problem
- 现有代码基准多评测函数生成、补丁修复或局部任务，无法衡量模型是否能**从零搭建完整可用应用**。
- 真实“vibe coding”需要跨越多文件开发、配置、部署、数据库、认证、支付/邮件集成和前端交互，这比单点代码题更重要也更难。
- 缺少统一、可复现、实现无关的评测方法，会让行业高估模型在真实软件生产中的能力。

## Approach
- 构建了一个包含 **100** 个 Web 应用规格的基准：**50** 个公开验证任务、**50** 个保留测试任务，总计 **964** 个浏览器工作流、**10,131** 个子步骤。
- 每个模型在统一的 agent 开发环境中，从一段自然语言需求出发，用浏览器、终端和常见服务（如 **Supabase、MailHog、Stripe**）在最多 **5 小时** 内完成应用开发。
- 评测时不看内部代码，而是用 автономous 浏览器 agent 对部署后的应用执行端到端用户流程；若一个工作流中 **≥90%** 子步骤成功，则该工作流记为通过。
- 作者共评测 **16** 个前沿模型，并统计准确率、成本、时延、错误模式，以及“生成过程中是否自测”与最终表现之间的关系。
- 另外做了 evaluator 对齐研究，用跨评估器比较和外部人工标注来检验浏览器评测器是否稳定可靠。

## Results
- 测试集最好模型是 **GPT-5.3-Codex：61.77±4.71%**；其后是 **Claude Opus 4.6：57.57±4.37%**、**GPT-5.2：53.50±5.07%**、**Claude Opus 4.6 Thinking：53.50±4.68%**、**Claude Sonnet 4.6：51.48±4.64%**。这说明完整 Web 应用自动开发仍是前沿难题，而非已基本解决的问题。
- 基准区分度很强：文中称 **MiniMax M2.5 与 Claude Opus 4.6** 在 **SWE-Bench** 上仅差 **2.8%**，但在 **Vibe Code Bench** 上相差 **42.7%**。
- 难度分层显示性能急剧下滑：对 **GPT-5.3-Codex**，Easy/Medium/Hard 分别为 **81.88% / 57.91% / 13.13%**；所有模型平均值分别为 **44.29% / 21.36% / 6.03%**。
- 外部集成显著增加难度：**GPT-5.3-Codex** 在无集成任务上为 **71.25%**，需要同时接入 **Email+Stripe** 时降到 **29.58%**；全模型平均从 **34.18%** 降到 **13.49%**。
- 成本/时延方面，**GPT-5.3-Codex** 达到 **61.77%**，平均成本 **$11.91**、时延 **75.8 分钟**；**Claude Opus 4.6** 以更低成本/时延达到接近表现：**57.57%**、**$8.69**、**21.3 分钟**。
- 自测行为是强预测信号：论文报告生成过程中浏览器自测频率与最终性能的相关性为 **Pearson r = 0.72**；同时评估器选择影响显著，不同评估器两两在步骤级别的一致率范围为 **31.8%–93.6%**。

## Link
- [http://arxiv.org/abs/2603.04601v1](http://arxiv.org/abs/2603.04601v1)
