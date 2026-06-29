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
language_code: en
---

# Helping Decision-Makers Say Yes to Kotlin Multiplatform (KMP)

## Summary
This post argues that Kotlin Multiplatform helps companies cut duplicate mobile work by sharing business logic across iOS, Android, and sometimes web while keeping native UI. The evidence is a set of case-study claims from JetBrains and Touchlab clients rather than a controlled research evaluation.

## Problem
- Separate iOS and Android codebases duplicate business logic, create feature lag between platforms, and raise maintenance cost.
- Duplicated logic increases regression risk because fixes and rule changes must be implemented and verified more than once.
- Platform-specific teams can slow onboarding, reduce staffing flexibility, and make cross-platform product launches harder to coordinate.

## Approach
- Use Kotlin Multiplatform to place business logic, data models, and calculations in a shared Kotlin module while each platform keeps its native UI.
- Build and verify the core logic once, then connect that shared code to iOS, Android, and in some cases web front ends.
- Start with a pilot in pure logic-heavy areas such as calculations, business rules, and data handling, where the article estimates about 75% sharing potential.
- The claimed mechanism is simple: one implementation of core rules reduces duplicate coding, duplicate testing, and platform drift.

## Results
- The post says many organizations see ROI in **3–6 months**, but it does not provide a study design, sample size, or a benchmark method.
- **Blackstone** reportedly achieved a **50% increase in implementation speed within 6 months** while sharing about **90% of business logic**.
- **Duolingo** reportedly spent **5 engineer-months** to adopt KMP and ship iOS for Adventures, then **1.5 engineer-months** to ship web using the same KMP codebase, compared with **9 engineer-months** for the initial Android implementation; the article also claims **6–12 engineer-months saved**.
- **Bitkey** reportedly shares **95% of its mobile codebase** with KMP.
- **Forbes** reportedly consolidated **80%+ of logic** across platforms and about **90% of business logic** overall.
- **Philips** reportedly cut cross-platform feature development time by about **50%**, and the post also claims onboarding time often drops by **30–50%**.

## Link
- [https://blog.jetbrains.com/kotlin/2026/04/helping-decision-makers-say-yes-to-kmp/](https://blog.jetbrains.com/kotlin/2026/04/helping-decision-makers-say-yes-to-kmp/)
