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
论文认为，具身世界模型需要有物理结构的潜在动力学，才能做基于动作条件的预测。它提出哈密顿世界模型：把观测编码为相空间变量，用受哈密顿思想启发的动力学推进这些变量，解码未来观测，并用展开轨迹进行规划。

## 问题
- 机器人和自主智能体需要在动作作用下仍保持物理可行的预测，因为基于错误展开轨迹做规划可能会选择不安全或会失败的动作。
- 当前 2D 视频模型、3D 场景模型和类 JEPA 潜在模型优化的目标不同，可能漏掉接触、动量、物体恒存性、动作影响或长时域稳定性。
- z_{t+1}=fθ(z_t,a_t) 这类通用潜在转移常把外观、语义和运动纠缠在一起，这会提高数据需求，并让误差在规划时域内累积。

## 方法
- 核心机制是：把过去观测编码为潜在相状态 z_t=[q_t,p_t]，其中 q 表示广义坐标，p 表示广义动量。
- 学习一个类似能量的标量 H(q,p)，再由它的梯度推出潜在运动：qdot=∂H/∂p，pdot=-∂H/∂q。
- 加入动作控制、耗散和残差项，使模型能够处理机器人、摩擦、接触、碰撞以及其他非保守效应。
- 将预测的潜在轨迹解码为未来观测，再用效用函数给候选动作序列打分以进行规划。
- 该架构包含 4 个命名部分：编码器 Eθ、哈密顿展开 T_H、解码器 Dθ，以及规划器或效用函数 U。

## 结果
- 摘录报告了 0 个基准数值、0 个数据集结果，以及 0 个与基线的直接比较。
- 论文声称的主要贡献是概念性贡献：它把当前世界模型分为 3 条路线，即 2D 视频生成、3D 场景中心和类 JEPA 潜在预测，并指出它们在物理建模上的缺口。
- 论文声称，哈密顿结构可以通过保持相空间结构来改善长时域稳定性，特别是在配合辛积分时；文中未提供展开长度指标。
- 论文声称，一个学到的能量函数可以约束不同初始条件下的动力学，因此能提高数据效率；文中未提供样本效率数值。
- 论文声称，潜在变量映射到相坐标、动量、能量变化和交互项，因此可解释性更好；文中未报告用户研究或诊断基准。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00412v1](https://arxiv.org/abs/2605.00412v1)
