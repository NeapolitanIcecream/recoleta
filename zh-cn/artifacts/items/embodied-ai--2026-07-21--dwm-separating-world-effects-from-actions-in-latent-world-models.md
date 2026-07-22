---
source: arxiv
url: https://arxiv.org/abs/2607.18715v1
published_at: '2026-07-21T05:13:26'
authors:
- Yi-Ge Zhang
- Tianqi Du
- Qi Zhang
- Yisen Wang
topics:
- latent-world-models
- model-based-control
- world-action-disentanglement
- cem-planning
- persistent-dynamics
- robotics
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# DWM: Separating World Effects from Actions in Latent World Models

## Summary
## 总结
DWM 训练潜在世界模型，将与动作无关的环境运动和由动作驱动的变化分离开来。在包含持续重力或漂移的基准任务上，它提升了 CEM 规划性能，同时不改变推理时的模型架构。

## 问题
- 标准的动作条件潜在世界模型使用单一的下一潜变量目标进行监督，将由智能体引起的运动与即使采取空动作也会发生的变化混合在一起。
- 这一点很重要，因为重力、惯性、接触反弹和漂移等持续性效应会导致多步滚动预测不准确，并造成较差的规划决策。

## 方法
- DWM 在现有预测器上增加一个仅用于训练的 world head；对于同一状态，将当前动作替换为另一个动作时，该 head 被训练为输出相同的表示。
- 归一化的 InfoNCE 世界对比损失鼓励动作不变性，同时保留状态区分能力；正交损失则将 world head 的输出与剩余的动作驱动成分分离开来。
- 原始预测 head 仍然预测完整的下一潜变量，并且推理时只使用这一 head，因此规划流程保持不变。
- 评估使用 PushT-W、Reacher-W 和 TwoRoom-W。这些任务在标准任务基础上分别加入了重力驱动的滑动、竖直平面中的重力以及恒定的环境漂移，此外还包括 Ball-in-Cup。

## 结果
- 在 PushT-W、Reacher-W 和 TwoRoom-W 上，DWM 的 CEM 规划成功率分别提高 12.0%、10.7% 和 16.7%，平均绝对提升为 13.1%。
- 在 Ball-in-Cup 上，DWM 将性能提升了 6.0%。
- 在标准 PushT 基准上，单 head 的 LeWM 基线达到 94.0% 的 CEM 成功率；而在 PushT-W 上，其成功率为 32%。增加 30% 的空动作训练数据并未带来帮助，成功率为 30%。
- 在没有显著世界效应的普通任务上，DWM 的表现仍与单 head 基线相当；诊断实验和消融实验表明，其性能提升与更强的动作不变性以及更准确的多步潜在空间滚动预测有关。
- 报告的评估主要基于受控的模拟基准变体；该摘录并未证明 DWM 在实体机器人或广泛真实世界数据集上的性能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.18715v1](https://arxiv.org/abs/2607.18715v1)
