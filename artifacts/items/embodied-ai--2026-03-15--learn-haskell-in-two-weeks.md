---
source: hn
url: https://mercury.com/blog/learn-haskell-in-two-weeks
published_at: '2026-03-15T22:28:07'
authors:
- cosmic_quanta
topics:
- haskell
- programming-pedagogy
- exercise-driven-learning
- feedback-loops
- developer-onboarding
relevance_score: 0.01
run_id: materialize-outputs
---

# Learn Haskell in Two Weeks

## Summary
这篇文章介绍了 Mercury 为新工程师设计的两周 Haskell 入职训练计划 LHbE，核心主张是“练习优先于讲解、反馈密度决定学习速度”。它不是研究论文，而是一份基于企业内部实践的教学方法总结。

## Problem
- 文章要解决的问题是：**如何让没有 Haskell 背景的新员工在仅 10 个工作日内达到可在真实后端代码库中高效工作的水平**。
- 这很重要，因为 Mercury 的后端依赖 Haskell；如果新员工学习曲线过陡，会拖慢上手速度、影响代码质量，也增加导师负担。
- 作者还强调传统做法（读书、听课、长篇讲解）容易让学习者停留在“看懂了但不会做”，因此需要一种更高效、更可操作的训练流程。

## Approach
- 核心机制是一个**完全以练习驱动**的两周课程：10 组按顺序排列的练习，覆盖从类型签名、Maybe/Either、IO、类型类，到 Functor/Applicative/Monad，再到 monad transformer stacks。
- 方法上强调**几乎不使用长篇教材或讲座**，而是通过 worked example + 大量渐进式练习，让学习者在真实编码中形成心智模型。
- 训练配套了**一对一每日导师辅导**，导师尽量不直接给答案，而通过苏格拉底式提问避免“stealing learning”，迫使学习者自己推理。
- 文章提出一个**分层反馈体系**：即时类型检查、15 秒内的类型错误反馈、1 分钟内 Hoogle 查询、5 分钟内 LLM/搜索、15 分钟内导师答疑，再加上测试、PR review 和每日 call 形成闭环。
- 在认知层面，课程特别强调**通过类型进行推理**、主动暴露不确定性、持续自检和利用工具（Hoogle、GHCi、typed holes）来缩短反馈回路。

## Results
- 过去 **6 个月**内，该项目已用于 **50+ 名学习者**，对象覆盖 **interns、managers、senior engineers**，说明方法被较广泛内部采用。
- 课程标准节奏是 **10 个工作日完成 10 组练习**；作者称学习者通常能在 **10 个工作日内学到 monad transformer stacks**。
- 文中给出一个具体案例：**一名实习生在 8 天内完成**整个 LHbE。
- 作者称他们设计了一个**10 分钟以内**的 Haskell placement test，用于已有基础员工的快速分流。
- 没有提供严格实验指标、对照组、通过率、测试分数或生产力提升等定量评测；最强的具体主张是：**移除配套书籍后，学习结果有所改善**，以及大量快速反馈能显著提升学习速度。

## Link
- [https://mercury.com/blog/learn-haskell-in-two-weeks](https://mercury.com/blog/learn-haskell-in-two-weeks)
