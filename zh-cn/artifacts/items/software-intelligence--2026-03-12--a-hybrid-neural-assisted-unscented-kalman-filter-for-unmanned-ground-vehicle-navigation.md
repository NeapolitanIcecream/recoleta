---
source: arxiv
url: http://arxiv.org/abs/2603.11649v1
published_at: '2026-03-12T08:20:26'
authors:
- Gal Versano
- Itzik Klein
topics:
- unscented-kalman-filter
- sensor-fusion
- ugv-navigation
- sim2real
- noise-estimation
relevance_score: 0.14
run_id: materialize-outputs
language_code: zh-CN
---

# A Hybrid Neural-Assisted Unscented Kalman Filter for Unmanned Ground Vehicle Navigation

## Summary
本文提出一种神经网络辅助的无迹卡尔曼滤波器（ANPMN-UKF），用于无人地面车辆的INS/GNSS融合导航，在不改动UKF核心方程的前提下自适应估计时变噪声。其关键卖点是仅用仿真数据训练、再直接泛化到多种真实车辆与环境。

## Problem
- 传统UKF通常使用固定的过程噪声协方差 **Q** 和测量噪声协方差 **R**，难以适应真实世界中随时间变化的传感器噪声和环境扰动。
- 当 **Q/R** 调参不准时，导航定位会变差，甚至导致滤波不稳定；这对无人车连续、可靠定位很关键。
- 纯模型自适应方法能在线调整噪声，但往往难以捕捉复杂、非线性的噪声变化模式。

## Approach
- 作者提出 **ANPMN-UKF**：保持标准UKF预测/更新公式不变，只额外加入两个小型神经网络来预测噪声大小。
- **σQ-Net** 从原始IMU窗口数据（3轴加速度+3轴陀螺，1秒/100点）回归惯性噪声标准差，用来构造过程噪声协方差 **Q**。
- **σR-Net** 从GNSS位置窗口数据（3通道，1秒/100点）回归位置噪声标准差，用来构造测量噪声协方差 **R**。
- 网络骨干是共享设计的1D卷积+全连接+层归一化结构，目标是轻量、实时、适合时序噪声回归。
- 训练采用 **sim2real**：在5类仿真轨迹上生成100Hz数据，并注入25档噪声（IMU噪声标准差范围 **[0.001, 0.02]**，GNSS位置噪声标准差范围 **[1.5, 3.0] m**），仅用仿真真值监督训练MSE损失。

## Results
- 在 **3个真实数据集**、总计 **160分钟** 测试中评估，覆盖 **越野车、乘用车、移动机器人**，以及不同IMU、路面和环境条件。
- 论文声称整体平均定位精度相对标准 **UKF 提升 22.70%**。
- 相对 **基于模型的自适应UKF**，平均定位提升 **12.72%**。
- 摘要中同样强调：跨3个数据集，相比自适应模型方法获得 **12.7%** 的位置改进，说明与正文的 **12.72%** 基本一致。
- 文本未给出更细粒度的逐数据集数值、绝对误差、方差或显著性检验；最强定量结论是上述两项平均相对提升。

## Link
- [http://arxiv.org/abs/2603.11649v1](http://arxiv.org/abs/2603.11649v1)
