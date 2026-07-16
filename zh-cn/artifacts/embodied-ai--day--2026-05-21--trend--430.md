---
kind: trend
trend_doc_id: 430
granularity: day
period_start: '2026-05-21T00:00:00'
period_end: '2026-05-22T00:00:00'
topics:
- vision-language-action
- robot manipulation
- spatial grounding
- runtime verification
- world models
- autonomous driving
run_id: materialize-outputs
aliases:
- recoleta-trend-430
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/spatial-grounding
- topic/runtime-verification
- topic/world-models
- topic/autonomous-driving
language_code: zh-CN
---

# VLA 工作现在用落地、记忆和动作检查来判断策略

## 概览
视觉-语言-动作（VLA）研究主导了这个时间段。CrossVLA、AVP 和 SOMA 说明了当前重点：策略质量正在通过后训练收益、显式空间落地、持续记忆、延迟和闭环执行结果来衡量。

## 研究发现

### 显式空间落地用于操作
一些机器人论文在语言和运动控制之间加入中间目标信号。AVP 让视觉-语言模型先输出视觉原语，再做动作预测，然后把这些 token 送入一个 flow-matching 动作专家。在中国象棋操作上，它报告的平均成功率为 90.28%，高于 π₀.₅ 的 62.67%，每条指令耗时 0.27 秒。

GesVLA 处理的是另一种歧义来源：人的指向。它把手腕和食指关键点转成手势 token，并与语言和场景感知结合。在三个真实机器人任务上，成功率达到 83.3%，高于仅文本 VLA 的 31.7%。SOMA 为当前摄像头视野之外的物体加入持续空间记忆，使用头部摄像头扫描和带语义及三维位置信息的记忆 token。它在成功率上的提升没那么大，但减少了视野外任务中的目标搜索时间和抓取尝试次数。

#### 资料来源
- [Action with Visual Primitives](../Inbox/2026-05-21--action-with-visual-primitives.md): AVP architecture and real-robot success, latency, and ablation results.
- [GesVLA: Gesture-Aware Vision-Language-Action Model Embedded Representations](../Inbox/2026-05-21--gesvla-gesture-aware-vision-language-action-model-embedded-representations.md): GesVLA gesture-token design and real-robot success rates.
- [Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action](../Inbox/2026-05-21--spatial-memory-for-out-of-vision-manipulation-in-vision-language-action.md): SOMA spatial memory method and out-of-vision manipulation results.

### 动作系统中的场景状态与潜在未来
另一组工作关注策略在首次观测之后使用的状态。EvoScene-VLA 在控制调用之间保留一个循环更新的场景前缀，并随动作块预测未来场景 token。在 31 个 RoboTwin 任务上，它把固定场景下的平均成功率提高到 89.1%，随机布局下提高到 88.5%。

LVDrive 把类似思路用于仅摄像头自动驾驶。它在潜在空间里预测未来场景特征，并用这些特征修正轨迹，在 Bench2Drive 上达到 80.71 Driving Score 和 58.26% Success Rate。TRM 论文展示了一个相关的规划问题：潜在世界模型可能包含正确状态，但终端代价会把候选项排得很差。把原始潜在距离换成学习到的可达性度量后，LeWM 在 hard TwoRoom 上的成功率从 7.0% 提升到 97.0%。

#### 资料来源
- [EvoScene-VLA: Evolving Scene Beliefs Inside the Action Decoder for Chunked Robot Control](../Inbox/2026-05-21--evoscene-vla-evolving-scene-beliefs-inside-the-action-decoder-for-chunked-robot-control.md): EvoScene-VLA recurrent scene prefix and RoboTwin success results.
- [LVDrive: Latent Visual Representation Enhanced Vision-Language-Action Autonomous Driving Model](../Inbox/2026-05-21--lvdrive-latent-visual-representation-enhanced-vision-language-action-autonomous-driving-model.md): LVDrive latent future prediction method and Bench2Drive metrics.
- [Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics](../Inbox/2026-05-21--beyond-euclidean-proximity-repairing-latent-world-models-with-horizon-matched-trajectory-reachability-metrics.md): TRM learned reachability metric and TwoRoom planning gains.

### 后训练与动作验证
CrossVLA 把 VLA 适配当作一个经验系统问题。它把 Direct Preference Optimization (DPO) 同时用于自回归动作 token 策略和 flow-matching 连续动作策略。在 OpenVLA 上、覆盖 LIBERO 的四个套件时，DoRA+DPO 的平均成功率达到 73.2%，高于监督微调的 62.75%。它的延迟拆分也很关键：π₀.₅ 把大约 78.6% 的 sample-actions 时间花在去噪循环里，所以前缀 key-value 缓存并不是好目标。

Pre-VLA 在执行或世界模型 rollout 之前加入运行时检查器。它为候选动作块预测动作有效性和 critic 推导的优势。在 LIBERO 上，它报告 0.9542 的有效性准确率，并把 RynnVLA-002 的平均闭环成功率从 30.79% 提高到 37.62%，每个动作块验证耗时 183.9 ms。

#### 资料来源
- [CrossVLA: Cross-Paradigm Post-Training and Inference Optimization for Vision-Language-Action Models](../Inbox/2026-05-21--crossvla-cross-paradigm-post-training-and-inference-optimization-for-vision-language-action-models.md): CrossVLA DPO results, latency analysis, and caching negative result.
- [Pre-VLA: Preemptive Runtime Verification for Reliable Vision-Language-Action and World-Model Rollouts](../Inbox/2026-05-21--pre-vla-preemptive-runtime-verification-for-reliable-vision-language-action-and-world-model-rollouts.md): Pre-VLA runtime verification method, LIBERO accuracy, success, and latency.

### 安全关键型 VLA 仍以提案为主，而非证据
端到端手术助手论文把 VLA 推理扩展到高风险场景，但它的证据来自架构和临床设想，而不是实验。它定义了一个 2–3 级自主助手，可以生成选项、监控手术场景，并在外科医生授权下执行受限的低层动作。这个拟议系统把内窥镜视频与术前和术中信号融合在一起，包括 CT/MRI 先验、超声、OCT、跟踪和力的代理信号。

这篇论文更像一份需求说明。它列出了牵拉、分离、止血、烟雾响应和出血点定位等具体子任务，还设定了亚秒级响应目标。它没有报告基准、运行时测量、临床试验或成功率，因此应把它看作未来 VLA 工作的安全规范，而不是已经部署的结果。

#### 资料来源
- [How can reasoning capability empower the AI copilot robot in endoscopic surgery](../Inbox/2026-05-21--how-can-reasoning-capability-empower-the-ai-copilot-robot-in-endoscopic-surgery.md): Surgical copilot autonomy level, proposed VLA design, use cases, and lack of quantitative results.
