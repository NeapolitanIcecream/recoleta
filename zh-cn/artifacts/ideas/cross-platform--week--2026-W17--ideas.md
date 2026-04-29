---
kind: ideas
granularity: week
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-27T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- kotlin-multiplatform
- cross-platform-mobile
- native-ui
- engineering-roi
- web-reuse
tags:
- recoleta/ideas
- topic/kotlin-multiplatform
- topic/cross-platform-mobile
- topic/native-ui
- topic/engineering-roi
- topic/web-reuse
language_code: zh-CN
---

# 共享业务逻辑层

## Summary
本周支持一小组具体的 Kotlin Multiplatform 动作，核心都围绕共享业务逻辑，同时保留原生 UI。近期最可信的用法，是在逻辑密集的模块中做试点，尤其适用于功能一致性和重复测试已经成为当前痛点的场景。同一来源也提供了足够多的细节，可以进一步考虑围绕单一共享规则层组织发布流程；如果更谨慎一些，也可以评估一个跨移动端和 web 的账户逻辑复用 SDK。所有证据都来自一篇与 JetBrains 相关的案例文章，因此它更清楚地说明了运营模式，而不是提供严谨的基准比较。

## 面向 iOS 和 Android 功能一致性的共享业务逻辑试点
对于同时维护 iOS 和 Android 重复逻辑的团队，围绕计算、业务规则和数据模型开展一个小范围的 Kotlin Multiplatform 试点，是当前最明确的下一步。来源文章认为，功能不同步的一个原因是同一套规则需要维护两遍，并给出了一个可操作的起点：把纯业务逻辑放进一个共享的 Kotlin 模块里，而每个应用继续保留原生 UI。这个范围足够小，可以先在一个产品领域试验，也足够具体，便于衡量结果。一个有用的试点应跟踪两件事：共享实现是否减少了移动团队之间的重复返工，以及 bug 修复和规则变更是否能同时落到两个平台上。支撑证据与供应商相关，应视为 adoption messaging，但它清楚指出了 KMP 最容易先在哪些部分试用，以及它针对哪些运营痛点。

### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 直接说明了运营痛点：重复的业务逻辑会造成功能不同步，而一套经过验证的共享实现可以同时供两个平台使用。
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 建议先在计算、数据模型和业务规则上做试点，并明确估计了可共享的比例。

## 围绕单一业务规则模块的共享发布规划
对于经常无法在同一天发布 iOS 和 Android 版本的团队，围绕一个共享逻辑层建立跨平台发布流程，现在看起来更可行了。文章中的案例说法把 KMP 采用与首次实现完成后的后续交付提速联系起来：据称，Duolingo 在 Android 之后复用了同一套 KMP 代码库发布 iOS，随后又用少得多的工程时间发布了 web；Philips 的跨平台功能开发时间据称减少了约一半。对移动团队来说，这更像是流程调整，而不只是语言选择。产品、QA 和发布计划可以围绕一套业务规则实现和各平台各自的 UI 对接来安排，并在共享模块边界上衡量功能一致性。证据是轶事性的，但已经具体到足以支持在一个经常出现跨平台漂移的功能族上做一次小规模发布试验。

### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 给出了 Duolingo 后续交付速度和 Philips 功能开发时间的具体案例数字。
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 解释了文中声称的机制：业务规则只构建和测试一次，然后在两个平台上复用，以减少功能不同步。

## 跨移动应用和 web 复用的 KMP 身份与账户 SDK
对于需要在移动应用和 web 产品上交付相同流程的公司，一个可复用的 KMP SDK，可用于身份、权益或其他账户逻辑，是一个可信的建设目标。这里最有力的支持来自文章中的 web 复用案例：据称，一个团队把现有、已测试的 KMP 代码暴露给 JavaScript 使用，在移动发布受阻后，三周内把目标转向了 web；另一家媒体公司则在 Android、iOS 和 web 之间复用了一个 KMP Identity SDK，并用更小的团队完成交付。这提示了一个值得在多品牌或多终端产品内部评估的具体支撑层：把通用的账户逻辑打包一次，然后让每个客户端保留自己的 UI 外壳。这适合那些已经同时运营多个应用、拥有相同登录和用户状态规则，并且持续花时间在不同平台之间对齐这些规则的组织。

### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 给出了两个具体复用案例：从 JavaScript 调用已测试的 KMP 代码，以及在 Android、iOS 和 web 上交付一个 KMP Identity SDK，并使用更小的团队。
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): 补充了一个具体的 web 转向案例：在移动发布受阻后，用三周时间完成了转向。
