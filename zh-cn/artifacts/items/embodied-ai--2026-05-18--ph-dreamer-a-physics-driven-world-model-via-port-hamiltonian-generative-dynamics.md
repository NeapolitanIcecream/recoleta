---
source: arxiv
url: https://arxiv.org/abs/2605.18303v1
published_at: '2026-05-18T12:20:54'
authors:
- Xueyu Luan
- Chenwei Shi
topics:
- world-model
- model-based-rl
- port-hamiltonian
- visual-control
- energy-regularization
- physics-informed-rl
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# PH-Dreamer: A Physics-Driven World Model via Port-Hamiltonian Generative Dynamics

## Summary
## 总结
PH-Dreamer 为基于 RSSM 的世界模型加入 Port-Hamiltonian 能量结构，使想象 rollout 按照学到的流动、耗散和动作功率信号运行。在 DeepMind Control 的六个视觉控制任务上，它的回报高于 DreamerV3 和 R2Dreamer，同时还降低了相空间体积、能耗和 jerk。

## 问题
- 像 Dreamer 和 R2Dreamer 这样的 RSSM 世界模型会学习视觉动力学，但没有显式的能量或耗散结构，所以长时间的想象 rollout 可能会偏离物理行为。
- 物理先验的强化学习方法通常需要手写方程、低维状态或可微分模拟器，这限制了它们在视觉控制任务中的使用。
- 这个问题很重要，因为基于模型的智能体会在自己学到的模拟器里训练策略；想象动力学出错会降低真实环境回报，还会产生低效或发抖的控制。

## 方法
- 该方法把确定性的 RSSM 状态拆成物理部分和残差环境部分，然后把物理部分投影到低维相空间。
- Port-Hamiltonian 影子转移用学习到的 Hamiltonian、流动矩阵、耗散矩阵和动作输入矩阵预测下一个投影潜变量；主 RSSM 仍然是骨干，PH 损失对投影动力学做正则化。
- PH 损失用 RK4 积分和退火权重训练，这样视觉模型先学到有用特征，再施加强物理正则。
- 单独的能量模型根据最近的关节坐标历史估计动量，计算动能和势能，并通过做功和耗散项预测动作引起的能量变化。
- Actor-Critic 阶段加入拉格朗日乘子约束，对预测的能量变化和沿动作方向的 Hamiltonian 曲率进行约束，让策略更偏向低能量、更平滑的动作。

## 结果
- 在六个 DeepMind Control 视觉任务、500k 步条件下，PH-Dreamer 的平均评估回报最好，达到 789.2；R2Dreamer 为 762.5，DreamerV3 为 735.1，Dreamer-INFO 为 698.3，HRSSM 为 695.5，DreamerPro 为 679.9。
- PH-Dreamer 在各任务上的评估回报分别是：Cheetah Run 798.6、Walker Stand 974.7、Reacher Easy 985.1、Hopper Hop 314.8、Walker Walk 967.2、Walker Run 694.8；这些数值都高于表 1 中列出的基线。
- 想象回报平均值为 738.9，高于 R2Dreamer 的 702.5 和 DreamerV3 的 689.1，支持论文关于想象回报与评估表现更一致的说法。
- 相对于 R2Dreamer，投影后的对数相空间体积在 Cheetah Run 上下降 7.35%，在 Walker 任务上下降 4.18%，在 Reacher Easy 上下降 8.00%，在 Hopper Hop 上下降 8.41%。
- 摘要报告能耗最高降低 7.80%，均方 jerk 最多降低 9.38%。
- 论文称，学到的能量模型能在六个 DMC 任务上跟踪 MuJoCo 的真实机械能，但给出的摘录里没有数值形式的能量预测误差。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.18303v1](https://arxiv.org/abs/2605.18303v1)
