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
这一时期的机器人学习工作集中在可运行于真实系统的预测控制上。MotuBrain、Being-H0.7 和 LaST-R1 给出了最清楚的信号：未来状态推理在提高长时程动作质量且不增加部署延迟时才有价值。

## Clusters

### 面向可部署机器人控制的世界-动作模型
世界-动作模型正在按控制系统来评估，评估范围已经从预测能力扩展到控制能力。MotuBrain 在一个扩散模型中结合未来视频潜变量和动作 token，并将报告的端到端延迟从 4.90 秒降到 0.09 秒。它在 RoboTwin 2.0 的干净设置和随机化设置中得分都保持在 95% 以上，因此延迟结果是其主张的核心依据。

Being-H0.7 采用更轻量的路线。它用未来观测训练潜在 token，然后在推理时移除感知未来的分支。该策略保留面向动作的潜在状态，避免测试时的视频 rollout，报告的部署速度为每步 3–4 ms。综述论文给出了这些系统背后的通用定义：机器人世界模型在当前状态、动作和可选语言条件下预测未来状态或观测。

#### Evidence
- [MotuBrain: An Advanced World Action Model for Robot Control](../Inbox/2026-04-30--motubrain-an-advanced-world-action-model-for-robot-control.md): MotuBrain 的摘要、架构、RoboTwin 得分和延迟降低。
- [Being-H0.7: A Latent World-Action Model from Egocentric Videos](../Inbox/2026-04-30--being-h0-7-a-latent-world-action-model-from-egocentric-videos.md): Being-H0.7 的潜在未来训练和部署延迟。
- [World Model for Robot Learning: A Comprehensive Survey](../Inbox/2026-04-30--world-model-for-robot-learning-a-comprehensive-survey.md): 综述对机器人世界模型的定义，以及它们在动作条件预测中的作用。

### 潜在推理正在用任务奖励和目标可达性来训练
这一组视觉-语言-动作（VLA）策略在输出动作前加入了表示物理进展的内部信号。LaST-R1 使用强化学习（RL）同时更新潜在推理嵌入和动作 token。报告结果是在每个任务只有一次演示的情况下，LIBERO 平均成功率达到 99.9%；在真实机器人部署中，相比监督微调最高提升 22.5%。

PRTS 加入了另一种进展信号。它训练一个 4B VLA 模型，用离线轨迹上的对比学习来评估一个状态-动作对是否能达到语言目标。摘录没有提供成功率表，但给出了运行规模：167B token、64 块 H100 GPU 训练一周，并在 LIBERO 系列基准、SimplerEnv 和 14 个真实世界操作任务上评估。

#### Evidence
- [LaST-R1: Reinforcing Robotic Manipulation via Adaptive Physical Latent Reasoning](../Inbox/2026-04-30--last-r1-reinforcing-robotic-manipulation-via-adaptive-physical-latent-reasoning.md): LaST-R1 方法，以及报告的 LIBERO 和真实世界增益。
- [PRTS: A Primitive Reasoning and Tasking System via Contrastive Representations](../Inbox/2026-04-30--prts-a-primitive-reasoning-and-tasking-system-via-contrastive-representations.md): PRTS 的目标可达性训练、规模和评估覆盖范围。

### XR 合成数据面向接触密集型操作覆盖
Lucid-XR 将扩展现实（XR）作为机器人操作的数据采集接口。演示者在 XR 头显上运行的基于浏览器的 MuJoCo 模拟器中操作。系统记录运动，将其重定向到机器人手或夹爪，并用生成式图像流水线把简单虚拟场景转换为逼真的多视角训练图像。

报告的数据指向数据吞吐量和视觉覆盖范围。模拟器在 Apple Vision Pro 上以 90 fps 运行，并以 25 fps 记录。在三个任务的 30 分钟采集会话中，用户收集的演示数量约为真实遥操作的两倍。经过增强后，有效数据集规模约达到真实遥操作基线的五倍。在使用未见过网格的厨房清理任务中，ACT 加 LucidSim 在低杂乱度设置下保持 90% 成功率，而单独使用 ACT 降至 0%。

#### Evidence
- [Lucid-XR: An Extended-Reality Data Engine for Robotic Manipulation](../Inbox/2026-04-30--lucid-xr-an-extended-reality-data-engine-for-robotic-manipulation.md): Lucid-XR 的系统设计、采集速度、增强规模和厨房清理结果。

### 世界模型综述正在收紧具身预测的词汇
两篇综述论文为这一时期提供了更清晰的分类。机器人世界模型综述把策略学习、学习型模拟器、可控视频预测、数据集和基准统一到动作条件预测之下。它列出了可执行模型的三项核心能力：预见、通过想象结果进行规划，以及数据放大。

图世界模型综述把视角收窄到实体和关系。它用结构抽象和关系转移操作来定义图世界模型，然后按空间、物理和逻辑偏置对既有工作分组。这一点对操作和导航有直接影响，因为许多失败来自遗漏物体关系、接触关系或长时程状态更新，而不只是视觉特征弱。

#### Evidence
- [World Model for Robot Learning: A Comprehensive Survey](../Inbox/2026-04-30--world-model-for-robot-learning-a-comprehensive-survey.md): 机器人世界模型综述的分类、方程和核心能力。
- [Graph World Models: Concepts, Taxonomy, and Future Directions](../Inbox/2026-04-30--graph-world-models-concepts-taxonomy-and-future-directions.md): 图世界模型的定义、分类和基于关系建模的主张。
