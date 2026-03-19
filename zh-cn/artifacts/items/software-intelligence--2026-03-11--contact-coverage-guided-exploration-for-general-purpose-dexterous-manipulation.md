---
source: arxiv
url: http://arxiv.org/abs/2603.10971v1
published_at: '2026-03-11T16:55:49'
authors:
- Zixuan Liu
- Ruoyi Qiao
- Chenrui Tie
- Xuanwei Liu
- Yunfan Lou
- Chongkai Gao
- Zhixuan Xu
- Lin Shao
topics:
- dexterous-manipulation
- reinforcement-learning
- intrinsic-exploration
- contact-aware-learning
- robot-learning
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# Contact Coverage-Guided Exploration for General-Purpose Dexterous Manipulation

## Summary
本文提出 CCGE，一种面向通用灵巧操作的接触覆盖引导探索方法，用“哪些手指接触了物体哪些区域”来驱动强化学习探索。它试图替代高度任务定制的奖励设计，让灵巧手在多类操作任务中更高效地学会有意义的接触策略。

## Problem
- 灵巧操作缺少像 Atari 分数或行走速度那样通用、可复用的默认奖励，现有方法常依赖任务特定的手工奖励和先验，难以跨任务泛化。
- 传统内在奖励多鼓励状态新奇或动力学预测误差，但在灵巧操作里常忽视“接触”这一核心因素，容易学到无关行为，如空中乱动或把物体推开。
- 仅靠接触后奖励又太稀疏，难以在接触发生前提供有效引导，因此需要一种既关注接触、又能在接触前持续导航的通用探索信号。

## Approach
- CCGE把接触表示为：手指上的预定义关键点与物体表面离散区域之间的接触关系，本质上是在统计“哪根手指碰到了物体哪个区域”。
- 方法维护一个按对象状态簇条件化的接触计数器 `C[s,f,k]`，其中 `s` 是通过自编码器+二值化+SimHash 得到的离散对象状态簇，`f` 是手指，`k` 是物体表面区域，用来避免不同任务阶段/姿态之间的计数相互干扰。
- 它同时使用两类奖励：接触后的 count-based 奖励，鼓励罕见的手指-区域接触；以及接触前的 energy-based reaching 奖励，引导手指靠近尚未充分探索的物体区域。
- 为避免训练早期陷入局部路径，作者将两类奖励都改成“只奖励本回合中超过历史最大值的前进”，从而减轻 detachment 和 short-sighted 行为。
- 整体训练仍基于 PPO，探索奖励与任务奖励相加，计数器在训练期间持续累积且不重置。

## Results
- 论文声称在 4 类模拟灵巧操作任务上验证了方法：cluttered object singulation、constrained object retrieval、in-hand reorientation、bimanual manipulation。
- 作者明确宣称 CCGE 在这些任务上“持续取得更高成功率和更快收敛”，并且在 hard exploration 任务（如 constrained object retrieval）中基线方法会失败，而 CCGE 仍表现强劲。
- 论文还声称，CCGE 学到的接触模式能够稳健迁移到真实机器人系统；实验平台包括 xArm + 16-DOF LEAP Hand。
- 文本摘录未给出具体数值指标，因此无法准确列出 success rate、sample efficiency 提升幅度、数据集上百分比增益或与各 baseline 的定量差距。
- 已给出的较具体实验范围包括：in-hand reorientation 使用 ContactDB 对象，bimanual manipulation 涉及 ARCTIC 数据集中的开盒/开盖任务。

## Link
- [http://arxiv.org/abs/2603.10971v1](http://arxiv.org/abs/2603.10971v1)
