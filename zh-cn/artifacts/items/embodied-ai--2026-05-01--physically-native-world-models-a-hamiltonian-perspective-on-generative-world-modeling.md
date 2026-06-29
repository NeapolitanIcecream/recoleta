---
source: arxiv
url: https://arxiv.org/abs/2605.00412v1
published_at: '2026-05-01T05:09:32'
authors:
- Sen Cui
- Jingheng Ma
topics:
- hamiltonian-dynamics
- world-models
- embodied-ai
- model-based-planning
- robotics
- physical-priors
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Physically Native World Models: A Hamiltonian Perspective on Generative World Modeling

## Summary
## 摘要
本文认为，具身世界模型需要带有物理结构的潜在动力学，才能做动作条件下的预测。文中提出 Hamiltonian World Models：把观测编码到相空间变量中，用受 Hamiltonian 启发的动力学推进这些变量，解码出未来观测，并把展开结果用于规划。

## 问题
- 机器人和自主智能体需要在动作条件下保持物理可行的预测，因为如果规划建立在错误的展开结果上，就可能选出不安全或会失败的动作。
- 现有的 2D 视频模型、3D 场景模型和类似 JEPA 的潜在模型优化目标不同，容易漏掉接触、动量、物体恒常性、动作影响或长时域稳定性。
- 典型的潜在状态转移，如 z_{t+1}=fθ(z_t,a_t)，常把外观、语义和运动混在一起，这会提高数据需求，也会让误差在规划时域里累积。

## 方法
- 核心机制很直接：把过去观测编码为潜在相空间状态 z_t=[q_t,p_t]，其中 q 表示广义坐标，p 表示广义动量。
- 学习一个类似能量的标量 H(q,p)，再从它的梯度推导潜在运动：qdot=∂H/∂p，pdot=-∂H/∂q。
- 加入动作控制、耗散和残差项，使模型能够处理机器人、摩擦、接触、碰撞以及其他非保守效应。
- 将预测出的潜在轨迹解码为未来观测，然后用效用函数对候选动作序列打分，供规划使用。
- 文中提出的架构包含 4 个命名部分：encoder Eθ、Hamiltonian rollout T_H、decoder Dθ，以及 planner 或 utility U。

## 结果
- 这段摘要没有报告基准数值，没有数据集结果，也没有与基线的直接比较。
- 主要贡献是概念层面的：它把当前世界模型分成 3 条路线，即 2D 视频生成、3D 场景中心建模和类似 JEPA 的潜在预测，并指出这些路线在物理建模上的缺口。
- 文中声称 Hamiltonian 结构可以通过保持相空间结构来提高长时域稳定性，尤其是在配合辛积分时；但没有给出展开长度指标。
- 文中声称它能提高数据效率，因为一个学到的能量函数可以在不同初始条件下约束动力学；但没有给出样本效率数值。
- 文中声称它能提高可解释性，因为潜在变量可以对应相空间坐标、动量、能量变化和交互项；但没有报告用户研究或诊断基准。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00412v1](https://arxiv.org/abs/2605.00412v1)
