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

## Overview
这一时间窗口中的机器人论文把 Vision-Language-Action（VLA）策略当作可部署的控制系统处理。紧凑世界状态、接触反馈、失败数据和低预算适配都经过具体测试。OneWM-VLA、AT-VLA 和 ForgeVLA 给出了最清晰的实测信号。

## Clusters

### 紧凑且可规划的世界模型
世界模型研究集中在更小的潜在状态和更好的规划信号上。OneWM-VLA 将每个相机视角和每一帧压缩为一个语义 token，然后同时生成未来潜在 token 和动作块。论文报告，MetaWorld 平均成功率为 61.3%，高于 π0 的 47.9%；LIBERO 平均成功率为 98.1%；在干净条件下，真实 Piper 机械臂成功率为 71.7%，高于 π0 的 50.0%。

RLA-WM 使用 Residual Latent Action（RLA），这是一种用于 DINO 特征变化的紧凑编码。它以每次推理 3.5T FLOPs 预测未来视觉特征，并在 ManiSkill 和 IWS 预测指标上超过列出的特征和流基线。RC-aux 向潜在世界模型加入可达性监督，显示准确的短视距预测仍可能误导规划器。在 Wall 上，它将成功率提高到 83.6 ± 3.6，而 LeWM control 为 50.4 ± 6.5。

#### Evidence
- [One Token Per Frame: Reconsidering Visual Bandwidth in World Models for VLA Policy](../Inbox/2026-05-08--one-token-per-frame-reconsidering-visual-bandwidth-in-world-models-for-vla-policy.md): OneWM-VLA 的压缩设计，以及在 MetaWorld、LIBERO 和真实 Piper 任务上的成功率结果。
- [Learning Visual Feature-Based World Models via Residual Latent Action](../Inbox/2026-05-08--learning-visual-feature-based-world-models-via-residual-latent-action.md): RLA-WM 的残差潜在动作设计、预测指标和计算量比较。
- [Predictive but Not Plannable: RC-aux for Latent World Models](../Inbox/2026-05-08--predictive-but-not-plannable-rc-aux-for-latent-world-models.md): RC-aux 的可达性训练和目标条件控制收益。

### 用于 VLA 控制的接触和失败信号
几篇论文加入了只在执行期间出现的反馈通道。AT-VLA 加入触觉门控和双流结构：较慢的视觉语言推理，加上较快的触觉修正。论文报告闭环触觉响应时间在 0.04 s 以内。在真实机器人接触密集任务中，AT-VLA 将 Unzip Bag 成功率提高到 0.33，高于 GO-1 的 0.20 和 π0.5 的 0.00；将 Wipe Vase 提高到 0.67，高于 0.07 和 0.33。

AFIL 将失败 rollout 用作扩散式和流式 VLA 策略的负向引导。它训练分开的成功动作生成器和失败动作生成器，同时共享一个视觉语言骨干。现有摘要没有给出表格数值，因此有依据的结论是架构层面的：失败数据成为在线训练信号和采样时的排斥项。

#### Evidence
- [AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models](../Inbox/2026-05-08--at-vla-adaptive-tactile-injection-for-enhanced-feedback-reaction-in-vision-language-action-models.md): AT-VLA 的触觉门控、双流设计、反应时间和真实机器人成功率。
- [Failing Forward: Adaptive Failure-Informed Learning for Vision-Language-Action Models](../Inbox/2026-05-08--failing-forward-adaptive-failure-informed-learning-for-vision-language-action-models.md): AFIL 的失败 rollout 收集、双动作生成器和自适应负向引导。

### 受数据约束的 VLA 训练
训练论文关注私有、稀疏或特定领域的数据。ForgeVLA 在分布式视觉动作日志上训练，不集中原始数据，也不添加人工语言标签。每个客户端在本地分配伪指令，使用对比式规划损失和服务器聚合处理非独立同分布机器人数据。在 LIBERO-Goal 上，它达到 55.2% 成功率和 100% Pass@50，而 FedAvg 为 28.8% 和 80%。

ACA 针对真实机器人适配预算小的问题：在选定锚点条件下重复演示，然后在策略发生偏离的边界处收集数据。在 Franka Panda 设置中使用 100 条轨迹时，π0.5 加 ACA 达到 72.5% 平均成功率，高于 π0.5 的 31.7%。BioProVLA-Agent 将同样的部署压力放到湿实验室中：它把生物学协议解析为经过验证的子任务，在动作前后使用视觉检查，并运行在报告价格为 800–850 USD 的硬件平台上，但摘录没有给出准确成功率。

#### Evidence
- [ForgeVLA: Federated Vision-Language-Action Learning without Language Annotations](../Inbox/2026-05-08--forgevla-federated-vision-language-action-learning-without-language-annotations.md): ForgeVLA 的联邦训练设计和 LIBERO 结果。
- [Escaping the Diversity Trap in Robotic Manipulation via Anchor-Centric Adaptation](../Inbox/2026-05-08--escaping-the-diversity-trap-in-robotic-manipulation-via-anchor-centric-adaptation.md): Anchor-Centric Adaptation 方法，以及在演示数量有限时带来的真实机器人成功率提升。
- [BioProVLA-Agent: An Affordable, Protocol-Driven, Vision-Enhanced VLA-Enabled Embodied Multi-Agent System with Closed-Loop-Capable Reasoning for Biological Laboratory Manipulation](../Inbox/2026-05-08--bioprovla-agent-an-affordable-protocol-driven-vision-enhanced-vla-enabled-embodied-multi-agent-system-with-closed-loop-capable-reasoning-for-biological-laboratory-manipulation.md): BioProVLA-Agent 的协议解析、验证循环、低成本平台和基准范围。

### 作为世界模型标准的物理一致性
LaWM 和 Sword 将 rollout 质量作为控制要求。LaWM 通过学习得到的最小作用量目标和展开求解器定义下一个潜在状态。它最强的数值来自受控物理运动：PIS-vx 达到 0.9938 ± 0.0045；加速度一致性 PIS-ax 达到 0.8964 ± 0.0275，高于 NewtonGen 的 0.6568 ± 0.013。

Sword 为视觉风格变化下的 LIBERO rollout 训练动作条件世界模型。Dynamic Latent Bootstrapping 缓存预测的 VAE 潜变量，并逐步把它们送入训练，将上下文帧存储降到 20 GB 以下。在 LIBERO-Mixed 上，Sword 报告 FID 为 32.59、FVD 为 111.19，而 WoVR 为 119.62 和 198.84。

#### Evidence
- [LaWM: Least Action World Models for Long-Horizon Physical Consistency from Visual Observations](../Inbox/2026-05-08--lawm-least-action-world-models-for-long-horizon-physical-consistency-from-visual-observations.md): LaWM 的最小作用量转移设计和物理一致性指标。
- [Sword: Style-Robust World Models as Simulators via Dynamic Latent Bootstrapping for VLA Policy Post-Training](../Inbox/2026-05-08--sword-style-robust-world-models-as-simulators-via-dynamic-latent-bootstrapping-for-vla-policy-post-training.md): Sword 的风格增强、Dynamic Latent Bootstrapping、存储声明和 LIBERO 生成指标。
