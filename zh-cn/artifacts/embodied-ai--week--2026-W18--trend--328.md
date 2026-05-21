---
kind: trend
trend_doc_id: 328
granularity: week
period_start: '2026-04-27T00:00:00'
period_end: '2026-05-04T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- sim-to-real
- robot deployment
- long-horizon manipulation
run_id: materialize-outputs
aliases:
- recoleta-trend-328
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/sim-to-real
- topic/robot-deployment
- topic/long-horizon-manipulation
language_code: zh-CN
---

# 机器人 VLA 主张现在取决于执行预算

## Overview
本周机器人论文集用实时执行来判断 Vision-Language-Action (VLA) 系统：延迟、恢复、数据循环和 sim-to-real 接触。MotuBrain、Sentinel-VLA 和 LWD 提供主要信号，分别把动作-世界预测、状态监控和机群学习连接到硬件或基准结果。

## Clusters

### 低延迟动作结构
VLA 论文把动作生成当作控制设计问题来处理。Libra-VLA 将粗粒度离散意图与连续精细控制分开，让规划器以较低频率运行，细化器按控制频率执行。它报告在 LIBERO 上平均成功率为 97.2%，在 LIBERO-Plus 零样本迁移上为 79.5%。

World-action 工作在同一约束下加入未来状态预测。MotuBrain 用一个扩散模型同时预测动作和未来视觉状态，支持多视角，并使用更快的推理栈。报告的延迟从 4.90 秒降至 0.09 秒，频率升至 11.11 Hz。实用结论很直接：预测模型只有适配机器人的更新预算时才有意义。

#### Evidence
- [Libra-VLA: Achieving Learning Equilibrium via Asynchronous Coarse-to-Fine Dual-System](../Inbox/2026-04-27--libra-vla-achieving-learning-equilibrium-via-asynchronous-coarse-to-fine-dual-system.md): Libra-VLA 摘要给出了粗到细的策略设计、LIBERO 结果和异步推理设置。
- [MotuBrain: An Advanced World Action Model for Robot Control](../Inbox/2026-04-30--motubrain-an-advanced-world-action-model-for-robot-control.md): MotuBrain 摘要给出了统一 world-action 模型设计以及延迟/频率结果。

### 执行时判断与恢复
多篇论文在执行过程中加入决策检查。VLA-ATTC 只在动作样本不一致时增加计算量，然后用 Relative Action Critic 在候选动作中选择。 在真实 Agilex Piper 任务上，自适应版本使 PI0 成功率从 46.0% 提高到 58.7%，论文报告控制频率为 20.8 Hz。

Sentinel-VLA 加入状态监视器，用于检测 Initial、Normal、New-subtask 和 Error 状态。它在开始时规划，在正常执行时复用记忆，并在出错后生成恢复行为。报告的 13 ms/action 延迟让监视器接近 PI0 的时序，同时把真实 Agilex Piper 三项任务的平均成功率提高到 60.0%。

导航工作在网络延迟下处理同类问题。AsyncShield 用 SE(2) 位姿变换重新对齐延迟的云端 VLA 路点，并加入带安全约束的局部策略。在混合网络退化下，成功率达到 76.7%；去掉对齐的消融版本降至 36.7%。

#### Evidence
- [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](../Inbox/2026-05-02--vla-attc-adaptive-test-time-compute-for-vla-models-with-relative-action-critic-model.md): VLA-ATTC 摘要给出了由不确定性触发的候选选择、真实机器人成功率提升和控制频率。
- [Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery](../Inbox/2026-05-02--sentinel-vla-a-metacognitive-vla-model-with-active-status-monitoring-for-dynamic-reasoning-and-error-recovery.md): Sentinel-VLA 摘要给出了状态监控、恢复行为、延迟和真实世界结果。
- [AsyncShield: A Plug-and-Play Edge Adapter for Asynchronous Cloud-based VLA Navigation](../Inbox/2026-04-27--asyncshield-a-plug-and-play-edge-adapter-for-asynchronous-cloud-based-vla-navigation.md): AsyncShield 摘要给出了延迟路点校正、安全策略设计以及退化/消融结果。

### 部署数据循环
本周的部署论文把已投放机器人当作数据来源。LWD 用离线数据、自主机群 rollout 和可选的人类干预来训练单一 VLA 策略。它的真实世界评估使用 16 台双臂机器人，覆盖 8 项任务，包括 3–5 分钟的长程操作；经过几小时在线交互后，报告平均成功率为 95%。

数据采集工作处理小实验室的瓶颈。Phone2Act 将 Android 手机变成 6-DoF 遥操作器，并以 LeRobot 格式记录同步示教。用采集到的 130 个 episode 微调 GR00T-N1.5-3B 后，在 10 次真实 Dobot CR5 试验中成功 9 次，但手机到机器人的路径实测延迟仍为 350–440 ms。

Lucid-XR 用基于头显的仿真和生成的多视角图像扩展数据路径。在 30 分钟会话中，用户采集的示教数量约为真实遥操作的两倍；数据增强把有效数据集规模提高到真实基线的约五倍。

#### Evidence
- [Learning while Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies](../Inbox/2026-05-01--learning-while-deploying-fleet-scale-reinforcement-learning-for-generalist-robot-policies.md): LWD 摘要给出了机群规模在线强化学习设置、任务集和 95% 平均成功率。
- [Phone2Act: A Low-Cost, Hardware-Agnostic Teleoperation System for Scalable VLA Data Collection](../Inbox/2026-05-03--phone2act-a-low-cost-hardware-agnostic-teleoperation-system-for-scalable-vla-data-collection.md): Phone2Act 摘要给出了手机遥操作设计、LeRobot 记录、延迟和微调结果。
- [Lucid-XR: An Extended-Reality Data Engine for Robotic Manipulation](../Inbox/2026-04-30--lucid-xr-an-extended-reality-data-engine-for-robotic-manipulation.md): Lucid-XR 摘要给出了 XR 数据采集速率、增强规模和真实机器人迁移主张。

### 面向接触的仿真与 sim-to-real 迁移
仿真论文关注接触、视觉保真度和硬件迁移。GS-Playground 将批处理 3D Gaussian Splatting 渲染器与并行物理引擎结合，并在运动和接触过程中把渲染出的高斯簇绑定到刚体。它报告在 640×480 分辨率下约 10,000 FPS 的渲染速度，并支持在该分辨率下最多 2048 个渲染场景。

DexSim2Real 使用视觉语言模型作为真实感评判器，为灵巧操作调节仿真随机化。最终策略在 Isaac Sim 中训练，并迁移到配有 Allegro Hand 的真实 Franka Panda。六项真实任务的平均成功率为 78.2%，sim-to-real 差距为 8.3%；消融显示，移除触觉输入、引导式随机化或技能课程都会带来损失。

#### Evidence
- [GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning](../Inbox/2026-04-28--gs-playground-a-high-throughput-photorealistic-simulator-for-vision-informed-robot-learning.md): GS-Playground 摘要给出了高吞吐照片级真实感仿真、接触物理和渲染吞吐量。
- [DexSim2Real: Foundation Model-Guided Sim-to-Real Transfer for Generalizable Dexterous Manipulation](../Inbox/2026-05-03--dexsim2real-foundation-model-guided-sim-to-real-transfer-for-generalizable-dexterous-manipulation.md): DexSim2Real 摘要给出了由基础模型引导的随机化、触觉-视觉策略设计和真实灵巧操作结果。
