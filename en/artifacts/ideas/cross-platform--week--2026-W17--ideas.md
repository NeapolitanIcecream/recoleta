---
kind: ideas
granularity: week
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-27T00:00:00'
run_id: 2aef0884-aa7a-49b3-b6a5-be58376727a5
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
language_code: en
pass_output_id: 92
pass_kind: trend_ideas
upstream_pass_output_id: 91
upstream_pass_kind: trend_synthesis
---

# Shared Business Logic Layer

## Summary
The week supports a small set of concrete Kotlin Multiplatform moves, all centered on shared business logic with native UI preserved. The most credible near-term use is a pilot in logic-heavy modules where feature parity and duplicate testing are current pain points. The same source also gives enough detail to consider a release workflow built around one shared rules layer and, with more caution, a reusable SDK for account logic that spans mobile and web. All of the evidence comes from a JetBrains-linked case-study article, so the operational patterns are clearer than the benchmarking.

## Shared business-logic pilot for iOS and Android feature parity
A narrow Kotlin Multiplatform pilot around calculations, business rules, and data models is the clearest next step for teams with duplicated iOS and Android logic. The source argues that feature lag comes from maintaining the same rules twice, then points to a practical starting scope: one shared Kotlin module for pure business logic while each app keeps its native UI. That scope is small enough to test in one product area and concrete enough to measure. A useful pilot would track two things: whether one shared implementation cuts rework across mobile teams, and whether bug fixes and rule changes land on both platforms at the same time. The supporting evidence is vendor-linked and should be treated as adoption messaging, but it is specific about where KMP is easiest to try first and what operational pain it targets.

### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): States the operational pain directly: duplicated business logic creates feature lag, and a single verified implementation can serve both platforms.
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Recommends a pilot in calculations, data models, and business rules, with an explicit estimate of sharing potential.

## Shared release planning around a single business-rules module
A cross-platform release workflow built around one shared logic layer looks newly practical for teams that keep missing same-day iOS and Android launches. The article’s case-study claims tie KMP adoption to faster follow-on delivery once the first implementation exists: Duolingo reportedly reused the same KMP codebase to ship iOS after Android, then web with much less engineering time, and Philips reportedly cut cross-platform feature development time by about half. For a mobile org, this points to a workflow change more than a language decision. Product, QA, and release planning can center on one implementation of business rules and platform-specific UI hookups, with parity measured at the shared module boundary. The evidence is anecdotal, but it is concrete enough to justify a small release experiment on one feature family that often drifts across platforms.

### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Provides concrete case-study numbers on follow-on delivery speed for Duolingo and feature development time for Philips.
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Explains the claimed mechanism: build and test business rules once, then use them on both platforms to reduce feature lag.

## Reusable KMP identity and account SDK across mobile apps and web
A reusable KMP SDK for identity, entitlement, or other account logic is a credible build target for companies shipping the same flows across mobile apps and web properties. The strongest support here is the article’s web reuse examples: one team reportedly exposed existing tested KMP code to JavaScript to retarget a blocked mobile release to the web in three weeks, and a media company used a KMP Identity SDK across Android, iOS, and web with a smaller team. That suggests a specific support layer worth evaluating inside multi-brand or multi-surface products: package the common account logic once, then let each client keep its own UI shell. This fits organizations that already run several apps with the same sign-in and user-state rules and spend time reconciling them across platforms.

### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Gives two concrete reuse cases: calling tested KMP code from JavaScript and shipping a KMP Identity SDK across Android, iOS, and web with a smaller team.
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Adds a concrete web-retargeting example with a three-week timeline after a mobile release was blocked.
