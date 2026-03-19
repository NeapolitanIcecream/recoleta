---
source: arxiv
url: http://arxiv.org/abs/2603.11110v1
published_at: '2026-03-11T11:27:08'
authors:
- Jseen Zhang
- Gabriel Adineera
- Jinzhou Tan
- Jinoh Kim
topics:
- visual-rl
- model-based-rl
- world-models
- continuous-control
- residual-actions
- robotics
relevance_score: 0.35
run_id: materialize-outputs
language_code: zh-CN
---

# ResWM: Residual-Action World Model for Visual RL

## Summary
ResWM针对视觉连续控制中的世界模型学习不稳定问题，把动作从“绝对动作”改写为“相对上一步的残差动作”，以获得更平滑、更稳定的控制。它还用相邻观测差分来建模动态变化，并在DMControl上报告了比Dreamer、TD-MPC及多种像素RL基线更好的样本效率和最终回报。

## Problem
- 现有视觉模型式RL通常直接用绝对动作条件化未来预测，但最优绝对动作分布任务相关、先验未知，导致优化高方差、长时规划不稳定。
- 这种建模方式容易产生振荡或抖动控制，在机器人和连续控制场景中会带来低效、能耗高甚至安全风险。
- 纯静态帧编码会保留大量冗余背景信息，不利于捕捉真正驱动控制变化的时序动态。

## Approach
- 将策略和世界模型中的控制变量从绝对动作改为残差动作：策略预测增量 \(\delta a_t\)，最终动作为 \(a_t=\tanh(a_{t-1}+\delta a_t)\)。
- 在Dreamer风格的RSSM中，潜在动力学和奖励预测都直接条件于残差动作，而不是绝对动作，使想象 rollout 与策略优化使用同一种动作表示。
- 提出 Observation Difference Encoder，通过相邻观测的特征差 \(f(o_t)-f'(o_{t-1})\) 提取动态变化，形成更紧凑、与残差控制天然匹配的潜表示。
- 在演员优化中加入对残差动作的KL先验约束，并可选加入能量惩罚 \(\|\delta a_t\|_2^2\)，抑制过大、抖动的控制更新。
- 该方法声称只需对Dreamer式框架做最小改动，且不引入额外超参数。

## Results
- 在DMControl 6个常见任务上，ResWM在 **100K steps** 的平均分为 **828.7**，高于 **DeepRAD 695.1**、**RAD 663.6**、**DeepMDP 460.5**、**pixel SAC 167.3**。
- 在相同6任务上，ResWM在 **500K steps** 的平均分为 **925.0**，高于 **DeepRAD 890.8**、**RAD 872.5**、**DeepMDP 764.6**、**pixel SAC 216.8**。
- 具体任务上，100K时 ResWM 达到 **Cartpole 845**（vs DeepRAD **703**）、**Reacher 942**（vs **792**）、**Cheetah 542**（vs **453**）、**Walker 694**（vs **582**）、**Finger 986**（vs **832**）、**Ball-in-cup 963**（vs **809**）。
- 500K时，ResWM达到 **Cartpole 882**（vs DeepRAD **870**）、**Reacher 986**（vs **942**）、**Cheetah 783**（vs **721**）、**Walker 957**（vs **925**）、**Finger 964**（vs **932**）、**Ball-in-cup 978**（vs **954**）。
- 文中还声称在更强基线比较中可超过 **ResAct**（例如困难任务1M steps平均 **644.8 vs 630.2**），并超过 **TACO 887.1**、**MaDi 885.1**；但这些结果在给定摘录中未完整展开实验表。
- 除回报外，论文宣称ResWM还能产生更平滑、更稳定、更节能的动作轨迹，并减少长时预测误差；不过摘录里未给出动作平滑性/能耗的明确量化指标。

## Link
- [http://arxiv.org/abs/2603.11110v1](http://arxiv.org/abs/2603.11110v1)
