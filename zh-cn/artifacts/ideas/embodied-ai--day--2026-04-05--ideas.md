---
kind: ideas
granularity: day
period_start: '2026-04-05T00:00:00'
period_end: '2026-04-06T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- embodied-ai
- vla-safety
- adaptive-control
- driving-world-models
- dexterous-grasping
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/vla-safety
- topic/adaptive-control
- topic/driving-world-models
- topic/dexterous-grasping
language_code: zh-CN
---

# 自适应策略控制

## Summary
这里的具身智能工作正在控制接口上变得更具体。近期最清晰的变化有三项：面向已部署 VLA 策略的训练后遗忘工作流、用于机器人重规划的推理时自适应 chunking 层，以及面向自动驾驶世界模型的联合视频与轨迹评估线。每一项都对应一个明确的操作痛点：在不抹掉任务能力的前提下移除不安全行为、减少操作任务里对固定 chunk 的调参，以及提升自动驾驶规划器的零样本迁移。

## 面向已部署 VLA 机器人策略的训练后遗忘工作流
正在微调 VLA 策略的机器人团队需要一条训练后安全编辑路径，在不重训整套系统的情况下改变行为。VLA-Forget 指向一种具体做法：分别针对视觉编码器、跨模态投影器和上层动作层的策略编辑流程，然后在部署前对保留任务和安全探针运行一套固定的回归测试。实际用户是这样一类团队：他们已经在演示数据中发现了某种不良行为，或在已发布模型中发现了隐私敏感模式，现在需要一个范围收窄的修复方案。

这篇论文有价值，因为它把遗忘当作机器人控制问题来处理，而不只是模型合规问题。在 OpenVLA-7B 配合 Open X-Embodiment 的实验中，它报告 FC 93、RC 91、TSR 78 和 SVR 5，同时保留性能明显好于 GA，并且量化后的行为恢复也优于其他基线。这支持一种以分阶段编辑加量化后验收测试为中心的构建方式，因为模型在为部署而压缩后，可能会恢复不安全行为。

一个低成本验证步骤很直接：在现有策略中选一个反复出现的禁行动作，或一个已知的伪相关视觉触发因素，做一次模块级编辑，然后在同一套评测集上并排测三个指标：遗忘成功率、保留任务成功率，以及量化后的安全违规恢复。如果这些数字能同步改善，遗忘就可以成为机器人部署评审中的一个实用支持层。

### Evidence
- [VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models](../Inbox/2026-04-05--vla-forget-vision-language-action-unlearning-for-embodied-foundation-models.md): 对分阶段遗忘方法以及 OpenVLA-7B 和 pi0fast-base 基准结果的总结。
- [VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models](../Inbox/2026-04-05--vla-forget-vision-language-action-unlearning-for-embodied-foundation-models.md): 摘要中关于遗忘效果、保留能力和量化后恢复降低的结论。
- [VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models](../Inbox/2026-04-05--vla-forget-vision-language-action-unlearning-for-embodied-foundation-models.md): 引言将这一操作性问题界定为不安全或敏感行为会转化为物理动作。

## 用于机器人重规划的推理时自适应动作 chunking 中间件
在长任务上运行操作模型的团队可以加入一个推理时控制器，根据策略不确定性调整动作 chunk 长度。AAC 给出了一套具体方法：采样候选动作 chunk，估计未来各步的熵，在不确定性上升时执行较短片段，在预测保持稳定时让机器人在再次重规划前运行更长时间。

这很有用，因为固定 chunk 长度仍然是 VLA 部署中的一个调参负担。某一种设置会让动作更平滑，但响应较慢；另一种会更快重规划，但可能引入不连续。AAC 不需要重训，可以作为现有模型外的一层封装。论文报告的提升幅度不大，但很稳定：GR00T 在 RoboCasa 上从 59.7% 提升到 62.0%，在 LIBERO 上从 94.1% 提升到 95.0%，在 LIBERO-Long 上从 88.8% 提升到 92.8%。pi-0.5 和 LIBERO-Pro 扰动测试上也有同样的模式。

第一步可以先为一个现有策略做一层重规划中间件，并记录所选 chunk 长度、熵变化趋势和任务结果。一个低成本检查方法是在相同算力预算下，用固定 chunk 长度和 AAC 分别重放一套基准任务或实验室任务，然后比较成功率、重规划次数和可见的运动不连续性。这能帮助机器人团队判断，在改动训练数据或模型权重之前，自适应 chunking 是否值得采用。

### Evidence
- [Adaptive Action Chunking at Inference-time for Vision-Language-Action Models](../Inbox/2026-04-05--adaptive-action-chunking-at-inference-time-for-vision-language-action-models.md): 对 AAC、固定 chunk 部署问题以及 RoboCasa 和 LIBERO 基准提升的总结。
- [Adaptive Action Chunking at Inference-time for Vision-Language-Action Models](../Inbox/2026-04-05--adaptive-action-chunking-at-inference-time-for-vision-language-action-models.md): 摘要描述了分块执行中响应性与一致性的权衡。
- [Adaptive Action Chunking at Inference-time for Vision-Language-Action Models](../Inbox/2026-04-05--adaptive-action-chunking-at-inference-time-for-vision-language-action-models.md): 引言指出 chunk 大小会随策略和任务变化，这支持中间件式的部署工具。

## 面向零样本自动驾驶迁移的联合视频与轨迹规划器评估
构建世界模型规划器的自动驾驶团队可以加入一条联合视频与轨迹生成的训练和评估线，然后测试它是否能在不过多增加采样成本的情况下提升零样本迁移。DriveVA 给出了一个具体目标：在同一个共享生成过程中预测未来视频 latent 和自车轨迹 token，并把 rollout 控制得足够短，使两步采样仍能交付接近峰值的闭环性能。

这篇论文有用，因为它把规划质量和一个可测量的设计选择直接联系起来。在 NAVSIM v1 上，DriveVA 达到 90.9 PDMS，高于文中列出的一些基线，摘要还将很大一部分提升归因于稠密视频监督，在加入视频监督后，PDMS 从 71.4 提升到 90.9。论文还报告了在 nuScenes 和 Bench2Drive/CARLA v2 上很大的零样本迁移增益，其中包括相对于文中给出的世界模型基线，在 nuScenes 上碰撞率降低 83.3%。

一个实际的下一步是在现有自动驾驶系统中做一组配对消融：在同一来源数据集上训练一个仅动作规划器和一个联合视频-动作规划器，然后比较闭环分数、碰撞率以及向一个留出域的迁移效果。如果联合模型在低采样步数下仍然保持优势，这个结果就支持把它作为规划器训练和模拟器评估的新默认方案。

### Evidence
- [DriveVA: Video Action Models are Zero-Shot Drivers](../Inbox/2026-04-05--driveva-video-action-models-are-zero-shot-drivers.md): 对 DriveVA、联合生成设计、稠密视频监督作用和基准结果的总结。
- [DriveVA: Video Action Models are Zero-Shot Drivers](../Inbox/2026-04-05--driveva-video-action-models-are-zero-shot-drivers.md): 摘要解释了先前松耦合规划器中的视频-轨迹一致性问题。
- [DriveVA: Video Action Models are Zero-Shot Drivers](../Inbox/2026-04-05--driveva-video-action-models-are-zero-shot-drivers.md): 在 NAVSIM、nuScenes 和 Bench2Drive/CARLA v2 上报告的闭环和零样本迁移指标。
