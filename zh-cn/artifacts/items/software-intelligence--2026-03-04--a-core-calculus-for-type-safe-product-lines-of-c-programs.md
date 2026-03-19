---
source: arxiv
url: http://arxiv.org/abs/2603.04013v1
published_at: '2026-03-04T12:51:23'
authors:
- Ferruccio Damiani
- Daisuke Kimura
- Luca Paolini
- Makoto Tatsuta
topics:
- software-product-lines
- type-systems
- c-programming
- preprocessor-variability
- family-based-analysis
relevance_score: 0.42
run_id: materialize-outputs
language_code: zh-CN
---

# A Core Calculus for Type-safe Product Lines of C Programs

## Summary
本文提出了一个面向 C 语言软件产品线的核心形式化框架：LC 用于刻画不含预处理器的 C 子集，CLC 在此基础上加入 `#define/#if` 风格的变体注解，并配套家族式类型系统。其目标是在不枚举所有变体的情况下，静态保证由预处理器生成的所有产品变体都是良类型的 C 程序。

## Problem
- C 软件产品线常通过预处理器指令实现变体，但特性组合数可呈指数爆炸，逐个生成并检查所有变体在实践中不可行。
- 现有工具虽可分析带预处理器的 C 代码，但作者声称缺少一个“真正是 C 子集”的核心演算上、针对该问题的形式化家族式类型检查框架。
- 需要一个既能表达 C 中结构体、指针、堆分配等关键机制，又能证明“所有合法产品都类型安全”的简单理论基础，这对分析和教学都重要。

## Approach
- 提出 **Lightweight C (LC)**：一个形式化的 ANSI C 核心子集，覆盖结构体、指针、条件表达式、表达式序列、结构体成员赋值，以及动态内存分配/释放等机制。
- 提出 **Colored LC (CLC)**：在 LC 上加入特性条件注解，抽象 C 预处理器中的 `#define`、`#if/#ifdef/#ifndef` 风格变体选择。
- 采用 **family-based type checking**：不是为每个产品单独类型检查，而是在共享代码库上结合特性模型与注解信息一次性检查整个产品线。
- 证明性目标是：若一个 CLC 软件产品线可类型检查，则由预处理器生成的所有 LC 变体都可类型检查，从而建立“产品线良类型 ⇒ 全部变体良类型”的保证。
- 用一个带 3 个特性（`LAST`、`OCCURS`、`INTERVAL`）和 6 个产品的队列示例说明如何对 C 代码中的结构定义、函数、参数和表达式进行变体注解。

## Results
- 论文的核心结果是一个**形式化保证**：作者在第 6 节声称证明了，所有由**良类型 CLC SPL** 生成的变体，都是**良类型 LC 程序**。
- 给出的运行示例包含 **3 个特性**、**6 个产品/变体**；作者说明这 6 个示例变体都是 **well-typed LC programs**。
- 论文明确对比了产品数爆炸问题：例如 **64 个特性**对应最多 **2^64** 个产品，Gentoo 统计中提到 **671617 个特性**分布在 **36197 个特性模型**上，对应最多 **2^671617** 个产品；这被用来论证逐变体检查不可行，家族式检查有必要。
- 论文未在摘录中提供实验评测、运行时间、准确率或与现有工具（如 TypeChef）在基准数据集上的定量比较结果。
- 最强的具体主张是：这是作者所知**首个**建立在“C 的真子集核心语言”之上的、针对注解式 C 软件产品线的**家族式类型检查形式化**，并且 LC/CLC 还可作为后续研究堆安全等分析的基础。

## Link
- [http://arxiv.org/abs/2603.04013v1](http://arxiv.org/abs/2603.04013v1)
