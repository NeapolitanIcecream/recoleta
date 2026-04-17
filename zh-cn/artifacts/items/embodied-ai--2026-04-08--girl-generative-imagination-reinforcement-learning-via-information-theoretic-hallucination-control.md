---
source: arxiv
url: http://arxiv.org/abs/2604.07426v1
published_at: '2026-04-08T17:14:21'
authors:
- Prakul Sunil Hiremath
topics:
- model-based-rl
- world-models
- imagination-rollouts
- dexterous-manipulation
- visual-grounding
relevance_score: 0.73
run_id: materialize-outputs
language_code: zh-CN
---

# GIRL: Generative Imagination Reinforcement Learning via Information-Theoretic Hallucination Control

## Summary
## 摘要
GIRL 是一种基于模型的强化学习方法，目标是在长时间跨度下让想象 rollout 更接近真实动力学。它加入了一个外部 grounding 信号和一个自适应 KL trust region，并在控制与操作基准上报告了比 DreamerV3 和 TD-MPC2 更高的样本效率和更低的 rollout 漂移。

## 问题
- DreamerV3 这类潜在世界模型强化学习方法会在想象 rollout 中训练策略，但微小的模型误差会随时间累积，把想象状态推离真实环境中见过的数据分布。
- 这种漂移在长时程、稀疏奖励、接触丰富和视觉干扰强的任务上影响最大，因为错误的想象状态会带来错误的价值估计，并削弱真实环境中的策略表现。
- 标准的 KL 正则通常由固定日程控制，因此无法在模型不确定，或想象 rollout 开始偏离真实经验时及时调整。

## 方法
- GIRL 在潜在状态转移先验中加入了一个来自冻结 DINOv2 编码器的 grounding 向量。直白地说，世界模型会从一个预训练视觉模型那里得到对当前观测含义的第二个判断。
- 它用 gated residual 将这个 grounding 注入转移先验，并训练一个小型 projector，通过 L2 cross-modal consistency loss 约束想象潜变量与 grounding 信号在语义上保持一致。
- GIRL 用自适应 trust-region bottleneck 取代固定的 KL 权重。它根据 Expected Information Gain 和来自真实转移的 Relative Performance Loss 信号，更新允许的漂移范围和 KL 乘子。
- 对于没有图像的本体感觉任务，ProprioGIRL 用基于近期关节状态历史的 masked state autoencoder 替代 DINOv2，从本体感觉输入中提供同类锚点。
- 论文还给出了 value-gap 分析，通过 Performance Difference Lemma 和 Integral Probability Metrics 将 I-ELBO 目标与 regret 关联起来。

## 结果
- 在 8 个 DeepMind Control 任务上、3e6 个环境步时，GIRL 报告的 IQM 为 **0.81**，95% CI 为 **[0.77, 0.84]**；DreamerV3 为 **0.67 [0.63, 0.71]**，TD-MPC2 为 **0.71 [0.67, 0.75]**。
- 在同一 DMC 基准上，GIRL 报告的 DFM(1000) 为 **2.14**，DreamerV3 为 **4.81**，TD-MPC2 为 **3.47**。论文称，相比 DreamerV3，潜在 rollout 漂移在无干扰任务上下降了 **38–61%**，在 distractor 任务上下降了 **49–68%**。
- 在 DMC 上，GIRL 相对 DreamerV3 的 Probability of Improvement 为 **0.74 [0.70, 0.78]**。在 distractor 任务中，相对 DreamerV3 的 IQM 差距从无干扰任务中的 **0.10** 扩大到 **0.22**。
- 在 3 个 Adroit 任务上、3e6 步时，ProprioGIRL 报告的 IQM 为 **0.63 [0.58, 0.68]**；DreamerV3 为 **0.44 [0.39, 0.49]**，TD-MPC2 为 **0.58 [0.53, 0.63]**。DFM(500) 为 **2.28**，DreamerV3 为 **3.92**，TD-MPC2 为 **2.81**。
- 论文称，在 horizon **>= 500** 的任务上，GIRL 以 **40–55% 更少的环境步数**获得了更高的渐近回报。
- 在计算成本方面，distilled-prior 变体将 DINOv2 的额外开销从墙钟时间的 **22%** 降到 **4% 以下**，使其运行时间更接近原始 DreamerV3。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07426v1](http://arxiv.org/abs/2604.07426v1)
