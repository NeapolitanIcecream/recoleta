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
ConSFT 是一种用于流匹配 VLA 机器人策略的监督微调损失，可在任务适配期间减少灾难性遗忘。它让目标任务成功率接近普通 SFT，同时保留更多已有机器人技能，并且不需要先前数据、参考模型或架构改动。

## 问题
- 在范围较窄的机器人演示上使用普通 SFT，可能覆盖大量参数，并抹去预训练得到的空间推理、物体操作和双臂控制技能。
- 现有修复方法成本高或限制多：Experience Replay 需要先前数据，正则化需要并行参考模型，LoRA 可能限制适配能力。
- 这一点很重要，因为机器人基础模型需要适配新任务，同时不能丢失大规模预训练中学到的技能。

## 方法
- ConSFT 使用逐样本流匹配 SFT 损失作为置信度信号：高损失表示模型对该转移的置信度较低。
- 它用 stop-gradient 权重 exp(-L_SFT/tau) 乘以 SFT 损失，使低置信度样本产生更小的梯度。
- 温度 tau 在训练期间退火，因此更新一开始较保守，之后允许更多目标任务拟合。
- 该机制在监督训练中复现 PPO 式有界更新的效果，同时避免动作似然 ODE 求解和并行参考网络。
- 论文声称，在 Fisher 二次近似下，遗忘风险会按 exp(-2L_SFT/tau) 乘以普通 SFT 风险的比例缩放。

## 结果
- 在 pi0 LIBERO 消融中，带裁剪的 PPO 保留了 0.39 的平均先前任务性能，SFT 为 0.09，PPO-NoClip 为 0.03；目标 LIBERO-Spatial 成功率中，PPO 为 0.95，SFT 为 0.90，PPO-NoClip 为 0.87。
- 同一消融报告称，trust-region clipping 带来更低的更新量：15% 的参数发生变化，而无约束 SFT 为 30%；核心 Attention 和 MLP 权重的稀疏度超过 99%。
- 在使用 pi0 的 LIBERO 上，ConSFT 在目标任务上达到与 SFT 相同的 0.90 成功率，并将平均先前任务保留率提高到 0.34，SFT 为 0.09；Object 保留率为 0.32，SFT 为 0.02；Goal 保留率为 0.35，SFT 为 0.16。
- 在使用 pi0.5 的 LIBERO 上，ConSFT 达到与 SFT 相同的 1.00 目标成功率，并将平均先前任务保留率提高到 0.43，SFT 为 0.23。
- 在使用 GR00T 的 LIBERO 上，ConSFT 将平均先前任务保留率提高到 0.59，SFT 为 0.49；目标成功率较低，为 0.63，SFT 为 0.70。
- 在使用 pi0 的 RoboTwin 上，ConSFT 在 RoboTwin-Indep. 上达到 0.60 的目标成功率，SFT 为 0.55；平均先前任务成功率保留为 0.28，SFT 为 0.14；RoboTwin-Coord. 保留率为 0.13，SFT 为 0.00。摘要还声称，相比普通 SFT，平均绝对保留率提升超过 20%，真实世界成功率优势约为 20%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08879v2](https://arxiv.org/abs/2605.08879v2)
