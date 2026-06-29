---
source: arxiv
url: https://arxiv.org/abs/2605.21330v1
published_at: '2026-05-20T15:57:27'
authors:
- Senlan Yao
- Chenyu Yang
- Jaehoon Kim
- Aristotelis Sympetheros
- Robert K. Katzschmann
topics:
- dexterous-manipulation
- proprioceptive-control
- transformer-policy
- in-hand-rotation
- sim2real
- joint-sensing
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Learning Robust Dexterous In-Hand Manipulation from Joint Sensors with Proprioceptive Transformer

## Summary
## 摘要
本体感知 Transformer 仅用关节位置和速度历史，就学会了在腱驱动的 ORCA 机械手上持续旋转立方体。论文声称，纯关节控制在真实硬件上的表现可以超过基于视觉和 PPO 的基线。

## 问题
- 灵巧手内操作通常需要相机或触觉传感器来跟踪物体，这会带来遮挡、标定、计算开销和仿真到现实的失败点。
- 大多数机器人手都有关节传感，但在腱驱动机械手上，电机编码器可能会误读真实的手指状态，因为电缆拉伸、摩擦和回差会影响读数。
- 这个任务之所以重要，是因为如果机械手能从自身关节推断物体状态，它就能在没有外部位姿跟踪的情况下操作物体。

## 方法
- 教师策略在 Isaac Lab 中用 PPO 和特权物体位姿训练，使用 8192 个并行的 ORCA 机械手仿真环境。
- 学生策略 Proprioceptive Transformer 只接收一段时间窗口内带噪声的关节位置和速度，以及上一动作、上一指令和目标指令。
- 该 Transformer 通过关节历史上的自注意力，从运动模式中推断隐藏的接触信息和物体信息。
- 训练把来自教师的行为克隆和辅助重建损失结合起来，重建目标包括物体位置、干净的关节位置和干净的关节速度。
- 真实的 ORCA 机械手在手指关节上使用 16 个 AS5600 磁角度传感器，论文比较了这些直接关节读数和电机编码器读数。

## 结果
- 在 55 mm 立方体上，PT-Joint 达到 11.83 ± 0.52 RPM，而 Proprio-PPO 为 3.83 ± 0.51 RPM，Extero-PPO 为 3.08 ± 0.12 RPM。
- 在 55 mm 立方体上，PT-Joint 的旋转准确率为 100 ± 0%，无掉落成功率为 100 ± 0%，在 3 次 60 秒试验中没有掉落。
- 在 65 mm 立方体上，PT-Joint 达到 11.33 ± 0.12 RPM，而 Proprio-PPO 为 5.17 ± 0.12 RPM，Extero-PPO 为 4.83 ± 0.12 RPM，PT-Motor 为 8.53 ± 1.48 RPM。
- 直接关节传感在 55 mm 立方体上比电机编码器更快：PT-Joint 为 11.83 RPM，PT-Motor 为 9.33 RPM，提升 26.8%。
- 对于根据关节历史重建物体位置，Transformer 在 32 个仿真环境中的 RMSE 为 13.70 ± 4.62 mm，而 MLP 为 17.87 ± 4.60 mm，LSTM 为 15.64 ± 4.46 mm。
- 对于干净关节状态重建，Transformer 的关节位置 RMSE 为 0.098 rad、速度 RMSE 为 0.070 rad/s，而 LSTM 分别为 0.110 rad 和 0.112 rad/s。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.21330v1](https://arxiv.org/abs/2605.21330v1)
