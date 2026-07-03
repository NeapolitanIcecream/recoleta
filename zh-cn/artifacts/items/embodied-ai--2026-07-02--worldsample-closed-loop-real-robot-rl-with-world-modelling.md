---
source: arxiv
url: https://arxiv.org/abs/2607.02431v1
published_at: '2026-07-02T17:00:37'
authors:
- Yuquan Xue
- Le Xu
- Zeyi Liu
- Zhenyu Wu
- Zhengyi Gu
- Xinyang Song
- Bofang Jia
- Ziwei Wang
topics:
- real-robot-rl
- world-model
- robot-data-augmentation
- sim2real
- dexterous-manipulation
- policy-learning
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# WorldSample: Closed-loop Real-robot RL with World Modelling

## Summary
## 摘要
WorldSample 使用由动作条件世界模型生成的额外转移来训练真实机器人强化学习策略，并用真实 rollout 让生成内容保持贴合任务。它面向需要接触处理和精确对齐的操作任务，目标是降低物理 rollout 成本。

## 问题
- 真实机器人强化学习可以在示范之外继续改进，但每次物理 rollout 都耗时，可能磨损硬件，可能需要人工复位，并且只记录一条动作-结果路径。
- 模仿学习在示范缺失的状态中可能失败，而完全生成的 rollout 可能加入视觉或接触错误，污染 critic 目标。
- 这对接触丰富的操作任务很重要，因为失败状态和恢复状态收集成本高，但对学习有用。

## 方法
- 从物理机器人 rollout 开始，然后在已执行动作附近采样局部扰动的动作序列。
- 使用动作条件 Cosmos-Predict2.5 世界模型生成未来视频观测；该模型在示范和在线 rollout 上适配。
- 用奖励模型标注生成轨迹，然后将其作为合成转移加入强化学习训练。
- 使用 Policy-Paced Learning：Q-aware selection 平衡正负生成样本，基于熵的调度在 actor 不确定时减少合成数据。
- 异步运行视频生成和世界模型后训练，使机器人控制和策略更新持续执行。

## 结果
- 在五个真实操作任务上，WorldSample 的平均成功率为 82%，HIL-SERL 为 56%，WMPO 为 69%，VLAW 为 64%。
- 平均训练步数从 HIL-SERL 的 56K 降至 WorldSample 的 23K，减少 59%。平均训练时间从 83 分钟降至 64 分钟。
- WorldSample 在各任务上的成功率分别为：Pushing 95%、Insertion 95%、Sorting 95%、Pick & Place 84%、Assemble 42%。HIL-SERL 在相同任务上分别达到 84%、63%、66%、55% 和 10%。
- 相比仅用示范适配，世界模型质量提高：仅示范适配的 PSNR/SSIM/LPIPS 为 10.27/0.428/0.809，而双视角示范+rollout 适配达到 29.89/0.925/0.035。
- 在 insertion 消融实验中，完整 WorldSample 在 10K 步和 30 分钟内达到 95% 成功率。去掉调度后，在 18K 步和 48 分钟内达到 61%；去掉 Q-selection 后，在 12K 步和 36 分钟内达到 76%；去掉完整 PPL 后，在 32K 步和 69 分钟内达到 86%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.02431v1](https://arxiv.org/abs/2607.02431v1)
