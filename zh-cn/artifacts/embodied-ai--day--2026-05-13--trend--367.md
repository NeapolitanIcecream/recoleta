---
kind: trend
trend_doc_id: 367
granularity: day
period_start: '2026-05-13T00:00:00'
period_end: '2026-05-14T00:00:00'
topics:
- robotics
- vision-language-action models
- manipulation
- reinforcement learning
- latency
- OOD robustness
run_id: materialize-outputs
aliases:
- recoleta-trend-367
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/manipulation
- topic/reinforcement-learning
- topic/latency
- topic/ood-robustness
language_code: zh-CN
---

# 机器人 VLA 研究正在收紧围绕动作质量和时序的控制回路

## 概览
当前的机器人视觉语言动作（VLA）研究把部署当作执行问题来处理。最强的论文在动作表征、子任务调用、关键帧训练、视觉不变性和推理延迟上做调整，LIBERO、RoboTwin、SimplerEnv 和 ManiSkill 提供了大部分证据。

## 研究发现

### 动作表征与关键时间步
有几篇论文直接处理动作流本身。RotVLA 将帧间转移编码为连续的 SO(n) 潜在动作，并在训练中对它们进行组合。它在 LIBERO 上报告了 98.2% 的平均成功率，并在预训练超过 1700 小时的机器人和人类视频后，在 RoboTwin2.0 的干净和随机设置上分别达到 89.6% 和 88.5%。

FrameSkip 和 AttenA+ 在数据和损失层面提出了相关主张。FrameSkip 只保留 20% 的独特轨迹帧，并优先保留对齐、接触、夹爪闭合和释放帧。它在 RoboCasa-GR1、SimplerEnv 和 LIBERO 上的宏平均成功率从 66.50% 提升到 76.15%。AttenA+ 给缓慢、精度要求高的动作更高的损失权重，并把 OpenVLA-OFT 在 LIBERO 上的成功率从 97.10% 提升到 98.60%。

#### 资料来源
- [RotVLA: Rotational Latent Action for Vision-Language-Action Model](../Inbox/2026-05-13--rotvla-rotational-latent-action-for-vision-language-action-model.md): RotVLA summary, method, and LIBERO/RoboTwin results.
- [FrameSkip: Learning from Fewer but More Informative Frames in VLA Training](../Inbox/2026-05-13--frameskip-learning-from-fewer-but-more-informative-frames-in-vla-training.md): FrameSkip retention policy and benchmark gains.
- [AttenA+: Rectifying Action Inequality in Robotic Foundation Models](../Inbox/2026-05-13--attena-rectifying-action-inequality-in-robotic-foundation-models.md): AttenA+ velocity-weighted loss and success-rate gains.

### 用于长时程任务的规划器调用型 VLA 工具
长时程操作论文把高层规划器和机器人策略之间的接口收窄了。VLAs-as-Tools 让视觉语言模型规划器调用受限的 VLA 工具族，例如 grasp、open 或 place。Tool-Aligned Post-Training 用测试时相同的调用单元来训练这些策略，包括工具族、局部指令、动作和进度反馈。

在更难的任务集合上，效果提升很大。工具族设置把 π0.5 在 LIBERO-Long 上的成功率从 92.4% 提升到 97.2%，在 RoboTwin 上从 39.4% 提升到 62.5%。GTA-VLA 增加了一条面向人的纠正路径：用户可以提供点、框或轨迹，模型会在动作前把这个空间提示纳入推理。它在域内的 SimplerEnv WidowX 上报告了 81.2% 的成功率，但可用摘录里没有给出它在 OOD 场景下的精确提升数值。

#### 资料来源
- [Towards Long-horizon Embodied Agents with Tool-Aligned Vision-Language-Action Models](../Inbox/2026-05-13--towards-long-horizon-embodied-agents-with-tool-aligned-vision-language-action-models.md): VLAs-as-Tools interface, TAPT training, and LIBERO/RoboTwin gains.
- [Guide, Think, Act: Interactive Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-05-13--guide-think-act-interactive-embodied-reasoning-in-vision-language-action-models.md): GTA-VLA visual guidance mechanism and SimplerEnv result.

### 把 OOD 视觉行为作为 RL 训练目标
PAIR-VLA 把视觉可靠性作为行为层面的强化学习目标。PPO 微调时，它比较成对视觉变体下的动作分布。干扰物和纹理变化应该保持动作分布不变；目标位姿变化应该让动作分布分开。

结果是在 ManiSkill3 的抓取放置任务上取得了明确的 OOD 操作提升。OpenVLA 在桌面纹理、光照、目标位姿和杂乱度测试上的平均 OOD 成功率从 PPO 的 77.90% 提升到 PAIR-VLA 的 87.00%。π0.5 从 46.25% 提升到 62.87%。辅助损失只在训练时使用，所以部署策略保持相同的推理架构。

#### 资料来源
- [What to Ignore, What to React: Visually Robust RL Fine-Tuning of VLA Models](../Inbox/2026-05-13--what-to-ignore-what-to-react-visually-robust-rl-fine-tuning-of-vla-models.md): PAIR-VLA paired visual losses and OOD ManiSkill3 results.

### 面向部署规模 VLA 控制的推理与 RL 吞吐量
延迟优化现在和机器人可见的效果直接相关。Realtime-VLA FLASH 使用一个小的草稿模型和主模型验证，避免了很多完整的扩散重规划调用。在 LIBERO 上，带 Triton 的 FLASH 把平均任务级延迟从 58.0 ms 降到 19.1 ms，同时成功率只下降 0.3 个百分点，论文还报告了在对比方法失败的速度下进行传送带抓取的结果。

D-VLA 处理同一压力点的训练侧。它把 rollout 流量和权重更新分开，并把采样、接收、训练和分发串联起来。在 OpenVLA-OFT 上，它在单节点设置下报告 156.0 steps/s，而 RLinf-co 为 108.24，RL-VLA³ 为 110.88。摘录给出了吞吐量数字，但没有提供最终成功率。

#### 资料来源
- [Realtime-VLA FLASH: Speculative Inference Framework for Diffusion-based VLAs](../Inbox/2026-05-13--realtime-vla-flash-speculative-inference-framework-for-diffusion-based-vlas.md): Realtime-VLA FLASH latency, success tradeoff, and real-world conveyor result.
- [D-VLA: A High-Concurrency Distributed Asynchronous Reinforcement Learning Framework for Vision-Language-Action Models](../Inbox/2026-05-13--d-vla-a-high-concurrency-distributed-asynchronous-reinforcement-learning-framework-for-vision-language-action-models.md): D-VLA distributed RL design and throughput comparisons.
