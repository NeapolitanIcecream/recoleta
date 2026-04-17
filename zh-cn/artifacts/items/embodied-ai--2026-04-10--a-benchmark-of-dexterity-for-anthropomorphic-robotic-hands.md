---
source: arxiv
url: http://arxiv.org/abs/2604.09294v1
published_at: '2026-04-10T13:04:28'
authors:
- Davide Liconti
- Yuning Zhou
- Yasunori Toshimitsu
- Ronan Hinchet
- Robert K. Katzschmann
topics:
- dexterous-manipulation
- robot-hand-benchmark
- anthropomorphic-hands
- in-hand-manipulation
- grasp-evaluation
- mujoco
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# A Benchmark of Dexterity for Anthropomorphic Robotic Hands

## Summary
## 摘要
POMDAR 是一个新的基准，用抓取和手内操作任务的完成质量与完成速度来衡量拟人机器人手的灵巧性。它用一个基于分类体系的基准替代了临时性的手部评测，并且可在现实环境和 MuJoCo 中运行。

## 问题
- 拟人机器人手的灵巧性缺少统一的、基于任务表现的定义，因此论文常用不同任务和不同指标来比较不同的手。
- 常见的代理指标，如自由度、关节限位或可操作性，反映的是潜在能力，而不是真实的富接触操作表现。
- 没有标准基准时，很难比较不同手部设计、跟踪设计进展，或让手部设计匹配目标应用场景。

## 方法
- 论文提出了 **POMDAR**，这是一个基于已有人手分类体系构建的基准：包括来自 Elliott 和 Connolly 以及 Ma 和 Dollar 的 14 种操作模式，以及 GRASP 分类体系中的 33 种抓握类型。
- 这些分类体系被转换为一个紧凑的任务集合，包含 **12 个操作任务** 和 **6 个纯抓取任务**，分为四种配置：垂直带支架任务、水平带支架任务、连续旋转任务，以及自由空间抓取任务。
- 机械支架会约束运动，因此基准测量的是预期的手部行为，并减少手掌支撑、重力辅助或手臂过度运动等补偿策略。
- 评分结合任务完成质量和速度：**Score = 0.8 × correctness + 0.2 × speed**，其中速度用用户研究得到的人类基线时间做归一化。操作任务的正确性是连续值，抓取任务的正确性是离散值。
- 该基准是开源的、可完整 3D 打印的，并在 **MuJoCo** 中实现且支持遥操作，因此用户可以在相同任务逻辑下测试实体手和仿真手。

## 结果
- 该基准总共包含 **18 个任务**：**12 个操作任务** 和 **6 个抓取任务**。
- 人类基线数据来自 **6 名参与者**，每人对每个任务执行 **3 次试验**，因此每个任务有 **18 条轨迹**。动作捕捉使用 **22 个手部关键点，采样频率为 100 Hz**。
- 机器人评测使用了 **4 种 ORCA 手部实现**：**2 指、5-DoF** 版本、**3 指** 版本、**无外展的 5 指** 版本，以及**完整的 5 指、16-DoF** 版本，全部安装在 **7-DoF Franka Emika 机械臂**上。
- 每个机器人任务在每种实现上都重复 **20 次**。摘录说明这些实验展示了不同实现之间的基准比较，但在可用文本中**没有给出实际的分任务或总体数值分数**。
- 用户研究报告参与者之间的策略差异较小，PCA 图显示手部轨迹按任务聚类。论文据此认为，这些带支架的任务容易理解，并且能将用户约束到预期的操作模式上。
- 主要的明确结论是，POMDAR 可以在仿真和真实硬件中，对拟人机器人手进行客观、可复现、基于吞吐量的比较；摘录中没有提供相较既有基准更强的定量优势。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09294v1](http://arxiv.org/abs/2604.09294v1)
