---
source: arxiv
url: https://arxiv.org/abs/2606.10825v1
published_at: '2026-06-09T13:09:21'
authors:
- Zakariae El Asri
- Philippe Gratias-Quiquandon
- Nicolas Thome
- Olivier Sigaud
topics:
- diffusion-policy
- model-based-rl
- world-model
- mpc
- robot-manipulation
- offline-to-online-rl
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# MODIP: Efficient Model-Based Optimization for Diffusion Policies

## Summary
## 总结
MODIP 是一种离线到在线的方法，先用基于模型的规划改进机器人扩散策略，再用规划得到的轨迹做监督去噪训练。它针对扩散策略直接做 RL 微调时成本高、稳定性差的问题。

## 问题
- 扩散策略可以建模机器人动作的多峰分布，但行为克隆只会照搬离线数据，无法超过示范水平。
- 直接做 RL 微调成本很高，因为每次动作查询都要经过多步去噪链。
- 混合 MPC 方法通常用 Q(s, pi(s)) 给终止状态打分；对扩散策略来说，这会让规划时在很多终止状态上额外做去噪。

## 方法
- MODIP 训练一个潜变量世界模型，包含编码器、潜变量动力学模型、奖励模型、终止状态价值函数和扩散策略。
- 在线控制时，MPPI 从一个混合提议分布中采样动作序列：扩散策略候选加高斯探索候选。
- 规划器在潜空间里向前滚动候选序列，用预测奖励加终止状态价值 V(z) 打分，并在回滚时域 MPC 中执行得分最高的序列。
- 规划得到的轨迹会存入回放缓冲区，并用同样的去噪行为克隆损失作为扩散策略的监督目标。
- Critic 的目标用下一状态的价值，而不是从当前扩散策略采样动作，这样在更新 critic 时就不需要反复调用去噪。

## 结果
- 在 D4RL/Kitchen Complete 上，MODIP 报告的成功率是 0.94 ± 0.14，高于 BC 的 0.41 ± 0.20、DPPO 的 0.88 ± 0.02、PA-RL 的 0.85 ± 0.01 和 TD-MPC2 的 0.65 ± 0.13。
- 在 D4RL/Kitchen Partial 上，MODIP 报告的成功率是 0.98 ± 0.01，高于 BC 的 0.32 ± 0.06、DQL 的 0.45 ± 0.03、DPPO 的 0.67 ± 0.04、PA-RL 的 0.93 ± 0.01 和 TD-MPC2 的 0.55 ± 0.28。
- 在 D4RL/MuJoCo 上，MODIP 在 halfcheetah 上报告 13775 ± 203，在 walker 上报告 6081 ± 66，在 hopper 上报告 3281 ± 370；对应的 BC 分数分别是 5108 ± 730、5721 ± 324 和 3050 ± 90。
- 在 RoboMimic 上，MODIP 在 Lift 上报告 0.98 ± 0.03 的成功率，在 Can 上报告 0.92 ± 0.01；BC 在这两个任务上的结果分别是 0.95 ± 0.01 和 0.87 ± 0.04。
- 表中显示，PA-RL 在 halfcheetah 上高于 MODIP，分别是 14254 ± 1564 和 13775 ± 203；DSRL 在 RoboMimic 的 Lift 和 Can 上高于 MODIP，分别是 1.0 ± 0.0 和 0.94 ± 0.02，对比 MODIP 的 0.98 ± 0.03 和 0.92 ± 0.01。
- 摘要说明，终止状态价值 V(z) 降低了规划成本，policy-independent 的 critic 目标降低了训练成本，但没有给出 wall-clock、推理时间或去噪调用次数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10825v1](https://arxiv.org/abs/2606.10825v1)
