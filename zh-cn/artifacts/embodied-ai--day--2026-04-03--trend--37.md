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

# 具身控制论文正在修复动作、规划和迁移中的具体瓶颈

## 概览
这一天最强的是把具体失效点封住的具身控制工作。证据集中在动作瓶颈、层级规划、预测视频控制和 sim-to-real 迁移。和前几天相比，这些工作更少在泛泛地诊断风险，而是直接在机器人和驾驶任务上展示可量化的控制指标提升。

## 研究发现

### Control quality now depends on the action interface as much as the perception stack
机器人控制论文现在更明确地指出动作质量在哪些地方丢失，以及如何修复。最清楚的证据来自两个方向。一篇论文显示，当动作被压缩成离散 token 时，更好的视觉编码器并不一定能稳定提升 vision-language-action 策略。在 LIBERO-10 上，Diffusion Policy 在 M 规模下从 36.4% 升到 57.6%，方法是把编码器从 ResNet-18 升级到 SigLIP；OAT 则从 53.8% 升到 57.4%。另一篇论文通过把规划拆成潜变量宏动作和低层动作，提升了长时域世界模型控制。HWM 把真实 Franka 抓取放置成功率从 0% 提高到 70%，把抽屉任务从 30% 提高到 70%，同一报告里还给出了更低的规划成本说法。

#### 资料来源
- [The Compression Gap: Why Discrete Tokenization Limits Vision-Language-Action Model Scaling](../Inbox/2026-04-03--the-compression-gap-why-discrete-tokenization-limits-vision-language-action-model-scaling.md): Compression Gap results on encoder scaling versus discrete action bottlenecks.
- [Hierarchical Planning with Latent World Models](../Inbox/2026-04-03--hierarchical-planning-with-latent-world-models.md): HWM results on hierarchical latent planning for long-horizon control.

### Video prediction is being used as an action model for manipulation
低数据量操作任务现在更多依赖可预测的视频结构，而不只是静态图像特征。MV-VDP 同时预测未来的多视角 RGB 视频和动作热力图，然后把热力图回投到 3D 动作估计中。在 Meta-World 里，每个任务只有 5 个示范时，它的平均成功率达到 89.1%，高于 Track2Act 的 67.4% 和 DreamZero 的 61.1%。真实机器人表格更小，也更不完整，但结果仍然具体：Put Lion 是 10/10，Scoop Tortilla 是 7/10，Push-T 是 4/10，列出的基线分数更低。这个模式说明，场景动态和 3D 一致性正在直接被训练进策略输出。

#### 资料来源
- [Multi-View Video Diffusion Policy: A 3D Spatio-Temporal-Aware Video Action Model](../Inbox/2026-04-03--multi-view-video-diffusion-policy-a-3d-spatio-temporal-aware-video-action-model.md): MV-VDP method and benchmark results for low-data manipulation.

### Sim-to-real work is targeting the observation-action mismatch directly
这一时期的 sim-to-real 论文把重点放在部署时保住控制语义。对四足机器人，DreamTIP 给 Dreamer 世界模型加入了任务不变属性，例如接触稳定性和地形间隙。它报告了在 8 个模拟迁移任务上的 28.1% 平均提升，以及 Unitree Go2 上的明显真实世界收益，包括 Climb 52 cm 任务从 WMP 的 10% 提高到 100%。在驾驶上，Sim2Real-AD 把迁移拆成观测桥接和动作重映射。它在 Ford E-Transit 上的零样本真实车辆结果是：跟车 90%，避障 80%，识别停车标志交互 75%，报告设置里没有真实世界 RL 训练数据。

#### 资料来源
- [Learning Task-Invariant Properties via Dreamer: Enabling Efficient Policy Transfer for Quadruped Robots](../Inbox/2026-04-03--learning-task-invariant-properties-via-dreamer-enabling-efficient-policy-transfer-for-quadruped-robots.md): DreamTIP sim-to-real transfer results on quadruped locomotion.
- [Sim2Real-AD: A Modular Sim-to-Real Framework for Deploying VLM-Guided Reinforcement Learning in Real-World Autonomous Driving](../Inbox/2026-04-03--sim2real-ad-a-modular-sim-to-real-framework-for-deploying-vlm-guided-reinforcement-learning-in-real-world-autonomous-driving.md): Sim2Real-AD zero-shot real-vehicle deployment results.

### VLA inference is being trimmed with online verification
VLA 效率工作现在更精确地控制大模型什么时候需要运行。SV-VLA 保留一个用于动作块的重型规划器，再加一个小型验证器，用当前观测检查每一步。在 LIBERO 上，它报告在三个子任务上的平均提升，从开环基线的 79.5% 提高到 90.90%。这段证据比机器人规划论文更窄，因为摘录里没有逐任务分数或延迟表，但方法很清楚：先分块，在线验证，只有当前状态和计划动作不一致时才重新规划。

#### 资料来源
- [Open-Loop Planning, Closed-Loop Verification: Speculative Verification for VLA](../Inbox/2026-04-03--open-loop-planning-closed-loop-verification-speculative-verification-for-vla.md): SV-VLA speculative verification setup and headline LIBERO result.
