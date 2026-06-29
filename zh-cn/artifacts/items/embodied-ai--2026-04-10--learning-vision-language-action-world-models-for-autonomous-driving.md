---
source: arxiv
url: http://arxiv.org/abs/2604.09059v1
published_at: '2026-04-10T07:38:05'
authors:
- Guoqing Wang
- Pin Tang
- Xiangxuan Ren
- Guodongfang Zhao
- Bailan Feng
- Chao Ma
topics:
- autonomous-driving
- vision-language-action
- world-models
- future-frame-generation
- trajectory-planning
relevance_score: 0.73
run_id: materialize-outputs
language_code: zh-CN
---

# Learning Vision-Language-Action World Models for Autonomous Driving

## Summary
## 摘要
VLA-World 将视觉-语言-动作驾驶策略与一个世界模型结合起来。这个世界模型先生成一张短期未来图像，再在这张想象出来的画面上进行推理，然后再细化驾驶计划。论文的目标是通过给动作生成加入明确的前瞻能力和自检步骤，让端到端自动驾驶更安全，也更容易解释。

## 问题
- 现有的 VLA 驾驶模型可以把观测映射到动作，但它们对场景动态和其他交通参与者的建模还不够，难以在复杂交通中提供强前瞻能力。
- 现有的驾驶世界模型可以生成看起来合理的未来场景，但通常不会评估这些想象中的未来是否意味着风险、安全问题，或者更好的动作。
- 自动驾驶同时需要预测场景如何变化，也需要在预测出的未来看起来不安全时修正决策。

## 方法
- VLA-World 先预测一条短期自车轨迹，然后用这条轨迹和多视角观测来生成 0.5 秒后的下一帧驾驶图像。
- 模型把这张自生成的未来图像送回反思推理模块，检查交通参与者、运动线索和潜在风险，然后细化最终的 3 秒轨迹和动作。
- 训练分三阶段：用于未来帧生成的视觉预训练、在混合驾驶任务上的监督微调，以及带有基于规则奖励的 GRPO 强化学习。奖励项包括输出格式、短期预测、视觉 token 有效性、动作质量和轨迹质量。
- 论文还引入了 **nuScenes-GR-20K**，这是一个基于 nuScenes 构建的数据集，用于以想象中的未来为条件进行未来生成和推理。

## 结果
- 论文声称，VLA-World 在规划和未来生成两个基准上都持续优于之前的 VLA 和世界模型基线。
- 摘录中展示的规划定量结果使用了 **ST-P3** 和 **UniAD** 指标，包括 **L2 轨迹误差** 和 **碰撞率**，但提供的文本里看不到 **VLA-World** 那一行，所以这里无法提取它的具体数值。
- 从可见文本里最明确的结论是，VLA-World 在 Figure 1 中对比方法里拿到了 **最低的碰撞率和 FID 分数**，但摘录没有给出具体的 FID 数值。
- 表格中可见的基线包括 **FeD*** 在 UniAD 上的 **0.58 平均 L2** 和 **0.19 平均碰撞率（%）**，**UniAD*** 的 **0.46 平均 L2** 和 **0.37 平均碰撞率（%）**，以及 **BEV-Planner*** 在 ST-P3 上的 **0.35 平均 L2** 和 **0.34 平均碰撞率（%）**。作者表示 VLA-World 超过了这些最先进基线。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09059v1](http://arxiv.org/abs/2604.09059v1)
