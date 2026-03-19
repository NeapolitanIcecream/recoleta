---
source: arxiv
url: http://arxiv.org/abs/2603.04531v1
published_at: '2026-03-04T19:17:42'
authors:
- Rosy Chen
- Mustafa Mukadam
- Michael Kaess
- Tingfan Wu
- Francois R Hogan
- Jitendra Malik
- Akash Sharma
topics:
- robot-learning
- dexterous-manipulation
- tactile-sensing
- sim-to-real
- privileged-distillation
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# PTLD: Sim-to-real Privileged Tactile Latent Distillation for Dexterous Manipulation

## Summary
PTLD提出一种不需要在仿真中显式模拟触觉传感器的灵巧操作学习方法。它先用仿真中的“特权传感器”训练强策略，再在真实世界中把该策略的潜表示蒸馏到触觉编码器上，实现更强的触觉操控。

## Problem
- 论文解决的是**多指灵巧手触觉操控难以训练**的问题：示教数据昂贵，而触觉仿真既慢又不真实，导致传统模仿学习和端到端触觉RL都受限。
- 这很重要，因为家庭与服务机器人中的接触丰富任务（如手内旋转、重定向、工具操作）需要比仅靠本体感觉更强的状态感知能力。
- 现有零样本sim-to-real方法通常退回到仅用本体感觉的“盲操作”策略，性能上限受限，尤其在滑移、质量变化和复杂重定向任务上不足。

## Approach
- 核心机制很简单：**不去仿真触觉，而是仿真中训练一个能看见更多信息的强老师，在真实机器人上运行它，再让触觉学生去模仿老师内部的潜表示。**
- 在仿真中，作者用**Asymmetric Actor-Critic + PPO**训练策略：critic看特权状态，actor只看可部署观测，并加入在线latent distillation损失，让actor编码器学会逼近特权表示。
- 在真实世界中，作者搭建带**4个RGB-D相机 + Aruco标记**的“特权传感器”环境，得到物体位姿等高可观测信息，从而实际部署特权策略并采集**触觉观测-特权latent**配对数据。
- 然后用监督学习训练触觉编码器：输入包括Allegro手上的**18个Xela uSkin触觉pad，共368个传感点、3轴原始信号**及相关位置信息，输出匹配老师latent；为减轻离线蒸馏分布偏移，还使用**DAgger**迭代聚合数据。
- 针对任务，旋转任务使用**0.5秒、100Hz**触觉历史 + 1D时序卷积编码器；重定向任务使用结合触觉、关节本体感觉、目标姿态和历史latent的**因果Transformer**编码器。

## Results
- 在**in-hand rotation**基准任务上，PTLD相对**proprioception-only policy**实现了**182% improvement**；摘要未给出绝对分数，但明确声称加入触觉后显著提升旋转表现。
- 在更难的**tactile in-hand reorientation**任务上，PTLD使**number of goals reached**相比仅用本体感觉提升**57%**。
- 图注与摘要还宣称：在手内旋转中，PTLD对**物体滑移、质量变化、腕部朝向变化**更鲁棒；但摘录中未提供这些鲁棒性实验的完整定量表格。
- 论文还声称，重定向任务**无法仅靠本体感觉历史在仿真中学成**，而PTLD能够学会该任务，表明触觉蒸馏突破了纯本体感觉策略的能力上限。
- 关于训练方法，作者声称其**单阶段AAC + 在线latent distillation**在仿真评估中达到与传统两阶段privileged latent distillation**相近性能**，但摘录未给出具体数值。

## Link
- [http://arxiv.org/abs/2603.04531v1](http://arxiv.org/abs/2603.04531v1)
