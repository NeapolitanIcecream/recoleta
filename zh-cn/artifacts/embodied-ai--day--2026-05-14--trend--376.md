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

# 具身 AI 论文正在检验机器人模型能否在长时程执行中保持控制

## 概览
这一窗口中的具身 AI 工作把机器人智能当作执行问题来处理。Pelican-Unified 把推理、未来视频和动作连到同一个潜在状态里。Evo-Depth 加入从 RGB 提取的深度信息，以便更快地做空间控制。LongAct 显示，家庭自主系统在长任务链上仍然会失效。

## 研究发现

### 统一的 VLA 控制与空间动作
视觉-语言-动作（VLA）模型现在被检验的是：它们的内部状态能否同时帮助动作、预测和空间定位。Pelican-Unified 通过共享的潜在状态训练语言推理、未来视频生成和机器人动作块。它在 50 个任务的 RoboTwin 双臂套件上报告了 93.5% 的平均成功率，在 WorldArena 上的 EWM Score 为 66.03。

Evo-Depth 解决的是更具体的部署瓶颈：在不增加深度硬件的情况下提高空间精度。它把从 RGB 提取的深度特征送入一个 0.9B 参数的 VLA 模型。报告的真实世界结果是，在三个任务上平均成功率为 90%，使用 3.2 GB GPU 内存，运行频率为 12.3 Hz。

#### 资料来源
- [Pelican-Unified 1.0: A Unified Embodied Intelligence Model for Understanding, Reasoning, Imagination and Action](../Inbox/2026-05-14--pelican-unified-1-0-a-unified-embodied-intelligence-model-for-understanding-reasoning-imagination-and-action.md): Pelican-Unified architecture and RoboTwin/WorldArena results
- [Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model](../Inbox/2026-05-14--evo-depth-a-lightweight-depth-enhanced-vision-language-action-model.md): Evo-Depth depth module, model size, real-world success, memory, and speed

### 滚动过程中的灵巧修正
HandITL 关注的是自主灵巧策略和人工操作员之间的交接。核心设计是相对修正：操作员在 VLA 策略继续运行的同时调整机器人手和手臂，这样在接管时不会出现突然的姿态跳变。

在接管测试中，这个效果很明显。在 Bread Clip 上，直接切换到遥操作时，平均命令变化约为 4.38e-2；HandITL 把它降到约 6.8e-5。在 Pick Up and Place the Parts 中，它在 42.8 ± 5.0 秒内完成，10 次试验里只重试 1 次。论文还报告说，在三个长时程灵巧任务上，修正回滚生成的微调数据比同等时长的标准遥操作数据平均好 19%。

#### 资料来源
- [Hand-in-the-Loop: Improving Dexterous VLA via Seamless Interventional Correction](../Inbox/2026-05-14--hand-in-the-loop-improving-dexterous-vla-via-seamless-interventional-correction.md): HandITL correction method, takeover discontinuity metrics, task timing, retry counts, and fine-tuning result

### 长时程家庭规划
LongAct 把家庭智能体的评测长度拉长了。这个基准在 100 多个 ProcTHOR 和 AI2-THOR 房子里使用 300 个 episode，开放式家务平均大约有 9 个目标，步数上限是 16,000。这套设置检验的是跨房间、跨物体的记忆、依赖跟踪和恢复能力。

结果显示，目标推进和完整完成之间差距很大。纯 Qwen3-VL-32B 的 Goal-Condition Success 只有 6.14%，Success Rate 为 0%。带有 Qwen3-VL-32B 的 HoloMind 把这两个指标提升到 51.2% 和 15.0%。报告中的最佳 HoloMind 变体使用 GPT-5，Goal-Condition Success 为 59.0%，Success Rate 为 16.0%，而人类的目标完成率为 93%。

#### 资料来源
- [When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution](../Inbox/2026-05-14--when-robots-do-the-chores-a-benchmark-and-agent-for-long-horizon-household-task-execution.md): LongAct benchmark design, HoloMind components, and detailed split results

### 世界模型接受物理测试
这一窗口中的世界模型论文增加了对几何、物体状态和可执行动力学的显式检查。PDI-Bench 按照尺度-深度对齐、3D 轨迹一致性和结构刚性来给生成视频打分。真实视频的 PDI 为 0.1206；列出的最佳生成模型 Seedance 2.0 得分为 0.2422。Sora 和 HunyuanVideo 的尺度残差大得多，比真实视频的尺度残差高出 25 倍以上。

还有两篇规划论文指向面向动作的世界模型。Slot-MPC 使用物体槽和可微的动作条件动力学模型做目标图像操控；它报告的潜在大小比基于 patch 的 DINO-WM 小 99%。Coding Agent Is Good As World Simulator 通过编写和修复代码来搭建 PyChrono 仿真；它在三个报告任务上达到了 100% 的 Pass@1 计划生成率，但有代表性的成功运行会消耗数百万 token。

#### 资料来源
- [Quantitative Video World Model Evaluation for Geometric-Consistency](../Inbox/2026-05-14--quantitative-video-world-model-evaluation-for-geometric-consistency.md): PDI-Bench metric definition, dataset size, model rankings, and scale-error findings
- [Slot-MPC: Goal-Conditioned Model Predictive Control with Object-Centric Representations](../Inbox/2026-05-14--slot-mpc-goal-conditioned-model-predictive-control-with-object-centric-representations.md): Slot-MPC object-centric planning method and latent-size reduction claim
- [Coding Agent Is Good As World Simulator](../Inbox/2026-05-14--coding-agent-is-good-as-world-simulator.md): Code-based simulator construction, pass rates, runtime, token use, and WorldModelBench results
