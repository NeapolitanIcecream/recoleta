---
source: arxiv
url: http://arxiv.org/abs/2603.11395v1
published_at: '2026-03-12T00:15:11'
authors:
- Abdulaziz Alyahya
- Abdallah Al Siyabi
- Markus R. Ernst
- Luke Yang
- Levin Kuhlmann
- Gideon Kowadlo
topics:
- continual-rl
- world-model
- dreamerv3
- replay-buffer
- catastrophic-forgetting
relevance_score: 0.63
run_id: materialize-outputs
language_code: zh-CN
---

# ARROW: Augmented Replay for RObust World models

## Summary
ARROW 是一种面向持续强化学习的模型式方法：它把重放重点放在世界模型而非直接放在策略上，并用更省内存的双缓冲机制减少灾难性遗忘。论文表明，在 Atari 这类任务共享结构很弱的连续任务序列中，ARROW 比 DreamerV3 明显更稳健，同时保持接近的前向迁移能力。

## Problem
- 持续强化学习需要智能体**不断学新任务而不忘旧任务**，但常见方法会出现灾难性遗忘。
- 现有高效方法常依赖**大规模 replay buffer** 来缓解遗忘，带来明显的内存与扩展性问题。
- 关键问题是：**能否用更省内存、且更有策略的重放方式训练世界模型，从而在持续学习中兼顾稳定性与可塑性？**

## Approach
- ARROW 基于 **DreamerV3**：先训练一个 **World Model** 来预测环境与奖励，再用模型“想象”出的轨迹训练 actor-critic。
- 核心机制是 **双重 replay buffer**：一个短期 FIFO 缓冲区保留最近经验；一个长期 **global distribution matching** 缓冲区保留跨任务更有代表性的历史样本。
- 长期缓冲区用 **reservoir sampling** 维护全局分布覆盖，目标是在有限容量下尽量保留任务多样性，而不是只记住最近数据。
- 为了在小 buffer 下存更多不同轨迹，论文不存完整 episode，而是把经验切成 **长度 512 的 spliced rollouts**；训练时从两类 buffer 并行均匀采样。
- 在相同总内存预算下，ARROW 使用两个各含 **2^18 ≈ 262k observations** 的 buffer，总容量 **2^19 = 524,288 observations**，与 DreamerV3 / TES-SAC 的单 buffer 预算匹配。

## Results
- **Atari / 默认任务顺序 / one-cycle**：ARROW 的 forgetting 为 **0.197**，DreamerV3 为 **1.217**，约 **6 倍以上更低**；同时 ARROW 的 **WC-ACC = 0.615**，明显优于两种基线（文中称基线为负值）。
- **Atari / 反向任务顺序 / one-cycle**：ARROW 的 forgetting 进一步降到 **0.039**，而 DreamerV3 为 **1.348**；ARROW 的 **WC-ACC = 0.618**，再次为最好。
- **Atari / two-cycle**：ARROW 的 **Max-F = 0.012**，几乎表示最坏情况下也几乎不忘；DreamerV3 为 **0.735**，TES-SAC 为 **0.089**。同时 ARROW 的 **WC-ACC = 0.388**，而两个基线仍为负值。
- 论文还声称：在 Atari 这类**无共享结构**任务上，ARROW 在显著减少遗忘的同时，**前向迁移与基线大体可比**；DreamerV3 有轻微前向迁移优势，但代价是严重遗忘。
- 评测使用 **5 个随机种子**，图中报告的是 **median 与四分位区间**。
- 对 **CoinRun（共享结构）** 的完整定量结果在给定摘录中未展示，因此无法从提供文本中准确列出其数值结果；但论文明确声称它同时考察了共享结构下的迁移与保留表现。

## Link
- [http://arxiv.org/abs/2603.11395v1](http://arxiv.org/abs/2603.11395v1)
