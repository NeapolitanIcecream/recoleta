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
这篇文章认为，Kotlin Multiplatform 通过在 iOS、Android，有时也包括 web 之间共享业务逻辑，同时保留原生 UI，帮助公司减少重复的移动端工作。证据来自 JetBrains 和 Touchlab 客户的案例说法，而不是受控研究评估。

## 问题
- 独立的 iOS 和 Android 代码库会重复业务逻辑，造成平台之间的功能滞后，并提高维护成本。
- 重复逻辑会增加回归风险，因为修复和规则变更必须实施和验证不止一次。
- 平台专属团队会拖慢入职速度，降低人员调配灵活性，也让跨平台产品发布更难协调。

## 方法
- 使用 Kotlin Multiplatform，把业务逻辑、数据模型和计算放在一个共享的 Kotlin 模块中，同时让各个平台保留自己的原生 UI。
- 先编写并验证核心逻辑，再把这段共享代码连接到 iOS、Android，在某些情况下也连接到 web 前端。
- 先在纯逻辑、重业务规则和数据处理的领域做试点，文章估计这些地方大约有 75% 的共享潜力。
- 文中给出的机制很直接：核心规则只实现一遍，就能减少重复编码、重复测试和平台偏移。

## 结果
- 文章说许多组织会在 **3–6 个月**内看到 ROI，但没有提供研究设计、样本量或基准方法。
- 据称 **Blackstone** 在 **6 个月内**实现了 **50% 的实施速度提升**，同时共享了约 **90% 的业务逻辑**。
- 据称 **Duolingo** 为在 Adventures 中采用 KMP 并交付 iOS 花了 **5 个工程月**，随后用同一套 KMP 代码库交付 web 又花了 **1.5 个工程月**，而最初的 Android 实现花了 **9 个工程月**；文章还声称节省了 **6–12 个工程月**。
- 据称 **Bitkey** 用 KMP 共享了其移动端代码库的 **95%**。
- 据称 **Forbes** 在各个平台间整合了 **80%+** 的逻辑，整体业务逻辑共享率约 **90%**。
- 据称 **Philips** 将跨平台功能开发时间缩短了约 **50%**，文章还声称入职时间通常会下降 **30–50%**。

## Problem

## Approach

## Results

## Link
- [https://blog.jetbrains.com/kotlin/2026/04/helping-decision-makers-say-yes-to-kmp/](https://blog.jetbrains.com/kotlin/2026/04/helping-decision-makers-say-yes-to-kmp/)
