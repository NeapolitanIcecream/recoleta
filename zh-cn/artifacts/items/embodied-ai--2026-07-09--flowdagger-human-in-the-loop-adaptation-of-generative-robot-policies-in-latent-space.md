---
source: arxiv
url: https://arxiv.org/abs/2607.08877v1
published_at: '2026-07-09T19:07:33'
authors:
- Michael Murray
- Daphne Chen
- Simran Bagaria
- Dean Fortier
- Tess Hellebrekers
- Galen Mullins
- Harshavardhan Gajarla
- Oier Mees
- Maya Cakmak
- Andrey Kolobov
topics:
- robot-foundation-model
- generative-robot-policy
- human-in-the-loop
- latent-space-adaptation
- vision-language-action
- world-action-model
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# FlowDAgger: Human-in-the-Loop Adaptation of Generative Robot Policies in Latent Space

## Summary
## 摘要
FlowDAgger 将人类提供的少量纠正动作转换为潜在噪声目标，用于适配冻结的生成式机器人策略。它在保留基础策略预训练技能的同时提高任务成功率，只需训练一个小型控制器。

## 问题
- 生成式机器人策略在训练数据之外的物体、动力学、机器人形态和边缘情况下容易失败。
- 收集示范数据、微调大型模型以及在实体机器人上运行强化学习，都需要大量数据和算力，并会带来安全风险。
- 在动作空间中进行纠正可能使行为超出基础策略的可靠支持范围；更新模型权重则可能损害无关技能。

## 方法
- 对于每次人类纠正，动作反演会逆向运行冻结策略的生成过程，寻找能够复现专家动作的噪声向量。
- 一个小型的观测到噪声策略学习这些反演目标；部署时，将该策略预测的噪声输入冻结的基础策略。
- 该方法使用逐步固定点反演，每一步迭代 5 次，以处理少步数流匹配动作头。
- 对于 Cosmos-Policy 等世界-动作模型，方法会反演联合潜在过程，只修改动作帧，同时保留预测的状态帧和值帧。
- 训练时将反演后的干预数据与成功自主运行中的噪声混合，以保留原有行为。

## 结果
- 在使用 pi_0.5 的 12 个 MetaWorld 任务上，FlowDAgger 在匹配的 50 次运行预算后达到 0.78 的平均成功率，相比冻结基础策略的 0.53 提高 +0.25；SFT 达到 0.71，LoRA-DAgger 达到 0.68，Residual-DAgger 达到 0.64，DSRL 达到 0.55。
- FlowDAgger 在 12 个 MetaWorld 任务中的 8 个任务上取得最高成绩；在 Coffee Pull 和 Stick Push 上成功率达到 1.00，在 Hand Insert 上为 0.99，在 Assembly 上为 0.89。
- 在一组共用的七个 MetaWorld 任务上，使用 pi_0.5 时平均成功率从 0.53 提高到 0.79，使用 Cosmos-Policy（一种世界-动作模型）时从 0.53 提高到 0.74；对应增幅分别为 +0.26 和 +0.21。
- 在 Hammer 适配测试中，成功率从 0.40 提高到 0.84；在五个未参与训练的任务上，平均表现为 0.88，而未适配基础策略为 0.96；Residual-DAgger 在这些保留任务上的表现降至 0.69。
- 该方法只训练小型噪声策略。在报告的 pi_0.5 设置中，显存需求约为 8 GB；摘录还称，该方法已在模拟任务以及真实世界的单臂和双臂操作中完成成功评估。
- 提供的摘录没有给出真实世界实验的完整定量结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08877v1](https://arxiv.org/abs/2607.08877v1)
