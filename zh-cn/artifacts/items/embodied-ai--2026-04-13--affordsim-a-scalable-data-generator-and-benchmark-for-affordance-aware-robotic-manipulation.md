---
source: arxiv
url: http://arxiv.org/abs/2604.11674v1
published_at: '2026-04-13T16:21:44'
authors:
- Mingyang Li
- Haofan Xu
- Haowen Sun
- Xinzhe Chen
- Sihua Ren
- Liqi Huang
- Xinyang Sui
- Chenyang Miao
- Qiongjie Cui
- Zeyang Liu
- Xingyu Chen
- Xuguang Lan
topics:
- robot-simulation
- affordance-learning
- vision-language-robotics
- sim2real
- imitation-learning
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# AffordSim: A Scalable Data Generator and Benchmark for Affordance-Aware Robotic Manipulation

## Summary
## 摘要
AffordSim 是一个面向机器人操作的仿真系统和基准，它使用 3D 可供性预测来大规模生成任务正确的轨迹。论文表明，当前的模仿学习策略在简单抓取上表现较好，但在机器人必须作用于物体特定功能区域的任务上仍然吃力。

## 问题
- 现有的机器人操作仿真数据生成器在选择抓取和动作时不使用物体可供性，因此常会生成物理上可行但任务上错误的轨迹。
- 这会影响诸如从杯沿倒水、抓住马克杯把手、或把马克杯挂到钩子上这类任务，因为任务是否成功取决于是否接触到物体的正确部位。
- 手动设计抓取方式无法扩展，而 AnyGrasp 这类通用抓取方法忽略任务语义。

## 方法
- AffordSim 接收自然语言任务，使用 VLM 在 NVIDIA Isaac Sim 中构建场景，采集物体点云，用 VoxAfford 预测 3D 可供性图，然后基于这些图规划抓取和动作。
- VoxAfford 是一个开放词汇 3D 可供性检测器：给定诸如“可抓取的把手”或“可倾倒的杯沿”这样的查询，它会为物体上的点打分，表示这些点对该交互有多合适。
- 抓取选择器会在高可供性区域周围采样候选抓取，并按两个因素为每个候选抓取打分：它与高可供性点的接触程度，以及机器人能否在不碰撞的情况下到达该位置。
- 系统支持四种机械臂：Franka FR3、Franka Panda、UR5e 和 Kinova。
- 为了实现 sim-to-real 迁移，AffordSim 加入了五类域随机化，其中包括基于 DA3 的 3D Gaussian 背景重建，使用 10-20 张真实照片生成。

## 结果
- 基准：涵盖 7 个类别的 50 个任务，使用 4 个模仿学习基线，并为每个任务训练 300 条演示数据。在 17 个代表性任务上，平均成功率分别为 BC 16%、ACT 35%、Diffusion Policy 44%、Pi 0.5 61%。
- 简单抓取比高度依赖可供性的任务容易得多：抓取任务成功率达到 53-93%，而向窄口杯中倒水为 1-43%，挂杯为 0-47%，长时序任务为 0-21%，具体取决于方法。
- 示例任务结果：`pick_banana` 对 BC/ACT/DP/Pi 0.5 的得分为 53/63/87/93%；`pour_cup_into_bowl` 为 1/24/36/43%；`hang_mug_on_rack` 为 0/10/17/47%。
- 轨迹生成中的可供性消融：手动抓取设计平均为 87%，AnyGrasp 为 20%，VoxAfford 为 61%，人工可供性标注为 92%。在 `pour_into_cup` 上，AnyGrasp 为 0%，VoxAfford 为 63%；在 `pour_into_pan` 上，AnyGrasp 为 20%，VoxAfford 为 80%。
- 跨本体轨迹生成成功率为：Franka FR3 94%，Panda 92%，UR5e 83%，Kinova 95%。
- 在真实 Franka FR3 上进行的零样本 sim-to-real 实验中，Pi 0.5 在抓取上达到 60%，放置 30%，堆叠 20%，推/拉 40%，倒水 20%，挂杯 10%，平均为 30%。论文还报告，VoxAfford 本身将开放词汇 3D 可供性检测的表现比现有方法提高了约 8 个 mIoU。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11674v1](http://arxiv.org/abs/2604.11674v1)
