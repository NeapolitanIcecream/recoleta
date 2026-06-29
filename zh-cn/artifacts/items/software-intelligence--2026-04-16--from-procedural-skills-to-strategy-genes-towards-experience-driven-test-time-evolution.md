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
本文认为，供 LLM 代理复用的经验，用紧凑的控制对象来表示，比用长篇技能文档更有效。在 45 个科学代码求解场景的 4,590 次试验中，提出的 **strategy gene** 格式优于以文档为主的 skill package，也更能支持迭代式经验更新。

## 问题
- 论文研究如何在测试时复用过去的经验，让 LLM 代理在不改变模型权重的情况下调整行为。
- 许多既有系统把经验存成较长的 skill、reflection 或 memory 文档，但这些格式可能更方便人阅读和审查，不一定更利于模型在推理时直接使用。
- 这对代码和科学任务求解很重要，因为 token 预算和注意力都有限；额外文档会稀释有用指引，降低通过率。

## 方法
- 作者比较了两种由相同底层任务知识构成的经验格式：**Skill**，一种约 2,500 token、以文档为主的包；以及 **Gene**，一种约 230 token、面向控制的紧凑对象。
- Gene 包含一个小而固定的结构：任务匹配信号、简短摘要、少量策略步骤，以及面向失败的 **AVOID** 提示，并可附加约束和验证钩子。
- 他们加入 **Gene Evolution Protocol (GEP)**，把 gene 规范化为结构化对象，便于编辑、比较、积累，并在任务之间复用。
- 评估使用 45 个科学代码生成场景中的 4,590 次保留试验，以检查点通过率评分，模型是两个 Gemini 版本：Gemini 3.1 Pro Preview 和 Gemini 3.1 Flash Lite Preview。
- 论文做了三个探针：Skill probe 用来定位长 skill 中的有效信号，Gene probe 用来测试 Gene 是否优于短提示词，Evolution probe 用来测试经验应如何随时间累积。

## 结果
- 在主比较中，**Gene** 的平均通过率达到 **54.0%**，而 **no guidance** 为 **51.0%**，**Skill** 为 **49.9%**。相对 no guidance，Gene 提升 **+3.0 个百分点**，Skill 下降 **-1.1 个百分点**。
- 按模型看，Skill 让 **Gemini Pro** 从 **60.1%** 降到 **50.7%**，让 **Flash** 从 **41.8%** 升到 **49.0%**。Gene 让 **Pro** 基本保持在基线附近，达到 **59.9%**，并把 **Flash** 提升到 **48.2%**。
- 在 Gene 构造消融中，**仅关键词** 得分 **53.5%**（**+2.5 pp**），**关键词 + 摘要** 得分 **51.0%**（**+0.0 pp**），**关键词 + 摘要 + 策略** 得分 **54.0%**（**+3.0 pp**）。提升来自加入明确策略，而不是单纯增加文本量。
- 图 1 给出一个代表性比较：紧凑 Gene 比基线高 **+3.0 pp**，完整 Skill package 反而低 **-1.1 pp**。
- 在 **CritPt** 上做迭代进化时，gene-evolved 系统相对配对基座模型分别从 **9.1% 提升到 18.57%**，以及从 **17.7% 提升到 27.14%**。
- 这段摘要没有给出每个 probe 的完整数值表，但明确说明了这些结果：Skill 中可用于控制的有效信号很稀疏；按相同预算切出的 Skill 片段优于完整 Skill，但仍落后于 Gene；结构扰动对 Gene 的伤害更小；把失败历史压缩成简短警告，比直接追加原始失败历史更有效。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15097v1](http://arxiv.org/abs/2604.15097v1)
