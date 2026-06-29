---
source: arxiv
url: https://arxiv.org/abs/2605.25620v1
published_at: '2026-05-25T09:21:43'
authors:
- Minghao Fu
- Fan Feng
- Nicklas Hansen
- Biwei Huang
topics:
- world-models
- robot-planning
- visual-foundation-models
- latent-representation-learning
- offline-control
- proprioceptive-alignment
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Back to Parsimonious Latents: Learning Task-Centric World Models from Visual Foundations

## Summary
## 总结
TC-WM 从冻结的视觉基础模型嵌入和本体感觉中学习紧凑的世界模型潜变量。论文声称，这些潜变量能改进无奖励离线规划与控制，覆盖导航、操作和运动控制基准。

## 问题
- 世界模型需要支持动作条件预测和规划的潜变量，但像素潜变量可能缺少语义结构，而冻结的视觉嵌入可能包含与任务无关的细节，例如纹理、光照和背景。
- 这个问题在高维机器人控制中更明显：摘录提到 Robomimic，包含一个 7 自由度机械臂和一个 43 维本体感觉状态，额外的潜在因素会浪费规划能力。
- 无奖励离线设置让问题更难，因为模型必须只从固定轨迹中学习有用的状态结构，没有奖励标签，也没有在线修正。

## 方法
- TC-WM 用冻结的视觉编码器（例如 DINOv2）对每张图像编码，用可训练层嵌入本体感觉，然后把两者拼接成联合嵌入。
- 一个线性编码器把联合嵌入投影到紧凑潜状态，用于展开轨迹。
- 一个基于 InfoNCE 的对比损失把潜变量中的稀疏子空间与当前本体感觉状态对齐，其余潜变量维度保留用于重建所需的视觉信息。
- 一个 ViT 动力学模型根据最近的潜变量和动作预测下一步潜变量，另一个头预测下一步本体感觉。
- 一个线性解码器从紧凑潜变量重建冻结嵌入，训练后的潜变量可支持 CEM 规划、结合逆动力学模型的潜空间扩散规划，或 SAC。

## 结果
- 摘录报告了跨 9 个基准的评测，覆盖 Robomimic、D4RL、导航、运动控制、操作，以及仿真和真实世界设置。
- 它声称方法在世界建模质量和控制精度上都优于当前最优方法，但摘录没有给出具体的成功率、回报或 MSE 数值。
- 图 2 被描述为展示了 Robomimic 上的成功率提升、更低的潜变量展开 MSE、在 Lift 和 Can 任务上的更强线性探测表现，以及与表示坍塌相比更好的潜空间使用。
- 该方法面向更难的操作场景，使用 7 自由度机械臂和 43 维本体感觉状态，而摘录将这些场景与 Maze 和 Push-T 这类 2 维动作任务作了对比。
- 对于连续控制结果，论文报告了 3 个随机种子的平均单回合回报，但摘录没有包含具体数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.25620v1](https://arxiv.org/abs/2605.25620v1)
