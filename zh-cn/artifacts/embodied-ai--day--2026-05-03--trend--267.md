---
kind: trend
trend_doc_id: 267
granularity: day
period_start: '2026-05-03T00:00:00'
period_end: '2026-05-04T00:00:00'
topics:
- robot learning
- VLA
- sim-to-real
- teleoperation
- world models
- planning security
run_id: materialize-outputs
aliases:
- recoleta-trend-267
tags:
- recoleta/trend
- topic/robot-learning
- topic/vla
- topic/sim-to-real
- topic/teleoperation
- topic/world-models
- topic/planning-security
language_code: zh-CN
---

# 机器人学习论文把部署细节纳入测试

## 概览
这一天的机器人学习工作都围绕可部署系统展开。视觉-语言-动作（VLA）策略在真实手部、长时序子目标、低成本数据采集和低价硬件上接受测试。DexSim2Real、Anticipation-VLA 和 Phone2Act 给出的信号最清楚：成功率主张现在取决于硬件试验、延迟、数据格式和失败检查。

## 研究发现

### Dexterous sim-to-real transfer
DexSim2Real 面向无需真实示范的 sim-to-real 方法下的高接触手部操作。它把 GPT-4V 用作视觉真实性评审器，然后围绕光照、纹理、摩擦、质量和相机噪声优化仿真随机化。该策略还在接触过程中通过交叉注意力融合 RGB、触觉读数和本体感觉。

这篇论文报告的硬件结果在这个语料里很强：在 Franka Panda 搭配 Allegro Hand 的 6 个真实世界任务上，平均成功率为 78.2%。论文还报告了 8.3% 的平均 sim-to-real gap，而基础 domain randomization 为 28.5%，active domain randomization 为 19.2%。最有价值的是这一机制，因为视觉评审器给随机化提供了可测目标，而不是只依赖人工设定的范围。

#### 资料来源
- [DexSim2Real: Foundation Model-Guided Sim-to-Real Transfer for Generalizable Dexterous Manipulation](../Inbox/2026-05-03--dexsim2real-foundation-model-guided-sim-to-real-transfer-for-generalizable-dexterous-manipulation.md): Summary gives the FM-DR, tactile-visual policy, progressive curriculum, and six-task real-world success metrics.

### Adaptive subgoals for long-horizon VLA tasks
Anticipation-VLA 通过维护一个由当前目标和可达子目标组成的栈来应对长任务。高层模型提出文本和图像子目标。然后一个 value model 检查任务是已完成、在改善还是停滞，并由这个状态控制系统继续执行、细化子目标，还是弹出已完成目标。

论文在 Libero-Long 上报告了 63.2 的成功率，超过底层的 pi_0.5 风格策略的 54.6，也高于一个带 VLM 的版本的 53.2。在真实世界的 Arx-X5 测试中，摘要给出的是相对提升而不是精确成功率：已见配置提升 +60%，未见配置提升 +107%。这里的可操作结论很直接。长时序 VLA 执行需要依赖状态的子目标和进度检查，而不是在 rollout 开始前就固定一套流程。

#### 资料来源
- [Anticipation-VLA: Solving Long-Horizon Embodied Tasks via Anticipation-based Subgoal Generation](../Inbox/2026-05-03--anticipation-vla-solving-long-horizon-embodied-tasks-via-anticipation-based-subgoal-generation.md): Summary describes the goal stack, text-and-image subgoal generation, value model, Libero-Long result, and real-world relative gains.

### Low-cost data and hardware for real VLA deployment
两篇论文把数据采集和机器人成本当作核心研究约束。Phone2Act 把 Android 手机变成一个 6-DoF 远程操作器，通过 ROS 2 发送姿态事件，并直接以 LeRobot 格式记录同步机器人数据。用 130 个采集到的 episode 对 GR00T-N1.5-3B 进行微调后，在 Dobot CR5 的球入篮任务上 10 次试验成功 9 次，端到端延迟为 350–440 ms。

VILAS 用 Fairino FR5 机械臂、双 RealSense 相机、远程操作和用于脆弱物体的 kirigami 软夹爪扩展，搭建了一个大约 8,000 美元的操作系统。在葡萄抓取上，pi_0.5 的单次抓取成功率达到 84%，而 GR00T N1.6 的多次抓取成功率达到 58%，并且在测试模型里平均推理延迟最低。这些结果把成本、日志格式和夹爪机制都纳入了 VLA 性能主张。

#### 资料来源
- [Phone2Act: A Low-Cost, Hardware-Agnostic Teleoperation System for Scalable VLA Data Collection](../Inbox/2026-05-03--phone2act-a-low-cost-hardware-agnostic-teleoperation-system-for-scalable-vla-data-collection.md): Summary gives Phone2Act architecture, LeRobot export, data rate, latency, and 90% real-world fine-tuning result.
- [VILAS: A VLA-Integrated Low-cost Architecture with Soft Grasping for Robotic Manipulation](../Inbox/2026-05-03--vilas-a-vla-integrated-low-cost-architecture-with-soft-grasping-for-robotic-manipulation.md): Summary gives VILAS hardware cost, soft gripper design, tested VLA models, grasp success rates, and latency.

### World-model planning needs sufficiency tests and attack tests
世界模型论文关注的是规划状态保留了什么，以及规划器在触发条件下如何失败。Latent State Design 提议按潜在状态必须支持的功能来评价世界模型：预测、控制、规划、记忆、grounding 或反事实推理。它给出一个六角色分类法和一个七轴评估矩阵，但没有报告新的基准分数。

TRAP 提供了安全侧的对应问题。它通过一个部署时视觉 patch 改变想象轨迹的排序，从而攻击世界模型规划器。在 DreamerV3 Crafter 上，它报告了 98.1% 的攻击成功率和 63.2% 的平均回报下降。在若干 DreamerV3 Atari 和 TD-MPC2 DMControl 任务上，它报告了 100% 的攻击成功率。两篇论文放在一起，给 planned-control agent 提出一个明确要求：先针对任务评估潜在状态，再测试规划器的轨迹排序是否能被操控。

#### 资料来源
- [Latent State Design for World Models under Sufficiency Constraints](../Inbox/2026-05-03--latent-state-design-for-world-models-under-sufficiency-constraints.md): Summary gives the latent-state roles, sufficiency relationships, and seven-axis evaluation matrix.
- [TRAP: Tail-aware Ranking Attack for World-Model Planning](../Inbox/2026-05-03--trap-tail-aware-ranking-attack-for-world-model-planning.md): Summary gives TRAP’s tail-aware ranking attack method and reported attack success and return-drop metrics.
