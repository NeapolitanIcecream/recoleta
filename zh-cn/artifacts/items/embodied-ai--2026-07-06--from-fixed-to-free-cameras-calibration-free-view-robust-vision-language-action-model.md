---
source: arxiv
url: https://arxiv.org/abs/2607.05396v1
published_at: '2026-07-06T17:59:59'
authors:
- Wenhao Li
- Xueying Jiang
- Quanhao Qian
- Deli Zhao
- Shijian Lu
- Gongjie Zhang
- Ran Xu
topics:
- vision-language-action
- robot-manipulation
- viewpoint-generalization
- hand-eye-calibration
- monocular-rgb
- robot-foundation-models
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# From Fixed to Free Cameras: Calibration-Free View-Robust Vision-Language-Action Model

## Summary
## 摘要
CamVLA 是一种免标定 VLA 方法，在摄像头移动或重新安装后仍能让机器人操作保持可用。它在摄像头坐标系中预测动作，从一张 RGB 图像估计摄像头到机器人的位姿，并把动作转换到机器人基座坐标系。

## 问题
- 标准 VLA 根据摄像头视角图像预测机器人基座坐标系中的动作，因此摄像头位姿变化可能破坏已学习到的视觉到动作映射。
- 以往具备视角容忍能力的 VLA 方法通常要求部署时已知摄像头外参；当摄像头漂移、被碰动或重新安装时，这一要求会失效。
- 论文报告称，π0 在 RLBench 上的成功率从训练视角下约 65.3% 降至摄像头旋转 15° 后的 6.3%。

## 方法
- CamVLA 有两个头：动作头预测局部摄像头坐标系中的末端执行器增量动作，几何头预测摄像头与机器人基座之间的 6-DoF 手眼矩阵。
- 模型使用单目 RGB 图像、机器人状态和语言指令。部署时无需深度、外部摄像头标定或多视角输入。
- 一个确定性变换把预测的摄像头坐标系平移与旋转增量转换为基座坐标系中的机器人动作。
- 该方法在手眼位姿中预测平移用于几何监督，虽然相对动作执行依赖预测的旋转。

## 结果
- 在 RLBench 的 6 个任务未见视角上，加入 CamVLA 后，π0 的平均成功率从 33.2% 提高到 51.4%，绝对提升 18.2 个百分点。
- 在同一 RLBench 设置中，加入 CamVLA 后，GR00T N1.7 的平均成功率从 28.4% 提高到 38.4%，绝对提升 10.0 个百分点。
- 在真实世界 Franka 实验的 5 个家务任务中，π0 + CamVLA 在 0°、5°、10° 和 15° 摄像头偏移下的平均成功率分别为 79.0%、68.0%、55.3% 和 29.3%；相比之下，π0 分别为 63.3%、53.3%、39.3% 和 16.0%。
- 在同一真实世界设置中，GR00T N1.7 + CamVLA 在 0°、5°、10° 和 15° 下分别达到 80.7%、72.3%、53.0% 和 33.0%；相比之下，GR00T 分别为 64.7%、52.0%、35.7% 和 14.7%。
- 真实世界手眼误差在 0° 下为 1.35 cm / 2.49°，5° 下为 2.12 cm / 4.73°，10° 下为 7.91 cm / 5.98°，15° 下为 27.16 cm / 9.39°。
- 几何头增加 6.30M 参数、1.0G FLOPs，并在 RTX 4090 上增加 1 ms 延迟：总量为 3244.4M 参数、661.9G FLOPs、62 ms 推理时间；相比之下，π0 为 3238.1M、660.9G 和 61 ms。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.05396v1](https://arxiv.org/abs/2607.05396v1)
