---
source: arxiv
url: http://arxiv.org/abs/2603.14327v1
published_at: '2026-03-15T11:13:04'
authors:
- Yixuan Li
- Le Ma
- Yutang Lin
- Yushi Du
- Mengya Liu
- Kaizhe Hu
- Jieming Cui
- Yixin Zhu
- Wei Liang
- Baoxiong Jia
- Siyuan Huang
topics:
- humanoid-teleoperation
- whole-body-control
- benchmarking
- vision-language-action
- sim2real
relevance_score: 0.87
run_id: materialize-outputs
---

# OmniClone: Engineering a Robust, All-Rounder Whole-Body Humanoid Teleoperation System

## Summary
OmniClone提出了一个面向类人机器人全身遥操作的工程化系统，并配套了细粒度诊断基准OmniBench。其目标是在低成本硬件和有限数据下，实现更稳健、更通用、可部署的全身运动跟踪与数据采集。

## Problem
- 现有类人全身遥操作系统通常只报告粗粒度汇总指标，掩盖了在下蹲、跳跃、低位操作等不同运动模式下的失败模式。
- 现有方案往往与特定硬件、操作者体型和通信设置强耦合，需要繁琐校准，难以稳定落地到真实场景。
- 这很重要，因为全身遥操作不仅用于实时远程控制，也是采集高质量示范数据、训练通用机器人/VLA策略的重要基础设施。

## Approach
- 作者先构建**OmniBench**：一个按6类技能（如manipulation、walking、running、jumping等）和18个分层难度/动态类别评测的诊断基准，专门测试未见动作上的泛化。
- 核心控制策略是一个**Transformer全身跟踪策略**，通过teacher-student蒸馏训练，让模型从历史本体感觉和参考动作序列中输出关节控制。
- 作者用OmniBench反向指导训练数据配方：最终采用约**60% manipulation + 40% dynamic maneuvers/stable locomotion**的平衡数据组成，以避免模型只擅长单一技能。
- 在系统层面加入**与操作者无关的retargeting**，通过动态尺度校正减少不同人体身材和MoCap系统带来的几何误差；文中指出未校正时最大偏差约**20 cm**，会带来约**20 mm MPJPE**增加。
- 为应对真实部署中的抖动和延迟，系统使用**基于队列的数据管理 + zero-order hold + UDP通信**，实现约**80 ms**端到端延迟；同一策略还支持实时遥操作、生成动作回放和VLA控制输入，属于control-source-agnostic设计。

## Results
- 论文宣称，相比可比方法，OmniClone通过数据配方和系统优化使**MPJPE降低超过66%**，同时所需计算资源少几个数量级；训练仅需约**30小时动作数据**、单张**RTX 4090**，总计约**80 GPU小时**（teacher约60小时，student约22小时）。
- 在OmniBench上，OmniClone在18个分层类别上整体优于GMT和Twist2。例如：**Loco-Manip Low**中MPJPE为**51.3 mm**，优于GMT的**180.5 mm**和Twist2的**210.5 mm**；**Manip Medium**中为**20.4 mm**，优于GMT的**54.7 mm**和Twist2的**156.3 mm**。
- 在动态运动上也显著更强：**Run Medium**中OmniClone达到**100% SR / 42.0 mm MPJPE**，对比GMT的**100% / 120.8 mm**、Twist2的**100% / 176.9 mm**；**Jump Medium**中为**100% / 34.5 mm**，对比GMT的**90% / 105.3 mm**、Twist2的**85% / 177.2 mm**。
- 在部分更困难场景中也保持高成功率，例如**Walk Fast**为**100% SR / 63.5 mm**，而OmniClone的MLP版本仅**20% SR / 111.7 mm**，说明Transformer骨干明显优于MLP。
- 真实系统可泛化到**1.47 m–1.94 m**的6名操作者，跨越**47 cm**身高差；文中称所有新手在**5–7次**练习内完成复合loco-manipulation任务。
- 作为示范数据引擎，基于OmniClone采集的数据训练出的VLA策略在真实任务上达到**85.71%**（Pick-and-Place）和**80.00%**（Squat to Pick-and-Place）成功率。

## Link
- [http://arxiv.org/abs/2603.14327v1](http://arxiv.org/abs/2603.14327v1)
