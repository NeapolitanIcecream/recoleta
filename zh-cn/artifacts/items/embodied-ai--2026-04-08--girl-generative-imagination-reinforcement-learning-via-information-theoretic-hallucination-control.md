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
GIRL 是一种基于模型的强化学习方法，目标是在长时间跨度内让想象中的 rollout 尽量贴近真实动力学。它加入了外部锚定信号和自适应 KL 信任区域，并报告在控制和操作基准上，相比 DreamerV3 和 TD-MPC2 有更高的样本效率和更低的 rollout 漂移。

## 问题
- 像 DreamerV3 这样的潜在世界模型强化学习方法，会在想象 rollout 中训练策略，但小的模型误差会随着时间累积，把想象状态推离真实环境中的数据分布。
- 这种漂移在长时程、稀疏奖励、接触密集和视觉干扰任务上最明显，因为糟糕的想象状态会带来糟糕的价值估计和较弱的真实环境策略。
- 标准 KL 正则项通常按固定计划设置，因此它不会根据模型何时不确定，或想象 rollout 何时不再匹配真实经验来调整。

## 方法
- GIRL 从冻结的 DINOv2 编码器中加入一个锚定向量，注入潜在转移先验。简单说，世界模型会从一个预训练视觉模型那里再得到一层对当前观测含义的判断。
- 一个门控残差把这个锚定信号注入转移先验，同时训练一个小型投影器，让想象中的潜变量必须通过 L2 跨模态一致性损失与锚定信号保持语义一致。
- GIRL 用自适应信任区域瓶颈替代固定的 KL 权重。它利用 Expected Information Gain 和来自真实转移的 Relative Performance Loss 信号，更新允许漂移的大小和 KL 乘子。
- 对没有图像的本体感知任务，ProprioGIRL 用一个针对近期关节状态历史的掩码状态自编码器替换 DINOv2，从本体感知输入中提供同类锚定。
- 论文还给出了价值差分析，通过 Performance Difference Lemma 和 Integral Probability Metrics 将 I-ELBO 目标与 regret 联系起来。

## 结果
- 在 8 个 DeepMind Control 任务、3e6 个环境步下，GIRL 的 IQM 为 **0.81**，95% CI 为 **[0.77, 0.84]**；DreamerV3 为 **0.67 [0.63, 0.71]**，TD-MPC2 为 **0.71 [0.67, 0.75]**。
- 在同一 DMC 套件上，GIRL 的 DFM(1000) 为 **2.14**，DreamerV3 为 **4.81**，TD-MPC2 为 **3.47**。论文称，与 DreamerV3 相比，干净任务上的 latent rollout 漂移下降了 **38–61%**，带干扰任务上下降了 **49–68%**。
- GIRL 相比 DreamerV3 在 DMC 上的 Probability of Improvement 为 **0.74 [0.70, 0.78]**。在带干扰任务上，相对 DreamerV3 的 IQM 差距从干净任务上的 **0.10** 扩大到 **0.22**。
- 在 3 个 Adroit 任务、3e6 步下，ProprioGIRL 的 IQM 为 **0.63 [0.58, 0.68]**，DreamerV3 为 **0.44 [0.39, 0.49]**，TD-MPC2 为 **0.58 [0.53, 0.63]**。DFM(500) 为 **2.28**，DreamerV3 为 **3.92**，TD-MPC2 为 **2.81**。
- 论文称，在 horizon **>= 500** 的任务上，最终回报更高，同时需要的环境步数减少了 **40–55%**。
- 在计算开销上，蒸馏后的 prior 变体把 DINOv2 开销从 wall-clock time 的 **22%** 降到 **4% 以下**，让运行时更接近原始 DreamerV3。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07426v1](http://arxiv.org/abs/2604.07426v1)
