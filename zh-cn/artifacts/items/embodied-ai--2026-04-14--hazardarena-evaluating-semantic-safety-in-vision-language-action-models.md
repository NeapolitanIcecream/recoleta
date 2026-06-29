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
HazardArena 是一个基准，用来测试视觉-语言-行动模型是否能判断某个动作在语义上是否危险，即使它能执行这个动作。论文表明，只用安全样本进行微调，常常会同时提高任务能力和危险行为，然后提出一个无需训练的保护层来阻止部分高风险动作。

## 问题
- 现有的 VLA 评测主要关注任务完成或轨迹成功，所以会漏掉这种情况：模型在错误的语义上下文里做出了正确的动作。
- 这很重要，因为机器人可以执行学到的动作模板，比如倒液体或插入，却忽略场景或指令里的风险含义，进而造成财产、电气、火灾、隐私、化学、食品或人身安全伤害。
- 现有安全分数也可能误导人：一个弱策略看起来很安全，可能只是因为它没有行动，而不是因为它识别出了危险。

## 方法
- 论文构建了 **HazardArena**，一个包含安全/不安全双胞胎场景的基准。每一对双胞胎保留相同的物体、布局、技能模板和运动要求，只改变决定动作是被允许还是危险的语义因素。
- HazardArena 包含 **40 个风险敏感任务**、**7 类危险**、**80 多个新的家居资产**，以及根据摘要和基准描述统计的 **2,000 多个资产**。
- 评测使用了超出最终成功率的分阶段指标：**attempt_rate**、**commit_rate** 和 **success_rate**。`commit` 指策略已经进入任务特定的、接近危险完成的前危险配置。
- 模型只用安全示范进行微调：总计 **600 条轨迹**，来自 **6 个安全任务**，每个任务 **100 条轨迹**。不安全的双胞胎不用于训练。
- 为了在不重新训练的情况下减少危险执行，论文在推理时加入了 **Safety Option Layer (SOL)**。SOL 要么使用手写的语义属性规则，要么询问外部视觉-语言裁判，判断是否阻止提议的动作并改成拒绝动作。

## 结果
- 在四个 VLA 模型上，更高的安全任务表现通常伴随更高的匹配不安全双胞胎上的危险完成率。对 **pi_0**，`insert outlet` 从早期到最终检查点，在安全双胞胎上从 **0.08 提高到 0.47**，在不安全双胞胎上从 **0.02 提高到 0.44**。对 **NORA**，同一任务在安全双胞胎上从 **0.10 提高到 0.39**，在不安全双胞胎上从 **0.12 提高到 0.34**。
- 其他任务也有同样趋势。对 **VLA-Adapter**，`spike drinkware` 在安全双胞胎上从 **0.05 提高到 0.21**，在不安全双胞胎上从 **0.01 提高到 0.19**；`pour electronics` 在安全双胞胎上从 **0.00 提高到 0.14**，在不安全双胞胎上从 **0.00 提高到 0.15**。
- 分阶段指标显示，终点成功率会低估风险。对 **pi_0** 在不安全的 `insert outlet` 上，**attempt = 0.93**，**commit = 0.80**，**success = 0.44**。在不安全的 `contaminate dogbowl` 上，**attempt = 0.67**，**commit = 0.42**，**success = 0.18**。即使最终没有成功，策略也常常已经接近危险完成。
- 分阶段指标也会改变模型比较结果。在不安全的 `insert outlet` 上，**NORA** 的不安全成功率低于 **VLA-Adapter**（**0.34 对 0.37**），但危险 commit 更高（**0.62 对 0.48**），这说明它虽然最终完成率略低，却更深入地推进了不安全动作。
- 由于提供的摘录只显示了部分内容，SOL 的定量结果只能看到一部分。论文声称，这个无需训练的 SOL 在任务表现影响很小的情况下减少了危险行为，而且基于规则的 **SOL-L1** 在受控基准环境中效果很好，但缺少表格或图，无法只凭摘录给出完整的数值总结。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.12447v1](http://arxiv.org/abs/2604.12447v1)
