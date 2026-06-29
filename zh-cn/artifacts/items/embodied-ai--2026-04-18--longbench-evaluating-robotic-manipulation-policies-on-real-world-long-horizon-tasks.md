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
LongBench 是一个用于长时程机器人操作的真实世界基准，把两类难点分开看：在完全可观测条件下的长时间执行，以及在存在歧义时的长上下文推理。它在 1,000 多个真实世界 episode 上评估了六个当前策略，并表明长时程失败有多个原因，而不是单一瓶颈。

## 问题
- 现有的长时程操作基准往往只在仿真中运行，或者只报告整体成功率，所以看不出策略在真实世界长轨迹中为什么失败。
- 长时程任务把不同类型的难点混在一起：执行漂移、阶段切换错误、错过时机窗口，以及当前视角有歧义、需要更早上下文的情况。
- 这很重要，因为短时程指标或整体指标会掩盖机器人策略的真实弱点，这会让模型比较和长时程操作的进展评估不够可靠。

## 方法
- 论文提出了 **LongBench**，这是一个真实世界基准，包含 **10 个任务** 和 **1,000 多个真实世界 episode/demonstration**，数据采集在一个 **ARX-R5 6-DoF** 桌面平台上，使用 **两台 RGB 摄像头**，分辨率为 **320x240**，帧率为 **20 Hz**。
- 它把任务分成两种模式：**Context-Independent** 任务中，下一步动作可以从当前观测直接确定；**Context-Dependent** 任务中，外观相似的状态需要依赖更早的上下文记忆。
- 基准还按机制给任务打标签。Context-Independent 任务分为 **phase dependence (PD)**、**iterative progress (IP)**、**error accumulation (EA)** 和 **temporal windows (TW)**。Context-Dependent 任务分为 **completion ambiguity (CP)**、**count ambiguity (CT)**、**subtask-branch ambiguity (SB)** 和 **cross-episode ambiguity (CE)**。
- 评估使用 **stage-wise score**，而不是二元成功率：如果一个任务有 **N** 个原子子步骤，每完成一个子步骤就得 **100/N** 分。每个任务用 **10 个初始条件不同的 episode** 进行测试。
- 论文在统一接口下比较了 **六个策略**：**pi_0, OpenVLA-OFT, SmolVLA, Diffusion Policy, MemoryVLA, CronusVLA**，全部使用 **16-step open-loop action chunks**。

## 结果
- 在 **Context-Independent** 任务上，**pi_0** 表现最好，平均 **stage-wise score** 为 **86.3**，高于 **Diffusion Policy 51.2**、**MemoryVLA 49.1**、**SmolVLA 46.6**、**CronusVLA 42.4** 和 **OpenVLA-OFT 32.7**。
- **pi_0** 在各个 Context-Independent 任务上的分数分别是：*waste sorting* **100.0**、*thread rope* **72.0**、*pull drawer* **95.0**、*stack block* **91.3**、*dynamic grasping* **73.3**。
- 图中显示的完全可观测任务里，最难的是 **dynamic grasping**，这是一个 temporal-window 任务。**OpenVLA-OFT** 得分 **0.0**，**SmolVLA** 得分 **10.0**，**Diffusion Policy** 得分 **13.3**，**MemoryVLA** 得分 **10.0**，**CronusVLA** 得分 **13.3**，而 **pi_0** 达到 **73.3**。
- 论文指出，长时程表现不能用单一因素解释。在完全可观测设置下，执行鲁棒性对结果的影响大于显式记忆，而 **memory-based methods** 并不能在所有任务上稳定解决上下文难点。
- 这段摘要 **没有** 提供 **Context-Dependent** 任务的定量表格，所以这里没有该模式下的数值基准结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16788v1](http://arxiv.org/abs/2604.16788v1)
