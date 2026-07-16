---
source: arxiv
url: https://arxiv.org/abs/2607.13818v1
published_at: '2026-07-15T13:25:52'
authors:
- Xiaopeng Zhang
- Yueyang Weng
- Qi Liu
- Yongjin Mu
- Yanjie Li
topics:
- robot-foundation-model
- vision-language-action
- generalist-robot-policy
- reinforcement-learning
- failure-recovery
- sim2real
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Learning Robust Execution in Robotic Manipulation with Agentic Reinforcement Learning

## Summary
## 摘要
该论文为冻结的机器人操作策略加入了一个高层强化学习执行管理器。在 LIBERO 上，该方法在标准条件下提高了成功率，并在注入扰动时显著改善了恢复能力，同时无需重新训练底层策略。

## 问题
- 由于感知误差、接触不确定性、扰动以及不断累积的执行失败，长时程操作策略可能逐渐偏离预期行为。
- 视觉-语言-动作策略和模仿策略通常会生成动作，但不会显式监测执行稳定性或选择恢复行为；这一点很重要，因为微小偏差可能逐渐导致不可逆的任务失败。

## 方法
- 该方法根据近期末端执行器的有效性和运动平滑度计算局部执行质量，并根据当前执行前缀与按阶段匹配的成功参考轨迹之间的距离计算全局执行质量。
- 一个轻量级高层策略观测本体感知信息、低层动作和质量分数的历史记录，然后从四种模式中选择一种：执行（Execute）、重试（Retry）、修复（Repair）或重置（Reset）。
- 重试和修复使用操作空间控制，将机器人回退到近期的高质量状态；重置则重新开始当前回合。底层 VLA 或扩散策略保持冻结。
- 该智能体策略使用 PPO 进行训练，训练目标包括任务成功、失败、时间和恢复成本；论文报告的设置为每个任务使用 50 条成功参考轨迹、10 个进度区间、5 个最近邻、长度为 20 的历史记录，以及每 5 个低层步长做出一次决策。

## 结果
- 在 LIBERO 各套件上，标准条件下的平均成功率提升分别为：Spatial 提升 5.1 个百分点，Object 提升 5.4 个百分点，Goal 提升 6.6 个百分点，Long 提升 13.7 个百分点。
- 在随机运动学扰动下，相应的平均提升分别为 25.7、27.4、28.3 和 39.2 个百分点。
- 在标准 LIBERO-Long 设置中，OpenVLA 的成功率从 54.0% 提升至 74.5%，Diffusion Policy 从 50.5% 提升至 72.4%；在扰动设置中，OpenVLA 从 33.4% 提升至 67.6%，Diffusion Policy 从 30.5% 提升至 60.5%。
- 对于 pi_0 和 pi_0.5 等性能更强的策略，该方法也保持了接近饱和的性能；但所提供的摘录不包含完整的消融实验、成本分析或真实机器人评估结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13818v1](https://arxiv.org/abs/2607.13818v1)
