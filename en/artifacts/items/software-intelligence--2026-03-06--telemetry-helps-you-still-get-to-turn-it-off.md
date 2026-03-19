---
source: hn
url: https://ritter.vg/blog-telemetry.html
published_at: '2026-03-06T23:44:30'
authors:
- birdculture
topics:
- telemetry
- browser-engineering
- privacy-engineering
- software-reliability
- security-rollout
relevance_score: 0.34
run_id: materialize-outputs
language_code: en
---

# Telemetry helps. you still get to turn it off

## Summary
This article argues that telemetry is not “useless surveillance,” but an important technical tool in browser engineering for continuously improving stability, security, performance, and release safety; at the same time, the author clearly supports users disabling telemetry according to their own threat model.

## Problem
- The article rebuts a common claim: **telemetry has no practical value and only collects data**.
- For complex software like browsers, without real-world signals, developers have difficulty discovering problems not covered by testing, assessing compatibility risks, or determining whether dangerous/low-usage features can be safely removed.
- This matters because bad releases, performance regressions, or widespread compatibility breakage caused by security hardening directly affect huge numbers of real users.

## Approach
- The core mechanism is simple: **have the software send technical runtime signals back to the developer**, such as performance, feature usage, hang stacks, crash reports, and compatibility behavior, for engineering decisions rather than just product click statistics.
- The author distinguishes “telemetry” from other networked behaviors: update checks, Remote Settings, certificate/add-on/driver blocklists, captive portal detection, etc. are not all part of the telemetry under discussion.
- In Firefox, these signals are used to discover anomalous paths in the real world, verify that high-risk security changes will not “break” Nightly, compare the real-world speed of different implementations, and measure the actual usage of certain features.
- The article also emphasizes privacy-protecting design: for example, regular telemetry immediately discards IPs, OHTTP prevents the server from seeing the IP, Prio enables privacy-preserving computation, and data is automatically deleted, segmented, and stored in a de-linked way; but users should still retain the right to disable it.

## Results
- **There is no systematic benchmark experiment or unified quantitative table**; this is a developer’s experiential case summary rather than an academic paper, so there are no complete comparative numbers on standard datasets or unified metrics.
- For choosing the implementation of “canvas anti-fingerprinting noise,” telemetry helped reach a concrete engineering conclusion: **use SHA-256 when SHA instruction extensions are available; use SipHash when they are not; or use SipHash when the input is smaller than about 2.5KB**. The author stresses that this difference matters at the scale of “**billions of calls**.”
- In the effort to remove `eval` from the parent process, the first rollout to **Nightly** “immediately caused problems in Nightly.” The author then says multiple rounds of telemetry were needed to identify the real-world paths still using `eval` and the ecosystem of user custom scripts, making it possible to redesign it safely and reduce breakage.
- **Background Hang Reporter (BHR)** captured hang stacks on pre-release channels. After refactoring code based on this, the author claims that “**hang graphs dropped**,” meaning hang charts declined significantly, though no specific percentage is provided.
- In **Fission/site isolation** and data minimization work, telemetry was used to confirm that removing cross-origin and device-identifying information did not break user workflows; for disabling `jar:` web exposure, telemetry showed that “**real-web usage was basically nonexistent**,” thereby supporting directly shrinking the attack surface.
- The article also claims telemetry informed decisions around **CRLite, TLS/HTTPS-First/Certificate Transparency rollout, OS sandbox hardening, the case for de-featuring XSLT, Android font allowlist, and estimating the size of the Resist Fingerprinting user population**, but aside from the approximately 2.5KB threshold, it does not provide additional concrete numbers.

## Link
- [https://ritter.vg/blog-telemetry.html](https://ritter.vg/blog-telemetry.html)
