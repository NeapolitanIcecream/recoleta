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
- world-models
- experience-replay
- dreamerv3
- catastrophic-forgetting
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# ARROW: Augmented Replay for RObust World models

## Summary
ARROW 是一种面向持续强化学习的模型式方法，通过把回放重点放在世界模型而不是直接放在策略上，用更省内存的双缓冲回放来减轻灾难性遗忘。论文表明，在持续 Atari 和共享结构的 CoinRun 变体中，它能在相同回放内存预算下比基线更稳地保留旧任务能力。

## Problem
- 持续强化学习需要智能体一边学习新任务，一边保留旧任务能力，但常见方法容易出现**灾难性遗忘**。
- 现有高效方法多依赖大规模模型无关回放缓冲区，内存开销大，扩展性差。
- 关键问题是：能否用**更省内存的策略性回放**来训练世界模型，从而同时保留稳定性、可塑性和迁移能力。

## Approach
- 在 DreamerV3 上构建 ARROW：先学习一个**世界模型**预测环境，再用该模型“想象”轨迹训练 actor-critic；也就是先把经验教给模型，再由模型教策略。
- 使用两个互补回放缓冲区：一个**短期 FIFO**保存最新经验，保证当前任务学习；一个**长期 LTDM**缓冲区用 reservoir sampling 保留跨任务的全局分布与多样性。
- 为了让小缓冲区也能覆盖更多行为模式，作者把完整 episode 切成长度 **512** 的 **spliced rollouts** 存储，而不是整局存储。
- 两个缓冲区各存 **2^18 ≈ 262,000** 个观测，总容量 **2^19 = 524,288** 个观测；与 DreamerV3 和 TES-SAC 在**相同内存预算**下比较。
- 方法**不需要任务 ID**，并在无共享结构任务上结合固定熵正则和预设 reward scale 改善探索。

## Results
- **Atari，默认任务顺序（one-cycle）**：ARROW 的 forgetting 为 **0.197**，DreamerV3 为 **1.217**，遗忘降低超过 **6 倍**；同时 ARROW 的 **WC-ACC = 0.615**，高于两个基线的负值表现。
- **Atari，反向任务顺序（one-cycle）**：ARROW 的 forgetting 进一步降到 **0.039**，DreamerV3 为 **1.348**；ARROW 的 **WC-ACC = 0.618**，说明对任务顺序变化也更稳健。
- **Atari，两轮训练（two-cycle）**：ARROW 的 **Max-F = 0.012**，几乎表示在第一次和第二次接触之间**几乎没有最坏遗忘**；DreamerV3 为 **0.735**，TES-SAC 为 **0.089**。
- **Atari，两轮训练（two-cycle）**：ARROW 的 **WC-ACC = 0.388**，而两个基线仍为负值，说明 revisiting 任务时 ARROW 更能恢复并维持旧知识。
- 论文还声称在**无共享结构任务**上，ARROW 相比同等大小回放的模型式/模型无关基线表现出**显著更少的遗忘**，同时保持**可比的 forward transfer**。
- 对 **CoinRun 共享结构任务**，摘要声称也进行了评测并分析前向/后向迁移，但当前给定摘录里**未提供具体量化数字**。

## Link
- [http://arxiv.org/abs/2603.11395v1](http://arxiv.org/abs/2603.11395v1)
