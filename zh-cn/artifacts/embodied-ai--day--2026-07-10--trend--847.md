---
kind: trend
trend_doc_id: 847
granularity: day
period_start: '2026-07-10T00:00:00'
period_end: '2026-07-11T00:00:00'
topics:
- robot learning
- sample efficiency
- action representations
- tactile manipulation
- active perception
run_id: materialize-outputs
aliases:
- recoleta-trend-847
tags:
- recoleta/trend
- topic/robot-learning
- topic/sample-efficiency
- topic/action-representations
- topic/tactile-manipulation
- topic/active-perception
language_code: zh-CN
---

# 机器人策略的提升取决于能否用好稀缺经验和动作信号

## Overview
机器人学习正在处理现有策略流程中的实际瓶颈。失败的执行轨迹被转化为监督信号，潜在动作会去除视觉混杂因素，动作轨迹也加入了明确的速度和力控制。最明显的结果体现在样本效率、可控性和真实环境执行上。

## Clusters

### 高效的策略后训练
Learning from Hindsight 会将失败的机器人执行轨迹重新标注为机器人实际完成的行为，然后根据新的指令为这些轨迹评分。对于视觉-语言-动作（VLA）模型的后训练，该方法使 70%–80% 的轨迹组可用于训练，而标准方法只有 20%–40%。在分布外 LIBERO-PRO 任务上，它约用 5 个训练步骤就达到标准训练接近 30 步后的最终性能。使用 160 次实体机器人执行轨迹时，成功率达到 56%，标准组相对策略优化的成功率为 22%。

#### Evidence
- [Learning More from Less: Reinforcement Learning from Hindsight](../Inbox/2026-07-10--learning-more-from-less-reinforcement-learning-from-hindsight.md): 摘要介绍了事后重新标注方法、可用轨迹组比例、样本效率结果和实体机器人成功率。

### 可控的潜在动作
CD-LAM 面向动作条件世界模型，这类模型学习到的动作编码也会响应相机运动、背景或未被操作的物体。以实体为权重的重建、对比训练和零转移校准可以减少这些捷径。相机水平位移响应从 0.555 降至 0.156，垂直位移响应从 0.545 降至 0.110。这个 140 亿参数的模型只需不到 DreamDojo 参考方法 1/12 的机器人动作适配更新次数，就能达到相当的性能。

#### Evidence
- [Causally Debiased Latent Action Model for Embodied Action Conditioned World Models](../Inbox/2026-07-10--causally-debiased-latent-action-model-for-embodied-action-conditioned-world-models.md): 摘要记录了去除混杂因素的方法、相机位移审计、下游性能提升和适配效率。

### 动作执行速度与力安全
两篇论文都将执行质量视为动作表示和训练目标的属性。B-spline Policy 预测连续动作曲线，这些曲线可以按更高的控制频率重新采样。在桌面清洁任务中，它将平均完成时间从 23.57 秒缩短至 11.80 秒，成功次数从 13/20 增至 14/20；4× 的激进加速导致一个堆叠任务失败，暴露出控制器的限制。PAC-ACT 将强化学习与八步动作块对齐，并限制更新不要偏离预训练策略。在精密接触任务中，它将超过 60 N 的力读数占比降低了 46 倍。

#### Evidence
- [B-spline Policy: Accelerating Manipulation Policies via B-spline Action Representations](../Inbox/2026-07-10--b-spline-policy-accelerating-manipulation-policies-via-b-spline-action-representations.md): 摘要包含连续 B-spline 表示、真实机器人上的时间和成功率结果，以及高速执行失败案例。
- [PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers](../Inbox/2026-07-10--pac-act-post-training-actor-critic-for-action-chunking-transformers.md): 摘要支持动作块级后训练以及不安全接触力读数下降这一结果。

### 实体感知与主动观测
TactiDex 在 757 次示范中记录了 510 万帧同步数据，包含整手压力、手部运动、物体姿态、任务阶段和文本。它的残差策略利用人类压力模式指导接触时机和力调节，但现有证据没有提供数值化的成功率。对于空中感知，ATRNet-LUDO 在 40 个室外场景中提供 121,000 张全景图像和 121 万个目标图像块。主动 UAV 观测比被动感知的识别率高约 20 个百分点；在运动成本相近的情况下，其预测世界模型比深度强化学习基线再高出 2–3 个百分点。

#### Evidence
- [TactiDex: A Real-World Tactile-Guided Benchmark for Human-Like Dexterous Manipulation](../Inbox/2026-07-10--tactidex-a-real-world-tactile-guided-benchmark-for-human-like-dexterous-manipulation.md): 摘要给出了触觉数据集规模、传感规格、策略设计以及已报告定量证据的局限。
- [Toward Active Object Detection for UAVs in the Wild: A Large-Scale Dataset, Benchmark and Method](../Inbox/2026-07-10--toward-active-object-detection-for-uavs-in-the-wild-a-large-scale-dataset-benchmark-and-method.md): 摘要给出了 UAV 基准的规模，以及主动观测和预测建模带来的识别率提升。
