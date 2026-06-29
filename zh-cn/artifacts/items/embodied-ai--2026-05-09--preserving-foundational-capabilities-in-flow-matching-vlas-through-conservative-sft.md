---
source: arxiv
url: https://arxiv.org/abs/2605.08879v2
published_at: '2026-05-09T10:59:03'
authors:
- Tianyi Zhang
- Shaopeng Zhai
- Haoran Zhang
- Fuxian Huang
- Qi Zhang
topics:
- vision-language-action
- robot-foundation-model
- flow-matching
- catastrophic-forgetting
- supervised-fine-tuning
- robot-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Preserving Foundational Capabilities in Flow-Matching VLAs through Conservative SFT

## Summary
## 摘要
ConSFT 是一种用于 flow-matching VLA 机器人策略的监督微调损失，用来减少任务适应过程中的灾难性遗忘。它在保持目标任务成功率接近普通 SFT 的同时，保留了更多既有机器人技能，而且不需要先前数据、参考模型或架构改动。

## 问题
- 在狭窄的机器人示范数据上做普通 SFT，可能会覆盖大量参数，抹去空间推理、物体操作和双臂控制等预训练技能。
- 现有修正方法代价高或限制多：Experience Replay 需要先前数据，正则化需要并行参考模型，LoRA 可能限制适应能力。
- 这很重要，因为机器人基础模型需要在不丢失大规模预训练中学到的技能的前提下适应新任务。

## 方法
- ConSFT 把逐样本的 flow-matching SFT 损失当作置信度信号：损失越高，说明模型对该转换越不确定。
- 它把 SFT 损失乘以一个 stop-gradient 权重 exp(-L_SFT/tau)，让低置信度样本产生更小的梯度。
- 温度 tau 会在训练中退火，因此更新一开始更保守，后面再允许更多目标任务拟合。
- 这种机制在监督训练中复制了 PPO 风格的有界更新效果，同时避免了 action-likelihood ODE 求解和并行参考网络。
- 论文声称，在 Fisher 二次形式下，遗忘风险按 exp(-2L_SFT/tau) 缩放，相当于普通 SFT 风险的该倍数。

## 结果
- 在 pi0 的 LIBERO 消融实验中，带 clipping 的 PPO 保留了 0.39 的平均先前任务表现，SFT 为 0.09，PPO-NoClip 为 0.03；目标 LIBERO-Spatial 成功率分别为 0.95、0.90 和 0.87。
- 同一消融实验报告，trust-region clipping 的更新量更低：15% 的参数发生变化，而无约束 SFT 为 30%，核心 Attention 和 MLP 权重的稀疏度超过 99%。
- 在 pi0 的 LIBERO 上，ConSFT 的目标任务成功率与 SFT 持平，都是 0.90，同时把平均先前任务保留率提高到 0.34，SFT 为 0.09；Object 保留率为 0.32 对 0.02，Goal 保留率为 0.35 对 0.16。
- 在 pi0.5 的 LIBERO 上，ConSFT 的目标成功率与 SFT 持平，都是 1.00，并把平均先前任务保留率提高到 0.43，SFT 为 0.23。
- 在 GR00T 的 LIBERO 上，ConSFT 把平均先前任务保留率提高到 0.59，SFT 为 0.49，但目标成功率较低，为 0.63 对 0.70。
- 在 pi0 的 RoboTwin 上，ConSFT 在 RoboTwin-Indep. 上达到 0.60 的目标成功率，SFT 为 0.55，并保留 0.28 的平均先前任务成功率，SFT 为 0.14；RoboTwin-Coord. 保留率为 0.13 对 0.00。摘要还声称，相比普通 SFT，平均绝对保留提升超过 20%，现实部署中的成功率提升约 20%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08879v2](https://arxiv.org/abs/2605.08879v2)
