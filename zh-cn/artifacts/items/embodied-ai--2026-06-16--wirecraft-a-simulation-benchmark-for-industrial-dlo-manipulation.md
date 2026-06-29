---
source: arxiv
url: https://arxiv.org/abs/2606.18097v1
published_at: '2026-06-16T15:59:46'
authors:
- Chongyu Zhu
- Ramy ElMallah
- Hyegang Kim
- Zachary Tang
- Jiachen Rao
- Artem Arutyunov
- Seungyeon Ha
- Chi-Guhn Lee
topics:
- deformable-linear-objects
- robot-manipulation
- simulation-benchmark
- vision-language-action
- sim2real
- industrial-assembly
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# WireCraft: A Simulation Benchmark for Industrial DLO Manipulation

## Summary
## 摘要
WireCraft 是一个面向工业线缆操作任务的仿真基准，覆盖连接器插入、卡扣走线和槽道就位。它使用共享的任务定义、指标和数据格式，测试 RL、模仿学习和 VLA 策略。

## 问题
- 工业装配经常要求机器人对电线、电缆等可变形线性物体进行走线、就位和插入；这些物体会弯曲、相互遮挡，并在接触过程中改变形状。
- 现有 DLO 基准多关注通用形状控制或自由空间操作，许多工业线缆研究则依赖固定硬件、夹具和传感配置，复用难度高。
- 这个缺口会影响策略比较和 sim-to-real 研究，因为这些研究需要共同的任务、资产、数据 schema 和指标。

## 方法
- WireCraft 基于 Isaac Lab 2.2.1 和 Isaac Sim 4.5 构建，提供可配置的工业资产，包括连接器、端口、卡扣、槽道和可 3D 打印的任务板。
- 它支持两种线缆模型：用于更快生成 rollout 的铰接刚体链模型，以及用于更高保真弯曲和接触的 FEM 可变形体模型。
- 该基准覆盖三类任务：连接器插入、卡扣走线和槽道就位，并包含随机线缆初始化和任务特定随机化。
- 它提供来自脚本化仿真策略、RL rollout、仿真遥操作和真实 UR5 轨迹的演示数据，采用兼容 LeRobot 的 schema。
- 它在共享成功指标下评估 PPO、SACfD、Vision PPO、ACT、Diffusion Policy、Diffusion Transformer VLA 和 π0.5。

## 结果
- 在 3 mm 间隙的 Ethernet 连接器插入任务中，使用特权状态的 RL 达到较高插入成功率：State PPO 的插入成功率为 95.86±1.93%，SACfD 为 92.40±5.91%。
- Vision PPO 在同一 Ethernet 插入任务上表现差很多：到达成功率为 51.63±4.82%，插入成功率为 17.74±1.21%，显示出从到达到插入的大幅下降。
- 在不同连接器类型上，State PPO 的插入成功率都高于 92%：Cylinder 为 93.75±1.25%，Cuboid 为 95.00±3.75%，Ethernet 为 95.86±1.93%，DisplayPort 为 92.92±3.15%。
- Vision PPO 在更难的视觉对齐场景中性能下降：Cuboid 插入成功率为 6.25±3.31%，DisplayPort 插入成功率为 3.32±1.45%。
- 使用特权状态的 State PPO 也能在仿真中解决初始的非插入任务：1-clip routing 成功率为 95.32±0.93%，straight-channel seating 成功率为 82.33±0.31%。
- 在真实 UR5 Ethernet 插入实验中，ACT 在 40k-step checkpoint 下，纯仿真数据得到 0/10 次插入成功，真实数据+脚本化仿真数据得到 4/10 次插入成功；论文将其视为仍存在 sim-to-real 差距的证据，而非对数据混合方案的最终排序。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.18097v1](https://arxiv.org/abs/2606.18097v1)
