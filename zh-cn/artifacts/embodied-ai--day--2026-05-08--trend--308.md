---
kind: trend
trend_doc_id: 308
granularity: day
period_start: '2026-05-08T00:00:00'
period_end: '2026-05-09T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- tactile control
- federated learning
- policy adaptation
run_id: materialize-outputs
aliases:
- recoleta-trend-308
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/tactile-control
- topic/federated-learning
- topic/policy-adaptation
language_code: zh-CN
---

# 机器人 VLA 论文正在优化可部署的前瞻能力

## 概览
这段时间窗口里的机器人论文把 Vision-Language-Action（VLA）策略当作可部署的控制系统来处理。紧凑的世界状态、接触反馈、失败数据和低预算适配都接受了具体测试。OneWM-VLA、AT-VLA 和 ForgeVLA 给出了最清楚的量化信号。

## 研究发现

### Compact and plannable world models
世界模型研究聚焦于更小的潜在状态和更好的规划信号。OneWM-VLA 将每个相机视图和每一帧压缩成一个语义 token，然后把未来潜在 token 和动作块一起生成。它报告在 MetaWorld 上平均成功率为 61.3%，高于 π0 的 47.9%；在 LIBERO 上平均成功率为 98.1%；在真实 Piper 机械臂、清洁条件下成功率为 71.7%，高于 π0 的 50.0%。

RLA-WM 使用 Residual Latent Action（RLA），这是一个描述 DINO 特征变化的紧凑编码。它以每次推理 3.5T FLOPs 预测未来视觉特征，并在 ManiSkill 和 IWS 的预测指标上优于列出的 feature 和 flow 基线。RC-aux 给潜在世界模型加入可达性监督，说明准确的短期预测仍然可能误导规划器。在 Wall 任务上，它把成功率提升到 83.6 ± 3.6，而 LeWM 对照组是 50.4 ± 6.5。

#### 资料来源
- [One Token Per Frame: Reconsidering Visual Bandwidth in World Models for VLA Policy](../Inbox/2026-05-08--one-token-per-frame-reconsidering-visual-bandwidth-in-world-models-for-vla-policy.md): OneWM-VLA compression design and success-rate results across MetaWorld, LIBERO, and real Piper tasks.
- [Learning Visual Feature-Based World Models via Residual Latent Action](../Inbox/2026-05-08--learning-visual-feature-based-world-models-via-residual-latent-action.md): RLA-WM residual latent action design, prediction metrics, and compute comparison.
- [Predictive but Not Plannable: RC-aux for Latent World Models](../Inbox/2026-05-08--predictive-but-not-plannable-rc-aux-for-latent-world-models.md): RC-aux reachability training and goal-conditioned control gains.

### Contact and failure signals for VLA control
有些论文加入只在执行时出现的反馈通道。AT-VLA 增加了触觉门控和双流结构：较慢的视觉-语言推理，加上更快的触觉修正。论文报告闭环触觉响应时间为 0.04 秒。在真实机器人接触密集任务中，AT-VLA 将 Unzip Bag 的成功率提高到 0.33，而 GO-1 是 0.20，π0.5 是 0.00；Wipe Vase 提高到 0.67，而前两者分别是 0.07 和 0.33。

AFIL 用失败 rollout 作为扩散和 flow 型 VLA 策略的负向引导。它训练分开的成功动作生成器和失败动作生成器，同时共享一个视觉-语言骨干。现有摘要没有表格数值，所以这里能确定的是架构层面的结论：失败数据变成了在线训练信号和采样时的排斥项。

#### 资料来源
- [AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models](../Inbox/2026-05-08--at-vla-adaptive-tactile-injection-for-enhanced-feedback-reaction-in-vision-language-action-models.md): AT-VLA tactile gating, dual-stream design, reaction time, and real-robot success rates.
- [Failing Forward: Adaptive Failure-Informed Learning for Vision-Language-Action Models](../Inbox/2026-05-08--failing-forward-adaptive-failure-informed-learning-for-vision-language-action-models.md): AFIL failure-rollout collection, dual action generators, and adaptive negative guidance.

