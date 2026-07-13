---
source: arxiv
url: https://arxiv.org/abs/2607.09042v1
published_at: '2026-07-10T02:17:41'
authors:
- Iris Xu
- Sunshine Jiang
- John Marangola
- Nitish Dashora
- Richard Li
- Thomas Liu
- Zexue He
- Yuheng Zhi
- Alex Pentland
- Pulkit Agrawal
- Zhang-Wei Hong
topics:
- vision-language-action
- robot-reinforcement-learning
- hindsight-relabeling
- sample-efficiency
- robot-data-scaling
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Learning More from Less: Reinforcement Learning from Hindsight

## Summary
## 摘要
后见之明学习（Learning from Hindsight，LfH）将失败的机器人轨迹转化为对机器人实际执行行为的训练数据，从而改进视觉-语言-动作模型的强化学习后训练。在分布外 LIBERO-PRO 任务上，LfH 将样本效率提高了约 5 倍，并让物理 Franka 机器人更快取得性能提升。

## 问题
- 稀疏的成功奖励会让早期的大多数操作轨迹失去训练价值：如果一个组中的所有轨迹都失败，该组的奖励方差为零，无法产生 GRPO 更新。
- 机器人轨迹采集缓慢且成本高，丢弃大部分已采集轨迹会限制 VLA 后训练。
- 更充分地利用已有轨迹，可以减少提升机器人策略所需的实体数据和训练步数，因此这个问题会直接影响训练效率。

## 方法
- 对于成功率较低的轨迹组，视觉语言模型（VLM）观察失败轨迹，并生成描述机器人实际完成行为的语言指令，例如“拿起杯子。”
- 同一个 VLM 使用这条共享的后见之明指令评估组内每条轨迹，并分配 0、0.5 或 1 的奖励。
- LfH 对带有后见之明标签的轨迹组应用 GRPO，并针对原始指令下采样的动作进行重要性修正，然后将这次更新与标准 GRPO 更新结合起来。
- LfH 主要对低奖励轨迹组进行重标注；对于原始任务已经获得有效奖励的轨迹组，则保留原始训练信号。

## 结果
- 在分布外 LIBERO-PRO 任务上，LfH 约用 5 个训练步就达到标准 GRPO 近 30 个训练步才能达到的最终性能，样本效率约提高 5 倍。
- LfH 保持约 70% 至 80% 的轨迹组可用于训练；标准 GRPO 和使用 RoboMETER 稠密奖励的 GRPO 只有约 20% 至 40% 的轨迹组可用。
- 在 LIBERO-90 的一个示例中，LfH 保留了近 80% 的轨迹组，并将成功率从 0 提高到 60%；在报告的训练阶段内，标准 GRPO 的成功率仍为 0。
- LfH 的表现优于 RoboMETER 稠密进度奖励基线。这表明，当策略很少接近目标任务时，重标注任务可能比为该任务增加更密集的反馈更有效。
- 结果在 pi0.5、GR00T 和 OpenVLA-OFT 主干模型之间具有可迁移性，也能迁移到物理 Franka FR3 机器人上。使用 160 条真实世界轨迹时，LfH 的成功率达到 56%，GRPO 为 22%；使用 128 条轨迹时，LfH 的成功率约为 GRPO 的两倍。
- 单独进行指令重标注或奖励重标注只能带来有限提升；随机奖励也无法达到完整方法的效果。这说明，需要将具有语义依据的指令与奖励结合起来。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.09042v1](https://arxiv.org/abs/2607.09042v1)
