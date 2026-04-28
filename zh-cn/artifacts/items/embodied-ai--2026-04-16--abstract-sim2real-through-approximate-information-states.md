---
source: arxiv
url: http://arxiv.org/abs/2604.15289v1
published_at: '2026-04-16T17:53:16'
authors:
- Yunfu Deng
- Yuhao Li
- Josiah P. Hanna
topics:
- sim2real
- state-abstraction
- reinforcement-learning
- robotics
- history-based-modeling
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Abstract Sim2Real through Approximate Information States

## Summary
## 摘要
本文研究这样一种 sim2real 迁移场景：模拟器使用比真实机器人更粗粒度的状态表示，因此缺少关键动力学信息。论文将这一设定形式化为一个状态抽象问题，并提出了 ASTRA，这是一种基于历史信息的模拟器校准方法，只需少量真实世界数据进行训练。

## 问题
- 论文关注 **abstract sim2real**：在一个简化模拟器中训练 RL 策略，这个模拟器的状态省略了真实世界中的部分细节，然后再把该策略迁移到真实机器人上。
- 这一问题很重要，因为在大规模、复杂环境中，构建高保真机器人模拟器成本高或并不现实，而抽象模拟器速度更快，也更容易构建。
- 主要技术问题是，抽象会带来 **部分可观测性**。两个不同的真实状态可能映射到同一个抽象状态，因此那些假设状态空间一致、或只处理参数不匹配的标准 sim2real 方法可能会失效。

## 方法
- 论文用 RL 中的 **状态抽象** 形式化 abstract sim2real。核心观点是，要让抽象模拟器与目标任务对齐，必须使用 **状态-动作历史**，因为仅靠抽象状态本身通常不满足马尔可夫性。
- 论文提出 **ASTRA**（Augmented Simulation with self-predicTive abstRAction），它从经过抽象的真实世界历史中学习一个循环潜在状态。
- ASTRA 在成对的模拟器/真实数据上用三种损失来训练这个潜在状态：用于预测下一个潜在状态的 **潜在状态转移损失**，用于保留任务相关信息的 **奖励预测损失**，以及用于把模拟器的下一状态预测修正到真实抽象下一状态附近的 **抽象下一状态校正损失**。
- 校准后的模拟器随后使用修正后的抽象状态和学到的潜在动力学向前滚动，并在这个校准模拟器上训练 RL 策略。部署时，目标侧编码器会把真实世界历史映射到同一个潜在空间。

## 结果
- 论文称，在 **sim2sim** 和 **sim2real** 两种设定下，当直接迁移和若干基线方法失败时，ASTRA 都能实现成功迁移。
- 在 **AntMaze sim2sim navigation** 中，ASTRA 在 **U-Maze** 和 **Long Maze** 上都取得了对比方法中 **最高的成功率**，对比方法包括 Direct Transfer、Domain Randomization、COMPASS、RMA、NAS 和 DT+IQL。摘录没有给出 Figure 3 中的具体成功率数值。
- 在修改版 Ant、**腿长为 1.25×** 的 **形态变化测试** 中，在标准 Ant 上训练的 ASTRA 策略在 **U-Maze** 上达到 **65% success**，而直接迁移为 **21%**。
- 在 AntMaze 的校准数据设置中，ASTRA 和 NAS 都使用了 **200 条轨迹**，平均长度为 **500 步**，由随机行为策略采集。
- 该设定下，抽象模拟器与目标环境之间的差距很大：目标 AntMaze 状态有 **29 维**，而抽象模拟器只使用 **位置和速度**。
- 摘录还提到，ASTRA 也适用于 **真实 NAO humanoid 任务** 和模拟 humanoid locomotion，但提供的文本没有包含这些实验的最终定量结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15289v1](http://arxiv.org/abs/2604.15289v1)
