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
## 总结
POMDAR 是一个新的基准，用于按拟人机器人手完成一组抓取和手内操作任务的质量与速度来衡量灵巧性。它用基于分类学的基准取代了临时性的手部评估，并可在真实环境和 MuJoCo 中运行。

## 问题
- 拟人机器人手的灵巧性没有共享的、基于性能的定义，所以论文常常用不同任务和不同指标来比较不同的手。
- 常见的代理指标，比如自由度、关节极限或可操作性，衡量的是潜在能力，不是接触丰富的操作表现。
- 没有标准基准时，就很难比较手的设计、跟踪设计进展，或把某种手匹配到目标使用场景。

## 方法
- 论文提出 **POMDAR**，一个基于已建立的人手分类学构建的基准：来自 Elliott 和 Connolly 以及 Ma 和 Dollar 的 14 种操作模式，和来自 GRASP 分类学的 33 种抓取类型。
- 这些分类学被转成一组紧凑任务，包括 **12 个操作任务** 和 **6 个纯抓取任务**，并组织成四种配置：垂直支架任务、水平支架任务、连续旋转任务和自由空间抓取任务。
- 机械支架限制运动，使基准测量预期的手部行为，并减少诸如掌心支撑、重力辅助或过多手臂运动之类的补偿策略。
- 评分结合任务完成质量和速度：**Score = 0.8 × correctness + 0.2 × speed**，其中速度按用户研究中的人类基线时间归一化。操作任务的正确性是连续值，抓取任务的正确性是离散值。
- 这个基准是开源的、可完全 3D 打印的，并在 **MuJoCo** 中实现，支持遥操作，因此用户可以在同一套任务逻辑下测试实体手和仿真手。

## 结果
- 这个基准总共包含 **18 个任务**：**12 个操作任务** 和 **6 个抓取任务**。
- 人类基线来自 **6 名参与者**，每人对每个任务执行 **3 次试验**，每个任务共得到 **18 条轨迹**。动作捕捉使用了 **22 个手部关键点，频率为 100 Hz**。
- 机器人评估使用了 **4 种 ORCA 手的形态**：**2 指、5 自由度** 版本、**3 指** 版本、**5 指无外展** 版本，以及 **完整 5 指、16 自由度** 版本，全部安装在一台 **7 自由度 Franka Emika 机械臂** 上。
- 每个机器人任务在每种形态上重复 **20 次**。摘要说明这些实验展示了不同形态之间的基准比较，但可用文本 **没有给出每个任务或整体的具体数值分数**。
- 用户研究报告显示参与者之间的策略差异较小，PCA 图显示手部轨迹按任务聚类。论文把这作为证据，说明这些带支架的任务直观，并且把用户限制在预期的操作模式上。
- 核心具体主张是，POMDAR 让拟人机器人手可以在仿真和真实硬件上进行客观、可复现、以吞吐量为基础的比较；摘录中没有给出比前序基准更强的定量提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09294v1](http://arxiv.org/abs/2604.09294v1)
