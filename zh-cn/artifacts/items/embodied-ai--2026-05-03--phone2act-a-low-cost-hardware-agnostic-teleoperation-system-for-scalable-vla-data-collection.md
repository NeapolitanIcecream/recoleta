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
## 摘要
Phone2Act 将一部 Android 手机变成 6-DoF 机器人遥操作器，并直接以 LeRobot 格式记录同步示范。论文面向 VLA 训练数据采集，因为成本和机器人专用工具限制了数据集增长。

## 问题
- VLA 机器人策略需要真实操作示范，但实体数据采集的成本高于网页规模的数据采集。
- 主从式机械臂、VR 控制器和平台专用遥操作栈增加了硬件成本和工程工作量。
- 使用不同机械臂的实验室需要一种通用方法来采集可直接用于训练的示范，而不用为每台机器人重写控制和记录栈。

## 方法
- Android 应用使用 Google ARCore，以 50 Hz 通过 WebSocket 向 ROS 2 发布手机位姿和按键事件。
- ROS 2 规划器将手机运动映射为机器人的笛卡尔目标位姿，并加入离合重定位、工作空间限制、零跳变滤波器和 RPY 增量处理。
- 机器人专用桥接节点把共享的目标位姿和夹爪主题转换为各机器人 API 调用；论文描述了一个 Dobot CR5 桥接器和一个双臂 SO-101 配置。
- Universal Recorder 以 20 Hz 同步 RGB 相机帧、关节状态、末端执行器位姿和夹爪状态，然后以 LeRobot 数据集格式写入 MP4 和 Parquet 文件。

## 结果
- 在 130 个 Phone2Act 片段上微调 GR00T-N1.5-3B 后，真实世界成功率达到 90%：在 Dobot CR5 的球入篮任务上 10 次试验中成功 9 次。
- 在论文报告的任务中，系统以每分钟 2 到 3 个片段的速度采集示范。
- 端到端的手机运动到机器人执行延迟为 350–440 毫秒，平均 395 毫秒；该结果是在 2.4 GHz Wi-Fi 下用 240 FPS 高速视频测得。
- 记录器运行频率为 20 Hz，而手机位姿输入频率为 50 Hz。
- GR00T 微调使用一块 NVIDIA RTX A6000，有效批大小 48，峰值学习率 1e-4，bfloat16，10 步动作块，以及 7D 动作空间。
- 到 2,000 步时，训练损失在 0.05 MSE 附近趋于平稳；论文还报告了在留出轨迹上的定性开环跟踪表现。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01948v1](https://arxiv.org/abs/2605.01948v1)
