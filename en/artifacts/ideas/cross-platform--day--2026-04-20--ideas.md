---
kind: ideas
granularity: day
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-21T00:00:00'
run_id: 2aef0884-aa7a-49b3-b6a5-be58376727a5
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
language_code: en
pass_output_id: 78
pass_kind: trend_ideas
upstream_pass_output_id: 77
upstream_pass_kind: trend_synthesis
---

# Cross-client shared application logic

## Summary
The available evidence supports narrow KMP adoption moves tied to duplicated mobile logic, multi-client reuse, and faster web extension. The source is one JetBrains-hosted article built from case-study claims, so the most credible pieces are scoped pilots and internal shared modules with clear before-and-after checks, not broad rewrite claims.

## KMP pilot for shared business rules and data models
A KMP pilot for business rules, calculations, and data models is the clearest near-term test for teams that already ship separate iOS and Android apps and keep hitting duplicate implementation work. The current case for this scope is straightforward: one shared Kotlin module can hold the logic that changes often, while each platform keeps its native UI and app-specific integration points. The source material repeatedly points to this pattern as the practical starting point and even gives a rough sharing expectation of about 75% in logic-heavy areas.

This pilot is easiest to justify where product teams already feel platform drift: pricing rules, eligibility checks, content gating, sync logic, or other features that must behave the same way on both apps. The claimed upside is faster feature parity and less repeated testing because the rule implementation lives in one place. The evidence here is still vendor-linked and anecdotal, so the cheap check is narrow: pick one rule-heavy feature, move only the shared core into KMP, and compare delivery time, defect count, and parity issues against a recent feature built twice.

### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Summary identifies KMP shared business logic with native UI as the main adoption pattern and recommends a pilot in logic-heavy areas with about 75% sharing potential.
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Chunk explains that subsequent platforms connect shared data models and logic to native UI, with consistency and synchronized launches as the operational benefit.
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Chunk explicitly recommends starting with pure business logic such as calculations, data models, and business rules.

## Shared identity and entitlement SDK across mobile and web clients
A cross-platform identity or policy SDK is a concrete build for companies that run several consumer apps and keep re-implementing the same login, entitlement, or account-state logic on each platform. The article includes one direct example of a national media company building a KMP Identity SDK for Android, iOS, and web with a team half the size usually assigned to platform-specific projects. That makes a reusable internal SDK more credible than a broad mobile rewrite.

The practical target is a package that owns session state, token handling, entitlement checks, account rules, and related models once, then exposes native bindings to each client. This fits organizations with multiple brand apps, subscription products, or a web surface that must match mobile behavior. A first validation step is small and measurable: ship one shared auth or entitlements library to one iOS app, one Android app, and one web client, then track duplicate bug fixes avoided and release coordination time.

### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Chunk reports high logic sharing at Forbes and cites web delivery after mobile, supporting reuse of shared core logic across clients.
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Chunk cites a national media company building a KMP Identity SDK across Android, iOS, and web with a smaller team, which directly supports an internal SDK use case.
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Summary states that KMP use extends beyond mobile to web while keeping native UI layers.

## Web fallback path built on shared mobile domain logic
A web fallback path for mobile-first products is a concrete adoption change for teams that may need to expose an existing app workflow on the web with little warning. The article gives two usable signals. Duolingo reportedly used the same KMP codebase to extend Adventures from Android to iOS and then to web with much lower follow-on effort, and another company reportedly retargeted a mobile app to the web in three weeks by calling already implemented and tested code from JavaScript.

This points to a specific build choice: keep domain logic, validation rules, and core flows in a shared KMP module so a browser client can call them when product, partner, or distribution needs change. Teams in regulated rollout paths, event-driven launches, or app-store-dependent businesses would care first. The low-cost test is to expose one existing mobile flow on the web using the shared module and measure what remains platform-specific after the core logic is reused.

### Evidence
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Chunk gives Duolingo's reported engineer-month comparison for extending an Android implementation to iOS and web using the same KMP codebase.
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Chunk reports a three-week retargeting to web by calling already implemented and tested KMP code from JavaScript.
- [Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)](../Inbox/2026-04-20--helping-decision-makers-say-yes-to-kotlin-multiplatform-kmp.md): Summary states that shared logic can cover iOS, Android, and sometimes web.
