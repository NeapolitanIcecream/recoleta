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
- robot-manipulation
- task-and-motion-planning
- vision-language-planning
- open-vocabulary
- modular-robotics
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# TiPToP: A Modular Open-Vocabulary Planning System for Robotic Manipulation

## Summary
TiPToP 是一个面向机器人操作的模块化开放词汇规划系统：输入RGB图像和自然语言，输出多步操作轨迹。它把预训练视觉基础模型与GPU加速任务-运动规划结合起来，在**零机器人训练数据**下完成真实与仿真桌面操作，并在多类任务上达到或超过经过 350 小时特定机体演示微调的 VLA 基线。

## Problem
- 目标是让机器人能够**开箱即用**地根据自然语言和相机图像，对**任意对象**执行多步操作，而不依赖对象、环境或机体专门调参。
- 现有 VLA 模型虽然接口简洁，但通常需要大量机器人数据，且跨机体泛化与失败可解释性不足；传统 TAMP 又常常与特定硬件/感知栈深度耦合，难以复用。
- 这很重要，因为真正可部署的通用操作系统需要同时具备**开放词汇理解、几何可行性、多步推理、低数据成本和易部署性**。

## Approach
- 用一次初始观测（立体 RGB）和语言指令构建场景：深度模型生成稠密深度，抓取模型给出 6-DoF 候选抓取，VLM 检测并命名物体、把语言目标转成符号目标，SAM-2 做分割，再合成为以物体为中心的 3D 场景表示。
- 规划端使用 GPU 并行的 cuTAMP：先枚举符号计划骨架，再对抓取位姿、放置位姿、关节构型等连续变量进行并行优化，并调用 cuRobo 生成无碰撞轨迹。
- 执行端使用关节阻抗控制器跟踪规划出的整段轨迹；系统是**开环执行**，不依赖执行中视觉反馈。
- 核心机制可以最简单地理解为：**先用基础模型“看懂场景和任务”，再用经典规划器“算出一串可行的抓取/放置动作”**，而不是直接让大模型端到端输出动作。
- 模块化设计使其容易替换组件、定位失败来源，并宣称可在支持的平台上**1 小时内安装部署**，只需相机标定，并可较容易迁移到新机体。

## Results
- 在 **28 个桌面操作任务/场景、共 165 次试验** 上，TiPToP 总体成功率 **98/165 = 59.4%**，而 \(\pi_{0.5}\)-DROID 为 **55/165 = 33.3%**；平均任务进度（Task Progress）分别为 **74.6% vs 52.4%**。
- 与基线对比：基线是 **\(\pi_{0.5}\)-DROID**，其经过 **350 小时机体特定演示数据**微调；而 TiPToP 使用 **零机器人数据**。
- 分类别结果：**Simple** 任务上二者接近，TiPToP 的任务进度 **84.0% vs 79.5%**，但成功率 **22/40 vs 27/40** 略低；**Distractor** 上 TiPToP **27/45 (60.0%) vs 12/45 (26.7%)**，任务进度 **71.6% vs 41.1%**。
- **Semantic** 任务上 TiPToP **26/40 (65.0%) vs 10/40 (25.0%)**，任务进度 **71.3% vs 46.8%**；文中称 TiPToP 在 8 个语义场景中的 **7 个** 上成功率更高，而基线有 **4 个场景为 0/5**。
- **Multi-step** 任务上 TiPToP **23/40 (57.5%) vs 6/40 (15.0%)**，任务进度 **75.2% vs 52.2%**；例如 “Color cubes -> bowl (sim)” 为 **9/10 vs 0/10**，“Three marbles -> cup” 为 **2/5 vs 0/5**。
- 论文还声称系统在 **仿真与真实世界** 上评测，总计分析了 **173 次试验** 的失败模式，并展示了在 **DROID、UR5e、Trossen WidowX AI** 等机体上的部署可行性；不过给定摘录中未提供更细的按模块失败率数字。

## Link
- [http://arxiv.org/abs/2603.09971v1](http://arxiv.org/abs/2603.09971v1)
