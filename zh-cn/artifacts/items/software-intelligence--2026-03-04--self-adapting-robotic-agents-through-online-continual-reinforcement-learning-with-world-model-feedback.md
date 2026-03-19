---
source: arxiv
url: http://arxiv.org/abs/2603.04029v1
published_at: '2026-03-04T13:07:42'
authors:
- Fabian Domberg
- Georg Schildbach
topics:
- continual-reinforcement-learning
- model-based-rl
- robot-adaptation
- world-models
- out-of-distribution-detection
relevance_score: 0.32
run_id: materialize-outputs
language_code: zh-CN
---

# Self-adapting Robotic Agents through Online Continual Reinforcement Learning with World Model Feedback

## Summary
本文提出一种让机器人在部署后也能**自动发现环境/机体变化并在线继续学习**的框架，核心是用世界模型的预测误差来触发 DreamerV3 微调。作者在连续控制、四足机器人仿真和真实小车上展示了该方法可在无外部监督下恢复性能。

## Problem
- 传统学习型机器人通常**离线训练、上线参数固定**，一旦遇到未见过的动力学变化、执行器故障或 sim-to-real 偏移，性能会明显下降。
- 持续强化学习的关键难点有两个：**何时检测到变化**，以及**如何在运行中自动适配**，且不依赖人工标注任务边界。
- 这很重要，因为真实机器人长期运行时不可避免会遇到**分布外事件**；若不能自适应，系统鲁棒性和自主性都会受限。

## Approach
- 基于 **DreamerV3**：同时学习一个潜在空间里的**世界模型**和策略，策略主要在世界模型“想象”的轨迹上训练，从而提高样本效率。
- 在部署时持续做未来 **n=15** 步预测，并计算**观测预测残差（OPR）**和**奖励预测残差（RPR）**；如果任一指标超过滚动均值的 **3 个标准差**，就判定发生分布外变化。
- 一旦检测到变化，就用 DreamerV3 的原始训练回路在线微调世界模型和策略；实现上使用 **12M 参数** 的 medium 配置、**train ratio=16**。
- 为了**自动判断适配是否完成**，不仅看任务层面的 reward/残差，还联合监控内部训练信号：**dynamics loss、advantage magnitude、value loss** 是否趋于稳定收敛。
- 微调时**不把变化前的数据放入回放缓冲区**，避免旧动力学干扰对新情况的学习。

## Results
- **DMC Walker-walk**：在 **5,000 steps** 时随机将一个关节的齿轮比减半，奖励立刻下降、RPR 上升；方法可快速检测并启动适配，**少于 10,000 steps**（约 **2 分钟**仿真时间）后，大多数指标回到接近改动前水平；结果基于**10 次运行均值**。
- **ANYmal 四足机器人（Isaac Lab）**：先训练 **25M steps**，再在 **9,000 steps** 时把右后腿 3 个执行器速度限制降为原来的 **1/3**；方法平均在约 **5,000 steps**（约 **4 分钟**）后恢复稳定步态，最后一条运行在 **26,000 steps** 停止微调；结果基于**9 次运行均值**。
- **真实 F1Tenth 1:10 小车，sim-to-real**：仿真预训练 **10M steps**，在 **10,000 steps** 切换到真车后 OPR 激增、reward 下滑；在线微调约 **10,000 steps**（约 **8 分钟**）后行为稳定，约到 **50,000 steps** 时奖励恢复到接近仿真水平。
- **真实小车摩擦变化**：在约 **52,000 steps** 给后轮套袜子降低摩擦后，奖励下降约 **20%**；系统再次进入适配阶段，损失很快回落，最终学会以**稍低速度**过弯以避免打滑，但总奖励因此略低于改动前。
- 论文也展示了**失败案例**：当多项指标始终不稳定时，系统可识别为**未收敛**并中止适配；这支持其“自动评估适配成败”的主张。
- 论文未给出与其他 CRL/MBRL 方法的**统一数值对比表**或标准 benchmark SOTA 指标；最强证据主要是上述跨仿真与真实系统的恢复时间、步数和性能恢复现象。

## Link
- [http://arxiv.org/abs/2603.04029v1](http://arxiv.org/abs/2603.04029v1)
