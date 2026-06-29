---
kind: trend
trend_doc_id: 246
granularity: day
period_start: '2026-04-30T00:00:00'
period_end: '2026-05-01T00:00:00'
topics:
- robot world models
- vision-language-action policies
- latent reasoning
- reinforcement learning
- synthetic robot data
- extended reality
- graph world models
run_id: materialize-outputs
aliases:
- recoleta-trend-246
tags:
- recoleta/trend
- topic/robot-world-models
- topic/vision-language-action-policies
- topic/latent-reasoning
- topic/reinforcement-learning
- topic/synthetic-robot-data
- topic/extended-reality
- topic/graph-world-models
language_code: zh-CN
---

# 机器人世界模型现在必须在延迟和数据限制下证明控制价值

## Overview
这一时期的机器人学习工作集中在能在真实系统上运行的预测控制。MotuBrain、Being-H0.7 和 LaST-R1 给出的信号最清楚：只要未来状态推理能提高长时程动作质量，又不增加部署延迟，它就有价值。

## Clusters

### 适用于可部署机器人控制的世界-行动模型
世界-行动模型现在被当作控制系统来评估，而不只是预测器。MotuBrain把未来视频潜变量和动作 token 放进一个扩散模型里，然后把报告的端到端延迟从 4.90 秒降到 0.09 秒。它在 RoboTwin 2.0 上的得分在干净和随机化设置下都保持在 95% 以上，这让延迟结果成了这项主张的核心。

Being-H0.7 走的是更轻的路线。它在训练时用未来观测训练潜变量 token，然后在推理时去掉感知未来的分支。这个策略保留了面向动作的潜在状态，避免了测试时的视频展开，报告的部署延迟是每步 3–4 毫秒。综述论文给出了这些系统背后的共同定义：机器人世界模型会在当前状态、动作和可选语言条件下预测未来状态或观测。

#### Evidence
- [MotuBrain: An Advanced World Action Model for Robot Control](../Inbox/2026-04-30--motubrain-an-advanced-world-action-model-for-robot-control.md): MotuBrain summary, architecture, RoboTwin scores, and latency reduction.
- [Being-H0.7: A Latent World-Action Model from Egocentric Videos](../Inbox/2026-04-30--being-h0-7-a-latent-world-action-model-from-egocentric-videos.md): Being-H0.7 latent future training and deployment latency.
- [World Model for Robot Learning: A Comprehensive Survey](../Inbox/2026-04-30--world-model-for-robot-learning-a-comprehensive-survey.md): Survey definition of robot world models and their role in action-conditioned prediction.

### 潜在推理正在用任务奖励和目标可达性来训练
这一组里的视觉-语言-行动（VLA）策略会在输出动作前加入表示物理进展的内部信号。LaST-R1 用强化学习（RL）同时更新潜在推理嵌入和动作 token。报告结果是在 LIBERO 上每个任务只示范一次后，平均成功率达到 99.9%，在真实机器人部署中比监督微调最高提升 22.5%。

PRTS 加入了另一种进展信号。它用离线轨迹上的对比学习训练一个 4B VLA 模型，判断状态-动作对是否能到达语言目标。摘录没有给出成功率表，但给出了运行规模：167B token、64 块 H100 GPU、训练一周，以及覆盖 LIBERO 系列基准、SimplerEnv 和 14 个真实世界操作任务的评测。

#### Evidence
- [LaST-R1: Reinforcing Robotic Manipulation via Adaptive Physical Latent Reasoning](../Inbox/2026-04-30--last-r1-reinforcing-robotic-manipulation-via-adaptive-physical-latent-reasoning.md): LaST-R1 method and reported LIBERO and real-world gains.
- [PRTS: A Primitive Reasoning and Tasking System via Contrastive Representations](../Inbox/2026-04-30--prts-a-primitive-reasoning-and-tasking-system-via-contrastive-representations.md): PRTS goal-reachability training, scale, and evaluation coverage.

### XR 合成数据瞄准高接触操作覆盖
Lucid-XR 把扩展现实（XR）当成机器人操作的数据采集界面。示范者在运行于 XR 头显上的浏览器版 MuJoCo 仿真器里操作。系统记录运动，把运动重定向到机器人手或夹爪，并用生成式图像流水线把简单虚拟场景变成逼真的多视角训练图像。

报告数字指向数据吞吐量和视觉覆盖。这个仿真器在 Apple Vision Pro 上以 90 fps 运行，以 25 fps 记录。在三个任务的 30 分钟采集中，用户收集到的示范数量大约是实际遥操作的两倍。加入增强后，有效数据集规模达到了实际遥操作基线的约五倍。在使用未见网格的厨房清理任务上，ACT 加 LucidSim 在低杂乱环境中保持了 90% 成功率，而 ACT 单独使用时降到 0%。

#### Evidence
- [Lucid-XR: An Extended-Reality Data Engine for Robotic Manipulation](../Inbox/2026-04-30--lucid-xr-an-extended-reality-data-engine-for-robotic-manipulation.md): Lucid-XR system design, collection speed, augmentation scale, and kitchen clearing results.

### 世界模型综述正在收紧具身预测的术语
两篇综述论文给这一阶段加上了更清楚的分类层。机器人世界模型综述把策略学习、学习到的模拟器、可控视频预测、数据集和基准都放在动作条件预测之下。它把可行动模型的三个核心能力命名为：前瞻、通过想象结果进行规划，以及数据放大。

图世界模型综述把视角收窄到实体和关系。它用结构抽象和关系转移操作来定义图世界模型，然后按空间、物理和逻辑偏置来归类既有工作。这对操作和导航很重要，因为很多失败来自漏掉对象关系、接触关系或长时程状态更新，而不只是视觉特征不够强。

#### Evidence
- [World Model for Robot Learning: A Comprehensive Survey](../Inbox/2026-04-30--world-model-for-robot-learning-a-comprehensive-survey.md): Robot world-model survey taxonomy, equations, and core capabilities.
- [Graph World Models: Concepts, Taxonomy, and Future Directions](../Inbox/2026-04-30--graph-world-models-concepts-taxonomy-and-future-directions.md): Graph world-model definition, taxonomy, and relation-based modeling claims.
