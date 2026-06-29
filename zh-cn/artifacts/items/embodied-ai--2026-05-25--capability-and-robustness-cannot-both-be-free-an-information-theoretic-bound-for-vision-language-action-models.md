---
source: arxiv
url: https://arxiv.org/abs/2605.25889v3
published_at: '2026-05-25T14:16:57'
authors:
- Jianwei Tai
topics:
- vision-language-action
- robot-policy-robustness
- information-theory
- adversarial-attacks
- openvla
- libero
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Capability and Robustness Cannot Both Be Free: An Information-Theoretic Bound for Vision-Language-Action Models

## Summary
## 摘要
这篇论文提出，VLA 策略的能力和对抗鲁棒性的总和有一个通用的信息论上界。它针对像 OpenVLA 这样的机器人动作策略，也覆盖 token 化、连续、多步和基于编码器的变体。

## 问题
- VLA 模型在干净的机器人基准上表现很好，但在很小的图像扰动下会失效；摘录提到，OpenVLA-7B 在 16/255 的 PGD 攻击下，LIBERO 成功率从 95% 以上降到 5% 以下。
- 现有关于 VLA 攻击和防御的工作报告了经验上的权衡，但没有说明干净能力和攻击鲁棒性是否都能在没有上限的情况下提高。
- 这个问题很重要，因为 VLA 的输出是物理机器人动作，视觉脆弱性会直接造成不安全行为，而不是错一个标签。

## 方法
- 核心上界是：能力加上鲁棒性，最多等于任务熵加攻击信道容量：`I(A*; A_pi) + I(A_pi; A_tilde_pi) - I(A_pi; delta) <= H(A*) + I(X; X_tilde)`。
- 能力指策略动作和 oracle 动作之间的互信息。
- 鲁棒性指干净动作和受攻击动作共享多少信息，同时扣除通过动作输出泄露的攻击信号。
- 证明用到了两次数据处理不等式：动作来自观测，受攻击的动作来自扰动后的观测，所以动作通道携带的信息不会超过观测通道。
- 论文把这个上界扩展到量化的连续动作、最长到 `T` 的多步 rollout，以及用 `I(phi(X); phi(X_tilde))` 表示的编码器特定预算。

## 结果
- 论文报告了 320 个验证单元都没有违反这个上界，覆盖高斯 VLA 代理、带 PGD 和 Square 攻击的 OpenVLA-7B、全部 4 个 LIBERO 套件、最长到 `T=10` 的 horizon，以及两种结构不同的动作头，分别是连续 `L1` 回归和 flow-matching。
- 在闭式高斯代理中，解析 slack 和 MINE 估计的 slack 在 252/252 个单元里都非负；按组后，在 `alpha=0.05` 且经过 Holm-Bonferroni 校正时，52/84 个配置显示显著的正 slack。
- 对 LIBERO 上的 OpenVLA，摘录报告 `H(A*) ≈ 26` nats，而在 `epsilon=4/255` 时，像素/PCA 的 `I(X; X_tilde) ≈ 5,000` nats。
- 论文报告，编码器特定上界在 4 个 LIBERO 套件上、`epsilon in {2,4,8,16}/255` 时，比像素-PCA 上界紧 28 倍到 68 倍。
- 在 `epsilon=8/255` 时，原始 OpenVLA 的编码器特定预算报告为 86 到 142 nats，离散化能力约为 7.5 nats，slack 从大约 `3.7-4.3e3` nats 降到 79 到 134 nats。
- 论文声称有三种可直接从最多 200 个样本中计算的实用诊断：大约 5 分钟的部署前编码器上限、用于防御取证的偏移特征，以及一个与动作头无关的鲁棒性比率 `Rob_disc/Cap_disc`。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.25889v3](https://arxiv.org/abs/2605.25889v3)
