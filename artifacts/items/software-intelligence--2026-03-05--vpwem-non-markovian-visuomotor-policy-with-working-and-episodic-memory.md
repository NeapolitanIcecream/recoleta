---
source: arxiv
url: http://arxiv.org/abs/2603.04910v1
published_at: '2026-03-05T07:52:50'
authors:
- Yuheng Lei
- Zhixuan Liang
- Hongyuan Zhang
- Ping Luo
topics:
- robot-imitation-learning
- visuomotor-policy
- long-term-memory
- diffusion-policy
- non-markovian-control
relevance_score: 0.24
run_id: materialize-outputs
---

# VPWEM: Non-Markovian Visuomotor Policy with Working and Episodic Memory

## Summary
VPWEM提出一种面向机器人模仿学习的非马尔可夫视觉-运动策略，把短期工作记忆与长期情节记忆结合起来，以低而近似常数的每步开销利用整段轨迹历史。它主要针对需要长期记忆的操作任务，在保持实时性的同时提升成功率。

## Problem
- 现有视觉-运动策略通常只看单帧或很短历史，难以处理需要记住早期关键信息的非马尔可夫任务。
- 直接把历史窗口做长会带来高计算/显存成本（如注意力随序列长度增长），也更容易学到伪相关，导致分布偏移下灾难性失败。
- 机器人实际任务常因部分可观测、环境随机性和长时程子目标而需要长期记忆，因此仅靠短上下文不够。

## Approach
- 用**工作记忆**保存最近的固定长度观测窗口，负责短期局部信息。
- 用一个**Transformer记忆压缩器**把滑出窗口的旧观测递归压缩成固定数量的**情节记忆token**，相当于把长历史浓缩成摘要。
- 压缩器同时对过去的摘要token做自注意力、对历史观测缓存做交叉注意力，从而在固定记忆预算下整合长程依赖。
- 将工作记忆和情节记忆一起作为条件输入到**diffusion policy**中生成动作；压缩器与策略端到端联合训练，使其自动保留任务相关信息、过滤无关历史。
- 推理时维护观测缓存与摘要缓存，因此能以近似常数的每步内存和计算处理整段历史，而不需要不断扩张上下文窗口。

## Results
- 在**MIKASA**记忆密集型操作任务上，VPWEM相对SOTA基线（包括diffusion policies和VLA模型）**提升超过20%**。
- 在**MoMaRT**移动操作基准上，VPWEM取得**平均约5%提升**，相对多种基线更优。
- 在近似马尔可夫的**Robomimic**任务上，作者声称VPWEM与基线**表现相当**，说明额外记忆模块不会明显伤害短记忆任务。
- 方法被实例化到两类扩散策略基线（**DP**与**MaIL**）上，并在三类基准上做了广泛实验。
- 文段未给出更细的逐任务数值表、标准差或具体baseline逐项分数；最明确的量化结论是**MIKASA >20%**、**MoMaRT 平均+5%**。

## Link
- [http://arxiv.org/abs/2603.04910v1](http://arxiv.org/abs/2603.04910v1)
