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
- diffusion-policy
- long-term-memory
- non-markovian-policy
- mobile-manipulation
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# VPWEM: Non-Markovian Visuomotor Policy with Working and Episodic Memory

## Summary
本文提出 VPWEM，一种给视觉运动策略加入“工作记忆+情景记忆”的非马尔可夫控制方法，用固定大小记忆摘要长历史。它主要面向需要长期记忆的机器人模仿学习任务，并在多个基准上优于强基线。

## Problem
- 现有视觉运动/扩散策略通常只看单步或很短历史，难以处理需要记住早期信息的**非马尔可夫**机器人任务。
- 直接把上下文窗口拉长会带来高计算与显存开销（如自注意力随序列长度增长），还容易过拟合历史中的伪相关，导致分布偏移下失败。
- 这很重要，因为真实机器人任务常有部分可观测、长时程依赖和多子目标；若策略记不住关键过去信息，就会在操作和移动操作中出错。

## Approach
- VPWEM 把最近的少量观测保留为**working memory**（滑动窗口短期记忆），用于当前局部决策。
- 对超出窗口的旧观测，不再全部丢弃，而是用一个**Transformer contextual memory compressor**递归压缩成固定数量的**episodic memory tokens**。
- 这个压缩器一方面对过去的摘要 token 做自注意力，另一方面对历史观测缓存做交叉注意力，从而把“整段轨迹里重要的信息”浓缩到少量 token 中。
- 压缩器与扩散策略联合端到端训练；动作生成同时条件化于短期工作记忆和长期情景记忆，因此每步推理的内存与计算接近常数。
- 作者将该框架实例化到 diffusion policy baselines（如 DP、MaIL）上，并在训练中用缓存、子采样和梯度截断来降低成本与过拟合。

## Results
- 在 **MIKASA** 记忆密集型操作任务上，VPWEM 相比包括 diffusion policies 和 VLA models 在内的**state-of-the-art baselines 提升超过 20%**。
- 在 **MoMaRT** 移动操作基准上，VPWEM 取得**平均 5% 提升**。
- 在近似马尔可夫的 **Robomimic** 任务上，作者称其表现与基线**大致持平**，说明加入记忆不会明显伤害不太需要长期记忆的场景。
- 文中给出实现与实验设置数字：例如默认短期 token 数 **L=2**、长期 memory token 数 **M=2**、缓存大小 **8**、扩散采样步数 **50**、动作块长度 **H=8**。
- 提供的摘录未包含完整逐任务表格数值、标准差或相对具体基线分项结果，因此无法进一步列出更细粒度定量比较。}

## Link
- [http://arxiv.org/abs/2603.04910v1](http://arxiv.org/abs/2603.04910v1)
