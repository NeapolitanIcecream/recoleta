---
kind: trend
trend_doc_id: 376
granularity: day
period_start: '2026-05-14T00:00:00'
period_end: '2026-05-15T00:00:00'
topics:
- embodied AI
- robotics
- VLA
- world models
- long-horizon planning
- video evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-376
tags:
- recoleta/trend
- topic/embodied-ai
- topic/robotics
- topic/vla
- topic/world-models
- topic/long-horizon-planning
- topic/video-evaluation
language_code: zh-CN
---

# 具身 AI 论文正在测试机器人模型能否在长时间执行中保持控制

## Overview
这一窗口的具身 AI 工作把机器人智能视为执行问题。Pelican-Unified 在一个潜在状态中连接推理、未来视频和动作。Evo-Depth 加入 RGB 推导的深度，以实现更快的空间控制。LongAct 显示，家庭自主系统在长任务链下仍会失效。

## Clusters

### 统一的 VLA 控制与空间动作
Vision-Language-Action（VLA）模型正在被用同一个标准评估：其内部状态能否同时帮助动作、预测和空间放置。Pelican-Unified 通过共享潜在状态训练语言推理、未来视频生成和机器人动作块。它在 50 项任务的 RoboTwin 双臂套件上报告 93.5% 的平均成功率，在 WorldArena 上报告 66.03 的 EWM Score。

Evo-Depth 处理的是更窄的部署瓶颈：不增加深度硬件的空间精度。它用 RGB 推导出的深度特征输入一个 0.9B 参数的 VLA 模型。报告的真实世界结果是在三项任务上达到 90% 的平均成功率，使用 3.2 GB GPU 内存，并以 12.3 Hz 运行。

#### Evidence
- [Pelican-Unified 1.0: A Unified Embodied Intelligence Model for Understanding, Reasoning, Imagination and Action](../Inbox/2026-05-14--pelican-unified-1-0-a-unified-embodied-intelligence-model-for-understanding-reasoning-imagination-and-action.md): Pelican-Unified 架构和 RoboTwin/WorldArena 结果
- [Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model](../Inbox/2026-05-14--evo-depth-a-lightweight-depth-enhanced-vision-language-action-model.md): Evo-Depth 深度模块、模型规模、真实世界成功率、内存和速度

### Rollout 期间的灵巧校正
HandITL 关注自主灵巧策略与人类操作员之间的接管。关键设计是相对校正：操作员调整机器人手和手臂，同时 VLA 策略继续运行，这避免了接管时姿态突然跳变。

接管测试中的测量效果很大。在 Bread Clip 上，直接切换到遥操作导致平均命令变化约为 4.38e-2；HandITL 将其降至约 6.8e-5。在 Pick Up and Place the Parts 中，它用 42.8 ± 5.0 秒完成任务，并在 10 次试验中重试 1 次。论文还报告，在三个长时程灵巧任务上，校正 rollout 产生的微调数据平均比等时长标准遥操作数据好 19%。

#### Evidence
- [Hand-in-the-Loop: Improving Dexterous VLA via Seamless Interventional Correction](../Inbox/2026-05-14--hand-in-the-loop-improving-dexterous-vla-via-seamless-interventional-correction.md): HandITL 校正方法、接管不连续性指标、任务用时、重试次数和微调结果

### 长时程家务规划
LongAct 拉长了家庭智能体的评估长度。该基准在 100 多个 ProcTHOR 和 AI2-THOR 房屋中使用 300 个 episode，自由形式家务平均约有 9 个目标，并设置 16,000 步上限。这个设置测试跨房间和物体的记忆、依赖跟踪和恢复能力。

结果显示，目标进展与完整完成之间差距很大。纯 Qwen3-VL-32B 达到 6.14% Goal-Condition Success 和 0% Success Rate。使用 Qwen3-VL-32B 的 HoloMind 达到 51.2% Goal-Condition Success 和 15.0% Success Rate。报告中最好的 HoloMind 变体使用 GPT-5，达到 59.0% Goal-Condition Success 和 16.0% Success Rate，而人类目标完成率报告为 93%。

#### Evidence
- [When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution](../Inbox/2026-05-14--when-robots-do-the-chores-a-benchmark-and-agent-for-long-horizon-household-task-execution.md): LongAct 基准设计、HoloMind 组件和详细划分结果

### 世界模型接受物理测试
这一窗口中的世界模型论文加入了对几何、物体状态和可执行动力学的显式检查。PDI-Bench 按尺度-深度对齐、3D 轨迹一致性和结构刚性为生成视频打分。真实视频的 PDI 为 0.1206；列出的最佳生成模型 Seedance 2.0 得分 0.2422。Sora 和 HunyuanVideo 显示出大得多的尺度残差，超过真实尺度残差的 25 倍。

两篇规划论文指向面向动作的世界模型。Slot-MPC 使用物体 slot 和可微的动作条件动力学模型来做目标图像操控；报告称，与基于 patch 的 DINO-WM 相比，其潜在大小减少 99%。Coding Agent Is Good As World Simulator 通过编写和修复代码来构建 PyChrono 仿真；它在报告的三项任务上达到 100% Pass@1 计划生成率，但代表性的成功运行会消耗数百万 token。

#### Evidence
- [Quantitative Video World Model Evaluation for Geometric-Consistency](../Inbox/2026-05-14--quantitative-video-world-model-evaluation-for-geometric-consistency.md): PDI-Bench 指标定义、数据集规模、模型排名和尺度误差发现
- [Slot-MPC: Goal-Conditioned Model Predictive Control with Object-Centric Representations](../Inbox/2026-05-14--slot-mpc-goal-conditioned-model-predictive-control-with-object-centric-representations.md): Slot-MPC 以物体为中心的规划方法和潜在大小减少声明
- [Coding Agent Is Good As World Simulator](../Inbox/2026-05-14--coding-agent-is-good-as-world-simulator.md): 基于代码的仿真器构建、通过率、运行时间、token 使用和 WorldModelBench 结果
