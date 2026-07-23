---
source: arxiv
url: https://arxiv.org/abs/2607.19749v1
published_at: '2026-07-22T04:46:49'
authors:
- Gurp Nijjer
topics:
- continual-reinforcement-learning
- model-based-reinforcement-learning
- world-models
- policy-rehearsal
- imagination-based-learning
- catastrophic-forgetting
relevance_score: 0.58
run_id: materialize-outputs
language_code: zh-CN
---

# The World Model Remembers, the Actor Forgets: Dream Rehearsal for Continual Model-Based RL

## Summary
## 摘要
论文指出，在 DreamerV3 风格的持续性基于模型的强化学习中，经验回放能够保留世界模型，但 actor 会忘记如何使用它。论文提出“梦境演练”（graded dream rehearsal），通过对高评分的想象轨迹进行行为克隆来训练 actor，并在不使用任务标签、不增加参数、演练期间不与环境额外交互的情况下保留技能。

## 问题
- 即使使用无界经验回放缓冲区，DreamerV3 agent 在按顺序训练任务时仍可能灾难性遗忘较早的任务。
- 基于标准回报的评估无法说明遗忘究竟来自世界模型知识退化、表征退化，还是 actor 行为退化。
- 这一问题很重要，因为保护回放经验和世界模型准确性并不一定能保留可执行技能。

## 方法
- 在使用三个随机种子的 MiniGrid 任务链上探测 DreamerV3 的各个组件，比较保留的奖励辨别能力、价值估计、终止预测、表征和 actor 行为。
- 冻结世界模型，并分别使用基于想象的标准强化学习或监督式自模仿训练 actor，以隔离技能恢复所依赖的通道。
- 使用梦境演练：从缓冲状态开始进行想象 rollout，利用世界模型的奖励、持续性和价值头进行评分，然后对排名前 25% 的轨迹进行行为克隆，并使用同一个共享 actor。
- 使用“已实现结果优先”且考虑终止状态的评分规则，使已经获得的奖励优先于仅由评论家预测的回报，并防止终止后的模型预测污染筛选结果。

## 结果
- 在从不清空的回放设置下，被遗忘任务的奖励辨别能力保留比率为 0.99、1.06 和 1.01；评论家价值从 0.84 上升到 0.91，终止辨别能力保持在 0.95–1.0，但 actor 行为仍然崩溃。
- 在世界模型冻结且使用相同想象数据的条件下，基于想象的标准强化学习在 0/3 个种子中恢复了遗失技能；监督式自模仿在 3/3 个种子中恢复了该技能，所需更新次数为 2,000–7,500 次，且没有新增环境步数。
- 在四任务 MiniGrid 任务链上，梦境演练在 3/3 个种子中通过了全部任务，而普通回放为 0/3；历史上最弱的任务平均保留率为 0.824，而存储策略隔离参考的结果为 0.62 ± 0.13。
- 在最弱任务上，梦境演练优于匹配的、经过能力筛选的真实轨迹克隆：平均保留率分别为 0.815 和 0.684，配对差值为 +0.131，bootstrap 95% 置信区间为 [0.073, 0.238]；两种方法在所有任务上的通过率均为 3/3。
- 修正后的评分规则在测试的两个任务配置上均达到选择 AUC 1.0 和前四分位纯度 1.0；八任务链在 3/3 个种子中保留了全部任务。该研究使用的是 MiniGrid 上的 1,700 万参数 agent，因此尚未测试其在更大领域中的泛化能力。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.19749v1](https://arxiv.org/abs/2607.19749v1)
