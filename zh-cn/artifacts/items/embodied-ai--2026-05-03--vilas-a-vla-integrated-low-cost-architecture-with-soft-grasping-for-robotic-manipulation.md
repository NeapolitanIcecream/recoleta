---
source: arxiv
url: https://arxiv.org/abs/2605.02037v1
published_at: '2026-05-03T20:04:42'
authors:
- Zijian An
- Hadi Khezam
- Bill Cai
- Ran Yang
- Shijie Geng
- Yiming Feng
- Yue
- Zheng
- Lifeng Zhou
topics:
- vision-language-action
- robot-manipulation
- low-cost-robotics
- soft-grasping
- teleoperation-data
- fragile-object-grasping
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# VILAS: A VLA-Integrated Low-cost Architecture with Soft Grasping for Robotic Manipulation

## Summary
## 摘要
VILAS 是一个约 8,000 美元的机器人操作平台，用于在脆弱物体抓取任务上微调和部署 VLA 策略。它把工业协作机械臂、双 RGB-D 摄像头、遥操作数据采集和 kirigami 柔性夹爪延伸件结合在一起。

## 问题
- 像葡萄这样的脆弱物体会被刚性夹爪或突然的机器人动作压坏，所以操作需要柔和接触和稳定抓取。
- 许多 VLA 机器人系统依赖昂贵的一体化硬件；论文把约 8,000 美元的 VILAS 和约 33,000 美元的 ALOHA 套件做了比较。
- 力传感器、触觉阵列和力控制系统会增加成本和集成工作量，这限制了 VLA 策略研究的可用性。

## 方法
- 这个平台使用 Fairino FR5 机械臂、Jodell RG52-50 夹爪、GELLO 遥操作手臂、RealSense D455 基座摄像头、RealSense D405 腕部摄像头，以及基于 ZMQ 的控制栈。
- 人类操作员使用 GELLO 收集示范。每个时间步保存 7 自由度关节状态、两个 RGB 摄像头视图和一个语言提示。
- 一个 PEBA kirigami 延伸件安装在平行夹爪上，会在受压时弯曲，把接触面积分散到果实表面，并减少对力传感的依赖。
- 作者从公开检查点出发，在同一数据集上微调 pi_0、pi_0.5 和 GR00T N1.6：100 个 episode，每个 episode 1,200 帧，在 NVIDIA H200 上训练 50,000 次迭代。
- 部署时，机器人以 20 Hz 运行。pi_0 和 pi_0.5 输出 50 步动作块，GR00T N1.6 输出 16 步动作块。

## 结果
- 总硬件成本约为 8,000 美元，而 ALOHA 约为 33,000 美元。
- 在葡萄任务上，每个模型都测试了 50 次。单次抓取成功率分别为：pi_0 70%，pi_0.5 84%，GR00T N1.6 82%。
- 多次抓取成功率定义为至少连续两次抓取成功，pi_0 为 22%，pi_0.5 为 36%，GR00T N1.6 为 58%。
- 平均推理延迟分别为：pi_0 73.8 ms，pi_0.5 82.8 ms，GR00T N1.6 63.6 ms。
- 每步推理成本分别为：pi_0 1.48 ms，pi_0.5 1.66 ms，GR00T N1.6 3.98 ms，这反映了 GR00T N1.6 更短的动作时域。
- 最强的结论是系统层面的：当前 VLA 策略可以在低成本模块化机器人上完成微调和部署，用于现实中的脆弱物体抓取；在这个设置里，GR00T N1.6 的连续抓取可靠性最好。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02037v1](https://arxiv.org/abs/2605.02037v1)
