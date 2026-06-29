---
source: arxiv
url: https://arxiv.org/abs/2605.08732v1
published_at: '2026-05-09T06:36:23'
authors:
- Hoang Nguyen
- Xiaohao Xu
- Xiaonan Huang
topics:
- world-model-planning
- inverse-dynamics
- goal-conditioned-control
- latent-representations
- amortized-planning
- robot-manipulation
relevance_score: 0.64
run_id: materialize-outputs
language_code: zh-CN
---

# Latent Geometry Beyond Search: Amortizing Planning in World Models

## Summary
## 摘要
GC-IDM 用一个小型、以目标为条件的逆动力学模型，替代了预训练 LeWorldModel 中的在线轨迹搜索。它把每步决策成本降低约 100 到 130 倍，同时把成功率保持在接近 CEM、甚至高于 CEM 的水平。

## 问题
- 基于视觉的世界模型可以低成本预测潜在状态中的未来，但选动作通常还是要依赖昂贵的在线搜索。
- 在 LeWorldModel 中，默认的 CEM 每次规划要用 9000 个候选 rollout 和 45000 次预测器前向传播，所以动作选择占了主要计算量。
- 论文想回答的是：一个平滑、对动作敏感的潜在空间，能否把面向目标的控制变成一个监督式逆动力学问题。

## 方法
- 该方法冻结一个预训练的 LeWorldModel 编码器，并在与世界模型相同的离线轨迹上训练 GC-IDM。
- 每个训练样本使用当前潜在状态、未来目标潜在状态、采样得到的时间跨度，以及数据集中当前步骤的动作。
- GC-IDM 是一个 3 层 MLP，隐藏层大小为 512，使用 LayerNorm、GELU、10% dropout，并通过 64 维正弦编码加 AdaLN-Zero 注入时间跨度条件。
- 测试时，控制器只编码一次目标，在每次动作后重新编码当前观测，并用一次前向传播预测下一步动作；它不做 rollout 搜索。
- 这个逆模型大约有 150 万参数，在单张 GPU 上每个环境训练大约需要 20 分钟。

## 结果
- 在 Two-Room、Push-T、OGBench-Cube 和 Reacher 上，GC-IDM 在 8 个环境-协议设置中的 7 个里与 CEM 持平或更好。
- 每步规划成本降低了 100 到 130 倍。CEM 使用一个 1080 万参数的预测器，每次规划要调用 45000 次；GC-IDM 只增加一个 150 万参数的 MLP，预测器调用次数为 0。
- 在 n=200 时，Two-Room 的成功率为 100.0% ± 0.0，CEM 为 84.0% ± 2.8，规划速度提升 104 倍。
- 在 n=200 时，OGBench-Cube 的成功率为 98.7% ± 0.6，CEM 为 67.0% ± 2.1，规划速度提升 130 倍。
- 在 n=200 时，Reacher 的成功率为 99.7% ± 0.3，CEM 为 70.3% ± 4.3，规划速度提升 110 倍。
- Push-T 是最接近的一组：在 n=50 时，GC-IDM 为 84.7% ± 5.0，CEM 为 89.3% ± 6.4；在 n=200 时，GC-IDM 为 84.2% ± 2.8，CEM 为 82.5% ± 1.3。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08732v1](https://arxiv.org/abs/2605.08732v1)
