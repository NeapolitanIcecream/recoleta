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
Dream-MPC 是一种基于梯度的 MPC 方法，它通过带策略先验、确定性不确定性惩罚和动作复用的学习型潜在世界模型进行规划。它面向高维连续控制中的更快规划，同时提升基础策略的表现，在 BMPC 实验中也优于 MPPI。

## 问题
- CEM 和 MPPI 这类基于采样的 MPC 方法，往往在每一步要评估数百到数千条动作序列，这在高维控制中代价很高，也更难在算力受限的硬件上运行。
- 纯策略网络在推理时更便宜，但因为测试时不做在线规划，泛化往往较差。
- 先前使用学习模型的基于梯度规划器，经常不如无梯度规划器，部分原因是梯度会把动作推到模型误差较大的区域。

## 方法
- Dream-MPC 从随机策略先验中采样少量候选动作序列，然后在学习到的潜在世界模型中展开。
- 它对每条动作序列按预测回报做梯度上升，使用预测奖励和终值 Q 值进行优化。
- 它对由 Q 函数集成估计的认知不确定性进行惩罚，因此模型不确定性高的计划会得到更低的目标值。
- 它在 MPC 步之间复用先前优化过的动作，并使用复用系数，把优化工作带到滚动时域循环中。
- 论文报告的默认规划器使用 5 个候选、1 步梯度更新、3 步时域、0.1 步长、0.1 复用系数和 0.01 不确定性系数。

## 结果
- 在 DeepMind Control Suite、HumanoidBench 和 Meta-World 的 24 个连续控制任务上，Dream-MPC 配合 BMPC 后，IQM 归一化分数比 BMPC 提升 26.7%，平均归一化分数提升 20.5%。
- 以 TD-MPC2 作为基础模型时，Dream-MPC 相比仅用策略的 TD-MPC2 基线，IQM 提升 144.7%，平均分提升 43.4%，但它并不总能达到 TD-MPC2 搭配 MPPI 的水平。
- 在给定设置下，这个规划器每个时间步要做 15 次世界模型评估；论文引用的 TD-MPC2 配置下，MPPI 要做 9216 次。
- Dream-MPC 在 TD-MPC2 上的各领域平均分为：DMControl 433 ± 259，HumanoidBench 379 ± 897，Meta-World 为 0.62 ± 0.31；同样领域里，TD-MPC2 加 MPPI 的分数分别是 657 ± 225、761 ± 1617 和 0.67 ± 0.33。
- 在 6 个带图像观测的 DMControl 任务上，Dream-MPC 配合 BMPC 的分数为：Cartpole Swingup Sparse 725 ± 141，Cheetah Run 643 ± 9，Hopper Hop 275 ± 3，Quadruped Walk 435 ± 76，Walker Run 762 ± 6；在 Acrobot Swingup 上基本持平，Dream-MPC 为 288 ± 31，BMPC 仅策略为 292 ± 18。
- 论文认为，当 Dream-MPC 配合来自 BMPC 的强策略先验时，可以优于无梯度 MPC，同时使用的模型评估次数远少于 MPPI。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04568v1](https://arxiv.org/abs/2605.04568v1)
