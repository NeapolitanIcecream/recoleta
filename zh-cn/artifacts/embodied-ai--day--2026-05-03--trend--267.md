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

# 机器人学习论文开始检验部署细节

## Overview
这一天的机器人学习工作集中在可部署系统上。Vision-Language-Action (VLA) 策略通过真实机械手、长时程子目标、低成本数据采集和低成本硬件接受测试。DexSim2Real、Anticipation-VLA 和 Phone2Act 给出的信号最清楚：现在的成功主张取决于硬件试验、延迟、数据格式和失败检查。

## Clusters

### 灵巧操作的 sim-to-real 迁移
DexSim2Real 面向接触密集的灵巧手操作，sim-to-real 方法不使用真实演示。它用 GPT-4V 作为视觉真实度评判器，然后在光照、纹理、摩擦、质量和相机噪声上优化仿真随机化。策略还在接触过程中通过交叉注意力融合 RGB、触觉读数和本体感知。

这组材料中，它报告的硬件结果较强：在 Franka Panda 和 Allegro Hand 上完成六个真实世界任务，平均成功率为 78.2%。论文还报告平均 sim-to-real 差距为 8.3%，相比之下，普通域随机化为 28.5%，主动域随机化为 19.2%。主要价值在机制上：视觉评判器给随机化提供了可测量目标，而不只依赖人工设定的范围。

#### Evidence
- [DexSim2Real: Foundation Model-Guided Sim-to-Real Transfer for Generalizable Dexterous Manipulation](../Inbox/2026-05-03--dexsim2real-foundation-model-guided-sim-to-real-transfer-for-generalizable-dexterous-manipulation.md): 摘要给出了 FM-DR、触觉-视觉策略、渐进式课程，以及六个真实世界任务的成功率指标。

### 长时程 VLA 任务的自适应子目标
Anticipation-VLA 通过维护一组活跃目标和可达子目标来处理长任务。高层模型提出文本和图像子目标。价值模型随后检查任务状态是已达成、在改善，还是已停滞，并由这个状态控制系统继续执行、细化子目标，或弹出已完成目标。

论文报告 Libero-Long 成功率为 63.2，高于底层 pi_0.5 风格策略的 54.6，也高于 VLM 辅助版本的 53.2。在真实世界 Arx-X5 测试中，摘录给出的是相对提升，而非精确成功率：已见配置提升 +60%，未见配置提升 +107%。可用的经验偏向执行层面。长时程 VLA 执行需要依赖状态的子目标和进度检查，不能只用 rollout 开始前固定的一套流程。

#### Evidence
- [Anticipation-VLA: Solving Long-Horizon Embodied Tasks via Anticipation-based Subgoal Generation](../Inbox/2026-05-03--anticipation-vla-solving-long-horizon-embodied-tasks-via-anticipation-based-subgoal-generation.md): 摘要描述了目标栈、文本和图像子目标生成、价值模型、Libero-Long 结果，以及真实世界相对提升。

### 真实 VLA 部署中的低成本数据和硬件
两篇论文把数据采集和机器人成本视为核心研究约束。Phone2Act 把 Android 手机变成 6-DoF 遥操作器，通过 ROS 2 发送位姿事件，并直接以 LeRobot 格式记录同步机器人数据。在采集的 130 个 episode 上微调 GR00T-N1.5-3B 后，Dobot CR5 投球入篮任务 10 次试验成功 9 次，端到端延迟为 350–440 ms。

VILAS 使用 Fairino FR5 机械臂、双 RealSense 相机、遥操作，以及面向易损物体的 kirigami 软夹爪扩展，搭建了约 $8,000 的操作系统。在葡萄抓取任务上，pi_0.5 达到 84% 单次抓取成功率，GR00T N1.6 达到 58% 多次抓取成功率，并在测试模型中平均推理延迟最低。这些结果把成本、日志格式和夹爪机械结构纳入 VLA 性能主张。

#### Evidence
- [Phone2Act: A Low-Cost, Hardware-Agnostic Teleoperation System for Scalable VLA Data Collection](../Inbox/2026-05-03--phone2act-a-low-cost-hardware-agnostic-teleoperation-system-for-scalable-vla-data-collection.md): 摘要给出了 Phone2Act 架构、LeRobot 导出、数据速率、延迟，以及 90% 的真实世界微调结果。
- [VILAS: A VLA-Integrated Low-cost Architecture with Soft Grasping for Robotic Manipulation](../Inbox/2026-05-03--vilas-a-vla-integrated-low-cost-architecture-with-soft-grasping-for-robotic-manipulation.md): 摘要给出了 VILAS 硬件成本、软夹爪设计、测试的 VLA 模型、抓取成功率和延迟。

### 世界模型规划需要充分性测试和攻击测试
世界模型论文关注规划状态保留什么，以及规划器在触发条件下如何失败。Latent State Design 提出，应根据潜在状态必须支持的功能来评估世界模型：预测、控制、规划、记忆、落地，或反事实推理。它给出六种角色的分类法和七轴评估矩阵，但没有报告新的基准分数。

TRAP 给出了安全侧的对应问题。它在部署时使用视觉补丁，改变想象轨迹的排序，从而攻击世界模型规划器。在 DreamerV3 Crafter 上，它报告攻击成功率为 98.1%，平均回报下降 63.2%。在多个 DreamerV3 Atari 和 TD-MPC2 DMControl 任务上，它报告攻击成功率为 100%。两篇论文共同指出了规划控制智能体的一项具体要求：按任务评估潜在状态，然后测试规划器的轨迹排序是否会被操纵。

#### Evidence
- [Latent State Design for World Models under Sufficiency Constraints](../Inbox/2026-05-03--latent-state-design-for-world-models-under-sufficiency-constraints.md): 摘要给出了潜在状态角色、充分性关系和七轴评估矩阵。
- [TRAP: Tail-aware Ranking Attack for World-Model Planning](../Inbox/2026-05-03--trap-tail-aware-ranking-attack-for-world-model-planning.md): 摘要给出了 TRAP 的尾部感知排序攻击方法，以及报告的攻击成功率和回报下降指标。
