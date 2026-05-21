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
GC-IDM 用一个小型目标条件逆动力学模型，替代预训练 LeWorldModel 中的在线轨迹搜索。它将成功率保持在接近或高于 CEM 的水平，同时把每次决策的规划成本降低约 100 到 130 倍。

## 问题
- 基于视觉的世界模型可以低成本预测潜在未来，但选择动作通常仍需要昂贵的在线搜索。
- 在 LeWorldModel 中，默认 CEM 每个规划步骤使用 9,000 条候选 rollout 和 45,000 次预测器前向传播，因此动作选择占用了主要计算量。
- 论文研究一个平滑、对动作敏感的潜在空间能否把目标导向控制转化为监督式逆动力学问题。

## 方法
- 该方法冻结预训练 LeWorldModel 编码器，并在用于训练世界模型的同一批离线轨迹上训练 GC-IDM。
- 每个训练样本使用当前潜在状态、未来目标潜在状态、采样的时域长度，以及数据集中当前步骤的动作。
- GC-IDM 是一个 3 层 MLP，隐藏层大小为 512，使用 LayerNorm、GELU、10% dropout，并通过 64 维正弦编码加 AdaLN-Zero 进行时域条件化。
- 测试时，控制器对目标编码一次，在每个动作后重新编码当前观测，并用一次前向传播预测下一个动作。它不执行 rollout 搜索。
- 该逆模型约有 1.5M 个参数，在单块 GPU 上每个环境约需 20 分钟训练。

## 结果
- 在 Two-Room、Push-T、OGBench-Cube 和 Reacher 上，GC-IDM 在 8 个环境-协议设置中的 7 个达到或超过 CEM。
- 每次决策的规划成本下降 100 到 130 倍。CEM 使用 10.8M 参数的预测器，每次规划调用 45,000 次；GC-IDM 增加一个 1.5M 参数的 MLP，预测器调用次数为 0。
- 当 n=200 时，Two-Room 成功率为 GC-IDM 的 100.0% ± 0.0，对比 CEM 的 84.0% ± 2.8，规划速度提升 104 倍。
- 当 n=200 时，OGBench-Cube 成功率为 98.7% ± 0.6，对比 67.0% ± 2.1，规划速度提升 130 倍。
- 当 n=200 时，Reacher 成功率为 99.7% ± 0.3，对比 70.3% ± 4.3，规划速度提升 110 倍。
- Push-T 是最接近的案例：当 n=50 时，GC-IDM 得到 84.7% ± 5.0，CEM 为 89.3% ± 6.4；当 n=200 时，GC-IDM 得到 84.2% ± 2.8，CEM 为 82.5% ± 1.3。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08732v1](https://arxiv.org/abs/2605.08732v1)
