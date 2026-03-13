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
- humanoid-robotics
- world-models
- mixture-of-experts
- vision-language-models
- imitation-learning
relevance_score: 0.18
run_id: materialize-outputs
---

# MetaWorld-X: Hierarchical World Modeling via VLM-Orchestrated Experts for Humanoid Loco-Manipulation

## Summary
MetaWorld-X提出一种面向人形机器人行走-操作一体化控制的分层框架，把复杂控制拆成多个专长专家，再用VLM监督的路由器按任务语义组合这些专家。其目标是同时提升动作自然性、稳定性、训练效率和跨任务组合泛化能力。

## Problem
- 该工作要解决的是**高自由度人形机器人在同时行走与操作时，单一策略难以稳定学习多技能组合**的问题；单体策略容易出现跨技能梯度干扰、动作冲突、抖动、跌倒和不自然姿态。
- 这很重要，因为loco-manipulation是人形机器人执行真实世界多阶段任务的核心能力；如果控制不稳定或动作不自然，就难以可靠完成复杂任务。
- 现有世界模型/RL方法虽有样本效率优势，但长时域预测偏差、值高估和对任务回报的单一优化，往往不能保证生物力学合理性与组合泛化。

## Approach
- 核心思路很简单：**不要让一个大策略学会所有事**，而是先训练一组“专科医生式”的专家策略（SEP），每个只负责站立、行走、奔跑、坐下、搬运、伸手等基础技能。
- 这些专家通过**带有人类动作先验的模仿约束强化学习**训练：把MoCap动作重定向到机器人，再用基于关节位置/速度对齐的能量奖励去鼓励机器人模仿自然的人类动作，从而生成更自然、更稳定的运动原语。
- 在专家之上，作者设计了**VLM监督的智能路由机制（IRM）**：VLM根据任务语义给出“哪些专家更相关”的指导，路由器再输出各专家的权重，并将多个专家动作按权重加权组合。
- 路由训练分两层：先用任务级语义先验做粗对齐，再用少样本演示做时序行为细化；随着训练进行，VLM指导权重衰减，路由器逐步从“被教”过渡到“自主路由”。
- 推理时不再频繁查询VLM，只保留低延迟路由网络，因此可以实时控制人形机器人执行多阶段任务。

## Results
- 在Humanoid-bench基础技能评测中，**Ours (IRM)** 的峰值回报和收敛速度均显著优于基线：例如 **Walk 1118.7±7.1 vs TD-MPC2 644.2±162.3，收敛步数0.5M vs 1.8M**；**Run 2056.9±13.6 vs TD-MPC2 66.1±4.7，1.0M vs 2.0M**；**Carry 963.5±5.1 vs 438.0±72.9，0.5M vs 1.9M**。
- 其他基础技能同样提升明显：**Stand 815.9±0.3 vs TD-MPC2 749.8±63.1，0.6M vs 1.8M**；**Sit 862.2±2.1 vs 733.9±120.6，0.6M vs 1.1M**。相较DreamerV3、PPO、SAC也普遍更高回报且更快收敛。
- 在成功率（10次试验）上，作者方法在500k步后达到：**Stand 9/10、Walk 9/10、Run 9/10、Sit 8/10、Carry 9/10**；而TD-MPC2仅为**3/10、3/10、2/10、4/10、3/10**，DreamerV3为**2/10、2/10、1/10、3/10、2/10**。
- 在复杂操作任务上也优于基线：**Door 470.0±2.2 vs TD-MPC2 285.0±12.0**，**Basketball 250.0±11.9 vs 148.4±3.3**，**Push 70.0±2.1 vs -113.8±6.8**，**Truck 1500.0±15.6 vs 1213.2±1.1**，**Package -5200.0±47.2 vs -6788.5±552.7**。
- 消融实验显示模块互补：在Door任务上，**Full Model** 以 **12.64w steps、return 303.95** 优于 **TD-MPC2 的32.38w、198.42**；**w/o Router** 仍可成功但较差（20.36w，296.57）；**w/o VLM** 无法训练成功；**w/o IL** 失败且步数趋于无穷，说明VLM语义路由和模仿学习先验都很关键。
- 论文还声称具备**few-shot与zero-shot组合泛化**能力，但在给定摘录中，除路由日程和任务表现外，这部分没有更细的单独量化指标。

## Link
- [http://arxiv.org/abs/2603.08572v1](http://arxiv.org/abs/2603.08572v1)
