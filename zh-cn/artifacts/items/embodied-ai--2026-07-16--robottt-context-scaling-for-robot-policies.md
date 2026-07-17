---
source: arxiv
url: https://arxiv.org/abs/2607.15275v1
published_at: '2026-07-16T17:59:06'
authors:
- Yunfan Jiang
- Yevgen Chebotar
- Ruijie Zheng
- Fengyuan Hu
- Yunhao Ge
- Jimmy Wu
- Tianyuan Dai
- Scott Reed
- Li Fei-Fei
- Yuke Zhu
- Linxi "Jim" Fan
topics:
- robot-foundation-model
- long-context-policy
- test-time-training
- vision-language-action
- dexterous-manipulation
- in-context-imitation
relevance_score: 0.99
run_id: materialize-outputs
language_code: zh-CN
---

# RoboTTT: Context Scaling for Robot Policies

## Summary
## 总结
RoboTTT 通过在训练和推理期间更新快速神经网络权重，将机器人策略的上下文扩展到 8K 个时间步。在真实机器人双臂装配任务中，它提高了长时域任务的完成率，支持基于人类视频的一次性模仿，并且不会随着上下文长度增加而提高推理延迟，还能适应任务失败。

## 问题
- 大多数机器人基础模型使用单步或短历史的视觉运动输入，这限制了它们跟踪任务进展、处理部分可观测性、模仿演示以及在多阶段任务中恢复的能力。
- 这一问题之所以重要，是因为长时域操作任务需要保留与任务相关的历史信息，同时保持推理计算的实用性。

## 方法
- RoboTTT 在 GR00T N1.7 视觉-语言-动作策略中加入测试时训练层。小型快速权重 MLP 在每个时间步接收梯度更新，将历史信息压缩到参数中，供后续观测使用。
- 模型在每个时间步内使用注意力机制，并在不同时间步之间使用 TTT 层，使快速权重状态能够传播，同时使推理延迟不随总上下文长度增加。
- 序列动作强制为每个动作片段独立采样扩散噪声水平，而截断反向传播通过时间在各个片段之间传递快速权重，无需存储完整序列的激活值。
- 在适应过程中，掩码训练将演示或机器人失败作为上下文，并将人类动作作为目标；这支持一次性视频模仿和 DAgger Distillation 的“从失败到纠正”流程。

## 结果
- 在三个真实机器人 YAM 双臂装配任务——Pup Go Car、Circuit 和 Gear Bot——中，RoboTTT 的平均任务完成得分达到 79%，而单步 GR00T N1.7 为 42%，GDN 为 56%；论文将其分别报告为较单步基线提高 87%、较 GDN 提高 41%。
- 在 Pup Go Car、Circuit 和 Gear Bot 上，RoboTTT 分别有 9/20、13/20 和 2/10 次试验完全成功。它是唯一一个完全完成 Gear Bot 的评估方法；Gear Bot 是一项持续五分钟、包含十个阶段的装配任务，但 RoboTTT 仅在 10 次试验中成功 2 次。
- 使用 8K 时间步预训练上下文时，RoboTTT 的平均完成率达到 71.5%；相比之下，同一模型使用 1K 时间步预训练时为 43.9%，最佳短上下文基线为 45.6%。论文将其描述为较 1K 设置提高 63%、较短上下文基线提高 57%；摘要将前一项比较报告为 62%，表明两处存在轻微的报告差异。
- 在针对未见过的配置、基于单段人类视频进行的 Circuit 一次性模仿中，RoboTTT 的完成得分为 65%，成功 rollout 次数为 6/10；GDN 的完成得分为 33%，成功 rollout 次数为 0/10。
- 在外部扰动下，RoboTTT 在 83% 的试验中成功，而最佳短上下文基线为 53%；与未采用这种即时改进训练的同一模型相比，DAgger Distillation 带来了 36% 的性能提升。
- 证据来自三个任务系列和固定的试验次数——每项任务 20 次试验，Gear Bot 为 10 次——因此，这些提升证明了 RoboTTT 在这些真实机器人评估中的表现，而不能据此断言它在所有机器人平台或任务上都具有普遍优势。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.15275v1](https://arxiv.org/abs/2607.15275v1)
