---
source: arxiv
url: https://arxiv.org/abs/2606.24177v1
published_at: '2026-06-23T05:57:09'
authors:
- Youran Sun
- Xingyu Ren
- Chugang Yi
- Jiaxuan Guo
- Kejia Zhang
- Jianda Du
- Haizhao Yang
topics:
- autonomous-research
- multi-agent-systems
- prompt-orchestration
- research-automation
- human-ai-interaction
- software-agents
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Agon: An Autonomous Large-Scale Omnidisciplinary Research System Built on Prompt Economy

## Summary
## 摘要
Agon 是一个由提示词驱动的多智能体系统，用于并行运行许多研究工作流，覆盖从选题到论文草稿的过程。它的目标是扩大研究产物的生成规模，同时把主张判断和科学方向交给人类。

## 问题
- 研究智能体现在可以生成代码、实验、评审和手稿，因此难点转向核查主张、新颖性和证据。
- 大型自主工作流常会增加许多角色、长提示词和脆弱的控制代码，这使其难以检查、维护和迁移到不同领域。
- 该系统面向计算型研究场景，在这些场景中，实验、文献综述和论文起草可以通过模型调用和远程计算来运行。

## 方法
- Agon 使用可复用的生产者-批评者循环，称为工厂，用于生成想法、提案、实验和论文。
- 它的核心机制是 Prompt Economy：保留一小组角色提示词，并在许多研究产物中反复复用，而不是为每个项目编写特定任务的提示词。
- 深度文献循环会搜索、筛选、阅读、撰写 wiki 条目、扩展查询并重复这些步骤，为后续智能体提供共享的文献记忆。
- 实验工厂将科学家、编码者、审计者和评审者角色分开；编码者运行任务，审计者检查计划、代码、结果和交接状态。
- 调度主要由基于提示词的调度器处理，而不是依赖特定工作流的状态机或大量解析器控制代码。

## 结果
- 论文报告了跨领域的 444 次 Prompt Economy 循环迭代。
- Agon 使用 18 个角色和 230.6 KiB 的提示词文本；相比之下，AI Scientist v2 约有 110 个角色和 302.4 KiB，ARIS 有 79 个角色和 1157.4 KiB，AutoResearchClaw 有 78 个角色和 1297.5 KiB。
- 在当前运行规模下，深度文献流程每个主题大约阅读 400-2000 篇论文。
- 作者报告了 10 多个科学领域的项目和数千次科学家-编码者-审计者迭代，实验代码没有由人类编写。
- 他们报告了调度器连续运行一个月且无人干预。
- 摘录没有给出关于科学正确性、论文接收或主张有效性的定量基准；其最强证据是部署规模、提示词表面积和失败分类法。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.24177v1](https://arxiv.org/abs/2606.24177v1)
