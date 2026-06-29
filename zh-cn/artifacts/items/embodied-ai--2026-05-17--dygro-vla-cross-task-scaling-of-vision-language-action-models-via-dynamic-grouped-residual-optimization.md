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
## 总结
DyGRO-VLA 解决的是 VLA 机器人策略在多任务下进行 RL 微调时，如何不破坏共享特征的问题。它冻结基础 VLA，只学习路由后的残差 RL 专家，用来修正动作块。

## 问题
- RL 后训练可以提高单任务机器人的成功率，但在多任务 VLA 训练中，它会扭曲共享表征并导致遗忘。
- 这个问题很关键，因为 VLA 模型本来要在任务之间复用视觉、语言和动作特征；任务特定的 RL 会把它们变成更窄的控制器。
- 在 LIBERO 分析中，基于 SAC 的强化微调随着任务数量增加变得不稳定，20 任务训练时平均成功率明显下降；摘录没有给出具体降幅。

## 方法
- 离线阶段在示范数据上训练基础 VLA，并使用信息瓶颈损失：保留动作预测所需的特征，丢弃背景和光照等观测细节。
- VLA 编码器使用腕部和第三视角相机图像、语言指令、本体感觉、DINOv2、SigLIP 和 Qwen2.5-0.5B 来生成融合后的潜在特征。
- 在线阶段冻结基础 VLA，并学习一个 Mixture-of-RL-Residuals，它预测一个 delta 动作块，再加到基础动作块上。
- 路由器用带对比损失训练的任务嵌入，从任务原型中选出 top-m 个残差专家。
- 训练混合离线和在线回放，加入负载均衡正则以避免专家塌缩，并根据最近的成功率更频繁采样更难的任务。

## 结果
- 在 LIBERO 上，DyGRO-VLA 的平均成功率为 97.1%，比它的离线基础模型绝对提升 4.4 个百分点。
- 在 LIBERO-Long 上，它报告提升 9.8 个百分点，这是摘录中给出的 LIBERO 最大增益。
- 在 RoboTwin2 仿真中，它报告整体成功率 79.2%，并且在摘录提到的方法里总体结果最好。
- 在 RoboTwin2 的 Sim2Real 迁移中，它超过了 RFT 基线，在复杂双臂和长时程任务上的提升最大；摘录没有给出精确的真实世界成功率。
- 表征分析在单任务 RFT 前后对 40 个 LIBERO 任务各取 10 个样本进行嵌入，显示 RFT 会把调优后的任务推到一个孤立簇中。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17486v1](https://arxiv.org/abs/2605.17486v1)
