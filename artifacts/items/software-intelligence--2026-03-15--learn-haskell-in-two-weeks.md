---
source: hn
url: https://mercury.com/blog/learn-haskell-in-two-weeks
published_at: '2026-03-15T22:28:07'
authors:
- cosmic_quanta
topics:
- haskell-training
- active-learning
- developer-education
- feedback-loops
- mentorship
relevance_score: 0.48
run_id: materialize-outputs
---

# Learn Haskell in Two Weeks

## Summary
这篇文章介绍了 Mercury 用于新员工的两周 Haskell 培训项目 LHbE，核心是“只做练习、密集反馈、每日导师辅导”。作者主张，相比书本和讲授，这种以练促学的方法能更快让工程师达到可在真实后端代码库中工作的熟练度。

## Problem
- 要在**仅两周**内让不同背景的新员工掌握足够的 Haskell，能胜任真实的后端/Web 开发任务。
- 传统做法如读书、长篇讲解、被动听课，作者认为会让学习停滞，尤其不利于快速形成解决实际问题的能力。
- Haskell 学习门槛高、概念多、错误反馈复杂，如果没有高频且高质量的反馈，学习者容易卡住或只会“得到答案”而非真正理解。

## Approach
- 设计了一个 **10 个练习集、10 个工作日**的线性训练流程，内容覆盖从类型、Hoogle、GHCi、Maybe/Either 到 Monad 与 monad transformer stacks，并穿插真实代码库任务，如新增路由、JSON Handler、测试和数据库模型。
- 采用**纯练习驱动**：不用书、不上课、几乎不提供长篇材料；每个模块先给一个 worked example，再通过 20–30 个渐进式练习巩固概念。
- 建立**分层反馈体系**：即时类型检查、15 秒内看类型错误、1 分钟内用 Hoogle、5 分钟内可问 LLM/搜索、15 分钟内联系导师；再叠加测试、PR review、每日 30 分钟一对一导师通话。
- 导师以**苏格拉底式提问**为主，尽量避免“替学员思考”或直接给答案，重点训练基于类型推理、主动查找信息、检查自己工作和表达不确定性的能力。
- 训练目标不是灌输固定知识点，而是培养可迁移的技能：尤其是**reasoning with types**、使用工具链（Hoogle/GHCi/typechecker）和在未知问题中保持学习主动性。

## Results
- 过去 **6 个月**内，该项目已用于 **50+ 名学习者**，覆盖从实习生到经理、资深工程师的广泛人群。
- 学员通常在 **10 个工作日**内推进到 **monad transformer stacks**；文中明确称“learners routinely reach the topic of monad transformer stacks within 10 business days”。
- 项目配有一个 **少于 10 分钟**的分级测试，用于识别已有 Haskell 能力并提供加速版本，减少已掌握内容上的时间浪费。
- 有实例显示学习速度可更快：一名实习生在 **8 天**内完成 LHbE；作者还提到有人第一天甚至不知道 `Double`，仍可完成项目。
- 文中**没有提供严格对照实验、标准化数据集或正式基线指标**，因此没有可报告的 accuracy/F1/pass@k 之类量化结果。
- 最强的具体主张是：移除配套书本后“outcomes improved”，且作者认为高强度主动练习 + 丰富反馈是新员工“super quickly”获得 Haskell fluency 的关键，但这主要基于内部经验总结而非正式实验验证。

## Link
- [https://mercury.com/blog/learn-haskell-in-two-weeks](https://mercury.com/blog/learn-haskell-in-two-weeks)
