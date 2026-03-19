---
source: hn
url: https://ritter.vg/blog-telemetry.html
published_at: '2026-03-06T23:44:30'
authors:
- birdculture
topics:
- telemetry
- browser-engineering
- privacy-preserving-measurement
- security-rollout
- performance-optimization
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Telemetry helps. you still get to turn it off

## Summary
This is an empirical technical article whose core argument is: telemetry remains very useful for browser stability, security, performance optimization, and safe releases, while still respecting users' right to turn it off. The article is based mainly on real Firefox engineering cases to show that the claim that “telemetry is useless” does not hold.

## Problem
- The problem the article addresses is: **how to determine whether software telemetry truly has practical value for improving a product**, and why it is worth preserving as an optional mechanism under privacy constraints.
- This matters because complex software like browsers must discover **crashes, hangs, compatibility regressions, and risks during safe rollout** in heterogeneous real-world environments, and test suites plus internal dogfooding are often not enough.
- The article also responds to a common controversy: many users believe telemetry is just “surveillance” and “useless.” The author tries to rebut the “useless” part with engineering examples, rather than denying users the right to disable it.

## Approach
- The core method is simple: **collect technical signals from real user environments**, such as performance, feature usage, crashes, hangs, hardware characteristics, and experiment rollout data, and use them to guide fixes, rollbacks, compatibility handling, and feature tradeoffs.
- The author distinguishes different kinds of “phone-home” behavior: true telemetry sends measurements back to the publisher; by contrast, update checks, Remote Settings, certificate/driver blocklists, and similar mechanisms are more about delivering data to users, so they do not fully count as telemetry.
- On privacy mechanisms, the article mentions that Firefox uses approaches such as **regular telemetry that immediately drops IP addresses, OHTTP, Prio, automatic data deletion, segmented storage, and unlinkable storage** to reduce privacy risk, though it does not claim this is a perfect solution.
- The article mainly uses **case-based argumentation** rather than formal experiments: it shows through multiple Firefox engineering examples how telemetry helps identify hangs, validate risky security changes, assess whether low-usage features can be removed, and choose faster implementation paths.

## Results
- **No systematic, paper-style quantitative experimental results are provided**; there is no unified benchmark, dataset, ablation study, or overall metrics table. The strongest evidence consists of multiple real engineering cases and localized threshold/scale descriptions.
- In the “**anti-fingerprinting canvas noise**” implementation choice, the author claims telemetry showed that **SHA-256 is faster when SHA instruction extensions are available; SipHash is faster without them; or SipHash is better when input is smaller than about 2.5KB**. This choice affects overall performance at the scale of **billions of calls**.
- In the “**kill eval in parent process**” case, the first rollout to **Nightly** immediately caused serious breakage in real user environments; the author then added multiple rounds of telemetry, identified residual eval usage in the wild and dependencies in the userChromeJS community, and thereby achieved a safer compatibility migration. The article **does not provide a failure rate or regression percentage**.
- In the “**Background Hang Reporter**” case, the author says telemetry revealed a specific interaction hang caused by their code, and that after refactoring, “**hang graphs dropped**,” but **does not give the magnitude of the drop**.
- In the “**jar: URI**” and “**XSLT**” cases, the author says telemetry showed that real-web usage was **extremely low / basically nonexistent**, making it reasonable to close the attack surface or push deprecation; however, **no specific usage-share figures are provided**.
- In the “**Resist Fingerprinting**” case, telemetry helped show that although users who manually enabled the feature were very vocal, they were only a “**minute portion of the population**,” which helped avoid having management directly block it; again, **no precise proportion is given**.

## Link
- [https://ritter.vg/blog-telemetry.html](https://ritter.vg/blog-telemetry.html)
