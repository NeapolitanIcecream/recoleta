---
kind: ideas
granularity: day
period_start: '2026-05-01T00:00:00'
period_end: '2026-05-02T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- vision-language-action models
- reinforcement learning
- long-horizon manipulation
- spatial attention
- autonomous driving
- interpretability
- world models
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/reinforcement-learning
- topic/long-horizon-manipulation
- topic/spatial-attention
- topic/autonomous-driving
- topic/interpretability
- topic/world-models
language_code: zh-CN
---

# Operational Robot Learning

## Summary
机器人团队可以直接做三项具体改动：把部署 rollout 收集为训练数据，把长时程计划暴露为缓存的文本和关键帧轨迹，再给快速模仿控制器加入空间注意点跟踪。共同的压力来自运行层面：固定的演示集、隐藏的计划和不稳定的视觉特征，会在机器人离开受控测试环境后变成失败。

## Fleet replay loop for deployed VLA manipulators
运行多个机械臂的机器人团队应该把部署日志当作训练输入，包括自动尝试失败、部分进展、恢复过程和人工介入。LWD 给出了一种具体做法：把当前检查点发送到共享机队，收集 rollout 放入在线回放缓冲区，与离线数据混合，再用能把稀疏奖励传播到长任务中的价值学习来重新训练共享的 VLA 策略。

采用这类方法时，成本较低的验证办法很窄：挑两到三个在物体、摆放或用户指令有小变化后会失败的任务，然后跑一个带成功、失败和介入标签的短回放循环。LWD 仍然是研究结果，但它的评估用了 16 台双臂机器人、8 个真实世界任务，包括 3 到 5 分钟的操作任务，并报告在几小时的在线交互后平均成功率达到 95%。这已经足够说明，在再买一轮干净演示数据之前，先把数据管道搭起来是值得的。

### Evidence
- [Learning while Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies](../Inbox/2026-05-01--learning-while-deploying-fleet-scale-reinforcement-learning-for-generalist-robot-policies.md): Summarizes LWD's fleet rollout, online replay, mixed offline-online retraining, sparse-reward value learning, and 16-robot real-world result.
- [Learning while Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies](../Inbox/2026-05-01--learning-while-deploying-fleet-scale-reinforcement-learning-for-generalist-robot-policies.md): Confirms the deployment problem: offline data misses distribution shifts, long-tail failures, task variations, and human correction opportunities.

## Cached text-and-keyframe traces for multi-stage manipulation tasks
长时程操作策略需要一个在执行前能让操作员和评估者查看的显式任务计划。IVLR 给出了一种可实现的版本：先根据初始图像和指令生成一次完整任务轨迹，把每个子目标和一个 RGB 关键帧配对，缓存这条轨迹，再让动作解码器同时基于轨迹和实时相机观测来决定动作。

这对那类常见失败点在于步骤顺序和目标位置的任务最有用，比如移动多个物体、在最终放置前先使用工具，或准备一串物品。第一次测试应该记录生成的轨迹、执行视频和失败位置，然后比较无轨迹、仅文本、仅视觉和完整轨迹这几种变体。在 LIBERO-Long 上，IVLR 在无轨迹时成功率为 37.7%，仅文本轨迹为 62.0%，仅视觉轨迹为 68.4%，完整交错轨迹为 92.4%。当前限制是实用层面的：完整轨迹生成在一块 NVIDIA H20 GPU 上大约需要 10 秒，所以它适合在运动开始前留有规划余量的任务。

### Evidence
- [Thinking in Text and Images: Interleaved Vision--Language Reasoning Traces for Long-Horizon Robot Manipulation](../Inbox/2026-05-01--thinking-in-text-and-images-interleaved-vision-language-reasoning-traces-for-long-horizon-robot-manipulation.md): Describes IVLR-Trace, its text subgoals plus RGB keyframes, cached execution, ablations, and planning latency.
- [Thinking in Text and Images: Interleaved Vision--Language Reasoning Traces for Long-Horizon Robot Manipulation](../Inbox/2026-05-01--thinking-in-text-and-images-interleaved-vision-language-reasoning-traces-for-long-horizon-robot-manipulation.md): Confirms the LIBERO-Long ablation numbers and notes the limits around stale plans and initial planning latency.

## Spatial attention-point tracking for ACT-based real-time controllers
使用 ACT 风格模仿策略的团队可以加入显式的二维注意点跟踪，在不切换到更慢控制器的情况下减少视觉漂移。MSACT 保留了 ACT 的动作分块和低延迟执行，然后从相机图像中提取与任务相关的点，并训练策略预测未来的注意点序列。关键实现细节是，注意监督来自未来帧的自监督，因此不需要人工关键点标注。

这种改造适合双臂精细操作和移动操作，那里漏接、相机视角变化和干扰物会破坏稠密视觉特征。在 ALOHA 双臂试验中，MSACT 在 400 次真实世界试验中报告总体成功率 53.00%，而 ACT 为 23.25%，同时延迟几乎不变，约 45 毫秒。一个相关的双目移动操作系统在四个真实世界任务上的平均成功率为 85.0%，ACT 为 46.0%，在扰动测试下也表现更好。实际验证时可以保留现有的 ACT 基线，再把注意点漂移、推理延迟和随机视觉扰动检查加入任务评分表。

### Evidence
- [MSACT: Multistage Spatial Alignment for Stable Low-Latency Fine Manipulation](../Inbox/2026-05-01--msact-multistage-spatial-alignment-for-stable-low-latency-fine-manipulation.md): Summarizes MSACT's self-supervised attention-point tracking, real-world ALOHA results, and ACT-level latency.
- [Stereo Multistage Spatial Attention for Real-Time Mobile Manipulation Under Visual Scale Variation and Disturbances](../Inbox/2026-05-01--stereo-multistage-spatial-attention-for-real-time-mobile-manipulation-under-visual-scale-variation-and-disturbances.md): Summarizes stereo multistage spatial attention for mobile manipulation, including four-task real-world success and disturbance tests.
