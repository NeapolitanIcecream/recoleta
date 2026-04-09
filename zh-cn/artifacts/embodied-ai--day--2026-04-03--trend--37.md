---
kind: trend
trend_doc_id: 37
granularity: day
period_start: '2026-04-03T00:00:00'
period_end: '2026-04-04T00:00:00'
topics:
- embodied-control
- robotics
- world-models
- vision-language-action
- sim-to-real
run_id: materialize-outputs
aliases:
- recoleta-trend-37
tags:
- recoleta/trend
- topic/embodied-control
- topic/robotics
- topic/world-models
- topic/vision-language-action
- topic/sim-to-real
language_code: zh-CN
---

# 具身控制论文正在修补动作、规划和迁移中的具体瓶颈

## Overview
这一天最强的一组工作集中在 embodied control，并且都在补具体的失效点。证据主要围绕动作瓶颈、分层规划、预测式视频控制和 sim-to-real 迁移。和前几天相比，这批工作更少停留在一般性的风险诊断上，更多是在机器人和驾驶任务中用直接控制指标展示具体提升。

## Clusters

### 控制质量现在和动作接口一样依赖感知栈
机器人控制论文越来越明确地指出动作质量会在哪些环节损失，以及如何补回来。最清楚的证据来自两个方向。一篇论文表明，当动作被压缩成离散 token 时，更强的视觉编码器并不能稳定提升 vision-language-action 策略。在 LIBERO-10 上，尺寸为 M 时，Diffusion Policy 从 36.4% 提升到 57.6%（ResNet-18 升级到 SigLIP），而 OAT 只从 53.8% 提升到 57.4%。另一篇论文通过把规划拆成潜在宏动作和低层动作，提升了长时程 world-model 控制。HWM 将真实 Franka 抓取放置任务的成功率从 0% 提高到 70%，抽屉任务从 30% 提高到 70%；同一篇报告还称规划成本更低。

#### Evidence
- [The Compression Gap: Why Discrete Tokenization Limits Vision-Language-Action Model Scaling](../Inbox/2026-04-03--the-compression-gap-why-discrete-tokenization-limits-vision-language-action-model-scaling.md): Compression Gap 关于编码器扩展与离散动作瓶颈的结果。
- [Hierarchical Planning with Latent World Models](../Inbox/2026-04-03--hierarchical-planning-with-latent-world-models.md): HWM 在长时程控制分层潜在规划上的结果。

### 视频预测正被用作操作任务的动作模型
低数据操作方向越来越依赖预测式视频结构，而不只是静态图像特征。MV-VDP 同时预测未来的多视角 RGB 视频和动作热力图，再把热力图还原成 3D 动作估计。在 Meta-World 中，每个任务 5 个示范时，它的平均成功率达到 89.1%，高于 Track2Act 的 67.4% 和 DreamZero 的 61.1%。真实机器人结果表更小、表现也有差异，但数据仍然具体：Put Lion 为 10/10，Scoop Tortilla 为 7/10，Push-T 为 4/10，列出的基线分数更低。这个模式说明，场景动态和 3D 一致性正在被直接训练进策略输出。

#### Evidence
- [Multi-View Video Diffusion Policy: A 3D Spatio-Temporal-Aware Video Action Model](../Inbox/2026-04-03--multi-view-video-diffusion-policy-a-3d-spatio-temporal-aware-video-action-model.md): MV-VDP 在低数据操作上的方法和基准结果。

### Sim-to-real 工作在直接处理观测-动作失配
这一时期的 sim-to-real 论文把重点放在部署时保留控制语义。对四足机器人，DreamTIP 把接触稳定性、地形离地间隙等任务不变属性加入 Dreamer world model。它报告在 8 个模拟迁移任务上平均提升 28.1%，并且在 Unitree Go2 上也有明显的真实世界增益，其中 Climb 52 cm 从 WMP 的 10% 提高到 100%。在自动驾驶中，Sim2Real-AD 把迁移拆成观测桥接和动作重映射。按文中设定，它在 Ford E-Transit 真车上的零样本结果是：跟车 90%，避障 80%，停车标志交互 75%，且没有使用真实世界 RL 训练数据。

#### Evidence
- [Learning Task-Invariant Properties via Dreamer: Enabling Efficient Policy Transfer for Quadruped Robots](../Inbox/2026-04-03--learning-task-invariant-properties-via-dreamer-enabling-efficient-policy-transfer-for-quadruped-robots.md): DreamTIP 在四足运动上的 sim-to-real 迁移结果。
- [Sim2Real-AD: A Modular Sim-to-Real Framework for Deploying VLM-Guided Reinforcement Learning in Real-World Autonomous Driving](../Inbox/2026-04-03--sim2real-ad-a-modular-sim-to-real-framework-for-deploying-vlm-guided-reinforcement-learning-in-real-world-autonomous-driving.md): Sim2Real-AD 的零样本真车部署结果。

### VLA 推理正通过在线验证来压缩开销
VLA 效率方向越来越细化地处理大模型该在何时运行。SV-VLA 保留一个较重的规划器来生成动作块，再加上一个小型验证器，在每一步根据当前观测做检查。在 LIBERO 上，相比开环基线，它在三个子任务上的平均成绩从 79.5% 提高到 90.90%。这部分证据比机器人规划论文更窄，因为摘录里没有给出单任务分数或延迟表，但方法本身很清楚：先分块规划，在线验证，只有当前状态与计划动作不一致时才重新规划。

#### Evidence
- [Open-Loop Planning, Closed-Loop Verification: Speculative Verification for VLA](../Inbox/2026-04-03--open-loop-planning-closed-loop-verification-speculative-verification-for-vla.md): SV-VLA 的推测式验证设定和 LIBERO 主要结果。
