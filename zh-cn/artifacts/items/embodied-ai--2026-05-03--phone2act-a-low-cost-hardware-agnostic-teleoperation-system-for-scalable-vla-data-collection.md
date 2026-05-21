---
source: arxiv
url: https://arxiv.org/abs/2605.01948v1
published_at: '2026-05-03T16:17:16'
authors:
- Om Mandhane
- Bipin Yadav
- Sangeetha Prasanna Ram
- Gopalakrishnan Narayanan
topics:
- vision-language-action
- robot-data-collection
- teleoperation
- lerobot
- generalist-robot-policy
- robot-data-scaling
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Phone2Act: A Low-Cost, Hardware-Agnostic Teleoperation System for Scalable VLA Data Collection

## Summary
## 概要
Phone2Act 将一部 Android 手机变成 6 自由度机器人遥操作器，并以 LeRobot 格式直接记录同步的演示数据。论文面向 VLA 训练数据采集；在这类采集中，成本和面向特定机器人的工具限制了数据集增长。

## 问题
- VLA 机器人策略需要真实的操作演示，但实体数据采集的成本高于 Web 规模的数据采集。
- 主从机械臂、VR 控制器和平台专用遥操作栈会增加硬件成本和工程工作量。
- 使用不同机械臂的实验室需要一种通用方法来采集可直接用于训练的演示数据，而不必为每种机器人重写控制和日志记录栈。

## 方法
- Android 应用使用 Google ARCore 获取手机位姿和按钮事件，并以 50 Hz 通过 WebSocket 发布到 ROS 2。
- ROS 2 规划器将手机运动映射为机器人的笛卡尔目标位姿，并支持离合式重定位、工作空间限制、零跳变过滤器和 RPY 增量处理。
- 机器人专用桥接节点将共享的目标位姿和夹爪 topic 转换为各机器人的 API 调用；论文描述了一个 Dobot CR5 桥接节点和一个双臂 SO-101 配置。
- Universal Recorder 以 20 Hz 同步 RGB 相机帧、关节状态、末端执行器位姿和夹爪状态，然后以 LeRobot 数据集格式写入 MP4 和 Parquet 文件。

## 结果
- 在 130 个 Phone2Act episode 上微调 GR00T-N1.5-3B 后，在真实世界中达到 90% 的成功率：在 Dobot CR5 球到篮筐任务的 10 次试验中成功 9 次。
- 在报告的任务中，系统以每分钟 2–3 个 episode 的速度采集演示数据。
- 端到端手机运动到机器人执行的延迟为 350–440 ms，平均 395 ms；该结果是在 2.4 GHz Wi-Fi 下用 240 FPS 高速视频测得的。
- 记录器以 20 Hz 运行，手机位姿输入以 50 Hz 运行。
- GR00T 微调使用一块 NVIDIA RTX A6000，有效 batch size 为 48，峰值学习率为 1e-4，bfloat16，10 步 action chunks，以及 7D action space。
- 训练损失在 2,000 step 时接近 0.05 MSE 并进入平台期；论文还报告了在留出轨迹上的定性开环跟踪结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01948v1](https://arxiv.org/abs/2605.01948v1)
