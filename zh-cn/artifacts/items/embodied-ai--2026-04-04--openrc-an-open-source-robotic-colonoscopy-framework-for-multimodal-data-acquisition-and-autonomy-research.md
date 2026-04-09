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
OpenRC 是一个开源机器人结肠镜平台，可在标准结肠镜上加装使用，并记录同步的视频、操作者动作、机器人状态和远端镜尖位姿。论文的主要贡献是将低成本硬件验证与一个多模态数据集结合起来，用于结肠镜闭环自主研究。

## 问题
- 结肠镜研究常把感知与控制分开：许多数据集只有视频，而机器人系统通常缺少可共享、同步的动作、驱动和镜尖运动日志。
- 这使结肠镜闭环机器人研究、考虑控制的感知研究，以及 vision-language-action 训练难以复现，因为这些工作都需要把观测、动作和状态对齐。
- 这个问题很重要，因为结肠镜检查是结直肠癌筛查的核心手段，但腺瘤漏检率最高可达 **34%**，操作者差异和设备局限仍会影响结果。

## 方法
- 作者为传统结肠镜构建了一个模块化机器人改装系统，提供 **3 个临床相关自由度（DoFs）**：插入/回撤，以及远端两条弯曲轴。
- 系统在统一的 ROS 2 栈上记录四种主要模态：结肠镜视频、操作者命令向量、电机/驱动状态，以及通过 **6-DoF EM 跟踪**得到的远端镜尖位姿。
- 他们用受控正弦激励验证时序和运动一致性，然后估计各模态的时间偏移，并以视频为参考，将所有数据流重采样到 **30 Hz**。
- 他们在两个结肠体模中采集遥操作数据，并将数据集存储为 **LeRobot 2.1** 格式，其中包含任务指令，以及导航、失败和恢复等 episode。

## 结果
- 除 EM 跟踪器外，整套系统可在 **5,000 美元以下**组装完成。
- 该数据集包含 **1,894 个 episode**，约 **19 小时**的遥操作结肠镜数据，覆盖 **10 种任务变化**。
- 数据集包含 **142 个失败 episode** 和 **141 个恢复 episode**，覆盖管腔丢失、接触肠壁和卡入皱襞等情况。
- 在时序表征中，相对于控制动作估计的偏移约为：电机编码器状态 **102 ms**、EM 跟踪 **435 ms**、基于光流推导的运动 **412 ms**。
- 对齐后，**操作者动作与驱动状态**之间的残余时滞中位数为 **55.6 ms**（在 30 Hz 下约 **1.6 帧**）。
- 对齐后，**驱动状态与远端镜尖位姿**之间的残余时滞以 **0.0 ms** 为中心。论文没有报告相对于某个自主基线的任务性能提升；它最明确的结论是，论文提供了一个开放、同步的平台和数据集，而此前的结肠镜资源没有把这两者结合起来。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03781v1](http://arxiv.org/abs/2604.03781v1)
