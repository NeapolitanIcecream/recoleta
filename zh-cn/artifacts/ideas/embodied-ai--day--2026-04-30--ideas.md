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

# 延迟感知的机器人策略训练

## Summary
机器人团队可以用控制测试评估预测型策略，报告动作质量、p95 推理延迟、更新率和所需任务数据量。具体工作包括延迟感知评测框架、把潜在推理纳入策略更新的 RL 后训练，以及用于物理遥操作较慢的富接触操作场景的 XR 数据采集流程。

## 面向世界-动作机器人策略的延迟感知评测框架
机器人策略团队应加入控制循环测试框架，同时报告成功率、端到端延迟、p95 延迟、动作更新频率和未来状态预测成本。有效的比较是在同一任务套件、相同相机布局和相同动作分块下，对比直接 VLA 控制、带潜在未来信息的控制，以及视频-动作联合预测。

MotuBrain 给出了这类测试的具体目标：它报告 RoboTwin 2.0 成功率超过 95%，同时将端到端延迟从 4.90 秒降到 0.09 秒，并把频率提高到 11.11 Hz。Being-H0.7 给出另一个设计点：训练时使用未来观测，推理时去掉未来感知分支，在没有测试时视频 rollout 的情况下达到每步 3–4 ms。一个实用的初步检查是在长程操作任务上做回放和真机运行；如果某个模型提高了预测质量却错过机器人的控制截止时间，报告应将其判为失败。

### Evidence
- [MotuBrain: An Advanced World Action Model for Robot Control](../Inbox/2026-04-30--motubrain-an-advanced-world-action-model-for-robot-control.md): MotuBrain 报告了未来视频/动作联合预测、RoboTwin 2.0 成功率超过 95%，并将延迟从 4.90 s 降到 0.09 s。
- [Being-H0.7: A Latent World-Action Model from Egocentric Videos](../Inbox/2026-04-30--being-h0-7-a-latent-world-action-model-from-egocentric-videos.md): Being-H0.7 使用未来观测进行训练，推理时移除后验分支，并报告了每步 3–4 ms 的部署速度。
- [World Model for Robot Learning: A Comprehensive Survey](../Inbox/2026-04-30--world-model-for-robot-learning-a-comprehensive-survey.md): 机器人世界模型综述定义了动作条件下的未来预测，并把前瞻、规划和数据扩增列为核心能力。

## 同时更新潜在推理和动作 token 的 RL 后训练运行
微调 VLA 操作策略的团队可以测试一次小规模 RL 后训练，把潜在推理 token 当作可训练的决策变量，而非只当作隐藏特征。运行应从一个范围较窄的任务族开始，每个任务使用一个或少量示范，并用任务奖励同时更新潜在嵌入和输出的动作块。

LaST-R1 是最清楚的局部案例。它从 Qwen3-VL-4B 出发，使用 SigLIP2-Large 视觉编码，采用基于 DINOv3 CLS 特征的紧凑潜在目标，并将 Latent-to-Action Policy Optimization 应用于潜在序列和动作序列。报告结果足以支持一次复现实验：在每个任务用一个示范进行预热后，LIBERO 各套件平均成功率为 99.9%；在四个真实世界任务中，相比监督微调平均提升最高 22.5%。有用的采用测试是：同一奖励路径能否在不增加推理时编码器的情况下，减少团队自有长程任务中的误差累积。

### Evidence
- [LaST-R1: Reinforcing Robotic Manipulation via Adaptive Physical Latent Reasoning](../Inbox/2026-04-30--last-r1-reinforcing-robotic-manipulation-via-adaptive-physical-latent-reasoning.md): LaST-R1 描述了 LAPO、对潜在推理和动作 token 的联合 RL 优化、LIBERO 单示范预热，以及报告的真实机器人增益。
- [LaST-R1: Reinforcing Robotic Manipulation via Adaptive Physical Latent Reasoning](../Inbox/2026-04-30--last-r1-reinforcing-robotic-manipulation-via-adaptive-physical-latent-reasoning.md): 论文称，在一次监督预热后，LIBERO 平均成功率为 99.9%；相比监督微调，真实世界表现最高提升 22.5%。

## 用于补齐富接触操作数据缺口的 XR 示范采集流程
机器人数据团队可以在物理遥操作时间大量耗在复位、安全检查和场景搭建的任务上，试点 XR 示范采集。工作流很明确：在头显浏览器中运行 MuJoCo，记录 SE(3) 手部或控制器运动，用逆运动学将其重定向到机器人手或夹爪，然后生成包含不同相机位姿、光照、杂物和物体网格的多视角训练图像。

Lucid-XR 报告的运行数据足以支持一次有限试验。系统在 Apple Vision Pro 上以 90 fps 运行，以 25 fps 记录；在三个任务的 30 分钟采集会话中，采集到的示范约为真实遥操作的两倍。加入增强后，有效数据集规模达到真实遥操作基线的约五倍。低成本验证方式是在一个富接触任务上做匹配的 30 分钟采集对比，然后进行有杂物的留出测试；在 Lucid-XR 的厨房清理结果中，ACT + LucidSim 在低杂物环境中保持 90% 成功率，而单独 ACT 降至 0%。

### Evidence
- [Lucid-XR: An Extended-Reality Data Engine for Robotic Manipulation](../Inbox/2026-04-30--lucid-xr-an-extended-reality-data-engine-for-robotic-manipulation.md): Lucid-XR 描述了基于浏览器的 MuJoCo 采集、重定向、生成式多视角数据、90 fps 运行、25 fps 记录，以及相对真实遥操作的吞吐提升。
- [Lucid-XR: An Extended-Reality Data Engine for Robotic Manipulation](../Inbox/2026-04-30--lucid-xr-an-extended-reality-data-engine-for-robotic-manipulation.md): 论文描述了用 MuJoCo 逆运动学和标记绑定，将人体姿态数据重定向到机器人形态。
