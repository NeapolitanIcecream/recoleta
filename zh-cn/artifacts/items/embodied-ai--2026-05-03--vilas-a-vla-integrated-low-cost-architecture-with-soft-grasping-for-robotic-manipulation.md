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
VILAS 是一个 8,000 美元的机器人操作平台，用于在易碎物体抓取任务上微调和部署 VLA 策略。它结合了工业协作机械臂、双 RGB-D 相机、遥操作数据采集，以及剪纸结构软夹爪扩展件。

## 问题
- 葡萄等易碎物体可能被刚性夹爪或突然的机器人运动压坏，因此操作需要轻柔接触和稳定抓取。
- 许多 VLA 机器人系统依赖昂贵的集成硬件；论文将约 8,000 美元的 VILAS 与约 33,000 美元的 ALOHA 套件进行了比较。
- 力传感器、触觉阵列和力控制系统会增加成本和集成工作量，从而限制 VLA 策略研究的可及性。

## 方法
- 该平台使用 Fairino FR5 机械臂、Jodell RG52-50 夹爪、GELLO 遥操作机械臂、RealSense D455 底座相机、RealSense D405 腕部相机，以及基于 ZMQ 的控制栈。
- 人类操作员使用 GELLO 采集演示。每个时间步存储一个 7-DoF 关节状态、两个 RGB 相机视角和一个语言提示。
- PEBA 剪纸结构扩展件安装在平行夹爪上，并在受压时弯曲，把接触分散到果实表面，降低对力传感的需求。
- 作者从公开检查点微调 pi_0、pi_0.5 和 GR00T N1.6，并使用同一数据集：100 个 episode，每个 episode 1,200 帧，在一块 NVIDIA H200 上训练 50,000 次迭代。
- 部署期间，机器人以 20 Hz 运行。pi_0 和 pi_0.5 输出 50 个动作的块，GR00T N1.6 输出 16 个动作的块。

## 结果
- 硬件总成本约为 8,000 美元，而 ALOHA 约为 33,000 美元。
- 在葡萄任务中，每个模型测试了 50 次。单次抓取成功率为：pi_0 70%，pi_0.5 84%，GR00T N1.6 82%。
- 多次抓取成功率定义为至少连续两次抓取成功，结果为：pi_0 22%，pi_0.5 36%，GR00T N1.6 58%。
- 平均推理延迟为：pi_0 73.8 ms，pi_0.5 82.8 ms，GR00T N1.6 63.6 ms。
- 单步推理成本为：pi_0 1.48 ms，pi_0.5 1.66 ms，GR00T N1.6 3.98 ms，这与 GR00T N1.6 更短的动作时域有关。
- 最有力的结论在系统层面：当前 VLA 策略可以在成本更低的模块化机器人上微调并部署，用于真实环境中的精细抓取；在该设置中，GR00T N1.6 的连续抓取可靠性最高。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02037v1](https://arxiv.org/abs/2605.02037v1)