### Data-constrained VLA training
这些训练论文关注的是私有、稀疏或特定领域的数据。ForgeVLA 在分布式视觉-动作日志上训练，不集中原始数据，也不添加人工语言标注。每个客户端在本地分配伪指令，随后由对比式规划损失和服务器聚合来处理非独立同分布的机器人数据。在 LIBERO-Goal 上，它达到 55.2% 的成功率和 100% 的 Pass@50，而 FedAvg 分别是 28.8% 和 80%。

ACA 通过在选定锚点条件下重复演示，然后收集策略偏离的边界数据，来应对小规模真实机器人适配预算。在 Franka Panda 设置下使用 100 条轨迹时，π0.5 加 ACA 的平均成功率达到 72.5%，而 π0.5 自身是 31.7%。BioProVLA-Agent 把同样的部署压力带到湿实验室：它把生物协议解析成已验证子任务，在动作前后做视觉检查，并运行在一个报告为 800–850 美元的硬件平台上，不过摘录没有给出精确成功率。

#### 资料来源
- [ForgeVLA: Federated Vision-Language-Action Learning without Language Annotations](../Inbox/2026-05-08--forgevla-federated-vision-language-action-learning-without-language-annotations.md): ForgeVLA federated training design and LIBERO results.
- [Escaping the Diversity Trap in Robotic Manipulation via Anchor-Centric Adaptation](../Inbox/2026-05-08--escaping-the-diversity-trap-in-robotic-manipulation-via-anchor-centric-adaptation.md): Anchor-Centric Adaptation method and real-robot success gains under limited demonstrations.
- [BioProVLA-Agent: An Affordable, Protocol-Driven, Vision-Enhanced VLA-Enabled Embodied Multi-Agent System with Closed-Loop-Capable Reasoning for Biological Laboratory Manipulation](../Inbox/2026-05-08--bioprovla-agent-an-affordable-protocol-driven-vision-enhanced-vla-enabled-embodied-multi-agent-system-with-closed-loop-capable-reasoning-for-biological-laboratory-manipulation.md): BioProVLA-Agent protocol parsing, verification loop, low-cost platform, and benchmark scope.

### Physical consistency as a world-model criterion
LaWM 和 Sword 把 rollout 质量当作控制要求。LaWM 通过学习到的最小作用量目标和展开求解器来定义下一个潜在状态。它最强的结果出现在受控物理运动上：PIS-vx 达到 0.9938 ± 0.0045，速度一致性 PIS-ax 达到 0.8964 ± 0.0275，高于 NewtonGen 的 0.6568 ± 0.013。

Sword 为带视觉风格变化的 LIBERO rollout 训练动作条件世界模型。Dynamic Latent Bootstrapping 会缓存预测得到的 VAE latent，并逐步把它们送入训练，把上下文帧存储压到 20 GB 以下。在 LIBERO-Mixed 上，Sword 报告 FID 为 32.59、FVD 为 111.19，而 WoVR 分别是 119.62 和 198.84。

#### 资料来源
- [LaWM: Least Action World Models for Long-Horizon Physical Consistency from Visual Observations](../Inbox/2026-05-08--lawm-least-action-world-models-for-long-horizon-physical-consistency-from-visual-observations.md): LaWM least-action transition design and physical consistency metrics.
- [Sword: Style-Robust World Models as Simulators via Dynamic Latent Bootstrapping for VLA Policy Post-Training](../Inbox/2026-05-08--sword-style-robust-world-models-as-simulators-via-dynamic-latent-bootstrapping-for-vla-policy-post-training.md): Sword style augmentation, Dynamic Latent Bootstrapping, storage claim, and LIBERO generation metrics.
