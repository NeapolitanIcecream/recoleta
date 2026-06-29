---
kind: trend
trend_doc_id: 546
granularity: day
period_start: '2026-06-05T00:00:00'
period_end: '2026-06-06T00:00:00'
topics:
- robotics
- vision-language-action
- action representation
- policy adaptation
- long-horizon control
- edge deployment
run_id: materialize-outputs
aliases:
- recoleta-trend-546
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/action-representation
- topic/policy-adaptation
- topic/long-horizon-control
- topic/edge-deployment
language_code: zh-CN
---

# 机器人策略的提升来自动作接口和执行约束

## Overview
这一天的机器人策略工作集中在可执行动作设计上。Vision-Language-Action（VLA）论文在动作头、潜在动作对齐、任务适配器和机载延迟上做调整。最强信号很实际：更高的 LIBERO 成功率、更低的 Franka 误差，以及 10 Hz 的闭环目标，和模型大小一样重要。

## Clusters

### VLA 策略中的动作表示
一些论文把动作接口当作改进操作能力的主要位置。ActionMap 用体素热图替代逐点动作预测，分别表示平移、旋转和夹爪状态。在 OpenVLA-OFT 其他部分不变的情况下，它把 LIBERO 四个子集的平均成绩从 89.1% 提高到 97.3%，并把真实 Franka 试验在全量数据下从 7/30 提高到 20/30。

LARA 通过潜在动作处理同样的控制瓶颈。它把 Latent Action Model（LAM）和扩散式 VLA 策略一起训练，并将 LAM 的潜变量与中间策略特征对齐。在 OXE 约束的 LIBERO 设置下，LARA full 的平均成功率是 88.6，高于 OpenVLA 的 76.5，也高于只用 DiT 的版本 84.4。

Spline Policy 更偏方法设计。它把固定动作块换成样条参数，这些参数可以重采样、加约束，并传给控制器。可用摘录里没有成功率表，所以它的证据指向兼容性和执行结构，而不是测得的提升。

#### Evidence
- [ActionMap: Robot Policy Learning via Voxel Action Heatmap](../Inbox/2026-06-05--actionmap-robot-policy-learning-via-voxel-action-heatmap.md): ActionMap summary and reported LIBERO and Franka gains.
- [LARA: Latent Action Representation Alignment for Vision-Language-Action Models](../Inbox/2026-06-05--lara-latent-action-representation-alignment-for-vision-language-action-models.md): LARA joint latent-action alignment method and benchmark results.
- [Spline Policy: A Structured Representation for Robot Policies](../Inbox/2026-06-05--spline-policy-a-structured-representation-for-robot-policies.md): Spline Policy action-output design and limits of the available evidence.

### 没有目标动作标注的任务适配
WIZARD 关注把冻结的 VLA 策略适配到新任务的成本。它根据语言指令和一段简短示范视频预测任务专属的 Low-Rank Adaptation（LoRA）权重，然后在测试时直接运行适配后的策略，不做梯度更新。

最强结果出现在留出的 LIBERO-Spatial 上：WIZARD 的平均成功率达到 0.40，而使用 π0.5 的 MT-VLA 是 0.19，最近邻适配器检索是 0.02。论文也展示了方法边界。LIBERO-Object 仍然只有 0.03 的平均成功率，LIBERO-10 上完整任务的零样本完成在摘录里仍是 0.00。

#### Evidence
- [Robotic Policy Adaptation via Weight-Space Meta-Learning](../Inbox/2026-06-05--robotic-policy-adaptation-via-weight-space-meta-learning.md): WIZARD method, held-out LIBERO results, and stated limitations.

### 长时程控制仍然紧贴动作
Coarse-to-Control 增加了内部计划，但这个计划由动作 token 组成。模型先预测粗粒度的未来动作 token，再在这个计划上预测可执行 token。这样，规划就一直和腕部运动、夹爪状态和路点结构绑定在一起。它在 LIBERO 上报告 97.9% 的总成功率，在 SimplerEnv-WidowX 上是 83.3%，真实世界测试中每个任务用 50 个演示时，四个操作任务的平均成功率是 62.5%。

FLIGHT 把同样的问题放到无人机上。这个基准使用自然语言任务和连续 6-DoF 控制，模型把工作分成较慢的视频-语言模块和更快的扩散动作模型。数据集包含 6,689 条细粒度导航轨迹，并以 10 Hz 采样连续动作。

STRIPS-WM 处理从图像出发的高层规划。它从 RGB 动作转移中学习符号化的前提条件和效果，然后在谓词空间里规划。它的数值反映的是抽象质量：在 BlocksWorld 中，它为 16 个真实状态恢复了 16 个学到的图结构状态，transition slack 和 applicability slack 都是 0。

#### Evidence
- [Coarse-to-Control: Action-Token Planning for Vision-Language-Action Models](../Inbox/2026-06-05--coarse-to-control-action-token-planning-for-vision-language-action-models.md): Coarse-to-Control action-token planning design and LIBERO, SimplerEnv, and real-world results.
- [Think Like a Pilot: Fine-Grained Long-Horizon UAV Navigation](../Inbox/2026-06-05--think-like-a-pilot-fine-grained-long-horizon-uav-navigation.md): FLIGHT benchmark, fast-slow control architecture, and dataset statistics.
- [STRIPS-WM: Learning Grounded Propositional STRIPS-style World Models from Images](../Inbox/2026-06-05--strips-wm-learning-grounded-propositional-strips-style-world-models-from-images.md): STRIPS-WM visual-to-symbolic planning method and reported abstraction metrics.

### 部署延迟与跨机器人接口
RhinoVLA 是这一组里最明确的部署论文。它面向边缘硬件上的闭环操作，使用 Qwen3-VL 降低视觉 token 成本，并用连续的 Action Expert 处理动作块。系统在 Huixi R1 边缘系统上的端到端推理速度为 11.69 Hz，高于 10 Hz 的控制目标。

论文也指出了它要压缩的运行时瓶颈。在 Jetson AGX Orin 上的 π0.5 延迟分解里，VLM 主干和 Action Expert 占了超过 90% 的运行时间，VLM 的 MLP 投影约占 VLM 延迟的 74.7%。它的跨机器人设计用了 View Registry、共享的 72D 状态-动作槽空间、缺失机器人维度的掩码，以及机器人实例 LoRA 模块。

#### Evidence
- [RhinoVLA Technical Report](../Inbox/2026-06-05--rhinovla-technical-report.md): RhinoVLA deployment design, latency breakdown, and 11.69 Hz result.
