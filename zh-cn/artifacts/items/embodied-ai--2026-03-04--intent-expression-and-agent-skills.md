---
source: hn
url: https://www.shincbm.com/agentic-code/2026/02/15/claude-skill-document-review.html
published_at: '2026-03-04T22:51:41'
authors:
- hogehoge51
topics:
- agentic-coding
- documentation-workflow
- llm-tools
- human-ai-collaboration
- prompt-scaffolding
relevance_score: 0.07
run_id: materialize-outputs
language_code: zh-CN
---

# Intent Expression and Agent Skills

## Summary
这篇文章提出了一套面向 agentic coding 的文档生成与审阅技能流水线，用结构化文档把“人脑中的意图”转成 agent 可稳定执行的输入。核心观点是：在智能体写代码时，清晰表达意图与分阶段审阅，比直接让模型“帮忙写”更能提升开发杠杆。

## Problem
- 它要解决的问题是：开发者把 AI 智能体接入传统“先在脑中想清楚、再直接写代码”的工作流时，往往得不到效率提升，因为关键瓶颈变成了**如何把意图清楚地外化给 agent**。
- 这很重要，因为当代码主要由 agent 生成时，文档不再只是事后产物，而是决定 agent 是否能正确实现、复用和持续迭代需求的核心接口。
- 文章还指出实际风险：LLM 会给人“文档已经完整”的错觉，可能产生幻觉、伪造链接、错误假设或冗余填充，若缺少检查点会把问题放大到实现阶段。

## Approach
- 核心方法是把文档工作拆成 3 个可复用 skills：`flesh-out`（从原始笔记扩展成结构化文档）、`review-steps`（分阶段润色、校验、最佳实践对照、链接验证）、`strong-edit`（先批判再修改，强化核心论点与可读性）。
- 最简单地说：先让 agent **理解你的意思**，再让它**整理和检查文档**，最后让它**挑战文档中最薄弱的地方**；每一阶段都暂停，等人确认后再继续，避免错误一路传递。
- 该机制依赖“docs as code”：文档与源码一起版本管理，使其成为人和 agent 的共享、可持续更新的参考，而不是一次性对话。
- 设计上强调“分工明确”：人类提供新想法、工程判断和最终决策；agent 负责结构化、语言润色、搜索框架、检查一致性与发现明显缺口。
- 文章还总结了若干行为规律：skill 文件式脚手架比把规则写进 `CLAUDE.md/AGENTS.md` 更稳定；不同术语如“review”“flesh-out”“strong-edit”会显著塑造模型行为。

## Results
- 在本文写作案例中，`/flesh-out` 把 **727 词**原始笔记扩展到 **2279 词**，约 **3.1x**；随后人工编辑把字数从 **2279** 降到 **2007**，约削减 **12%**，主要去掉 agent 生成的填充与 hedging。
- 同一案例中，`/review-steps` 又把内容增至 **2257 词**，加入了外部参考与观察；`/strong-edit` 最终压缩到约 **1930 词**，并改善开头论点、句子力度和论证结构。
- 一个关键负面结果促成方法改进：`/review-steps` 曾加入一个**伪造 URL**，而且该错误穿过人工编辑与 `strong-edit` 未被发现，最终促使作者新增 **Stage 6: verify links**，要求逐一验证链接可解析且能支撑所述主张。
- 在另一个 CPU 模型设计案例中，`/flesh-out` 将 **169 词**原始笔记扩展到 **1962 词**，约 **11.6x**；随后 agent 研究源码，发现 **21+** 个用户态汇编文件，分布于 **10** 个库模块和 **3** 个应用，推翻了原先“只有内核直接使用 ISA”的核心假设。
- 作者给出一个粗略经验值：在 `flesh-out` 的“Extract Idea”和 `strong-edit` 的“Core Argument”第 0 阶段，agent 对核心意图的把握约 **70%** 正确，剩余部分通过提问澄清。
- 文中还引用一项开发者信任数据：开发者对 AI 准确性的信任仅 **43%**；作者据此主张分阶段检查点和信息来源可追踪性，是降低盲目信任风险的关键。

## Link
- [https://www.shincbm.com/agentic-code/2026/02/15/claude-skill-document-review.html](https://www.shincbm.com/agentic-code/2026/02/15/claude-skill-document-review.html)
