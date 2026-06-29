---
source: arxiv
url: https://arxiv.org/abs/2606.04534v1
published_at: '2026-06-03T07:17:57'
authors:
- Xinhong Zhang
- Runqing Wang
- Yunfan Ren
- Ding Yu
- Boyu Zhou
- Jian Sun
- Fang Deng
- Jie Chen
- Gang Wang
topics:
- world-models
- quadrotor-flight
- occupancy-mapping
- sim2real
- reinforcement-learning
- agile-navigation
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# MAD: Mapping-Aware World Models for Agile Quadrotor Flight

## Summary
## 摘要
MAD 训练了一个四旋翼世界模型，从深度信息和本体感知预测局部占据图和可见性图，然后把这个潜在状态用于灵活飞行策略。论文报告称，它在视觉导航上优于仅视觉基线，并且在真实世界的森林飞行中达到 5.05 m/s。

## 问题
- 灵活四旋翼需要在部分可见、感知范围短和计算延迟紧的条件下避开障碍物。
- 传统导航栈使用里程计、建图、规划和跟踪，这会增加人工工程工作，也可能带来延迟或误差累积。
- 端到端视觉策略可以飞得很快，但它们往往缺少显式空间记忆，这让跨环境迁移和故障诊断更难。

## 方法
- MAD 使用类似 DreamerV3 的递归状态空间模型，训练输入包括深度图像、动作、奖励、持续标志和 9D 本体感知。
- 模型重建以机体为中心的占据栅格图和可见性栅格图，而不是把原始深度重建作为主要训练目标。
- 占据损失只在可见体素上计算，所以在监督时，未知空间不会被当作空闲或占据。
- DiffAero 在 GPU 上生成栅格图监督，使用覆盖 8 m × 8 m × 4 m 的局部三维网格，体素大小为 0.4 m，每张图有 4,000 个体素。
- 学到的潜在状态用于三种策略模式：用于想象轨迹展开的 MAD-Dreamer，以及在仿真交互时作为冻结特征编码器的 MAD-PPO 和 MAD-SHAC。

## 结果
- GPU 建图模块每秒可完成 4.84e8 次体素占据和可见性评估，运行在一块 GPU 上。
- 文中报告的工作站上，仿真加栅格图计算每秒可完成 1.21e5 次环境交互。
- 论文声称，基于 MAD 的智能体在成功率、飞行速度和跨任务迁移上都优于对应的仅视觉基线，但摘要片段没有给出具体成功率表格。
- 学到的策略在仿真中达到 9.66 m/s。
- 真实四旋翼使用 Intel RealSense D435i，在真实世界的森林实验中达到 5.05 m/s。
- 观测设置使用 18 × 32 的深度图像和一个 9D 本体感知向量，部署时把 MAD 编码器和 actor 导出为一个机载策略，输出加速度指令。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.04534v1](https://arxiv.org/abs/2606.04534v1)
