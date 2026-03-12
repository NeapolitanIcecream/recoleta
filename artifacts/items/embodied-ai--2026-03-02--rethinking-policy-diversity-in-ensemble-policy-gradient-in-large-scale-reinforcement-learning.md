---
source: arxiv
url: http://arxiv.org/abs/2603.01741v2
published_at: '2026-03-02T11:06:40'
authors:
- Naoki Shitanda
- Motoki Omura
- Tatsuya Harada
- Takayuki Osa
topics:
- reinforcement-learning
- policy-ensemble
- policy-gradient
- importance-sampling
- dexterous-manipulation
relevance_score: 0.44
run_id: materialize-outputs
---

# Rethinking Policy Diversity in Ensemble Policy Gradient in Large-Scale Reinforcement Learning

## Summary
本文研究大规模并行强化学习中的“策略多样性”该如何控制，而不是一味增大。作者提出 CPO，通过把跟随者策略限制在领导者附近，同时保留适度差异，来提升探索质量、样本效率与训练稳定性。

## Problem
- 论文解决的是：在**数万并行环境**下，单一策略探索不够多样，而多策略集成若彼此差异过大，又会让重要性采样失真、训练变得不稳定。
- 这很重要，因为大规模机器人强化学习（尤其灵巧操作）越来越依赖海量并行仿真；如果多收集的数据对学习无效，算力和样本都会被浪费。
- 现有 leader-follower 集成方法（如 SAPG）能增加探索，但没有显式约束 follower 和 leader 的距离，可能出现策略错位（misalignment）。

## Approach
- 核心方法是 **Coupled Policy Optimization (CPO)**：在 leader-follower 框架里，对每个 follower 的更新加入**相对 leader 的 KL 散度约束**，让 follower 在 leader 周围探索，而不是跑得太远。
- 最简单地说：作者想让多个策略“**分散但别失联**”。这样 follower 采到的数据仍然对 leader 有用，重要性采样比值更接近 1。
- 理论上，论文分析了过大 inter-policy diversity 的坏处：策略差太远会降低 **effective sample size (ESS)**，并加大 PPO clipping 带来的梯度偏差；同时证明 IS ratio 偏离 1 可由 follower-leader 的 KL 上界控制。
- 为防止所有 follower 又挤成一团，作者再加入**对抗式内在奖励**：训练一个判别器根据状态-动作识别策略身份，鼓励不同 follower 在 leader 周围覆盖不同区域。
- 实验设置上，方法基于 PPO/SAPG，在 Isaac Gym 中使用 **24,576** 个并行环境、**M=6** 个并行策略块，在灵巧操作、夹爪操作和 locomotion 任务上评测。

## Results
- 在 **6 个灵巧操作任务**上，经过 **2×10^10 environment steps**，CPO 在多数任务上达到最好或并列最好结果：ShadowHand **13762±414**（SAPG **12882±343**，PPO **10661±1050**），AllegroHand **14421±885**（PBT **13239±239**，SAPG **11989±817**），Reorientation **43.75±0.65**（SAPG **38.79±1.66**，PBT **2.92±4.27**，PPO **1.04±0.98**）。
- 在 **Two-Arms Reorientation** 上提升尤为明显：CPO **35.30±2.77**，显著高于 SAPG **5.11±3.41**，也高于 PBT **26.43±11.12** 和 PPO **1.41±0.80**。
- 在 **Regrasping** 上，CPO **37.44±1.21**，与 SAPG **37.20±0.65**、PBT **35.26±2.82** 接近并略优；在 **Throw** 上，CPO **21.69±2.44**，略低于 SAPG **22.51±1.15**，但仍优于 PBT **19.08±1.02** 和 PPO **15.69±3.34**。
- 作者声称在许多任务中，CPO 用大约**一半环境步数**即可达到 SAPG 的最终性能，说明其样本效率更高；给定摘录中未提供逐任务的完整曲线数值，但这是论文的明确经验性主张。
- 机制层面的结果是：KL 约束让 leader 使用 follower 数据时的 **IS ratio 更接近 1**，从而提高 ESS、减轻 PPO clipping bias，并形成“follower 围绕 leader 分布”的更有结构的探索形态。

## Link
- [http://arxiv.org/abs/2603.01741v2](http://arxiv.org/abs/2603.01741v2)
