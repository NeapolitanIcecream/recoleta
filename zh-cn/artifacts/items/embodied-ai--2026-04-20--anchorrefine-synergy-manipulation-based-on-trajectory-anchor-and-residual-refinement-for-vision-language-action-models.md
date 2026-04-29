---
source: arxiv
url: http://arxiv.org/abs/2604.17787v1
published_at: '2026-04-20T04:25:24'
authors:
- Tingzheng Jia
- Kan Guo
- Lanping Qian
- Yongli Hu
- Daxin Tian
- Guixian Qu
- Chunmian Lin
- Baocai Yin
- Jiapu Wang
topics:
- vision-language-action
- robot-manipulation
- hierarchical-policy
- residual-refinement
- gripper-control
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# AnchorRefine: Synergy-Manipulation Based on Trajectory Anchor and Residual Refinement for Vision-Language-Action Models

## Summary
## 概要
AnchorRefine 将机器人动作预测拆分为粗粒度的轨迹锚点和小幅修正两个部分。论文针对视觉-语言-动作策略中的精度失误，并报告其在 LIBERO、CALVIN 和真实机器人测试中都带来稳定提升。

## 问题
- 标准 VLA 策略在一个空间中预测完整动作块，因此大幅度机械臂运动主导训练，而小幅修正信号得到的监督较弱。
- 这会损害对精度要求高的操作任务，例如最终位姿对齐、接触时机和夹爪闭合；在这些场景里，细小误差就可能让任务从成功变为失败。
- 论文指出夹爪控制是主要失败来源：在他们对 LIBERO 的分析中，超过 88% 的失败与夹爪相关错误有关。

## 方法
- AnchorRefine 采用两阶段动作模型：锚点规划器先预测粗略动作轨迹，然后细化模块预测该锚点与真实动作之间的残差误差。
- 对机械臂运动，最终动作是 `anchor + residual`，因此第二个模块只需学习粗略规划之后剩余的小幅修正。
- 训练按顺序进行：先用原始动作目标训练锚点规划器，再将其冻结，并用相对于锚点的残差来训练残差分支。
- 对夹爪控制，论文加入了一个决策感知的细化头，根据锚点夹爪预测距离开合决策边界的接近程度进行修正。
- 该方法可以接入基于回归和基于扩散的 VLA 主干模型，文中用 GR-1 和 X-VLA 进行了展示。

## 结果
- 在 **LIBERO-LONG** 上，**AnchorRefine (GR-1)** 将成功率从 **74.5%** 提高到 **82.3%**，提升 **+7.8** 个百分点。
- 在 **LIBERO-LONG** 上，**AnchorRefine (X-VLA)** 将成功率从 **95.8%** 提高到 **97.4%**，提升 **+1.6** 个百分点。
- 在 **CALVIN ABC→D** 上，**AnchorRefine (GR-1)** 将 5 任务链成功率从 **52.0%** 提高到 **55.3%**（**+3.3**），将 3 任务成功率从 **68.5%** 提高到 **71.9%**（**+3.4**），并将平均序列长度从 **3.51** 提高到 **3.64**（**+0.13**）。
- 在 **CALVIN ABC→D** 上，**AnchorRefine (X-VLA)** 将 5 任务链成功率从 **74.6%** 提高到 **76.5%**（**+1.9**），将 4 任务成功率从 **81.3%** 提高到 **83.7%**（**+2.4**），将 3 任务成功率从 **86.9%** 提高到 **89.1%**（**+2.2**），并将平均序列长度从 **4.31** 提高到 **4.40**（**+0.09**）。
- 摘要称，仿真成功率最高提升 **7.8%**，真实世界成功率最高提升 **18%**。
- 在列出的 LIBERO 结果中，**AnchorRefine (X-VLA)** 达到 **97.4%**，高于表中报告的 **95.8%** 的 X-VLA 基线和 **95.2%** 的 AtomicVLA 结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17787v1](http://arxiv.org/abs/2604.17787v1)
