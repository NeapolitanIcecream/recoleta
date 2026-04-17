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
VLA-World 将视觉-语言-动作驾驶策略与世界模型结合起来：先生成短期未来图像，再基于这张想象出的未来帧进行推理，随后细化驾驶规划。论文的目标是通过在动作生成中加入明确的前瞻能力和自检过程，提高端到端自动驾驶的安全性与可解释性。

## 问题
- 当前的 VLA 驾驶模型可以将观测映射为动作，但对场景动态和其他交通参与者的建模还不足，难以在复杂交通中提供强前瞻能力。
- 当前的驾驶世界模型可以生成看似合理的未来场景，但通常不会判断这些想象出的未来是否意味着风险、安全问题，或是否对应更优动作。
- 这很重要，因为自动驾驶既需要预测场景将如何变化，也需要在预测未来显示出不安全时修正决策。

## 方法
- VLA-World 先预测短期自车轨迹，再将该轨迹与多视角观测结合，生成 0.5 秒后的下一帧驾驶图像。
- 模型将这张自生成的未来图像送回反思式推理模块，用来检查交通参与者、运动线索和潜在风险，然后细化最终的 3 秒轨迹与动作。
- 训练分为三个阶段：用于未来帧生成的视觉预训练、面向混合驾驶任务的监督微调，以及带有基于规则奖励的 GRPO 强化学习，奖励项包括输出格式、短期预测、视觉 token 有效性、动作质量和轨迹质量。
- 论文还提出了 **nuScenes-GR-20K**，这是一个基于 nuScenes 构建的数据集，用于以想象出的未来为条件的未来生成与推理。

## 结果
- 论文称，VLA-World 在规划和未来生成两个基准上都稳定超过此前的 VLA 和世界模型基线。
- 摘录中展示的定量规划结果使用 **ST-P3** 和 **UniAD** 指标，以及 **L2 trajectory error** 和 **collision rate**，但提供的文本里看不到 **VLA-World** 对应的表格行，因此这里无法提取其确切数值。
- 从可见文本中能得到的最强具体结论是：根据 Figure 1，VLA-World 在对比方法中取得了**最低的 collision rate 和 FID score**，但摘录没有给出确切的 FID 数值。
- 表格中可见的基线包括：使用 UniAD 的 **FeD***，**0.58 avg L2**、**0.19 avg collision (%)**；**UniAD***，**0.46 avg L2**、**0.37 avg collision (%)**；以及使用 ST-P3 的 **BEV-Planner***，**0.35 avg L2**、**0.34 avg collision (%)**。作者称 VLA-World 超过了这些当前最先进的基线。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09059v1](http://arxiv.org/abs/2604.09059v1)
