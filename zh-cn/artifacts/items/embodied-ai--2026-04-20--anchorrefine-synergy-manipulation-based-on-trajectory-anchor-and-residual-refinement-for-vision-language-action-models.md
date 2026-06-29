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
## 摘要
AnchorRefine 将机器人动作预测拆成一个粗轨迹锚点和一个小幅修正步骤。论文针对 vision-language-action 策略中的精度失误，在 LIBERO、CALVIN 和真实机器人测试中都报告了稳定提升。

## 问题
- 标准 VLA 策略把完整动作块放在同一个空间里预测，因此大幅机械臂运动会主导训练，小幅修正信号得到的监督很弱。
- 这会影响精度关键的操作，比如最终位姿对齐、接触时机和夹爪闭合，因为很小的误差就可能把成功变成失败。
- 论文把夹爪控制视为主要失误来源：他们的分析显示，LIBERO 中超过 88% 的失败涉及夹爪相关错误。

## 方法
- AnchorRefine 使用两阶段动作模型：锚点规划器先预测一条粗动作轨迹，然后修正模块预测该锚点与真实动作之间的残差。
- 对机械臂运动来说，最终动作是 `anchor + residual`，所以第二个模块只学习粗规划后剩下的小修正。
- 训练是顺序进行的：先用原始动作目标训练锚点规划器，再冻结它，并用相对锚点的残差训练残差分支。
- 对夹爪控制，论文加入了一个感知决策的修正头，根据锚点夹爪预测离张开/闭合决策边界有多近来进行修正。
- 该方法可以接入基于回归和基于扩散的 VLA 主干，文中用 GR-1 和 X-VLA 做了演示。

## 结果
- 在 **LIBERO-LONG** 上，**AnchorRefine (GR-1)** 将成功率从 **74.5% 提升到 82.3%**，提升 **7.8** 个百分点。
- 在 **LIBERO-LONG** 上，**AnchorRefine (X-VLA)** 将成功率从 **95.8% 提升到 97.4%**，提升 **1.6** 个百分点。
- 在 **CALVIN ABC→D** 上，**AnchorRefine (GR-1)** 将 5 任务链成功率从 **52.0% 提升到 55.3%**（**+3.3**），3 任务成功率从 **68.5% 提升到 71.9%**（**+3.4**），平均序列长度从 **3.51 提升到 3.64**（**+0.13**）。
- 在 **CALVIN ABC→D** 上，**AnchorRefine (X-VLA)** 将 5 任务链成功率从 **74.6% 提升到 76.5%**（**+1.9**），4 任务成功率从 **81.3% 提升到 83.7%**（**+2.4**），3 任务成功率从 **86.9% 提升到 89.1%**（**+2.2**），平均序列长度从 **4.31 提升到 4.40**（**+0.09**）。
- 摘要声称仿真成功率最高提升 **7.8%**，真实世界成功率最高提升 **18%**。
- 在列出的 LIBERO 结果中，**AnchorRefine (X-VLA)** 达到 **97.4%**，高于表中的 **95.8%** X-VLA 基线和 **95.2%** AtomicVLA 结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17787v1](http://arxiv.org/abs/2604.17787v1)
