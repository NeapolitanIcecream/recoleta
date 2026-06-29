---
kind: ideas
granularity: week
period_start: '2026-04-27T00:00:00'
period_end: '2026-05-04T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- world models
- sim-to-real
- robot deployment
- long-horizon manipulation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/sim-to-real
- topic/robot-deployment
- topic/long-horizon-manipulation
language_code: zh-CN
---

# 机器人执行反馈循环

## Summary
机器人 VLA 工作正在转向三个实际变化：为不确定性和错误增加 rollout 检查，按机器人端延迟和能耗预算评估模型变更，并把已部署机器人作为带干预日志的数据源。共同压力来自执行：策略必须能从错误动作中恢复，符合控制循环，并从发布后遇到的失败中改进。

## 面向不确定 VLA 动作和执行错误的 rollout 门控
操作团队可以先在现有 VLA 策略外加一层 rollout 门控，再重训整个模型。门控在执行时应观察两个信号：采样 action chunks 之间的分歧，以及可见的任务状态错误，例如抓取失败、拿错物体或位姿滑移。低风险步骤可以继续由基础策略执行。高分歧状态或错误状态可以触发候选动作采样、relative action critic 或恢复计划。

VLA-ATTC 给出了一种实现方式：采样两个 action chunks，用 Dynamic Time Warping 距离作为不确定性信号，只在距离超过阈值时增加计算量。在真实 Agilex Piper 任务上，PI0 使用自适应版本后平均成功率从 46.0% 升至 58.7%，同时报告了 20.8 Hz 控制频率。Sentinel-VLA 给出互补的状态监控方式：预测 Initial、Normal、New-subtask 或 Error，保留任务记忆，并在检测到错误时生成恢复行为。它报告在三个真实 Agilex Piper 任务上的平均成功率为 60.0%，在 RTX4090 上为 13 ms/action。

一个有用的首个测试，是回放近期失败 rollout，并注入抓取、位姿和语义错误。验收标准应包括成功率提升、错误恢复触发的误报，以及每个动作增加的延迟，因为恢复层即使改善了离线轨迹，只要超出控制预算，在机器人上仍会失败。

### Evidence
- [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](../Inbox/2026-05-02--vla-attc-adaptive-test-time-compute-for-vla-models-with-relative-action-critic-model.md): VLA-ATTC 报告了自适应测试时计算、基于采样 action chunks 的不确定性检测、真实 Agilex Piper 成功率提升，以及 20.8 Hz 控制频率。
- [Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery](../Inbox/2026-05-02--sentinel-vla-a-metacognitive-vla-model-with-active-status-monitoring-for-dynamic-reasoning-and-error-recovery.md): Sentinel-VLA 报告了状态监控、错误恢复、真实世界 Agilex Piper 结果，以及 13 ms/action 的时延。

## VLA 模型变更的机器人端延迟和能耗验收测试
机器人团队应把每一次 VLA 模型替换、量化处理、扩散步数变更或硬件迁移，都作为一次机器人端验收测试。测试应在目标机器人计算机上记录闭环延迟、控制频率、内存使用、每次 rollout 的能耗和任务成功率。移动操作机器人在推理错过控制周期时会卡顿或振荡，桌面 GPU 数字不足以说明问题。

XPU 表征论文说明了原因。对于 pi0，论文报告 RTX 4090 推理为 102.3 ms，Jetson Thor 为 246.0 ms，AGX Orin 为 920.6 ms，Intel B60 Pro 为 306.5 ms，Ascend 310P 为 818.0 ms，且能耗成本不同。编译把 RTX 4090 上的 pi0 加速到 35.2 ms 和 28.41 Hz，但同一优化在 Jetson Thor 上只有 6.13 Hz，在 Ascend 310P 上只有 2.86 Hz。论文还报告了一项 OpenVLA 加速会使 LIBERO 平均成功率从 76.5% 降至 68.5%，因此速度检查需要配套成功率检查。

MotuBrain 对 world-action 模型也指向同一条门控规则。它声称的价值取决于把端到端延迟从 4.90 秒降至 0.09 秒，把频率提高到 11.11 Hz，同时在优化栈之后让 RoboTwin 2.0 成功率变化低于一个百分点。实用的发布清单应要求同一组成对报告：部署硬件上的动作频率和成功率。

### Evidence
- [Characterizing Vision-Language-Action Models across XPUs: Constraints and Acceleration for On-Robot Deployment](../Inbox/2026-04-27--characterizing-vision-language-action-models-across-xpus-constraints-and-acceleration-for-on-robot-deployment.md): XPU 表征论文报告了模型-硬件延迟、能耗、控制频率筛选、加速结果，以及一次 OpenVLA 优化后的成功率回退。
- [MotuBrain: An Advanced World Action Model for Robot Control](../Inbox/2026-04-30--motubrain-an-advanced-world-action-model-for-robot-control.md): MotuBrain 报告了一个 world-action 模型优化栈，将延迟从 4.90 s 降至 0.09 s，并把控制频率提高到 11.11 Hz。

## 带人工干预记录的部署 replay buffer
运行多台机器人的团队应为自主 rollout、失败尝试、部分进展、稀疏奖励和人工干预增加一个共享 replay buffer。数据路径需要时间戳、任务指令、相机流、机器人状态、action chunks、操作员纠正和结果标签。这是面向已部署机器人的训练工作流变更，不只是发布前的数据采集活动。

LWD 报告了这种车队规模循环：当前 checkpoints 被部署到 16 台双臂机器人，自主 rollout 和可选人工干预被加入在线 replay，单个 VLA 策略在混合离线和在线数据上重训。评估覆盖 8 个真实操作任务，包括耗时 3–5 分钟的长时程任务，并报告在数小时在线交互后达到 95% 平均成功率。论文的主要操作经验是，失败和经过纠正的部署轨迹可以成为共享策略的训练信号。

较小的实验室可以用更便宜的遥操作硬件测试日志层。Phone2Act 使用 Android 手机、ROS 2、RGB 帧、关节状态、末端执行器位姿和夹爪状态，以 LeRobot 格式记录同步演示。用 130 个采集 episode 微调 GR00T-N1.5-3B 后，在 10 次真实 Dobot CR5 试验中成功 9 次。它测得的 350–440 ms 手机到机器人延迟也给出一个提醒：在遥操作路径快到足以支持所有纠正工作流之前，记录器可能更适合用于演示采集。

### Evidence
- [Learning while Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies](../Inbox/2026-05-01--learning-while-deploying-fleet-scale-reinforcement-learning-for-generalist-robot-policies.md): LWD 报告了一个使用自主 rollout 和人工干预的车队学习循环、16 台双臂机器人、长时程任务，以及 95% 平均成功率。
- [Phone2Act: A Low-Cost, Hardware-Agnostic Teleoperation System for Scalable VLA Data Collection](../Inbox/2026-05-03--phone2act-a-low-cost-hardware-agnostic-teleoperation-system-for-scalable-vla-data-collection.md): Phone2Act 报告了一条低成本遥操作和记录路径，采用 LeRobot 格式，包含 130 个演示 episode、9/10 次真实成功，以及测得的遥操作延迟。
