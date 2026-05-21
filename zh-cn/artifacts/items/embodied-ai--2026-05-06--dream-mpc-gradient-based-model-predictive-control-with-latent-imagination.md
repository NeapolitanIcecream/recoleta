---
source: arxiv
url: https://arxiv.org/abs/2605.04568v1
published_at: '2026-05-06T07:13:11'
authors:
- Jonathan Spieler
- Sven Behnke
topics:
- world-models
- model-predictive-control
- gradient-based-planning
- model-based-rl
- continuous-control
- robot-learning
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination

## Summary
## 摘要
Dream-MPC 是一种基于梯度的 MPC 方法。它通过学习到的潜在世界模型进行规划，并使用策略先验、不确定性惩罚和动作复用。它面向高维连续控制中的更快规划，同时在性能上超过基础策略；在 BMPC 实验中，它也超过了 MPPI。

## 问题
- 基于采样的 MPC 方法（如 CEM 和 MPPI）通常每一步要评估数百到数千个动作序列。这对高维控制成本很高，也更难在受限硬件上运行。
- 纯策略网络的推理成本更低，但它们在测试时不做在线规划，因此泛化可能较差。
- 以往使用学习模型的基于梯度的规划器经常弱于无梯度规划器，部分原因是梯度可能把动作推向模型误差较大的区域。

## 方法
- Dream-MPC 从随机策略先验中采样少量候选动作序列，然后在学习到的潜在世界模型中展开这些序列。
- 它根据预测回报对每个动作序列做梯度上升优化，使用预测奖励和终止 Q 值。
- 它对由 Q 函数集成估计的认知不确定性施加惩罚，因此模型不确定性高的规划会得到更低的目标值。
- 它在多个 MPC 步之间用复用系数复用先前优化过的动作，把优化工作带入滚动时域循环的后续步骤。
- 论文报告的默认规划器使用 5 个候选序列、1 个梯度步、时域长度 3、步长 0.1、复用系数 0.1 和不确定性系数 0.01。

## 结果
- 在来自 DeepMind Control Suite、HumanoidBench 和 Meta-World 的 24 个连续控制任务上，使用 BMPC 的 Dream-MPC 相比 BMPC 将 IQM 归一化分数提高 26.7%，将平均归一化分数提高 20.5%。
- 以 TD-MPC2 作为基础模型时，Dream-MPC 相比仅使用 TD-MPC2 策略的基线在 IQM 上提高 144.7%，在平均分数上提高 43.4%，但它没有稳定达到使用 MPPI 的 TD-MPC2 的水平。
- 在给定设置中，该规划器每个时间步使用 15 次世界模型评估；相比之下，引用的 TD-MPC2 配置下 MPPI 使用 9216 次。
- 在 TD-MPC2 上，Dream-MPC 的平均领域分数为：DMControl 上 433 ± 259，HumanoidBench 上 379 ± 897，Meta-World 上 0.62 ± 0.31；使用 MPPI 的 TD-MPC2 在相同领域上的分数为 657 ± 225、761 ± 1617 和 0.67 ± 0.33。
- 在 6 个使用图像观测的 DMControl 任务上结合 BMPC 时，Dream-MPC 在 Cartpole Swingup Sparse 上得分 725 ± 141，在 Cheetah Run 上 643 ± 9，在 Hopper Hop 上 275 ± 3，在 Quadruped Walk 上 435 ± 76，在 Walker Run 上 762 ± 6；它在 Acrobot Swingup 上大致持平，得分为 288 ± 31，而仅使用 BMPC 策略为 292 ± 18。
- 论文称，当 Dream-MPC 搭配来自 BMPC 的强策略先验时，可以超过无梯度 MPC，同时使用的模型评估次数远少于 MPPI。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04568v1](https://arxiv.org/abs/2605.04568v1)
