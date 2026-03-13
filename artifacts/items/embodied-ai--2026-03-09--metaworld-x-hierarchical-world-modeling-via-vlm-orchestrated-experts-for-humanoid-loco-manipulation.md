---
source: arxiv
url: http://arxiv.org/abs/2603.08572v1
published_at: '2026-03-09T16:28:26'
authors:
- Yutong Shen
- Hangxu Liu
- Penghui Liu
- Jiashuo Luo
- Yongkang Zhang
- Rex Morvley
- Chen Jiang
- Jianwei Zhang
- Lei Zhang
topics:
- humanoid-control
- world-model
- mixture-of-experts
- vision-language-models
- loco-manipulation
relevance_score: 0.88
run_id: materialize-outputs
---

# MetaWorld-X: Hierarchical World Modeling via VLM-Orchestrated Experts for Humanoid Loco-Manipulation

## Summary
MetaWorld-X 是一个面向人形机器人行走-操作一体化（loco-manipulation）的分层世界模型框架。它把复杂控制拆成多个带有人类动作先验的专家策略，并用 VLM 监督的路由器按任务语义组合这些专家，从而提升自然性、稳定性和组合泛化。

## Problem
- 论文要解决的是：单一整体策略在高自由度人形机器人上同时学习行走和操作时，容易出现跨技能梯度干扰、动作模式冲突、抖动、跌倒和不自然运动。
- 这很重要，因为人形机器人若想执行真实世界多阶段任务，必须同时保持平衡、移动和精细操作；仅优化任务回报常会牺牲动作自然性与稳定性。
- 现有世界模型或 MoE 方法要么有长时滚动偏差和策略失配，要么缺少显式语义驱动，难以实现稳定且可组合的技能编排。

## Approach
- 核心方法是“分而治之”：先训练一个 **Specialized Expert Pool (SEP)**，把站立、走路、跑步、坐下、搬运、伸手等基础技能分别学成独立专家，避免单一策略里不同技能互相打架。
- 每个专家都用 **人类动作数据 + 模仿约束强化学习** 训练：通过动作重定向把 MoCap/SMPL 运动映射到机器人，再用基于关节位置/速度误差的能量型奖励去逼近人类动作，从而让运动更自然、符合生物力学。
- 框架保留 **world model / latent planning**：把模仿对齐奖励接入世界模型的奖励头和值函数，在潜空间里用 MPPI/CEM 规划，提高样本效率和前瞻控制能力。
- 再训练一个 **Intelligent Routing Mechanism (IRM)**：输入当前观测和任务语义，输出各专家的混合权重，最终动作是各专家动作的加权和。
- 这个路由器由 **VLM 监督蒸馏**：先用任务级语义相关性做粗对齐，再用少样本演示做细化，使其从依赖 VLM 指导过渡到自主路由，并支持零样本/少样本组合泛化。

## Results
- 在 **Humanoid-bench** 的基础技能评测中，IRM 相比强基线在回报和收敛速度上更强：例如 **Walk** 上 Ours **1118.7±7.1**，高于 **TD-MPC2 644.2±162.3**、**DreamerV3 428.2±14.5**；收敛步数仅 **0.5M**，优于 TD-MPC2 的 **1.8M** 和 DreamerV3 的 **6.0M**。
- 在 **Run** 上优势尤其大：Ours **2056.9±13.6**，对比 **TD-MPC2 66.1±4.7**、**DreamerV3 298.5±84.5**；收敛步数 **1.0M**，优于 TD-MPC2 的 **2.0M** 与 DreamerV3 的 **6.0M**。
- 其他基础技能同样领先：**Stand 815.9±0.3 vs TD-MPC2 749.8±63.1**；**Sit 862.2±2.1 vs 733.9±120.6**；**Carry 963.5±5.1 vs 438.0±72.9**，且收敛通常在 **0.5–0.6M**，显著快于基线的 **1.1–6.0M**。
- 在 10 次独立试验的成功率上，Ours 在 **Stand/Walk/Run/Carry** 都达到 **9/10**，**Sit 8/10**；相比 **TD-MPC2** 仅 **3/10、3/10、2/10、3/10、4/10**，PPO 则多数为 **0/10**。
- 在复杂操作任务上，MetaWorld-X 也优于基线：**Door 470.0±2.2 vs TD-MPC2 285.0±12.0**，**Basketball 250.0±11.9 vs 148.4±3.3**，**Push 70.0±2.1 vs -113.8±6.8**，**Truck 1500.0±15.6 vs 1213.2±1.1**，**Package -5200.0±47.2 vs -6788.5±552.7**。
- 消融表明两个关键组件都重要：在 **Door** 任务上，**Full Model** 的 return 为 **303.95**、训练步数 **12.64w**；去掉 Router 后降为 **296.57 / 20.36w**；去掉 VLM 或 IL 则任务失败（其中 **w/o IL** return **193.61**，但无法有效收敛/适配）。

## Link
- [http://arxiv.org/abs/2603.08572v1](http://arxiv.org/abs/2603.08572v1)
