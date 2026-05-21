---
source: arxiv
url: https://arxiv.org/abs/2605.17486v1
published_at: '2026-05-17T14:55:32'
authors:
- Sixu Lin
- Yunpeng Qing
- Litao Liu
- Ming Zhou
- Ruixing Jin
- Xiaoyi Fan
- Guiliang Liu
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- reinforcement-finetuning
- sim2real
- multi-task-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# DyGRO-VLA: Cross-Task Scaling of Vision-Language-Action Models via Dynamic Grouped Residual Optimization

## Summary
## 摘要
DyGRO-VLA 处理 VLA 机器人策略在多任务上的 RL 微调问题，目标是在不破坏共享特征的情况下提升策略。它冻结基础 VLA，并学习带路由的残差 RL 专家，用来修正基础模型的动作块。

## 问题
- RL 后训练可以提高单任务机器人的成功率，但在多任务 VLA 训练中可能扭曲共享表征并造成遗忘。
- 这个问题很重要，因为 VLA 模型需要在任务之间复用视觉-语言-动作特征；任务专用 RL 会把它们变成适用范围更窄的控制器。
- 在 LIBERO 分析中，基于 SAC 的强化学习微调随着任务数量增加而变得不稳定，20 个任务训练导致平均成功率大幅下降；摘录没有给出确切降幅。

## 方法
- 离线阶段使用演示数据训练基础 VLA，并加入信息瓶颈损失：保留动作预测所需的特征，丢弃背景和光照等观测细节。
- VLA 编码器使用腕部和第三视角相机图像、语言指令、本体感知、DINOv2、SigLIP 和 Qwen2.5-0.5B，生成融合后的潜在特征。
- 在线阶段冻结基础 VLA，并学习一个 RL 残差混合模型，用来预测加到基础动作块上的 delta 动作块。
- 路由器使用任务嵌入选择 top-m 个残差专家；该任务嵌入通过与任务原型的对比损失训练得到。
- 训练混合离线和在线回放，加入负载均衡正则化以避免专家坍缩，并根据近期成功率更频繁地采样较难任务。

## 结果
- 在 LIBERO 上，DyGRO-VLA 报告的平均成功率为 97.1%，相比其离线基础模型绝对提升 4.4 个百分点。
- 在 LIBERO-Long 上，它报告提升 9.8 个百分点，这是摘录中给出的最大 LIBERO 增益。
- 在 RoboTwin2 仿真中，它报告总体成功率为 79.2%，在摘录列出的对比方法中总体结果最好。
- 在 RoboTwin2 的 Sim2Real 迁移中，它超过 RFT 基线；摘录称复杂双臂任务和长时程任务上的增益最大，但没有提供真实世界成功率的确切数值。
- 表征分析在单任务 RFT 前后对 40 个 LIBERO 任务进行嵌入，每个任务 10 个样本，结果显示 RFT 会把被微调的任务推入一个孤立簇。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17486v1](https://arxiv.org/abs/2605.17486v1)
