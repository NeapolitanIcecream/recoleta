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

# Adaptive policy control

## Summary
这里的具身 AI 工作在控制接口上变得更具体了。最清楚的近期开端是：给已部署的 VLA 策略做训练后遗忘流程，给机器人重规划加一层推理时自适应分块，以及为驾驶世界模型建立联合视频-轨迹评测线。每一项都对准了一个明确的操作痛点：在不丢掉任务能力的前提下移除不安全行为，减少操控里的固定块长调参，以及提升驾驶规划器的零样本迁移。

## Post-training unlearning workflow for deployed VLA robot policies
微调 VLA 策略的机器人团队需要一条训练后安全修正路径，在不重训整个栈的情况下改行为。VLA-Forget 给出了一种具体做法：把策略编辑流程分别作用于视觉编码器、跨模态投影层和上层动作层，然后在部署前对保留任务和安全探针跑一套固定回归测试。实际使用者是已经在示教数据里发现坏行为，或者在已上线模型里发现隐私敏感模式的团队，他们需要的是一次窄范围修正。

这篇论文的价值在于，它把遗忘问题当成机器人控制问题，而不只是模型合规问题。在 OpenVLA-7B 和 Open X-Embodiment 上，它报告 FC 93、RC 91、TSR 78、SVR 5，同时保留性能比 GA 好得多，量化后恢复能力也优于其他基线。这支持一种以分阶段编辑和量化后验收测试为核心的流程，因为模型在压缩部署时可能把不安全行为恢复出来。

一个低成本验证步骤很直接：从现有策略里挑一个反复出现的禁用动作，或者一个已知的伪视觉触发器，做一次模块级编辑，然后在同一组评测集上并排看三项指标：遗忘成功率、保留任务成功率、量化后的安全违规恢复情况。如果这些数值一起变化，遗忘就会成为机器人部署审查里的实用支撑层。

### Evidence
- [VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models](../Inbox/2026-04-05--vla-forget-vision-language-action-unlearning-for-embodied-foundation-models.md): Summary of the staged unlearning method and benchmark results on OpenVLA-7B and pi0fast-base.
- [VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models](../Inbox/2026-04-05--vla-forget-vision-language-action-unlearning-for-embodied-foundation-models.md): Abstract claims on forgetting efficacy, retention, and post-quantization recovery reduction.
- [VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models](../Inbox/2026-04-05--vla-forget-vision-language-action-unlearning-for-embodied-foundation-models.md): Introduction frames the operational problem as unsafe or sensitive behaviors turning into physical actions.

## Inference-time adaptive action chunking middleware for robot replanning
在长任务上跑操控模型的团队，可以加一个推理时控制器，根据策略不确定性改变动作块长度。AAC 的做法很直接：采样候选动作块，估计未来各步的熵，在不确定性上升时执行更短的片段，在预测稳定时让机器人跑更长再重规划。

这之所以有用，是因为固定块长在 VLA 部署里仍然是个调参负担。一个设置让动作更平滑，但反应慢；另一个重规划更快，却可能带来不连续。AAC 不需要重训，可以作为现有模型外面的一层包装。报告的提升不大，但很稳定：GR00T 在 RoboCasa 上从 59.7% 提升到 62.0%，LIBERO 从 94.1% 提升到 95.0%，LIBERO-Long 从 88.8% 提升到 92.8%。pi-0.5 和 LIBERO-Pro 的扰动测试也出现了同样的模式。

第一版实现应该是一层重规划中间件，接到一个现有策略上，并记录选中的块长、熵变化和任务结果。一个低成本检查是，在相同算力预算下，把固定块长和 AAC 都跑一遍基准或实验室任务集，再比较成功率、重规划次数和可见的运动不连续情况。这样机器人团队就能在动训练数据或模型权重之前判断自适应分块值不值得上。

### Evidence
- [Adaptive Action Chunking at Inference-time for Vision-Language-Action Models](../Inbox/2026-04-05--adaptive-action-chunking-at-inference-time-for-vision-language-action-models.md): Summary of AAC, the fixed-chunk deployment problem, and benchmark gains across RoboCasa and LIBERO.
- [Adaptive Action Chunking at Inference-time for Vision-Language-Action Models](../Inbox/2026-04-05--adaptive-action-chunking-at-inference-time-for-vision-language-action-models.md): Abstract describes the responsiveness versus consistency trade-off in chunked execution.
- [Adaptive Action Chunking at Inference-time for Vision-Language-Action Models](../Inbox/2026-04-05--adaptive-action-chunking-at-inference-time-for-vision-language-action-models.md): Introduction states that chunk size varies by policy and task, which supports a middleware-style deployment tool.

## Joint video-and-trajectory planner evaluation for zero-shot driving transfer
做世界模型规划器的驾驶团队，可以加一条联合视频和轨迹生成的训练与评测线，再测试它能否提升零样本迁移，同时不过多增加采样成本。DriveVA 给出的目标很明确：在一个共享生成过程中同时预测未来视频潜变量和自车轨迹 token，然后把 rollout 控制得足够短，让两步采样也能得到接近峰值的闭环表现。

这篇论文的价值在于，它把规划质量和一个可测的设计选择绑在一起。在 NAVSIM v1 上，DriveVA 达到 90.9 PDMS，高于文中列出的多个基线；摘要还把很大一部分提升归因于密集视频监督，加入视频监督后 PDMS 从 71.4 升到 90.9。它还在 nuScenes 和 Bench2Drive/CARLA v2 上报告了较大的零样本迁移提升，包括相对文中所述世界模型基线，在 nuScenes 上碰撞率下降 83.3%。

一个实际的下一步是在现有驾驶栈里做一组配对消融：用同一份源数据训练一个只输出动作的规划器和一个联合视频-动作规划器，然后比较闭环分数、碰撞率，以及到一个留出的目标域的迁移表现。如果联合模型在较少采样步数下仍然保持优势，这个结果就支持把它作为规划器训练和仿真评测的新默认方案。

### Evidence
- [DriveVA: Video Action Models are Zero-Shot Drivers](../Inbox/2026-04-05--driveva-video-action-models-are-zero-shot-drivers.md): Summary of DriveVA, joint generation design, dense video supervision effect, and benchmark results.
- [DriveVA: Video Action Models are Zero-Shot Drivers](../Inbox/2026-04-05--driveva-video-action-models-are-zero-shot-drivers.md): Abstract explains the video-trajectory consistency problem in prior loosely coupled planners.
- [DriveVA: Video Action Models are Zero-Shot Drivers](../Inbox/2026-04-05--driveva-video-action-models-are-zero-shot-drivers.md): Reported closed-loop and zero-shot transfer metrics on NAVSIM, nuScenes, and Bench2Drive/CARLA v2.
