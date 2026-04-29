---
kind: ideas
granularity: day
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-21T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- kotlin-multiplatform
- cross-platform-mobile
- shared-business-logic
- engineering-roi
tags:
- recoleta/ideas
- topic/kotlin-multiplatform
- topic/cross-platform-mobile
- topic/shared-business-logic
- topic/engineering-roi
language_code: zh-CN
---

# 跨客户端共享应用逻辑

## Summary
现有证据支持几种范围较窄的 KMP 采用动作，重点是处理重复的移动端逻辑、跨客户端复用，以及更快扩展到 Web。来源只有一篇 JetBrains 托管、基于案例说法的文章，因此最可信的部分是范围受控的试点和内部共享模块，并且要有清楚的前后对比检查，而不是大范围重写的说法。

## 面向共享业务规则和数据模型的 KMP 试点
对于已经分别维护 iOS 和 Android 应用、并持续遭遇重复实现工作的团队，围绕业务规则、计算和数据模型开展 KMP 试点，是近期最清晰的验证方式。这个范围的理由很直接：一个共享的 Kotlin 模块可以承载经常变化的逻辑，而各平台继续保留原生 UI 和各自应用的集成点。来源材料多次把这种模式视为最实际的起点，并给出一个粗略预期：在逻辑密集型领域，共享比例大约可达 75%。

当产品团队已经感受到平台漂移时，这类试点最容易成立，例如定价规则、资格校验、内容门槛、同步逻辑，或其他必须在两个应用中表现一致的功能。文中声称的收益是更快实现功能一致，以及更少的重复测试，因为规则实现只保留在一个地方。这里的证据仍然与供应商相关，且以案例说法为主，所以低成本验证应当保持很窄：选一个规则密集型功能，只把共享核心迁移到 KMP，再把交付时间、缺陷数量和一致性问题与最近一个被做了两遍的功能进行比较。

### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 摘要将“原生 UI + KMP 共享业务逻辑”列为主要采用模式，并建议在逻辑密集型领域开展试点，共享潜力约为 75%。
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 该片段说明，后续平台会把共享的数据模型和逻辑接到原生 UI 上，而一致性和同步发布是操作层面的收益。
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 该片段明确建议从纯业务逻辑开始，例如计算、数据模型和业务规则。

## 跨移动端与 Web 客户端的共享身份与权益 SDK
对于运营多个面向消费者应用、并且不断在各平台重复实现同一套登录、权益或账户状态逻辑的公司，跨平台身份或策略 SDK 是一个具体的构建方向。文章给出一个直接案例：一家全国性媒体公司为 Android、iOS 和 Web 构建了 KMP Identity SDK，团队规模只有平台专属项目常见配置的一半。这让可复用的内部 SDK 比大范围移动端重写更可信。

实际目标是做一个统一负责会话状态、令牌处理、权益校验、账户规则及相关模型的包，然后向各客户端暴露原生绑定。这适合拥有多个品牌应用、订阅产品，或需要让 Web 端与移动端行为一致的组织。第一步验证可以很小，也容易衡量：把一个共享的认证或权益库发布到一个 iOS 应用、一个 Android 应用和一个 Web 客户端，然后跟踪避免了多少重复缺陷修复，以及发布协同耗时。

### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 该片段提到 Forbes 有较高的逻辑共享比例，并提到在移动端之后交付 Web，支持跨客户端复用共享核心逻辑。
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 该片段提到一家全国性媒体公司在 Android、iOS 和 Web 上构建 KMP Identity SDK，且团队更小，这直接支持内部 SDK 的使用场景。
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 摘要指出，KMP 的使用可从移动端扩展到 Web，同时保留原生 UI 层。

## 建立在共享移动端领域逻辑之上的 Web 后备路径
对于那些可能需要在几乎没有预警的情况下，把现有应用流程暴露到 Web 上的移动优先产品团队，基于 Web 的后备路径是一个具体的采用变化。文章给出两个可用信号。Duolingo 据称使用同一套 KMP 代码库，把 Adventures 从 Android 扩展到 iOS，再扩展到 Web，后续投入明显更低；另一家公司据称通过从 JavaScript 调用已经实现并测试过的代码，在三周内把一个移动应用改向到 Web。

这指向一个明确的构建选择：把领域逻辑、校验规则和核心流程放进共享的 KMP 模块，这样当产品、合作方或分发需求变化时，浏览器客户端就可以直接调用它们。处于受监管发布流程、事件驱动上线节奏，或依赖应用商店分发的企业会更先在意这一点。低成本测试方式是：用共享模块把一个现有移动流程暴露到 Web 上，再衡量在核心逻辑复用之后，还剩下哪些部分仍然是平台专属。

### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 该片段给出了 Duolingo 的工程师月数对比，说明其使用同一套 KMP 代码库，把 Android 实现扩展到 iOS 和 Web。
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 该片段提到，一家公司通过从 JavaScript 调用已经实现并测试过的 KMP 代码，在三周内完成了面向 Web 的改向。
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 摘要指出，共享逻辑可覆盖 iOS、Android，有时也可覆盖 Web。
