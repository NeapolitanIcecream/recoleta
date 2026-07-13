---
source: arxiv
url: https://arxiv.org/abs/2607.09185v1
published_at: '2026-07-10T08:20:27'
authors:
- Yufan Wei
- Kun Zhou
- Lingjun Mao
- Zijun Zhang
- Ziming Xu
- Ziqiao Xi
- Shuang Liang
- Ruobing Han
- Yuchen Yan
- Xinyue Wang
- Fan Feng
- Biwei Huang
topics:
- embodied-world-model
- latent-action-model
- robot-action-following
- causal-debiasing
- robot-data-efficiency
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Causally Debiased Latent Action Model for Embodied Action Conditioned World Models

## Summary
## 摘要
CD-LAM 通过移除不描述具身动作的视觉因素，改进了动作条件世界模型中的潜在动作表示。在 2B 和 14B 模型上，它在动作跟随、视觉保真度、鲁棒性和机器人动作适配效率方面取得了更好的结果。

## 问题
- 动作条件世界模型需要带有动作标签的机器人数据，而这类数据采集成本很高。
- 潜在动作模型可以从无标签视频中学习，但仅使用重建目标进行训练时，可能会把背景、相机位移和未交互物体编码进动作表示。
- 这些混杂因素会让世界模型生成的轨迹在视觉上合理，却降低模型对给定潜在动作或机器人动作的遵循程度。

## 方法
- CD-LAM 使用以具身为中心的重建目标对潜在动作模型进行微调，并为机器人和交互物体设置高于背景的损失权重。
- 以动作为中心的对比学习会拉近具有相同粗粒度操作原语的转移，同时在不同视觉环境中区分具有不同操作原语的转移。
- 潜在空间校准会将重复帧输入锚定在接近零转移向量的位置，并通过 free-bits KL 惩罚控制表示容量。
- 三阶段流程先对 LAM 进行去偏，再使用去偏后的潜在动作训练世界模型，最后训练一个轻量级 MLP，将可执行的机器人动作映射到同一潜在空间中。

## 结果
- 在潜在动作审计中，CD-LAM 将零转移响应的中位数从 0.527 降至 0.043，并将潜在向量范数绝对值的中位数从 3.119 降至 0.226。
- 水平相机位移的响应从 0.555 降至 0.156，垂直相机位移的响应从 0.545 降至 0.110；捷径信息泄漏从 0.151 降至 0.014。
- 相比 DreamDojo，潜在动作 FDCE 在 2B 主干模型上下降了 42%，在 14B 主干模型上下降了 26%。
- 机器人动作适配后，FDCE 在 2B 模型上进一步下降了 35%，在 14B 模型上进一步下降了 30%；去偏后的 14B 模型在所有报告指标上均排名第一。
- CD-LAM 达到 DreamDojo 参考结果时所需的机器人动作适配更新次数不到其 1/12，并在 6,000 步检查点超过了 DreamDojo；去偏阶段使用了 1,000 次 LAM 更新和 2,000 次世界模型更新。
- 评估使用了 300 个留出的 EgoDex 视频片段进行潜在动作轨迹测试，并使用 300 个 AgiBot 视频片段在 2B 和 14B ACWM 主干模型上进行机器人动作测试。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.09185v1](https://arxiv.org/abs/2607.09185v1)
