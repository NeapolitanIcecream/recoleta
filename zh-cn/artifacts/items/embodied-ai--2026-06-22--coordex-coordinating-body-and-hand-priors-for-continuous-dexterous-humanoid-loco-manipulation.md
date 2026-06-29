---
source: arxiv
url: https://arxiv.org/abs/2606.23680v1
published_at: '2026-06-22T17:59:20'
authors:
- Sikai Li
- Shuning Li
- Zhenyu Wei
- Yunchao Yao
- Chenran Li
- Mingyu Ding
topics:
- dexterous-manipulation
- humanoid-locomotion
- loco-manipulation
- latent-action-space
- reinforcement-learning
- motion-priors
relevance_score: 0.57
run_id: materialize-outputs
language_code: zh-CN
---

# CoorDex: Coordinating Body and Hand Priors for Continuous Dexterous Humanoid Loco-Manipulation

## Summary
## 概要
CoorDex 使用身体和手指的独立学习先验，训练带灵巧手的人形机器人在行走时抓取、搬运、打开和转动物体。

## 问题
- 人形机器人移动操作通常把行走和操作拆成不同阶段，这避开了更难的情形：机器人必须在身体仍在运动时完成抓取。
- 高自由度手让直接强化学习变难，因为策略必须同时协调平衡、手腕位置、手指预成形、接触和物体搬运。
- 这个问题很重要，因为真实人形机器人需要在运动中完成手指级操作，而不是只在停下后执行夹爪式开合动作。

## 方法
- CoorDex 训练两个运动先验：一个身体先验，用于移动、伸手和手腕定位；一个手腕稳定的手部先验，用于主动手指关节。
- 每个先验先从模拟演示中训练一个有特权信息的运动跟踪教师，再蒸馏成一个以本体感觉为条件的潜在先验和解码器。
- 下游 PPO 冻结两个先验，并在潜在空间中预测残差修正，而不是预测原始关节目标。
- 一个共享协调主干读取任务状态、物体几何、接触特征、本体感觉、先验均值和上一时刻残差；独立的残差头输出身体和手部的潜在修正。
- 解码后的动作是 29 自由度 Unitree G1 身体和 20 自由度 WUJI 手的关节位置目标，其中身体潜在维度为 16，手部潜在维度为 12。

## 结果
- 评估使用在 10,000 个并行 Isaac Lab 仿真环境中收集的 50,000 个 episode。
- 在 WalkGrab 上，CoorDex 达到 0.55 成功率、0.00 跌倒率和 0.40 掉落率；它在瓶子附近保持运动，在抓取点的前向速度约为 0.25 m/s。
- 在 OpenFridge 上，它达到 0.66 成功率和 0.00 跌倒率，门角度为 57.76°，目标为 60°。
- 在 WalkPickTurn 上，它达到 0.89 成功率、0.01 跌倒率、0.10 掉落率，以及 180° 转向任务的 9.98° 最小朝向误差。
- 在相同 PPO 预算下，WalkGrab 消融中的直接或较弱动作空间会失败：All Joint Space 的成功率为 0，到达率为 1.00，抓取率为 0.00，停止率为 0.86，跌倒率为 0.04；Body Prior + Hand Joint Space 的成功率为 0，到达率为 0.96，抓取率为 0.01，停止率为 0.90，跌倒率为 0.04。
- 在两个先验都可用时，Monolithic Latent Residual 仍只有 0.00 成功率、0.40 动作率和 0.02 跌倒率，而 CoorDex 达到 0.55 成功率、0.22 动作率和 0.00 跌倒率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23680v1](https://arxiv.org/abs/2606.23680v1)
