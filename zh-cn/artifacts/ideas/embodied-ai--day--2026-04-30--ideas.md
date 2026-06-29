---
kind: ideas
granularity: day
period_start: '2026-04-30T00:00:00'
period_end: '2026-05-01T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot world models
- vision-language-action policies
- latent reasoning
- reinforcement learning
- synthetic robot data
- extended reality
- graph world models
tags:
- recoleta/ideas
- topic/robot-world-models
- topic/vision-language-action-policies
- topic/latent-reasoning
- topic/reinforcement-learning
- topic/synthetic-robot-data
- topic/extended-reality
- topic/graph-world-models
language_code: zh-CN
---

# 面向机器人策略训练的低延迟评测

## Summary
机器人团队可以用控制测试来检验预测式策略，报告动作质量、p95 推理延迟、更新频率，以及任务数据需求。具体工作包括一个考虑延迟的评测工具、把潜在推理作为策略一部分来更新的 RL 训练后处理，以及一种适用于物理遥操作较慢的接触密集操作任务的 XR 数据采集流程。

## 用于 world-action 机器人策略的低延迟评测工具
机器人策略团队应加入一个控制回路测试工具，报告成功率、端到端延迟、p95 延迟、动作更新频率，以及未来状态预测的成本。更有用的比较方式是在同一套任务上，用相同的相机布局和动作分块，直接比较 VLA 控制、潜在未来感知控制和视频-动作联合预测。

MotuBrain 给出了这类测试的一个具体目标：它在 RoboTwin 2.0 上的成功率超过 95%，同时把端到端延迟从 4.90 秒降到 0.09 秒，把频率提高到 11.11 Hz。Being-H0.7 指向另一个设计点：训练时使用未来观测，推理时去掉未来感知分支，在不做测试时视频展开的情况下把每步运行时间压到 3–4 毫秒。一个实用的首轮检查，是在长时程操作任务上做回放和真机运行，凡是只提高预测质量、却错过机器人控制截止时间的模型，都应被判失败。

### Evidence
- [MotuBrain: An Advanced World Action Model for Robot Control](../Inbox/2026-04-30--motubrain-an-advanced-world-action-model-for-robot-control.md): MotuBrain reports joint future-video/action prediction, RoboTwin 2.0 success above 95%, and a latency reduction from 4.90 s to 0.09 s.
- [Being-H0.7: A Latent World-Action Model from Egocentric Videos](../Inbox/2026-04-30--being-h0-7-a-latent-world-action-model-from-egocentric-videos.md): Being-H0.7 trains with future observations, removes the posterior branch at inference, and reports 3–4 ms per-step deployment.
- [World Model for Robot Learning: A Comprehensive Survey](../Inbox/2026-04-30--world-model-for-robot-learning-a-comprehensive-survey.md): The robot world-model survey defines action-conditioned future prediction and frames foresight, planning, and data amplification as core capabilities.

## 同时更新潜在推理和动作 token 的 RL 训练流程
对 VLA 操作策略做微调的团队，可以测试一次小规模的 RL 训练后处理，把潜在推理 token 当作可训练的决策变量，而不只是隐藏特征。这个流程应从一个窄任务族开始，每个任务用一条或少量示范，并用任务奖励同时更新潜在嵌入和输出的动作分块。

LaST-R1 是最清楚的本地案例。它以带有 SigLIP2-Large 视觉编码的 Qwen3-VL-4B 为起点，用基于 DINOv3 CLS 特征的紧凑潜在目标，并把 Latent-to-Action Policy Optimization 用在潜在序列和动作序列上。报告结果足以支持一次复现检查：在每个任务只用一条示范做 warm-up 后，LIBERO 各套件的平均成功率达到 99.9%，在四个真实世界任务上，相比监督微调最高平均提升 22.5%。真正有用的采用测试，是看同样的奖励路径能否在团队自己的长时程任务上减少连锁误差，同时不增加推理时编码器。

### Evidence
- [LaST-R1: Reinforcing Robotic Manipulation via Adaptive Physical Latent Reasoning](../Inbox/2026-04-30--last-r1-reinforcing-robotic-manipulation-via-adaptive-physical-latent-reasoning.md): LaST-R1 describes LAPO, joint RL optimization of latent reasoning and action tokens, one-demonstration LIBERO warm-up, and reported real-robot gains.
- [LaST-R1: Reinforcing Robotic Manipulation via Adaptive Physical Latent Reasoning](../Inbox/2026-04-30--last-r1-reinforcing-robotic-manipulation-via-adaptive-physical-latent-reasoning.md): The paper states 99.9% LIBERO average success with one-shot supervised warm-up and up to 22.5% real-world improvement over supervised fine-tuning.

## 适用于接触密集操作数据缺口的 XR 示范采集流程
机器人数据团队可以先试行 XR 示范采集，适用于那些物理遥操作时间被重置、安全检查和场景搭建消耗掉的任务。流程很直接：在头显浏览器里运行 MuJoCo，记录 SE(3) 手部或控制器运动，用逆运动学把它重定向到机器人手或夹爪，再用不同的相机位姿、光照、杂乱程度和物体网格生成多视角训练图像。

Lucid-XR 给出了值得做小规模试验的运营数据。这个系统在 Apple Vision Pro 上以 90 fps 运行，以 25 fps 记录数据，并且在三个任务的 30 分钟采集中，采到的示范数量大约是现实遥操作的两倍。经过增强后，有效数据集规模约为现实遥操作基线的五倍。一个低成本验证方式，是在一个接触密集任务上做 30 分钟的配对采集比较，再做一个杂乱场景的留出测试；在 Lucid-XR 的厨房清理结果里，ACT 加 LucidSim 在低杂乱下保持了 90% 成功率，而单独的 ACT 掉到 0%。

### Evidence
- [Lucid-XR: An Extended-Reality Data Engine for Robotic Manipulation](../Inbox/2026-04-30--lucid-xr-an-extended-reality-data-engine-for-robotic-manipulation.md): Lucid-XR describes browser-based MuJoCo collection, retargeting, generative multi-view data, 90 fps operation, 25 fps recording, and throughput gains over real teleoperation.
- [Lucid-XR: An Extended-Reality Data Engine for Robotic Manipulation](../Inbox/2026-04-30--lucid-xr-an-extended-reality-data-engine-for-robotic-manipulation.md): The paper describes retargeting human pose data to robot form factors with MuJoCo inverse kinematics and markup bindings.
