---
source: arxiv
url: https://arxiv.org/abs/2606.18697v1
published_at: '2026-06-17T05:24:18'
authors:
- Yibin Hu
- Xiaolin Sun
- Zizhan Zheng
topics:
- world-model
- data-poisoning
- model-based-rl
- planning-security
- continuous-control
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# Stealthy World Model Manipulation via Data Poisoning

## Summary
## 摘要
SWAAP 是一种针对学习型世界模型的两阶段数据投毒攻击，这类世界模型用于基于模型的规划。它表明，修改微调转移目标中的一个有界子集，可以把世界模型推向有害动力学，同时让投毒数据接近正常预测误差。

## 问题
- 学习型世界模型会根据收集到的轨迹更新，因此被攻破的微调缓冲区可以在不直接访问已部署模型权重的情况下改变后续规划行为。
- 现有的监督学习投毒方法不适合这一设置，因为下一状态目标有结构、高维，并且会影响长时域 rollout。
- 这一风险影响机器人、自主系统以及其他在部署后依赖世界模型适应的基于模型的智能体。

## 方法
- 阶段 1 搜索一个目标世界模型，使其降低真实环境回报，同时保持接近干净动力学。
- 论文使用一阶双层方法和转移梯度定理来更新转移模型参数，无需对完整规划器或策略优化器求导。
- 阶段 2 通过只修改微调集中的选定下一状态目标来投毒数据，保持状态、动作和奖励不变。
- 它选择在目标模型下残差最大的 top-rp 比例转移，然后优化投毒目标，使其训练梯度匹配会把受害模型推向阶段 1 目标的梯度。
- 预测误差正则项让投毒目标接近干净模型的自然单步误差；轨迹一致变体会在相邻转移之间一致地修改共享中间状态。

## 结果
- 摘录没有给出实验中的定量回报下降、投毒率或防御成功率。
- 论文称 SWAAP 是首个为深度基于模型强化学习中的学习型世界模型动力学构建的数据投毒攻击。
- 它评估了 2 个世界模型智能体：TD-MPC2 和 DINO-WM。
- 它报告了在 3 个基准套件上的实验：DMControl、MyoSuite 和 MetaWorld。
- 它评估了针对 3 个防御阶段的隐蔽性：训练前转移检测、使用 TRIM 的鲁棒微调，以及测试时模型监控。
- 文中给出的定性结果是，对一小部分微调数据进行投毒会造成大幅性能下降，同时避开所评估的 residual、CUSUM 和 TRIM-style 防御，但摘录没有提供具体数值差距。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.18697v1](https://arxiv.org/abs/2606.18697v1)
