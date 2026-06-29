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
AffordSim 是一个用于机器人操作的仿真系统和基准测试，它用 3D 可供性预测来大规模生成任务正确的轨迹。论文表明，当前的模仿学习策略在简单抓取上表现不错，但在机器人必须作用于物体特定功能区域的任务上仍然吃力。

## 问题
- 现有的机器人操作仿真数据生成器在选择抓取和运动时不会使用物体可供性，因此常常生成物理上可行、但任务上错误的轨迹。
- 这会影响从杯沿倒水、抓住杯柄、把马克杯挂到挂钩上这类任务，因为成功取决于是否接触到物体的正确部位。
- 手工设计抓取方式无法扩展，而 AnyGrasp 这类通用抓取方法会忽略任务语义。

## 方法
- AffordSim 接收自然语言任务，用 VLM 在 NVIDIA Isaac Sim 中搭建场景，采集物体点云，再用 VoxAfford 预测 3D 可供性图，最后根据这些图规划抓取和运动。
- VoxAfford 是一个开放词汇的 3D 可供性检测器：给定“可抓握的把手”或“可倾倒的杯沿”这类查询，它会为物体上的点打分，表示这些位置适合该交互的程度。
- 抓取选择器会在高可供性区域周围采样候选抓取，并按两个因素给每个候选抓取打分：它与高可供性点的接触程度，以及机器人是否能在不碰撞的情况下到达该位置。
- 该系统支持四种机械臂：Franka FR3、Franka Panda、UR5e 和 Kinova。
- 为了做仿真到现实迁移，AffordSim 加入了五类域随机化，其中包括基于 DA3 的 3D 高斯背景重建，重建素材来自 10 到 20 张真实照片。

## 结果
- 基准测试包含 7 个类别、50 个任务，并在每个任务上用 300 条示范训练了 4 个模仿学习基线。在 17 个代表性任务上，平均成功率分别是 BC 16%、ACT 35%、Diffusion Policy 44%、Pi 0.5 61%。
- 简单抓取比依赖可供性的任务容易得多：抓取达到 53% 到 93% 的成功率，而向窄杯中倒水为 1% 到 43%，挂马克杯为 0% 到 47%，长时程任务为 0% 到 21%，具体取决于方法。
- 示例任务结果：`pick_banana` 在 BC/ACT/DP/Pi 0.5 上分别是 53/63/87/93%；`pour_cup_into_bowl` 是 1/24/36/43%；`hang_mug_on_rack` 是 0/10/17/47%。
- 轨迹生成中的可供性消融结果：手工抓取设计平均 87%，AnyGrasp 20%，VoxAfford 61%，人工可供性标签 92%。在 `pour_into_cup` 上，AnyGrasp 是 0%，VoxAfford 是 63%；在 `pour_into_pan` 上，AnyGrasp 是 20%，VoxAfford 是 80%。
- 跨本体轨迹生成成功率在 Franka FR3 上为 94%，Panda 为 92%，UR5e 为 83%，Kinova 为 95%。
- 在真实 Franka FR3 上做零样本仿真到现实测试时，Pi 0.5 在抓取上达到 60%，放置 30%，堆叠 20%，推/拉 40%，倒水 20%，挂杯 10%，平均为 30%。论文还报告，VoxAfford 本身把开放词汇 3D 可供性检测的 mIoU 比先前方法提高了约 8 个点。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11674v1](http://arxiv.org/abs/2604.11674v1)
