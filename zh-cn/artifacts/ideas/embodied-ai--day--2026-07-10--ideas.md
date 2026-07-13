---
kind: ideas
granularity: day
period_start: '2026-07-10T00:00:00'
period_end: '2026-07-11T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- sample efficiency
- action representations
- tactile manipulation
- active perception
tags:
- recoleta/ideas
- topic/robot-learning
- topic/sample-efficiency
- topic/action-representations
- topic/tactile-manipulation
- topic/active-perception
language_code: zh-CN
---

# 机器人策略训练与部署诊断

## Summary
机器人团队可以从失败 rollout 中恢复训练信号，在执行速度测试中检查力和控制器限制，并在投入机器人动作适配成本前审计潜在动作中的视觉混淆因素。每项改动都能接入现有的 VLA、动作分块或世界模型流程，并可通过小规模离线批次或受限机器人试验进行验证。

## 失败 VLA rollout 的 hindsight 重标注
早期成功率较低的 VLA 团队应在 RL 后训练中加入重标注阶段。VLM 检查失败的 rollout，为机器人实际完成的行为写出指令，再根据该指令为 rollout 打分；策略随后同时使用原任务信号和重标注样本进行训练。Learning from Hindsight 让 70%–80% 的 rollout 组可用于训练，在约 5 个训练步内达到标准 GRPO 在 LIBERO-PRO 上的最终性能，而标准 GRPO 接近需要 30 步；在 160 次实体机器人 rollout 中，其成功率达到 56%，GRPO 为 22%。

在收集更多机器人数据前，可以先对已保存的失败样本进行低成本检查。重标注几百条轨迹，人工检查分层抽样样本中的指令和奖励准确性，再将可用组比例及留出任务成功率与当前奖励流程进行比较。部署时应只对行为完整且连贯的片段进行重标注，并拒绝含义不明确的片段，因为错误的 hindsight 指令会让策略学习错误标注的动作。

### Evidence
- [Learning More from Less: Reinforcement Learning from Hindsight](../Inbox/2026-07-10--learning-more-from-less-reinforcement-learning-from-hindsight.md): 记录了重标注方法、可用组比例、样本效率结果、骨干网络覆盖范围和实体 Franka 对比结果。
- [Learning More from Less: Reinforcement Learning from Hindsight](../Inbox/2026-07-10--learning-more-from-less-reinforcement-learning-from-hindsight.md): 说明了具体流程：一个 VLM 提出 hindsight 指令，为 rollout 组打分，并提供联合训练信号。

## 动作分块策略的速度与力验收测试
操作团队应在确定执行速度前，评估动作策略在速度和接触条件范围内的表现。B-spline Policy 提供连续动作曲线，可以在更高的控制频率下重新采样，也可以调整时间尺度而无需重新训练。PAC-ACT 则为接触任务提供互补的后训练方法：使用 PPO 优化八步动作块，并将更新限制在预训练 ACT 策略附近。

验收测试应在每个速度设置下报告完成时间、成功率、跟踪误差、峰值力，以及超过任务特定阈值的力采样占比。B-spline Policy 将清洁桌面的时间从 23.57 秒降至 11.80 秒，成功次数从 13/20 变为 14/20；但由于控制器跟踪能力受限，其 Speed Stacking 在 4× 速度下的结果降至 0/20。PAC-ACT 在一项精密接触任务中将超过 60 N 的力读数减少了 46 倍。在进行更长时间的部署测试前，可以先以 1×、2× 和 4× 速度开展受限试验，确定可用的运行范围。

### Evidence
- [B-spline Policy: Accelerating Manipulation Policies via B-spline Action Representations](../Inbox/2026-07-10--b-spline-policy-accelerating-manipulation-policies-via-b-spline-action-representations.md): 提供了实体机器人上的时间和成功率结果、集成细节，以及高速执行时的失败结果。
- [PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers](../Inbox/2026-07-10--pac-act-post-training-actor-critic-for-action-chunking-transformers.md): 提供了分块级 RL 设计，以及超过 60 N 的力读数降幅。
- [PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers](../Inbox/2026-07-10--pac-act-post-training-actor-critic-for-action-chunking-transformers.md): 解释了位姿和接触分布偏移为何会导致行为克隆动作分块策略出现力安全问题。

## 潜在动作模型的视觉混淆因素审计
使用无标注视频的世界模型团队，应在进行机器人动作适配前，检查潜在动作是否编码了相机运动、静态背景或未接触物体。一次小规模审计可以包含：将重复帧作为零转移对照、水平和垂直相机位移、背景替换，以及交互区域之外的物体变化。对于重复帧，模型应输出接近零的动作；对于不改变具身动作的视觉变化，模型的输出应保持稳定。

CD-LAM 表明，这类审计可以指导有针对性的微调阶段，包括具身加权重建、以动作为中心的对比学习和潜在空间校准。其相机位移响应在水平方向从 0.555 降至 0.156，在垂直方向从 0.545 降至 0.110；14B 模型只使用少于 DreamDojo 参考方法 1/12 的机器人动作适配更新次数，就达到了相当的结果。团队可以先在几百个留出片段上运行这些扰动测试，只有在潜在响应持续对应机器人和物体交互后，再进行成本较高的动作标注训练。

### Evidence
- [Causally Debiased Latent Action Model for Embodied Action Conditioned World Models](../Inbox/2026-07-10--causally-debiased-latent-action-model-for-embodied-action-conditioned-world-models.md): 报告了混淆因素审计指标、去偏目标和机器人动作适配效率。
- [Causally Debiased Latent Action Model for Embodied Action Conditioned World Models](../Inbox/2026-07-10--causally-debiased-latent-action-model-for-embodied-action-conditioned-world-models.md): 解释了仅使用重建训练的潜在动作模型如何将背景和未交互物体纳入动作编码。
- [Causally Debiased Latent Action Model for Embodied Action Conditioned World Models](../Inbox/2026-07-10--causally-debiased-latent-action-model-for-embodied-action-conditioned-world-models.md): 详细说明了在适配可执行机器人动作前采用的分阶段微调流程。
