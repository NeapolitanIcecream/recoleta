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
本文研究的是一种 sim2real 迁移场景：模拟器使用的状态比真实机器人更粗粒度，因此缺少关键动力学信息。论文把这个问题形式化为状态抽象问题，并提出 ASTRA，一种基于历史信息的模拟器对齐方法，只需要少量真实世界数据来训练。

## 问题
- 论文关注的是 **abstract sim2real**：先在一个简化模拟器里训练 RL 策略，这个模拟器的状态省略了真实世界细节，然后把策略迁移到真实机器人上。
- 这个问题重要，因为在大型、复杂领域里，高保真机器人模拟器成本高，或者根本不现实；抽象模拟器更快，也更容易搭建。
- 主要技术难点在于抽象会带来 **部分可观测性**。两个不同的真实状态可能映射到同一个抽象状态，所以假设状态空间匹配、或者只存在参数偏差的常规 sim2real 方法可能会失效。

## 方法
- 论文用 RL 里的 **state abstraction** 来形式化 abstract sim2real。核心观点是，要让抽象模拟器对齐到目标任务，必须使用 **state-action history**，因为单独的抽象状态通常不是马尔可夫的。
- 论文提出 **ASTRA**（Augmented Simulation with self-predicTive abstRAction），它从抽象后的真实世界历史中学习一个循环式潜在状态。
- ASTRA 在配对的模拟器/真实数据上用三个损失训练这个潜在状态：**latent transition loss** 用来预测下一个潜在状态，**reward prediction loss** 用来保留与任务相关的信息，**abstract next-state correction loss** 用来把模拟器对下一状态的预测调整到更接近真实的抽象下一状态。
- 对齐后的模拟器会使用修正后的抽象状态和学到的潜在动力学向前滚动，然后在这个对齐后的模拟器上训练 RL 策略。部署时，目标端编码器把真实世界历史映射到同一个潜在空间里。

## 结果
- 论文声称，ASTRA 在直接迁移和多个基线方法失败的 **sim2sim** 和 **sim2real** 场景中，都能成功迁移。
- 在 **AntMaze sim2sim navigation** 中，ASTRA 在 **U-Maze** 和 **Long Maze** 上都取得了比较方法中的 **最高成功率**，比较对象包括 Direct Transfer、Domain Randomization、COMPASS、RMA、NAS 和 DT+IQL。摘录没有给出 Figure 3 里的具体成功率数字。
- 在一个 **morphology-shift test** 中，使用 **1.25× leg length** 的改造 Ant，ASTRA 用标准 Ant 训练出的策略在 **U-Maze** 上达到 **65% success**，而直接迁移只有 **21%**。
- 在 AntMaze 的对齐数据上，ASTRA 和 NAS 使用了 **200 trajectories**，平均长度 **500 steps**，这些轨迹由随机行为策略收集。
- 在这个设置里，抽象到目标的差距很大：目标 AntMaze 状态有 **29 dimensions**，而抽象模拟器只使用 **location and velocity**。
- 摘录还说 ASTRA 也能用于 **real NAO humanoid tasks** 和模拟的人形机器人行走，但提供的文本里没有这些实验的最终定量结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15289v1](http://arxiv.org/abs/2604.15289v1)
