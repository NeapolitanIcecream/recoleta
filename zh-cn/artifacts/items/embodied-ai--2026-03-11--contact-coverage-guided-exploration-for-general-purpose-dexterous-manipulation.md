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
- contact-modeling
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Contact Coverage-Guided Exploration for General-Purpose Dexterous Manipulation

## Summary
本文提出 CCGE，一种面向通用灵巧操作的接触覆盖引导探索方法，用“哪些手指接触了物体哪些区域”来产生任务无关的探索奖励。其目标是在缺少手工奖励设计时，让灵巧手更高效地学会有意义的接触策略，并支持仿真到真实系统迁移。

## Problem
- 灵巧操作缺少像游戏分数或速度跟踪那样可复用的默认奖励，现有方法往往依赖任务特定的手工 shaping 或先验。
- 通用探索方法若只奖励状态新颖性或动力学预测误差，常会鼓励与操作无关的行为，例如空中乱动或把物体推走，而不是建立有效接触。
- 对灵巧手而言，真正关键的是**接触模式探索**：不同手指在不同任务阶段接触物体不同区域，这决定了后续能否抓取、重定位或双手协作。

## Approach
- 将接触状态表示为“手指 keypoints 与物体表面区域的交集”，并统计在不同对象状态簇下，手指-区域对的接触计数；越少见的接触模式奖励越高。
- 用学习式哈希把当前/目标物体状态离散成状态簇，为每个簇维护独立接触计数器，避免在一个状态下学到的接触模式抑制另一状态下的探索。
- 设计两个互补奖励：接触后用 count-based contact coverage reward 鼓励新颖手指-区域接触；接触前用 energy-based reaching reward 引导手指靠近未充分探索的物体区域。
- 为避免训练早期陷入局部路径，作者只奖励单回合内“超过历史最佳”的接触/能量进展，从而抑制 detachment 和短视振荡。

## Results
- 论文声称在 4 类模拟灵巧操作任务上验证了 CCGE：cluttered object singulation、constrained object retrieval、in-hand reorientation、bimanual manipulation。
- 文中明确结论是：CCGE 在这些任务上相较现有探索方法实现了**更高成功率**和**更快收敛/更高样本效率**；图 4 还特别指出在 **Constrained Object Retrieval** 这类“hard exploration”任务中，基线方法会失败而 CCGE 表现更强。
- 作者还声称，CCGE 学到的接触模式能够**稳健迁移到真实机器人系统**，并在真实世界中保持有效接触行为。
- 该摘要/节选**未给出具体数值指标**（如成功率百分比、训练步数、具体基线提升幅度），因此无法准确列出 metric/dataset/baseline 的定量对比数字。最强的具体主张是：在多任务、多阶段接触丰富的灵巧操作中，CCGE 一致优于已有探索方法，并且支持 sim-to-real 转移。

## Link
- [http://arxiv.org/abs/2603.10971v1](http://arxiv.org/abs/2603.10971v1)
