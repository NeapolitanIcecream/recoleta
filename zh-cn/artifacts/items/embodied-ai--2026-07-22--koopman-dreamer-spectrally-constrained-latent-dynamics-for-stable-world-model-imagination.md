---
source: arxiv
url: https://arxiv.org/abs/2607.19719v1
published_at: '2026-07-22T03:38:15'
authors:
- Jiaqi Li
- Xinglong Zhang
- Haibin Xie
- Yixing Lan
- Wei Pan
- Xin Xu
topics:
- world-model
- model-based-reinforcement-learning
- koopman-dynamics
- latent-imagination
- continuous-control
- autonomous-navigation
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# Koopman Dreamer: Spectrally Constrained Latent Dynamics for Stable World-Model Imagination

## Summary
## 摘要
Koopman Dreamer 在 DreamerV3 风格的世界模型中加入受谱约束的确定性潜在状态转移，以提高长时域想象的稳定性。该方法在模拟连续控制任务中取得了更好的性能，包括在 DeepMind Control Suite 的九项任务中有八项获得提升；在 UAV-LiDAR 任务中，目标成功率从 53.8% 提高到 73.8%。

## 问题
- 通用神经潜在状态转移无法直接控制模态持续性、阻尼或振荡，因此长时域滚动预测中的误差难以调节和诊断。
- 误差累积会使想象回报、策略更新和控制决策产生偏差，尤其是在连续控制和自主导航任务中。
- 过度收缩也可能抹去控制所需的信息，因此必须在稳定性与长期信息保留之间取得平衡。

## 方法
- 将 DreamerV3 的传统确定性循环状态转移替换为受 Koopman 启发的主干网络。该网络由二维旋转—缩放模块组成，其模态半径限制在预先设定的谱范围内。
- 加入线性动作效应、低秩双线性状态—动作项和随机状态调制，使结构化主干网络能够表示受控非线性动力学以及局部后验修正。
- 使用 EMA 教师目标、单步一致性、多步滚动预测和开环观测预测目标，训练同一个状态转移同时支持以后验为条件的学习和无后验想象。
- 推导多步滚动预测误差界，将自主谱放大、双线性交互效应、随机状态不匹配和建模残差区分开来。

## 结果
- 在本体感知连续控制任务中，Koopman Dreamer 在九项模拟任务中的八项优于 DreamerV3。
- 在使用向量化 LiDAR 观测的模拟 UAV 导航任务中，目标成功率从 DreamerV3 的 53.8% 提高到 Koopman Dreamer 的 73.8%，提升了 20.0 个百分点。
- 开环评估显示，本体感知观测和速度预测的提升最为稳定；在大多数任务中，回报预测也有所改善。
- 谱半径敏感性分析和消融研究支持模态收缩、EMA 教师目标以及状态依赖的动作效应所发挥的作用，同时表明收缩性最强的设置不一定最有利于控制。
- 报告的验证基于模拟；摘录未提供真实物理机器人上的结果，也未提供完整的逐任务指标表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.19719v1](https://arxiv.org/abs/2607.19719v1)
