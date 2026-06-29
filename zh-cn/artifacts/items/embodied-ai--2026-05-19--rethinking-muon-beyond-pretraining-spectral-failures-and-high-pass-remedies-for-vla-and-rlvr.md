---
source: arxiv
url: https://arxiv.org/abs/2605.19282v1
published_at: '2026-05-19T03:00:26'
authors:
- Chongyu Fan
- Gaowen Liu
- Mingyi Hong
- Ramana Rao Kompella
- Sijia Liu
topics:
- vla-training
- robot-policy
- optimizer-design
- spectral-optimization
- rlvr
- newton-schulz
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# Rethinking Muon Beyond Pretraining: Spectral Failures and High-Pass Remedies for VLA and RLVR

## Summary
Pion 是一种类似 Muon 的优化器，适用于 VLA 训练和 RLVR 后训练。它保留大的奇异方向，抑制小而噪声大的方向。论文声称，它在机器人策略训练和 RLVR 中都比 Muon 更好，而且每步开销与 Muon 相同。

## Problem
- Muon 会把动量矩阵的所有非零奇异值都推向 1，这会放大小而噪声大的奇异方向。
- 在 VLA 训练中，动作模块梯度是低秩的，因为机器人动作的维度很低，所以 Muon 可能会破坏动作更新。
- 在 RLVR 中，策略梯度的信噪比很低，Muon 可能会把有用方向和噪声方向拉到同一尺度，从而导致训练崩溃。

## Approach
- Pion 在保持优化器控制流程和每步开销不变的前提下，修改了 Muon 的 Newton-Schulz 更新系数。
- 它使用两阶段的高通 Newton-Schulz 迭代：Promotion 阶段提升前导奇异值，Suppression 阶段把小奇异值推向 0。
- Promotion 多项式使用系数 `(1.875, -1.25, 0.375)`，并保持 `[0,1]` 上奇异值的顺序。
- Suppression 阶段把大的奇异值锚定在 1 附近，同时压缩小奇异值，得到一种软的、适应秩的更新，不需要 SVD 或 sketching。
- 对于注意力层，Pion 可以按 head 重塑投影，并对每个 head 单独应用相同更新，在不增加额外开销的情况下保留预训练时的 head 级差异。

## Results
- 在 LIBERO Object 上的 VLA-Adapter 中，Pion 在 `1,500` 个训练步后达到 `100%` 成功率，而 Muon 为 `97.0%`，AdamW 为 `32.2%`。
- 在 LIBERO 和 LIBERO-Plus 上，Pion 在 `l1`-regression 的 VLA-Adapter 和 flow-matching 的 VLANeXt 架构中都超过了 Muon 和 AdamW；摘录没有给出完整表格数值。
- 在 DROID 设置下、使用 `pi_0.5` 主干的真实 Franka Research 3 机器人上，Pion 提升了三个抓取并放置任务；摘录没有给出具体成功率。
- 在 LIBERO Object 的动作模块比较中，Low-rank Muon 在 AdamW、Muon 和 LRMuon 里成功率最高，但训练时间大约是 AdamW 和 Muon 的 `15x`。
- 在使用 GRPO 和 GMPO、基于 Qwen3-1.7B 和 Qwen3-4B 的 RLVR 后训练中，Pion 在 MATH 和 GSM8K 上超过了 AdamW，而 Muon 崩溃到 `0`；摘录没有给出准确率的具体数值。

## Link
- [https://arxiv.org/abs/2605.19282v1](https://arxiv.org/abs/2605.19282v1)
