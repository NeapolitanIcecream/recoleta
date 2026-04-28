---
source: arxiv
url: http://arxiv.org/abs/2604.16788v1
published_at: '2026-04-18T02:25:30'
authors:
- Xueyao Chen
- Jingkai Jia
- Tong Yang
- Yibo Fu
- Wei Li
- Wenqiang Zhang
topics:
- robot-benchmark
- long-horizon-manipulation
- real-world-evaluation
- vision-language-action
- context-dependent-reasoning
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks

## Summary
## 摘要
LongBench 是一个面向长时程机器人操作的真实世界基准，它将两类难点分开评估：完全可观测条件下的长程执行，以及存在歧义时依赖上下文的长程推理。该基准在 1,000 多个真实世界 episode 上评测了六种当前策略，并表明长时程失败有多种原因，而不是单一瓶颈。

## 问题
- 现有长时程操作基准常常只在仿真中评测，或只报告总体成功率，因此无法说明策略为何会在真实世界的长程 rollout 中失败。
- 长时程任务混合了不同来源的难度：执行漂移、阶段切换错误、错过时间窗口，以及当前视角存在歧义、必须依赖更早上下文的情况。
- 这很重要，因为短时程指标或总体指标可能掩盖机器人策略的真实弱点，从而让模型比较和长时程操作上的进展判断变得不可靠。

## 方法
- 论文提出了 **LongBench**，这是一个真实世界基准，包含 **10 个任务** 和 **1,000 多个真实世界 episodes/demonstrations**，数据采集于 **ARX-R5 6-DoF** 桌面平台，使用 **两个 RGB 摄像头**，分辨率为 **320x240**，频率为 **20 Hz**。
- 它将任务分为两种设定：**Context-Independent** 任务中，下一步动作可由当前观测直接确定；**Context-Dependent** 任务中，视觉上相似的状态需要依赖更早的上下文记忆。
- 该基准还按机制对任务进一步标注。Context-Independent 任务分为 **phase dependence (PD)**、**iterative progress (IP)**、**error accumulation (EA)** 和 **temporal windows (TW)**。Context-Dependent 任务分为 **completion ambiguity (CP)**、**count ambiguity (CT)**、**subtask-branch ambiguity (SB)** 和 **cross-episode ambiguity (CE)**。
- 评测使用 **分阶段得分**，而不是二元成功率：如果一个任务有 **N** 个原子子步骤，每完成一个子步骤就得到 **100/N** 分。每个任务都在 **10 个 episode** 上测试，并使用不同的初始设置。
- 该基准在统一接口下比较了 **六种策略**：**pi_0、OpenVLA-OFT、SmolVLA、Diffusion Policy、MemoryVLA 和 CronusVLA**，全部使用 **16-step open-loop action chunks**。

## 结果
- 在 **Context-Independent** 任务上，**pi_0** 表现最好，平均分阶段得分为 **86.3**，高于 **Diffusion Policy 51.2**、**MemoryVLA 49.1**、**SmolVLA 46.6**、**CronusVLA 42.4** 和 **OpenVLA-OFT 32.7**。
- **pi_0** 在各个 Context-Independent 任务上的得分分别为：*waste sorting* **100.0**、*thread rope* **72.0**、*pull drawer* **95.0**、*stack block* **91.3**、*dynamic grasping* **73.3**。
- 已展示结果中最难的完全可观测任务是 **dynamic grasping**，它属于 temporal-window 任务。**OpenVLA-OFT** 降到 **0.0**，**SmolVLA** 为 **10.0**，**Diffusion Policy** 为 **13.3**，**MemoryVLA** 为 **10.0**，**CronusVLA** 为 **13.3**，而 **pi_0** 达到 **73.3**。
- 论文认为，长时程表现不能用单一因素解释。在完全可观测设定下，结果更多取决于执行稳健性，而不是显式记忆；并且 **基于记忆的方法并不能在各类任务中稳定解决上下文难题**。
- 该摘录 **没有** 给出 **Context-Dependent** 任务得分的定量表格，因此这里无法提供该设定下的数值基准结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16788v1](http://arxiv.org/abs/2604.16788v1)
