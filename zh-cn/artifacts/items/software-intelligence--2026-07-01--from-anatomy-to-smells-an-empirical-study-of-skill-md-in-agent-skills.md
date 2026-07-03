---
source: arxiv
url: https://arxiv.org/abs/2607.01456v1
published_at: '2026-07-01T20:21:33'
authors:
- David Boram Hong
- Aaron Imani
- Iftekhar Ahmed
topics:
- agent-skills
- skill-smells
- llm-agents
- software-quality
- code-intelligence
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# From Anatomy to Smells: An Empirical Study of SKILL.md in Agent Skills

## Summary
## 摘要
本文研究 Agent Skills 使用的 SKILL.md 文件，发现编写问题很普遍。论文定义了 SKILL.md 内容分类，提取了编写实践，并构建了一个检测器，用来发现被称为技能异味的违规情况。

## 问题
- Agent Skills 通过 SKILL.md 文件向 LLM 智能体提供任务特定指令，但 Markdown 正文基本不受约束，因此质量差的指导会浪费上下文，并把智能体行为引向不良方向。
- 现有研究关注技能有效性、安全性和优化；SKILL.md 编写质量以及对编写实践的违反缺少实证证据。
- 这个问题很重要，因为公开技能市场中已有超过 100,000 个技能，糟糕的 SKILL.md 模式可能通过复制的技能、生成的技能或未来训练数据传播。

## 方法
- 作者从 skills.sh 的一次转储中整理出 238 个英文 SKILL.md 文件；该转储包含来自 8,808 个发布者和 13,460 个代码库的 133,149 个技能，作者按下载量、代码库 star、去重和代码库多样性进行筛选。
- 两位作者在 H2 标题层级对 SKILL.md 正文进行定性编码，并构建了语义组件分类。
- 他们通过多声部文献综述审查了 29 个网页来源，提取 SKILL.md 编写最佳实践，并把违规情况反转定义为 26 种技能异味。
- 他们构建了 Skill Smell Detector，对 5 种可静态检测的异味使用脚本，对 21 种语义异味使用带 4-bit AWQ 量化的 Qwen3.6-27B。
- 他们挖掘了 1,295 条提交记录，随后分析了 142 个发生变化的 SKILL.md 文件，覆盖 1,199 次提交和 35 个每周时间窗口，用来衡量异味持续性。

## 结果
- 该分类包含 SKILL.md 正文中的 13 个高层级语义组件和 44 个低层级语义组件。
- 常见高层级组件包括 Task，占 238 个文件样本的 74.4%；Introduction，占 63.5%；References，占 57.1%；Principles，占 42.0%；Usecase，占 32.8%；Context，占 28.2%。
- 高频低层级组件包括 Steps Instruction，占 49.2%；Rules，占 39.1%；Prerequisites，占 31.1%；Reference Files，占 31.1%；Subtask Instruction，占 24.0%；Skill Trigger，占 23.1%；Return Artifact，占 21.9%。
- 最佳实践审查产出了 26 种技能异味，分为 5 种静态异味和 21 种语义异味。
- 论文称，超过 99% 的 SKILL.md 文件至少包含一种技能异味。
- 纵向分析发现，技能异味一旦出现，就很少消失；摘录未提供检测器的 precision、recall 或 F1 数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01456v1](https://arxiv.org/abs/2607.01456v1)
