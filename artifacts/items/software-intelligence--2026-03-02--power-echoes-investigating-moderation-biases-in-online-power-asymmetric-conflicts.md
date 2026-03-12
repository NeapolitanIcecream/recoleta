---
source: arxiv
url: http://arxiv.org/abs/2603.01457v1
published_at: '2026-03-02T05:16:11'
authors:
- Yaqiong Li
- Peng Zhang
- Peixu Hou
- Kainan Tu
- Guangping Zhang
- Shan Qu
- Wenshi Chen
- Yan Chen
- Ning Gu
- Tun Lu
topics:
- content-moderation
- human-ai-collaboration
- bias-analysis
- power-asymmetry
- online-conflict
relevance_score: 0.35
run_id: materialize-outputs
---

# Power Echoes: Investigating Moderation Biases in Online Power-Asymmetric Conflicts

## Summary
这篇论文研究在线“强弱势不对等”冲突中，人类版主是否会偏向强势一方，以及 AI 建议会怎样改变这种偏差。作者用消费者—商家真实冲突和 50 人实验发现：人工审核存在多种亲强势方偏差，AI 能缓解多数偏差，但也会放大少数偏差。

## Problem
- 论文要解决的问题是：在消费者与商家这类**权力不对等**的在线冲突里，人类审核者会出现哪些与“权力线索”相关的偏见，以及 AI 建议会让这些偏见减轻还是加重。
- 这很重要，因为许多平台仍依赖人工或众包审核来判断“该支持谁”，而强势方通常更会引用规则、展示专业性、给出补偿或威胁，可能让审核结果系统性失衡，伤害弱势方权益与平台公信力。
- 现有研究讨论了内容审核偏差，但几乎没有系统研究**权力不对等冲突审核**中的偏差类型与人机协作效应。

## Approach
- 作者以社会心理学的 **Bases of Social Power** 理论为基础，把在线冲突中的权力线索整理成一个 taxonomy，提出 10 种“权力表现”，如 legitimate claim、authority citation、punishment threat、compensation、expert knowledge、group preference、statement order、expression tone、choice trap、length difference。
- 数据来自大众点评上的真实消费者—商家冲突，作者收集约 **60,000** 个样本，并从中抽取与编码用于实验的冲突案例。
- 实验采用混合设计，共 **50** 名参与者，分为两组：**human moderation** 组独立判断；**human-AI moderation** 组在相同案例上额外看到“AI 建议”。
- 为避免不同大模型输出波动，作者使用 **Wizard-of-Oz** 设计：实际上预先准备高质量建议，但告知参与者这些建议来自 AI，从而研究“人们把建议当作 AI 时”会如何改变判断。
- 最简单地说，方法核心就是：**把同一类冲突稍微改变其中的权力线索，再比较人类单独判断和看到 AI 建议后的判断差异，看哪些线索会把审核者推向强势方、AI 又如何改变这种推力。**

## Results
- 在 **RQ1** 中，作者声称人工审核存在 **5 种** 偏向支持强势方的权力相关偏差；摘要未给出每一类偏差的详细统计数值或效应量。
- 在 **RQ2** 中，这些偏差在 human-AI 审核中并未完全消失；AI 对偏差的影响是混合的：**4 种偏差被缓解，1 种被消除**，但同时 **1 种新偏差被引入，另有 1 种被放大**。
- 论文的实验规模是 **50 名参与者**，场景为真实消费者—商家冲突；这是文中最明确的量化实验设置。
- 数据侧，作者收集约 **60,000** 条大众点评冲突样本，覆盖 **17** 个主题，并重点选择前 **5** 个主题；前五主题占总样本的 **92.7%**。
- 论文还提出一个具体发现：当 AI 建议明确提供“为什么**不应支持另一方**”的视角时，审核者更可能转而支持弱势方。
- 提供的节选**没有给出**更细的数值结果，如显著性检验、Likert 均值、具体基线比较或按偏差类别分解的百分比提升/下降。

## Link
- [http://arxiv.org/abs/2603.01457v1](http://arxiv.org/abs/2603.01457v1)
