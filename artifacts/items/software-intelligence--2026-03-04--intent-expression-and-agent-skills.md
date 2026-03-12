---
source: hn
url: https://www.shincbm.com/agentic-code/2026/02/15/claude-skill-document-review.html
published_at: '2026-03-04T22:51:41'
authors:
- hogehoge51
topics:
- agentic-coding
- documentation-workflow
- claude-skills
- human-ai-collaboration
- prompt-engineering
relevance_score: 0.91
run_id: materialize-outputs
---

# Intent Expression and Agent Skills

## Summary
本文提出一套面向 agentic coding 的“文档即技能”流程，目标是把开发者脑中的意图更完整地外化为可复用、可审查的文档，从而提升代理生成代码与设计文档的质量。核心观点是：在代理编程中，清晰表达意图比直接写代码更能形成杠杆。

## Problem
- 代理写代码后，瓶颈从“写实现”转移到“能否清楚表达需求与设计意图”。
- 仅靠一次性 plan mode 或对话式提示，难以支撑跨任务、跨迭代、可版本管理的长期软件知识。
- LLM 文档生成存在误解原意、虚构引用、制造“已完成错觉”等风险，若无结构化检查，错误会传导到实现阶段。

## Approach
- 提出 3 个可复用 Claude Code 技能文件，形成文档流水线：`/flesh-out`（从原始笔记扩展成结构化文档）、`/review-steps`（分阶段审阅与核验）、`/strong-edit`（先批判再修改）。
- 采用“docs as code”思路，把文档与源码一起纳入工作区和配置管理，作为人类与代理共享的持久参考物，而不是易消失的聊天记录。
- 每个技能都拆成编号阶段，并在每一阶段设置开发者确认点；代理完成后暂停，等待人工批准，以降低语义漂移和幻觉扩散。
- 劳动分工上，人类提供新颖问题、意图与工程判断；代理负责结构化、行业实践检索、语言润色、一致性检查和链接验证等高重复工作。
- 通过词汇与流程约束来控制代理行为，例如“review”偏保守、“flesh-out”偏生成、“strong-edit”偏质疑，从而让同一模型进入不同工作模式。

## Results
- 在本文写作案例中，原始笔记 **727 词** 经 `/flesh-out` 扩展为 **2279 词**，约 **3.1x**；随后人工编辑删减约 **12%**（**2279 → 2007**），`/review-steps` 又补充引用和观察到 **2257 词**，最终 `/strong-edit` 收敛到约 **1930 词**。
- 作者报告在 `flesh-out` 的 Stage 0 与 `strong-edit` 的 Stage 0 中，代理对核心意图的首次把握“约 **70%** 正确”，其余部分通过追问澄清；这是文中少数明确给出的经验性准确度数字。
- 在另一个 CPU 模型设计案例中，**169 词**原始笔记被扩展为 **1962 词**设计文档，约 **11.6x**；随后代理检索源码，发现 **21+** 个用户态汇编文件，分布在 **10** 个库模块和 **3** 个应用中，从而推翻了“只有内核直接使用 ISA”的关键假设，并直接改写了设计结构。
- 文中给出一个失败案例：`/review-steps` 曾添加一个**伪造 URL**，且该错误穿过人工编辑与 `/strong-edit` 未被发现，最终促使作者新增 Stage 6“逐条验证链接是否可解析、是否支持文中论断”。
- 作者还引用外部调查称开发者对 AI 准确性的信任仅 **43%**，以说明为何分阶段检查点和可追溯信息来源对代理式软件生产很重要。
- 这不是严格学术评测论文，没有标准基准数据、对照实验或统计显著性结果；最强的结果是多个真实工作流案例中，结构化技能显著放大文档产出、暴露错误假设，并改善代理遵循流程的稳定性。

## Link
- [https://www.shincbm.com/agentic-code/2026/02/15/claude-skill-document-review.html](https://www.shincbm.com/agentic-code/2026/02/15/claude-skill-document-review.html)
