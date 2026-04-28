---
source: arxiv
url: http://arxiv.org/abs/2604.15097v1
published_at: '2026-04-16T14:55:49'
authors:
- Junjie Wang
- Yiming Ren
- Haoyang Zhang
topics:
- test-time-adaptation
- llm-agents
- code-generation
- experience-reuse
- prompt-representation
- scientific-programming
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# From Procedural Skills to Strategy Genes: Towards Experience-Driven Test-Time Evolution

## Summary
## 摘要
这篇论文认为，对 LLM 代理来说，可复用经验做成紧凑的控制对象，比写成长篇技能文档效果更好。在 45 个科学代码求解场景的 4,590 次试验中，作者提出的 **strategy gene** 格式优于以文档为主的技能包，也更适合迭代式经验更新。

## 问题
- 论文研究的是如何在测试时复用过往经验，让 LLM 代理在不修改模型权重的情况下改变行为。
- 许多已有系统把经验存成长技能、反思或记忆文档，但这些格式可能更便于人阅读和审查，而不一定更有利于模型在推理时据此行动。
- 这对代码和科学任务求解很重要，因为 token 预算和注意力有限；额外文档可能会稀释有用指导，降低通过率。

## 方法
- 作者比较了两种基于同一底层任务知识构建的经验格式：**Skill**，约 2,500 token 的重文档式包；以及 **Gene**，约 230 token 的紧凑控制对象。
- Gene 包含一个小型固定结构：任务匹配信号、简短摘要、少量策略步骤，以及带失败规避信息的 **AVOID** 提示，并可选加入约束和验证钩子。
- 作者还提出 **Gene Evolution Protocol (GEP)**，把 gene 规范化为结构化对象，便于编辑、比较、累积，并在任务间复用。
- 评测包含 45 个科学代码生成场景中的 4,590 次保留试验，使用基于 checkpoint 的通过率评分，并测试了两个 Gemini 模型：Gemini 3.1 Pro Preview 和 Gemini 3.1 Flash Lite Preview。
- 论文进行了三类探针：Skill probe，用来定位长 Skill 中的有效信号；Gene probe，用来测试 Gene 是否优于短提示；Evolution probe，用来测试经验应如何随时间累积。

## 结果
- 在主要比较中，**Gene** 的平均通过率达到 **54.0%**，而**无指导**为 **51.0%**，**Skill** 为 **49.9%**。相对无指导，Gene 提高了 **+3.0 个百分点**，Skill 则下降 **-1.1 个百分点**。
- 分模型看，Skill 使 **Gemini Pro** 从 **60.1%** 变为 **50.7%**，使 **Flash** 从 **41.8%** 变为 **49.0%**。Gene 让 **Pro** 基本维持在基线附近，为 **59.9%**，并把 **Flash** 提升到 **48.2%**。
- 在 Gene 构造消融实验中，**仅关键词** 的平均得分为 **53.5%**（**+2.5 pp**），**关键词 + 摘要** 为 **51.0%**（**+0.0 pp**），**关键词 + 摘要 + 策略** 为 **54.0%**（**+3.0 pp**）。增益来自明确加入策略，而不是加入更多文本。
- 图 1 给出了一组代表性对比：紧凑 Gene 相比基线带来 **+3.0 pp**，而完整 Skill 包则是 **-1.1 pp**。
- 在 **CritPt** 上的迭代演化中，gene-evolved 系统相对各自配对的基础模型，分别从 **9.1% 提升到 18.57%**，以及从 **17.7% 提升到 27.14%**。
- 摘录没有给出每个探针的完整数值表，但明确陈述了这些结果：Skill 内部真正有用的控制信号很稀疏；在相同预算下截取的 Skill 片段虽然优于完整 Skill，但仍落后于 Gene；结构扰动对 Gene 的影响更小；把失败信息提炼成紧凑警示，比直接附加原始失败历史效果更好。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15097v1](http://arxiv.org/abs/2604.15097v1)
