---
source: rss
url: https://blog.jetbrains.com/kotlin/2026/04/helping-decision-makers-say-yes-to-kmp/
published_at: '2026-04-20T14:39:57'
authors:
- Ekaterina Volodko
topics:
- kotlin-multiplatform
- cross-platform-mobile
- shared-business-logic
- native-ui
- engineering-productivity
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)

## Summary
## 摘要
这篇文章认为，Kotlin Multiplatform 通过在 iOS、Android，有时也包括 Web 之间共享业务逻辑，同时保留原生 UI，帮助公司减少重复的移动端开发工作。文中的证据主要是一组来自 JetBrains 和 Touchlab 客户案例的说法，不是受控研究评估。

## 问题
- 独立的 iOS 和 Android 代码库会重复实现业务逻辑，造成平台之间的功能滞后，并提高维护成本。
- 重复的逻辑会增加回归风险，因为修复和规则变更必须多次实现并验证。
- 按平台划分的团队会减慢新成员上手，降低人员调配灵活性，也让跨平台产品发布更难协调。

## 方法
- 使用 Kotlin Multiplatform 将业务逻辑、数据模型和计算放入共享的 Kotlin 模块，同时各个平台保留原生 UI。
- 核心逻辑只构建和验证一次，再把这部分共享代码接到 iOS、Android，以及某些情况下的 Web 前端上。
- 先在纯逻辑密集的领域做试点，比如计算、业务规则和数据处理。文章估计这些部分大约有 75% 的共享潜力。
- 文中给出的机制很直接：核心规则只保留一份实现，可以减少重复编码、重复测试和平台分化。

## 结果
- 文章称很多组织能在 **3–6 个月**内看到 ROI，但没有提供研究设计、样本量或基准比较方法。
- 据称，**Blackstone** 在 **6 个月**内将实现速度提高了 **50%**，同时共享了大约 **90% 的业务逻辑**。
- 据称，**Duolingo** 采用 KMP 并为 Adventures 发布 iOS 版本用了 **5 个工程师月**，随后基于同一套 KMP 代码库发布 Web 版本用了 **1.5 个工程师月**；相比之下，最初的 Android 实现用了 **9 个工程师月**。文章还称因此节省了 **6–12 个工程师月**。
- 据称，**Bitkey** 通过 KMP 共享了其 **95% 的移动端代码库**。
- 据称，**Forbes** 在各平台之间整合了 **80% 以上的逻辑**，整体上共享了大约 **90% 的业务逻辑**。
- 据称，**Philips** 将跨平台功能开发时间缩短了约 **50%**，文章还称上手时间通常也会下降 **30–50%**。

## Problem

## Approach

## Results

## Link
- [https://blog.jetbrains.com/kotlin/2026/04/helping-decision-makers-say-yes-to-kmp/](https://blog.jetbrains.com/kotlin/2026/04/helping-decision-makers-say-yes-to-kmp/)
