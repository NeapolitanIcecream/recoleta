---
source: arxiv
url: https://arxiv.org/abs/2606.25591v1
published_at: '2026-06-24T08:59:59'
authors:
- Melya Boukheddimi
- Omar Adjali
- Daniel Sontag
- Frank Kirchner
topics:
- vision-language-action
- humanoid-locomotion
- optimal-control
- synthetic-robot-data
- whole-body-control
- robot-foundation-models
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# WOLF-VLA: Whole-Body Humanoid Optimal Locomotion Framework for Vision-Language-Action Learning

## Summary
## 摘要
WOLF-VLA 使用最优控制生成的示范，而不是遥操作数据，训练用于全身人形机器人运动的视觉-语言-动作策略。论文的核心主张是，最优控制轨迹可以为 VLA 训练提供动态可行、接触一致且可扩展的数据。

## 问题
- 现有 VLA 工作主要面向固定基座操作或复杂度较低的机器人任务，接触密集的人形机器人运动仍缺少 VLA 数据集和基准。
- 遥操作或动作捕捉数据采集成本高，并且常常没有显式的扭矩、关节限位、接触和能量准则。
- 人形机器人运动需要遵守动力学和安全约束的示范，因为跌倒、扭矩饱和和接触错误会让学习到的策略无法使用。

## 方法
- 系统通过求解多阶段最优控制问题来生成人形机器人示范，任务包括行走、侧向行走、上楼梯、上下楼梯、180° 转身和下蹲。
- 每条轨迹在满足关节、速度、扭矩和接触约束的同时，最小化质心跟踪误差、足部跟踪误差、扭矩和姿态偏差等代价。
- 示范在 MuJoCo 中用 RH5 运行；RH5 是带自由浮动基座和 25 个驱动关节的人形机器人。记录的输入包括本体感觉、第一视角 RGB 帧和自然语言任务指令。
- VLA 策略从 GR00T-N1.5-3B 初始化；其语言和视觉编码器保持冻结，投影层和动作扩散模块使用流匹配训练。
- 语言指令包含结构化的距离和高度标签，使模型能把任务文本与目标位置和楼梯高度联系起来。

## 结果
- 摘录没有给出数值化的成功率表或直接的策略性能数字，但称训练后的模型有竞争性表现，并测试了模态消融。
- WOLF-VLA-dataset 包含六类运动任务中的 277 小时人形机器人运动数据。
- 表 I 报告了 15,276 个 episode，平均 episode 长度为 28 s：WF 为 2,874 个 episode、13.5 s，WA 为 8,234 个、43.2 s，W.CS.U 为 2,358 个、21.6 s，W.CS.U/D 为 1,810 个、33.6 s。
- 场景变化包括六种目标类型、六种颜色、约 40 × 40 个目标放置位置，以及随机视觉干扰物。
- 视觉数据以 33.33 Hz 采集，来自 120° 第一视角摄像头，格式为 224 × 224 RGB 帧。
- 训练使用 4 块 NVIDIA A100 GPU、200,000 个梯度步、有效批大小 128、500 个 warmup 步、峰值学习率 1e-4 和最终学习率 1e-5。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.25591v1](https://arxiv.org/abs/2606.25591v1)
