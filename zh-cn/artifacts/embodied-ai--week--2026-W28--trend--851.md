---
kind: trend
trend_doc_id: 851
granularity: week
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-13T00:00:00'
topics:
- robot manipulation
- vision-language-action models
- task memory
- sample efficiency
- action control
- dexterous benchmarks
run_id: materialize-outputs
aliases:
- recoleta-trend-851
tags:
- recoleta/trend
- topic/robot-manipulation
- topic/vision-language-action-models
- topic/task-memory
- topic/sample-efficiency
- topic/action-control
- topic/dexterous-benchmarks
language_code: zh-CN
---

# 机器人策略的进步取决于记忆、失败经验复用和可执行的动作控制

## Overview
本周的机器人学习研究集中于视觉-语言-动作（VLA）策略中的执行瓶颈。任务记忆支持重试和阶段跟踪。失败轨迹与无标注视频提供了更多有用监督。连续轨迹和考虑力的后训练提升了速度与接触安全性。DexVerse显示，这些提升仍有限：在其19项任务评估子集上，测试方法的最高平均成功率只有34%。

## Clusters

### 任务记忆与未来状态推理
为策略提供明确的任务进度状态。TFP维护连续时间的潜在信念，使LIBERO Long-10的成功率从92.4%升至97.0%；在真实物体交换任务中，成功率从3/20升至15/20。Harness VLA围绕冻结控制器配置记忆引导规划器，使用已存储的轨迹、重新定位、分阶段执行和重试。在LIBERO-Pro上，它达到82.4%，而直接使用冻结控制器的基线为50.0%。LEEVLA在训练期间加入任务相关区域加权和潜在未来特征预测，在LIBERO上达到98.2%的平均成功率，且推理时无需额外记忆或计算。

#### Evidence
- [TFP: Temporally Conditioned Memory-Fusion Policies for Visuomotor Learning](../Inbox/2026-07-09--tfp-temporally-conditioned-memory-fusion-policies-for-visuomotor-learning.md): 介绍TFP的连续时间任务记忆，以及其在基准测试和真实机器人上的提升。
- [Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents](../Inbox/2026-07-09--harness-vla-steering-frozen-vlas-into-reliable-manipulation-primitives-via-memory-guided-agents.md): 介绍Harness VLA的规划器、记忆、重试机制和扰动测试结果。
- [LEEVLA: Seeing What Matters in Latent Environment Evolution for Vision-Language-Action](../Inbox/2026-07-09--leevla-seeing-what-matters-in-latent-environment-evolution-for-vision-language-action.md): 支持潜在未来特征预测，以及无需增加推理成本时的LIBERO结果。

### 从稀缺经验中获得更多监督
已收集的经验得到更充分的复用。Learning from Hindsight会根据机器人实际完成的行为，为失败轨迹重新标注。在分布外LIBERO-Pro任务上，它约用5个训练步骤就达到标准强化学习方法近30个步骤才能达到的性能；经过160次真实机器人轨迹采集后，成功率达到56%，基线为22%。CD-LAM从视频学习的潜在动作编码中去除背景、相机运动和无关物体。它用少于参考方法12倍的机器人动作适配更新次数达到相当的结果，使无标注视频成为更干净的动作监督来源。

#### Evidence
- [Learning More from Less: Reinforcement Learning from Hindsight](../Inbox/2026-07-10--learning-more-from-less-reinforcement-learning-from-hindsight.md): 提供后见之明重新标注机制、样本效率结果和实体机器人对比。
- [Causally Debiased Latent Action Model for Embodied Action Conditioned World Models](../Inbox/2026-07-10--causally-debiased-latent-action-model-for-embodied-action-conditioned-world-models.md): 提供潜在动作去偏方法和适配效率测量结果。

### 速度、力安全与更难的灵巧操作测试
动作表示正被作为控制接口进行评估，其时间性能和安全边界可以量化。B-spline Policy预测可按不同速度执行的连续曲线；在长时程桌面清洁任务中，它将平均完成时间从23.57秒缩短至11.80秒，成功率则从13/20变为14/20。PAC-ACT将强化学习与八步动作块对齐，在Contour任务中把超过60 N的力读数减少了46倍。DexVerse显示出尚未突破的上限：在19项任务中，最高平均成功率为0.34，四种受测策略在PushT上的得分均为零。

#### Evidence
- [B-spline Policy: Accelerating Manipulation Policies via B-spline Action Representations](../Inbox/2026-07-10--b-spline-policy-accelerating-manipulation-policies-via-b-spline-action-representations.md): 报告连续B样条动作、完成时间缩短、成功率和控制器限制。
- [PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers](../Inbox/2026-07-10--pac-act-post-training-actor-critic-for-action-chunking-transformers.md): 报告动作块级后训练，以及不安全接触力读数的减少。
- [DexVerse: A Modular Benchmark for Multi-Task, Multi-Embodiment Dexterous Manipulation](../Inbox/2026-07-09--dexverse-a-modular-benchmark-for-multi-task-multi-embodiment-dexterous-manipulation.md): 说明灵巧操作基准的范围，以及0.34的最高平均在线成功率。
