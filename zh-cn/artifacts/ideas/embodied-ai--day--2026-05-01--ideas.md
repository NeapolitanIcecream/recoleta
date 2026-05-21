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

# 面向运行的机器人学习

## Summary
机器人团队可以采取三项具体改变：把部署 rollout 收集为训练数据，把长时程计划公开为缓存文本与关键帧 trace，并为快速模仿控制器加入空间注意力点跟踪。共同的压力来自运行阶段：固定演示集、隐藏计划和不稳定视觉特征，会在机器人离开受控测试环境后表现为失败。

## 已部署 VLA 机械臂的机器人队列 replay 循环
运行多台机械臂的机器人团队应把部署日志作为训练输入，包括自主尝试失败、部分进展、恢复过程和人工干预。LWD 给出了一个具体模式：把当前检查点发送到共享机器人队列，把 rollout 收集到在线 replay buffer 中，与离线数据混合，并用价值学习重新训练共享 VLA 策略，使稀疏奖励能够在长任务中传播。

低成本采用测试应保持范围很窄：选择两三个任务，这些任务中预训练策略会在物体、放置位置或用户指令发生小变化后失败，然后运行一个短 replay 循环，记录成功、失败和干预标签。LWD 结果仍是研究结果，但它的评估使用了 16 台双臂机器人，覆盖 8 个真实世界任务，包括 3–5 分钟的操作任务，并报告在几小时在线交互后达到 95% 平均成功率。这些证据足以支持先建设数据管道，再购买下一轮干净演示数据。

### Evidence
- [Learning while Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies](../Inbox/2026-05-01--learning-while-deploying-fleet-scale-reinforcement-learning-for-generalist-robot-policies.md): 概述 LWD 的机器人队列 rollout、在线 replay、离线与在线混合再训练、稀疏奖励价值学习，以及 16 台机器人的真实世界结果。
- [Learning while Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies](../Inbox/2026-05-01--learning-while-deploying-fleet-scale-reinforcement-learning-for-generalist-robot-policies.md): 确认部署问题：离线数据会漏掉分布偏移、长尾失败、任务变化和人工纠正机会。

## 用于多阶段操作任务的缓存文本与关键帧 trace
长时程操作策略需要一个可见的任务计划，供操作员和评估人员在执行前检查。IVLR 展示了一个可构建版本：从初始图像和指令一次性生成完整任务 trace，把每个子目标与一个 RGB 关键帧配对，缓存该 trace，并让动作解码器基于 trace 和实时相机观测生成动作。

这最适合步骤顺序和目标放置经常出错的任务，例如移动多个物体、在最终放置前使用工具，或按顺序准备一组物品。第一次测试应记录生成的 trace、执行视频和失败点，然后比较无 trace、仅文本、仅视觉和完整 trace 变体。在 LIBERO-Long 上，IVLR 报告无 trace 的成功率为 37.7%，仅文本 trace 为 62.0%，仅视觉 trace 为 68.4%，完整交错 trace 为 92.4%。当前限制来自实际运行：在一块 NVIDIA H20 GPU 上生成完整 trace 约需 10 秒，因此它适合运动开始前有规划余量的任务。

### Evidence
- [Thinking in Text and Images: Interleaved Vision--Language Reasoning Traces for Long-Horizon Robot Manipulation](../Inbox/2026-05-01--thinking-in-text-and-images-interleaved-vision-language-reasoning-traces-for-long-horizon-robot-manipulation.md): 描述 IVLR-Trace、其文本子目标加 RGB 关键帧、缓存执行、消融实验和规划延迟。
- [Thinking in Text and Images: Interleaved Vision--Language Reasoning Traces for Long-Horizon Robot Manipulation](../Inbox/2026-05-01--thinking-in-text-and-images-interleaved-vision-language-reasoning-traces-for-long-horizon-robot-manipulation.md): 确认 LIBERO-Long 消融数字，并指出过期计划和初始规划延迟方面的限制。

## 用于 ACT 实时控制器的空间注意力点跟踪
使用 ACT 式模仿策略的团队可以加入显式 2D 注意力点跟踪，以减少视觉漂移，同时避免换成更慢的控制器。MSACT 保留 ACT 的动作分块和低延迟执行，然后从相机图像中提取任务相关点，并训练策略预测未来注意力点序列。关键工程细节是，注意力监督来自未来帧的自监督信号，因此不需要人工关键点标签。

这种改造适合双臂精细操作和移动操作，在这些场景中，接触错失、相机视角变化和干扰物会破坏密集视觉特征。在 ALOHA 双臂试验中，MSACT 报告在 400 次真实世界试验中的成功率为 53.00%，ACT 为 23.25%，同时延迟几乎不变，约为 45 ms。一个相关的立体移动操作系统报告在四个真实世界任务上的平均成功率为 85.0%，ACT 为 46.0%，并且在干扰测试中表现更好。一次实用验证可以保留现有 ACT 基线，并把注意力漂移、推理延迟和随机视觉干扰检查加入任务记分板。

### Evidence
- [MSACT: Multistage Spatial Alignment for Stable Low-Latency Fine Manipulation](../Inbox/2026-05-01--msact-multistage-spatial-alignment-for-stable-low-latency-fine-manipulation.md): 概述 MSACT 的自监督注意力点跟踪、真实世界 ALOHA 结果和 ACT 级延迟。
- [Stereo Multistage Spatial Attention for Real-Time Mobile Manipulation Under Visual Scale Variation and Disturbances](../Inbox/2026-05-01--stereo-multistage-spatial-attention-for-real-time-mobile-manipulation-under-visual-scale-variation-and-disturbances.md): 概述用于移动操作的立体多阶段空间注意力，包括四任务真实世界成功率和干扰测试。
