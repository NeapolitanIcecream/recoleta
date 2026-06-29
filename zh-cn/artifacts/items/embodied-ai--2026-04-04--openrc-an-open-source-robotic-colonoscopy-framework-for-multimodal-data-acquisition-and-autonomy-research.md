---
source: arxiv
url: http://arxiv.org/abs/2604.03781v1
published_at: '2026-04-04T16:07:33'
authors:
- Siddhartha Kapuria
- Mohammad Rafiee Javazm
- Naruhiko Ikoma
- Joga Ivatury
- Mohammad Ali Nasseri
- Nassir Navab
- Farshid Alambeigi
topics:
- robot-data-collection
- medical-robotics
- vision-language-action
- surgical-autonomy
- multimodal-dataset
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# OpenRC: An Open-Source Robotic Colonoscopy Framework for Multimodal Data Acquisition and Autonomy Research

## Summary
## 摘要
OpenRC 是一个开源机器人结肠镜平台，可改装标准内镜，并记录同步的视频、操作者动作、机器人状态和远端尖端位姿。论文的主要贡献是把低成本硬件验证和一个用于结肠镜闭环自主研究的多模态数据集结合起来。

## 问题
- 结肠镜研究常把感知和控制分开：很多数据集只有视频，而机器人系统往往没有共享的、同步的日志来记录动作、执行状态和尖端运动。
- 这阻碍了可复现的闭环机器人结肠镜研究、感知与控制联合研究，以及 vision-language-action 训练，因为观测、动作和状态必须对齐。
- 这个问题很重要，因为结肠镜是结直肠癌筛查的核心手段，但腺瘤漏检率仍可高达 **34%**，操作者差异和设备限制也会影响结果。

## 方法
- 作者为传统结肠镜构建了一个模块化机器人改装方案，包含 **3 个与临床相关的自由度**：插入/回撤，以及两个远端弯曲轴。
- 该系统在共享的 ROS 2 栈上记录四种主要模态：结肠镜视频、操作者指令向量、电机/执行状态，以及 **6 自由度 EM 跟踪**的远端尖端位姿。
- 他们用受控正弦激励验证了时序和运动一致性，然后估计各模态偏移，并以视频为参考把所有流重采样到 **30 Hz**。
- 他们在两个结肠仿体中采集了遥操作数据，并将数据集存成 **LeRobot 2.1** 格式，包括任务指令，以及用于导航、故障和恢复的 episodes。

## 结果
- 除去 EM 跟踪器后，整套框架的组装成本可控制在 **5,000 美元以下**。
- 数据集包含 **1,894 个 episodes**，约 **19 小时**的遥操作结肠镜数据，覆盖 **10 种任务变体**。
- 数据集包含 **142 个故障 episodes** 和 **141 个恢复 episodes**，涵盖管腔丢失、壁面接触和皱襞卡住等情况。
- 在时序表征中，相对于控制动作估计的偏移约为电机编码器状态 **102 ms**、EM 跟踪 **435 ms**、以及由光流推导的运动 **412 ms**。
- 对齐后，操作者动作与执行状态之间的中位残余滞后为 **55.6 ms**，约等于 **30 Hz 下的 1.6 帧**。
- 对齐后，执行状态与远端尖端位姿之间的残余滞后中心为 **0.0 ms**。论文没有报告相对于自主基线的任务性能提升；它最明确的结论是，OpenRC 提供了一个开放、同步的平台和数据集，而以往的结肠镜资源没有把这些内容结合起来。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03781v1](http://arxiv.org/abs/2604.03781v1)
