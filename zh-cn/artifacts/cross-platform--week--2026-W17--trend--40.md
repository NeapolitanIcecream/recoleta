---
kind: trend
trend_doc_id: 40
granularity: week
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-27T00:00:00'
topics:
- kotlin-multiplatform
- cross-platform-mobile
- native-ui
- engineering-roi
- web-reuse
run_id: materialize-outputs
aliases:
- recoleta-trend-40
tags:
- recoleta/trend
- topic/kotlin-multiplatform
- topic/cross-platform-mobile
- topic/native-ui
- topic/engineering-roi
- topic/web-reuse
language_code: zh-CN
---

# Kotlin Multiplatform 以一个具体但带宣传性质的移动代码共享案例支撑了本周

## Overview
本周有一个可以发布的研究信号，但范围较窄：Kotlin Multiplatform 被作为一种降低移动交付成本、让 iOS 和 Android 保持同步的实用途径来推广。证据来自一篇与 JetBrains 有关的案例文章，因此它适合作为采用论证，而不是严格的基准评测。与前一周覆盖范围更广的框架和工具更新相比，这一周的内容更具体，但只建立在单一来源之上。

## Clusters

### 共享逻辑与原生 UI
本周唯一可靠的信号是一个关于 Kotlin Multiplatform（KMP）的商业论证。核心主张很直接：在 iOS 和 Android 之间共享业务逻辑，保留原生 UI，并减少重复的工程工作。来源带有宣传性质，但这个说法足够具体，值得规划移动架构的团队关注。

#### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 条目内容说明了在保留原生 UI 的同时共享逻辑，并将其与更低的总成本联系起来。

### 速度与回报主张
这篇文章主要强调交付速度和回报周期。文中称，KMP 让团队为两端共用一套业务规则实现，从而减少移动平台之间的功能滞后。文章还称，许多组织会在三到六个月内看到回报，并建议先在计算、数据模型和其他纯业务逻辑上做试点。这些数字来自与供应商相关的材料，因此更适合看作采用推广信息，而不是独立测量。

#### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 条目内容描述了功能一致性，以及一套业务规则实现可供两端共用。

### 复用扩展到 Web 交付
这些案例不只限于移动应用。一个案例称，现有且经过测试的 KMP 代码很容易从 JavaScript 调用。另一个案例称，一家媒体公司用更小的团队，把一个 KMP 身份 SDK 用在 Android、iOS 和 Web 上。这让它的吸引力从移动代码共享扩大到更广的产品复用，尽管证据仍然主要是轶事。

#### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 条目内容提到了 JavaScript 复用和跨平台 SDK 部署。
