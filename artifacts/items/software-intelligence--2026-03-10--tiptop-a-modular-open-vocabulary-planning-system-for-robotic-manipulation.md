---
source: arxiv
url: http://arxiv.org/abs/2603.09971v1
published_at: '2026-03-10T17:59:00'
authors:
- William Shen
- Nishanth Kumar
- Sahit Chintalapudi
- Jie Wang
- Christopher Watson
- Edward Hu
- Jing Cao
- Dinesh Jayaraman
- Leslie Pack Kaelbling
- "Tom\xE1s Lozano-P\xE9rez"
topics:
- robotic-manipulation
- task-and-motion-planning
- vision-language-models
- open-vocabulary
- modular-robotics
relevance_score: 0.19
run_id: materialize-outputs
---

# TiPToP: A Modular Open-Vocabulary Planning System for Robotic Manipulation

## Summary
TiPToP 是一个面向机器人操作的模块化开放词汇规划系统：输入一次性 RGB 图像和自然语言指令，输出完整操作轨迹。它把预训练视觉/语言基础模型与 GPU 加速的任务与运动规划结合起来，在零机器人训练数据下完成多步抓取与摆放任务。

## Problem
- 论文要解决的是：如何让机器人**开箱即用**地根据自然语言和相机图像完成多步操作，而不依赖大量特定机器人示教数据或为每个硬件/场景单独调参。
- 这很重要，因为端到端 VLA 虽然强大，但通常需要大量训练数据、跨硬件泛化不稳定、失败原因也难以诊断；传统 TAMP 又往往依赖手工建模、系统耦合重、难部署。
- 目标是在真实世界未知物体、干扰物、语义歧义和多步约束下，仍能生成可执行的操作计划。

## Approach
- 系统分成三部分：**感知、规划、执行**。先从一次立体 RGB 观测和文本指令出发，构建对象级 3D 场景表示，再生成完整操作轨迹并开环执行。
- 感知模块组合多个预训练模型：FoundationStereo 做深度估计，M2T2 预测 6-DoF 抓取，Gemini Robotics-ER 做开放词汇目标检测与语言目标落地，SAM-2 做分割，最后重建每个物体的近似 3D 网格并把抓取候选分配给对应物体。
- 规划模块使用 **cuTAMP**：先根据符号目标枚举动作骨架，再对抓取位姿、放置位姿、逆解和轨迹进行并行采样与可微优化；必要时会自动插入“先移开障碍物再抓取目标”的中间步骤。
- 执行模块用关节阻抗控制器跟踪规划出的定时轨迹。系统是**开环视觉执行**：规划时只看一次图像，执行中不再根据新视觉重规划。
- 设计上强调模块化与可替换性：新感知模型可独立替换，失败也能定位到具体模块，且作者声称在支持的机器人上仅需相机标定即可在 1 小时内完成部署。

## Results
- 在 **28 个桌面操作任务、165 次评测试验**中，TiPToP 总体成功率为 **98/165 = 59.4%**，而对比的 **π0.5-DROID** 为 **55/165 = 33.3%**；平均任务进度分别为 **74.6% vs 52.4%**。论文同时强调 TiPToP **无需机器人数据训练**，而对手经过 **350 小时**特定硬件示教微调。
- 在**简单任务**上两者接近：TiPToP **22/40 = 55.0%**，π0.5-DROID **27/40 = 67.5%**；但任务进度 TiPToP 略高，**84.0% vs 79.5%**。
- 在**干扰物任务**上，TiPToP 明显更强：**27/45 = 60.0%**，对比 **12/45 = 26.7%**；任务进度 **71.6% vs 41.1%**。例如 *PB crackers → tray (hard)* 上 TiPToP **5/5**，对手 **0/5**。
- 在**语义任务**上，TiPToP 为 **26/40 = 65.0%**，对比 **10/40 = 25.0%**；任务进度 **71.3% vs 46.8%**。如 *sort blocks by color* 上 TiPToP **5/5, 100% TP**，对手 **0/5, 32% TP**。
- 在**多步任务**上，TiPToP 为 **23/40 = 57.5%**，对比 **6/40 = 15.0%**；任务进度 **75.2% vs 52.2%**。如 *color cubes → bowl (sim)* 上 TiPToP **9/10**，对手 **0/10**。
- 最强的定性主张是：TiPToP 在零训练数据、模块可解释、快速部署的前提下，能够达到或超过强 VLA 基线；同时其失败可按感知/规划/执行模块拆解分析，但文中也明确其开环执行在物体滑动、意外移动和轨迹误差下会失败。

## Link
- [http://arxiv.org/abs/2603.09971v1](http://arxiv.org/abs/2603.09971v1)
