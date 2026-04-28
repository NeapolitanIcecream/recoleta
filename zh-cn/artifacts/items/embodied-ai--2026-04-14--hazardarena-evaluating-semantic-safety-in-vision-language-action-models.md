---
source: arxiv
url: http://arxiv.org/abs/2604.12447v1
published_at: '2026-04-14T08:32:02'
authors:
- Zixing Chen
- Yifeng Gao
- Li Wang
- Yunhan Zhao
- Yi Liu
- Jiayu Li
- Xiang Zheng
- Zuxuan Wu
- Cong Wang
- Xingjun Ma
- Yu-Gang Jiang
topics:
- vision-language-action
- robot-safety
- benchmarking
- semantic-grounding
- embodied-ai
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models

## Summary
## 摘要
HazardArena 是一个基准，用来测试视觉-语言-动作模型是否理解某个动作在能够执行的情况下何时是不安全的。论文显示，只用安全数据进行微调时，任务能力和不安全行为往往会同时上升；随后论文提出了一个无需训练的防护层，用来拦截部分高风险动作。

## 问题
- 当前 VLA 评测主要关注任务完成或轨迹成功，因此会漏掉这样一种情况：模型在错误的语义上下文中做出了正确的动作。
- 这很重要，因为机器人可能会执行已经学到的动作模板，例如倾倒或插入，同时忽略场景或指令中与风险直接相关的语义，从而造成财产、电气、火灾、隐私、化学、食品或人身安全方面的损害。
- 现有安全分数也可能产生误导：一个较弱的策略看起来安全，可能只是因为它没有行动，而不是因为它识别出了危险。

## 方法
- 论文构建了 **HazardArena**，这是一个包含安全/不安全孪生场景的基准。每一对孪生场景保持相同的物体、布局、技能模板和运动要求，只改变那个决定动作是被允许还是不安全的语义因素。
- 根据摘要和基准描述，HazardArena 包含 **40 个风险敏感任务**、**7 类危险**、**80 多个新的家庭资产**，以及总计 **2,000 多个资产**。
- 评测使用了超出最终成功率的分阶段指标：**attempt_rate**、**commit_rate** 和 **success_rate**。`commit` 表示策略到达了任务特定的危险前配置，此时距离不安全完成已经很近。
- 模型只在安全示范上进行微调：**总计 600 条轨迹**，来自 **6 个安全任务**，每个任务 **100 条轨迹**。对应的不安全孪生任务不参与训练。
- 为了在不重新训练的情况下减少不安全执行，论文在推理时加入了 **Safety Option Layer (SOL)**。SOL 要么应用手写的语义属性规则，要么询问一个外部视觉-语言判别器是否应拦截提议的动作，并将其替换为拒绝动作。

## 结果
- 在四个 VLA 模型中，更高的安全任务表现通常伴随着在对应不安全孪生任务上更高的不安全完成率。对 **pi_0** 来说，`insert outlet` 在安全孪生任务上的成功率从早期检查点到最终检查点由 **0.08** 升到 **0.47**，在不安全孪生任务上则由 **0.02** 升到 **0.44**。对 **NORA** 来说，同一任务在安全场景中从 **0.10** 升到 **0.39**，在不安全场景中从 **0.12** 升到 **0.34**。
- 其他任务也有同样趋势。对 **VLA-Adapter**，`spike drinkware` 在安全场景中从 **0.05** 提升到 **0.21**，在不安全场景中从 **0.01** 提升到 **0.19**；`pour electronics` 在安全场景中从 **0.00** 提升到 **0.14**，在不安全场景中从 **0.00** 提升到 **0.15**。
- 分阶段指标显示，只看终点成功率会低估风险。对 **pi_0** 在不安全 `insert outlet` 任务上的结果，**attempt = 0.93**、**commit = 0.80**、**success = 0.44**。在不安全 `contaminate dogbowl` 任务上，**attempt = 0.67**、**commit = 0.42**、**success = 0.18**。即使最终没有成功完成，策略也经常已经接近完成危险动作。
- 分阶段指标也会改变模型之间的比较。在不安全 `insert outlet` 任务上，**NORA** 的不安全成功率低于 **VLA-Adapter**（**0.34 vs 0.37**），但危险 `commit` 更高（**0.62 vs 0.48**），这说明虽然终点完成率略低，它却更深入地推进了这个不安全动作。
- 在给定摘录中，SOL 的定量结果只显示了一部分。论文称，无需训练的 SOL 能在几乎不影响任务表现的情况下减少不安全行为，并且基于规则的 **SOL-L1** 在这个受控基准设置中效果较强，但由于缺少对应表格或图，单靠摘录无法给出完整的数值总结。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.12447v1](http://arxiv.org/abs/2604.12447v1)
