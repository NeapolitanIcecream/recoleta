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

# 机器人 VLA 研究正在围绕动作质量和时序收紧控制环

## Overview
当前机器人视觉-语言-动作（VLA）研究把部署视为执行问题。证据最强的论文在调整动作表示、子任务调用、关键帧训练、视觉不变性和推理延迟，主要证据来自 LIBERO、RoboTwin、SimplerEnv 和 ManiSkill。

## Clusters

### 动作表示和关键时间步
几篇论文直接处理动作流。RotVLA 将帧间转移编码为连续的 SO(n) 潜在动作，并在训练中组合这些动作。它在超过 1700 小时的机器人和人类视频上预训练后，报告了 LIBERO 98.2% 的平均成功率，以及 RoboTwin2.0 干净设置和随机设置下 89.6% / 88.5% 的成功率。

FrameSkip 和 AttenA+ 在数据和损失层面提出了相关主张。FrameSkip 保留唯一轨迹帧的 20%，优先保留对齐、接触、抓取闭合和释放。它在 RoboCasa-GR1、SimplerEnv 和 LIBERO 上的宏平均成功率从 66.50% 升至 76.15%。AttenA+ 对缓慢、精度要求高的动作给予更高损失权重，使 OpenVLA-OFT 在 LIBERO 上从 97.10% 提升到 98.60%。

#### Evidence
- [RotVLA: Rotational Latent Action for Vision-Language-Action Model](../Inbox/2026-05-13--rotvla-rotational-latent-action-for-vision-language-action-model.md): RotVLA 摘要、方法以及 LIBERO/RoboTwin 结果。
- [FrameSkip: Learning from Fewer but More Informative Frames in VLA Training](../Inbox/2026-05-13--frameskip-learning-from-fewer-but-more-informative-frames-in-vla-training.md): FrameSkip 保留策略和基准提升。
- [AttenA+: Rectifying Action Inequality in Robotic Foundation Models](../Inbox/2026-05-13--attena-rectifying-action-inequality-in-robotic-foundation-models.md): AttenA+ 速度加权损失和成功率提升。

### 由规划器调用的长时程任务 VLA 工具
长时程操作论文让高层规划器与机器人策略之间的约定更窄。VLAs-as-Tools 使用视觉语言模型规划器调用有边界的 VLA 工具族，例如抓取、打开或放置。Tool-Aligned Post-Training 按测试时使用的同一调用单元训练这些策略，包括工具族、局部指令、动作和进度反馈。

在更难的任务套件上，测得的提升很大。工具族设置使 π0.5 在 LIBERO-Long 上从 92.4% 升至 97.2%，在 RoboTwin 上从 39.4% 升至 62.5%。GTA-VLA 增加了一条面向人的纠错路径：用户可以提供点、框或轨迹，模型在行动前把这个空间提示纳入推理。它报告了域内 SimplerEnv WidowX 上 81.2% 的成功率，但可用摘录没有给出其 OOD 改进主张的确切数字。

#### Evidence
- [Towards Long-horizon Embodied Agents with Tool-Aligned Vision-Language-Action Models](../Inbox/2026-05-13--towards-long-horizon-embodied-agents-with-tool-aligned-vision-language-action-models.md): VLAs-as-Tools 接口、TAPT 训练以及 LIBERO/RoboTwin 提升。
- [Guide, Think, Act: Interactive Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-05-13--guide-think-act-interactive-embodied-reasoning-in-vision-language-action-models.md): GTA-VLA 视觉引导机制和 SimplerEnv 结果。

### 作为 RL 训练目标的 OOD 视觉行为
PAIR-VLA 把视觉可靠性作为行为层面的强化学习目标。在 PPO 微调期间，它比较成对视觉变体之间的动作分布。干扰物和纹理变化应保持动作分布不变；目标位姿变化应使动作分布分离。

这在 ManiSkill3 拾取放置任务上带来明确的 OOD 操作提升。在桌面纹理、光照、目标位姿和杂乱测试中，OpenVLA 从使用 PPO 的 77.90% 提升到使用 PAIR-VLA 的 87.00%。π0.5 从 46.25% 提升到 62.87%。辅助损失只在训练期间使用，因此部署策略保持相同的推理架构。

#### Evidence
- [What to Ignore, What to React: Visually Robust RL Fine-Tuning of VLA Models](../Inbox/2026-05-13--what-to-ignore-what-to-react-visually-robust-rl-fine-tuning-of-vla-models.md): PAIR-VLA 成对视觉损失和 OOD ManiSkill3 结果。

### 面向部署规模 VLA 控制的推理和 RL 吞吐量
延迟研究现在与机器人可见的效果绑定。Realtime-VLA FLASH 使用小型草稿模型和主模型验证，避免许多完整扩散重规划调用。在 LIBERO 上，带 Triton 的 FLASH 将平均任务级延迟从 58.0 ms 降至 19.1 ms，成功率下降 0.3 个百分点；论文还报告了在对比方法失败的速度下完成传送带抓取。

D-VLA 处理同一压力点的训练侧。它将 rollout 流量与权重更新分离，并对采样、接收、训练和分发进行流水线处理。在 OpenVLA-OFT 上，它报告单节点设置下达到 156.0 steps/s，而 RLinf-co 为 108.24，RL-VLA³ 为 110.88。摘录给出了吞吐量数字，但没有提供最终成功率。

#### Evidence
- [Realtime-VLA FLASH: Speculative Inference Framework for Diffusion-based VLAs](../Inbox/2026-05-13--realtime-vla-flash-speculative-inference-framework-for-diffusion-based-vlas.md): Realtime-VLA FLASH 延迟、成功率权衡和真实传送带结果。
- [D-VLA: A High-Concurrency Distributed Asynchronous Reinforcement Learning Framework for Vision-Language-Action Models](../Inbox/2026-05-13--d-vla-a-high-concurrency-distributed-asynchronous-reinforcement-learning-framework-for-vision-language-action-models.md): D-VLA 分布式 RL 设计和吞吐量对比。
